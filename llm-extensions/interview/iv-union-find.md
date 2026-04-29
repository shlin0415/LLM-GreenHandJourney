# union find 1 20251029

你能教教我如何在线上机考做这题吗？
使用python, java和cpp写, 非常感谢。

21.

实体匹配结果归并与排序

在数据治理平台中，不同的实体匹配引擎会各自产出“被认为指向同一真实实体”的编号集合。每一行输入代表某个引擎得到的一组编号（集合），行内的编号可能有重复。若两组集合存在至少一个公共编号，则它们应当被视作同一簇，需合并为一个更大的集合。请你将所有集合按上述规则进行传递式合并与去重，并按指定顺序输出。  
  
编号仅由数字字符构成（如“1”“23”“0005”），每行不超过100个编号，总不同编号数不超过100000，匹配系统行数 N 在 1 到 10000 之间。  
  
排序规则  
\- 行内排序：将一个合并后的集合中的编号按字典序（字符串比较）升序排列后输出为一行，编号之间用单个空格分隔。  
\- 行间排序：将所有行作为“编号有序序列”，按字典序（逐个编号从左到右比较，若一行是另一行的前缀，则较短者更小）升序排列后输出。  

时间限制：C/C++ 1秒，其他语言2秒

空间限制：C/C++ 256M，其他语言512M

输入描述：

第1行：整数 N，表示有 N 行匹配结果。  
接下来的 N 行：每行是若干个用空格分隔的数字字符串，表示该系统判定为“同一实体”的编号集合。行内可能出现重复编号。  

输出描述：

输出 M 行（M ≤ N）。每一行是一组经传递式合并与去重后的编号序列，满足“行内字典序、行间字典序”的排序要求。

补充说明：

本题由牛友@Charles 整理上传

示例1

输入例子：

6
10 20
30 40
500
7 7 8 9
1
9 11

输出例子：

1
10 20
11 7 8 9
30 40
500

例子说明：

解释如下（按“字符串字典序”进行排序）：

-   合并关系
    
    -   第4行“7 7 8 9”和第6行“9 11”因共同包含“9”，属于同一簇，合并为集合{7,8,9,11}，并去重。
-   行内排序（字符串字典序）
    
    -   合并后的集合按字符串排序为“11 7 8 9”（因为“11”作为字符串小于“7”“8”“9”）。
    -   其余行分别为：“10 20”“30 40”“500”“1”。
-   行间排序（按整行序列的字典序进行比较）
    
    -   比较每行的第一个编号，得到整体顺序：  
        1  
        10 20  
        11 7 8 9  
        30 40  
        500

---

# ans union find 1

这道题是并查集（Union-Find）的经典应用题。它的核心逻辑是：**将具有公共元素的集合合并**。

### 核心解题思路

1.  **数据建模**：每一个不同的编号字符串看作图中的一个节点。如果一行中出现了多个编号，说明这些编号属于同一个“簇”（即它们在图中是连通的）。
2.  **并查集（Union-Find）**：
    *   使用并查集来维护编号之间的连通性。
    *   由于编号是字符串，为了方便处理，我们可以使用一个哈希表（Map/Dictionary）将**字符串编号映射为整数索引**。
3.  **合并逻辑**：
    *   遍历每一行。将该行中的第一个编号与其他所有编号进行 `union` 操作。
    *   注意：同一行内可能存在重复编号，并查集天然支持去重合并。
4.  **结果归并**：
    *   遍历所有出现的编号，通过并查集的 `find` 操作找到它们的根节点。
    *   将具有相同根节点的编号放到同一个列表中。
5.  **排序规则（关键点）**：
    *   **行内排序**：将每个合并后的列表按字符串字典序升序排列。
    *   **行间排序**：将所有处理好的行列表进行排序。排序规则是比较列表的每一个元素（类似于字符串比较，但元素是编号字符串）。

---

### Python 实现

Python 处理字符串和嵌套列表排序非常简洁，`list.sort()` 默认就支持“序列字典序”。

```python
import sys

# 并查集查找（带路径压缩）
def find(parent, i):
    if parent[i] == i:
        return i
    parent[i] = find(parent, parent[i])
    return parent[i]

# 并查集合并
def union(parent, i, j):
    root_i = find(parent, i)
    root_j = find(parent, j)
    if root_i != root_j:
        parent[root_i] = root_j

def solve():
    try:
        line1 = sys.stdin.readline()
        if not line1: return
        n = int(line1.strip())
    except EOFError:
        return

    id_to_idx = {}
    idx_to_id = []
    
    # 存储原始输入的索引表示
    rows_indices = []
    
    for _ in range(n):
        line = sys.stdin.readline().split()
        if not line: continue
        
        current_row_indices = []
        for s in line:
            if s not in id_to_idx:
                id_to_idx[s] = len(idx_to_id)
                idx_to_id.append(s)
            current_row_indices.append(id_to_idx[s])
        rows_indices.append(current_row_indices)

    # 初始化并查集
    num_ids = len(idx_to_id)
    parent = list(range(num_ids))

    # 执行合并
    for row in rows_indices:
        for i in range(1, len(row)):
            union(parent, row[0], row[i])

    # 归并结果
    groups = {}
    for i in range(num_ids):
        root = find(parent, i)
        if root not in groups:
            groups[root] = []
        groups[root].append(idx_to_id[i])

    # 排序
    final_rows = []
    for root in groups:
        # 行内排序：字符串字典序
        groups[root].sort()
        final_rows.append(groups[root])

    # 行间排序：按整行序列的字典序
    final_rows.sort()

    # 输出
    for row in final_rows:
        print(" ".join(row))

if __name__ == "__main__":
    solve()
```

---

### C++ 实现

C++ 中利用 `unordered_map` 做映射，并利用 `vector` 的默认比较运算符完成行间排序。

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <unordered_map>
#include <algorithm>
#include <set>

using namespace std;

struct DSU {
    vector<int> parent;
    DSU(int n) {
        parent.resize(n);
        for (int i = 0; i < n; ++i) parent[i] = i;
    }
    int find(int i) {
        if (parent[i] == i) return i;
        return parent[i] = find(parent[i]);
    }
    void unite(int i, int j) {
        int root_i = find(i);
        int root_j = find(j);
        if (root_i != root_j) parent[root_i] = root_j;
    }
};

int main() {
    int N;
    if (!(cin >> N)) return 0;
    string line;
    getline(cin, line); // 消耗掉N后的换行符

    unordered_map<string, int> id_to_idx;
    vector<string> idx_to_id;
    vector<vector<int>> input_rows;

    for (int i = 0; i < N; ++i) {
        getline(cin, line);
        stringstream ss(line);
        string id;
        vector<int> current_row;
        while (ss >> id) {
            if (id_to_idx.find(id) == id_to_idx.end()) {
                id_to_idx[id] = idx_to_id.size();
                idx_to_id.push_back(id);
            }
            current_row.push_back(id_to_idx[id]);
        }
        if (!current_row.empty()) input_rows.push_back(current_row);
    }

    DSU dsu(idx_to_id.size());
    for (auto& row : input_rows) {
        for (size_t i = 1; i < row.size(); ++i) {
            dsu.unite(row[0], row[i]);
        }
    }

    unordered_map<int, vector<string>> groups;
    for (int i = 0; i < idx_to_id.size(); ++i) {
        groups[dsu.find(i)].push_back(idx_to_id[i]);
    }

    vector<vector<string>> final_rows;
    for (auto& pair : groups) {
        sort(pair.second.begin(), pair.second.end());
        final_rows.push_back(pair.second);
    }

    sort(final_rows.begin(), final_rows.end());

    for (auto& row : final_rows) {
        for (int i = 0; i < row.size(); ++i) {
            cout << row[i] << (i == row.size() - 1 ? "" : " ");
        }
        cout << endl;
    }

    return 0;
}
```

---

### Java 实现

Java 的实现需要注意 `StringTokenizer` 提高读取速度，并实现一个自定义的 `Comparator` 来处理 `List<String>` 的行间排序。

```java
import java.util.*;
import java.io.*;

public class Main {
    static class DSU {
        int[] parent;
        DSU(int n) {
            parent = new int[n];
            for (int i = 0; i < n; i++) parent[i] = i;
        }
        int find(int i) {
            if (parent[i] == i) return i;
            return parent[i] = find(parent[i]);
        }
        void union(int i, int j) {
            int r1 = find(i), r2 = find(j);
            if (r1 != r2) parent[r1] = r2;
        }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String firstLine = br.readLine();
        if (firstLine == null) return;
        int N = Integer.parseInt(firstLine.trim());

        Map<String, Integer> idToIdx = new HashMap<>();
        List<String> idxToId = new ArrayList<>();
        List<int[]> inputRows = new ArrayList<>();

        for (int i = 0; i < N; i++) {
            String line = br.readLine();
            if (line == null || line.trim().isEmpty()) continue;
            String[] tokens = line.trim().split("\\s+");
            int[] rowIdx = new int[tokens.length];
            for (int j = 0; j < tokens.length; j++) {
                if (!idToIdx.containsKey(tokens[j])) {
                    idToIdx.put(tokens[j], idxToId.size());
                    idxToId.add(tokens[j]);
                }
                rowIdx[j] = idToIdx.get(tokens[j]);
            }
            inputRows.add(rowIdx);
        }

        DSU dsu = new DSU(idxToId.size());
        for (int[] row : inputRows) {
            for (int j = 1; j < row.length; j++) {
                dsu.union(row[0], row[j]);
            }
        }

        Map<Integer, List<String>> groups = new HashMap<>();
        for (int i = 0; i < idxToId.size(); i++) {
            int root = dsu.find(i);
            groups.computeIfAbsent(root, k -> new ArrayList<>()).add(idxToId.get(i));
        }

        List<List<String>> finalRows = new ArrayList<>();
        for (List<String> group : groups.values()) {
            Collections.sort(group);
            finalRows.add(group);
        }

        // 行间排序
        finalRows.sort((a, b) -> {
            int len = Math.min(a.size(), b.size());
            for (int i = 0; i < len; i++) {
                int cmp = a.get(i).compareTo(b.get(i));
                if (cmp != 0) return cmp;
            }
            return Integer.compare(a.size(), b.size());
        });

        StringBuilder sb = new StringBuilder();
        for (List<String> row : finalRows) {
            for (int i = 0; i < row.size(); i++) {
                sb.append(row.get(i)).append(i == row.size() - 1 ? "" : " ");
            }
            sb.append("\n");
        }
        System.out.print(sb);
    }
}
```

---

### 考试技巧总结

1.  **并查集的模版化**：并查集由 `find` 和 `union` 组成，考试时直接默写即可。
2.  **字符串字典序**：这道题最容易掉坑的是编号按字符串排序。比如 `"11"` 字典序是比 `"7"` 小的。在 Java/C++/Python 中，直接对字符串使用默认排序函数即符合此规则。
3.  **行间排序的逻辑**：
    *   Python：`list1 < list2` 自动比较。
    *   C++：`vector1 < vector2` 自动比较。
    *   Java：需要显式写出 `a.get(i).compareTo(b.get(i))` 的循环比较。
4.  **数据范围**：
    *   $N=10000$，$M=100000$，复杂度 $O(N \cdot \text{row\_len} \cdot \alpha(M) + \text{排序复杂度})$。
    *   排序是最大的开销，但由于总编号数有限，在时限内能轻松通过。

---

# class union find

will using class to write be better?
thank you.
```py
# 模板来源 https://leetcode.cn/circle/discuss/mOr1u6/
class UnionFind:
    def __init__(self, n: int):
        # 一开始有 n 个集合 {0}, {1}, ..., {n-1}
        # 集合 i 的代表元是自己，大小为 1
        self._fa = list(range(n))  # 代表元
        self._size = [1] * n  # 集合大小
        self.cc = n  # 连通块个数

    # 返回 x 所在集合的代表元
    # 同时做路径压缩，也就是把 x 所在集合中的所有元素的 fa 都改成代表元
    def find(self, x: int) -> int:
        fa = self._fa
        # 如果 fa[x] == x，则表示 x 是代表元
        if fa[x] != x:
            fa[x] = self.find(fa[x])  # fa 改成代表元
        return fa[x]

    # 判断 x 和 y 是否在同一个集合
    def is_same(self, x: int, y: int) -> bool:
        # 如果 x 的代表元和 y 的代表元相同，那么 x 和 y 就在同一个集合
        # 这就是代表元的作用：用来快速判断两个元素是否在同一个集合
        return self.find(x) == self.find(y)

    # 把 from 所在集合合并到 to 所在集合中
    # 返回是否合并成功
    def merge(self, from_: int, to: int) -> bool:
        x, y = self.find(from_), self.find(to)
        if x == y:  # from 和 to 在同一个集合，不做合并
            return False
        self._fa[x] = y  # 合并集合。修改后就可以认为 from 和 to 在同一个集合了
        self._size[y] += self._size[x]  # 更新集合大小（注意集合大小保存在代表元上）
        # 无需更新 _size[x]，因为我们不用 _size[x] 而是用 _size[find(x)] 获取集合大小，但 find(x) == y，我们不会再访问 _size[x]
        self.cc -= 1  # 成功合并，连通块个数减一
        return True

    # 返回 x 所在集合的大小
    def get_size(self, x: int) -> int:
        return self._size[self.find(x)]  # 集合大小保存在代表元上
```

在机考（如华为、字节、腾讯、美团等）中，使用 **Class（类）** 来封装并查集是非常推荐的做法。

### 为什么使用 Class 更好？

1.  **逻辑清晰**：并查集的初始化、查找、合并逻辑是独立的。封装成类可以让你的 `main` 函数或核心逻辑部分非常干净，只负责处理输入输出和业务合并。
2.  **避免 Bug**：使用成熟的模板（如你提供的代码）可以避免在手写 `find` 函数时漏掉“路径压缩”，或者在 `merge` 时忘记更新连通分量计数。
3.  **可复用性**：很多图论题目（冗余连接、岛屿数量、省份数量等）都可以直接把这个类 Copy 过去。

### 针对机考的优化建议

虽然你提供的模板很标准，但在** Python **中做机考，建议增加两个细节：

1.  **增加递归深度限制**：Python 默认递归深度是 1000。如果并查集退化严重或节点数过万，可能会报 `RecursionError`。
2.  **迭代式 Find**：如果不想改递归深度，可以把 `find` 写成迭代版。
3.  **按秩合并（可选）**：你的模板是简单的 `self._fa[x] = y`，这在绝大多数情况下够用。如果追求极致性能，可以根据 `_size` 来判断谁合并到谁。

---

### 使用你提供的 Class 重新实现《实体匹配结果归并》

以下是应用了 Class 封装的 Python 代码：

#### Python 版（使用类封装）

```python
import sys

# 设置递归深度，防止 find 深度过大
sys.setrecursionlimit(200000)

class UnionFind:
    def __init__(self, n: int):
        self._fa = list(range(n))
        self.cc = n

    def find(self, x: int) -> int:
        # 迭代版 find，完全避免递归深度限制
        root = x
        while self._fa[root] != root:
            root = self._fa[root]
        # 路径压缩（可选，为了提速）
        while self._fa[x] != root:
            new_fa = self._fa[x]
            self._fa[x] = root
            x = new_fa
        return root

    def merge(self, from_: int, to: int) -> bool:
        x, y = self.find(from_), self.find(to)
        if x == y: return False
        self._fa[x] = y
        self.cc -= 1
        return True

def solve():
    input_data = sys.stdin.read().splitlines()
    if not input_data: return
    n = int(input_data[0])
    
    id_to_idx = {}
    idx_to_id = []
    rows_as_indices = []
    
    # 1. 建立 String 到 Int 的映射
    for i in range(1, n + 1):
        line = input_data[i].split()
        if not line: continue
        current_row = []
        for s in line:
            if s not in id_to_idx:
                id_to_idx[s] = len(idx_to_id)
                idx_to_id.append(s)
            current_row.append(id_to_idx[s])
        rows_as_indices.append(current_row)
    
    # 2. 使用 UnionFind 类
    uf = UnionFind(len(idx_to_id))
    for row in rows_as_indices:
        # 将行内所有编号与第一个编号合并
        for j in range(1, len(row)):
            uf.merge(row[0], row[j])
            
    # 3. 归并结果
    groups = {}
    for i in range(len(idx_to_id)):
        root = uf.find(i)
        if root not in groups:
            groups[root] = []
        groups[root].append(idx_to_id[i])
        
    # 4. 排序逻辑
    res = []
    for g in groups.values():
        g.sort() # 行内字典序
        res.append(g)
    
    res.sort() # 行间字典序
    
    for row in res:
        print(" ".join(row))

solve()
```

---

### C++ 版（推荐使用 struct 封装）

在 C++ 中，`struct` 默认权限是 public，非常适合用来写并查集模板。

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <unordered_map>
#include <algorithm>

using namespace std;

// 推荐在机考中使用的 C++ 模板
struct UnionFind {
    vector<int> parent;
    int count; // 连通块数量

    UnionFind(int n) : count(n) {
        parent.resize(n);
        for (int i = 0; i < n; ++i) parent[i] = i;
    }

    int find(int i) {
        if (parent[i] == i) return i;
        return parent[i] = find(parent[i]); // 路径压缩
    }

    bool unite(int i, int j) {
        int root_i = find(i);
        int root_j = find(j);
        if (root_i != root_j) {
            parent[root_i] = root_j;
            count--;
            return true;
        }
        return false;
    }
};

// ... 后续逻辑同前 ...
```

---

### 总结：机考中的 Class 使用建议

1.  **直接粘模板**：平时整理好一份自己最顺手的并查集、堆、树状数组等模板，机考时遇到这类题，**第一时间先把 Class 框架打出来**。
2.  **映射处理**：并查集通常处理整数 `0 ~ n-1`。如果题目给的是字符串（如本题），先用一个 `Map<String, Integer>` 统一转换成整数，再喂给 `UnionFind`。
3.  **迭代 vs 递归**：
    *   **Python**：推荐迭代式 `find`（用 `while` 循环），最稳。
    *   **C++/Java**：直接写递归 `find` 即可（带路径压缩），C++/Java 的默认栈深度通常足够处理 $10^5$ 级别的节点。

使用 Class 这种“工业化”的写法，能显著提升你代码的**健壮性**，在机考紧张的环境下减少低级逻辑错误。

# union find directly use dict

i use dict to pass, but i am not sure if it is always right.
can you help me check?
use chinese to reply, thanks.

```py
import sys

class UnionFind():
    def __init__(self):
        self.roots = {}
        self.sizes = {}
        self.num = 0

    def find(self, x):
        root = x
        while self.roots[root] != root:
            root = self.roots[root]
        while self.roots[x] != x:
            new_x = self.roots[x]
            self.roots[x] = root
            x = new_x
        return root

    def merge(self, a, b):
        root1, root2 = self.find(a), self.find(b)
        if root1 == root2:
            return False
        self.roots[root1] = root2
        self.sizes[root2] += self.sizes[root1]
        del self.sizes[root1]
        self.num -= 1
        return True
        
# inputs = sys.stdin.read().split()
n = int(sys.stdin.readline().strip())
uf = UnionFind()
ele_set = set()
for i in range(n):
    inputs = sys.stdin.readline().strip().split()
    root = inputs[0]
    # size = 0
    for ele in inputs:
        if ele not in uf.roots: 
            uf.roots[ele] = ele
            uf.num += 1
        if ele not in uf.sizes: uf.sizes[ele] = 1
        _ = uf.merge(ele, root)
        # size += 1
        ele_set.add(ele)
    # uf.sizes[root] = size
    # uf.num += 1
# print(ele_set)
# print(f"uf num {uf.num}")
ans = []
# for i in range(uf.num):
# if uf.num > 0:
tmp_dict = {}
for ele in ele_set:
    tmp_root = uf.find(ele)
    if tmp_root not in tmp_dict: tmp_dict[tmp_root] = []
    tmp_dict[tmp_root].append(ele)
# print(tmp_dict)
for tmp_root in tmp_dict:
    tmp_dict[tmp_root].sort()
    tmp_str = ' '.join(tmp_dict[tmp_root])
    tmp_str.strip()
    ans.append(tmp_str)
ans.sort()
for i in ans:
    print(i)



```

---

# ans direct dict

这是一个非常好的问题。在机考中，使用 `dict`（字典）来实现并查集不仅是**正确**的，而且在处理**字符串编号**或**不连续的数字**时，往往比使用固定长度的数组（List）更方便。

以下是对你代码的详细分析和机考建议：

### 1. 使用 `dict` 实现并查集的好处
*   **无需预处理映射**：如果使用数组，你需要先遍历一遍数据，用一个 `dict` 把所有字符串编号映射成 `0` 到 `N-1` 的整数。直接用 `dict` 作为并查集的底层存储，省去了这个步骤，代码更简洁。
*   **动态扩展**：数组必须提前知道有多少个不同的元素（初始化大小），而 `dict` 可以在运行时动态增加新元素。

### 2. 你的代码逻辑检查
你的代码在大逻辑上是正确的，但在细节和**机考严谨性**上有几点需要注意：

#### (1) 关于 `num`（连通块数量）的维护
你在 `merge` 时减小了 `num`，但在 `if ele not in uf.roots` 时增加了 `num`。这个逻辑虽然能跑通，但其实在最后提取结果时，你并**没有用到**这个 `num`。
*   **机考建议**：如果题目不需要输出连通块的总数，可以不维护这个变量。

#### (2) 路径压缩的实现
你的 `find` 函数写了两个 `while` 循环：一个找根，一个做路径压缩。
```py
def find(self, x):
    root = x
    while self.roots[root] != root: # 找根
        root = self.roots[root]
    while self.roots[x] != x: # 路径压缩
        new_x = self.roots[x]
        self.roots[x] = root
        x = new_x
    return root
```
这是**完全正确且高效**的（迭代式路径压缩），可以避免 Python 在处理深度很大的树时触发 `RecursionError`（递归深度限制）。

#### (3) 排序逻辑（非常重要！）
这是你代码中最可能丢分的地方。
*   **你目前的做法**：先 `join` 成字符串，再对 `ans` 这个**字符串列表**进行排序。
*   **潜在风险**：题目要求的是“按编号序列的字典序”排序。
    *   假设有一行是 `['1', '2']` -> 变成 `"1 2"`
    *   另一行是 `['12']` -> 变成 `"12"`
    *   由于空格的 ASCII 码小于数字，`"1 2"` 会排在 `"12"` 前面。
    *   在这一题中，因为编号内部也是按字典序排的，`join` 后排序在大部分情况下是正确的，但**最稳妥、最标准**的做法是**对列表（List of Lists）进行排序**。

### 3. 改进建议（机考高分模板）

这是根据你的思路优化后的代码，更符合机考的鲁棒性要求：

```py
import sys

class UnionFind:
    def __init__(self):
        self.roots = {}
        # sizes 在这题合并时没用到（因为不是按秩合并），可以省略
        # 如果要优化性能，可以加上按秩合并

    def find(self, x):
        # 如果元素不在字典里，初始化它
        if x not in self.roots:
            self.roots[x] = x
            return x
        
        # 迭代版路径压缩
        curr = x
        while self.roots[curr] != curr:
            curr = self.roots[curr]
        root = curr
        
        curr = x
        while self.roots[curr] != root:
            parent = self.roots[curr]
            self.roots[curr] = root
            curr = parent
        return root

    def merge(self, a, b):
        root1, root2 = self.find(a), self.find(b)
        if root1 != root2:
            self.roots[root1] = root2
            return True
        return False

def solve():
    # 使用 sys.stdin.read().splitlines() 读所有行，防止空行干扰
    lines = sys.stdin.read().splitlines()
    if not lines: return
    
    n = int(lines[0].strip())
    uf = UnionFind()
    all_elements = set()
    
    for i in range(1, n + 1):
        elements = lines[i].split()
        if not elements: continue
        
        first = elements[0]
        for ele in elements:
            all_elements.add(ele)
            uf.merge(ele, first)

    # 归并结果
    groups = {}
    for ele in all_elements:
        root = uf.find(ele)
        if root not in groups:
            groups[root] = []
        groups[root].append(ele)

    # 排序处理
    final_rows = []
    for g in groups.values():
        g.sort()  # 行内排序：字符串字典序
        final_rows.append(g)

    # 行间排序：Python 直接支持 List 的字典序排序，非常方便！
    final_rows.sort()

    # 格式化输出
    for row in final_rows:
        print(" ".join(row))

if __name__ == "__main__":
    solve()
```

### 总结：
1.  **`dict` 是安全的吗？** 是的，在 Python 中使用 `dict` 实现并查集是完全可以的，时间复杂度同样是 $O(\alpha(N))$。
2.  **空间问题**：`dict` 比 `list` 多耗费一些内存，但在 256MB/512MB 的限制下，处理 10 万个字符串绰绰有余。
3.  **排序避坑**：**永远优先对 `List[List[str]]` 进行排序**，而不是 `List[str]`。
    *   `[['1', '2'], ['12']].sort()` 结果是 `[['1', '2'], ['12']]`。
    *   `["1 2", "12"].sort()` 虽然在这里结果一样，但在复杂字符下可能会出问题。

你原来的代码已经能拿到大部分甚至全部分数了，主要的改进点在于处理输入时的稳健性，以及排序时的规范性。加油！