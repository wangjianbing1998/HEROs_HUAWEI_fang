# coding=gbk
import time


def run_time(func):
    def _warp(*args, **kwargs):
        start = time.time()
        remove_set = func(*args, **kwargs)
        end = time.time()
        print(f'{func.__name__} run at {end - start} s')
        return remove_set

    return _warp


def compare_(a, b):
    return a < b if len(a) == len(b) else len(a) < len(b)


class CompareAble:
    def __init__(self, priority, value):
        self.priority = priority
        self.value = value

    def __lt__(self, other):
        def compare__(A, B):
            if len(A) == 0:
                return True

            return compare__(A[1:], B[1:]) if A[0] == B[0] else compare_(A[0], B[0])

        return compare__(self.value, other.value) if self.priority == other.priority else \
            self.priority < other.priority


def default_dict_list(d, key, appended_val):
    if key in d:
        d[key].append(appended_val)
    else:
        d[key] = [appended_val]


class Solution():

    def __init__(self, in_file_path, out_file_path):
        self.in_file_path = in_file_path
        self.out_file_path = out_file_path

        self.ans = [[] for i in range(5)]
        self.o_edge_out = {}
        self.o_edge_in = {}
        self.ix = set()

        self.n = self.get_data(self.in_file_path)
        self.SIGN = -100
        self.xi = {}
        self.edge_out = [[] for _ in range(self.n)]
        self.edge_in = [[] for _ in range(self.n)]

        for index, x in enumerate(self.ix):
            self.xi[x] = index

        for x in self.o_edge_out:
            xi = self.xi[x]
            self.edge_out[xi] = [self.xi[y] for y in self.o_edge_out[x]]
            self.edge_out[xi].sort()
        for x in self.o_edge_in:
            xi = self.xi[x]
            self.edge_in[xi] = [self.xi[y] for y in self.o_edge_in[x]]
            self.edge_in[xi].sort()

        del self.o_edge_out
        del self.o_edge_in
        del self.xi

        self.instack = [False for i in range(self.n)]
        self.target_visit = [-1 for i in range(self.n)]
        self.path = []
        self.circle = {}

    def add_circle_path(self, path):
        for p in range(len(path)):
            default_dict_list(self.circle, path[p], path[p + 1:] + path[:p])

    def get_data(self, in_file_path):
        with open(in_file_path, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if len(line) > 0:
                    x, y, money = list(map(int, line.split(',')))
                    default_dict_list(self.o_edge_out, x, y)
                    default_dict_list(self.o_edge_in, y, x)
                    self.ix.add(x)
                    self.ix.add(y)
        self.ix = list(self.ix)
        return len(self.ix)

    def show_ans(self, verbose=False):
        with open(self.out_file_path, 'w+') as f:

            cnt = sum(len(p) for p in self.ans)
            f.write(str(cnt) + '\n')
            if verbose:
                print(cnt)

            for rr in self.ans:
                for r in rr:
                    if verbose:
                        print([self.ix[p] for p in r])

                    for i in range(len(r) - 1):
                        f.write(f'{self.ix[r[i]]},')
                    f.write(f'{self.ix[r[len(r) - 1]]}\n')

    def get_pre_path(self, paths, s):

        def find_path(path, v):
            pre_path = []
            for p in path:
                pre_path.append(p)
                if p == v:
                    return pre_path
            return None

        ans = []
        js = []
        for j in range(len(s) - 1, -1, -1):

            for path in paths:
                pre_path = find_path(path, s[j])
                if pre_path:
                    if len(ans) > 0:
                        if pre_path != ans[-1]:
                            ans.append(pre_path)
                            js.append(j)
                    else:
                        ans.append(pre_path)
                        js.append(j)
            if ans:
                break
        return ans, js

    def resort(self, path):
        min_v = path[0]
        min_i = 0
        for i, p in enumerate(path):
            if p < min_v:
                min_i = i
                min_v = p
        return path[min_i:] + path[:min_i]

    def dfs(self, u, target, cur_path):

        for v in self.edge_out[u]:

            if v < target:
                continue

            if self.target_visit[v] == self.SIGN and not self.instack[v]:
                cur_path.append(v)
                length = len(cur_path)
                if length >= 3:
                    copy_path = cur_path.copy()
                    self.ans[length - 3].append(copy_path)
                    self.add_circle_path(copy_path)
                cur_path.pop()

            if len(cur_path) == 6 or v == target or self.instack[v] or (
                    self.target_visit[v] != target and self.target_visit[v] != self.SIGN):
                continue

            if v in self.circle:
                find_path = False
                for path in self.circle[v]:
                    if path == cur_path or path[-1] == u:
                        continue
                    print(self.ix[u], self.ix[v], [self.ix[p] for p in path], [self.ix[p] for p in cur_path])
                    pre_paths, js = self.get_pre_path(self.circle[v], cur_path)
                    if pre_paths:  # find the pre path
                        find_path = True
                        for pre_path, j in zip(pre_paths, js):
                            path = [v] + pre_path + cur_path[j + 1:]
                            self.add_circle_path(path)
                            path = self.resort(path)
                            length = len(path)
                            if 3 <= length <= 7:
                                print([self.ix[p] for p in path])
                                self.ans[length - 3].append(path)
                            break
                        break
                if find_path:
                    continue
            self.instack[v] = True
            cur_path.append(v)
            self.dfs(v, target, cur_path)
            self.instack[v] = False
            cur_path.pop()

    def dfs_n_step(self, edges, u, target, length, n):
        for v in edges[u]:
            if v < target or self.instack[v]:
                continue
            self.target_visit[v] = target
            if length == n:  # find the n step target
                continue
            self.instack[v] = True
            self.dfs_n_step(edges, v, target, length + 1, n)
            self.instack[v] = False

    def solve(self, start):
        self.path.append(start)
        self.dfs_n_step(self.edge_out, start, start, 1, 3)
        self.dfs_n_step(self.edge_in, start, start, 1, 3)
        self.set_edge_state(start, self.SIGN)
        self.dfs(start, start, self.path)
        self.set_edge_state(start, start)
        self.path.pop()

    def set_edge_state(self, u, value):
        for j in self.edge_in[u]:
            self.target_visit[j] = value


@run_time
def main(_):
    # global solution

    # solution = Solution(in_file_path='/data/test_data.txt', out_file_path='/projects/student/result.txt')
    # solution = Solution(in_file_path='T.txt', out_file_path='resT.txt')
    # solution = Solution(in_file_path='test_data2.txt', out_file_path='res2.txt')
    solution = Solution(in_file_path='in4_12.txt', out_file_path='out12.txt')
    # solution = Solution(in_file_path='test_data.txt', out_file_path='res.txt')
    for start in range(solution.n):
        solution.solve(start)
    solution.show_ans(verbose=False)


if __name__ == "__main__":
    main(1)
