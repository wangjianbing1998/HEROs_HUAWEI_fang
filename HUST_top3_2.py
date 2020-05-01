# coding=gbk
from collections import defaultdict

import better_exceptions
import numpy as np

better_exceptions.hook()


class Solution:

    def __init__(self, file_path):

        self.s = []
        self.edge_out = defaultdict(list)
        self.edge_in = defaultdict(list)

        self.o_edge_out = defaultdict(list)
        self.o_edge_in = defaultdict(list)

        max_id = -1
        with open(file_path, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if len(line) > 0:
                    x, y, money = line.split(',')
                    self.edge_out[int(x)].append(int(y))
                    self.o_edge_out[int(x)].append(int(y))
                    self.edge_in[int(y)].append(int(x))
                    self.o_edge_in[int(y)].append(int(x))

                    max_id = max(max_id, int(x))

        self.instack = [False for i in range(max_id + 1)]
        self.visited = [False for i in range(max_id + 1)]

        self.circle = defaultdict(list)
        self.ans = []

        # import collections
        # print(collections.Counter([len(a) for a in list(self.edge_out.values())]))

    def get_pre_path(self, paths, pre):

        def find_path(path):
            pre_path = []
            for p in path:
                pre_path.append(p)
                if p == pre:
                    return pre_path
            return None

        ans = []
        for path in paths:
            pre_path = find_path(path)
            if pre_path:
                ans.append(pre_path)
        return ans

    def resort(self, path):
        a = np.array(path)
        index = np.argmin(a)
        return path[index:] + path[:index]
        # return path

    def clear_edge(self, u):
        for v in self.edge_out[u]:
            new_edge_in = []
            for u_ in self.edge_in[v]:
                if u_ != u:
                    new_edge_in.append(u_)
            self.edge_in[v] = new_edge_in
        self.edge_out[u] = []

    def dfs(self, pre, u):
        if len(self.edge_out[u]) == 0 or len(self.edge_in[u]) == 0:
            return
        self.visited[u] = True
        self.s.append(u)
        self.instack[u] = True

        for i in range(len(self.edge_out[u])):
            v = self.edge_out[u][i]
            if not self.instack[v]:
                if v in self.circle:
                    # print(u, v)
                    pre_paths = self.get_pre_path(self.circle[v], pre)
                    if pre_paths:  # find the pre path
                        for pre_path in pre_paths:
                            self.circle[u].append([v] + pre_path)
                            # print([u, v] + pre_path)
                            if len(pre_path) >= 1 and len(pre_path) <= 5:
                                self.ans.append(self.resort([u, v] + pre_path))
                        continue
                    else:
                        self.dfs(u, v)
                else:
                    self.dfs(u, v)
            else:
                k = 0
                for j in range(len(self.s) - 1, -1, -1):
                    if self.s[j] == v:
                        k = j
                        break
                # print(self.s[u:])
                if 7 + k >= len(self.s) >= 3 + k:
                    self.ans.append(self.resort(self.s[k:]))

                for j in range(k, len(self.s)):
                    self.circle[self.s[j]].append(self.s[j + 1:] + self.s[k:j])
                    # if self.s[j] not in self.circle:
                    #     self.circle[self.s[j]] = [self.s[j + 1:] + self.s[u:j]]
                    # else:
                    #     self.circle[self.s[j]].append(self.s[j + 1:] + self.s[u:j])

                    # print(self.circle)
                # print()

        self.s.pop()
        self.instack[u] = False

        self.clear_edge(u)

    def show_ans(self):

        self.ans.sort(key=lambda x: (len(x), x[0]))
        print(len(self.ans))
        for ans in self.ans:
            print(ans[0], end='')
            for a in ans[1:]:
                print(f',{a}', end='')
            print()


if __name__ == '__main__':
    solution = Solution('test_data.txt')
    for start in list(solution.edge_out.keys()):
        if not solution.visited[start] and len(solution.edge_in[start]) > 0 and len(solution.edge_out[start]) > 0:
            solution.dfs(-1, start)
    solution.show_ans()
