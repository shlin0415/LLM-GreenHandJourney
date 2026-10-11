# dp min sum area meituan 2026

题目描述：
给定数组t，定义任意数x在t中的出现次数为cnt(x)。称t被v支配，当且仅当对任意v'有cnt(v) >= cnt(v')；若出现次数相同，则取数值最大的那个v。定义数组t的权值为 v * |t|（其中|t|为t的长度）。

现在给定长度为n的数组a，需要将其划分为若干个非空连续子数组，使得各子数组权值之和最小，输出该最小值。

输入：多组测试数据，T组。每组n，然后n个整数a_i。n总和不超过5000。

输出：每组最小权值和。

示例：
3
5
1 1 2 2 3
3
5 5 5
4
1 2 3 4
输出：
8
15
10

解释：
样例1：划分 [1,1,2],[2],[3] 权值：1*3 + 2*1 + 3*1 = 3+2+3=8。
样例2：任意划分总和均为5*3=15。
样例3：单点划分 1+2+3+4=10。

## ans dpsk

这道题可以用 **区间 DP + 贪心枚举** 解决。因为 `n` 总和不超过 5000，单个 `n` 最大 2000，所以 `O(n²)` 的 DP 完全可行。

### 思路

1. **定义 dp[i]**：表示将前 `i` 个元素划分成若干连续子数组后，权值之和的最小值。
2. **转移**：枚举最后一段子数组的起点 `j`（从 `i` 向前扫描到 `1`），则  
   `dp[i] = min(dp[i], dp[j-1] + cost(j, i))`  
   其中 `cost(j, i)` 是子数组 `a[j..i]` 的权值。
3. **如何快速求 cost(j, i)**：  
   从右向左固定 `i`，向左扩展 `j`，同时用一个字典统计每个元素的出现次数，并维护当前出现次数最多的元素（若次数相同取数值最大的）。这样就能在 `O(1)` 时间内得到当前子数组的支配元素 `v`，权值就是 `v * (i - j + 1)`。

### 复杂度

- 时间：`O(n²)`，`n` 总和 ≤ 5000，最坏约 10⁷ 次操作，Python 可轻松通过。
- 空间：`O(n)`。

### 代码实现

```python
import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    T = int(next(it))
    out = []
    INF = 10**18

    for _ in range(T):
        n = int(next(it))
        a = [0] + [int(next(it)) for _ in range(n)]  # 1-indexed

        dp = [0] * (n + 1)

        for i in range(1, n + 1):
            dp[i] = INF
            cnt = {}                 # 当前子数组各元素出现次数
            max_cnt = -1             # 当前最大出现次数
            dominant = None          # 当前支配元素

            # 从 i 向左扩展 j，子数组为 a[j..i]
            for j in range(i, 0, -1):
                x = a[j]
                cnt[x] = cnt.get(x, 0) + 1
                c = cnt[x]

                # 更新支配元素：出现次数更多，或次数相同但数值更大
                if c > max_cnt or (c == max_cnt and x > dominant):
                    max_cnt = c
                    dominant = x

                cost = dominant * (i - j + 1)
                if dp[j - 1] + cost < dp[i]:
                    dp[i] = dp[j - 1] + cost

        out.append(str(dp[n]))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

### 样例验证

输入：
```
3
5
1 1 2 2 3
3
5 5 5
4
1 2 3 4
```
输出：
```
8
15
10
```
与题目示例一致。

### 关键点说明

- 支配元素的选择规则：先比出现次数，次数相同取数值最大。
- 由于 `a[i]` 可能为负数，比较数值大小时直接用 `x > dominant` 即可（Python 支持负数比较）。
- 代码中 `dominant` 初始为 `None`，但第一次一定会因为 `c > max_cnt`（`max_cnt` 初始为 `-1`）而更新，不会执行到 `x > dominant`，所以安全。
- 多组测试数据用 `sys.stdin.read().split()` 一次性读入，处理更高效。

如果还有疑问，欢迎继续讨论！

```py
import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return

    ptr = 0
    T = int(data[ptr]); ptr += 1
    out = []
    INF = 10**18

    for _ in range(T):
        n = int(data[ptr]); ptr += 1
        a = [0] * (n + 1)  # 1-indexed
        for i in range(1, n + 1):
            a[i] = int(data[ptr]); ptr += 1

        dp = [0] * (n + 1)

        for i in range(1, n + 1):
            dp[i] = INF
            cnt = {}                 # 当前子数组各元素出现次数
            max_cnt = -1             # 当前最大出现次数
            dominant = None          # 当前支配元素

            # 从 i 向左扩展 j，子数组为 a[j..i]
            for j in range(i, 0, -1):
                x = a[j]
                cnt[x] = cnt.get(x, 0) + 1
                c = cnt[x]

                # 更新支配元素：出现次数更多，或次数相同但数值更大
                if c > max_cnt or (c == max_cnt and x > dominant):
                    max_cnt = c
                    dominant = x

                cost = dominant * (i - j + 1)
                if dp[j - 1] + cost < dp[i]:
                    dp[i] = dp[j - 1] + cost

        out.append(str(dp[n]))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

### self write

```py
import sys

INT_MAX = 2 * (10 ** 12) + 1

def cal_min_val(n, arr):
    dp = [INT_MAX] * (n + 1)
    dp[0] = 0
    # tmp_sum = 0
    for j in range(1, n + 1):
        # tmp_sum += arr[j]
        tmp_dict = {}
        lead = -1
        lead_cnt = 0
        for k in range(j - 1, -1, -1):
            tmp = arr[k]
            if tmp not in tmp_dict:
                tmp_dict[tmp] = 1
                tmp_cnt = 1
            else:
                tmp_dict[tmp] += 1
                tmp_cnt = tmp_dict[tmp]
            if tmp_cnt > lead_cnt or (tmp_cnt == lead_cnt and tmp > lead):
                lead = tmp
                lead_cnt = tmp_cnt
            dp[j] = min(dp[j], dp[k] + lead * (j - k))
    return dp[n]


inputs = sys.stdin.read().split()
t = int(inputs[0])
# print(f"t = {t}")
pos = 1
for i in range(t):
    n = int(inputs[pos])
    # print(f"n = {n}")
    pos += 1
    arr = []
    for p in range(n):
        arr.append(int(inputs[pos]))
        pos += 1
    # arr = list(map(int, inputs[pos, pos + n]))
    # print(f"arr = {arr}")
    min_val = cal_min_val(n, arr)
    print(min_val)




```