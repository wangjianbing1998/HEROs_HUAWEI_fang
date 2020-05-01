# coding=gbk
from collections import defaultdict

import better_exceptions
import numpy as np

better_exceptions.hook()


class Solution:

    def __init__(self, file_path):

        self.m, self.n = 9, 12
        self.s = []
        data = np.loadtxt(file_path, dtype=int)
        max_X, max_Y, max_money = data.max(axis=0)
        self.instack = [False for i in range(len(data))]
        self.edges = [[] for i in range(max(max_X, max_Y) + 1)]
        self.cnt = 0
        for x, y, money in data:
            self.edges[x].append(y)
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

    def dfs(self, pre, u):

        self.s.append(u)
        self.instack[u] = True

        for i in range(len(self.edges[u])):
            v = self.edges[u][i]
            if not self.instack[v]:
                if v in self.circle:
                    print(u, v)
                    pre_path = self.get_pre_path(self.circle[v], pre)
                    if pre_path:  # find the pre path
                        self.circle[u].append([v] + pre_path)
                        print([u,v] + pre_path)
                        self.ans.append([u,v] + pre_path)
                        continue
                    else:
                        self.dfs(u, v)
                else:
                    self.dfs(u, v)
            else:
                self.cnt += 1
                print(f'find -> {self.cnt}')
                k = 0
                for j in range(len(self.s) - 1, -1, -1):
                    if self.s[j] == v:
                        k = j
                        break
                print(self.s[k:])
                self.ans.append(self.s[k:])

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


if __name__ == '__main__':
    solution = Solution('in.txt')
    solution.dfs(-1, 1)
