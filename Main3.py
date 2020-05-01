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


class Solution:

    def __init__(self, in_file_path, out_file_path):

        self.out_file_path = out_file_path
        self.s = []
        self.edge_out = {}
        self.o_edge_out = {}
        self.edge_in = {}
        self.o_edge_in = {}

        max_id = self.get_data(in_file_path)
        self.ix = []
        self.xi = {}
        for index, x in enumerate(self.o_edge_out):
            self.ix.append(x)
            self.xi[x] = index

        for x in self.o_edge_out:

            for y in self.o_edge_out[x]:
                if y in self.xi:
                    default_dict_list(self.edge_out, self.xi[x], self.xi[y])
            if x in self.o_edge_in:
                for y in self.o_edge_in[x]:
                    if y in self.xi:
                        default_dict_list(self.edge_in, self.xi[x], self.xi[y])

        # del self.o_edge_out
        # del self.o_edge_in
        # del self.xi
        self.instack = [False for i in range(len(self.ix) + 1)]
        self.visited = [False for i in range(len(self.ix) + 1)]

        self.circle = {}
        self.ans = []

    def get_data(self, file_path):
        with open(file_path, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if len(line) > 0:
                    x, y, money = line.split(',')

                    default_dict_list(self.o_edge_out, x, y)
                    default_dict_list(self.o_edge_in, y, x)


        return -1

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
        min_v = self.ix[path[0]]
        min_i = 0
        for i, p in enumerate(path):
            if compare_(self.ix[p], min_v):
                min_i = i
                min_v = self.ix[p]
        return [self.ix[i] for i in path[min_i:] + path[:min_i]]

    def clear_edge(self, u):
        for v in self.edge_out[u]:
            new_edge_in = []
            if v in self.edge_in:
                for u_ in self.edge_in[v]:
                    if u_ != u:
                        new_edge_in.append(u_)
                self.edge_in[v] = new_edge_in
        self.edge_out[u] = []

    def add_circle_path(self, path):
        for p in range(len(path)):
            default_dict_list(self.circle, path[p], path[p + 1:] + path[:p])

    def dfs(self, start, u):
        # print(self.ix[u])
        # self.debug([1005, 1359, 2246, 1436, 1594, 1375])
        # print(f'depth={len(self.s)}')
        if u < start or u not in self.edge_out or len(self.edge_out[u]) == 0 or u not in self.edge_in or len(
                self.edge_in[u]) == 0:
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
                                resort_v = self.resort(path)
                                self.ans.append(resort_v)
                        continue
                    else:
                        self.dfs(start, v)
                else:
                    self.dfs(start, v)
            else:
                k = 0
                for j in range(len(self.s) - 1, -1, -1):
                    if self.s[j] == v:
                        k = j
                        break
                ans = self.s[k:]

                if 3 <= len(ans) <= 7:
                    resort_v = self.resort(ans)
                    self.ans.append(resort_v)

                for j in range(k, len(self.s)):
                    default_dict_list(self.circle, self.s[j], self.s[j + 1:] + self.s[k:j])

        self.s.pop()
        self.instack[u] = False

        self.clear_edge(u)

    def show_ans(self, write=True):
        self.ans.sort(key=lambda x: CompareAble(len(x), x))
        if write:
            with open(self.out_file_path, 'w+') as f:
                def write_file(datas):
                    for data in datas:
                        f.write(','.join(data) + '\n')

                f.write(str(len(self.ans)) + '\n')
                write_file(self.ans)

        else:
            print(len(self.ans))
            for value in self.ans:
                self.show_one(value)

    def show_one(self, arr):
        print(arr[0], end='')
        for a in arr[1:]:
            print(f',{a}', end='')
        print()

    def debug(self, err_list):
        print(f's={[self.ix[x] for x in self.s]}')
        for node in err_list:
            node = str(node)
            print(
                f'node={node},ou={self.o_edge_out[node]},oi={self.o_edge_in[node]},u={[self.ix[x] for x in self.edge_out[self.xi[node]]]},i={[self.ix[x] for x in self.edge_in[self.xi[node]]]},instack={self.instack[self.xi[node]]},visited={self.visited[self.xi[node]]},circle={[[self.ix[x] for x in xs] for xs in (self.circle[self.xi[node]] if self.xi[node] in self.circle else [])]}')

        print(self.ans)


@run_time
def main(_):
    # global solution

    # solution = Solution(in_file_path='/data/test_data.txt', out_file_path='/projects/student/result.txt')
    # solution = Solution(in_file_path='T.txt', out_file_path='resT.txt')
    # solution = Solution(in_file_path='test_data2.txt', out_file_path='res2.txt')
    # solution = Solution(in_file_path='in.txt', out_file_path='out.txt')
    solution = Solution(in_file_path='test_data.txt', out_file_path='ans.txt')
    for start in list(solution.edge_out.keys()):
        if not solution.visited[start] and start in solution.edge_in and len(
                solution.edge_in[start]) > 0 and start in solution.edge_out and len(solution.edge_out[start]) > 0:
            solution.dfs(start, start)
    solution.show_ans(write=True)


if __name__ == '__main__':
    main(1)