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
                    ans.append(pre_path)
                    js.append(j)
            if ans:
                break
        return ans, js

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

    def add_circle_path(self, path):
        for p in range(len(path)):
            self.circle[p].append(path[p + 1:] + path[:p])

    def dfs(self, u):
        if len(self.edge_out[u]) == 0 or len(self.edge_in[u]) == 0:
            return

        self.visited[u] = True
        self.s.append(u)
        self.instack[u] = True

        for i in range(len(self.edge_out[u])):
            v = self.edge_out[u][i]
            if not self.instack[v]:
                if v in self.circle:

                    pre_paths, js = self.get_pre_path(self.circle[v], self.s)
                    if pre_paths:  # find the pre path
                        for pre_path, j in zip(pre_paths, js):
                            path = [v] + pre_path + self.s[j + 1:]

                            self.add_circle_path(path)
                            if 3 <= len(path) <= 7:
                                self.ans.append(self.resort(path))
                        continue
                    else:
                        self.dfs(v)
                else:
                    self.dfs(v)
            else:
                k = 0
                for j in range(len(self.s) - 1, -1, -1):
                    if self.s[j] == v:
                        k = j
                        break
                ans = self.s[k:]

                if 3 <= len(ans) <= 7:
                    self.ans.append(self.resort(ans))

                for j in range(k, len(self.s)):
                    self.circle[self.s[j]].append(self.s[j + 1:] + self.s[k:j])

        self.s.pop()
        self.instack[u] = False

        self.clear_edge(u)

    def show_ans(self):
        self.ans.sort(key=lambda x: (len(x), x[0]))

        print(len(self.ans))
        for ans in self.ans:
            self.show_one(ans)

        # new_ans = [self.ans[0]]
        #
        # for index in range(1, len(self.ans)):
        #     if self.ans[index] == self.ans[index - 1]:
        #         continue
        #     # self.show_one(index)
        #     new_ans.append(self.ans[index])
        # print(len(new_ans))
        # for index in range(len(new_ans)):
        #     self.show_one(new_ans[index])

    def show_one(self, arr):
        print(arr[0], end='')
        for a in arr[1:]:
            print(f',{a}', end='')
        print()

    def debug(self, err_list):
        print(self.s)
        for node in err_list:
            print(
                f'node={node},ou={self.o_edge_out[node]},oi={self.o_edge_in[node]},u={self.edge_out[node]},i={self.edge_in[node]},instack={self.instack[node]},visited={self.visited[node]},circle={self.circle[node]}')


if __name__ == '__main__':
    solution = Solution('test_data.txt')
    for start in list(solution.edge_out.keys()):
        if not solution.visited[start] and len(solution.edge_in[start]) > 0 and len(solution.edge_out[start]) > 0:
            solution.dfs(start)
    solution.show_ans()

    # solution.debug([1131, 1780, 1627, 2196, 2112, 1630])
