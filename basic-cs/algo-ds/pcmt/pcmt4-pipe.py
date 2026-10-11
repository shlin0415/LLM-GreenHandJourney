#!/usr/bin/env python
# coding: utf-8

# conda activate /mnt/sda/alex/miniconda3/envs/pcmt
# nohup time python pcmt4-pipe.py --input_adata /mnt/sdb/alex/maize-xtma/new-sugar.h5ad --out_pcmtm /mnt/sdb/alex/pcmt/pcmtm-new-sugar.h5ad --out_pcmte /mnt/sdb/alex/pcmt/pcmte-new-sugar.h5ad  --out_pcmt3 /mnt/sdb/alex/pcmt/pcmt3-new-sugar.h5ad  --out_pcmt4 /mnt/sdb/alex/pcmt/pcmt4-new-sugar.h5ad
    parser.add_argument("--out_pcmte", required=True)
    parser.add_argument("--out_pcmt3", required=True)
    parser.add_argument("--out_pcmt4", required=True)

"""
PCMT maize kernel pipeline (memory-safe)

Order:
1. pcmtm
2. pcmte
3. pcmt-3
4. pcmt-4
"""

# pcmtm
import sys
sys.path.append('/mnt/sda/alex/PSCMTrait/')
import PSCMTrait as pcmt
import scanpy as sc

# pcmte
import time
import sys
import os
from math import ceil
from typing import Tuple, Iterable, Optional, Dict, List
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances
from scipy.stats import poisson
import numpy as np
import sys
import argparse
import gc
import scanpy as sc

# pcmt-3
import sys
sys.path.append('/mnt/sda/alex/PSCMTrait/')
import PSCMTrait as pcmt
import scanpy as sc
import pandas as pd
import numpy as np
import pickle

# pcmt-4
import sys
sys.path.append('/mnt/sda/alex/PSCMTrait/')
import PSCMTrait as pcmt
import scanpy as sc
import pandas as pd
import numpy as np
import pickle


def enhance(
        X: np.ndarray,
        target_transcript_count: Optional[int] = 200000,
        max_neighbor_frac: Optional[float] = 0.02,
        pc_var_fold_thresh: Optional[float] = 2.0,
        max_components: Optional[int] = 50,
        k: Optional[int] = None,
        use_double_precision: Optional[bool] = False,
        seed: Optional[int] = 0) -> np.ndarray:
    """Remove technical noise from a scRNA-Seq expression matrix."""
    
    if use_double_precision:
        X = np.array(X, dtype=np.float64, order='C', copy=False)
    else:
        X = np.array(X, dtype=np.float32, order='C', copy=False)

    t0_total = time.time()

    transcript_count = np.median(X.sum(axis=1))
    
    if k is None:
        k = int(ceil(target_transcript_count / transcript_count))

        k_max = int(max_neighbor_frac * X.shape[0])
        if k <= k_max:
            pass
        else:
            k = k_max
    else:
        pass

    # determine number of significant PCs
    sys.stdout.flush()
    
    num_components = determine_num_components(
        X, pc_var_fold_thresh, max_components,
        seed=seed)
    
    # aggregate cells
    X_agg, cell_sizes = knn_aggregate(X, k, num_components, seed=seed)
    
    # denoise using PCA
    D, scores, components, mean = denoise_pca(
        X_agg, num_components, cell_sizes,
        seed=seed)
    
    t1_total = time.time()

    return D, scores, components, mean, cell_sizes

def determine_num_components(
        X: np.ndarray,
        var_fold_thresh: float = 2.0,
        max_components: int = 50,
        seed: int = 0) -> int:
    """Determine the number of significant principal components."""
    
    transcript_count = np.median(X.sum(axis=1))

    # apply PCA to real matrix
    _, real_pca_model = apply_pca(X, max_components, transcript_count, seed)
    
    # simulate pure noise matrix
    np.random.seed(seed)
    mean = normalize(X, transcript_count).mean(axis=0)
    X_noise = np.empty(X.shape, dtype=X.dtype)
    for i in range(X.shape[0]):
        X_noise[i, :] = poisson.rvs(mean)

    # apply PCA to pure noise matrix
    _, random_pca_model = apply_pca(X_noise, max_components, transcript_count, seed)
    var_thresh = var_fold_thresh * random_pca_model.explained_variance_[0]

    # determine number of components
    num_components = np.sum(real_pca_model.explained_variance_ >= var_thresh)
    
    return num_components


def normalize(
        X: np.ndarray,
        transcript_count: float = None) -> np.ndarray:
    """Perform median-normalization."""
    
    num_transcripts = X.sum(axis=1)

    if transcript_count is None:
        transcript_count = np.median(num_transcripts)

    N = ((transcript_count / num_transcripts) * X.T).T
    return N


def ft_transform(X: np.ndarray) -> np.ndarray:
    """Apply the Freeman-Tukey transformation."""
    
    # work around a bug where np.sqrt() says input is invalid for arrays
    # of type np.float32 that contain zeros
    invalid_errstate = 'warn'
    if np.issubdtype(X.dtype, np.float32):
        if np.amin(X) >= 0:
            invalid_errstate = 'ignore'
    with np.errstate(invalid=invalid_errstate):
        T = np.sqrt(X) + np.sqrt(X + 1)
    
    return T


def apply_pca(
        X, num_components: int = 50,
        transcript_count = None,
        seed: int = 0) -> Tuple[np.ndarray, PCA]:
    """Apply principal component analysis."""
    
    pca_model = PCA(
        n_components=num_components,
        svd_solver='randomized',
        random_state=seed)
    
    X_trans = ft_transform(normalize(X, transcript_count))
    scores = pca_model.fit_transform(X_trans)

    return scores, pca_model


def knn_aggregate(
        X: np.ndarray, k: int, num_components: int,
        seed: int = 0) -> np.ndarray:
    """Aggregate measurements from nearest neighbors."""

    transcript_count = np.median(X.sum(axis=1))
    
    scores, _ = apply_pca(X, num_components, transcript_count, seed=seed)
    X_agg, _ = aggregate_neighbors(X, scores, k)
    
    _, pca_model = apply_pca(X_agg, num_components, transcript_count, seed=seed)
    input_matrix = ft_transform(normalize(X, transcript_count))
    scores = pca_model.transform(input_matrix)
    X_agg, cell_sizes = aggregate_neighbors(X, scores, k)
    
    return X_agg, cell_sizes


def aggregate_neighbors(
        X: np.ndarray, scores: np.ndarray, k: int) \
        -> Tuple[np.ndarray, np.ndarray]:
    """Sub-routine for nearest neighbor aggregation."""
    
    num_transcripts = X.sum(axis=1)
    dtype = X.dtype

    # make sure score matrix is C-contiguous
    scores = np.array(scores, dtype=dtype, order='C', copy=False)
    
    # work around a bug where np.sqrt() says input is invalid for arrays
    # of type np.float32 that contain zeros
    invalid_errstate = 'warn'
    if np.issubdtype(scores.dtype, np.float32):
        invalid_errstate = 'ignore'
    with np.errstate(invalid=invalid_errstate):
        D = pairwise_distances(scores, n_jobs=1, metric='euclidean')    

    S = np.argsort(D, axis=1, kind='mergesort')
    X_agg = np.empty(X.shape, dtype=dtype)
    cell_sizes = np.empty(X.shape[0], dtype=dtype)
    for i in range(X.shape[0]):
        ind = S[i, :k]
        X_agg[i, :] = np.sum(X[ind, :], axis=0, dtype=dtype)
        cell_sizes[i] = np.median(num_transcripts[ind])
    
    return X_agg, cell_sizes


def restore_matrix(
        scores: np.ndarray, components: np.ndarray,
        mean: np.ndarray, cell_sizes: np.ndarray) -> np.ndarray:
    """Restore the expression matrix from PCA results and cell sizes."""

    # transform from PC space to original space
    D = scores.dot(components)

    # add gene means
    D = D + mean

    # invert the Freeman-Tukey transform
    D[D < 1] = 1
    D = np.power(D, 2)
    D = np.power(D-1, 2) / (4*D)
    
    D = ((cell_sizes / D.sum(axis=1)) * D.T).T
    return D


def denoise_pca(
        X: np.ndarray, num_components: int,
        cell_sizes: np.ndarray,
        seed: int = 0) -> np.ndarray:
    """Denoise data using PCA."""
    
    scores, pca_model = apply_pca(X, num_components, seed=seed)
    components = pca_model.components_
    mean = pca_model.mean_
    
    D = restore_matrix(scores, components, mean, cell_sizes)
    
    return D, scores, components, mean


def write_factorized(
        file_path: str,
        scores: np.ndarray, components: np.ndarray,
        mean: np.ndarray, cell_sizes: np.ndarray,
        cells: Iterable[str], genes: Iterable[str],
        compressed: bool = True) -> None:
    """Write ENHANCE results in factorized form."""

    file_path = os.path.expanduser(file_path)

    data = {}
    data['scores'] = np.array(scores, copy=False)
    data['components'] =  np.array(components, copy=False)
    data['mean'] = np.array(mean, copy=False)
    data['cell_sizes'] = np.array(cell_sizes, copy=False)
    data['cells'] = np.array(list(cells))
    data['genes'] = np.array(list(genes))

    if compressed:
        np.savez_compressed(file_path, **data)
    else:
        np.savez(file_path, **data)

    
def read_factorized(file_path: str) \
        -> Tuple[np.ndarray, List[str], List[str], Dict[str, np.ndarray]]:
    """Read ENHANCE output in factorized form."""
    file_path = os.path.expanduser(file_path)
    data = np.load(file_path)
    scores = data['scores']
    components = data['components']
    mean = data['mean']
    cell_sizes = data['cell_sizes']
    cells = data['cells'].tolist()
    genes = data['genes'].tolist()

    D = restore_matrix(scores, components, mean, cell_sizes)
    return D, cells, genes, data


import numpy as np
from anndata import AnnData

def enhance_adata(
    adata: AnnData,
    target_transcript_count: int = 200000,
    max_neighbor_frac: float = 0.02,
    pc_var_fold_thresh: float = 2.0,
    max_components: int = 50,
    num_neighbors: int = None,
    use_double_precision: bool = False,
    seed: int = 0,
    inplace: bool = False
):
    """
    Apply the ENHANCE denoising algorithm to an AnnData object.
    
    Parameters
    ----------
    adata : AnnData
        The input AnnData object with raw count matrix in .X.
    target_transcript_count : int
        Target total transcripts to determine k if not given.
    max_neighbor_frac : float
        Max fraction of total cells to use for neighbors.
    pc_var_fold_thresh : float
        Fold increase in variance to consider a PC significant.
    max_components : int
        Maximum number of principal components to consider.
    num_neighbors : int, optional
        Fixed number of neighbors (k), overrides auto calculation.
    use_double_precision : bool
        Whether to use float64 instead of float32.
    seed : int
        Random seed for reproducibility.
    inplace : bool
        Whether to update `adata` in-place or return a new one.
    
    Returns
    -------
    AnnData
        The denoised AnnData object, unless inplace=True.
    """
    import warnings
    from scipy.sparse import issparse

    X = adata.X
    if issparse(X):
        X = X.toarray()
    else:
        X = np.array(X)

    D, scores, components, mean, cell_sizes = enhance(
        X,
        target_transcript_count=target_transcript_count,
        max_neighbor_frac=max_neighbor_frac,
        pc_var_fold_thresh=pc_var_fold_thresh,
        max_components=max_components,
        k=num_neighbors,
        use_double_precision=use_double_precision,
        seed=seed
    )

    # Create new AnnData or modify existing
    if inplace:
        adata.X = D
        adata.obsm['X_enhance_pca'] = scores
        adata.uns['enhance'] = {
            'components': components,
            'mean': mean,
            'cell_sizes': cell_sizes,
            'params': {
                'target_transcript_count': target_transcript_count,
                'max_neighbor_frac': max_neighbor_frac,
                'pc_var_fold_thresh': pc_var_fold_thresh,
                'max_components': max_components,
                'k': num_neighbors,
                'seed': seed
            }
        }
    else:
        from anndata import AnnData
        new_adata = AnnData(X=D)
        new_adata.var_names = adata.var_names
        new_adata.obs_names = adata.obs_names
        new_adata.obsm['X_enhance_pca'] = scores
        new_adata.uns['enhance'] = {
            'components': components,
            'mean': mean,
            'cell_sizes': cell_sizes,
            'params': {
                'target_transcript_count': target_transcript_count,
                'max_neighbor_frac': max_neighbor_frac,
                'pc_var_fold_thresh': pc_var_fold_thresh,
                'max_components': max_components,
                'k': num_neighbors,
                'seed': seed
            }
        }

# ===========================
# pcmtm
# ===========================
def run_pcmtm(
    input_adata: str,
    output_adata: str,
    min_genes: int,
    min_cells: int
):
    adata = sc.read(input_adata)
    print(f"[pcmtm] loaded: {adata}")

    # filters BEFORE pcmtm
    sc.pp.filter_cells(adata, min_genes=min_genes)
    sc.pp.filter_genes(adata, min_cells=min_cells)

    adata = pcmt.pp.mag.mag_adata(adata=adata)

    adata.write(output_adata)
    print(f"[pcmtm] saved: {output_adata}")

    del adata
    gc.collect()

    return output_adata



# ===========================
# pcmte
# ===========================
def run_pcmte(input_adata: str, output_adata: str,
              min_genes: int,
              min_cells: int):
    adata = sc.read(input_adata)
    print(f"[pcmte] loaded: {adata}")

    sc.pp.filter_cells(adata, min_genes=min_genes)
    sc.pp.filter_genes(adata, min_cells=min_cells)

    # enhance_adata intentionally omitted
    enhance_adata(adata, inplace=True)

    adata.write(output_adata)
    print(f"[pcmte] saved: {output_adata}")

    # release memory
    del adata
    gc.collect()

    return output_adata


# ===========================
# pcmt-3
# ===========================
def run_pcmt3(pcmte_adata: str,
              pcmtm_adata: str,
              output_adata: str):

    pcmt1 = sc.read(pcmte_adata)
    print(f"[pcmt-3] loaded pcmte: {pcmt1}")

    pcmt2 = sc.read(pcmtm_adata)
    print(f"[pcmt-3] loaded pcmtm: {pcmt2}")

    # align genes
    common_genes = pcmt1.var_names.intersection(pcmt2.var_names)
    pcmt1 = pcmt1[:, common_genes]
    pcmt2 = pcmt2[:, common_genes]

    # matrix add
    pcmt1.X = pcmt1.X + pcmt2.X

    pcmt1.write(output_adata)
    print(f"[pcmt-3] saved: {output_adata}")

    # release memory aggressively
    del pcmt1
    del pcmt2
    gc.collect()

    return output_adata


# ===========================
# pcmt-4
# ===========================
def run_pcmt4(input_adata: str, output_adata: str):
    adata = sc.read(input_adata)
    print(f"[pcmt-4] loaded: {adata}")

    adata = pcmt.pp.rank.normalize_by_e_nonzero_median(adata)

    adata.write(output_adata)
    print(f"[pcmt-4] saved: {output_adata}")

    # release memory
    del adata
    gc.collect()

    return output_adata


# ===========================
# CLI
# ===========================
def parse_args():
    parser = argparse.ArgumentParser(
        description="PCMT maize kernel pipeline (memory-safe)"
    )

    parser.add_argument("--input_adata", required=True)
    parser.add_argument("--out_pcmtm", required=True)
    parser.add_argument("--out_pcmte", required=True)
    parser.add_argument("--out_pcmt3", required=True)
    parser.add_argument("--out_pcmt4", required=True)

    parser.add_argument("--min_genes", type=int, default=100)
    parser.add_argument("--min_cells", type=int, default=3)

    return parser.parse_args()


def main():
    args = parse_args()

    pcmtm_path = run_pcmtm(
        args.input_adata,
        args.out_pcmtm,
        args.min_genes,
        args.min_cells
    )

    pcmte_path = run_pcmte(
        args.input_adata,
        args.out_pcmte,
        args.min_genes,
        args.min_cells
    )

    pcmt3_path = run_pcmt3(
        pcmte_path,
        pcmtm_path,
        args.out_pcmt3
    )

    run_pcmt4(
        pcmt3_path,
        args.out_pcmt4
    )


if __name__ == "__main__":
    main()
