#include <stdio.h>

__global__ void hello_cuda() {
    printf("hello cuda from gpu.");
}
// nvcc hello-cuda.cu -o hello-cuda
int main(void) {
    hello_cuda<<<2, 2>>>();
    cudaDeviceSynchronize();
    
    return 0;
}

