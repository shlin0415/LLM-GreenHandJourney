# seq dp ?

你能教教我如何在线上机考做这题吗？
使用python, java和cpp写。

---

22.

最优分词器

你在为一门极少见的语言做专用分词。语言学家给出了一个“小词典”，每个条目都有一个分值，表示该词单独成词的合理性强弱。  
同时，还收集了“相邻词对”的转移加分：当上一个词与下一个词按某种搭配出现时，整体会多（或少）一些分数。  
你的目标是在给定的连续小写字母串中，切分出一条完整的词序列，使“词典分+转移加分”的总和最大。如果无法用词典完全覆盖整串，则输出0。  

时间限制：C/C++ 1秒，其他语言2秒

空间限制：C/C++ 256M，其他语言512M

输入描述：

第一行：文本串 text，仅含小写英文字母。  
第二行：整数 n，表示词典条目数。  
接下来 n 行：每行一个词与其分值，中间用空格分隔。  
接下来一行：整数 m，表示转移加分条目数。  
接下来 m 行：每行包含“前词 后词 加分”，三者以空格分隔，加分可为负。  

输出描述：

一行，一个整数：最大可获得的总分。如果不存在任何完整切分，输出0。

补充说明：

本题由牛友@Charles 整理上传

示例1

输入例子：

aababa
4
a 1
aa 3
ab 2
ba 2
3
aa ba 2
ba ba -1
ab a 1

输出例子：

8

例子说明：

-   最优切分：aa | ba | ba
    -   词典分：3 + 2 + 2 = 7
    -   转移分：aa→ba = +2，ba→ba = -1
    -   总分：7 + 2 - 1 = 8
-   其他可行切分（例如：a | ab | a | ba）
    -   词典分：1 + 2 + 1 + 2 = 6
    -   转移分：ab→a = +1（其余未命中）
    -   总分：6 + 1 = 7  
        因此最优答案为 8。

---

# ans

这道题是**序列型动态规划（Sequence DP）**的变体。它在普通的分词 DP（比如“单词拆分”）基础上，增加了一个**状态维度**（前一个词是谁），用来处理“相邻词对”的转移加分。

### 解题思路

1.  **状态定义**：
    $dp[i][word]$ 表示：文本串的前 $i$ 个字符，在最后一个拆出的词是 $word$ 的情况下，能获得的最高总分。
2.  **转移方程**：
    假设当前我们要从位置 $j$ 切换到位置 $i$（即 `text[j:i]` 是词典里的一个词 `curr_word`）：
    *   **情况 A（它是第一个词）**：如果 $j=0$（即 `text[0:i]` 为 `curr_word`），则：
        $dp[i][curr\_word] = score(curr\_word)$
    *   **情况 B（它不是第一个词）**：我们需要遍历所有在位置 $j$ 结束的上一个词 `prev_word`：
        $dp[i][curr\_word] = \max(dp[i][curr\_word], dp[j][prev\_word] + score(curr\_word) + bonus(prev\_word, curr\_word))$
3.  **优化**：
    由于我们只关心“能组成词的子串”，所以外部循环遍历结束位置 $i$，内部循环只需回溯到词典中词的最大长度即可。

---

### Python 实现

Python 处理字符串和字典非常方便。使用 `defaultdict` 来简化 DP 表的初始化。

```python
import sys

def solve():
    # 读取输入
    input_data = sys.stdin.read().split()
    if not input_data: return
    
    text = input_data[0]
    n = int(input_data[1])
    
    dict_scores = {}
    idx = 2
    for _ in range(n):
        word = input_data[idx]
        score = int(input_data[idx+1])
        dict_scores[word] = score
        idx += 2
    
    m = int(input_data[idx])
    idx += 1
    trans_scores = {} # (prev, curr) -> bonus
    for _ in range(m):
        w1 = input_data[idx]
        w2 = input_data[idx+1]
        bonus = int(input_data[idx+2])
        trans_scores[(w1, w2)] = bonus
        idx += 3
        
    L = len(text)
    # dp[i] 是一个字典：{词: 分数}，表示以该词结束且覆盖了text[:i]的最大分
    dp = [{} for _ in range(L + 1)]
    
    # 获取词典中词的最大长度，优化搜索
    max_len = 0
    if dict_scores:
        max_len = max(len(w) for w in dict_scores)

    for i in range(1, L + 1):
        # 尝试所有可能的当前词结束位置 i，起始位置 j
        for length in range(1, min(i, max_len) + 1):
            # length from small to large
            j = i - length
            curr_word = text[j:i] # key point
            
            if curr_word in dict_scores:
                c_score = dict_scores[curr_word]
                # 情况A: text[0:i] 直接就是一个词
                if j == 0:
                    dp[i][curr_word] = max(dp[i].get(curr_word, -float('inf')), c_score)
                # 情况B: 接在之前的分词结果后面
                elif dp[j]:
                    for prev_word, p_total_score in dp[j].items():
                        bonus = trans_scores.get((prev_word, curr_word), 0)
                        new_score = p_total_score + c_score + bonus
                        dp[i][curr_word] = max(dp[i].get(curr_word, -float('inf')), new_score)
    
    # 结果
    if not dp[L]:
        print(0)
    else:
        ans = max(dp[L].values())
        print(max(0, ans)) # 题目要求无法覆盖输出0，如果结果为负也应根据题意判断，此处取max(0)

solve()
```

---

### C++ 实现

C++ 中使用 `unordered_map` 来存储转移分数和 DP 状态。

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>

using namespace std;

typedef long long ll;

int main() {
    string text;
    if (!(cin >> text)) return 0;

    int n;
    cin >> n;
    unordered_map<string, int> dict_scores;
    int max_len = 0;
    for (int i = 0; i < n; ++i) {
        string w;
        int s;
        cin >> w >> s;
        dict_scores[w] = s;
        max_len = max(max_len, (int)w.length());
    }

    int m;
    cin >> m;
    // 使用嵌套 map 存储转移分: trans[prev][curr] = bonus
    unordered_map<string, unordered_map<string, int>> trans;
    for (int i = 0; i < m; ++i) {
        string w1, w2;
        int b;
        cin >> w1 >> w2 >> b;
        trans[w1][w2] = b;
    }

    int L = text.length();
    // dp[i] 存储以某个 word 结尾的 text[0...i-1] 的最大分数
    vector<unordered_map<string, ll>> dp(L + 1);

    for (int i = 1; i <= L; ++i) {
        for (int len = 1; len <= max_len && len <= i; ++len) {
            int j = i - len;
            string curr_word = text.substr(j, len);
            if (dict_scores.count(curr_word)) {
                ll c_score = dict_scores[curr_word];
                if (j == 0) {
                    if (dp[i].find(curr_word) == dp[i].end() || c_score > dp[i][curr_word])
                        dp[i][curr_word] = c_score;
                } else {
                    for (auto const& [prev_word, p_score] : dp[j]) {
                        int bonus = 0;
                        if (trans.count(prev_word) && trans[prev_word].count(curr_word)) {
                            bonus = trans[prev_word][curr_word];
                        }
                        ll new_score = p_score + c_score + bonus;
                        if (dp[i].find(curr_word) == dp[i].end() || new_score > dp[i][curr_word])
                            dp[i][curr_word] = new_score;
                    }
                }
            }
        }
    }

    if (dp[L].empty()) {
        cout << 0 << endl;
    } else {
        ll max_ans = -2e18; // 极小值
        for (auto const& [word, score] : dp[L]) {
            max_ans = max(max_ans, score);
        }
        cout << max(0LL, max_ans) << endl;
    }

    return 0;
}
```

---

### Java 实现

Java 版本注意 `Map` 的嵌套和 `Long` 类型的使用。

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNext()) return;
        
        String text = sc.next();
        int n = sc.nextInt();
        Map<String, Integer> dictScores = new HashMap<>();
        int maxLen = 0;
        for (int i = 0; i < n; i++) {
            String w = sc.next();
            int s = sc.nextInt();
            dictScores.put(w, s);
            maxLen = Math.max(maxLen, w.length());
        }
        
        int m = sc.nextInt();
        Map<String, Map<String, Integer>> trans = new HashMap<>();
        for (int i = 0; i < m; i++) {
            String w1 = sc.next();
            String w2 = sc.next();
            int b = sc.nextInt();
            trans.computeIfAbsent(w1, k -> new HashMap<>()).put(w2, b);
        }
        
        int L = text.length();
        Map<String, Long>[] dp = new HashMap[L + 1];
        for (int i = 0; i <= L; i++) dp[i] = new HashMap<>();
        
        for (int i = 1; i <= L; i++) {
            for (int len = 1; len <= maxLen && len <= i; len++) {
                int j = i - len;
                String currWord = text.substring(j, i);
                if (dictScores.containsKey(currWord)) {
                    long cScore = dictScores.get(currWord);
                    if (j == 0) {
                        dp[i].put(currWord, Math.max(dp[i].getOrDefault(currWord, Long.MIN_VALUE), cScore));
                    } else {
                        for (Map.Entry<String, Long> entry : dp[j].entrySet()) {
                            String prevWord = entry.getKey();
                            long pScore = entry.getValue();
                            int bonus = 0;
                            if (trans.containsKey(prevWord) && trans.get(prevWord).containsKey(currWord)) {
                                bonus = trans.get(prevWord).get(currWord);
                            }
                            long newScore = pScore + cScore + bonus;
                            dp[i].put(currWord, Math.max(dp[i].getOrDefault(currWord, Long.MIN_VALUE), newScore));
                        }
                    }
                }
            }
        }
        
        if (dp[L].isEmpty()) {
            System.out.println(0);
        } else {
            long maxAns = Long.MIN_VALUE;
            for (long score : dp[L].values()) {
                maxAns = Math.max(maxAns, score);
            }
            System.out.println(Math.max(0, maxAns));
        }
    }
}
```

---

### 机考技巧

1.  **为什么用 `dp[i]` 存 Map 而不是数组？**
    词典里的词是不确定的，无法用简单的数字索引。存 `Map<词, 分数>` 可以让我们只处理“确实能走到这一步”的词，大大减少无效计算。
2.  **处理“无法覆盖”**：
    初始化 DP 时，如果某个位置 `dp[j]` 是空的，说明前 `j` 个字符根本没法拆出合法的词。我们跳过这些位置，自然就处理了“必须完整覆盖”的要求。
3.  **负分处理**：
    由于 `bonus` 可能为负，初始化最大值时要用一个非常小的数（如 `LLONG_MIN` 或 `-1e18`），最后输出时再与 0 做对比。


# float dp

你能教教我如何在线上机考做这题吗？
使用python, java和cpp写。
碰到浮点数背包？
不会写了，救命。
谢谢。

---

21.

加速优化问题

某物流公司需要为一条运输线路上的多个中转段选择运输方案。整条线路由若干个中转段组成，每个中转段可以选择不同的运输方式（如空运、陆运等），不同方式的运费和延误风险各不相同。  
  
公司的目标是在保证总延误风险不超过给定阈值的前提下，使得整条线路的总运费最低。  
  
具体条件如下：每个中转段在不同运输方式下有各自的延误风险值（浮点数）和运费（浮点数）。每个中转段必须且只能选择一种运输方式。所有中转段的延误风险之和不能超过阈值 T。  
  
请设计算法，为每个中转段选择最优的运输方式，使得总运费最小且满足总延误风险不超过 T。  

时间限制：C/C++ 1秒，其他语言2秒

空间限制：C/C++ 256M，其他语言512M

输入描述：

第一行：整数 L（中转段数量）和浮点数 T（延误风险阈值）。  
接下来 L 行，每行描述一个中转段的可选方案：先是一个整数 K（该中转段可选的运输方式数量），随后是 K 组数据，每组包含：方式名称（字符串）、延误风险（浮点数）、运费（浮点数）。  

输出描述：

输出最优总运费（保留两位小数）。

补充说明：

本题由牛友@Charles 整理上传

示例1

输入例子：

2 0.4
2 express 0.1 300.0 standard 0.25 120.0
2 express 0.05 250.0 standard 0.2 100.0

输出例子：

370.00

例子说明：

2 个中转段，延误风险阈值为 0.4。  
枚举所有组合：  
(1) express+express：风险 0.1+0.05=0.15，运费 300+250=550  
(2) express+standard：风险 0.1+0.2=0.3，运费 300+100=400  
(3) standard+express：风险 0.25+0.05=0.3，运费 120+250=370  
(4) standard+standard：风险 0.25+0.2=0.45 > 0.4，不可行  
满足约束的方案中，最小运费为方案(3)的 370。  

示例2

输入例子：

3 0.5
1 ground 0.15 80.0
2 air 0.1 200.0 ground 0.3 90.0
2 air 0.05 180.0 ground 0.2 70.0

输出例子：

350.00

例子说明：

3 个中转段，延误风险阈值为 0.5。第一段只有 ground 可选（风险 0.15，运费 80）。  
可行方案：  
(1) ground+ground+air：风险 0.15+0.3+0.05=0.5，运费 80+90+180=350  
(2) ground+air+ground：风险 0.15+0.1+0.2=0.45，运费 80+200+70=350  
(3) ground+air+air：风险 0.15+0.1+0.05=0.3，运费 80+200+180=460  
ground+ground+ground 风险 0.65 超出阈值，不可行。  
最小运费为 350。  

# float dp ans

这种题目的难点在于：**延误风险（Risk）和运费（Cost）都是浮点数**。

常规的“背包问题”通常要求重量是整数，我们可以用数组下标来表示状态。但当“重量”是浮点数时，直接开数组是不行的。

### 解题思路：帕累托前沿（Pareto Frontier）

这道题属于 **“分组背包问题”** 的变体。对于每一个中转段，我们必须从多个选项中选一个。

由于是求最小值且有约束，我们可以维护一个 **“有效状态列表”**。一个状态由 `(总风险, 总运费)` 组成。
如果状态 A 的风险比状态 B 小，且运费也比 B 小，那么状态 B 就是“多余的”（无用状态），可以丢弃。这种只保留“最优可能”状态的集合被称为**帕累托前沿**。

**算法步骤：**
1. 初始化状态列表 `dp = [(0.0, 0.0)]`（风险, 运费）。
2. 遍历每一个中转段：
   - 创建一个新的空列表 `next_candidates`。
   - 遍历 `dp` 中的每一个旧状态 `(prev_r, prev_c)`。
   - 遍历当前中转段的每一个选项 `(opt_r, opt_c)`。
   - 如果 `prev_r + opt_r <= T`，将新状态 `(prev_r + opt_r, prev_c + opt_c)` 加入 `next_candidates`。
3. **关键步骤：去重与剪枝**。
   - 对 `next_candidates` 按风险从小到大排序。
   - 遍历排序后的列表，只保留那些 **“运费比之前所有风险更低的状态更小”** 的状态。
   - 更新 `dp = 筛选后的列表`。
4. 最终 `dp` 列表中运费最小的值即为答案。

---

### Python 实现

Python 的列表处理非常灵活，适合快速实现逻辑。

```python
import sys

def solve():
    # 使用 split() 读取所有输入，自动处理换行和空格
    data = sys.stdin.read().split()
    if not data:
        return
    
    L = int(data[0])
    T = float(data[1])
    
    # dp 存储 (风险, 运费)，并保持按风险升序
    dp = [(0.0, 0.0)]
    
    ptr = 2
    for _ in range(L):
        K = int(data[ptr])
        ptr += 1
        
        options = []
        for _ in range(K):
            # 格式：方式名称(跳过) 风险 运费
            r = float(data[ptr + 1])
            c = float(data[ptr + 2])
            options.append((r, c))
            ptr += 3
        
        # 1. 生成所有可能的组合
        next_candidates = []
        for prev_r, prev_c in dp:
            for opt_r, opt_c in options:
                new_r = prev_r + opt_r
                if new_r <= T + 1e-9: # 浮点数比较加上 epsilon
                    next_candidates.append((new_r, prev_c + opt_c))
        
        if not next_candidates:
            continue
            
        # 2. 排序并剪枝 (Pareto Pruning)
        next_candidates.sort() # 先按风险排，风险相同按运费排
        
        new_dp = []
        min_cost = float('inf')
        for r, c in next_candidates:
            # 如果当前状态的运费比之前风险更低的状态还要低，它就是有效的
            if c < min_cost:
                new_dp.append((r, c))
                min_cost = c
        dp = new_dp

    # 在所有满足风险约束的状态中找到运费最低的
    if not dp:
        print("0.00")
    else:
        ans = min(c for r, c in dp)
        print("{:.2f}".format(ans))

if __name__ == "__main__":
    solve()
```

---

### C++ 实现

C++ 中使用 `std::vector` 结合 `std::sort` 效率非常高。

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <iomanip>

using namespace std;

struct State {
    double risk;
    double cost;
    // 用于排序：风险从小到大，风险相同时运费从小到大
    bool operator<(const State& other) const {
        if (abs(risk - other.risk) > 1e-9) return risk < other.risk;
        return cost < other.cost;
    }
};

int main() {
    int L;
    double T;
    if (!(cin >> L >> T)) return 0;

    vector<State> dp;
    dp.push_back({0.0, 0.0});

    for (int i = 0; i < L; ++i) {
        int K;
        cin >> K;
        vector<State> options;
        for (int j = 0; j < K; ++j) {
            string name;
            double r, c;
            cin >> name >> r >> c;
            options.push_back({r, c});
        }

        vector<State> next_candidates;
        for (auto& prev : dp) {
            for (auto& opt : options) {
                double nr = prev.risk + opt.risk;
                if (nr <= T + 1e-9) {
                    next_candidates.push_back({nr, prev.cost + opt.cost});
                }
            }
        }

        if (next_candidates.empty()) continue;

        // 剪枝
        sort(next_candidates.begin(), next_candidates.end());
        vector<State> next_dp;
        double min_cost_so_far = 1e18;
        for (auto& s : next_candidates) {
            if (s.cost < min_cost_so_far - 1e-9) {
                next_dp.push_back(s);
                min_cost_so_far = s.cost;
            }
        }
        dp = next_dp;
    }

    double min_total_cost = 1e18;
    for (auto& s : dp) min_total_cost = min(min_total_cost, s.cost);

    cout << fixed << setprecision(2) << min_total_cost << endl;
    return 0;
}
```

---

### Java 实现

Java 的逻辑与 C++ 类似，注意使用 `printf` 格式化输出。

```java
import java.util.*;

public class Main {
    static class State implements Comparable<State> {
        double r, c;
        State(double r, double c) { this.r = r; this.c = c; }
        public int compareTo(State o) {
            if (Math.abs(this.r - o.r) > 1e-9) return Double.compare(this.r, o.r);
            return Double.compare(this.c, o.c);
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        
        int L = sc.nextInt();
        double T = sc.nextDouble();
        
        List<State> dp = new ArrayList<>();
        dp.add(new State(0.0, 0.0));
        
        for (int i = 0; i < L; i++) {
            int K = sc.nextInt();
            List<State> options = new ArrayList<>();
            for (int j = 0; j < K; j++) {
                sc.next(); // name
                options.add(new State(sc.nextDouble(), sc.nextDouble()));
            }
            
            List<State> nextCandidates = new ArrayList<>();
            for (State prev : dp) {
                for (State opt : options) {
                    double nr = prev.r + opt.r;
                    if (nr <= T + 1e-9) {
                        nextCandidates.add(new State(nr, prev.c + opt.c));
                    }
                }
            }
            
            if (nextCandidates.isEmpty()) continue;
            
            Collections.sort(nextCandidates);
            List<State> nextDp = new ArrayList<>();
            double minCostSoFar = Double.MAX_VALUE;
            for (State s : nextCandidates) {
                if (s.c < minCostSoFar - 1e-9) {
                    nextDp.add(s);
                    minCostSoFar = s.c;
                }
            }
            dp = nextDp;
        }
        
        double ans = Double.MAX_VALUE;
        for (State s : dp) ans = Math.min(ans, s.c);
        System.out.printf("%.2f\n", ans);
    }
}
```

### 为什么这个算法能过？

1.  **分组背包性质**：每一层迭代代表处理一个中转段，保证了“每个中转段只选一个”。
2.  **浮点数处理**：不使用数组下标，而是使用 `list` 或 `vector` 存储具体坐标，完美解决了浮点数作为“重量”的问题。
3.  **剪枝效率**：由于舍弃了“风险更高且运费更高”的状态，状态列表 `dp` 的长度在每一层都不会爆炸式增长。在实际业务数据中，这个列表通常很短。

---

# float matrix dp?

你能教教我如何在线上机考做这题吗？
使用python, java和cpp写。
其实没咋看懂题目。
不会写了，救命。
非常感谢。

21.

最大能量和

在一幅高为 H、宽为 W 的灰度图中，每个像素都有一个实数信号值。给定一个 K×K 的策略矩阵（K 为奇数），我们先依据该矩阵为整幅图计算“能量图” E；随后，从图像的第 1 列任意行作为起点，每一列向右选择一个格子，且列与列之间的移动仅允许三种：右、右上或右下，直到走到第 W 列。请你选择一条合规路径，使路径上对应能量之和最大，并输出该最大值。

-   能量图计算规则（零填充相关）：记 r = K//2  
    E\[i\]\[j\] = Σu=0..K-1 Σv=0..K-1 P\[u\]\[v\] · I\[i+u−r\]\[j+v−r\]  
    若 i+u−r 或 j+v−r 越界，则视为该项贡献为 0。
    
-   路径规则：起点为第 1 列任意行；从 (i, j) 到下一列可走到 (i, j+1)、(i−1, j+1) 或 (i+1, j+1)，越界无效。
    
-   输出：最大能量和，保留 1 位小数。
    

时间限制：C/C++ 1秒，其他语言2秒

空间限制：C/C++ 256M，其他语言512M

输入描述：

-   第一行：H W K
-   接下来 H 行：每行 W 个浮点数，表示图像 I
-   接下来 K 行：每行 K 个浮点数，表示策略矩阵 P

输出描述：

一行一个浮点数：最大能量和（四舍五入保留 1 位小数）

补充说明：

本题由牛友@Charles 整理上传

示例1

输入例子：

2 2 1
1 2
3 4
2

输出例子：

14.0

例子说明：

K=1 且 P=\[2\]，能量图即 E=2·I=\[\[2,4\],\[6,8\]\]。从第 1 列到第 2 列的最优路径为 (2,1)→(2,2)，能量和 6+8=14.0。


# ans float matrix dp?

这道题可以拆解为两个标准算法步骤：
1.  **二维卷积（2D Convolution）**：计算能量图 $E$。
2.  **动态规划（DP）**：在能量图上寻找从第一列到最后一列的最大路径和（类似“数字金字塔”或“最长路径”问题）。

### 1. 题目逻辑详解

*   **能量图 $E$ 的计算**：
    对于图像中的每一个像素 $(i, j)$，我们要把以它为中心的 $K \times K$ 区域与策略矩阵 $P$ 对应项相乘并求和。
    注意：$K$ 是奇数，半径 $r = K // 2$。对于 $P[u][v]$，它对应的图像像素坐标是 $(i + u - r, j + v - r)$。如果这个坐标超出了图像边界，该项记为 0。

*   **路径 DP**：
    从左往右走，每一步可以向右、右上、右下移动。
    定义 `dp[i][j]` 为到达第 $j$ 列第 $i$ 行格子的最大能量和。
    转移方程：
    `dp[i][j] = E[i][j] + max(dp[i-1][j-1], dp[i][j-1], dp[i+1][j-1])`
    （注意处理边界：第一行没有右上，最后一行没有右下）。

---

### 2. Python 实现

Python 在处理大规模嵌套循环时较慢，但在机考中通常会给 Python 更宽的时间限制。我们可以通过简单的逻辑实现。

```python
import sys

def solve():
    # 使用 fast IO
    input_data = sys.stdin.read().split()
    if not input_data: return
    
    H = int(input_data[0])
    W = int(input_data[1])
    K = int(input_data[2])
    
    ptr = 3
    I = []
    for i in range(H):
        I.append([float(x) for x in input_data[ptr : ptr + W]])
        ptr += W
        
    P = []
    for i in range(K):
        P.append([float(x) for x in input_data[ptr : ptr + K]])
        ptr += K
        
    r = K // 2
    # 1. 计算能量图 E
    E = [[0.0] * W for _ in range(H)]
    for i in range(H):
        for j in range(W):
            energy = 0.0
            for u in range(K):
                for v in range(K):
                    ni = i + u - r
                    nj = j + v - r
                    # 零填充逻辑：越界不累加（即视为0）
                    if 0 <= ni < H and 0 <= nj < W:
                        energy += P[u][v] * I[ni][nj]
            E[i][j] = energy
            
    # 2. 路径 DP
    # dp[i][j] 表示到达 (i, j) 的最大能量和
    dp = [[-float('inf')] * W for _ in range(H)]
    
    # 第一列初始化
    for i in range(H):
        dp[i][0] = E[i][0]
        
    # 从左往右逐列更新
    for j in range(1, W): # 0 is sure
        for i in range(H):
            # 来源有三个：左方，左上方，左下方
            prev_max = dp[i][j-1] # 右
            if i > 0:
                prev_max = max(prev_max, dp[i-1][j-1]) # 右下
            if i < H - 1:
                prev_max = max(prev_max, dp[i+1][j-1]) # 右上
            
            dp[i][j] = E[i][j] + prev_max
            
    # 结果为最后一列的最大值
    ans = max(dp[i][W-1] for i in range(H))
    print(f"{ans:.1f}")

if __name__ == "__main__":
    solve()
```

---

### 3. C++ 实现

C++ 运行效率极高，处理这种多重循环非常轻松。

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <iomanip>

using namespace std;

int main() {
    int H, W, K;
    if (!(cin >> H >> W >> K)) return 0;

    vector<vector<double>> I(H, vector<double>(W));
    for (int i = 0; i < H; ++i)
        for (int j = 0; j < W; ++j) cin >> I[i][j];

    vector<vector<double>> P(K, vector<double>(K));
    for (int i = 0; i < K; ++i)
        for (int j = 0; j < K; ++j) cin >> P[i][j];

    int r = K / 2;
    // 1. 计算能量图 E
    vector<vector<double>> E(H, vector<double>(W, 0.0));
    for (int i = 0; i < H; ++i) {
        for (int j = 0; j < W; ++j) {
            double energy = 0.0;
            for (int u = 0; u < K; ++u) {
                for (int v = 0; v < K; ++v) {
                    int ni = i + u - r;
                    int nj = j + v - r;
                    if (ni >= 0 && ni < H && nj >= 0 && nj < W) {
                        energy += P[u][v] * I[ni][nj];
                    }
                }
            }
            E[i][j] = energy;
        }
    }

    // 2. 路径 DP
    vector<vector<double>> dp(H, vector<double>(W, -1e18));
    for (int i = 0; i < H; ++i) dp[i][0] = E[i][0];

    for (int j = 1; j < W; ++j) {
        for (int i = 0; i < H; ++i) {
            double best_prev = dp[i][j-1];
            if (i > 0) best_prev = max(best_prev, dp[i-1][j-1]);
            if (i < H - 1) best_prev = max(best_prev, dp[i+1][j-1]);
            dp[i][j] = E[i][j] + best_prev;
        }
    }

    double max_energy = -1e18;
    for (int i = 0; i < H; ++i) max_energy = max(max_energy, dp[i][W-1]);

    cout << fixed << setprecision(1) << max_energy << endl;
    return 0;
}
```

---

### 4. Java 实现

Java 实现时注意使用 `Scanner` 或 `StringTokenizer` 处理输入，最后使用 `printf` 格式化。

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        
        int H = sc.nextInt();
        int W = sc.nextInt();
        int K = sc.nextInt();
        
        double[][] I = new double[H][W];
        for (int i = 0; i < H; i++)
            for (int j = 0; j < W; j++) I[i][j] = sc.nextDouble();
            
        double[][] P = new double[K][K];
        for (int i = 0; i < K; i++)
            for (int j = 0; j < K; j++) P[i][j] = sc.nextDouble();
            
        int r = K / 2;
        double[][] E = new double[H][W];
        
        // 卷积计算能量图
        for (int i = 0; i < H; i++) {
            for (int j = 0; j < W; j++) {
                double energy = 0;
                for (int u = 0; u < K; u++) {
                    for (int v = 0; v < K; v++) {
                        int ni = i + u - r;
                        int nj = j + v - r;
                        if (ni >= 0 && ni < H && nj >= 0 && nj < W) {
                            energy += P[u][v] * I[ni][nj];
                        }
                    }
                }
                E[i][j] = energy;
            }
        }
        
        // 路径 DP
        double[][] dp = new double[H][W];
        for (int i = 0; i < H; i++) dp[i][0] = E[i][0];
        
        for (int j = 1; j < W; j++) {
            for (int i = 0; i < H; i++) {
                double prevMax = dp[i][j-1];
                if (i > 0) prevMax = Math.max(prevMax, dp[i-1][j-1]);
                if (i < H - 1) prevMax = Math.max(prevMax, dp[i+1][j-1]);
                dp[i][j] = E[i][j] + prevMax;
            }
        }
        
        double result = -Double.MAX_VALUE;
        for (int i = 0; i < H; i++) result = Math.max(result, dp[i][W-1]);
        
        System.out.printf("%.1f\n", result);
    }
}
```

### 关键点拨：
1.  **卷积边界**：题目明确提到越界贡献为 0，所以不需要像处理图像那样真的去做 Padding，直接在循环里用 `if` 判断索引是否合法即可。
2.  **DP 初始值**：因为能量值可能是负数，DP 表初始化应该用一个极小的负数（如 `-1e18`），不能用 0。
3.  **计算顺序**：DP 必须先外层循环“列 $j$”，内层循环“行 $i$”，因为这一列的值依赖于前一列。

---