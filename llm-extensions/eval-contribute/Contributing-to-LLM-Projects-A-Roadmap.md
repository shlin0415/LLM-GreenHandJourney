# Contributing to LLM Projects: A Roadmap

**Date**: March 7, 2026 at 09:08 PM
**Turns**: 1
**Source**: [Gemini Chat](https://gemini.google.com/app/c235928e446ff0ff)

---

## Turn 1

### 👤 User

you are an llm open source project expert, can you help me? thanks. how should i learn to try to contribute to famous and difficult projects like sglang and vllm when i do not have enough knowledge (a little ml python, green hand for lm sys and cuda) and do not have good devices (1 4090 linux, 1 3080 win wsl, 8 v100 linux) ?

### 🤖 Assistant

It is completely normal to feel like a "green hand" when looking at massive, cutting-edge repositories like `vllm` or `sglang`. These are highly complex systems, but contributing to them is entirely achievable if you break the process down into manageable phases.
First, let's reframe your hardware situation. You actually have a fantastic setup for open-source LLM systems development.

### Your Hardware Arsenal

- **1x 4090 (Linux):** This is your primary workhorse. The 4090 has 24GB of VRAM and modern Ada Lovelace architecture, making it perfect for debugging core logic, running local tests, and working with 7B-8B parameter models.
- **8x V100 (Linux):** While older, an 8-GPU node is incredibly valuable for LLM systems development. This is your dedicated cluster for testing Tensor Parallelism (TP) and Pipeline Parallelism (PP) implementations. Many contributors do not have access to multi-GPU setups to verify distributed inference bugs.
- **1x 3080 (Win WSL):** This is your ideal daily driver for reading code, writing documentation, and running lightweight Python unit tests using your preferred AI coding assistants and development environments.

### The "Green Hand" Roadmap to Contribution
You do not need to be a CUDA expert to make meaningful contributions. Both `vllm` and `sglang` have massive amounts of Python infrastructure, API routing, and scheduling logic.
**1. Leverage Your AI Tools for Codebase Navigation**
Large projects can be overwhelming. Use advanced IDEs and AI coding assistants to map out the repository. Ask your assistant to explain the execution flow from the moment an API request is received to the moment the model generates a token. Ensure you maintain strict safety protocols when using autonomous tools in your Linux environments—always back up configuration files and avoid destructive commands while the AI explores the repo.
**2. Start with the "Periphery" (Low-Hanging Fruit)**
Do not start by trying to write custom CUDA kernels. Begin where your current Python knowledge applies:

- **Documentation:** Read the docs while setting the project up on your 4090. If you hit a snag, update the documentation. This is one of the most appreciated contributions.
- **Reproducing Bugs:** Go to the GitHub Issues tab. Find newly reported bugs and try to reproduce them on your hardware. Provide the maintainers with error logs and environment details.
- **Adding Tests:** Write Python unit tests for untested utility functions. This builds your understanding of how the internal components work.
**3. Master the Core Concepts Conceptually**
Before diving into the code, make sure you deeply understand the theoretical bottlenecks in LLM inference.

- Study **PagedAttention**: Understand how `vllm` manages KV cache memory like an operating system manages virtual memory.
- Study **Continuous Batching**: Learn how requests are dynamically batched at the iteration level rather than the request level.
**4. Move to Python-Level Systems Engineering**
Once comfortable, look for issues labeled "good first issue" or "help wanted" that deal with Python infrastructure.

- Both projects need continuous work on their OpenAI-compatible API servers (using FastAPI).
- Look into the scheduling logic. For instance, testing how models behave under different parallel strategies using your 8x V100 setup.
**5. Slowly Introduce CUDA**
If you want to move down the stack, start by reading existing custom kernels. Look at how PyTorch binds to CUDA via pybind11. You can begin by simply adding profiling markers or optimizing how Python calls these kernels before writing your own C++ code.

### Recommended Daily Practice

1. **Sync the Repo:** Pull the latest `main` branch daily. Run the build process from source on your Linux machines. Getting comfortable with the build system (CMake, Ninja) is a crucial first step.
2. **Read Pull Requests (PRs):** Instead of just reading raw code, read merged PRs. Look at the description, the files changed, and the reviewer comments. This shows you exactly how real contributions are made.
3. **Document Your Journey:** Keeping a detailed markdown log of your learning process, commands run, and concepts mastered will help cement your transition from beginner to systems developer.
Would you like me to help you set up a local development environment for `vllm` on your 4090 machine, or should we look at GitHub together to find a "good first issue" that matches your current Python skills?

---

*Exported from [Gemini Voyager](https://github.com/Nagi-ovo/gemini-voyager)*  
*Generated on March 7, 2026 at 09:08 PM*

---

### GPT

Absolutely! You’re in a very common situation—eager to contribute to advanced open-source LLM projects but feeling green and constrained by hardware. The good news is: this is totally manageable if you approach it smartly. I’ll break it down step by step.

---

### **1. Understand the projects first, without fear of hardware limitations**

Projects like **SGLang** (a low-level LM runtime) and **vLLM** (efficient LLM serving and scheduling) are advanced and involve CUDA, distributed systems, and inference optimizations. Your first step is **conceptual understanding**:

* **Read the docs deeply**: Focus on design docs, READMEs, architecture diagrams, and system explanations. Even if you can’t run large models yet, understanding the logic and modules is crucial.
* **Follow simple tutorials**: Many of these projects have “quickstart” guides. Try them with small models like `gpt2-small` or `llama-7b` (4-bit) to avoid hardware bottlenecks.
* **Trace the code paths**: Start with the entry points of the system. For vLLM, for example, trace request handling → model loading → scheduler → inference.

---

### **2. Set up a hardware-efficient learning environment**

You don’t need a 4090 or a cluster of GPUs to start contributing:

* **Use small models**: e.g., `GPT2`, `LLaMA-7B-4bit`, `MPT-7B-4bit`. Tiny weights still let you test code changes.
* **Leverage CPU or mixed CPU+GPU**: Some modules (like schedulers, data loaders, quantization scripts) can be developed without a GPU.
* **Use your V100 nodes wisely**: These are great for testing real performance or distributed code. You can prepare and test small patches locally, then validate on V100.
* **Use cloud-free options**: Google Colab (free tier) can run smaller experiments if needed.

---

### **3. Focus on “low-hanging fruit” contributions**

Even in advanced projects, there are ways to contribute without being an expert:

1. **Documentation improvements**: Clearer docs, tutorials, setup instructions. Huge impact and easy to start.
2. **Bug reports and reproductions**: Try running examples on small setups, report errors or inconsistencies.
3. **Unit tests or CI improvements**: Every project needs better test coverage. You can write tests for CPU execution or edge cases.
4. **Small code improvements**: Refactoring, adding type hints, error handling, or helper functions.
5. **Model support additions**: e.g., integrating a tiny model or tokenizer for testing.

> These contributions will teach you the codebase and gain credibility before you tackle CUDA-heavy optimizations.

---

### **4. Learn strategically**

Since you’re green in ML systems and CUDA:

* **Python + ML basics**: Focus on PyTorch and Transformers API.
* **CUDA + memory management**: Learn tensor operations, kernel launches, and device memory handling. NVIDIA docs and tutorials are gold.
* **LLM runtime concepts**: Study attention, model parallelism, quantization, and batching. Even reading `vLLM`’s scheduler code gives insight.
* **Version control & CI**: Open-source contribution is 70% Git/GitHub skills—branches, pull requests, code reviews.

**Tip:** Treat this like a multi-year learning journey. Your early contributions don’t have to be high-performance code—they’re about learning the architecture.

---

### **5. Smart collaboration**

* **Engage on GitHub Issues / Discussions**: Ask clarifying questions or suggest small improvements.
* **Pair contributions with mentors**: Some repos are friendly to “first-timers” and will guide small PRs.
* **Track your learning via small PRs**: Even if trivial, they build credibility and confidence.

---

### **6. Experiment with “proxy setups”**

If your local GPUs are limited, you can:

* Run **1-layer toy models** to mimic attention behavior.
* Test **scheduler, batching, memory allocation** logic without full LLMs.
* Benchmark **tiny datasets** before scaling.

> This is exactly how many contributors learn: the logic is the same, only the scale is smaller.

---

### **7. Recommended path for you**

1. Pick **vLLM or SGLang**, read architecture and tutorials.
2. Run **tiny models** locally on 4090 / 3080.
3. Try **documentation / bugfix contributions** first.
4. Learn PyTorch + CUDA incrementally.
5. Move to **small performance patches**, then eventually distributed or attention optimizations.

---

If you want, I can **draft a concrete 3-month roadmap** tailored to your current setup and skill level, showing exactly what you can contribute week by week to vLLM or SGLang—even with limited hardware.

Do you want me to do that?

---
### STUDIO

Contributing to high-performance inference engines like **vLLM** and **SGLang** as a "green hand" is a marathon, not a sprint. These projects sit at the intersection of Deep Learning, Distributed Systems, and High-Performance Computing (HPC).

Since you have access to decent hardware (especially the 8 V100s and a 4090), you are in a better position than most beginners. Here is a structured roadmap to move from "green hand" to a meaningful contributor.

---

### Phase 1: The Knowledge Foundation (Crawl)
Don't jump into the C++/CUDA code immediately. Most of the complexity in vLLM/SGLang is actually in the **Python management layer**.

1.  **Understand the Architecture:**
    *   **KV Cache:** Learn why it's the bottleneck. Read about "PagedAttention" (vLLM) and "RadixAttention" (SGLang).
    *   **Continuous Batching:** Learn how these engines handle multiple requests of different lengths without waiting for the longest one to finish.
    *   **The Model Logic:** Study the `model.py` files in Hugging Face Transformers for a simple model like Llama. Understand how tensors flow through the layers.
2.  **Recommended Resources:**
    *   **[Fast LLM Inference From Scratch](https://andrewkchan.dev/posts/yalm.html):** A brilliant guide on building a tiny inference engine using C++/CUDA. It demystifies the kernels.
    *   **[vLLM Paper](https://arxiv.org/abs/2309.06180):** Focus on the "PagedAttention" concept. It’s the "Hello World" of modern LM systems.
    *   **Tinygrad (optional):** Browsing the codebase of Tinygrad can help you see how low-level operations are abstracted.

---

### Phase 2: Mastering Your Hardware (Walk)
You have three distinct environments. Use them strategically:

| Device | Best Use Case | Limitations to Know |
| :--- | :--- | :--- |
| **1x RTX 4090 (Linux)** | **Primary Dev Machine.** Best for debugging kernels and testing FP8 features. | 24GB VRAM limits you to 7B-14B models for full testing. |
| **8x Tesla V100 (Linux)** | **Distributed Testing.** Best for testing Multi-GPU features (Tensor Parallelism). | **No BF16 support.** Must use `--dtype float16`. No FlashAttention-2 support (uses xFormers fallback). |
| **RTX 3080 (WSL)** | **Docs & Frontend.** Use this for writing documentation or testing the OpenAI-compatible API. | WSL can have CUDA overhead; avoid performance-critical profiling here. |

**Pro Tip for V100s:** Since V100s only have 16GB or 32GB of VRAM and lack BF16, use **Quantization** (AWQ/GPTQ) to fit larger models. Testing how quantization affects different models is a great way to start contributing.

---

### Phase 3: Strategic Entry Points (Run)
Don't try to rewrite the memory manager. Start where the maintainers need the most help but have the least time.

1.  **Documentation & Examples:**
    *   SGLang often needs "Cookbook" examples (e.g., "How to use SGLang for RAG with DeepSeek").
    *   If you struggle to install something, **that is a bug**. Fix the installation guide or the error message once you solve it.
2.  **Model Support:**
    *   New models come out weekly. Adding support for a new model (e.g., a new architecture from Hugging Face) is often just writing a new Python class that maps the weights to vLLM's internal layers.
    *   Check "Model Request" issues on GitHub.
3.  **"Good First Issues":**
    *   Filter GitHub issues with the `good first issue` label.
    *   Look for **Bugfixes** in the Python layer (e.g., fixing an API endpoint that returns the wrong status code).
4.  **Unit Tests:**
    *   vLLM and SGLang have massive test suites. Adding a test case for a specific edge case (like a very long prompt causing an OOM) is a high-value contribution.

---

### Phase 4: Development Workflow
Setting up your environment correctly is 50% of the battle.

*   **Use `uv`:** vLLM specifically recommends using the `uv` package manager for incredibly fast environment setup.
*   **Incremental Compilation:** If you touch C++/CUDA code, learn how to do incremental builds so you don't wait 20 minutes for every change.
*   **Debug Mode:** Use environment variables to see what's happening under the hood:
    ```bash
    export VLLM_LOGGING_LEVEL=DEBUG
    export CUDA_LAUNCH_BLOCKING=1  # Makes CUDA errors easier to trace to a line of code
    ```

---

### The "Secret" to Getting Merged
1.  **Join the Community:** Join the [vLLM Discord](https://discord.gg/vllm) or [LMSYS (SGLang) Slack](https://lmsys.org/slack).
2.  **The "Lurker" Strategy:** Spend a week reading every Pull Request that gets merged. Look at the comments from senior maintainers (like @simon-mo or @merrymercy). Notice what they ask contributors to change.
3.  **Small PRs:** Your first PR should be tiny (5-10 lines). It builds trust. Maintainers are busy; they will review a 10-line fix in a day, but a 500-line "improvement" might sit for months.

**Summary for you:** Start by running a 7B model on your 4090 using SGLang. Try to break it with weird prompts. When it breaks, figure out why in the Python logs. That "why" is your first contribution.
