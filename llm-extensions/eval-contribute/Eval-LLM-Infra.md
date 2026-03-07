# Contributing LLM Infra Projects: A Roadmap

**Date**: March 7, 2026 at 10:16 PM
**Turns**: 1
**Source**: [Gemini Chat](https://gemini.google.com/app/c235928e446ff0ff)

---

## Turn 1

### 👤 User

actually i really want to build an eval system for train and inference, but i do not so clear how to build it. do you know sglang rl leader chenyang zhao or sglang cuda kernel leader bbuf, or other famous manager like vllm leader kaichao you, sglang leader yin sheng? maybe we can learn to them about how to eval things like cuda usage, band limit, compute limit, model acc, ttft, tpot, stress tests, etc.

### 🤖 Assistant

Building an evaluation system for LLM systems is a high-level task that bridges **performance engineering** (how fast the engine is) and **model alignment** (how good the answer is).
Leaders like **Ying Sheng**, **Chenyang Zhao**, **bbuf (Bo Wen)**, and **Kaichao You** approach this by breaking the problem into specific, measurable layers. Since you have a 4090 and an 8x V100 node, you are in a perfect position to build a "Full-Stack Eval Pipeline."
Here is how you can structure your learning and development, modeled after the experts:

### 1. The Performance Layer (Inference Metrics)
This is the "SGLang/vLLM" specialty. You want to measure the efficiency of the engine.

- **TTFT (Time to First Token):** Measures latency for the "prefill" phase. High TTFT usually means a bottleneck in prompt processing or prompt-cache misses.
- **TPOT (Time Per Output Token):** Measures the "decode" phase. This is usually **memory-bandwidth bound**.
- **Throughput (Tokens/sec):** How many tokens the system can spit out across all users.
- **Experts to follow:**
  - **bbuf (Bo Wen):** Focuses on **CUDA Kernels**. Learn from his work on `sgl-kernel` to see how he uses **NVIDIA Nsight Systems** and **Nsight Compute** to find where the "Bandwidth Limit" or "Compute Limit" is hit.
  - **Kaichao You (vLLM):** Look at the `vllm/benchmarks` folder. They use `benchmark_serving.py` to simulate real-world traffic.

### 2. The Systems Layer (Resource Utilization)
To build a pro eval system, you need to monitor what the hardware is actually doing.

- **CUDA Usage:** Don't just look at `nvidia-smi`. Use **Prometheus + DCGM Exporter** to see "SM Activity" and "Tensor Core Activity."
- **Memory Bandwidth:** Check if you are "IO-Bound." For LLM decoding, you are almost always limited by how fast weights can move from VRAM to the compute units.
- **Stress Testing:** Use your **8x V100s** to test **Tensor Parallelism**. Scale the concurrent requests until the TTFT explodes—this is your "Saturation Point."

### 3. The Accuracy Layer (Model Quality)
An engine is useless if it's fast but "dumb."

- **Model Acc (Accuracy):** Use frameworks like **OpenCompass** or **LM-Eval-Harness**.
- **RL Evaluation:****Chenyang Zhao** (SGLang RL lead) focuses on the "Training-Inference Mismatch." In RLHF, the model might behave differently during "Rollout" (inference) than during "Training." Your eval system should track if the model's performance drops after a training iteration.

---

### How to Build Your "Eval Workbench" (Step-by-Step)

| Phase | Task | Tools to Learn |
| --- | --- | --- |
| Step 1: The Runner | Create a script that sends 1000 prompts to an SGLang/vLLM server. | Python, asyncio, vLLM benchmark scripts |
| Step 2: The Profiler | Capture the hardware stats during the run. | NVIDIA DCGM, Nsight Systems |
| Step 3: The Collector | Store the TTFT, TPOT, and GPU power usage in a database. | SQLite or JSONL (keep it simple for now) |
| Step 4: The Reporter | Generate a "Manhattan-style" or "Waterfall" plot of latencies. | Matplotlib or Streamlit |

### A "Green Hand" Strategy to Connect with Leaders

1. **Read their PRs, not just their code:** Go to the vLLM or SGLang PR history. Search for "Benchmark" or "Profiling." See how **bbuf** explains why a kernel change improved throughput by 5%.
2. **Reproduce their Benchmarks:** Try to get the same numbers they report in their READMEs using your 4090. If your numbers are different, try to figure out why (Is it the PCIe bandwidth? The driver version?).
3. **Contribute to vllm bench or sglang benchmarks:** These areas are often less "scary" than the core C++ code but are highly valued by the maintainers.
**Would you like me to help you write a basic Python script to measure TTFT and TPOT on your 4090 using an SGLang local server?**

---

*Exported from [Gemini Voyager](https://github.com/Nagi-ovo/gemini-voyager)*  
*Generated on March 7, 2026 at 10:16 PM*

---

### GPT

Ah! Now it clicks—you’re not just trying to contribute small fixes, you want to **build a proper evaluation system** for LLM training and inference, similar to what the core contributors of **SGLang** or **vLLM** would do. That’s ambitious but very smart—it’s a way to add **high-impact contributions** even if you’re still learning CUDA or distributed LM systems. Let’s break this down carefully.

---

### **1. Understanding what “evaluation” really means here**

For a high-performance LLM system, evaluation isn’t just “does it run?” It’s **multi-dimensional**:

| Dimension                  | What it measures                                  | Example metric / test                                                          |
| -------------------------- | ------------------------------------------------- | ------------------------------------------------------------------------------ |
| **Throughput**             | How many tokens/sec the system can produce        | `tokens/sec` during inference, `samples/sec` during training                   |
| **Latency**                | Time per request or step                          | `TTFT` (time to first token), `TTOT` (time to output tokens)                   |
| **Resource usage**         | GPU/CPU/memory/bandwidth                          | CUDA memory footprint, SM utilization, bandwidth saturation, power draw        |
| **Accuracy / correctness** | Model outputs vs expected                         | Standard LLM benchmarks (perplexity, F1, BLEU)                                 |
| **Stress / robustness**    | Limits under heavy load                           | Max batch size before OOM, multiple concurrent requests, high sequence lengths |
| **Efficiency**             | Energy or compute efficiency                      | `tflops/W`, `tokens/sec/W`                                                     |
| **Scaling behavior**       | How system behaves with more GPUs or bigger batch | Multi-GPU, model parallel, pipeline parallel                                   |

> Leaders like **Chenyang Zhao (RL systems in SGLang)**, **Bbuf (CUDA kernels)**, and **Kaichao You (vLLM)** would all measure some combination of these.

---

### **2. What you can start building now**

Even without being a CUDA or ML systems master, you can **design a modular eval system**. I’ll break down what that could look like:

#### **a) Architecture**

* **Runner / Orchestrator**: Handles training or inference jobs. Could work on CPU first, then GPU.
* **Profiler**: Collects GPU/CPU metrics (memory, SM utilization, bandwidth).
* **Metrics Collector**: Logs latency, throughput, errors, model output quality.
* **Analyzer / Visualizer**: Plots metrics, compares configurations (TTFT, tpot, stress tests).

#### **b) Tools / libraries you can leverage**

* **PyTorch profiler**: Can measure memory, kernel calls, throughput.
* **NVIDIA Nsight / CUPTI / pynvml**: For CUDA metrics.
* **Timeit / Python perf**: For latency or TTFT measurement.
* **Benchmark datasets**: HuggingFace evaluation sets or synthetic sequences.
* **Stress testing**: Multiple threads or async requests, increasing batch/seq length.

#### **c) Small, incremental approach**

1. Start with **CPU/mini GPU experiments** (GPT2, LLaMA-7B-4bit).
2. Measure **tokens/sec and latency** for small batches.
3. Add **memory profiler** using `torch.cuda.memory_allocated()` and `pynvml`.
4. Gradually add stress tests: bigger batch, longer sequence, concurrent requests.
5. Implement **accuracy metrics**: perplexity or sample evaluation.
6. Optional: integrate simple visualization (matplotlib, Plotly).

---

### **3. Inspiration from core contributors**

You mentioned leaders:

* **Chenyang Zhao (RL / SGLang)** → likely focuses on **system-level efficiency and scheduler evaluation**. You can learn from him by:

  * Implementing **scheduler benchmarks**: e.g., how batch size affects latency and throughput.
  * Evaluating **multi-job scenarios** (RLHF or RL-style training workloads).

* **Bbuf (CUDA kernel / SGLang)** → kernel efficiency:

  * Collect **kernel-level metrics** (latency per op, memory footprint, bandwidth usage).
  * Track performance with **different input sizes**.

* **Kaichao You (vLLM)** → LLM inference system leader:

  * Focused on **serving pipelines**, **TTFT**, **stress tests**, **multi-model concurrency**.

* **Yin Sheng (SGLang lead)** → overall architecture:

  * Interested in **end-to-end system benchmarks**, **trade-offs between speed, accuracy, resource usage**.

> Observation: They all measure **both system efficiency and model quality**.

---

### **4. Your advantage and strategy**

Even if you’re green, you can **build a unified eval system** that:

* Uses **small models for correctness**, then scales to bigger models for stress testing.
* Logs **metrics like TTFT, tpot, GPU memory, SM utilization**.
* Generates **reports/plots** that core developers would find useful.
* Could even serve as a **CI benchmark** in the repo for future PRs.

This is a **high-impact contribution** that doesn’t require you to be a CUDA kernel expert yet—you just need **smart instrumentation, logging, and analysis**.

---

If you want, I can **sketch a concrete “eval system architecture” for SGLang/vLLM** that:

* Works on your current hardware (4090, 3080, V100 nodes).
* Collects **all important metrics**: CUDA usage, bandwidth, TTFT, throughput, accuracy.
* Includes **stress testing and plotting pipelines**.

This would be exactly the blueprint you could start implementing today and later scale to bigger models.

Do you want me to do that?

---

### STUDIO

It is an excellent goal to build an evaluation system. In the world of high-performance systems (like those managed by **Yin Sheng, Kaichao You, bbuf,** and **Chenyang Zhao**), "Evaluation" isn't just a script—it is the compass that guides optimization.

If you want to build an eval system that commands respect from these leaders, you need to measure three distinct layers: **Hardware Efficiency**, **System Throughput**, and **Model Quality**.

Here is how you can approach this, learning from the philosophies of the experts you mentioned.

---

### 1. The "bbuf" Layer: Hardware Efficiency (CUDA & Kernels)
**Zhiyuan (bbuf)** is famous for deep-diving into kernel optimization. To evaluate like him, you need to understand the **Roofline Model**.

*   **The Concept:** Every kernel is limited by either **Arithmetic Intensity** (Compute) or **Memory Bandwidth**.
*   **What to measure:**
    *   **Memory Bandwidth Utilization:** Are you hitting the 900 GB/s limit of your 4090? Or the 900 GB/s (HBM2) of the V100s?
    *   **TFLOPS:** How close are you to the theoretical peak of the Tensor Cores?
*   **How to build it:**
    *   Learn to use `ncu` (NVIDIA Nsight Compute).
    *   **The Task:** Write a script that runs a simple Matrix Multiplication (GEMM) and uses `ncu` to export the "Speed of Light" (SOL) percentages. This is the foundation of CUDA evaluation.

### 2. The "Kaichao You / Yin Sheng" Layer: System Performance
These leaders focus on how the whole system (vLLM/SGLang) handles thousands of requests.

*   **Key Metrics to Implement:**
    *   **TTFT (Time to First Token):** Measures responsiveness (crucial for chat).
    *   **TPOT (Time Per Output Token):** Measures the "reading speed" once the text starts appearing.
    *   **ITL (Inter-Token Latency):** The variance between tokens (consistency).
    *   **Throughput (Tokens/sec):** The total volume the system can handle.
*   **The "Stress Test" Logic:**
    *   You need a **Request Generator**. Don't just send one request. Build a system that sends requests using a **Poisson Distribution** (simulating real human traffic).
    *   **Tools to study:** Look at the `benchmarks/` folder in the [vLLM GitHub](https://github.com/vllm-project/vllm/tree/main/benchmarks). They use `benchmark_serving.py`. Study that file line-by-line.

### 3. The "Chenyang Zhao" Layer: Model Accuracy & RL
If you optimize a system but the model becomes stupid (e.g., through aggressive quantization or FP8), the system is a failure.

*   **What to measure:**
    *   **MMLU / GSM8K:** Standard benchmarks for reasoning.
    *   **Perplexity:** Does the optimized engine produce the exact same probability distribution as the reference (Hugging Face) implementation?
*   **How to build it:**
    *   Integrate **LM-Evaluation-Harness**.
    *   Learn how to track "Reward" if you are looking at RL (Reinforcement Learning).

---

### 4. How to use your specific Hardware for Eval

You have a perfect "Heterogeneous Lab." Use it to find different bottlenecks:

1.  **The 4090 (Linux):** Use this for **Compute Limit** testing. The 4090 has massive raw TFLOPS. Test how fast a kernel can run when it isn't limited by NVLink.
2.  **The 8x V100 (Linux):** Use this for **Communication & Bandwidth** testing.
    *   V100s use NVLink. This is where you test **Tensor Parallelism (TP)**.
    *   *Challenge:* Run a model across 2, 4, and 8 GPUs. Measure the "All-Reduce" time. If the speed doesn't double when you double the GPUs, why? (This is a question Kaichao You asks often).
3.  **The 3080 (WSL):** Use this as the **Client**.
    *   Run the SGLang server on your 4090.
    *   Run your Eval/Stress Test script on the 3080.
    *   This simulates a real-world network environment (Client -> Server).

---

### 5. Your Step-by-Step Learning Path

#### Step A: The "Metrics Python" Phase (Weeks 1-2)
Build a Python tool that wraps a `curl` command to an SGLang server.
*   Log the start time.
*   Log the time when the first chunk of text arrives (TTFT).
*   Log the total time and count tokens (Throughput).
*   Output a CSV or a nice WandB graph.

#### Step B: The "Hardware Profiling" Phase (Weeks 3-4)
Learn `nvidia-smi` and `dcgm-exporter`.
*   While your Python script is running, record the **Power Usage**, **Temperature**, and **Memory Clock**.
*   Learn why "Throttling" happens. (e.g., your 4090 might get too hot and slow down—your eval system should catch this!)

#### Step C: The "Deep Learning System" Phase (Weeks 5+)
Read the SGLang source code, specifically `sglang/test/`.
*   See how they use `pytest` to ensure that a code change didn't break model accuracy.
*   Try to add a "Model Accuracy" check to your benchmarking script.

### Summary of what to say to these Project Leaders:
If you want to engage with them on GitHub or Discord, don't ask "How do I learn?" Instead, ask:
> *"I am benchmarking SGLang on a V100 cluster. I noticed that when scaling from 4 to 8 GPUs, the Inter-Token Latency increases by 20%. Is this expected due to NVLink overhead, or is there a bottleneck in the scheduler?"*

That level of specific, data-driven questioning is how you get the attention of experts like **Yin Sheng** or **bbuf**. They love data. **Build the system that gives them that data.**

