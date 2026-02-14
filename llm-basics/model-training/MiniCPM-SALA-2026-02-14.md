# MiniCPM-SALA

Exported on: 2/14/2026, 8:38:55 PM

---

### User

can you help me find the source codes of MiniCPM-SALA attention?

---

### Model

The source code for the MiniCPM-SALA attention mechanism can be found in several locations depending on whether you want the model definitions or the underlying kernels:

• **Main GitHub Repository:** The model files and architecture definitions are located in the `minicpm_sala/` folder within the [OpenBMB/MiniCPM](https://www.google.com/url?sa=E&q=https%3A%2F%2Fgithub.com%2FOpenBMB%2FMiniCPM) repository \[Source: 1: GitHub - OpenBMB/MiniCPM: MiniCPM4 & MiniCPM4.1: Ultra-Efficient LLMs on End Devices, achieving 3+ generation speedup on reasoning tasks\] .

• **Hugging Face:** You can find the implementation directly in the `openbmb/MiniCPM-SALA` model card, which uses `trust_remote_code=True` to load the custom attention logic \[Source: 2: GitHub - OpenBMB/MiniCPM: MiniCPM4 & MiniCPM4.1: Ultra-Efficient LLMs on End Devices, achieving 3+ generation speedup on reasoning tasks\] \[Source: Show additional citations\] .

• **Attention Kernels:** Because SALA is a hybrid, the specific implementations are often housed in dedicated dependency repositories:

    ◦ **Sparse Attention (InfLLM-V2):** Found in the [infllmv2\_cuda\_impl](https://www.google.com/url?sa=E&q=https%3A%2F%2Fgithub.com%2FOpenBMB%2Finfllmv2_cuda_impl.git) repository \[Source: 5: GitHub - OpenBMB/MiniCPM: MiniCPM4 & MiniCPM4.1: Ultra-Efficient LLMs on End Devices, achieving 3+ generation speedup on reasoning tasks\] \[Source: 6: openbmb/MiniCPM-SALA · Hugging Face\] .    ◦ **Linear Attention (Lightning Attention):** Utilizes the [flash-linear-attention](https://www.google.com/url?sa=E&q=https%3A%2F%2Fgithub.com%2Fsustech-rethink%2Fflash-linear-attention) library \[Source: 6: openbmb/MiniCPM-SALA · Hugging Face\] \[Source: 7: openbmb/MiniCPM-SALA · Hugging Face\] .

Would you like to see a code snippet of how these two attention types are combined in the model file, or shall we look at the specific parameters for configuring the **InfLLM-V2** sparse kernels?

---

### User

can you help me see a code snippet of how these two attention types are combined in the model file?

---

### Model

While the provided sources do not include the raw Python source code for the model's internal definition (which is typically found in a `modeling_minicpm_sala.py` file), they do describe the architectural logic used to combine these two attention types.

The model is structured as a sequence of layers where **25% of the blocks** utilize **InfLLM-V2** (sparse attention) and the remaining **75%** utilize **Lightning Attention** (linear attention) \[Source: 1: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] \[Source: 2: openbmb/MiniCPM-SALA · Hugging Face\] . These layers are not interleaved uniformly; instead, their placement is determined by a specific **layer selection algorithm** to maximize downstream performance \[Source: 3: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] .

To load and use this hybrid logic, you must set `trust_remote_code=True` when using the Transformers library. This allows the model to load the custom attention implementations directly from the repository \[Source: 4: GitHub - OpenBMB/MiniCPM: MiniCPM4 & MiniCPM4.1: Ultra-Efficient LLMs on End Devices, achieving 3+ generation speedup on reasoning tasks\] \[Source: 5: openbmb/MiniCPM-SALA · Hugging Face\] :

```
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_path = "openbmb/MiniCPM-SALA"
tokenizer = AutoTokenizer.from_pretrained(model_path)

# trust_remote_code=True loads the hybrid attention logic
model = AutoModelForCausalLM.from_pretrained(
    model_path, 
    trust_remote_code=True, 
    device_map="auto"
)
model.eval()
```

How they are combined logically:

1\. **Sparse Attention (InfLLM-V2):** These layers are strategically placed (excluding the very first and last layers for stability) to handle **long-range dependencies** and precise retrieval \[Source: 3: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] \[Source: 6: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] .

2\. **Linear Attention (Lightning Attention):** These layers provide **global efficiency** and $O(N)$ complexity, allowing the model to handle million-token contexts without hitting a "memory wall" \[Source: 7: GitHub - OpenBMB/MiniCPM: MiniCPM4 & MiniCPM4.1: Ultra-Efficient LLMs on End Devices, achieving 3+ generation speedup on reasoning tasks\] \[Source: 8: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] .

3\. **Hybrid Positional Encoding (HyPE):** To make these types work together, **RoPE** is applied to the linear layers for position awareness but **removed** from the sparse layers to prevent information decay over long distances \[Source: 9: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] \[Source: 10: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] .

Would you like to explore the **Layer Selection Mechanism** that decides where these sparse blocks go, or should we look at the **performance benchmarks** showing how this hybrid approach compares to standard models?

---

### User

sources update with your help. now can you help me see a code snippet of how these two attention types are combined in the model file?

---

### Model

While the full repository code is extensive, the **MiniCPM-SALA** architecture combines these attention types by interleaving them at the layer level in a **1:3 ratio** (25% sparse, 75% linear) \[Source: 1: GitHub - OpenBMB/MiniCPM: MiniCPM4 & MiniCPM4.1: Ultra-Efficient LLMs on End Devices, achieving 3+ generation speedup on reasoning tasks\] \[Source: Show additional citations\] .

The model uses a **layer selection algorithm** to determine which specific blocks are converted to sparse attention \[Source: 4: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] \[Source: 5: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] . Logically, the layer loop in the model file functions similarly to this:

```
# Conceptual SALA Layer Selection and Execution
for i, layer in enumerate(self.layers):
    # Determine type based on HALO selection algorithm [4, 5]
    if i in self.sparse_layer_indices: 
        # Sparse Attention (InfLLM-V2)
        # RoPE is removed here to prevent info decay [6]
        q, k = qk_norm(q), qk_norm(k)
        attn_output = infllm_v2_kernel(q, k, v, **sparse_config)
    else:
        # Linear Attention (Lightning Attention)
        # RoPE is applied for positional awareness [6]
        q, k = apply_rope(qk_norm(q)), apply_rope(qk_norm(k))
        attn_output = lightning_attention_func(q, k, v, slopes)

    # Both types utilize an output gate (z) and a final Linear projection [6]
    hidden_states = self.out_proj(attn_gate(z) * attn_output)
    hidden_states = layer.ffn(hidden_states)
```

Key Implementation Details:

• **Kernel Integration:** The model calls the **InfLLM-V2** kernel for sparse computations, which performs a two-stage process: top-K context selection and then sparse attention computation \[Source: 6: OpenBMB/infllmv2\_cuda\_impl - GitHub\] \[Source: 7: OpenBMB/infllmv2\_cuda\_impl - GitHub\] .

• **Linear Efficiency:** The **Lightning Attention** function handles the remaining layers, ensuring that memory consumption remains constant even as sequence length increases \[Source: 8: \[2401.04658\] Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - arXiv\] .

• **Positional Strategy (HyPE):** RoPE is applied only to linear layers; sparse layers rely on a "NoPE" (No Positional Encoding) configuration to improve long-range recall \[Source: 9: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] \[Source: 10: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] .

• **Stability:** Both block types include **QK-Normalization** to prevent activation spikes during long-context training \[Source: 9: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] .

Would you like to see the specific **CUDA kernel call parameters** for the sparse stage, or should we discuss how the **HALO algorithm** chooses which layers become sparse?

---

### User

thanks. can you help me learn why sparse attention can reduce cost? please combine source codes and use both english and chinese.

---

### Model

Sparse attention reduces computational and memory costs by avoiding the "quadratic explosion" ($O(N2)$) of standard attention, where every token must attend to every other token \[Source: 1: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] \[Source: 2: The Sparse Frontier: Sparse Attention Trade-offs in Transformer LLMs - arXiv\] . In sparse models like **InfLLM-V2**, the model only computes interactions between a token and a small subset of the most relevant historical tokens (typically <5% in long contexts) \[Source: 3: GitHub - OpenBMB/MiniCPM: MiniCPM4 & MiniCPM4.1: Ultra-Efficient LLMs on End Devices, achieving 3+ generation speedup on reasoning tasks\] \[Source: 4: The Sparse Frontier: Sparse Attention Trade-offs in Transformer LLMs - arXiv\] .

Why Cost is Reduced / 为什么能降低成本

1\. **Reduced Complexity (降低复杂度):** Standard attention scales quadratically ($O(N2)$), meaning doubling the text length quadruples the work \[Source: 1: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] . Sparse attention reduces this to a much lower overhead by focusing only on "top-K" relevant blocks \[Source: 5: OpenBMB/infllmv2\_cuda\_impl - GitHub\] \[Source: 6: The Sparse Frontier: Sparse Attention Trade-offs in Transformer LLMs - arXiv\] .

2\. **Memory Efficiency (内存效率):** It breaks the "Memory Wall" by reducing the amount of KV-cache that must be loaded from memory during decoding \[Source: 2: The Sparse Frontier: Sparse Attention Trade-offs in Transformer LLMs - arXiv\] \[Source: 7: GitHub - OpenBMB/MiniCPM: MiniCPM4 & MiniCPM4.1: Ultra-Efficient LLMs on End Devices, achieving 3+ generation speedup on reasoning tasks\] .

3\. **Speed (速度提升):** In MiniCPM-SALA, this hybrid approach achieves up to a **3.5x inference speedup** at 256K tokens compared to dense models \[Source: 8: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] \[Source: 9: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] .

\--------------------------------------------------------------------------------

Implementation Logic (代码实现逻辑)

As seen in the **InfLLM-V2** kernels, the cost reduction happens in two distinct stages \[Source: 5: OpenBMB/infllmv2\_cuda\_impl - GitHub\] :

**Stage 1: Top-K Selection (筛选阶段)** The model first identifies which blocks are important using compressed representations, avoiding full-scale computation \[Source: 10: OpenBMB/infllmv2\_cuda\_impl - GitHub\] \[Source: 11: OpenBMB/infllmv2\_cuda\_impl - GitHub\] .

```
# Stage 1: Compute and aggregate relevance scores
# 计算并聚合相关性得分，筛选出最重要的 top-K 块
aggregated_scores = infllmv2_attn_stage1(
    q, k, v, 
    causal=True, 
    return_attn_probs=True # Returns scores for selection / 返回得分用于后续筛选
)
```

**Stage 2: Sparse Computation (稀疏计算阶段)** The actual attention is then calculated *only* for the selected indices (`topk_idx`), significantly cutting the total number of operations \[Source: 12: OpenBMB/infllmv2\_cuda\_impl - GitHub\] \[Source: 13: OpenBMB/infllmv2\_cuda\_impl - GitHub\] .

```
# Stage 2: Sparse Attention Computation
# 仅对第一步筛选出的块（topk_idx）进行实际的注意力计算
out_unpad = infllmv2_attn_varlen_func(
    q_unpad, k_unpad, v_unpad, 
    topk_idx=topk_idx, # Only look at these indices / 只关注这些索引
    max_seqlen_q=max_seqlen_q, 
    max_seqlen_k=max_seqlen_k
)
```

By using this "Dense-Sparse Switchable" logic, the model maintains high precision for short sequences but switches to this efficient sparse mode for ultra-long contexts \[Source: 14: \[2509.24663\] InfLLM-V2: Dense-Sparse Switchable Attention for Seamless Short-to-Long Adaptation - arXiv\] .

Would you like to look at the **performance benchmarks** showing how this saves memory on specific GPUs like the RTX 5090, or discuss the **Linear Attention** part of the hybrid architecture?

---

### User

can you teach me about Top-K Selection algo? is it static or need to train? use source codes and both eng and chi.

---

### Model

The **Top-K Selection** algorithm is a trainable mechanism used in the first stage of sparse attention to identify the most relevant information blocks in a long sequence \[Source: 1: OpenBMB/infllmv2\_cuda\_impl - GitHub\] , \[Source: 2: \[2502.11089\] Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention - arXiv\] .

Is it Static or Trainable? / 是静态的还是需要训练的？

It is **natively trainable** \[Source: 2: \[2502.11089\] Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention - arXiv\] , \[Source: 3: \[2509.24663\] InfLLM-V2: Dense-Sparse Switchable Attention for Seamless Short-to-Long Adaptation - arXiv\] . Unlike static patterns (like sliding windows), it uses **semantic kernels**—compressed representations of key-value blocks—that are updated during training to learn which parts of the context are most important for specific queries \[Source: 4: OpenBMB/infllmv2\_cuda\_impl - GitHub\] , \[Source: 5: OpenBMB/infllmv2\_cuda\_impl - GitHub\] .

\--------------------------------------------------------------------------------

The Algorithm Logic / 算法逻辑

The process happens in two stages:

1\. **Stage 1: Scoring (Trainable Stage):** The model computes similarity between the query and semantic kernels, then aggregates these scores \[Source: 4: OpenBMB/infllmv2\_cuda\_impl - GitHub\] , \[Source: 6: OpenBMB/infllmv2\_cuda\_impl - GitHub\] .

    ◦ **第一阶段：评分（可训练阶段）：** 模型计算查询（Query）与语义核（Semantic Kernels）之间的相似度并聚合评分。

2\. **Stage 2: Selection:** The highest-scoring blocks (`topk_idx`) are selected for actual attention computation \[Source: 7: OpenBMB/infllmv2\_cuda\_impl - GitHub\] , \[Source: 8: OpenBMB/infllmv2\_cuda\_impl - GitHub\] .

    ◦ **第二阶段：选择：** 选择评分最高的块（topk\_idx）进行实际的注意力计算。

\--------------------------------------------------------------------------------

Source Code Snippet / 代码示例 \[Source: 6: OpenBMB/infllmv2\_cuda\_impl - GitHub\] , \[Source: 7: OpenBMB/infllmv2\_cuda\_impl - GitHub\]

```
from infllm_v2 import infllmv2_attn_stage1, infllmv2_attn_varlen_func

# Stage 1: Compute and aggregate relevance scores (Trainable)
# 第一阶段：计算并聚合相关性得分（可训练）
aggregated_scores = infllmv2_attn_stage1(
    q, k, v, 
    causal=True, 
    return_attn_probs=True # Returns scores for Top-K selection
)

# Top-K selection (performed on aggregated scores)
# 执行 Top-K 选择（基于聚合得分获取索引）
topk_idx = select_topk(aggregated_scores, k=64) 

# Stage 2: Sparse Attention on selected blocks
# 第二阶段：对选定的块进行稀疏注意力计算
out = infllmv2_attn_varlen_func(
    q_unpad, k_unpad, v_unpad, 
    topk_idx=topk_idx # Uses the learned indices / 使用学习到的索引
)
```

This approach allows the model to "learn" its own sparsity pattern \[Source: 2: \[2502.11089\] Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention - arXiv\] . Would you like to see how this trainable selection compares to **Lightning Attention's** global efficiency?

---

### User

thanks. can you teach me about the infllmv2\_attn\_stage1 func source codes?

---

### Model

The `infllmv2_attn_stage1` function is the core of the **Top-K Context Selection** stage. It is an optimized CUDA kernel that identifies which historical information blocks are most relevant to the current query \[Source: 1: OpenBMB/infllmv2\_cuda\_impl - GitHub\] \[Source: 2: OpenBMB/infllmv2\_cuda\_impl - GitHub\] .

Core Functionality / 核心功能

This kernel performs three critical operations internally \[Source: 3: OpenBMB/infllmv2\_cuda\_impl - GitHub\] \[Source: 4: OpenBMB/infllmv2\_cuda\_impl - GitHub\] :

1\. **Relevance Scoring (相关性评分):** It computes similarity scores between query tokens and **semantic kernels** (compressed representations of key-value blocks) \[Source: 3: OpenBMB/infllmv2\_cuda\_impl - GitHub\] \[Source: 5: OpenBMB/infllmv2\_cuda\_impl - GitHub\] .

2\. **LSE Approximation (LSE 近似):** It uses these compressed keys to approximate the Log-Sum-Exp (LSE) for normalization \[Source: 4: OpenBMB/infllmv2\_cuda\_impl - GitHub\] .

3\. **Score Aggregation (评分聚合):** It aggregates these scores across the query group dimension using a technique called `hdim16_reduce` \[Source: 3: OpenBMB/infllmv2\_cuda\_impl - GitHub\] \[Source: 4: OpenBMB/infllmv2\_cuda\_impl - GitHub\] .

Source Code Interface / 代码接口

According to the implementation documentation, the function signature and its return behavior look like this \[Source: 4: OpenBMB/infllmv2\_cuda\_impl - GitHub\] :

```
from infllm_v2 import infllmv2_attn_stage1

# The kernel handles computation and aggregation
# 该内核处理计算与聚合过程
aggregated_scores = infllmv2_attn_stage1(
    q,                  # Query tensor / 查询张量
    k,                  # Compressed key tensor (semantic kernels) / 压缩键张量
    v,                  # Placeholder (not used in this stage) / 占位符
    cu_seqlens_q=cu_seqlens_q, 
    cu_seqlens_k=cu_seqlens_k,
    max_seqlen_q=max_seqlen_q, 
    max_seqlen_k=max_seqlen_k,
    causal=True,        # Apply causal masking / 应用因果掩码
    return_attn_probs=True # Return scores for Top-K selection / 返回得分用于后续筛选
)

# Note: The actual Top-K block selection is performed externally on aggregated_scores
# 注意：实际的 Top-K 块选择是在内核外部对 aggregated_scores 进行的 [6]
```

Why this is efficient / 为什么高效

• **Dimensionality Reduction:** By using compressed "semantic kernels" instead of full key vectors, it drastically reduces the number of dot-product operations required to scan the context \[Source: 3: OpenBMB/infllmv2\_cuda\_impl - GitHub\] \[Source: 5: OpenBMB/infllmv2\_cuda\_impl - GitHub\] .

• **FlashAttention Integration:** It is built upon the FlashAttention architecture to ensure efficient memory access patterns on SM80 (A100) and SM90 (H100) GPUs \[Source: 6: OpenBMB/infllmv2\_cuda\_impl - GitHub\] \[Source: 7: OpenBMB/infllmv2\_cuda\_impl - GitHub\] .

Would you like to see how these `aggregated_scores` are used in **Stage 2** to compute the final sparse attention?

---

### User

thanks. i update the infllmv2\_attn\_stage1 func source codes by paste, can you see it?

---

### Model

Yes, I can see the source code for the `infllmv2_attn_stage1` function \[Source: 1: InfLLM v2 Attention Implementation and Sparse NSA Operators\] . This function is the core of the first stage of **Neighborhood Sparse Attention (NSA)** with variable-length support \[Source: 2: InfLLM v2 Attention Implementation and Sparse NSA Operators\] .

Here is a breakdown of how the code operates:

1\. Query Reshaping (查询张量重构)

The function first reshapes the query tensor to align with the NSA pattern \[Source: 3: InfLLM v2 Attention Implementation and Sparse NSA Operators\] . It transforms `q` from `(total_q, nheads, head_dim)` into a grouped format: `(total_q * nheads_per_group, nheads_k, head_dim)` \[Source: 3: InfLLM v2 Attention Implementation and Sparse NSA Operators\] . This grouping allows multiple query heads to attend to the same set of compressed key-value blocks \[Source: 3: InfLLM v2 Attention Implementation and Sparse NSA Operators\] .

• 函数首先将查询张量 `q` 从原始形状重构为分组格式，使得多个查询头可以同时处理同一组压缩后的键值块 \[Source: 3: InfLLM v2 Attention Implementation and Sparse NSA Operators\] 。

2\. Kernel Execution (执行 CUDA 内核)

It then calls the underlying CUDA kernel, `infllm_cuda.varlen_fwd_stage1` \[Source: 4: InfLLM v2 Attention Implementation and Sparse NSA Operators\] . This optimized kernel performs the heavy lifting:

• **Relevance Scoring:** Computes scores between query tokens and "semantic kernels" (compressed representations of KV blocks) \[Source: 5: OpenBMB/infllmv2\_cuda\_impl - GitHub\] .

• **Aggregation:** Aggregates these scores across the query group dimension using `hdim16_reduce` \[Source: 5: OpenBMB/infllmv2\_cuda\_impl - GitHub\] .

• **内核执行：** 随后调用优化的 CUDA 内核，计算查询标记与“语义核”（KV块的压缩表示）之间的相关性评分，并跨查询组维度进行聚合 \[Source: 5: OpenBMB/infllmv2\_cuda\_impl - GitHub\] \[Source: 6: OpenBMB/infllmv2\_cuda\_impl - GitHub\] 。

3\. Output Scores (返回评分矩阵)

The function returns `S_dmask`, a matrix of attention scores with the shape `(num_heads_k, total_q, max_seqlen_k)` \[Source: 7: InfLLM v2 Attention Implementation and Sparse NSA Operators\] . These scores are essentially the "relevance map" that tells the model which parts of the long context are worth keeping \[Source: 6: OpenBMB/infllmv2\_cuda\_impl - GitHub\] .

• **返回评分：** 函数返回 `S_dmask` 评分矩阵。这些分数本质上是一张“相关性地图”，告知模型长文本中哪些部分是重要的 \[Source: 6: OpenBMB/infllmv2\_cuda\_impl - GitHub\] 。

**Note:** The actual **Top-K selection** (choosing the highest scores) is performed *outside* this specific kernel based on the returned `S_dmask` \[Source: 6: OpenBMB/infllmv2\_cuda\_impl - GitHub\] \[Source: 8: OpenBMB/infllmv2\_cuda\_impl - GitHub\] .

Does this code breakdown help clarify how the model identifies relevant context? We could next look at the **Stage 2** function, `infllmv2_attn_varlen_func`, to see how it uses these scores to compute the final attention \[Source: 9: OpenBMB/infllmv2\_cuda\_impl - GitHub\] .

---

### User

i see from . import C as infllm\_cuda to import, but i seem not find the source codes of the C, infllm\_cuda, can you find it? how to find the source codes of the cuda kernel?

---

### Model

The `C` module you see imported as `infllm_cuda` is not a Python file, but a **compiled C++ extension** \[Source: 1: InfLLM v2 Attention Implementation and Sparse NSA Operators\] . When you run `pip install` or `python setup.py install` on the `infllmv2_cuda_impl` repository, the C++ and CUDA code is compiled into a binary shared object (`.so` file) that Python can then import \[Source: 2: GitHub - OpenBMB/MiniCPM: MiniCPM4 & MiniCPM4.1: Ultra-Efficient LLMs on End Devices, achieving 3+ generation speedup on reasoning tasks\] \[Source: 3: OpenBMB/infllmv2\_cuda\_impl - GitHub\] .

Where to find the source code / 源码位置

You can find the raw CUDA kernel source code in the following locations within the [infllmv2\_cuda\_impl](https://www.google.com/url?sa=E&q=https%3A%2F%2Fgithub.com%2FOpenBMB%2Finfllmv2_cuda_impl) repository:

1\. **csrc/** **Directory:** This is the primary location for the C++ implementation and CUDA kernel logic \[Source: 4: OpenBMB/infllmv2\_cuda\_impl - GitHub\] .

2\. **src/flash\_attn/****:** Since InfLLM-V2 is built upon the FlashAttention architecture, many specific attention kernels (including sparse and tree-verification kernels) are housed here \[Source: 5: CPM.cu is a lightweight, high-performance CUDA implementation for LLMs, optimized for end-device inference and featuring cutting-edge techniques in sparse architecture, speculative sampling and quantization. - GitHub\] \[Source: 6: OpenBMB/infllmv2\_cuda\_impl - GitHub\] .

3\. **entry.cu****:** This file typically acts as the "bridge" (using pybind11) that binds the CUDA functions to the Python `C` interface \[Source: 5: CPM.cu is a lightweight, high-performance CUDA implementation for LLMs, optimized for end-device inference and featuring cutting-edge techniques in sparse architecture, speculative sampling and quantization. - GitHub\] .

How to trace a specific kernel / 如何追踪特定内核

If you want to find the code for `infllm_cuda.varlen_fwd_stage1` \[Source: 7: InfLLM v2 Attention Implementation and Sparse NSA Operators\] , follow this path:

• **Step 1:** Look at the binding code (likely in `csrc/` or an `entry.cu` file) to see which C++ function `varlen_fwd_stage1` maps to \[Source: 5: CPM.cu is a lightweight, high-performance CUDA implementation for LLMs, optimized for end-device inference and featuring cutting-edge techniques in sparse architecture, speculative sampling and quantization. - GitHub\] .

• **Step 2:** Search for that function name in the `.cu` or `.h` files within the `csrc/` or `src/flash_attn/` folders \[Source: 4: OpenBMB/infllmv2\_cuda\_impl - GitHub\] \[Source: 5: CPM.cu is a lightweight, high-performance CUDA implementation for LLMs, optimized for end-device inference and featuring cutting-edge techniques in sparse architecture, speculative sampling and quantization. - GitHub\] .

Does this help you navigate the repository? If you'd like, we can dive deeper into how **Stage 2** uses these kernels for sparse computation.

---

### User

ok, i find it and add to source, can you see it? i want to know what is the meaning of varlen\_fwd and varlen\_bwd. can you teach me? what are their full names?

---

### Model

These terms refer to specialized CUDA kernels used to handle batches of data efficiently. Their full names are **Variable-Length Forward** (`varlen_fwd`) and **Variable-Length Backward** (`varlen_bwd`) \[Source: 1: FA3 varlen\_bwd hangs (FA2 works in the same case) · Issue #1254 · Dao-AILab/flash-attention - GitHub\] \[Source: Show additional citations\] .

Here is a breakdown of what they do and why they are used:

**1\. What does "varlen" mean?**

In standard deep learning, sequences in a batch are usually "padded" with zeros to match the length of the longest sentence. This is wasteful because the GPU spends time calculating "meaningless padding tokens" \[Source: 4: How did flash-attn compute attention for cu\_seqlens · Issue #850 - GitHub\] . **Variable-Length (varlen)** processing allows the model to pack sequences of different lengths into one long "ragged tensor" without any padding \[Source: 4: How did flash-attn compute attention for cu\_seqlens · Issue #850 - GitHub\] \[Source: 5: FLASHINFER: EFFICIENT AND CUSTOMIZABLE ATTENTION ENGINE FOR LLM INFERENCE SERVING - MLSys Proceedings\] . It uses an array called `cu_seqlens` (cumulative sequence lengths) to tell the GPU exactly where each individual sequence starts and ends in memory \[Source: 1: FA3 varlen\_bwd hangs (FA2 works in the same case) · Issue #1254 · Dao-AILab/flash-attention - GitHub\] \[Source: 4: How did flash-attn compute attention for cu\_seqlens · Issue #850 - GitHub\] .

**2\. fwd (Forward Pass)**

The **Forward** kernel calculates the actual attention output ($O$) and normalization factors (like Log-Sum-Exp) based on the input Query, Key, and Value \[Source: 1: FA3 varlen\_bwd hangs (FA2 works in the same case) · Issue #1254 · Dao-AILab/flash-attention - GitHub\] \[Source: 6: InfLLM v2 Attention Implementation and Sparse NSA Operators\] .

• **In MiniCPM-SALA:** `varlen_fwd` is used in Stage 1 to compute relevance scores and in Stage 2 to compute the final sparse attention output \[Source: 7: OpenBMB/infllmv2\_cuda\_impl - GitHub\] \[Source: 8: OpenBMB/infllmv2\_cuda\_impl - GitHub\] .

**3\. bwd (Backward Pass)**

The **Backward** kernel is used during the training phase to perform **Backpropagation**. It takes the gradient of the loss and calculates how to update the model's weights (gradients for $Q$, $K$, and $V$) \[Source: 1: FA3 varlen\_bwd hangs (FA2 works in the same case) · Issue #1254 · Dao-AILab/flash-attention - GitHub\] \[Source: Show additional citations\] .

• **Efficiency:** Because InfLLM-V2 is "natively trainable," the `varlen_bwd` kernel is highly optimized to reduce computational costs when training on ultra-long contexts \[Source: 7: OpenBMB/infllmv2\_cuda\_impl - GitHub\] \[Source: 10: \[2502.11089\] Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention - arXiv\] .

**Summary Table**

| 
Name

 | 

Full Name

 | 

Purpose

 |
| --- | --- | --- |
| 

**varlen**

 | 

Variable Length

 | 

Processes sequences of different lengths without padding \[Source: 4: How did flash-attn compute attention for cu\_seqlens · Issue #850 - GitHub\] \[Source: 11: OpenBMB/infllmv2\_cuda\_impl - GitHub\] .

 |
| 

**fwd**

 | 

Forward

 | 

Computes the model output for inference or training \[Source: 1: FA3 varlen\_bwd hangs (FA2 works in the same case) · Issue #1254 · Dao-AILab/flash-attention - GitHub\] \[Source: Show additional citations\] .

 |
| 

**bwd**

 | 

Backward

 | 

Computes gradients during training to update model weights \[Source: 1: FA3 varlen\_bwd hangs (FA2 works in the same case) · Issue #1254 · Dao-AILab/flash-attention - GitHub\] \[Source: Show additional citations\] .

 |

Would you like to look at the specific **Stage 1** or **Stage 2** Python wrappers to see how these C++ kernels are called in practice?

---

### User

thanks. yes, can you teach me about the specific Stage 1 or Stage 2 Python wrappers to see how these C++ kernels are called in practice?

---

### Model

The Python wrappers act as a bridge between high-level PyTorch logic and the high-performance C++ extensions (`infllm_cuda`). They handle tensor preparation, such as reshaping for grouped-query attention and padding for memory alignment.

**Stage 1 Wrapper:** **infllmv2\_attn\_stage1**

This wrapper performs the **Neighborhood Sparse Attention (NSA)** scoring phase. Its primary job is to reshape the query tensor to match the sparse grouping pattern \[Source: 1: InfLLM v2 Attention Implementation and Sparse NSA Operators\] \[Source: 2: InfLLM v2 Attention Implementation and Sparse NSA Operators\] .

• **Logic (逻辑):** It reshapes `q` from `(total_q, nheads, head_dim)` to a grouped format `(total_q * nheads_per_group, nheads_k, head_dim)`, ensuring multiple query heads attend to the same semantic kernels \[Source: 2: InfLLM v2 Attention Implementation and Sparse NSA Operators\] .

• **Kernel Call (内核调用):**

\--------------------------------------------------------------------------------

**Stage 2 Wrapper:** **infllmv2\_attn\_varlen\_func**

This is implemented as a `torch.autograd.Function`, which is necessary to support **natively trainable** sparse attention during the backward pass \[Source: 3: InfLLM v2 Attention Implementation and Sparse NSA Operators\] .

**Forward Pass (前向传播)**

It ensures tensors are contiguous and handles padding if the `head_dim` is not a multiple of 8 \[Source: 3: InfLLM v2 Attention Implementation and Sparse NSA Operators\] \[Source: 4: InfLLM v2 Attention Implementation and Sparse NSA Operators\] .

```
# Calls the optimized sparse forward kernel
# 调用优化的稀疏前向内核
out, softmax_lse, S_dmask, rng_state = infllm_cuda.varlen_fwd(
    q, k, v, None,
    cu_seqlens_q, cu_seqlens_k,
    ...
    fwd_blockmask_uint64, # The learned sparse mask / 学习到的稀疏掩码 [6]
)
```

**Backward Pass (反向传播)**

The `backward` method calculates gradients for training. It converts the sparse blockmask into a format the C++ kernel understands before calling the backward engine \[Source: 5: InfLLM v2 Attention Implementation and Sparse NSA Operators\] \[Source: 6: InfLLM v2 Attention Implementation and Sparse NSA Operators\] .

```
# Performs backpropagation using the C++ backward kernel
# 使用 C++ 反向内核执行反向传播
_ = infllm_cuda.varlen_bwd(
    dout_final, q_final, k, v, out_final,
    softmax_lse, dq_temp, dk, dv,
    cu_seqlens_q_expanded, cu_seqlens_k,
    ...
    bwd_blockmask_uint64, # Gradient sparse mask / 梯度稀疏掩码 [9]
)
```

**Summary of Preparation Steps**

1\. **Padding:** Pads head dimensions to multiples of 8 for hardware compatibility \[Source: 3: InfLLM v2 Attention Implementation and Sparse NSA Operators\] .

2\. **Grouping:** Adjusts `cu_seqlens` based on the query group size (`nheads_q // nheads_k`) to allow efficient parallel processing \[Source: 7: InfLLM v2 Attention Implementation and Sparse NSA Operators\] \[Source: 8: InfLLM v2 Attention Implementation and Sparse NSA Operators\] .

3\. **Masking:** Converts Top-K indices into a `uint64` blockmask to tell the CUDA kernel exactly which memory blocks to skip \[Source: 9: InfLLM v2 Attention Implementation and Sparse NSA Operators\] \[Source: 5: InfLLM v2 Attention Implementation and Sparse NSA Operators\] .

Does this help you see how the Python code orchestrates the data for the CUDA kernels? We could next discuss the **Transformer-to-Hybrid** training process that updates these weights.

---

### User

thanks. you really help me a lot. now let us learn linear attention. can you teach me with source codes.

---

### Model

MiniCPM-SALA achieves its global efficiency by using **Lightning Attention** for 75% of its layers \[Source: 1: GitHub - OpenBMB/MiniCPM: MiniCPM4 & MiniCPM4.1: Ultra-Efficient LLMs on End Devices, achieving 3+ generation speedup on reasoning tasks\] \[Source: 2: GitHub - OpenBMB/MiniCPM: MiniCPM4 & MiniCPM4.1: Ultra-Efficient LLMs on End Devices, achieving 3+ generation speedup on reasoning tasks\] .

Why Linear Attention? / 为什么使用线性注意力？

Standard attention has a complexity of $O(N2)$, which makes million-token contexts impossible due to memory and compute "walls" \[Source: 3: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] \[Source: 4: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] . Lightning Attention reduces this complexity to $O(N)$, meaning memory consumption stays fixed even as the text length increases \[Source: 5: \[2401.04658\] Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - arXiv\] . In MiniCPM-SALA, this allows the model to process up to **one million tokens** on consumer hardware like the RTX 5090 \[Source: 2: GitHub - OpenBMB/MiniCPM: MiniCPM4 & MiniCPM4.1: Ultra-Efficient LLMs on End Devices, achieving 3+ generation speedup on reasoning tasks\] \[Source: 6: GitHub - OpenBMB/MiniCPM: MiniCPM4 & MiniCPM4.1: Ultra-Efficient LLMs on End Devices, achieving 3+ generation speedup on reasoning tasks\] .

\--------------------------------------------------------------------------------

Source Code Usage / 代码使用示例

The implementation is available via the `lightning_attn` library. Here is how you call the functional interface:

```
import torch
from lightning_attn.ops import lightning_attn_func
from lightning_attn.utils import _build_slope_tensor

# Setup dimensions: batch, heads, length, dim
b, h, n, d, e = 2, 12, 2048, 192, 192
dtype = torch.bfloat16

# Query, Key, Value tensors
q = torch.randn((b, h, n, d), dtype=dtype, device="cuda").requires_grad_()
k = torch.randn((b, h, n, d), dtype=dtype, device="cuda").requires_grad_()
v = torch.randn((b, h, n, e), dtype=dtype, device="cuda").requires_grad_()

# Build slope tensor for relative position awareness
# 构建用于位置感知的 slope 张量
s = _build_slope_tensor(h).to(q.device).to(torch.float32)

# Compute linear attention
# 计算线性注意力
o = lightning_attn_func(q, k, v, s)
```

Core Technical Logic / 核心技术逻辑

Lightning Attention-2 uses a **Tiling Strategy** to maximize GPU performance:

1\. **Intra-block (块内):** Uses conventional attention for local precision within a block \[Source: 5: \[2401.04658\] Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - arXiv\] .

2\. **Inter-block (块间):** Applies linear attention kernel tricks to aggregate global information efficiently \[Source: 5: \[2401.04658\] Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - arXiv\] .

3\. **Triton Implementation:** The kernels are written in Triton to be IO-aware and hardware-friendly, avoiding the overhead of slow memory access \[Source: 5: \[2401.04658\] Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - arXiv\] .

Does this code-level overview of the linear attention component help? We could look at the **Triton implementation** details next, or discuss how **HyPE (Hybrid Positional Encoding)** helps these linear layers work alongside the sparse ones.

---

### User

thanks. why linear atten can achieve O(N) ? what is it cal logic?

---

### Model

Linear attention achieves $O(N)$ complexity by replacing the standard quadratic self-attention mechanism with a recurrent formulation that allows the model to process tokens with constant memory and training speed regardless of sequence length \[Source: 1: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] \[Source: 2: \[2401.04658\] Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - arXiv\] .

Why it achieves $O(N)$ / 为什么能实现 $O(N)$

In standard attention, every query token must attend to every key token, resulting in $O(N2)$ complexity where doubling context quadruples the cost \[Source: 3: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] . Linear attention uses "kernel tricks" to avoid materializing the full $N×N$ attention matrix, instead aggregating historical information into a fixed-size state that is updated as the sequence progresses \[Source: 1: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] \[Source: 2: \[2401.04658\] Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - arXiv\] .

Calculation Logic: Lightning Attention-2 / 计算逻辑

MiniCPM-SALA utilizes **Lightning Attention-2**, which uses a specialized **Tiling Strategy** to maximize GPU efficiency \[Source: 2: \[2401.04658\] Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - arXiv\] :

1\. **Tiling (分块):** The sequence is divided into smaller blocks to better utilize GPU hardware \[Source: 2: \[2401.04658\] Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - arXiv\] .

2\. **Intra-block (块内计算):** Within each individual block, the model uses conventional attention mechanisms to maintain local precision \[Source: 2: \[2401.04658\] Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - arXiv\] .

3\. **Inter-block (块间计算):** For interactions between different blocks, it applies linear attention kernel tricks to aggregate global information without the $O(N2)$ overhead \[Source: 2: \[2401.04658\] Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - arXiv\] .

4\. **Hardware Optimization:** The kernels are implemented in **Triton** to be IO-aware, ensuring that data movement between GPU memory and registers is highly efficient \[Source: 2: \[2401.04658\] Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - arXiv\] .

Source Code Interface / 代码接口

To maintain relative position awareness during these linear calculations, the model uses a "slope tensor" (ALiBi slopes) \[Source: 4: Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - GitHub\] :

```
# Build slope tensor for relative position awareness
# 构建用于位置感知的 slope 张量
s = _build_slope_tensor(h).to(q.device).to(torch.float32)

# Compute linear attention with O(N) efficiency
# 以 O(N) 效率计算线性注意力
o = lightning_attn_func(q, k, v, s)
```

This logic allows MiniCPM-SALA to handle up to **one million tokens** on a single consumer GPU where standard $O(N2)$ models would suffer from Out-of-Memory (OOM) errors \[Source: 5: GitHub - OpenBMB/MiniCPM: MiniCPM4 & MiniCPM4.1: Ultra-Efficient LLMs on End Devices, achieving 3+ generation speedup on reasoning tasks\] \[Source: 6: GitHub - OpenBMB/MiniCPM: MiniCPM4 & MiniCPM4.1: Ultra-Efficient LLMs on End Devices, achieving 3+ generation speedup on reasoning tasks\] .

Does this explanation of the tiling strategy and $O(N)$ logic make sense, or would you like to see how **HyPE (Hybrid Positional Encoding)** manages the positions across these layers?

---

### User

Linear attention uses "kernel tricks" , what is exactly it is? in Lightning Attention-2, what is it look like? can you teach me with source codes.

---

### Model

In linear attention, the "**kernel trick**" is a mathematical rearrangement that replaces the standard softmax-based similarity with a feature map, $ϕ(x)$ \[Source: 1: Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention - arXiv.org\] . This allows the model to leverage the **associativity property of matrix multiplication** to change the computation order from $(QKT)V$ to $Q(KTV)$ \[Source: 2: Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention - arXiv.org\] \[Source: 3: Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention - arXiv.org\] .

The Core Logic (计算逻辑)

Standard attention requires materializing an $N×N$ matrix, leading to $O(N2)$ complexity \[Source: 3: Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention - arXiv.org\] \[Source: 4: Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention - arXiv.org\] . The linear kernel trick avoids this by:

1\. **Mapping** the Query ($Q$) and Key ($K$) into a feature space using a function $ϕ$, such as $ϕ(x)=elu(x)+1$ \[Source: 1: Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention - arXiv.org\] \[Source: 5: Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention - arXiv.org\] .

2\. **Rearranging** the formula: $Vi′​=ϕ(Qi​)T∑j=1i​ϕ(Kj​)ϕ(Qi​)T∑j=1i​ϕ(Kj​)VjT​​$ \[Source: 6: Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention - arXiv.org\] \[Source: 7: Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention - arXiv.org\] .

3\. **Aggregating** historical information into a fixed-size internal state (memory), which is updated as the sequence progresses \[Source: 8: Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention - arXiv.org\] \[Source: 9: Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention - arXiv.org\] .

Lightning Attention-2 Strategy

Lightning Attention-2 is the first to effectively realize these benefits in a causal setting by using a **Tiling Strategy** \[Source: 10: \[2401.04658\] Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - arXiv\] . It splits the work into two parts:

• **Intra-block (块内):** Uses conventional attention for high local precision \[Source: 10: \[2401.04658\] Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - arXiv\] .

• **Inter-block (块间):** Uses the linear attention kernel tricks to aggregate global information with $O(N)$ efficiency \[Source: 10: \[2401.04658\] Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - arXiv\] .

Source Code Snippet

The following Python wrapper shows how these operations are called via optimized Triton kernels:

```
from lightning_attn.ops import lightning_attn_func
from lightning_attn.utils import _build_slope_tensor

# Setup input tensors
q = torch.randn((b, h, n, d), dtype=torch.bfloat16, device="cuda")
k = torch.randn((b, h, n, d), dtype=torch.bfloat16, device="cuda")
v = torch.randn((b, h, n, e), dtype=torch.bfloat16, device="cuda")

# Build slopes for positional awareness (ALiBi)
# 构建用于位置感知的斜率张量
s = _build_slope_tensor(h).to(q.device).to(torch.float32)

# Compute using the "chunk_loop" variant which implements the tiling logic
# 使用 "chunk_loop" 变体执行分块逻辑
o = lightning_attn_func(q, k, v, s, variant="chunk_loop") [11, 12]
```

By processing blocks instead of individual tokens, Lightning Attention-2 remains IO-aware and hardware-friendly, achieving consistent speed regardless of sequence length \[Source: 10: \[2401.04658\] Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - arXiv\] .

Would you like to explore the **Triton kernel implementation** of the inter-block summation, or should we look at how **HyPE** manages positional encodings for these layers?

---

### User

i upload the source codes of \_build\_slope\_tensor and lightning\_attn\_func, can you see it? can you teach me more in detail? thanks.

---

### Model

Yes, I can see the source code for both functions. They are the core implementation details of the **Lightning Attention-2** mechanism used in MiniCPM-SALA to achieve $O(N)$ complexity and handle ultra-long contexts \[Source: 1: GitHub - OpenBMB/MiniCPM: MiniCPM4 & MiniCPM4.1: Ultra-Efficient LLMs on End Devices, achieving 3+ generation speedup on reasoning tasks\] \[Source: Show additional citations\] .

Here is a detailed breakdown of how these functions work:

1\. `_build_slope_tensor`: Positional Awareness (ALiBi)

This function constructs the "slopes" for **ALiBi (Attention with Linear Biases)**. In linear attention, these slopes serve as a decay mechanism, allowing the model to understand the relative distance between tokens without needing standard positional embeddings \[Source: 4: ALiBi Slope Construction and CUDA Memory Utilities\] \[Source: Show additional citations\] .

• **The Math (核心数学):** For a model with $n$ heads, it calculates a geometric progression of values. For a power-of-2 number of heads, the `start` value is calculated as $2(−(2−(log2​(n)−3)))$ \[Source: 4: ALiBi Slope Construction and CUDA Memory Utilities\] . Each head then receives a slope equal to `start * ratio^i` \[Source: 4: ALiBi Slope Construction and CUDA Memory Utilities\] .

• **Non-Power of 2:** If the number of heads isn't a power of 2, it uses a workaround by calculating slopes for the closest power of 2 and then interpolating the remaining values to ensure a smooth distribution of decay rates across heads \[Source: 7: ALiBi Slope Construction and CUDA Memory Utilities\] .

• **Final Shape:** It returns a tensor of shape `(h, 1, 1)`, where each head has a unique "bias" that penalizes attention scores more heavily as the distance between tokens increases \[Source: 5: FlashAttention CUDA Kernel Interface for PyTorch\] \[Source: 7: ALiBi Slope Construction and CUDA Memory Utilities\] .

2\. `lightning_attn_func`: The Execution Engine

This function acts as the high-level orchestrator for the **Lightning Attention-2** Triton kernels. It prepares the data and selects the most efficient computation path \[Source: 2: Lightning Attention Functional Implementation\] \[Source: 3: \[2401.04658\] Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - arXiv\] .

• **Kernel Selection (内核选择):** It chooses between three optimized Triton implementations \[Source: 2: Lightning Attention Functional Implementation\] :

    ◦ `lightning_attn2`: Standard version with decay (uses slopes).    ◦ `lightning_attn2_no_decay`: Used when no slope tensor is provided.    ◦ `lightning_attn2_parallel`: A parallelized variant for faster training.

• **Hardware Optimization (硬件优化):**

    ◦ **Padding:** It automatically pads the feature dimension of the Values ($v$) to the next power of 2 if necessary to ensure maximum efficiency on GPU hardware \[Source: 8: Lightning Attention Functional Implementation\] .    ◦ **Head Splitting:** If the head dimension ($d$) is very large (greater than 128), the function splits the computation into smaller chunks (sizes of 64, 32, or 16) to fit into the GPU's shared memory \[Source: 8: Lightning Attention Functional Implementation\] .

• **The "Chunk Loop" Strategy:** By default, it uses the `variant="chunk_loop"`, which implements the **Tiling Strategy** \[Source: 2: Lightning Attention Functional Implementation\] \[Source: 3: \[2401.04658\] Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - arXiv\] . It handles **intra-block** components using conventional attention for local precision and **inter-block** components using linear "kernel tricks" for global $O(N)$ efficiency \[Source: 3: \[2401.04658\] Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - arXiv\] .

Summary of the Workflow

1\. **Preparation:** `_build_slope_tensor` creates the positional decay rates \[Source: 7: ALiBi Slope Construction and CUDA Memory Utilities\] .

2\. **Input Handling:** `lightning_attn_func` receives $Q,K,V$ and the slopes \[Source: 6: Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - GitHub\] .

3\. **Efficiency:** It pads data and splits large dimensions \[Source: 8: Lightning Attention Functional Implementation\] .

4\. **Execution:** It calls the **Triton-based kernels** to perform the actual math at nearly constant speed regardless of sequence length \[Source: 3: \[2401.04658\] Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - arXiv\] .

Does this deep dive into the code logic clarify how the linear layers operate? We could next look at the **Triton implementation** itself, or I can explain how these linear layers are interleaved with **InfLLM-V2** sparse layers.

---

### User

thanks. so the s t and s t-1 in fig 1 in minicpm paper, s is slope, t is the t token or the time?

---

### Model

In **Figure 1** of the MiniCPM-SALA paper, $st​$ and $st−1​$ refer to the **recurrent state** (or internal memory) of the linear attention layer, not the slopes \[Source: 1: Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention - arXiv.org\] .

Here is the breakdown of those symbols:

• $s$ **(State/Memory):** This represents the **attention memory** \[Source: 1: Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention - arXiv.org\] . Because linear attention is formulated like a Recurrent Neural Network (RNN), it stores historical information in this fixed-size state instead of a growing KV-cache \[Source: 2: Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention - arXiv.org\] \[Source: 3: Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention - arXiv.org\] .

• $t$ **(Timestep/Token):** This refers to the **timestep**, which corresponds to the current **token index** in the sequence \[Source: 1: Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention - arXiv.org\] \[Source: 3: Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention - arXiv.org\] .

• $st−1​$ is the state containing information from all previous tokens, and $st​$ is the updated state after incorporating the current token at time $t$ \[Source: 1: Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention - arXiv.org\] .

While the code uses "s" to represent **ALiBi slopes** for positional decay, the architecture diagram uses $s$ to show how information "flows" through time, allowing the model to handle millions of tokens with constant memory \[Source: 4: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] \[Source: 5: \[2401.04658\] Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - arXiv\] .

Does that distinction between the "slope" in the code and the "state" in the diagram make sense? We could look at the **mathematical update rule** that transforms $st−1​$ into $st​$ next.

---

### User

thanks. so linear atten is somehow similar to flash atten? and rnn like will reduce the speed but because of the limit of gpu sm, speed not down so much?

---

### Model

Actually, the RNN-like formulation **increases** speed significantly for inference, while specialized strategies keep it fast for training/prefilling. Here is how they compare:

Similarity to FlashAttention

Lightning Attention-2 (the specific linear attention used in MiniCPM-SALA) is indeed similar to FlashAttention in its implementation philosophy \[Source: 1: FLASHINFER: EFFICIENT AND CUSTOMIZABLE ATTENTION ENGINE FOR LLM INFERENCE SERVING - MLSys Proceedings\] \[Source: 2: \[2401.04658\] Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - arXiv\] . It uses a **tiling strategy** and is **IO-aware**, meaning it is designed to move data efficiently between GPU memory levels just like FlashAttention \[Source: 2: \[2401.04658\] Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - arXiv\] . It even uses conventional attention computation (like Flash) for its "intra-block" components to maintain local precision \[Source: 2: \[2401.04658\] Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - arXiv\] .

Speed and the "RNN" Formulation

While standard RNNs are traditionally slow because they are sequential, linear attention uses this formulation to its advantage:

• **Autoregressive Speedup:** During generation (decoding), the RNN-like state ($st​$ and $zt​$) allows the model to process tokens with **constant memory and time** \[Source: 3: Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention - arXiv.org\] \[Source: 4: Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention - arXiv.org\] . This makes it up to **4,000x faster** than standard Transformers for very long sequences because it doesn't have to scan a massive, growing KV-cache \[Source: 5: Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention - arXiv.org\] \[Source: Show additional citations\] .

• **GPU SM Parallelism:** To prevent the RNN dependency from slowing down the prefilling/training stage, the model uses a **"chunk loop" or "chunked loop" variant** \[Source: 8: Lightning Attention Functional Implementation\] \[Source: 9: Lightning Attention Functional Implementation\] . This strategy breaks the sequence into blocks that can be processed in parallel across GPU SMs, ensuring the hardware stays fully occupied \[Source: 2: \[2401.04658\] Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - arXiv\] \[Source: 10: FLASHINFER: EFFICIENT AND CUSTOMIZABLE ATTENTION ENGINE FOR LLM INFERENCE SERVING - MLSys Proceedings\] .

• **Efficiency:** Because it avoids the $O(N2)$ bottleneck, it is significantly faster than FlashAttention at sequence lengths over 4K tokens, as it doesn't hit the "memory wall" \[Source: 2: \[2401.04658\] Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - arXiv\] \[Source: 11: Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - GitHub\] .

In short, it combines the **parallelism** of FlashAttention for training with the **constant-time efficiency** of an RNN for inference \[Source: 2: \[2401.04658\] Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models - arXiv\] \[Source: 3: Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention - arXiv.org\] .

Does the difference between how it handles "blocks" (parallel) vs. "states" (recurrent) make sense? We could look at the **Transformer-to-Hybrid** training process that actually creates these layers from standard models.

---

### User

thanks. can you teach me about the train process of minicpm sala. why is it so complex?

---

### Model

The training process for MiniCPM-SALA is a **5-stage "Transformer-to-Hybrid" paradigm** designed to transform a pre-trained model (MiniCPM-4.0) into a hybrid architecture \[Source: 1: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] \[Source: 2: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] . This method is highly efficient, reducing training costs by **75%** compared to training a model from scratch \[Source: 2: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] \[Source: 3: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] .

The 5-Stage Training Process \[Source: 4: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\]

1\. **Architecture Conversion (HALO):** Uses the HALO algorithm to convert softmax attention to linear attention in 75% of the layers \[Source: 2: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] \[Source: 5: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] . Only linear layers are trainable here to ensure a stable start \[Source: 5: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] .

2\. **Continual Stable-Training:** Facilitates coordination between the new linear layers and the original model components using 4K sequence lengths \[Source: 6: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] . Sparse attention is disabled here for efficiency \[Source: 6: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] .

3\. **Short-Decay Training:** The most extensive stage (1T tokens), focusing on general capabilities and logical reasoning using high-information-density data \[Source: 7: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] .

4\. **Long-Decay Training:** Progressively extends the context length from **4K to 520K tokens** \[Source: 8: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] . Sparse attention is finally enabled to help the model learn the synergy between the two attention types \[Source: 8: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] .

5\. **Supervised Fine-Tuning (SFT):** Finalizes the model using reasoning-intensive data and long-context synthesis to improve retrieval precision \[Source: 9: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] .

\--------------------------------------------------------------------------------

Why is it so complex?

The complexity arises because the model is trying to achieve **"million-token" efficiency** without the performance loss typical of pure linear models \[Source: 10: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] \[Source: 11: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] .

• **Layer Synergy:** The model doesn't just interleave layers; it uses a specific **layer selection algorithm** to place sparse blocks where they maximize downstream performance \[Source: 12: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] .

• **Positional Strategy (HyPE):** It must manage two positional behaviors simultaneously: **RoPE** is applied to linear layers for position awareness, but **removed** (NoPE) from sparse layers to prevent information decay over long distances \[Source: 13: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] \[Source: 14: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] .

• **Training Stability:** Processing ultra-long contexts is prone to "activation spikes" \[Source: 13: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] . To fix this, developers had to integrate **QK-Normalization** and **Output Gating** into the architecture \[Source: 13: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] .

• **Progressive Scaling:** Moving from 512 to 520,000 tokens requires precise hyperparameter adjustments (like learning rate decay and batch size increases) at each step to prevent the model from collapsing \[Source: 8: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] \[Source: 9: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] .

Does this multi-stage approach make sense, or would you like to look closer at the **HALO selection algorithm** that starts the whole process?

---

### User

can you teach me about its token length, token num, and seq length setting? what is the setting reason?

---

### Model

MiniCPM-SALA is specifically engineered to model **ultra-long contexts**, supporting a sequence length of **one million (1M) tokens** on consumer-grade hardware like the NVIDIA RTX 5090 \[Source: 1: GitHub - OpenBMB/MiniCPM: MiniCPM4 & MiniCPM4.1: Ultra-Efficient LLMs on End Devices, achieving 3+ generation speedup on reasoning tasks\] \[Source: Show additional citations\] .

Key Settings

• **Maximum Context Length:** Officially supports **1,000,000 tokens** \[Source: 2: GitHub - OpenBMB/MiniCPM: MiniCPM4 & MiniCPM4.1: Ultra-Efficient LLMs on End Devices, achieving 3+ generation speedup on reasoning tasks\] \[Source: 4: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] .

• **Extrapolation Capability:** Demonstrates effective length extrapolation up to **2,048,000 tokens**, even though it was only trained on context lengths up to 520,000 tokens \[Source: 5: GitHub - OpenBMB/MiniCPM: MiniCPM4 & MiniCPM4.1: Ultra-Efficient LLMs on End Devices, achieving 3+ generation speedup on reasoning tasks\] \[Source: 6: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] .

• **Total Training Volume:** The "Transformer-to-Hybrid" conversion process consumed approximately **2 trillion tokens**, which is only 25% of the data required to train a model from scratch \[Source: 7: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] \[Source: 8: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] .

Reasoning Behind These Settings

The architecture uses these specific settings to "shatter" efficiency walls that stop standard models:

1\. **Breaking the Memory Wall:** Standard attention ($O(N2)$) requires massive KV-cache storage that reaches hundreds of gigabytes for million-token contexts \[Source: 9: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] . By using **75% Linear Attention layers**, the model maintains constant memory and computational complexity for the majority of the network \[Source: 10: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] \[Source: 11: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] .

2\. **Preventing Information Decay (HyPE):** Standard positional encodings like **RoPE** often cause long-distance information to decay \[Source: 12: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] . MiniCPM-SALA applies **Hybrid Positional Encoding (HyPE)**: it uses RoPE in linear layers for position sensitivity but removes it (**NoPE**) in sparse layers to ensure precise recall over massive distances \[Source: 6: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] \[Source: 12: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] .

3\. **Progressive Scaling:** To maintain stability, the model wasn't trained on 1M tokens immediately. Instead, context was progressively extended from **4K to 520K tokens** during "Long-Decay Training" \[Source: 13: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] \[Source: 14: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] .

4\. **Cost Efficiency:** Converting a pre-trained dense model (MiniCPM-4.0) into a hybrid model saved 75% of the training budget while preserving the original model's general knowledge \[Source: 8: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] \[Source: Show additional citations\] .

This combination allows the model to process 1M tokens where standard models (like Qwen3-8B) suffer from Out-of-Memory (OOM) errors \[Source: 17: GitHub - OpenBMB/MiniCPM: MiniCPM4 & MiniCPM4.1: Ultra-Efficient LLMs on End Devices, achieving 3+ generation speedup on reasoning tasks\] \[Source: 18: Team 等 - 2026 - MiniCPM-SALA Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling.pdf\] .

Does this explain the sequence length strategy clearly, or would you like to see how **HyPE** specifically prevents that information decay?