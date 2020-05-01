# coding=gbk
from collections import defaultdict

import better_exceptions
import numpy as np

better_exceptions.hook()


class Solution:

    def __init__(self, file_path):

        self.s = []
        self.o_edges = defaultdict(list)
        self.o_edge_in = defaultdict(list)

        self.edges = defaultdict(list)
        self.edge_in = defaultdict(list)

        self.ix = {}
        self.xi = {}
        self.iy = {}
        self.yi = {}

        with open(file_path, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if len(line) > 0:
                    x, y, money = line.split(',')
                    self.o_edges[int(x)].append(int(y))
                    self.o_edge_in[int(y)].append(int(x))

            self.ix = dict([(i, j) for i, j in zip(range(len(self.o_edges)), self.o_edges.keys())])
            for ix, x in enumerate(self.o_edges):
                self.ix[ix] = x
                self.xi[x] = ix

        self.instack = [False for i in range(len(self.o_edges) + 1)]

        self.circle = defaultdict(list)
        self.ans = []

    def get_pre_path(self, paths, pre):
        for path in paths:
            pre_path = []
            for p in path:
                pre_path.append(p)
                if p == pre:
                    return pre_path

        return None

    def resort(self, path):
        a = np.array(path)
        index = np.argmin(a)
        return path[index:] + path[:index]

    def dfs(self, pre, u):
        if len(self.o_edges[u]) == 0 or len(self.o_edge_in[u]) == 0:
            return

        self.s.append(u)
        self.instack[u] = True

        for i in range(len(self.o_edges[u])):
            v = self.o_edges[u][i]
            if not self.instack[v]:
                if v in self.circle:
                    # print(u, v)
                    pre_path = self.get_pre_path(self.circle[v], pre)
                    if pre_path:  # find the pre path
                        self.circle[u].append([v] + pre_path)
                        # print([u, v] + pre_path)
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

    def show_ans(self):

        self.ans.sort(key=lambda x: (len(x), x[0]))
        print(len(self.ans))
        for ans in self.ans:
            print(ans[0], end='')
            for a in ans[1:]:
                print(f',{a}', end='')
            print()


if __name__ == '__main__':
    solution = Solution('in2.txt')
    for start in solution.o_edges:
        if not solution.instack[start] and len(solution.o_edge_in[start]) > 0:
            solution.dfs(-1, start)
    solution.show_ans()
