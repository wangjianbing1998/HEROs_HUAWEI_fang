# coding=gbk
import heapq
import threading
import time
from collections import defaultdict
from threading import Thread


def run_time(func):
    def _warp(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        print(f'{func.__name__} run at {end - start} s')
        return res

    return _warp


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

        return compare__(self.priority[1], other.priority[1]) if self.priority[0] == other.priority[0] else \
            self.priority[0] < other.priority[0]


class Solution:

    def __init__(self, in_file_path, out_file_path, thread_num=10):

        self.out_file_path = out_file_path
        self.thread_num = thread_num
        self.s = []
        self.edge_out = defaultdict(list)
        self.o_edge_out = defaultdict(list)
        self.edge_in = defaultdict(list)
        self.o_edge_in = defaultdict(list)

        max_id = self.get_data_by_thread(in_file_path, thread_num)
        self.ix = []
        self.xi = {}
        for index, x in enumerate(self.o_edge_out):
            self.ix.append(x)
            self.xi[x] = index

        for x in self.o_edge_out:

            for y in self.o_edge_out[x]:
                if y in self.xi:
                    self.edge_out[self.xi[x]].append(self.xi[y])

            for y in self.o_edge_in[x]:
                if y in self.xi:
                    self.edge_in[self.xi[x]].append(self.xi[y])

        del self.o_edge_out
        del self.o_edge_in
        del self.xi
        self.instack = [False for i in range(len(self.ix) + 1)]
        self.visited = [False for i in range(len(self.ix) + 1)]

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
        for i in range(thread_num):
            t[i].join()
            for line in t[i].get_result():
                x, y, money = line.split(',')
                self.o_edge_out[x].append(y)
                self.o_edge_in[y].append(x)
        return -1

    def get_data(self, file_path):
        with open(file_path, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if len(line) > 0:
                    x, y, money = line.split(',')
                    self.o_edge_out[x].append(y)
                    self.o_edge_in[y].append(x)

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
                                heapq.heappush(self.ans, CompareAble((len(resort_v), resort_v), resort_v))
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
                    resort_v = self.resort(ans)
                    heapq.heappush(self.ans, CompareAble((len(resort_v), resort_v), resort_v))

                for j in range(k, len(self.s)):
                    self.circle[self.s[j]].append(self.s[j + 1:] + self.s[k:j])

        self.s.pop()
        self.instack[u] = False

        self.clear_edge(u)

    def show_ans(self, write=True):

        def generate_ans(size):
            s = 0
            ans = []
            while self.ans:
                if s == size:
                    yield ans
                    ans = []
                    s = 0
                task = heapq.heappop(self.ans)
                ans.append(task.value)
                s += 1
            yield ans

        if write:
            with open(self.out_file_path, 'w+') as f:
                mu = threading.Lock()

                def write_file(datas):
                    if mu.acquire(True):
                        for data in datas:
                            for index, p_data in enumerate(data):
                                f.write(','.join(p_data) + '\n')
                        mu.release()

                f.write(str(len(self.ans)) + '\n')

                batch_size = len(self.ans) // self.thread_num
                for i in range(self.thread_num):
                    Thread(target=write_file, args=(generate_ans(batch_size),)).start()

        else:
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
        print(f's={[self.ix[x] for x in self.s]}')
        for node in err_list:
            print(
                f'node={node},ou={self.o_edge_out[node]},oi={self.o_edge_in[node]},u={[self.ix[x] for x in self.edge_out[self.xi[node]]]},i={[self.ix[x] for x in self.edge_in[self.xi[node]]]},instack={self.instack[self.xi[node]]},visited={self.visited[self.xi[node]]},circle={[[self.ix[x] for x in xs] for xs in self.circle[self.xi[node]]]}')


@run_time
def main(_):
    for __ in range(_):

        # solution = Solution(in_file_path='/data/test_data.txt', out_file_path='/projects/student/result.txt', thread_num=80)
        solution = Solution(in_file_path='T.txt', out_file_path='resT.txt', thread_num=280)
        # solution = Solution(in_file_path='test_data.txt', out_file_path='remove_set.txt', thread_num=80)
        for start in list(solution.edge_out.keys()):
            if not solution.visited[start] and len(solution.edge_in[start]) > 0 and len(solution.edge_out[start]) > 0:
                solution.dfs(start)
        solution.show_ans(write=True)


if __name__ == '__main__':
    main(1)
