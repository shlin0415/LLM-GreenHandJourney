# int8 quant

你能教教我如何在线上机考做这题吗？
使用python, java和cpp写, 非常感谢。


---

21.

INT8 非对称量化下的全连接与误差评估

在移动端或边缘设备上，浮点运算成本较高。常见做法是将输入向量和全连接层权重做 INT8 非对称量化（按张量整体 per-tensor），用整数在量化域直接做点积，最后用反量化结果评估与原始浮点结果的误差。

【任务】

-   对输入向量 x 和权重矩阵 W 分别做 INT8 非对称量化（范围 \[-128, 127\]，不加偏置），输出量化域的 m 个整数点积结果。
-   将量化后的 x 与 W 分别反量化为 x\_dequant、W\_dequant，计算二者在浮点域的全连接输出，与原始 x、W 的浮点输出做均方误差 MSE，并输出 round\_half\_up(MSE × 100000) 的整数。
-   量化/反量化细节（per-tensor）：
    -   scale = (max(v) - min(v)) / 255
    -   若 max(v) == min(v)，则 scale = 0，量化结果全为 -128；反量化直接取 min(v)
    -   量化：q = clamp(round((v - min(v)) / scale) - 128, -128, 127)，round 为就近取偶
    -   反量化：v\_dequant = (q + 128) \* scale + min(v)
-   MSE 四舍五入采用 half-up（即对 MSE×100000 做 “x+0.5 下取整”）

时间限制：C/C++ 1秒，其他语言2秒

空间限制：C/C++ 256M，其他语言512M

输入描述：

-   第一行：n（输入向量维度）
-   第二行：n 个浮点数（输入向量 x）
-   第三行：m n（权重矩阵维度）
-   接着 m 行：每行 n 个浮点数（权重矩阵 W）

输出描述：

-   第一行：m 个整数（使用 x\_quant 与 W\_quant 计算的量化域全连接输出）
-   第二行：1 个整数（round\_half\_up(MSE × 100000)）

补充说明：

本题由牛友@Charles 整理上传

示例1

输入例子：

3
0 128 255
2 3
0 0 0
255 255 255

输出例子：

128 -127
0

例子说明：

-   对 x：min=0, max=255, scale=1 → x\_quant=\[-128, 0, 127\]
-   对 W（按张量整体）：min=0, max=255, scale=1 → 第1行量化为\[-128,-128,-128\]，第2行为\[127,127,127\]
-   量化域点积：
    -   y0 = (-128)_(-128) + 0_(-128) + 127\*(-128) = 128
    -   y1 = (-128)_127 + 0_127 + 127\*127 = -127
-   反量化后与原始浮点结果一致，MSE=0，输出 0


---

# ans

这道题目考察的是工业界深度学习模型量化（Quantization）的基础实现。核心点在于**非对称量化算法**、**就近取偶（Banker's Rounding）**以及**精度损失评估（MSE）**。

下面我为你分别提供 Python、C++ 和 Java 的代码实现，并详细讲解线上机考的注意事项。

---

### 核心逻辑梳理

1.  **量化参数 (Scale, Min)**：按张量（Per-tensor）计算。
2.  **量化公式**：$q = \text{clamp}(\text{round}(\frac{v - min}{scale}) - 128, -128, 127)$。
    *   注意：此处的 `round` 是 **就近取偶**（4.5 $\to$ 4, 5.5 $\to$ 6）。
3.  **反量化公式**：$v_{dequant} = (q + 128) \times scale + min$。
4.  **量化域计算**：直接用 `int8` 的量化值 $q$ 进行矩阵乘法。
5.  **误差计算**：计算原始浮点结果与反量化后浮点结果的 MSE，最后进行 **四舍五入（Half-up）**。

---

### 1. Python 实现
Python 的内置 `round()` 默认就是“就近取偶”，非常方便。

```python
import sys

def solve():
    # 读取输入
    input_data = sys.stdin.read().split()
    if not input_data: return
    
    idx = 0
    n = int(input_data[idx]); idx += 1
    x = [float(input_data[i]) for i in range(idx, idx + n)]; idx += n
    m = int(input_data[idx]); idx += 1
    _n = int(input_data[idx]); idx += 1 # _n 应该等于 n
    w = []
    for i in range(m):
        w.append([float(input_data[j]) for j in range(idx, idx + n)])
        idx += n

    def get_quant_params(data):
        v_min, v_max = min(data), max(data)
        if v_min == v_max:
            return 0.0, v_min, [-128] * len(data)
        scale = (v_max - v_min) / 255.0
        # Python 的 round 就是就近取偶
        q = [max(-128, min(127, int(round((v - v_min) / scale)) - 128)) for v in data]
        return scale, v_min, q

    # 量化 x
    scale_x, min_x, q_x = get_quant_params(x)
    
    # 量化 W (按整个矩阵张量)
    all_w = [val for row in w for val in row]
    scale_w, min_w, _ = get_quant_params(all_w)
    q_w = []
    for row in w:
        if scale_w == 0:
            q_w.append([-128] * n)
        else:
            q_w.append([max(-128, min(127, int(round((v - min_w) / scale_w)) - 128)) for v in row])

    # 1. 计算量化域点积
    y_quant = []
    for i in range(m):
        dot = sum(q_x[j] * q_w[i][j] for j in range(n))
        y_quant.append(dot)
    print(*(y_quant))

    # 2. 计算反量化值与 MSE
    def dequant(q_list, s, v_min):
        return [(q + 128) * s + v_min for q in q_list]

    x_de = dequant(q_x, scale_x, min_x)
    w_de = [dequant(row, scale_w, min_w) for row in q_w]

    mse_sum = 0
    for i in range(m):
        # 原始浮点输出
        y_float = sum(x[j] * w[i][j] for j in range(n))
        # 反量化浮点输出
        y_dequant = sum(x_de[j] * w_de[i][j] for j in range(n))
        mse_sum += (y_float - y_dequant) ** 2
    
    mse = mse_sum / m
    # 四舍五入 (Half-up): int(x + 0.5)
    print(int(mse * 100000 + 0.5))

solve()
```

---

### 2. C++ 实现
C++ 需要手动实现“就近取偶”逻辑（或使用 `nearbyint`），并且要注意浮点数精度。

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <numeric>

using namespace std;

// 就近取偶实现
double banker_round(double x) {
    return nearbyint(x); 
}

struct QuantResult {
    double scale;
    double min_v;
    vector<int> q;
};

QuantResult quantize(const vector<double>& v) {
    double min_v = v[0], max_v = v[0];
    for (double x : v) {
        min_v = min(min_v, x);
        max_v = max(max_v, x);
    }
    
    if (min_v == max_v) {
        return {0.0, min_v, vector<int>(v.size(), -128)};
    }
    
    double scale = (max_v - min_v) / 255.0;
    vector<int> q(v.size());
    for (int i = 0; i < v.size(); ++i) {
        int val = (int)banker_round((v[i] - min_v) / scale) - 128;
        q[i] = max(-128, min(127, val));
    }
    return {scale, min_v, q};
}

int main() {
    int n, m;
    if (!(cin >> n)) return 0;
    vector<double> x(n);
    for (int i = 0; i < n; ++i) cin >> x[i];
    
    cin >> m >> n;
    vector<vector<double>> w(m, vector<double>(n));
    vector<double> all_w;
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            cin >> w[i][j];
            all_w.push_back(w[i][j]);
        }
    }

    auto res_x = quantize(x);
    auto res_w_all = quantize(all_w);

    // 1. 量化域点积
    vector<long long> y_quant(m);
    for (int i = 0; i < m; ++i) {
        long long sum_q = 0;
        for (int j = 0; j < n; ++j) {
            int qw = (res_w_all.scale == 0) ? -128 : (int)banker_round((w[i][j] - res_w_all.min_v) / res_w_all.scale) - 128;
            qw = max(-128, min(127, qw));
            sum_q += (long long)res_x.q[j] * qw;
        }
        y_quant[i] = sum_q;
        cout << y_quant[i] << (i == m - 1 ? "" : " ");
    }
    cout << endl;

    // 2. MSE 计算
    double mse_sum = 0;
    for (int i = 0; i < m; ++i) {
        double y_float = 0, y_dequant = 0;
        for (int j = 0; j < n; ++j) {
            y_float += x[j] * w[i][j];
            
            double x_de = (res_x.q[j] + 128) * res_x.scale + res_x.min_v;
            int qw = (res_w_all.scale == 0) ? -128 : (int)banker_round((w[i][j] - res_w_all.min_v) / res_w_all.scale) - 128;
            qw = max(-128, min(127, qw));
            double w_de = (qw + 128) * res_w_all.scale + res_w_all.min_v;
            
            y_dequant += x_de * w_de;
        }
        mse_sum += pow(y_float - y_dequant, 2);
    }

    double mse = mse_sum / m;
    cout << (long long)floor(mse * 100000 + 0.5) << endl;

    return 0;
}
```

---

### 3. Java 实现
Java 的 `Math.rint()` 是专门处理“就近取偶”的方法。

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        
        int n = sc.nextInt();
        double[] x = new double[n];
        for (int i = 0; i < n; i++) x[i] = sc.nextDouble();
        
        int m = sc.nextInt();
        int _n = sc.nextInt();
        double[][] w = new double[m][n];
        double minW = Double.MAX_VALUE, maxW = -Double.MAX_VALUE;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                w[i][j] = sc.nextDouble();
                minW = Math.min(minW, w[i][j]);
                maxW = Math.max(maxW, w[i][j]);
            }
        }

        // 处理 X 量化
        double minX = x[0], maxX = x[0];
        for (double val : x) {
            minX = Math.min(minX, val);
            maxX = Math.max(maxX, val);
        }
        double scaleX = (maxX == minX) ? 0 : (maxX - minX) / 255.0;
        int[] qX = new int[n];
        for (int i = 0; i < n; i++) {
            if (scaleX == 0) qX[i] = -128;
            else qX[i] = (int) Math.max(-128, Math.min(127, Math.rint((x[i] - minX) / scaleX) - 128));
        }

        // 处理 W 量化
        double scaleW = (maxW == minW) ? 0 : (maxW - minW) / 255.0;
        int[][] qW = new int[m][n];
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (scaleW == 0) qW[i][j] = -128;
                else qW[i][j] = (int) Math.max(-128, Math.min(127, Math.rint((w[i][j] - minW) / scaleW) - 128));
            }
        }

        // 1. 量化域点积
        for (int i = 0; i < m; i++) {
            long sum = 0;
            for (int j = 0; j < n; j++) sum += (long) qX[j] * qW[i][j];
            System.out.print(sum + (i == m - 1 ? "" : " "));
        }
        System.out.println();

        // 2. MSE
        double mseSum = 0;
        for (int i = 0; i < m; i++) {
            double yFloat = 0, yDequant = 0;
            for (int j = 0; j < n; j++) {
                yFloat += x[j] * w[i][j];
                double xDe = (qX[j] + 128) * scaleX + minX;
                double wDe = (qW[i][j] + 128) * scaleW + minW;
                yDequant += xDe * wDe;
            }
            mseSum += Math.pow(yFloat - yDequant, 2);
        }
        System.out.println((long) Math.floor(mseSum / m * 100000 + 0.5));
    }
}
```

---

### 💡 线上机考做题技巧

1.  **关于 Rounding（舍入方式）**：
    *   题目明确说是“就近取偶”（Banker's rounding），这是量化中减少系统误差的常用手段。
    *   **Python**: `round(4.5) -> 4`, `round(5.5) -> 6`（天然符合）。
    *   **C++**: `round(4.5)` 会得到 `5`。必须用 `nearbyint(x)` 或者 `std::remainder` 手写逻辑。
    *   **Java**: `Math.rint(x)` 是就近取偶，`Math.round(x)` 是四舍五入。
2.  **关于 MSE 四舍五入**：
    *   题目要求对 `MSE * 100000` 做 `x+0.5` 下取整，这其实就是最标准的 **四舍五入**。
    *   公式：`floor(val + 0.5)`。
3.  **注意 Scale=0 的特殊情况**：
    *   当 `max == min` 时，题目规定 `scale = 0` 且量化值全为 `-128`。代码中一定要有这个 `if` 判断，否则会发生除以零错误。
4.  **数据范围与类型**：
    *   量化域的点积结果（`y_quant`）可能会超过 `int`（32位整数）的范围吗？
        $127 \times 127 \times n$。如果 $n=10^5$，结果会到 $1.6 \times 10^9$，`int` 勉强够，但为了安全，建议 C++/Java 使用 `long long` / `long`。
5.  **Per-tensor 量化**：
    *   注意题目要求对 $W$ 整体做量化，意味着你要先找出整个 $W$ 矩阵（$m \times n$ 个数）的 `min` 和 `max`，而不是按行量化。