# logi reg l2 20251029

can you help me use python, java and cpp to write the follow?
你能教我这种题该怎么写吗？
如何写l2正则化呢？

---

22.

二分类逻辑回归

你需要基于用户的三个数值特征（年龄、月收入、浏览时长）训练一个二分类模型，判断其是否会购买某商品。每条训练数据包含三个特征与一个标签（0/1）。模型使用逻辑回归：以 Sigmoid 作为激活函数，损失为平均交叉熵，并加入 L2 正则。优化方式为批量梯度下降；达到最大迭代次数或相邻两次损失变化小于阈值即停止。随后对给定的测试样本输出预测标签与对应概率（四舍五入保留四位小数）。预测时，概率≥0.5 视为正类，否则为负类。

时间限制：C/C++ 1秒，其他语言2秒

空间限制：C/C++ 256M，其他语言512M

输入描述：

-   第1行：n max\_iter alpha lam tol
    -   n：训练样本条数
    -   max\_iter：最大迭代次数
    -   alpha：学习率（浮点数）
    -   lam：L2 正则系数（浮点数）
    -   tol：损失收敛阈值（浮点数）
-   接下来 n 行：每行 a inc dur label
    -   a 为年龄（数值），inc 为月收入（数值），dur 为浏览时长（数值），label 为 0 或 1
-   第 n+2 行：m（测试样本数）
-   接下来 m 行：每行 a inc dur（仅特征，无标签）

输出描述：

-   共 m 行。每行输出：pred prob
    -   pred 为预测标签（0 或 1）
    -   prob 为对应正类概率，保留四位小数

补充说明：

本题由牛友@Charles 整理上传

示例1

输入例子：

3 0 0.10 0.00 0.0001
20 3 2 0
30 10 8 1
40 15 12 1
2
25 5 4
35 12 9

输出例子：

1 0.5000
1 0.5000

例子说明：

max\_iter=0，训练不进行，参数保持 w=b=0。  
预测概率均为 0.5，阈值规则下均判为 1。

---

# ans logi reg l2

这道题是机器学习中**逻辑回归（Logistic Regression）**的经典工程实现。在机考中，这类题目考察的是对算法底层公式的理解，特别是**梯度下降**和**正则化**的细节。

### 核心公式推导

1.  **模型方程**：
    $z = w_1 \cdot \text{age} + w_2 \cdot \text{income} + w_3 \cdot \text{duration} + b$
2.  **激活函数 (Sigmoid)**：
    $h = \sigma(z) = \frac{1}{1 + e^{-z}}$
3.  **损失函数 (交叉熵 + L2正则)**：
    $Loss = -\frac{1}{n} \sum [y \log(h) + (1-y) \log(1-h)] + \frac{\lambda}{2} \sum_{j=1}^3 w_j^2$
    *注意：L2 正则通常只作用于权重 $w$，不作用于偏置 $b$。*
4.  **梯度更新规则 (批量梯度下降)**：
    *   $\frac{\partial Loss}{\partial w_j} = \frac{1}{n} \sum_{i=1}^n (h^{(i)} - y^{(i)})x_j^{(i)} + \lambda w_j$
    *   $\frac{\partial Loss}{\partial b} = \frac{1}{n} \sum_{i=1}^n (h^{(i)} - y^{(i)})$
    *   更新：$w = w - \alpha \cdot \frac{\partial Loss}{\partial w}$, $b = b - \alpha \cdot \frac{\partial Loss}{\partial b}$

---

### Python 实现
Python 代码最简洁，适合理清逻辑。

```python
import math
import sys

def solve():
    # 读取第一行
    line1 = sys.stdin.readline().split()
    if not line1: return
    n, max_iter, alpha, lam, tol = int(line1[0]), int(line1[1]), float(line1[2]), float(line1[3]), float(line1[4])
    
    # 读取训练数据
    X = []
    Y = []
    for _ in range(n):
        data = list(map(float, sys.stdin.readline().split()))
        X.append(data[:3])
        Y.append(data[3])
        
    # 初始化参数
    w = [0.0, 0.0, 0.0]
    b = 0.0
    prev_loss = float('inf')

    def get_loss(w, b, X, Y, n, lam):
        total_ce = 0.0
        for i in range(n):
            z = sum(X[i][j] * w[j] for j in range(3)) + b
            h = 1.0 / (1.0 + math.exp(-max(min(z, 500), -500))) # 防止exp溢出
            # 交叉熵，加入微小值防止log(0)
            total_ce += -(Y[i] * math.log(h + 1e-15) + (1 - Y[i]) * math.log(1 - h + 1e-15))
        
        reg = (lam / 2.0) * sum(wj**2 for wj in w)
        return (total_ce / n) + reg

    # 迭代训练
    for _ in range(max_iter):
        curr_loss = get_loss(w, b, X, Y, n, lam)
        if abs(prev_loss - curr_loss) < tol:
            break
        prev_loss = curr_loss
        
        # 计算梯度
        dw = [0.0, 0.0, 0.0]
        db = 0.0
        for i in range(n):
            z = sum(X[i][j] * w[j] for j in range(3)) + b
            h = 1.0 / (1.0 + math.exp(-max(min(z, 500), -500)))
            error = h - Y[i]
            for j in range(3):
                dw[j] += error * X[i][j]
            db += error
            
        # 更新参数
        for j in range(3):
            w[j] = w[j] - alpha * (dw[j] / n + lam * w[j])
        b = b - alpha * (db / n)

    # 预测
    m_line = sys.stdin.readline().strip()
    if not m_line: return
    m = int(m_line)
    for _ in range(m):
        test_x = list(map(float, sys.stdin.readline().split()))
        z = sum(test_x[j] * w[j] for j in range(3)) + b
        prob = 1.0 / (1.0 + math.exp(-max(min(z, 500), -500)))
        pred = 1 if prob >= 0.5 else 0
        print(f"{pred} {prob:.4f}")

solve()
```

---

### C++ 实现
C++ 需要注意浮点数输出格式和数学函数。

```cpp
#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>

using namespace std;

double sigmoid(double z) {
    if (z > 500) return 1.0;
    if (z < -500) return 0.0;
    return 1.0 / (1.0 + exp(-z));
}

double compute_loss(int n, const vector<vector<double>>& X, const vector<double>& Y, 
                    const vector<double>& w, double b, double lam) {
    double ce = 0;
    for (int i = 0; i < n; ++i) {
        double z = b;
        for (int j = 0; j < 3; ++j) z += w[j] * X[i][j];
        double h = sigmoid(z);
        ce += -(Y[i] * log(h + 1e-15) + (1 - Y[i]) * log(1 - h + 1e-15));
    }
    double reg = 0;
    for (int j = 0; j < 3; ++j) reg += w[j] * w[j];
    return (ce / n) + (lam / 2.0 * reg);
}

int main() {
    int n, max_iter;
    double alpha, lam, tol;
    if (!(cin >> n >> max_iter >> alpha >> lam >> tol)) return 0;

    vector<vector<double>> X(n, vector<double>(3));
    vector<double> Y(n);
    for (int i = 0; i < n; ++i) {
        cin >> X[i][0] >> X[i][1] >> X[i][2] >> Y[i];
    }

    vector<double> w(3, 0.0);
    double b = 0.0;
    double prev_loss = 1e18;

    for (int iter = 0; iter < max_iter; ++iter) {
        double curr_loss = compute_loss(n, X, Y, w, b, lam);
        if (abs(prev_loss - curr_loss) < tol) break;
        prev_loss = curr_loss;

        vector<double> dw(3, 0.0);
        double db = 0.0;
        for (int i = 0; i < n; ++i) {
            double z = b;
            for (int j = 0; j < 3; ++j) z += w[j] * X[i][j];
            double h = sigmoid(z);
            double err = h - Y[i];
            for (int j = 0; j < 3; ++j) dw[j] += err * X[i][j];
            db += err;
        }

        for (int j = 0; j < 3; ++j) w[j] -= alpha * (dw[j] / n + lam * w[j]);
        b -= alpha * (db / n);
    }

    int m;
    cin >> m;
    cout << fixed << setprecision(4);
    while (m--) {
        double tx[3];
        cin >> tx[0] >> tx[1] >> tx[2];
        double z = b;
        for (int j = 0; j < 3; ++j) z += w[j] * tx[j];
        double prob = sigmoid(z);
        int pred = (prob >= 0.5) ? 1 : 0;
        cout << pred << " " << prob << endl;
    }

    return 0;
}
```

---

### Java 实现
Java 注意 `Scanner` 读取数据和 `String.format`。

```java
import java.util.*;

public class Main {
    static double sigmoid(double z) {
        return 1.0 / (1.0 + Math.exp(-Math.max(Math.min(z, 500), -500)));
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNext()) return;
        int n = sc.nextInt();
        int maxIter = sc.nextInt();
        double alpha = sc.nextDouble();
        double lam = sc.nextDouble();
        double tol = sc.nextDouble();

        double[][] X = new double[n][3];
        double[] Y = new double[n];
        for (int i = 0; i < n; i++) {
            X[i][0] = sc.nextDouble();
            X[i][1] = sc.nextDouble();
            X[i][2] = sc.nextDouble();
            Y[i] = sc.nextDouble();
        }

        double[] w = new double[3];
        double b = 0.0;
        double prevLoss = Double.MAX_VALUE;

        for (int iter = 0; iter < maxIter; iter++) {
            double ce = 0;
            for (int i = 0; i < n; i++) {
                double z = b + w[0]*X[i][0] + w[1]*X[i][1] + w[2]*X[i][2];
                double h = sigmoid(z);
                ce += -(Y[i] * Math.log(h + 1e-15) + (1 - Y[i]) * Math.log(1 - h + 1e-15));
            }
            double currLoss = (ce / n) + (lam / 2.0 * (w[0]*w[0] + w[1]*w[1] + w[2]*w[2]));
            
            if (Math.abs(prevLoss - currLoss) < tol) break;
            prevLoss = currLoss;

            double[] dw = new double[3];
            double db = 0;
            for (int i = 0; i < n; i++) {
                double z = b + w[0]*X[i][0] + w[1]*X[i][1] + w[2]*X[i][2];
                double h = sigmoid(z);
                double err = h - Y[i];
                dw[0] += err * X[i][0];
                dw[1] += err * X[i][1];
                dw[2] += err * X[i][2];
                db += err;
            }

            for (int j = 0; j < 3; j++) w[j] -= alpha * (dw[j] / n + lam * w[j]);
            b -= alpha * (db / n);
        }

        if (sc.hasNextInt()) {
            int m = sc.nextInt();
            for (int i = 0; i < m; i++) {
                double tx0 = sc.nextDouble(), tx1 = sc.nextDouble(), tx2 = sc.nextDouble();
                double z = b + w[0]*tx0 + w[1]*tx1 + w[2]*tx2;
                double prob = sigmoid(z);
                int pred = prob >= 0.5 ? 1 : 0;
                System.out.println(String.format("%d %.4f", pred, prob));
            }
        }
    }
}
```

---

### 重点解析：如何处理 L2 正则化？

1.  **修改损失函数**：在原始的交叉熵后面加上 $\frac{\lambda}{2} \sum w_j^2$。
2.  **修改梯度**：
    *   **没有 L2 时**，梯度的 $w$ 部分是 $\frac{1}{n} \sum (h-y)x$。
    *   **有 L2 时**，梯度变成 $\frac{1}{n} \sum (h-y)x + \lambda w$。
    *   注意：代码实现时，更新公式变为 `w = w - alpha * (dw/n + lam * w)`。
3.  **机考细节**：
    *   **迭代次数为 0**：如果 `max_iter` 是 0，初始化 $w=0, b=0$，此时预测概率一定是 0.5。
    *   **数值稳定性**：$e^{-z}$ 在 $z$ 很大或很小时会溢出。使用 `min/max` 将 $z$ 限制在 `[-500, 500]` 之间是工程上的常用 trick。
    *   **收敛条件**：题目给出了两个条件（次数或阈值），记得用 `abs(prev_loss - curr_loss) < tol` 来提前跳出。
    *   **L2 的系数**：如果题目说 $\lambda$ 是正则项系数，通常对应损失函数里的 $\frac{\lambda}{2}$。这是为了求导后正好消去 2，使梯度项变为 $\lambda w$。


# q l2 l1 speed

如果是l1正则会怎么写？
l2正则的作用是什么？
怎么感觉更新速度变快了？
是理解错误了吗？

---

在机器学习的逻辑回归中，L1 和 L2 正则化是机考中最常考的变点。以下是针对你问题的详细解答：

### 1. 如果是 L1 正则化怎么写？

**L1 正则化（Lasso）** 的损失函数是在交叉熵基础上加上权重的绝对值之和：
$$Loss = Loss_{CE} + \lambda \sum |w_j|$$

在更新参数时，对 $|w_j|$ 求导得到的是符号函数 $\text{sgn}(w_j)$：
*   如果 $w_j > 0$，导数为 1
*   如果 $w_j < 0$，导数为 -1
*   如果 $w_j = 0$，导数在数学上不可导，但在代码实现中通常取 0

**Python 代码实现变动：**
```python
# 计算梯度时
for j in range(3):
    # sgn(w) 逻辑
    sgn_w = 1 if w[j] > 0 else (-1 if w[j] < 0 else 0)
    # 更新公式
    w[j] = w[j] - alpha * (dw[j] / n + lam * sgn_w)
```

**L1 的核心特性：** 它会产生**稀疏解**（即很多权重会直接变成 0），常用于**特征选择**。

---

### 2. L2 正则化的作用是什么？

L2 正则化（Ridge）的作用可以概括为：**“让模型变平滑，防止过拟合”**。

1.  **权重衰减（Weight Decay）：** 它惩罚过大的权重值。模型为了使 Loss 最小，会尽量让 $w$ 靠近 0。
2.  **降低复杂度：** 权重越小，函数曲线越平滑，模型对输入中的细微噪声就不那么敏感。
3.  **解决多重共线性：** 如果特征之间高度相关，模型容易给出一个特征巨大的正权重和另一个特征巨大的负权重。L2 约束了这种“打架”现象。
4.  **数值稳定性：** 在矩阵运算中，L2 相当于在对角线上加了扰动，使矩阵更易求逆，计算更稳定。

---

### 3. 为什么感觉“更新速度变快了”？是理解错误吗？

你的感觉**既对也错**，这取决于你如何定义“快”。

#### 为什么你会觉得“快”？（这是对的）
1.  **提前收敛（迭代次数减少）：**
    加入 L2 后，参数的搜索空间被限制在一个球形区域内。它消除了 Loss 函数表面的一些“平坦”区域或震荡，使得梯度下降更快地滑向局部最优点。
2.  **满足停止条件更快：**
    题目中有个条件：`相邻两次损失变化小于阈值即停止`。由于 L2 强制拉低 $w$，当 $w$ 变小时，损失的变化量会迅速变小，从而更快触发 `tol`（阈值）导致训练提前结束。
3.  **参数“坍塌”：**
    在更新公式 $w = w - \alpha(\dots + \lambda w)$ 中，你可以看作 $w = w(1 - \alpha\lambda) - \dots$。这意味着每轮迭代，$w$ 都会先被**打个折扣**（乘一个小于 1 的系数），这看起来参数变化很大。

#### 为什么它其实变“慢”了？（这是错的）
1.  **阻碍模型学习：**
    L2 本质上是在和“真实的梯度”做对抗。真实梯度想把 $w$ 拉向能解释数据的方向，而 L2 永远想把 $w$ 拉回 0。如果 $\lambda$（lam）设得太大，模型会因为**“步子迈不开”**而无法学到真正的规律。
2.  **单次计算量：**
    代码中多了 `lam * w` 的计算，单次迭代的计算耗时其实是微量增加的。

### 总结建议

*   **机考中：** 如果题目要求 L2，更新公式就是 `w -= alpha * (dw/n + lam * w)`。
*   **关于速度：** 正则化能让模型**更稳**，通常能让训练在更少的迭代次数内达到**“稳定状态”**，所以你感觉“变快了”是合理的，但在物理计算上它并没有提速。
*   **注意点：** 永远不要对偏置 $b$ 做正则化，因为 $b$ 决定了模型的平移位置，限制它并不能防止过拟合。

---

# origin self corrected

```py
import sys
import math

class Sample:
    def __init__(self, feature_list, label=None):
        self.feature_list = feature_list
        self.label = label

def get_loss(ws, b, samples, n_samples):
    # curr_loss = 0.0
    cross_etp = 0.0
    for j in range(n_samples):
        sample = samples[j]
        z = sum(w * x for w, x in zip(ws, sample.feature_list)) + b
        h = 1.0 / (1.0 + math.exp(-z))
        cross_etp += -( sample.label * math.log(h) + (1.0 - sample.label) * math.log(1.0 - h) )
    l2_reg = lam * 0.5 * sum(w * w for w in ws)
    return cross_etp / n_samples + l2_reg

inputs = sys.stdin.read().split()
n_samples = int(inputs[0])
max_iter = int(inputs[1])
alpha = float(inputs[2])
lam = float(inputs[3])
tol = float(inputs[4])
samples = []
for i in range(n_samples):
    sample = Sample(
        [float(inputs[5 + i * 4]),
        float(inputs[6 + i * 4]),
        float(inputs[7 + i * 4])],
        int(inputs[8 + i * 4]),
    )
    samples.append(sample)
ws = [0.0] * 3
b = 0.0
pre_loss = float('inf')
for i in range(max_iter):
    cur_loss = get_loss(ws, b, samples, n_samples)
    if abs(cur_loss - pre_loss) < tol:
        break
    pre_loss = cur_loss
    grad_ws = [0.0] * 3
    grad_b = 0.0
    for j in range(n_samples):
        sample = samples[j]
        z = sum(w * x for w, x in zip(ws, sample.feature_list)) + b
        h = 1.0 / (1.0 + math.exp(-z))
        err = h - sample.label
        for p in range(3):
            grad_ws[p] += err * sample.feature_list[p]
        grad_b += err
    for j in range(3):
        ws[j] -= alpha * (grad_ws[j] / n_samples + lam * ws[j])
    b -= alpha * grad_b / n_samples

n_samples_no_label = int(inputs[9 + n_samples * 4 - 4])
pos = 9 + n_samples * 4 - 4
samples_no_label = []
ans_probs = []
ans_labels = []
for i in range(n_samples_no_label):
    sample = Sample(
        [float(inputs[pos + 1 + i * 3]),
        float(inputs[pos + 2 + i * 3]),
        float(inputs[pos + 3 + i * 3])]
    )
    samples_no_label.append(sample)
    z = sum(w * x for w, x in zip(ws, sample.feature_list)) + b
    h = 1.0 / (1.0 + math.exp(-z))
    # ans_probs.append('{:.4f}'.format(h))
    if h >= 0.5:
        # ans_labels.append(1)
        ans_label = 1
        print(f"{ans_label} {h:.4f}")
    else:
        # ans_labels.append(0)
        ans_label = 0
        print(f"{ans_label} {h:.4f}")
```


# correct 

你的代码整体逻辑非常清晰，已经具备了逻辑回归训练的核心框架。但在**机考环境**中，有几个**致命的 Bug** 和**稳定性问题**需要修正，否则可能导致运行报错或计算结果错误。

以下是详细的审查意见和修正建议：

### 1. 致命错误：L2 正则项的计算 (在 `get_loss` 中)
这是你代码中最严重的问题：
*   **错误写法**：`l2_reg = 0.5 * sum(w * w for w in sample.feature_list)`
*   **问题**：
    1.  正则化是惩罚**权重 `ws`**，而不是样本的特征。
    2.  你漏掉了正则系数 **`lam`**。
*   **修正**：应该使用当前权重的平方和。
    ```python
    l2_reg = (lam / 2.0) * sum(w * w for w in ws)
    ```

### 2. 数学稳定性：防止溢出 (Exp 和 Log)
逻辑回归最容易在 `math.exp` 和 `math.log` 上崩溃。
*   **Exp 溢出**：如果 `z` 是很大的负数，`math.exp(-z)` 会爆炸。
*   **Log 域错误**：如果 `h` 恰好是 `0.0` 或 `1.0`（由于精度问题），`math.log(0)` 会直接报错退出。
*   **修正**：
    ```python
    # 限制 z 的范围防止 exp 溢出
    z = max(min(z, 500), -500) 
    h = 1.0 / (1.0 + math.exp(-z))
    # log 计算增加一个极小值 eps
    eps = 1e-15
    cross_etp += -(sample.label * math.log(h + eps) + (1.0 - sample.label) * math.log(1.0 - h + eps))
    ```

### 3. 输入读取的索引偏移
你的输入处理逻辑使用了 `split()` 展开成一维列表，这在 Python 中处理这种非对齐数据很有效，但索引计算非常容易错位。
*   你的 `pos` 计算逻辑：`9 + n_samples * 4 - 4` 等于 `5 + 4 * n_samples`。
*   **检查**：
    *   开头的 5 个参数：`n, max_iter, alpha, lam, tol` (索引 0-4)
    *   训练数据：每行 4 个，共 $n$ 行。占用的索引范围是 $5$ 到 $5 + 4n - 1$。
    *   所以测试样本数 $m$ 的位置确实是 `5 + 4 * n_samples`。**你的计算是对的，但建议直接用一个指针变量推进，这样更不容易出错。**

---

### 修正后的代码建议

我为你整合了以上修正，这样写在机考中会更稳健：

```python
import sys
import math

# 使用迭代器读取输入，比手动算索引更安全
def get_input():
    for line in sys.stdin:
        for word in line.split():
            yield word

input_gen = get_input()

def solve():
    try:
        n_samples = int(next(input_gen))
        max_iter = int(next(input_gen))
        alpha = float(next(input_gen))
        lam = float(next(input_gen))
        tol = float(next(input_gen))
    except StopIteration:
        return

    # 存储训练数据
    train_features = []
    train_labels = []
    for _ in range(n_samples):
        f = [float(next(input_gen)) for _ in range(3)]
        train_features.append(f)
        train_labels.append(int(next(input_gen)))

    ws = [0.0] * 3
    b = 0.0
    pre_loss = float('inf')
    eps = 1e-15

    for _ in range(max_iter):
        # 1. 计算当前 Loss (用于判断收敛)
        ce_loss = 0.0
        for i in range(n_samples):
            z = sum(ws[k] * train_features[i][k] for k in range(3)) + b
            z = max(min(z, 500), -500)
            h = 1.0 / (1.0 + math.exp(-z))
            ce_loss += -(train_labels[i] * math.log(h + eps) + (1.0 - train_labels[i]) * math.log(1.0 - h + eps))
        
        # 修正：L2 正则项使用 lam 和 ws
        curr_loss = (ce_loss / n_samples) + (lam / 2.0) * sum(w**2 for w in ws)
        
        if abs(curr_loss - pre_loss) < tol:
            break
        pre_loss = curr_loss

        # 2. 批量梯度下降更新
        grad_ws = [0.0] * 3
        grad_b = 0.0
        for i in range(n_samples):
            z = sum(ws[k] * train_features[i][k] for k in range(3)) + b
            z = max(min(z, 500), -500)
            h = 1.0 / (1.0 + math.exp(-z))
            err = h - train_labels[i]
            for k in range(3):
                grad_ws[k] += err * train_features[i][k]
            grad_b += err
        
        # 修正：L2 正则化的梯度部分
        for k in range(3):
            # w = w - alpha * ( (1/n) * dL/dw + lam * w )
            ws[k] -= alpha * (grad_ws[k] / n_samples + lam * ws[k])
        b -= alpha * (grad_b / n_samples)

    # 3. 预测阶段
    try:
        m = int(next(input_gen))
        for _ in range(m):
            test_f = [float(next(input_gen)) for _ in range(3)]
            z = sum(ws[k] * test_f[k] for k in range(3)) + b
            z = max(min(z, 500), -500)
            prob = 1.0 / (1.0 + math.exp(-z))
            label = 1 if prob >= 0.5 else 0
            print(f"{label} {prob:.4f}")
    except StopIteration:
        pass

if __name__ == "__main__":
    solve()
```

### 总结你的代码亮点与不足：
*   **亮点**：使用了批量梯度下降（BGD），这是符合题目要求的。逻辑结构非常清晰，`pre_loss` 和 `tol` 的判断位置正确。
*   **不足**：
    1.  **L2 公式理解偏差**（最关键）。
    2.  **数值稳定性考虑不足**（在极端输入下容易挂掉）。
    3.  **计算顺序建议**：通常在循环内部先算梯度更新，再算 Loss 判断。或者像我上面写的那样。

按照修正后的逻辑，这道题你应该能稳拿满分。


# logi reg

can you help me use python and cpp to write the follow?
你能教我这种题该怎么写吗？
逻辑回归，完全不会。

------

21.

设备故障预测程序

在一套对象存储集群中，运维同学希望根据设备运行日志，提前判断设备是否有故障风险，从而把数据在故障前迁移到其他节点。每条日志包含以下字段：设备ID、写入次数、读取次数、平均写入延迟(ms)、平均读取延迟(ms)、使用年限(年)、设备状态(0 正常/1 故障)。  
  
请你实现一个设备故障预测程序，基于训练数据学习一个逻辑回归模型，并对给定的待预测设备输出是否故障的判定结果。  
  
  
数据清洗规则  
\- 缺失值填充：数值字段出现字符串 NaN 时，用该字段在训练集中“有效数值”的均值进行填充。有效数值的含义见“异常值处理”。  
  
\- 异常值处理：若出现以下越界值，则视为异常，用该字段在训练集“有效数值”的中位数替换。  
   1.写入/读取次数：小于 0  
   2.平均写入/读取延迟：小于 0 或 大于 1000  
   3.使用年限：小于 0 或 大于 20  
  
\- 说明：计算均值/中位数时，只统计训练集中“有效数值”（即不含 NaN，且不越界）。若某字段在训练集没有任何有效数值，则该字段的均值与中位数都按 0 处理。  
\- 标签缺失：训练样本若无状态字段或无法解析为 0/1，丢弃该行，不参与训练，也不参与统计均值/中位数。  
  
模型与训练  
\- 模型：二分类逻辑回归，带偏置项 w0。  

\- 训练方法：批量梯度下降（Batch GD），每次迭代用全部训练样本，学习率 0.01，迭代 100 次，初始权重全 0。

\- 概率：  
  P(y=1) =11+e−z\\frac{1}{1+e^{-z}}1+e−z1​   其中 z = w0 + ∑i\=15wixi\\sum\_{i=1}^{5}{w\_ix\_i}∑i\=15​wi​xi​  
  

\- 判定阈值：若 P(y=1) ≥ 0.5 则输出 1，否则输出 0。  

时间限制：C/C++ 1秒，其他语言2秒

空间限制：C/C++ 256M，其他语言512M

输入描述：

第一行：N（2 ≤ N ≤ 100）  
接下来 N 行：每行一个训练样本  
device\_id,writes,reads,avg\_write\_ms,avg\_read\_ms,years,status  
第 N+1 行：M（1 ≤ M ≤ 10）  
接下来 M 行：每行一个待预测样本（无状态）  
  device\_id,writes,reads,avg\_write\_ms,avg\_read\_ms,years  

输出描述：

共 M 行，每行输出一个整数 0 或 1，对应各待预测设备是否判定为故障。

补充说明：

本题由牛友@Charles 整理上传

示例1

输入例子：

12
n1,50,25,5,2,1,0
n2,55,27,5.5,2.5,1.2,0
n3,60,30,6,3,1.5,0
n4,65,32,6.5,3.2,1.8,0
n5,70,35,7,3.5,2,0
n6,75,37,7.5,3.8,2.2,0
n7,80,40,8,4,2.5,0
n8,85,42,8.5,4.2,2.7,0
n9,90,45,9,4.5,3,0
n10,95,47,9.5,4.8,3.2,0
p1,400,200,20,10,6,1
p2,500,250,22,11,8,1
2
q1,88,44,8.8,4.3,2.9
q2,480,240,21.5,10.8,7.5

输出例子：

0
1

例子说明：

训练集中负类远多于正类，模型学到明显负偏置；但正类样本特征显著更大，使对应权重为正。  
q1落在负类量级附近，P<0.5 → 0；q2与正类量级接近，P≥0.5 → 1。  

---

逻辑回归（Logistic Regression）是机器学习中最基础的二分类算法。虽然名字叫“回归”，但它其实是用来做**分类**的。

这道题的难点不在于逻辑回归算法本身，而在于**极其繁琐的数据预处理规则**。在实际的工程或竞赛中，数据清洗往往占 70% 的工作量。

---

### 第一步：理解算法流程

1.  **线性回归部分**：先算出一个得分 $z$
    $z = w_0 + w_1x_1 + w_2x_2 + w_3x_3 + w_4x_4 + w_5x_5$
2.  **激活函数 (Sigmoid)**：把 $z$ 映射到 0 到 1 之间，代表概率
    $P = \frac{1}{1 + e^{-z}}$
3.  **损失函数与梯度下降**：
    我们需要更新权重 $w$，使得预测值 $P$ 靠近真实标签 $y$。
    每次迭代（Batch GD）：
    $w_j = w_j - \alpha \cdot \frac{1}{N} \sum_{i=1}^{N} (P^{(i)} - y^{(i)}) \cdot x_j^{(i)}$
    *(其中 $x_0$ 恒等于 1，对应偏置项 $w_0$)*

---

### 第二步：Python 实现

Python 适合理解逻辑。注意：为了适应 OJ（在线评测系统），不使用 numpy，只用原生语法。

```python
import math

def solve():
    # 1. 读取训练数据数量
    try:
        line = input().strip()
        if not line: return
        n = int(line)
    except EOFError:
        return

    raw_train_data = []
    # 存储每个特征的所有有效值，用于计算均值和中位数
    valid_features = [[] for _ in range(5)] 

    for _ in range(n):
        parts = input().strip().split(',')
        if len(parts) < 7: continue # 标签缺失
        
        # 验证标签是否有效
        try:
            status = int(parts[6])
            if status not in [0, 1]: raise ValueError
        except:
            continue # 丢弃无效标签行
        
        # 预处理该行的特征
        features = parts[1:6] # writes, reads, avg_write, avg_read, years
        row_data = []
        for i in range(5):
            val_str = features[i]
            if val_str == "NaN":
                row_data.append("NaN")
            else:
                try:
                    val = float(val_str)
                    # 检查是否为异常值 (基于题目规则)
                    is_anomaly = False
                    if i == 0 or i == 1: # writes/reads
                        if val < 0: is_anomaly = True
                    elif i == 2 or i == 3: # latency
                        if val < 0 or val > 1000: is_anomaly = True
                    elif i == 4: # years
                        if val < 0 or val > 20: is_anomaly = True
                    
                    if is_anomaly:
                        row_data.append("ANOMALY")
                    else:
                        row_data.append(val)
                        valid_features[i].append(val)
                except:
                    row_data.append("NaN")
        
        row_data.append(status)
        raw_train_data.append(row_data)

    # 2. 计算统计量 (均值和中位数)
    means = [0.0] * 5
    medians = [0.0] * 5
    for i in range(5):
        if valid_features[i]:
            means[i] = sum(valid_features[i]) / len(valid_features[i])
            sorted_f = sorted(valid_features[i])
            ln = len(sorted_f)
            if ln % 2 == 1:
                medians[i] = sorted_f[ln // 2]
            else:
                medians[i] = (sorted_f[ln // 2 - 1] + sorted_f[ln // 2]) / 2.0
        else:
            means[i] = 0.0
            medians[i] = 0.0

    # 3. 填充训练集中的缺失值和异常值
    final_train_x = []
    final_train_y = []
    for row in raw_train_data:
        x = [1.0] # 对应 w0 (偏置项)
        for i in range(5):
            if row[i] == "NaN":
                x.append(means[i])
            elif row[i] == "ANOMALY":
                x.append(medians[i])
            else:
                x.append(row[i])
        final_train_x.append(x)
        final_train_y.append(row[5]) # 最后一列是 status

    # 4. 逻辑回归训练 (Batch GD)
    weights = [0.0] * 6 # w0, w1, w2, w3, w4, w5
    alpha = 0.01
    num_samples = len(final_train_x)

    for _ in range(100):
        gradients = [0.0] * 6
        for i in range(num_samples):
            # z = sum(w * x)
            z = sum(weights[j] * final_train_x[i][j] for j in range(6))
            p = 1.0 / (1.0 + math.exp(-z))
            error = p - final_train_y[i] # math.log(x, bottom)
            for j in range(6):
                gradients[j] += error * final_train_x[i][j]
        
        for j in range(6):
            weights[j] -= alpha * (gradients[j] / num_samples)

    # 5. 处理待预测样本
    m = int(input().strip())
    for _ in range(m):
        parts = input().strip().split(',')
        x_test = [1.0]
        for i in range(5):
            val_str = parts[i+1]
            if val_str == "NaN":
                x_test.append(means[i])
            else:
                val = float(val_str)
                # 预测数据同样要处理异常值
                is_anomaly = False
                if i == 0 or i == 1:
                    if val < 0: is_anomaly = True
                elif i == 2 or i == 3:
                    if val < 0 or val > 1000: is_anomaly = True
                elif i == 4:
                    if val < 0 or val > 20: is_anomaly = True
                
                if is_anomaly:
                    x_test.append(medians[i])
                else:
                    x_test.append(val)
        
        # 计算预测结果
        z_test = sum(weights[j] * x_test[j] for j in range(6))
        p_test = 1.0 / (1.0 + math.exp(-z_test))
        print(1 if p_test >= 0.5 else 0)

solve()
```

---

### 第三步：C++ 实现

C++ 在处理字符串分割（CSV）和排序（中位数）时会稍显繁琐，但性能更高。

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <cmath>
#include <algorithm>

using namespace std;

// 数据结构存储样本
struct Sample {
    vector<double> features; // 5个特征
    int status;
    vector<string> raw_features; // 暂存原始字符串判断 NaN
};

// 分割字符串函数
vector<string> split(const string& s, char delimiter) {
    vector<string> tokens;
    string token;
    istringstream tokenStream(s);
    while (getline(tokenStream, token, delimiter)) {
        tokens.push_back(token);
    }
    return tokens;
}

int main() {
    int N;
    if (!(cin >> N)) return 0;
    string line;
    getline(cin, line); // 跳过首行换行符

    vector<Sample> train_pool;
    vector<vector<double>> valid_vals(5);

    for (int i = 0; i < N; ++i) {
        getline(cin, line);
        vector<string> parts = split(line, ',');
        if (parts.size() < 7) continue;

        int status;
        try {
            status = stoi(parts[6]);
            if (status != 0 && status != 1) continue;
        } catch (...) { continue; }

        Sample s;
        s.status = status;
        for (int j = 1; j <= 5; ++j) {
            s.raw_features.push_back(parts[j]);
            if (parts[j] != "NaN") {
                double v = stod(parts[j]);
                bool anomaly = false;
                if ((j == 1 || j == 2) && v < 0) anomaly = true;
                else if ((j == 3 || j == 4) && (v < 0 || v > 1000)) anomaly = true;
                else if (j == 5 && (v < 0 || v > 20)) anomaly = true;
                
                if (!anomaly) valid_vals[j-1].push_back(v);
            }
        }
        train_pool.push_back(s);
    }

    // 计算均值和中位数
    vector<double> means(5, 0), medians(5, 0);
    for (int j = 0; j < 5; ++j) {
        if (!valid_vals[j].empty()) {
            double sum_v = 0;
            for (double v : valid_vals[j]) sum_v += v;
            means[j] = sum_v / valid_vals[j].size();

            sort(valid_vals[j].begin(), valid_vals[j].end());
            int sz = valid_vals[j].size();
            if (sz % 2 == 1) medians[j] = valid_vals[j][sz / 2];
            else medians[j] = (valid_vals[j][sz / 2 - 1] + valid_vals[j][sz / 2]) / 2.0;
        }
    }

    // 准备最终训练矩阵 (加上偏置项 1.0)
    vector<vector<double>> X;
    vector<int> Y;
    for (auto& s : train_pool) {
        vector<double> row = {1.0};
        for (int j = 0; j < 5; ++j) {
            if (s.raw_features[j] == "NaN") row.push_back(means[j]);
            else {
                double v = stod(s.raw_features[j]);
                bool anomaly = false;
                if ((j == 0 || j == 1) && v < 0) anomaly = true;
                else if ((j == 2 || j == 3) && (v < 0 || v > 1000)) anomaly = true;
                else if (j == 4 && (v < 0 || v > 20)) anomaly = true;
                
                if (anomaly) row.push_back(medians[j]);
                else row.push_back(v);
            }
        }
        X.push_back(row);
        Y.push_back(s.status);
    }

    // 训练
    vector<double> w(6, 0.0);
    double alpha = 0.01;
    int m_samples = X.size();
    for (int iter = 0; iter < 100; ++iter) {
        vector<double> grad(6, 0.0);
        for (int i = 0; i < m_samples; ++i) {
            double z = 0;
            for (int j = 0; j < 6; ++j) z += w[j] * X[i][j];
            double p = 1.0 / (1.0 + exp(-z));
            double err = p - Y[i];
            for (int j = 0; j < 6; ++j) grad[j] += err * X[i][j];
        }
        for (int j = 0; j < 6; ++j) w[j] -= alpha * (grad[j] / m_samples);
    }

    // 预测
    int M;
    cin >> M;
    getline(cin, line);
    for (int i = 0; i < M; ++i) {
        getline(cin, line);
        vector<string> parts = split(line, ',');
        vector<double> test_x = {1.0};
        for (int j = 0; j < 5; ++j) {
            string val_str = parts[j+1];
            if (val_str == "NaN") test_x.push_back(means[j]);
            else {
                double v = stod(val_str);
                bool anomaly = false;
                if ((j == 0 || j == 1) && v < 0) anomaly = true;
                else if ((j == 2 || j == 3) && (v < 0 || v > 1000)) anomaly = true;
                else if (j == 4 && (v < 0 || v > 20)) anomaly = true;
                
                if (anomaly) test_x.push_back(medians[j]);
                else test_x.push_back(v);
            }
        }
        double z = 0;
        for (int j = 0; j < 6; ++j) z += w[j] * test_x[j];
        double p = 1.0 / (1.0 + exp(-z));
        cout << (p >= 0.5 ? 1 : 0) << endl;
    }

    return 0;
}
```

---

### 解题核心总结（建议收藏）：

1.  **数据清洗是核心**：
    *   **NaN** 用均值（Mean）。
    *   **越界值** 用中位数（Median）。
    *   计算均值和中位数时，**只能用训练集里正常的数**。
    *   如果标签（status）不合法，整行扔掉，也不参与均值计算。
2.  **逻辑回归参数**：
    *   偏置项 $w_0$ 相当于给每个样本多加一列特征，值永远是 $1.0$。
    *   初始权重全 $0$。
    *   学习率 $0.01$，迭代 $100$ 次。
3.  **梯度更新公式**：
    记住 $(Prediction - Actual) \times Feature$。这是梯度下降最常用的形式。
4.  **预测阈值**：
    $P \ge 0.5$ 判为 $1$。注意 $0.5$ 这个分界线。


# multi logi ? 20251105 

21.

多目标推荐排序模型优化

在推荐排序的双目标场景中，需要同时预测点击率(CTR)与转化率(CVR)。用一个共享的线性权重向量 w 提取通用特征，同时为两个任务各配置一个偏置 b\_ctr、b\_cvr。给定特征矩阵 X 与标签矩阵 Y（每行形如\[ctr, cvr\]），从全零参数出发，按批量梯度下降迭代 N 次，学习率为 lr。训练完成后，用最终参数重新计算一次联合损失：

-   预测：y\_hat\_ctr = X·w + b\_ctr，y\_hat\_cvr = X·w + b\_cvr
-   MSE\_ctr 与 MSE\_cvr 为对应任务的均方误差
-   联合损失：Loss = MSE\_ctr + alpha × MSE\_cvr
-   输出：将 Loss×10^10 按“四舍五入（Half Up）”取整为整数

时间限制：C/C++ 1秒，其他语言2秒

空间限制：C/C++ 256M，其他语言512M

输入描述：

输入格式

-   第1行：特征矩阵，形如“a,b;c,d;...”表示按行给出
-   第2行：标签矩阵，每行两个数“ctr,cvr”，整体同样用分号分行
-   第3行：迭代次数 N（可为 0）
-   第4行：学习率 lr（浮点数）
-   第5行：权重系数 alpha（浮点数）

输出描述：

-   一行，打印整数 round\_half\_up(Loss×10^10)

补充说明：

本题由牛友@Charles 整理上传

示例1

输入例子：

1,2;3,4
0.1,0.2;0.3,0.4
0
0.01
0.5

输出例子：

1000000000

例子说明：

N=0 时不训练，预测恒为 0  
MSE\_ctr=((0-0.1)^2+(0-0.3)^2)/2=0.05  
MSE\_cvr=((0-0.2)^2+(0-0.4)^2)/2=0.10  
Loss=0.05+0.5×0.10=0.10，Loss×1e10=1,000,000,000，四舍五入为 1000000000  

------

### np,pd,sl
你能帮我写一个numpy，pandas，scikit learn都可以用的版本吗？我想试试能不能用
not useable


# moe

how to build a special rule of compare for python and cpp list sort function?
can you use class group and class expert to write python and cpp version?

---

2.

MOE Top‑k 路由

在一个稀疏 MOE 模型中，有 n 个专家顺序编号为 0…n-1，这些专家被平均分布到 m 张 NPU 卡上，每张卡上一组，且同组专家编号连续。为降低跨卡通信，现将路由目标限制在最多 p 张 NPU 上：    
1) 先对每组求组内概率最大值及其专家编号，作为该组的代表值；    
2) 把所有组按“代表概率”从高到低排序，若概率相同则组号小的在前，取前 p 个组；    
3) 仅在上述 p 个组包含的所有专家里，按“概率降序、编号升序”挑选前 k 位的专家编号作为最终路由目标。    
  
约束与异常    
\- 若 n 不能被 m 整除，则无法平均分组，输出 error。    
\- 若 p>m，输出 error。    
\- 设每组大小 g=n/m，若可选专家总数 p·g<k，无法选够 k 人，输出 error。    

时间限制：C/C++ 1秒，其他语言2秒

空间限制：C/C++ 256M，其他语言512M

输入描述：

第一行：四个整数 n m p k（1≤n,m,p,k≤10000）  

第二行：n 个浮点数，依次为专家 0…n-1 的概率，均在 (0,1) 内

输出描述：

若发生异常，输出 error  

否则输出 k 个专家编号，升序，空格分隔（行尾无空格）

补充说明：

本题由牛友@Charles 整理上传

示例1

输入例子：

6 3 2 2
0.3 0.1 0.05 0.6 0.4 0.2

输出例子：

3 4

例子说明：

分组：g=6/3=2。组0=\[0,1\]→代表(0.3,idx0)，组1=\[2,3\]→代表(0.6,idx3)，组2=\[4,5\]→代表(0.4,idx4)。    
选组：按代表概率降序取前 p=2 个，得到组1与组2。    
选专家：在{2,3,4,5}中按概率降序取前 k=2，依次为 idx3(0.6)、idx4(0.4)；最后升序输出 3 4。  

示例2

输入例子：

6 4 2 2
0.1 0.2 0.3 0.4 0.5 0.6

输出例子：

error

例子说明：

因为 n=6、m=4，n 必须能被 m 整除才能把专家平均分到每张 NPU 上（组大小 g=n/m 为整数）。这里 6%4≠0，g=1.5 不是整数，无法等分成 4 组，所以按规则直接输出 error。

---

import sys

# for line in sys.stdin:
#     a = line.split()
#     print(int(a[0]) + int(a[1]))

# n exp, m card, p max card
# m group, max pval, 
# sort m group by max pval, min code first,
# get first p cards
# from p, get k max pval, min code first

# n // m != 0, err
# p > m, err
# p * (n / m) < k, err

class Group:
    def __init__(self) -> None:
        self.experts = []
        self.expert_pvals = []
        # self.represent_expert = -1
        self.represent_pval = -1.0

inputs = sys.stdin.read().split()
n = int(inputs[0])
m = int(inputs[1])
p = int(inputs[2])
k = int(inputs[3])
if n // m != 0 or p > m or p * (n / m) < k:
    print('error')
else:
    groups = []
    for i in range(m):
        group = Group()
        num_exp = n // m
        # max_exp = -1
        max_pval = -1.0
        for j in range(num_exp):
            cur_exp = i + j
            cur_pval = float(inputs[4 + i + j])
            if cur_pval > max_pval:
                max_pval = cur_pval
                # max_exp = cur_exp
            # elif cur_pval == max_pval and cur_exp < max_exp:
            #     max_exp = cur_exp
            group.experts.append(cur_exp)
            group.expert_pvals.append(cur_pval)
        # group.represent_expert = max_exp
        group.represent_pval = max_pval
        groups.append(group)
    groups.sort(key = lambda x : x.represent_pval)
    p_groups = []
    for i in range(p):
        p_groups.append(groups[i])
    tmp_experts = []
    for tmp_group in p_groups:
        for tmp_expert in 

-----

# answer moe

这个问题是典型的**多级排序**问题。在 Python 和 C++ 中处理这种“第一关键字降序，第二关键字升序”的规则有不同的优雅写法。

针对你的代码草稿，有两个关键逻辑错误需要先修正：
1. **整除判断**：应该是 `n % m != 0` 而不是 `n // m != 0`。
2. **专家分配**：组 $i$ 的专家编号范围是 `i*g` 到 `(i+1)*g - 1`。

---

### 1. Python 版本：利用元组 (Tuple) 进行多级排序

Python 的 `sort` 是稳定排序。最简便的方法是 `key` 函数返回一个元组：
*   如果想**升序**，直接放元素：`x`
*   如果想**降序**，对于数值可以取负：`-x`；对于非数值，可以使用 `functools.cmp_to_key`。

```python
import sys

class Expert:
    def __init__(self, eid, prob):
        self.eid = eid
        self.prob = prob

class Group:
    def __init__(self, gid, experts):
        self.gid = gid
        self.experts = experts  # Expert 对象列表
        # 代表值：组内概率最大的专家概率。若概率相同，题目未明确说，通常取编号小的。
        self.rep_prob = max(e.prob for e in experts)

def solve():
    input_data = sys.stdin.read().split()
    if not input_data: return
    
    n, m, p, k = map(int, input_data[:4])
    probs = list(map(float, input_data[4:]))

    # 异常判断
    if n % m != 0 or p > m or (p * (n // m)) < k:
        print("error")
        return

    g = n // m
    groups = []
    for i in range(m):
        group_experts = []
        for j in range(i * g, (i + 1) * g):
            group_experts.append(Expert(j, probs[j]))
        groups.append(Group(i, group_experts))

    # 规则 2：所有组按“代表概率”降序，组号升序
    # 小技巧：元组 (-概率, 组号) 即可实现 降序/升序 组合
    groups.sort(key=lambda x: (-x.rep_prob, x.gid))

    # 取前 p 个组
    selected_experts = []
    for i in range(p):
        selected_experts.extend(groups[i].experts)

    # 规则 3：在可选专家里，按“概率降序、编号升序”选前 k 个
    selected_experts.sort(key=lambda e: (-e.prob, e.eid))
    
    final_targets = []
    for i in range(k):
        final_targets.append(selected_experts[i].eid)

    # 最后升序输出编号
    final_targets.sort()
    print(*(final_targets))

solve()
```

---

### 2. C++ 版本：重载运算符或 Lambda 表达式

C++ 的 `std::sort` 默认使用 `operator<`。要实现自定义排序，最常用的是在 `sort` 第三个参数传入 **Lambda 表达式**。

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <iomanip>

using namespace std;

struct Expert {
    int id;
    double prob;
};

struct Group {
    int id;
    double rep_prob;
    vector<Expert> experts;
};

int main() {
    int n, m, p, k;
    if (!(cin >> n >> m >> p >> k)) return 0;

    vector<double> probs(n);
    for (int i = 0; i < n; ++i) cin >> probs[i];

    // 异常判断
    if (n % m != 0 || p > m || (p * (n / m)) < k) {
        cout << "error" << endl;
        return 0;
    }

    int g = n / m;
    vector<Group> groups(m);
    for (int i = 0; i < m; ++i) {
        groups[i].id = i;
        double max_p = -1.0;
        for (int j = i * g; j < (i + 1) * g; ++j) {
            Expert e = {j, probs[j]};
            groups[i].experts.push_back(e);
            if (e.prob > max_p) max_p = e.prob;
        }
        groups[i].rep_prob = max_p;
    }

    // 规则 2：组排序 (代表概率降序，组号升序)
    sort(groups.begin(), groups.end(), [](const Group& a, const Group& b) {
        if (a.rep_prob != b.rep_prob) return a.rep_prob > b.rep_prob; // 降序
        return a.id < b.id; // 升序
    });

    // 收集前 p 组的专家
    vector<Expert> candidates;
    for (int i = 0; i < p; ++i) {
        for (const auto& e : groups[i].experts) {
            candidates.push_back(e);
        }
    }

    // 规则 3：专家排序 (概率降序，编号升序)
    sort(candidates.begin(), candidates.end(), [](const Expert& a, const Expert& b) {
        if (a.prob != b.prob) return a.prob > b.prob;
        return a.id < b.id;
    });

    // 取前 k 个并按 ID 升序输出
    vector<int> result;
    for (int i = 0; i < k; ++i) {
        result.push_back(candidates[i].id);
    }
    sort(result.begin(), result.end());

    for (int i = 0; i < k; ++i) {
        cout << result[i] << (i == k - 1 ? "" : " ");
    }
    cout << endl;

    return 0;
}
```

---

### 核心知识点总结

#### 1. 排序的自定义规则
在算法题中，经常遇到 **"A 降序，B 升序"**：
*   **Python 逻辑**：`sort(key=lambda x: (-x.A, x.B))`。 
    *   *注意*：这只适用于 A 是数值类型。如果是字符串要降序，元组法失效，建议使用 `functools.cmp_to_key`。
*   **C++ 逻辑**：
    ```cpp
    bool compare(const T& a, const T& b) {
        if (a.A != b.A) return a.A > b.A; // 降序：大的在前
        return a.B < b.B; // 升序：小的在前
    }
    ```

#### 2. MOE 逻辑实现
*   **分组映射**：对于连续编号，组 $i$ 的成员公式是 `range(i*g, (i+1)*g)`，这是工程中平均切分数据的标准写法。
*   **Top-k 路由**：在模型中，MOE 路由通常是选概率最大的 $k$ 个专家。本题增加了“组过滤”的步骤（限制卡数），这是为了减少跨节点通信开销（All-to-All 通信量）。

#### 3. 错误处理
*   注意 `n % m` 的判断。
*   注意 `p * g < k`：这里的 `g` 是组的大小（`n/m`），意思是你选了 $p$ 张卡，如果这 $p$ 张卡上所有的专家总数加起来都不到 $k$，那肯定选不出 $k$ 个专家。


    
        
# dp >=m

what is the difference between dp = [[inf] * (m + 1) for _ in range(n + 1)] and dp = [[inf] * (m + 1)] * (n + 1)?


i want to know if java or c++ version of the follow codes can pass the test.
i usually cant write 1d dp at online tests.
---


import sys 
# from functools import cache
inputs = sys.stdin.read().split()
m = int(inputs[0])
n = int(inputs[1])

spaces = [0] * n 
# swaps = []
# recos = []
costs = [0] * n 
for i in range(n):
    # spaces.append(int(inputs[2 + i]))
    spaces[i] = int(inputs[2 + i])
    # swaps[i] = int(inputs[n + 2 + i])
    # recos[i] = int(inputs[2 * n + 2 + i])
    swap = int(inputs[n + 2 + i])
    reco = int(inputs[2 * n + 2 + i])
    costs[i] = min(swap, reco)
# print(spaces)
# print(costs)
inf = float('inf')
# dp = [[inf] * (m + 1)] * (n + 1)
dp = [[inf] * (m + 1) for _ in range(n + 1)]
# dp[0][0] = 0
for i in range(n + 1):
    dp[i][0] = 0
for i in range(1, n + 1):
    for j in range(m):
        if j - spaces[i - 1] < 0:
            dp[i][j] = dp[i-1][j]
        else:
            dp[i][j] = min(dp[i-1][j], dp[i-1][j - spaces[i - 1]] + costs[i - 1])
    dp[i][m] = dp[i - 1][m]
    for j in range(max(0, m - spaces[i - 1]), m + 1):
        dp[i][m] = min(dp[i][m], dp[i - 1][j] + costs[i - 1])
ans = dp[n][m]
if ans == inf:
    print('error')
else:
    print(ans)

---

it seems that only java can pass.

so can you tell me how to get inputs for java at online tests?
and can you teach me how to write fast for java?
is there a way to define int to long in java?


```python
import sys 
# from functools import cache
inputs = sys.stdin.read().split()
m = int(inputs[0])
n = int(inputs[1])

spaces = [0] * n 
# swaps = []
# recos = []
costs = [0] * n 
for i in range(n):
    # spaces.append(int(inputs[2 + i]))
    spaces[i] = int(inputs[2 + i])
    # swaps[i] = int(inputs[n + 2 + i])
    # recos[i] = int(inputs[2 * n + 2 + i])
    swap = int(inputs[n + 2 + i])
    reco = int(inputs[2 * n + 2 + i])
    costs[i] = min(swap, reco)
# print(spaces)
# print(costs)
inf = float('inf')
# dp = [[inf] * (m + 1)] * (n + 1)
# dp = [[inf] * (m + 1) for _ in range(n + 1)]
# # dp[0][0] = 0
# for i in range(n + 1):
#     dp[i][0] = 0
# for i in range(1, n + 1):
#     for j in range(m):
#         if j - spaces[i - 1] < 0:
#             dp[i][j] = dp[i-1][j]
#         else:
#             dp[i][j] = min(dp[i-1][j], dp[i-1][j - spaces[i - 1]] + costs[i - 1])
#     dp[i][m] = dp[i - 1][m]
#     for j in range(max(0, m - spaces[i - 1]), m + 1):
#         dp[i][m] = min(dp[i][m], dp[i - 1][j] + costs[i - 1])
# ans = dp[n][m]
dp = [inf] * (m + 1)
dp[0] = 0
for i in range(n):
    for j in range(m, -1, -1):
        # if j - spaces[i] < 0:
        #     continue
        target = max(0, j - spaces[i])
        if dp[target] != inf:
            dp[j] = min(dp[j], dp[target] + costs[i])
ans = dp[m]
if ans == inf:
    print('error')
else:
    print(ans)
```

# tf-idf 20250910

can you help me write the follow, python?

---

21.

找出相似度最高的文档

为了更快追踪突发热点，我们仅在“查询时刻 t 之前的最近 K 篇文档”内计算 TF‑IDF，并以加权余弦相似度挑选最相关的文档。

窗口内越新的文档权重越高（从旧到新第 j 篇的权重为 (K−j+1)/K）。

给定按时间递增的文档序列和若干查询（每条查询含时间点 t 与查询短语 q），请在窗口中找出与 q 的加权余弦相似度最高且相似度≥0.6 的文档编号；若存在并列最高，返回窗口中最早的那一篇；若无满足阈值的文档，输出 -1。

-   词向量用 TF‑IDF：TF 为词频；IDF 采用平滑公式 IDF(x)=log((N+1)/(df(x)+1))+1，其中 N 为窗口文档数，df(x) 为窗口内包含词 x 的文档数。
-   余弦相似度采用 q 与每个文档向量的点积除以范数乘积；文档向量还需乘以其时间权重。
-   文档与查询均以空格分词、统一小写，不做额外清洗。为避免早期窗口不足的问题，测试均保证 t ≥ K−1。

时间限制：C/C++ 1秒，其他语言2秒

空间限制：C/C++ 256M，其他语言512M

输入描述：

第一行：文档总数 N  

接下来 N 行：按时间从 0 到 N−1 的文档内容（小写，空格分词）    
下一行：窗口大小 K    
下一行：查询总数 P    
接下来 P 行：每行“t 空格 q”表示在时间点 t 的查询 q    
  

输出描述：

输出 P 个数字，空格分隔；每个数字是对应查询的文档编号或 -1  

补充说明：

本题由牛友@Charles 整理上传

示例1

输入例子：

5
breaking news finance market
sports football world cup
finance stock market rises
tech ai model training
finance market crash report
3
3
4 finance market
5 ai model
3 travel guide

输出例子：

4 3 -1

例子说明：

对 t=4，窗口为文档\[2,3,4\]。q="finance market" 与 2、4 的原始余弦相似度相同且约为 0.605≥0.6；时间权重越新越大（2:1/3, 3:2/3, 4:1），加权后 4 更高，返回 4。  
对 t=5，窗口为\[2,3,4\]。q="ai model" 仅与文档3匹配（含 ai、model），原始余弦≈0.707≥0.6，返回 3。  
对 t=3，窗口为\[1,2,3\]。q="travel guide" 窗口内均无重合词，余弦=0<0.6，返回 -1。  

# ans tf-idf

这道题是自然语言处理（NLP）中经典的 **TF-IDF 向量空间模型** 的变体。它的核心难点在于：
1. **滑动窗口**：IDF 的计算是基于当前查询窗口内的 $K$ 篇文档，而不是全局文档。
2. **时间加权**：余弦相似度计算出来后，需要根据文档在窗口中的“新鲜度”进行二次加权。
3. **判定逻辑**：阈值 $0.6$ 作用于原始相似度，而排名则基于加权后的相似度。

### 实现思路

1. **预处理**：由于文档量较大，先将每篇文档转为词频统计（`Counter`）和词集合（`Set`）。
2. **定位窗口**：根据 $t$ 和 $K$ 确定窗口范围。题目示例显示，若 $t$ 处有文档，窗口包含索引 $t$。窗口起始点为 $\max(0, t-K+1)$。
3. **计算 IDF**：
   - 遍历窗口内的文档，统计每个词出现的文档数 $df(x)$。
   - 使用公式 $IDF(x) = \ln((K+1)/(df(x)+1)) + 1$。
4. **计算余弦相似度**：
   - 查询向量 $V_q$ 和文档向量 $V_d$ 的分量均为 $TF \times IDF$。
   - 相似度 = $\frac{V_q \cdot V_d}{|V_q| \times |V_d|}$。
5. **时间加权与筛选**：
   - 权重 $W = \frac{\text{当前位置}}{\text{窗口大小}}$（旧到新为 $1/K \dots K/K$）。
   - **重要判断**：若 **原始余弦相似度 $\ge 0.6$**，则计算加权得分，并挑选最高分。

### Python 代码实现

```python
import sys
import math
from collections import Counter

def solve():
    # 使用 fast I/O 读取所有输入
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
    
    line_ptr = 0
    while line_ptr < len(input_data) and not input_data[line_ptr].strip():
        line_ptr += 1
    
    # 1. 读取文档
    N_docs = int(input_data[line_ptr].strip())
    line_ptr += 1
    
    docs_counts = []
    docs_unique = []
    
    for i in range(N_docs):
        # 统一小写分词
        tokens = input_data[line_ptr].strip().lower().split()
        docs_counts.append(Counter(tokens))
        docs_unique.append(set(tokens))
        line_ptr += 1
        
    # 2. 读取窗口大小 K 和查询数 P
    while line_ptr < len(input_data) and not input_data[line_ptr].strip():
        line_ptr += 1
    K = int(input_data[line_ptr].strip())
    line_ptr += 1
    
    while line_ptr < len(input_data) and not input_data[line_ptr].strip():
        line_ptr += 1
    P = int(input_data[line_ptr].strip())
    line_ptr += 1
    
    results = []
    
    # 3. 处理每个查询
    for _ in range(P):
        if line_ptr >= len(input_data): break
        query_line = input_data[line_ptr].strip().lower().split()
        line_ptr += 1
        if not query_line:
            results.append("-1")
            continue
            
        t = int(query_line[0])
        q_tokens = query_line[1:]
        q_counts = Counter(q_tokens)
        
        # 确定窗口范围 [start_idx, end_idx]
        end_idx = min(N_docs - 1, t)
        start_idx = max(0, end_idx - K + 1)
        
        # 统计窗口内的词频 df
        window_df = {}
        for i in range(start_idx, end_idx + 1):
            for word in docs_unique[i]:
                window_df[word] = window_df.get(word, 0) + 1
        
        # 计算 IDF (仅针对窗口内出现的词)
        idfs = {}
        for word, df_val in window_df.items():
            idfs[word] = math.log((K + 1) / (df_val + 1)) + 1
            
        # 计算查询向量的范数 |Vq|
        # 窗口外没出现的词 df=0，平滑计算
        idf_zero = math.log((K + 1) / 1) + 1
        norm_q_sq = 0
        for word, count in q_counts.items():
            idf_q = idfs.get(word, idf_zero)
            norm_q_sq += (count * idf_q) ** 2
        norm_q = math.sqrt(norm_q_sq)
        
        max_weighted_score = -1.0
        best_doc_id = -1
        
        # 遍历窗口文档计算相似度
        for i in range(start_idx, end_idx + 1):
            d_counts = docs_counts[i]
            
            # 计算点积和文档范数 |Vd|
            dot_product = 0
            for word, q_c in q_counts.items():
                if word in d_counts:
                    idf = idfs[word]
                    dot_product += (q_c * idf) * (d_counts[word] * idf)
            
            norm_d_sq = sum((count * idfs[word])**2 for word, count in d_counts.items())
            norm_d = math.sqrt(norm_d_sq)
            
            cos_sim = 0
            if norm_q > 0 and norm_d > 0:
                cos_sim = dot_product / (norm_q * norm_d)
            
            # 判定阈值：原始相似度 >= 0.6
            if cos_sim >= 0.6 - 1e-9:
                # 计算时间权重：越新权重越高
                # j 为从旧到新第几篇 (1 ~ K)
                j = i - start_idx + 1
                weight = j / K
                weighted_score = cos_sim * weight
                
                # 记录最高分（若分数相同，由于是顺序遍历，自动保留最早的编号）
                if weighted_score > max_weighted_score + 1e-9:
                    max_weighted_score = weighted_score
                    best_doc_id = i
        
        results.append(str(best_doc_id))
        
    print(" ".join(results))

if __name__ == "__main__":
    solve()
```

### 关键点解释

1.  **窗口边界**：根据题目示例 1，$t=4, K=3$ 时窗口是 `[2,3,4]`。这说明 $t$ 本身是包含在窗口内的。代码中通过 `range(start_idx, end_idx + 1)` 覆盖了这个范围。
2.  **IDF 平滑**：题目要求的公式是 `log((N+1)/(df+1)) + 1`。其中 $N$ 固定为窗口大小 $K$。即使某个查询词在窗口中一次也没出现过（$df=0$），它的 IDF 依然存在，需要参与查询向量范数的计算。
3.  **浮点数精度**：在进行 `weighted_score > max_weighted_score` 比较时，加入 `1e-9` 的偏移量可以避免浮点数精度误差导致的判断失误。
4.  **并列处理**：题目要求并列时取“窗口中最早的”。因为我们的循环是从 `start_idx`（旧）到 `end_idx`（新）进行的，使用 `>` 而不是 `>=` 就能保证在得分相同时保留第一次出现的那个文档。
        

        
# 最小二乘 slope 20250910

thank you. tf-idf is just too difficult for me.

how about this?
i am not sure how to calculate std and slope.
---

22.

统计量列表

给定一个整数序列与一个窗口大小列表。对每一行输入，固定一个公共右边界，对窗口列表中的每个窗口长度各取一个“右对齐”的子数组，分别计算5个统计量，并按窗口列表的顺序依次拼接成一行结果；沿着序列从左到右依次移动右边界，生成多行输出。

### 统计量与计算约定

-   每个子数组输出5项（固定顺序）：mean、std、min、max、slope。
-   **std**: 样本标准差（ddof=1）。当窗口长度为1时，std=0。
-   **slope**: 最小二乘直线斜率，横坐标为 x=0..w−1。若分母为0或 w=1，则 slope=0。
-   数值格式：若为整数则不带小数点；非整数最多保留3位小数，四舍五入，去掉末尾无意义的0（如 1.0→1，1.10→1.1，1.1116→1.112）。

### 窗口对齐与行数

-   **窗口对齐方式：右对齐**。第 i 行的公共右边界为 R=i+max(window\_array)−1。对窗口大小 w，取子数组 arr\[R−w+1…R\]。
-   行数 n = len(input\_array) − max(window\_array) + 1。若 len(input\_array) < 任一窗口大小，则输出为空。

时间限制：C/C++ 1秒，其他语言2秒

空间限制：C/C++ 256M，其他语言512M

输入描述：

支持多行输入；每行一组数据，格式为：  
  \[整数序列\], \[窗口大小序列\]  
例如：\[1, 2, 3, 4, 5\], \[2, 3\]  

输出描述：

对每一行输入，按行输出多个结果行；每个结果行是该位置处按窗口列表顺序拼接的统计量列表。  
若该行输入不满足条件（如数组过短），仅输出一行“\[\]”。  

# answer slope

这道统计量计算题的核心在于**滑动窗口**的处理和**最小二乘法（Linear Regression）**的公式应用。

### 1. 算法核心公式

*   **均值 (Mean)**: $\bar{y} = \frac{\sum y_i}{w}$
*   **样本标准差 (Std)**: $s = \sqrt{\frac{\sum (y_i - \bar{y})^2}{w - 1}}$ (注意 $w=1$ 时为 0)。
*   **最小二乘斜率 (Slope)**:
    已知自变量为 $x = [0, 1, 2, \dots, w-1]$。
    公式：$slope = \frac{SS_{xy}}{SS_{xx}}$
    其中：
    *   $SS_{xx} = \sum x_i^2 - \frac{(\sum x_i)^2}{w} = \frac{w(w^2-1)}{12}$
    *   $SS_{xy} = \sum (x_i \cdot y_i) - \frac{(\sum x_i)(\sum y_i)}{w}$
    *   $\sum x_i = \frac{w(w-1)}{2}$

### 2. Python 实现

Python 处理字符串和格式化非常方便。我们使用自定义函数来处理题目要求的“四舍五入并去除末尾无效 0”的逻辑。

```python
import sys
import math

def format_num(x):
    """格式化数字：保留3位小数，去掉末尾无效0，整数不带小数点"""
    # 题目要求四舍五入，round(1.1116, 3) -> 1.112
    r = round(float(x), 3)
    if r == int(r):
        return str(int(r))
    # 使用 .3f 确保保留三位，然后去掉右侧的 0 和可能剩下的点
    s = f"{r:.3f}"
    return s.rstrip('0').rstrip('.')

def solve():
    for line in sys.stdin:
        line = line.strip()
        if not line: continue
        
        # 1. 解析输入格式: [1, 2, 3], [2, 3]
        try:
            split_idx = line.find("], [")
            if split_idx == -1: continue
            
            data_part = line[1:split_idx]
            win_part = line[split_idx+4:-1]
            
            data = [int(x.strip()) for x in data_part.split(',')]
            windows = [int(x.strip()) for x in win_part.split(',')]
        except:
            continue

        # 2. 检查基本条件
        max_w = max(windows)
        if len(data) < max_w:
            print("[]")
            continue
        
        # 3. 滑动窗口计算 (R 是公共右边界索引)
        for r in range(max_w - 1, len(data)):
            row_results = []
            for w in windows:
                # 获取子数组 data[R-w+1 ... R]
                sub = data[r - w + 1 : r + 1]
                
                # --- Mean ---
                mean_val = sum(sub) / w
                
                # --- Std (ddof=1) ---
                if w == 1:
                    std_val = 0.0
                else:
                    variance = sum((y - mean_val)**2 for y in sub) / (w - 1)
                    std_val = math.sqrt(max(0, variance)) # max(0, var) 防止精度导致的负数
                
                # --- Min / Max ---
                min_val = min(sub)
                max_val = max(sub)
                
                # --- Slope ---
                if w == 1:
                    slope_val = 0.0
                else:
                    # x 为 0, 1, ..., w-1
                    ss_xx = w * (w * w - 1) / 12.0
                    sum_x = w * (w - 1) / 2.0
                    sum_y = sum(sub)
                    sum_xy = sum(i * sub[i] for i in range(w))
                    ss_xy = sum_xy - (sum_x * sum_y) / w
                    slope_val = ss_xy / ss_xx
                
                row_results.extend([mean_val, std_val, min_val, max_val, slope_val])
            
            # 4. 格式化输出
            print("[" + ", ".join(format_num(v) for v in row_results) + "]")

if __name__ == "__main__":
    solve()
```

---

### 3. C++ 实现

C++ 实现时，解析字符串较为繁琐，且需要注意 `double` 的精度和格式化输出。

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <numeric>
#include <cmath>
#include <algorithm>
#include <iomanip>

using namespace std;

// 自定义格式化函数
string formatNum(double val) {
    double r = round(val * 1000.0) / 1000.0;
    if (abs(r - round(r)) < 1e-9) return to_string((long long)round(r));
    
    stringstream ss;
    ss << fixed << setprecision(3) << r;
    string s = ss.str();
    s.erase(s.find_last_not_of('0') + 1, string::npos);
    if (s.back() == '.') s.pop_back();
    return s;
}

void processLine(string line) {
    // 简单的解析逻辑，实际面试建议用更健壮的解析
    size_t split_pos = line.find("], [");
    if (split_pos == string::npos) return;

    auto parseVec = [](string s) {
        vector<int> res;
        for (auto& ch : s) if (ch == '[' || ch == ']' || ch == ',') ch = ' ';
        stringstream ss(s);
        int temp;
        while (ss >> temp) res.push_back(temp);
        return res;
    };

    vector<int> data = parseVec(line.substr(0, split_pos + 1));
    vector<int> windows = parseVec(line.substr(split_pos + 2));

    int max_w = 0;
    for (int w : windows) max_w = max(max_w, w);

    if (data.size() < (size_t)max_w) {
        cout << "[]" << endl;
        return;
    }

    for (int r = max_w - 1; r < (int)data.size(); ++r) {
        cout << "[";
        for (size_t i = 0; i < windows.size(); ++i) {
            int w = windows[i];
            vector<double> sub;
            for (int j = r - w + 1; j <= r; ++j) sub.push_back(data[j]);

            double sum_y = accumulate(sub.begin(), sub.end(), 0.0);
            double mean = sum_y / w;

            double var_sum = 0;
            for (double y : sub) var_sum += (y - mean) * (y - mean);
            double std_v = (w == 1) ? 0 : sqrt(var_sum / (w - 1));

            double min_v = *min_element(sub.begin(), sub.end());
            double max_v = *max_element(sub.begin(), sub.end());

            double slope = 0;
            if (w > 1) {
                double ss_xx = w * (double(w) * w - 1) / 12.0;
                double sum_x = w * (w - 1) / 2.0;
                double sum_xy = 0;
                for (int j = 0; j < w; ++j) sum_xy += j * sub[j];
                double ss_xy = sum_xy - (sum_x * sum_y) / w;
                slope = ss_xy / ss_xx;
            }

            double res[5] = {mean, std_v, min_v, max_v, slope};
            for (int j = 0; j < 5; ++j) {
                cout << formatNum(res[j]) << (j == 4 && i == windows.size() - 1 ? "" : ", ");
            }
        }
        cout << "]" << endl;
    }
}

int main() {
    string line;
    while (getline(cin, line)) {
        if (!line.empty()) processLine(line);
    }
    return 0;
}
```

### 关键点总结：
1.  **右对齐窗口**：对于数组索引，`R` 从 `max_w - 1` 开始增加，子数组的范围始终是 `[R-w+1, R]`。
2.  **最小二乘法技巧**：当 $x$ 是连续整数 $0 \dots w-1$ 时，$\sum x$ 和 $SS_{xx}$ 都有直接的数学公式，可以极大减少计算量并提高精度。
3.  **格式化**：题目要求的格式化其实就是寻找 `round(x, 3)` 之后的最短字符串表示（不带多余的 `0`）。在 Python 中 `f"{val:g}"` 也有类似效果，但为了严格控制 3 位小数，建议用 `rstrip` 手动处理。




















