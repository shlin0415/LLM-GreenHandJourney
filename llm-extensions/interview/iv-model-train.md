# model train 1

你能教教我如何在线上机考做这题吗？
使用python, java和cpp写, 非常感谢。

21.

医疗诊断模型的训练

某医疗系统要用一次“线性映射 + 线性分类”结构对问卷症状序列做三步计算：前向预测、MSE 损失、一次 SGD 权重更新。设一条问卷包含 L 条症状记录，每条症状是 D 维向量。先用一个 D×D 的权重矩阵把每条症状做线性变换，再用一个 D×K 的权重矩阵得到 K 维分类打分。把所有记录的打分在“症状条目维度”求平均，得到最终的 K 维预测向量（不做 softmax 归一化）。随后与给定的 K 维真实向量做 MSE 损失，并用学习率 η 进行一次 SGD 更新这两个权重矩阵（均无偏置）。

时间限制：C/C++ 1秒，其他语言2秒

空间限制：C/C++ 256M，其他语言512M

输入描述：

-   输入第 1 行：L,D,K,η
-   第 2 行：真实向量 y（K 个数）
-   第 3 行：序列矩阵 X（按行展平，共 L×D 个数）
-   第 4 行：映射矩阵 W\_mlp（按行展平，共 D×D 个数）
-   第 5 行：分类矩阵 W\_cls（按行展平，共 D×K 个数）

计算规则（均为行优先展平与输出，四舍五入保留 2 位小数）：

-   H = X @ W\_mlp（逐行相乘），h\_mean = 每行 H 的平均（1×D）
-   y\_pred = h\_mean @ W\_cls（1×K）
-   MSE = (1/K) \* Σ(y\_pred\[i\] − y\[i\])^2
-   令 g = (2/K) \* (y\_pred − y)（1×K）
-   grad\_W\_cls = 外积(h\_mean, g)（D×K）
-   令 x\_mean = 每行 X 的平均（1×D），u = g @ W\_cls^T（1×D）  
    grad\_W\_mlp = 外积(x\_mean, u)（D×D）
-   参数更新：W\_mlp -= η \* grad\_W\_mlp，W\_cls -= η \* grad\_W\_cls

输出描述：

输出共 4 行：  
1) y\_pred（K 个数）    
2) MSE（1 个数）    
3) 更新后的 W\_mlp（D×D 个数，行优先）    
4) 更新后的 W\_cls（D×K 个数，行优先）  

补充说明：

本题由牛友@Charles 整理上传

示例1

输入例子：

1,2,3,0.3
0.5,1.5,2.0
1.0,2.0
1.0,0.0,0.0,1.0
1.0,0.0,0.0,0.0,1.0,1.0

输出例子：

1.00,2.00,2.00
0.17
0.90,-0.10,-0.20,0.80
0.90,-0.10,0.00,-0.20,0.80,1.00

例子说明：

h\_mean = \[1,2\]；y\_pred = \[1,2,2\]；MSE = 0.17。    
g = (2/3)\*(\[0.5,0.5,0\]) = \[0.33,0.33,0.00\]；据此求两矩阵梯度并以 η=0.3 更新后得到上述权重。  

---


# ans model train 1

这道题是深度学习中**多层感知机（MLP）反向传播**的简化实现。它涵盖了矩阵乘法、均值池化、MSE损失函数计算以及随机梯度下降（SGD）权重更新的核心逻辑。

### 核心计算步骤

1.  **前向传播**：
    *   $\mathbf{H} = \mathbf{X} \cdot \mathbf{W}_{mlp}$ (维度: $L \times D$)
    *   $\mathbf{h}_{mean} = \text{Average}(\mathbf{H}, \text{axis}=0)$ (维度: $1 \times D$)
    *   $\mathbf{y}_{pred} = \mathbf{h}_{mean} \cdot \mathbf{W}_{cls}$ (维度: $1 \times K$)
2.  **损失函数**：
    *   $MSE = \frac{1}{K} \sum_{i=1}^{K} (y_{pred,i} - y_i)^2$
3.  **反向传播（梯度计算）**：
    *   $\mathbf{g} = \frac{2}{K}(\mathbf{y}_{pred} - \mathbf{y})$ (维度: $1 \times K$)
    *   $\nabla \mathbf{W}_{cls} = \mathbf{h}_{mean}^T \cdot \mathbf{g}$ (外积，维度: $D \times K$)
    *   $\mathbf{x}_{mean} = \text{Average}(\mathbf{X}, \text{axis}=0)$ (维度: $1 \times D$)
    *   $\mathbf{u} = \mathbf{g} \cdot \mathbf{W}_{cls}^T$ (维度: $1 \times D$)
    *   $\nabla \mathbf{W}_{mlp} = \mathbf{x}_{mean}^T \cdot \mathbf{u}$ (外积，维度: $D \times D$)
4.  **权重更新**：
    *   $\mathbf{W} = \mathbf{W} - \eta \cdot \nabla \mathbf{W}$

---

### Python 实现

Python 的列表推导式非常适合处理这种矩阵运算。

```python
import sys

def solve():
    # 处理输入，兼容逗号或空格分隔
    input_data = sys.stdin.read().replace(',', ' ').split()
    if not input_data: return
    
    ptr = 0
    L = int(input_data[ptr]); ptr += 1
    D = int(input_data[ptr]); ptr += 1
    K = int(input_data[ptr]); ptr += 1
    eta = float(input_data[ptr]); ptr += 1
    
    y = [float(input_data[ptr+i]) for i in range(K)]; ptr += K
    X = []
    for i in range(L):
        X.append([float(input_data[ptr+j]) for j in range(D)])
        ptr += D
    
    W_mlp = []
    for i in range(D):
        W_mlp.append([float(input_data[ptr+j]) for j in range(D)])
        ptr += D
        
    W_cls = []
    for i in range(D):
        W_cls.append([float(input_data[ptr+j]) for j in range(K)])
        ptr += K

    # 1. 前向传播
    # H = X @ W_mlp
    H = [[sum(X[i][m] * W_mlp[m][j] for m in range(D)) for j in range(D)] for i in range(L)]
    # h_mean = average(H)
    h_mean = [sum(H[i][j] for i in range(L)) / L for j in range(D)]
    # y_pred = h_mean @ W_cls
    y_pred = [sum(h_mean[m] * W_cls[m][j] for m in range(D)) for j in range(K)]

    # 2. MSE 损失
    mse = sum((y_pred[i] - y[i])**2 for i in range(K)) / K

    # 3. 反向传播
    g = [(2/K) * (y_pred[i] - y[i]) for i in range(K)]
    
    # grad_W_cls = h_mean^T * g (外积)
    grad_W_cls = [[h_mean[i] * g[j] for j in range(K)] for i in range(D)]
    
    # x_mean
    x_mean = [sum(X[i][j] for i in range(L)) / L for j in range(D)]
    # u = g @ W_cls^T
    u = [sum(g[m] * W_cls[j][m] for m in range(K)) for j in range(D)]
    # grad_W_mlp = x_mean^T * u
    grad_W_mlp = [[x_mean[i] * u[j] for j in range(D)] for i in range(D)]

    # 4. 参数更新
    for i in range(D):
        for j in range(D):
            W_mlp[i][j] -= eta * grad_W_mlp[i][j]
        for j in range(K):
            W_cls[i][j] -= eta * grad_W_cls[i][j]

    # 输出格式化
    def print_list(lst):
        print(",".join(f"{x:.2f}" for x in lst))

    print_list(y_pred)
    print(f"{mse:.2f}")
    print_list([item for sublist in W_mlp for item in sublist])
    print_list([item for sublist in W_cls for item in sublist])

solve()
```

---

### C++ 实现

C++ 使用一维数组模拟矩阵可以简化输入输出的处理。

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <iomanip>

using namespace std;

// 辅助函数：解析逗号或空格分隔的输入
void read_doubles(vector<double>& v, int count) {
    string line;
    double val;
    char ch;
    int read = 0;
    while(read < count && cin >> val) {
        v.push_back(val);
        read++;
        if(cin.peek() == ',' || cin.peek() == ' ') cin.ignore();
    }
}

int main() {
    int L, D, K;
    double eta;
    string first;
    getline(cin, first);
    for(auto &c : first) if(c == ',') c = ' ';
    stringstream ss(first);
    ss >> L >> D >> K >> eta;

    vector<double> y, X_flat, W_mlp, W_cls;
    read_doubles(y, K);
    read_doubles(X_flat, L * D);
    read_doubles(W_mlp, D * D);
    read_doubles(W_cls, D * K);

    // 1. 前向传播
    vector<double> h_mean(D, 0.0);
    for (int j = 0; j < D; ++j) {
        double sum_h = 0;
        for (int i = 0; i < L; ++i) {
            for (int m = 0; m < D; ++m) {
                sum_h += X_flat[i * D + m] * W_mlp[m * D + j];
            }
        }
        h_mean[j] = sum_h / L;
    }

    vector<double> y_pred(K, 0.0);
    for (int j = 0; j < K; ++j) {
        for (int m = 0; m < D; ++m) {
            y_pred[j] += h_mean[m] * W_cls[m * K + j];
        }
    }

    // 2. MSE
    double mse = 0;
    for (int i = 0; i < K; ++i) mse += (y_pred[i] - y[i]) * (y_pred[i] - y[i]);
    mse /= K;

    // 3. 梯度
    vector<double> g(K);
    for (int i = 0; i < K; ++i) g[i] = (2.0 / K) * (y_pred[i] - y[i]);

    vector<double> x_mean(D, 0.0);
    for (int j = 0; j < D; ++j) {
        for (int i = 0; i < L; ++i) x_mean[j] += X_flat[i * D + j];
        x_mean[j] /= L;
    }

    vector<double> u(D, 0.0);
    for (int j = 0; j < D; ++j) {
        for (int m = 0; m < K; ++m) u[j] += g[m] * W_cls[j * K + m];
    }

    // 4. 更新
    cout << fixed << setprecision(2);
    for (int i = 0; i < K; ++i) cout << y_pred[i] << (i == K - 1 ? "" : ",");
    cout << endl << mse << endl;

    for (int i = 0; i < D; ++i) {
        for (int j = 0; j < D; ++j) {
            W_mlp[i * D + j] -= eta * (x_mean[i] * u[j]);
            cout << W_mlp[i * D + j] << (i == D - 1 && j == D - 1 ? "" : ",");
        }
    }
    cout << endl;

    for (int i = 0; i < D; ++i) {
        for (int j = 0; j < K; ++j) {
            W_cls[i * K + j] -= eta * (h_mean[i] * g[j]);
            cout << W_cls[i * K + j] << (i == D - 1 && j == K - 1 ? "" : ",");
        }
    }
    cout << endl;

    return 0;
}
```

---

### 机考避坑指南

1.  **输入解析**：题目中的数字可能由逗号或空格分隔。使用 Python 的 `replace(',', ' ').split()` 或 C++ 的 `stringstream` 处理是非常稳妥的。
2.  **外积（Outer Product）定义**：$\text{OuterProduct}(\mathbf{a}, \mathbf{b})$ 的结果矩阵中，第 $i$ 行第 $j$ 列的值是 $a_i \times b_j$。
3.  **均值池化的位置**：注意 $h\_mean$ 是先做 $X \cdot W_{mlp}$ 得到每条症状的变换，再求平均。
4.  **梯度公式**：
    *   $\mathbf{u} = \mathbf{g} \cdot \mathbf{W}_{cls}^T$ 意味着在求 $\mathbf{u}$ 时，索引是 $u_j = \sum g_m \cdot W_{cls}[j][m]$。
5.  **精度控制**：题目要求保留 2 位小数，最后输出时统一格式化，中间计算过程中尽量使用 `double` 以保持精度。
6.  **线性代数基础**：如果对矩阵乘法不熟悉，记住公式：$(A \cdot B)_{ij} = \sum A_{im} \cdot B_{mj}$。
