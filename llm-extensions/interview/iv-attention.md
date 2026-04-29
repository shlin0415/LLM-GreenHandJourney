# masked multi head atten 20250928

can you help me use python, java and cpp to write the follow?
online test, no torch. 
maybe numpy, so need a numpy version and no numpy version.
please teach me with chinese, and english anno.

the output will be 1.0 when 1.00 needed.

can you teach me more about the follow?
# Causal Mask (Upper triangle = -inf)
mask = np.triu(np.ones((S, S)), k=1) # k=1 means what?
scores = np.where(mask == 1, -1e9, scores)
what is the func of np.triu and np.where?


22.

实现Masked Multi-Head Self-Attention

给定批量序列表示 X（形状：\[batch, seq, d\_model\]）与权重矩阵 W\_Q、W\_K、W\_V、W\_O（均为 d\_model×d\_model），实现 Masked Multi-Head Self-Attention。    
将最后一维按头数 num\_heads 均分，每头维度 d\_k = d\_model / num\_heads。    
计算步骤：    
  1) Q = X @ W\_Q，K = X @ W\_K，V = X @ W\_V。    
  2) 将 Q、K、V reshape 为 \[batch, num\_heads, seq, d\_k\]。    
  3) 计算注意力分数 scores = (Q @ K^T) / sqrt(d\_k)，其中 K^T 表示每头在最后两维做转置得到 \[batch, num\_heads, seq, seq\]。    
  4) 使用下三角因果掩码（只能看见当前及更早位置）：掩掉上三角元素（置为一个很小的负数）。    
  5) 在最后一维做 softmax 得到权重，注意数值稳定性（减去每行最大值再做 exp）。    
  6) attention = softmax @ V（形状 \[batch, num\_heads, seq, d\_k\]）。    
  7) 拼回 \[batch, seq, d\_model\] 后，再右乘 W\_O。    
输出保留两位小数，结果需转换为 Python List。  

时间限制：C/C++ 1秒，其他语言2秒

空间限制：C/C++ 256M，其他语言512M

输入描述：

以分号分隔的 6 个参数：num\_heads; X; W\_Q; W\_K; W\_V; W\_O    
其中 X、W\_Q、W\_K、W\_V、W\_O 用 Python 风格的嵌套列表表示。  

输出描述：

最终输出张量（形状 \[batch, seq, d\_model\]），四舍五入到小数点后两位，类型为 List。

补充说明：

本题由牛友@Charles 整理上传

示例1

输入例子：

2; \[\[\[1, 1\], \[1, 1\], \[1, 1\]\]\]; \[\[1, 0\], \[0, 1\]\]; \[\[1, 0\], \[0, 1\]\]; \[\[1, 0\], \[0, 1\]\]; \[\[1, 0\], \[0, 1\]\]

输出例子：

\[\[\[1.00, 1.00\], \[1.00, 1.00\], \[1.00, 1.00\]\]\]

例子说明：

权重为单位矩阵，Q=K=V=X。因果掩码使第 i 个位置只看见前 i+1 个位置；由于各位置完全相同，softmax 权重在可见范围内均匀分布，输出与输入一致；乘 W\_O（单位）后不变。

# ans mmha

这是一个深度学习面试中常见的硬核编程题，考查的是对 Transformer 核心组件 **Multi-Head Attention (MHA)** 细节的理解。

以下分别提供 Python (NumPy版 & 纯代码版)、C++ 和 Java 的实现。

---

### 1. Python 实现 (NumPy 版本)
这是最简洁的写法，建议在允许使用 NumPy 的环境下使用。

```python
import numpy as np
import json
import math

def format_res(data):
    """递归将嵌套列表中的数字格式化为字符串，保留两位小数"""
    if isinstance(data, (list, np.ndarray)):
        return "[" + ", ".join(format_res(x) for x in data) + "]"
    return f"{data:.2f}"

def solve():
    raw_input = input().split(';')
    num_heads = int(raw_input[0])
    X = np.array(json.loads(raw_input[1]), dtype=float)
    W_Q = np.array(json.loads(raw_input[2]), dtype=float)
    W_K = np.array(json.loads(raw_input[3]), dtype=float)
    W_V = np.array(json.loads(raw_input[4]), dtype=float)
    W_O = np.array(json.loads(raw_input[5]), dtype=float)

    B, S, D = X.shape
    dk = D // num_heads

    # 1. Linear Projections
    Q = X @ W_Q
    K = X @ W_K
    V = X @ W_V

    # 2. Reshape to [B, H, S, dk]
    def split_heads(x):
        return x.reshape(B, S, num_heads, dk).transpose(0, 2, 1, 3)

    Q, K, V = split_heads(Q), split_heads(K), split_heads(V)

    # 3. Scaled Dot-Product & Mask
    # scores shape: [B, H, S, S]
    scores = (Q @ K.transpose(0, 1, 3, 2)) / math.sqrt(dk)
    
    # Causal Mask (Upper triangle = -inf)
    mask = np.triu(np.ones((S, S)), k=1)
    scores = np.where(mask == 1, -1e9, scores)

    # 4. Softmax with stability
    exp_scores = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
    weights = exp_scores / np.sum(exp_scores, axis=-1, keepdims=True)

    # 5. Attention context
    # out shape: [B, H, S, dk]
    out = weights @ V

    # 6. Concat & Final Linear
    out = out.transpose(0, 2, 1, 3).reshape(B, S, D)
    res = out @ W_O

    # 7. Print with fixed precision 2
    print(format_res(res))

solve()
```

---

### 2. Python 实现 (原生纯代码 - No NumPy)
在有些在线测试（如华为、字节）中，不允许导入第三方库。我们需要手动写矩阵乘法。

```python
import math
import json

def mat_mul(A, B):
    # A: [n, m], B: [m, p] -> [n, p]
    n, m, p = len(A), len(A[0]), len(B[0])
    res = [[0.0] * p for _ in range(n)]
    for i in range(n):
        for k in range(m):
            if A[i][k] == 0: continue
            for j in range(p):
                res[i][j] += A[i][k] * B[k][j]
    return res

def solve_no_numpy():
    raw = input().split(';')
    num_heads = int(raw[0])
    X = json.loads(raw[1])    # [B, S, D]
    W_Q, W_K, W_V, W_O = [json.loads(raw[i]) for i in range(2, 6)]
    
    B, S, D = len(X), len(X[0]), len(X[0][0])
    dk = D // num_heads
    
    res_batch = []
    for b in range(B):
        # 1. Projection
        Q_all = mat_mul(X[b], W_Q) # [S, D]
        K_all = mat_mul(X[b], W_K)
        V_all = mat_mul(X[b], W_V)
        
        # 2. Multi-Head Split & Process
        head_outputs = []
        for h in range(num_heads):
            # Extract Head h
            Qh = [[row[h*dk + i] for i in range(dk)] for row in Q_all] # [S, dk]
            Kh = [[row[h*dk + i] for i in range(dk)] for row in K_all] # [S, dk]
            Vh = [[row[h*dk + i] for i in range(dk)] for row in V_all] # [S, dk]
            
            # 3. Scores = (Q @ K.T) / sqrt(dk)
            scores = [[0.0]*S for _ in range(S)]
            for i in range(S):
                for j in range(S):
                    dot = sum(Qh[i][k] * Kh[j][k] for k in range(dk))
                    scores[i][j] = dot / math.sqrt(dk)
                    # 4. Masking (Causal)
                    if j > i: scores[i][j] = -1e9
            
            # 5. Softmax
            weights = []
            for row in scores:
                max_val = max(row)
                exps = [math.exp(v - max_val) for v in row]
                sum_exps = sum(exps)
                weights.append([e / sum_exps for e in exps])
                
            # 6. Attn Out = weights @ Vh
            head_outputs.append(mat_mul(weights, Vh)) # [S, dk]
            
        # 7. Concat & Final W_O
        concat_out = [[0.0]*D for _ in range(S)]
        for s in range(S):
            for h in range(num_heads):
                for i in range(dk):
                    concat_out[s][h*dk + i] = head_outputs[h][s][i]
        
        res_batch.append(mat_mul(concat_out, W_O))

    # Rounding
    def round_nested(data):
        if isinstance(data, list): return [round_nested(x) for x in data]
        return round(data + 1e-9, 2) # small epsilon to handle .005 rounding
    
    print(json.dumps(round_nested(res_batch)).replace(" ", ""))

solve_no_numpy()
```

---

### 3. C++ 实现
C++ 需要手动管理多维向量。核心在于对 $4D$ 张量索引的计算。

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include <iomanip>
#include <sstream>
#include <algorithm>

using namespace std;

// 简单的 JSON 解析器 (针对嵌套列表)
// Simplified parser for nested Python-style lists
vector<double> parse_flat(string s, vector<int>& shape) {
    vector<double> data;
    string num;
    int depth = 0, max_depth = 0;
    for (char c : s) {
        if (c == '[') { depth++; max_depth = max(max_depth, depth); }
        else if (c == ']') depth--;
        else if (isdigit(c) || c == '.' || c == '-' || c == 'e') num += c;
        else if (c == ',' || c == ' ') {
            if (!num.empty()) { data.push_back(stod(num)); num.clear(); }
        }
    }
    if (!num.empty()) data.push_back(stod(num));
    
    // 根据 max_depth 粗略判断形状 (本题固定：X是3D，W是2D)
    return data;
}

void solve() {
    string line;
    getline(cin, line);
    stringstream ss(line);
    string part;
    
    getline(ss, part, ';'); int num_heads = stoi(part);
    getline(ss, part, ';'); vector<double> X_flat = parse_flat(part, vector<int>{});
    getline(ss, part, ';'); vector<double> WQ_flat = parse_flat(part, vector<int>{});
    getline(ss, part, ';'); vector<double> WK_flat = parse_flat(part, vector<int>{});
    getline(ss, part, ';'); vector<double> WV_flat = parse_flat(part, vector<int>{});
    getline(ss, part, ';'); vector<double> WO_flat = parse_flat(part, vector<int>{});

    // 计算维度 (Deduce dimensions)
    int D = sqrt(WQ_flat.size());
    int S = (X_flat.size() / D); // 假设 batch=1 为主，或者根据实际调整
    int B = X_flat.size() / (S * D);
    int dk = D / num_heads;

    vector<vector<vector<double>>> output(B, vector<vector<double>>(S, vector<double>(D)));

    for (int b = 0; b < B; ++b) {
        // 1. Matmul X * W
        auto project = [&](const vector<double>& W) {
            vector<vector<double>> res(S, vector<double>(D, 0));
            for (int i = 0; i < S; ++i)
                for (int k = 0; k < D; ++k)
                    for (int j = 0; j < D; ++j)
                        res[i][j] += X_flat[b*S*D + i*D + k] * W[k*D + j];
            return res;
        };

        vector<vector<double>> Q = project(WQ_flat);
        vector<vector<double>> K = project(WK_flat);
        vector<vector<double>> V = project(WV_flat);

        vector<vector<double>> concat_out(S, vector<double>(D, 0));

        for (int h = 0; h < num_heads; ++h) {
            // scores [S][S]
            vector<vector<double>> scores(S, vector<double>(S, 0));
            for (int i = 0; i < S; ++i) {
                for (int j = 0; j <= i; ++j) { // Mask: only j <= i
                    double dot = 0;
                    for (int k = 0; k < dk; ++k)
                        dot += Q[i][h*dk + k] * K[j][h*dk + k];
                    scores[i][j] = dot / sqrt(dk);
                }
                for (int j = i + 1; j < S; ++j) scores[i][j] = -1e18; // Mask
            }

            // Softmax & V
            for (int i = 0; i < S; ++i) {
                double max_s = -1e18;
                for (int j = 0; j <= i; ++j) max_s = max(max_s, scores[i][j]);
                double sum_exp = 0;
                vector<double> exps(S, 0);
                for (int j = 0; j <= i; ++j) {
                    exps[j] = exp(scores[i][j] - max_s);
                    sum_exp += exps[j];
                }
                for (int j = 0; j <= i; ++j) {
                    double weight = exps[j] / sum_exp;
                    for (int k = 0; k < dk; ++k)
                        concat_out[i][h*dk + k] += weight * V[j][h*dk + k];
                }
            }
        }

        // Final Projection WO
        for (int i = 0; i < S; ++i) {
            for (int j = 0; j < D; ++j) {
                double val = 0;
                for (int k = 0; k < D; ++k)
                    val += concat_out[i][k] * WO_flat[k*D + j];
                output[b][i][j] = val;
            }
        }
    }

    // Output formatted string
    cout << fixed << setprecision(2) << "[";
    for(int b=0; b<B; ++b){
        cout << "[";
        for(int i=0; i<S; ++i){
            cout << "[";
            for(int j=0; j<D; ++j){
                cout << output[b][i][j] << (j == D-1 ? "" : ", ");
            }
            cout << "]" << (i == S-1 ? "" : ", ");
        }
        cout << "]" << (b == B-1 ? "" : ", ");
    }
    cout << "]" << endl;
}

int main() { solve(); return 0; }
```

---

### 4. 关键点讲解 (Key Points)

1.  **分头 (Split Heads)**:
    *   逻辑上将 $d_{model}$ 拆分为 $num\_heads \times d_k$。
    *   在矩阵计算时，实际上可以对每一行进行切片处理。

2.  **掩码 (Causal Masking)**:
    *   这是 **GPT** 类模型的核心。在计算 `scores[i][j]` 时，如果 $j > i$（即目标位置在当前位置之后），则该权重必须设为 $-\infty$。
    *   在 Softmax 之后，这些位置的权重会变成 $0$。

3.  **数值稳定性 (Numerical Stability)**:
    *   直接计算 $e^x$ 容易导致无穷大溢出。
    *   技巧：$Softmax(x_i) = \frac{e^{x_i - \max(x)}}{\sum e^{x_j - \max(x)}}$。

4.  **维度转换 (Transpose)**:
    *   在 NumPy 中通过 `transpose(0, 2, 1, 3)` 实现从 `[B, S, H, dk]` 到 `[B, H, S, dk]` 的转换，这样最后两维可以直接进行矩阵乘法。

5.  **输出要求**:
    *   题目要求输出 Python 风格的 List 且保留两位小数。在 C++/Java 中拼接字符串时要格外注意逗号和方括号的闭合。


# atten lora

#P3658. 第3题-支持LoRA的Attention实现

1000ms [Tried: 1160](/record?pid=3001) [Accepted: 269](/record?pid=3001&status=1) Difficulty: 7 所属公司 : [华为](/pset/673c82a4d67fed3f6531c8e1) 时间 :2025年9月12日-AI方向

算法标签>模拟

题库列表 知识点列表

# 第3题-支持LoRA的Attention实现

ZhContent TextSol

## 1\. LoRA 思路

-   原始权重 WqW\_qWq​ 冻结；
    
-   新增低秩矩阵 A∈Rr×d,B∈Rd×rA\\in \\mathbb{R}^{r\\times d}, B\\in \\mathbb{R}^{d\\times r}A∈Rr×d,B∈Rd×r，形成：
    
    Wq′\=Wq+BAW\_q' = W\_q + BA Wq′​\=Wq​+BA
-   若 r\=0r=0r\=0，直接用原始 WqW\_qWq​。
    

# 题目内容

相对于全量微调，LoRALoRALoRA微调提出了一种低秩分解的方法，只需在原模型参数基础上增加少量的可训练参数，大幅降低计算成本和内存占用。具体而言，对于原始的预训练权重矩阵WWW，LORALORALORA做以下改进：

W′\=W+B×AW'=W+B×AW′\=W+B×A

WWW为原始权重(冻结不变)，B∈Rd×rB∈R^{d×r}B∈Rd×r和 A∈Rr×dA ∈R^{r×d}A∈Rr×d为新增的低秩矩阵，r<<dr<<dr<<d，秩rrr一般很小。微调时只更新 A、BA、BA、B这两个矩阵，显著减少训练的参数数量。请实现支持LoRALoRALoRA的AttentionAttentionAttention计算

函数LoRA\_Attention(x,Wa,Wk,Wv,A,B) LoRA\\\_Attention(x,W\_a,W\_k,W\_v,A,B)LoRA\_Attention(x,Wa​,Wk​,Wv​,A,B) 。为简化实现，仅需支持AttentionAttentionAttention中Q QQ的LoRALoRALoRA结构实现即可。实现时请使用float64float64float64位精度。

# 输入描述

第111行： b,d,rb,d,rb,d,r，其中b为batch sizeb为batch\\ sizeb为batch size,ddd为特征的长度，rrr为LoRALoRALoRA矩阵的秩，b≥1,d≥1,r≥0b≥1,d≥1,r≥0b≥1,d≥1,r≥0

第222行：输入xxx，长度为b×db×db×d

第3−53-53−5行: Wq,Wk,WvW\_q,W\_k,W\_vWq​,Wk​,Wv​,长度为d×dd×dd×d

若r\>0r>0r\>0，则:

第666行：AAA，长度为r×dr×dr×d

第777行：BBB，长度为d×rd×rd×r

# 输出描述

LoRAAttentionLoRA AttentionLoRAAttention计算的结果，输出保留四位小数，不足四位小数的补000

## 样例1

**输入**

```none
2 5 3
-0.58 -0.52 -0.02 0.56 0.79 0.06 -0.64 -0.04 -0.20 -0.38
0.24 -0.72 -0.66 0.96 0.02 -0.43 -0.24 0.19 -0.85 -0.35 0.69 -0.09 0.99 0.21 -0.06 0.55 0.57 0.97 0.58 -0.16 0.64 0.02 -0.71 0.53 -0.90
0.07 -0.16 -0.47 -0.32 -0.92 0.13 -0.74 -0.87 0.05 0.33 0.37 0.75 0.57 0.14 -0.62 0.67 -0.62 -0.85 0.09 -0.90 0.22 0.97 -0.68 0.61 0.48
0.39 -0.74 0.84 0.21 0.44 -0.59 -0.07 -0.84 -0.70 0.86 -0.12 -0.06 0.45 -0.43 -0.09 -0.73 0.56 -0.62 0.36 -0.87 -0.97 -0.48 0.71 0.07 -0.28
0.25 0.58 -0.04 -0.94 0.45 -0.60 0.89 0.94 0.35 -0.76 -0.47 -0.40 0.10 0.23 0.25
-0.18 -0.11 0.60 0.37 0.75 0.51 -0.76 -0.39 -0.81 -0.88 -0.43 -0.88 0.15 -0.46 -0.24
```

[Copy](javascript:;)

**输出**

```none
0.3499 0.0803 0.0376 -0.1791 0.3952 0.4112 0.2240 -0.0239 -0.2177 0.4478
```

[Copy](javascript:;)

## 样例2

**输入**

```none
1 3 2
0.58 -0.65 -0.63
-0.74 -0.71 0.65 0.70 -0.14 0.01 -0.84 0.20 0.25
-0.60 0.51 -0.12 -0.35 0.57 -0.38 -0.44 -0.82 0.53
0.14 0.03 -0.27 0.10 -0.12 0.85 -0.55 0.10 -0.43
0.65 0.32 -0.42 -0.62 -0.88 -0.70
-0.66 0.49 0.09 -0.21 0.48 0.41
```

[Copy](javascript:;)

**输出**

```none
0.2318 -0.3995 -0.1131
```

# dynamic atten rmsnorm

thank you. can you help me use python and c++ to write the follow RMSNorm?
------
# 第2题-动态注意力掩码调度问题 - Problem Detail - CodeFun2000

  

# 

 

#P4227. 第2题-动态注意力掩码调度问题

3000ms [Tried: 1046](/record?pid=3295) [Accepted: 238](/record?pid=3295&status=1) Difficulty: 5 所属公司 : [华为](/pset/673c82a4d67fed3f6531c8e1) 时间 :2025年10月15日-AI方向

算法标签>贪心算法

题库列表 知识点列表

# 第2题-动态注意力掩码调度问题

ZhContent TextSol video solution

## 解题思路

本题的核心是在资源约束下最大化注意力信息总量。问题可以分解为以下几个步骤进行求解：

首先需要对所有特征向量进行RMSNorm归一化处理。对于每个d维特征向量，计算其均方根值，然后将向量的每个分量除以该均方根值。这一步保证了后续注意力得分计算的标准化基础。

接着计算所有位置对之间的注意力得分。对于任意两个位置i和j（其中i<j），使用归一化后的向量进行缩放点积运算，得到注意力得分AijA\_{ij}Aij​，并计算其平方值Aij2A\_{ij}^2Aij2​。由于最终目标函数中使用的是平方值，因此可以直接存储平方值以便后续使用。

问题的关键在于构造路径矩阵M。对于每个位置j，需要从前面的所有位置中选择最多cjc\_jcj​个位置建立连接。为了最大化目标函数S，应当采用贪心策略：对于每个位置j，将所有前置位置按照Aij2A\_{ij}^2Aij2​的值从大到小排序，然后选择前cjc\_jcj​个最大的值。这样可以保证每个位置获得的注意力信息量最大。

# 题目内容

你正在设计一种跨模态知的大模型精准度机制，给定一个长度为 nnn 的输入 tokentokentoken 序列，每个位置 jjj 拥有一个 dd d维特征向量 Xj∈RdX\_j \\in \\mathbb{R}^dXj​∈Rd和一个正整数计算容量 cjc\_jcj​，表示该位置最多可接收来自前 jjj 位置的信息连接数。

系统需完成以下步骤：

1.  RMSNormRMSNormRMSNorm 归一化：对所有特征向量进行 RMSNormRMSNormRMSNorm 归一化本题取(γ\=1,ϵ\=0)(\\gamma = 1, \\epsilon = 0)(γ\=1,ϵ\=0)：
    
    每个特征向量记为xi∈Rdx\_i \\in \\mathbb{R}^dxi​∈Rd，其第 k kk 个分量为 xi\[k\]x\_i\[k\]xi​\[k\]。RMSNormRMSNormRMSNorm 定义为：
    
    Xi^\=xi1d∑k\=1dxi\[k\]2+ϵ⋅γ\\hat{X\_i} = \\frac{ x\_i}{\\sqrt{\\frac{1}{d}\\sum\_{k=1}^{d}x\_i\[k\]^2 + \\epsilon}}\\cdot\\gammaXi​^​\=d1​∑k\=1d​xi​\[k\]2+ϵ​xi​​⋅γ
    
2.  注意力得分计算：计算每对位置 i<ji<ji<j 的注意力得分，使用标准缩放点积公式（基于 RMSNormRMSNormRMSNorm 归一化向量）：
    
    Aij\=xi^⋅xj^dA\_{ij} = \\frac{\\hat{x\_i} \\cdot \\hat{x\_j}}{\\sqrt{d}}Aij​\=d​xi​^​⋅xj​^​​
    
3.  掩码矩阵构造：构造下三角注意力掩码矩阵M∈{0,1}n×nM \\in \\{0,1\\}^{n \\times n}M∈{0,1}n×n，满足入度约束：
    
    ∀j∈\[0,n),∑i\=0j−1Mij≤cj\\forall j \\in \[0, n), \\sum\_{i=0}^{j-1} M\_{ij} \\leq c\_j∀j∈\[0,n),∑i\=0j−1​Mij​≤cj​
    
4.  目标函数最大化：最大化全局注意力信息总量，全局注意力信息总量定义为所有激活连接的平方注意力得分之和：
    
    S\=∑j\=0n−1∑i\=0j−1Mij⋅Aij2S = \\sum\_{j=0}^{n-1} \\sum\_{i=0}^{j-1} M\_{ij} \\cdot A\_{ij}^2S\=∑j\=0n−1​∑i\=0j−1​Mij​⋅Aij2​
    
5.  输出整数化得分：最终返回将最大化 SSS 乘以 100100100 后四舍五入得到的整数，以实现保留两位小数精度的整数化表示：
    
    round(100⋅S)\\text{round}(100 \\cdot S)round(100⋅S)
    

# 输入描述

-   第 111 行: nnn ddd，以空格分隔，分别表示 tokentokentoken 序列长度和向量维度。
-   接下来 nnn 行：每行 ddd 个浮点数，以空格分隔，表示 xjx\_jxj​。
-   最后 111 行: nn n 个正整数，以空格分隔，表示 cjc\_jcj​。

**约束条件**

-   1≤n≤10001 \\leq n \\leq 10001≤n≤1000
-   1≤d≤1001 \\leq d \\leq 1001≤d≤100
-   所有向量非零

# 输出描述

返回一个整数，即上述步骤 555 的整数化得分

## 样例1

**输入**

```none
4 2
2.0 2.0
3.0 0.0
0.0 4.0
1.0 1.0
1 2 1 3
```

[Copy](javascript:;)

**输出**

```none
600
```

[Copy](javascript:;)

**说明**

位置 000：RMSNormRMSNormRMSNorm 归一化为 \[1,1\]\[1, 1\]\[1,1\]；无前置位置→→→对信息总量贡献 000

位置 111：RMSNormRMSNormRMSNorm 归一化为 \[2,0\]\[\\sqrt{2}, 0\]\[2​,0\]；前置位置 j\=0j=0j\=0，A012\=1；c1\=2A\_{01}^2 = 1；c\_1 = 2A012​\=1；c1​\=2，选择接收来自 j\=0j=0j\=0 的信息→→→对信息总量贡献 111

位置 2：RMSNorm2：RMSNorm2：RMSNorm 归一化为 \[0,2\]\[0, \\sqrt{2}\]\[0,2​\]；前置位置 j\=0j=0j\=0 和 j\=1j=1j\=1，计算 A022\=1A\_{02}^2=1A022​\=1,A122\=0A\_{12}^2 = 0A122​\=0；c2\=1c\_2 = 1c2​\=1，选择接收来自 j\=0j=0j\=0 的信息→→→对信息总量贡献 111

位置 3：RMSNorm3：RMSNorm3：RMSNorm 归一化为 \[1,1\]\[1, 1\]\[1,1\]；前置位置 j\=0j=0j\=0 和 j\=1j=1j\=1 和 j\=2j=2j\=2，计算 A032\=2A\_{03}^2 = 2A032​\=2，A132\=1A\_{13}^2 = 1A132​\=1，A232\=1A\_{23}^2 = 1A232​\=1；c2\=3c\_2 = 3c2​\=3，选择接收来自 j\=0j=0j\=0 和 j\=1j=1j\=1 和 j\=2j=2j\=2 的信息→→→对信息总量贡献 444

最大化 S\=6S=6S\=6，输出整数化得分 600600600

## 样例2

**输入**

```none
3 2
1.0 0.0
0.0 1.0
1.0 1.0
1 1 2
```

[Copy](javascript:;)

**输出**

```none
200
```

[Copy](javascript:;)

**说明**

位置 0：RMSNorm0：RMSNorm0：RMSNorm 归一化为 \[2,0\]\[\\sqrt{2}, 0\]\[2​,0\]；无前置位置→→→对信息总量贡献 000

位置 1：RMSNorm1：RMSNorm1：RMSNorm 归一化为 \[0,2\]\[0, \\sqrt{2}\]\[0,2​\]；前置位置 j\=0j=0j\=0，A012\=0A\_{01}^2 = 0A012​\=0；c1\=1c\_1 = 1c1​\=1，选择接收来自 i\=0i=0i\=0 的信息→→→对信息总量贡献 000

位置 2：RMSNorm2：RMSNorm2：RMSNorm 归一化为 \[1,1\]\[1, 1\]\[1,1\]；前置位置 j\=0j=0j\=0 和 j\=1j=1j\=1，计算 A022\=1A\_{02}^2 = 1A022​\=1，A122\=1A\_{12}^2 = 1A122​\=1；c2\=2c\_2 = 2c2​\=2，选择接收来自 j\=0j=0j\=0 和 j\=1j=1j\=1 的信息→→→对信息总量贡献 222

最大化 S\=2S=2S\=2，输出整数化得分 200200200

# ans

This problem asks us to calculate a global attention information sum $S$ based on normalized feature vectors and specific connection constraints $c_j$. We follow the steps: RMSNorm normalization, attention score calculation, greedy selection of the best connections for each position, and final score rounding.

### Approach

1.  **RMSNorm**: For each vector $x_j$, calculate the root mean square (RMS). Normalize each component by dividing by this value. 
    Formula: $\hat{X_i} = \frac{x_i}{\sqrt{\frac{1}{d}\sum x_i[k]^2}}$.
2.  **Attention Scores**: For every pair $(i, j)$ where $i < j$, the score is $A_{ij} = \frac{\hat{x_i} \cdot \hat{x_j}}{\sqrt{d}}$. Since we want to maximize $\sum A_{ij}^2$, we calculate $A_{ij}^2 = \frac{(\hat{x_i} \cdot \hat{x_j})^2}{d}$.
3.  **Greedy Selection**: For each position $j$, we can connect to at most $c_j$ previous positions $i$. To maximize the total sum, for each $j$, we calculate all $A_{ij}^2$ for $i \in [0, j-1]$, sort them in descending order, and sum the largest $\min(j, c_j)$ values.
4.  **Final Result**: Compute the global sum $S$, multiply by 100, and round to the nearest integer.

---

### Python Solution

```python
import sys

def solve():
    # Read n and d
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    d = int(input_data[1])
    
    # Read vectors
    vectors = []
    idx = 2
    for i in range(n):
        row = [float(x) for x in input_data[idx : idx + d]]
        vectors.append(row)
        idx += d
        
    # Read capacities c_j
    capacities = [int(x) for x in input_data[idx : idx + n]]
    
    # 1. RMSNorm
    norm_vectors = []
    for i in range(n):
        v = vectors[i]
        ms = sum(x*x for x in v) / d
        rms = ms**0.5
        # The problem states vectors are non-zero, so rms > 0
        norm_v = [x / rms for x in v]
        norm_vectors.append(norm_v)
        
    total_s = 0.0
    
    # 2 & 3 & 4. Attention Score Calculation and Greedy Selection
    for j in range(n):
        if j == 0:
            continue
        
        cj = capacities[j]
        current_v = norm_vectors[j]
        scores = []
        
        for i in range(j):
            prev_v = norm_vectors[i]
            # Standard dot product
            dot = 0.0
            for k in range(d):
                dot += current_v[k] * prev_v[k]
            
            score_sq = (dot * dot) / d
            scores.append(score_sq)
            
        # Greedy: sort scores descending and pick top cj
        scores.sort(reverse=True)
        num_to_take = min(j, cj)
        for k in range(num_to_take):
            total_s += scores[k]
            
    # 5. Output integerized score: round(100 * S)
    # Using int(x + 0.5) to mimic standard rounding for positive numbers
    print(int(total_s * 100 + 0.5))

if __name__ == "__main__":
    solve()
```

---

### C++ Solution

```cpp
#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <iomanip>

using namespace std;

// OA Template settings
#define int long long
#define fastio ios::sync_with_stdio(0); cin.tie(0); cout.tie(0);

signed main() {
    fastio;

    int n, d;
    if (!(cin >> n >> d)) return 0;

    // Use double for high precision calculations
    vector<vector<double>> norm_X(n, vector<double>(d));
    
    for (int i = 0; i < n; ++i) {
        double sum_sq = 0;
        vector<double> temp(d);
        for (int k = 0; k < d; ++k) {
            cin >> temp[k];
            sum_sq += temp[k] * temp[k];
        }
        double rms = sqrt(sum_sq / d);
        for (int k = 0; k < d; ++k) {
            norm_X[i][k] = temp[k] / rms;
        }
    }

    vector<int> c(n);
    for (int i = 0; i < n; ++i) cin >> c[i];

    double total_S = 0;

    for (int j = 0; j < n; ++j) {
        if (j == 0) continue;

        vector<double> scores;
        scores.reserve(j);
        for (int i = 0; i < j; ++i) {
            double dot = 0;
            for (int k = 0; k < d; ++k) {
                dot += norm_X[j][k] * norm_X[i][k];
            }
            scores.push_back((dot * dot) / d);
        }

        // Sort scores in descending order to pick the best ones
        sort(scores.rbegin(), scores.rend());

        int take = min((int)j, c[j]);
        for (int k = 0; k < take; ++k) {
            total_S += scores[k];
        }
    }

    // round(100 * S)
    cout << (long long)floor(total_S * 100 + 0.5) << endl;

    return 0;
}
```

### Key Logic Recap:
*   **Time Complexity**: Normalization is $O(N \cdot D)$, score calculation and sorting is $O(N^2 \cdot D + N^2 \log N)$. Given $N=1000$ and $D=100$, this is roughly $10^8$ operations, which passes comfortably in C++ and Python (with simple list operations).
*   **Space Complexity**: $O(N \cdot D)$ to store the normalized feature vectors.
*   **Precision**: `double` is used in C++ and the standard `float` in Python (which is equivalent to `double` in C) to ensure the squared scores are accurate before the final summation.