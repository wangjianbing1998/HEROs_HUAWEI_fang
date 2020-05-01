# coding=gbk
from collections import defaultdict

import better_exceptions
from my_utils import run_time

better_exceptions.hook()
import heapq
import threading


class Reader(threading.Thread):
    def __init__(self, file_name, start_pos, end_pos):
        super(Reader, self).__init__()
        self.file_name = file_name
        self.start_pos = start_pos
        self.end_pos = end_pos

    def run(self):
        fd = open(self.file_name, 'r')
        if self.start_pos != 0:
            fd.seek(self.start_pos - 1)
            if fd.read(1) != '\n':
                line = fd.readline()
                self.start_pos = fd.tell()
        fd.seek(self.start_pos)

        self.result = []
        while (self.start_pos <= self.end_pos):
            line = fd.readline().strip()
            # print(line)
            if len(line) > 0:
                self.result.append(line)
            self.start_pos = fd.tell()

    def get_result(self):
        return self.result


class Partition(object):
    def __init__(self, file_name, thread_num):
        self.file_name = file_name
        self.block_num = thread_num

    def part(self):
        fd = open(self.file_name, 'r')
        fd.seek(0, 2)
        pos_list = []
        file_size = fd.tell()
        block_size = file_size / self.block_num
        start_pos = 0
        for i in range(self.block_num):
            if i == self.block_num - 1:
                end_pos = file_size - 1
                pos_list.append((start_pos, end_pos))
                break
            end_pos = start_pos + block_size - 1
            if end_pos >= file_size:
                end_pos = file_size - 1
            if start_pos >= file_size:
                break
            pos_list.append((start_pos, end_pos))
            start_pos = end_pos + 1
        fd.close()
        return pos_list


class CompareAble:
    def __init__(self, priority, value):
        self.priority = priority
        self.value = value

    def __lt__(self, other):
        return self.priority <= other.priority


class Solution:

    def __init__(self, file_path, thread_num=10):

        self.s = []
        self.edge_out = defaultdict(list)
        self.edge_in = defaultdict(list)

        # max_id = self.generate_data(in_file_path)

        max_id = self.get_data_by_thread(file_path, thread_num)

        self.instack = [False for i in range(max_id + 1)]
        self.visited = [False for i in range(max_id + 1)]

        self.circle = defaultdict(list)
        self.ans = []

    def get_data_by_thread(self, file_path, thread_num):
        p = Partition(file_path, thread_num=thread_num)
        t = []
        pos = p.part()
        for i in range(thread_num):
            t.append(Reader(file_path, *pos[i]))
        for i in range(thread_num):
            t[i].start()
        max_id = -1
        for i in range(thread_num):
            t[i].join()
            for line in t[i].get_result():
                x, y, money = line.split(',')
                self.edge_out[int(x)].append(int(y))
                self.edge_in[int(y)].append(int(x))

                max_id = max(max_id, int(x))
        return max_id

    def get_data(self, file_path):
        max_id = -1
        with open(file_path, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if len(line) > 0:
                    x, y, money = line.split(',')
                    self.edge_out[int(x)].append(int(y))
                    self.edge_in[int(y)].append(int(x))

                    max_id = max(max_id, int(x))
        return max_id

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
        min_v = path[0]
        min_i = 0
        for i, p in enumerate(path):
            if p < min_v:
                min_i = i
        return path[min_i:] + path[:min_i]

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
                                resort_v = self.resort(path)
                                heapq.heappush(self.ans, CompareAble((len(resort_v), resort_v[0]), resort_v))
                        return
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
                    resort_v = self.resort(ans)
                    heapq.heappush(self.ans, CompareAble((len(resort_v), resort_v[0]), resort_v))

                for j in range(k, len(self.s)):
                    self.circle[self.s[j]].append(self.s[j + 1:] + self.s[k:j])

        self.s.pop()
        self.instack[u] = False

        self.clear_edge(u)

    def show_ans(self):

        print(len(self.ans))
        while self.ans:
            task = heapq.heappop(self.ans)
            self.show_one(task.value)

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


@run_time
def main(_):
    for _ in range(_ // 5000):

        solution = Solution('test_data.txt')
        for start in list(solution.edge_out.keys()):
            if not solution.visited[start] and len(solution.edge_in[start]) > 0 and len(solution.edge_out[start]) > 0:
                solution.dfs(start)
        # solution.show_ans()


if __name__ == '__main__':
    main(280000)
