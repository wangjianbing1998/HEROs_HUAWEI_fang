# 初赛
## Test Dataset
- test_data.txt 官网给的，数据量较少，mini版,忽略时间
- test_data_2.txt 自己生成的，数据量达到280w,为了方便看到结果对不对，所以是直接复制几份test_data.txt得到的数
- test_data_3.txt 按照其他算法随机生成的280w数据量，result3.txt 就是对应的answer


## Algorithm

- 方法一（时间太慢）：
    - 使用circle保存了已经成环的路径，比如2-1-4-3-2形成一个环，则circle[2]=[1,4,3],circle[1]=[4,3,2],circle[4]=[3,2,1],circle[3]=[2,1,4]
    那么下一次访问到2,1,4,3中的任意一个点后，可以直接将路径加上去即可return
    - 对于只有入度或者只有出度的点不被访问，可以直接pass
    - 在访问的过程中，如果退栈之后可以将该点的出度全部删除，以防下一次再次访问，比如访问的栈为[2,1,4,3]访问完了3之后，从3回退到4时，可以将3的出度全部删除，之所以可以这样做，是因为3回退回去之后表明3的出度已经全部访问完了，无需第二次访问，这也就可以避免重复环路的出现
    - 出现的问题是当深度很大时，会爆栈，提交出现RE
    - 因为题目要求的是3-7的环路长度即可，所以走到7步之后可以停止了，所以就在走到7步之后就回退，但是这种情况下不会删除这条回退回去的边，从其他路回退的边可以删除，如果从其父节点再回退时也不会删除边，因为下次还需要访问这个点
    并且对所有点都尝试一次遍历，只需要该点的存在出度且存在入度即可


- 方法二（快很多）：
    - 三领域方法，从该点的入度和出度分别走三步即可，找出领域，然后对该点走最多七步找到环路
    - 本想可以将环路存储路径的方法加进去，但是还没有实现成功，最后提交时间是0.21s

## 初赛上分过程
- 第一版基于栈的6+1，线上4.8s
- 在第一版的基础上做了多进程优化，线上1.74s。这一版分配节点我采用的是4个进程，根据线下100w数据合理分配每个进程的处理的节点数，尽可能使每个进程时间相等，属于瞎调参。后面看到有个知乎老哥通过建模计算参数的方法，着实让我眼前一亮
- 多进程5+2版本，线上1.36s。多进程4+3版本，线上5.9s。这里我可能4+3实现得不好，导致时间反而增多了
- 6+1和5+2结合，一次性找两层环的方法。负优化了
- 之后把5+2的栈改写成了for循环，线上单线程1.39s
- 优化了写入，建立一个完整的char数组在去写入，线上单线程0.93s。到这里开始感觉这个比赛就是个IO大赛了。
- 由于多进程感觉要映射的共享内存太多了，使用多线程去做，线上8线程，成绩0.69s
- 根据线下的数据集，入度为零的节点占了一半。所以优化了建图。建图的时候(我是通过出度表和入度表这种感觉比较耗时的方式去建图的)，只对入度不为零的节点建图。线上成绩0.60s
- 去掉了重映射，采用计数排序的方法去统计节点和建图，同时基本把所有的vector改数组。线上0.37s
- 加了一个统计第二层子节点的遍历次数，若第二层子节点的遍历次数等于入度数时，就跳过的操作(因为此时第二层子节点已经不会有环了，有环的话在第一层子节点已经找过了)。线上0.35s。不确定是不是抖动
- 最后一天，赛题组奇怪的操作炸出了群里大佬的各种trick。利用这些trick做的优化，最终成绩0.21s，武长赛区第八名


# 复赛

基本上改的就是图的大小：
- 转账记录28W->200W
- 环的个数从200W变到2000W
- 转账金额要求[A,B,X][B,C,Y]要满足0.2<=Y/X<=3

## 复赛上分过程

- 复赛过程其实也知道自己实力进不了四强，所以花的时间并不多，基本上只做了四个版本的迭代。

- 修改了数据结构，改用结构体数组去做。之后在修改的过程中发现字典的查找和调用其实还是很耗时的，所以尽可能的去减少了字典的调用。
- 线上提交的有效成绩共三次，一次5+2单线程版本，58.6s
- 4+3单线程版本，24.74s
- 4+3多线程版本，7.98s
- 三层入度表一开始是用字典形式去做的，发现字典耗时之后，改了一半用数组去存储key，然后直接用链表去做的版本，线下1900w的数据提升了5s左右(优化做得不好，线下还是要17s)，线上反而慢了1s。不过没有细究原因，现在还是不解。
- 想做没做的优化:改数据结构，用左右边界去维护，做的出度表和入度表。这个改了一版，但是没有继续优化;用线程池的方式，用任务抢占去做负载均衡，这个没有去做。



## 复赛当天
事实上，2点开始比赛，3点前就把官方给的样例跑过了，也在群里对了其他同学的100w数据，也没错。然后上传都判了10min了，还以为过了，结果给一个0%WA的错误。然后发现是float精度不够，换了double。在等待反馈的过程中，简单调试了一下，发现double精度也不够。于是改了一个读小数点后两位，然后小数点前面*100再加上去的long int版本，线下100w和官方样例同样过了，信心满满的上传，等了十分钟又是0%WA。这时候其实就开始慌了，时间只剩下不到一个小时，机会只剩两次。觉得可能是有些数组没开够的原因，然后就尽可能把所有数组都开大，比如写入结果的数组，还是没出来结果。最后发现可能是id的问题，虽然我之前用了long int，但是在转换的过程中我用了int去转换，比无符号整型少了一位。太急了改完上传忘记去掉#define TEST了，直接路径错误，就没了。

最后交卷时间不够的时候，其实很慌，也没能仔细看进去代码。不过其实赛后看了一下，感觉也找不出问题。
可能经历过这种心扑通扑通之后才知道原来自己这么在乎这个比赛
不过过来了，也还好，希望哪位前四强的大佬看到这个后给小弟指点指点迷津，小弟也没白参加这次比赛
昨天简单看了一下大佬们开源的代码，才觉得自己写的代码实在是难看，没有封装，细节也没有做好。学到了很多，继续努力吧。最后，感谢一下我的队友，这一个月要是没有队友，一个人可能很早就放弃了

学习，加油，加油，学习
冲鸭呀呀呀呀呀~~~

