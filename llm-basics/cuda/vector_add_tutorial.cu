#include <iostream>
#include <cuda_runtime.h>

/**
 * 2.1.2.1. Specifying Kernels (指定内核)
 * Use __global__ to indicate this function runs on GPU and is callable from CPU.
 * 使用 __global__ 表示该函数在 GPU 上运行，并可从 CPU 调用。
 */
__global__ void vecAdd(float* A, float* B, float* C, int vectorLength) {
    
    /**
     * 2.1.2.3. Thread and Grid Index Intrinsics (线程和网格索引内建变量)
     * threadIdx.x: Index of the thread within the block.
     * blockIdx.x:  Index of the block within the grid.
     * blockDim.x:  Number of threads per block.
     * 
     * Formula for 1D global index: index = threadIdx.x + blockIdx.x * blockDim.x
     */
    int i = threadIdx.x + blockIdx.x * blockDim.x;

    /**
     * 2.1.2.3.1. Bounds Checking (边界检查)
     * Since we might launch more threads than elements, we must check the index.
     * 因为启动的线程数可能多于元素数量，我们必须检查索引是否越界。
     */
    if (i < vectorLength) {
        C[i] = A[i] + B[i];
    }
}

int main() {
    // 1. Define vector length (not a multiple of 256 to test bounds checking)
    // 定义向量长度（故意不设为 256 的倍数，以测试边界检查）
    int n = 1000;
    size_t size = n * sizeof(float);

    // 2. Allocate Host memory (CPU)
    // 分配主机内存 (CPU)
    float *h_A = (float*)malloc(size);
    float *h_B = (float*)malloc(size);
    float *h_C = (float*)malloc(size);

    // Initialize data
    for (int i = 0; i < n; i++) {
        h_A[i] = 1.0f;
        h_B[i] = 2.0f;
    }

    // 3. Allocate Device memory (GPU)
    // 分配设备内存 (GPU)
    float *d_A, *d_B, *d_C;
    cudaMalloc(&d_A, size);
    cudaMalloc(&d_B, size);
    cudaMalloc(&d_C, size);

    // 4. Copy data from Host to Device
    // 将数据从主机拷贝到设备
    cudaMemcpy(d_A, h_A, size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B, size, cudaMemcpyHostToDevice);

    /**
     * 2.1.2.2. Launching Kernels (启动内核)
     * Use triple chevron <<<blocks, threads>>>
     * Calculation: (n + threads - 1) / threads ensures we round up.
     */
    int threadsPerBlock = 256;
    int blocksPerGrid = (n + threadsPerBlock - 1) / threadsPerBlock;

    std::cout << "Launching kernel with " << blocksPerGrid << " blocks and " 
              << threadsPerBlock << " threads per block." << std::endl;
    std::cout << "使用 " << blocksPerGrid << " 个块和每个块 " 
              << threadsPerBlock << " 个线程启动内核。" << std::endl;

    // Kernel invocation (内核调用)
    vecAdd<<<blocksPerGrid, threadsPerBlock>>>(d_A, d_B, d_C, n);

    /**
     * Kernel launches are asynchronous. We must synchronize or use 
     * cudaMemcpy (which has implicit synchronization) to get results.
     * 内核启动是异步的。我们必须同步或使用 cudaMemcpy（具有隐式同步功能）来获取结果。
     */
    cudaDeviceSynchronize();

    // 5. Copy result back to Host
    // 将结果拷贝回主机
    cudaMemcpy(h_C, d_C, size, cudaMemcpyDeviceToHost);

    // 6. Verify results (验证结果)
    bool success = true;
    for (int i = 0; i < n; i++) {
        if (h_C[i] != 3.0f) {
            success = false;
            break;
        }
    }

    if (success) std::cout << "Success! 1.0 + 2.0 = 3.0" << std::endl;
    else std::cout << "Error in calculation!" << std::endl;

    // 7. Cleanup (清理内存)
    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);
    free(h_A);
    free(h_B);
    free(h_C);

    return 0;
}
