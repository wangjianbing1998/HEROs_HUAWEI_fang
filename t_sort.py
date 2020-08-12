# coding=gbk

import heapq

from Trick_version.Main import CompareAble

l = []

data = ['123', '234', '345']
heapq.heappush(l, CompareAble((len(data), data), data))

data = ['123', '234', '111111']
heapq.heappush(l, CompareAble((len(data), data), data))

data = ['38128938912839']
heapq.heappush(l, CompareAble((len(data), data), data))

while l:
    print(heapq.heappop(l).value)
