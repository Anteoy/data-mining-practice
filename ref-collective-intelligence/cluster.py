#!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image,ImageDraw
# 解析blogdata.txt数据文件
def readfile(filename):
    lines = [line for line in file(filename)]

    # 第一行是列标题 单词 strip 前后去空格
    colnames = lines[0].strip().split('\t')[1:]
    # 博客名
    rownames = []
    # 每行数据的个数
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        rownames.append(p[0])
        data.append([float(x) for x in p[1:]])
    return (rownames, colnames, data)

from math import sqrt

# 计算皮尔逊相似度
def pearson(v1, v2):
    sum1 = sum(v1)
    sum2 = sum(v2)

    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])

    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])

    num = pSum - sum1 * sum2 / len(v1)
    den = sqrt((sum1Sq - pow(sum1, 2) / len(v1)) * (sum2Sq - pow(sum2, 2)
               / len(v1)))
    if den == 0:
        return 0
    return 1.0 - num / den

# 聚类类定义 
class bicluster:
    def __init__(
        self,
        vec,
        left=None,
        right=None,
        distance=0.0,
        id=None,
        ):
        # 左节点
        self.left = left
        # 右节点
        self.right = right
        # 自由聚类的数据
        self.vec = vec
        # 聚类id
        self.id = id
        # 到哪儿的距离？ => closest 计算得来的最近距离
        self.distance = distance

def hcluster(rows, distance=pearson):
    # 距离缓存
    distances = {}
    currentclustid = -1

    # 最开始的聚类就是数据集中的行
    # 聚类列表
    clust = [bicluster(rows[i], id=i) for i in range(len(rows))]

    while len(clust) > 1:
        # 开始配对的是0,1
        lowestpair = (0, 1)
        # 最近的值？ 计算两个聚类的距离哦
        closest = distance(clust[0].vec, clust[1].vec)

        # 遍历每一个配对类 寻找最小距离
        for i in range(len(clust)):
            for j in range(i + 1, len(clust)):
                # distances 距离缓存 没有缓存则重新计算
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = \
                        distance(clust[i].vec, clust[j].vec)

                d = distances[(clust[i].id, clust[j].id)]

                if d < closest:
                    closest = d
                    lowestpair = (i, j)

        # 计算两个聚类的平均值作为新的聚类值
        mergevec = [(clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i])
                    / 2.0 for i in range(len(clust[0].vec))]

        # 创建新聚类 
        newcluster = bicluster(mergevec, left=clust[lowestpair[0]],
                               right=clust[lowestpair[1]], distance=closest,
                               id=currentclustid)

        # 归0
        currentclustid -= 1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)
    # 计算完成的根节点
    return clust[0]

def printclust(clust, labels=None, n=0):
    # 利用缩进建立层级布局
    for i in range(n):
        print ' ',
    if clust.id < 0:
        # 负数标记代表这是一个分支 
        print '-'
    else:
        # 正数标记代表这是一个叶节点
        if labels == None:
            print clust.id
        else:
            print labels[clust.id]
    # 递归打印左右分支
    if clust.left != None:
        printclust(clust.left, labels=labels, n=n + 1)
    if clust.right != None:
        printclust(clust.right, labels=labels, n=n + 1)

def getheight(clust):
    # 只有一个节点则高度为1
    if clust.left == None and clust.right == None:
        return 1

    # 每个分支的高度之和
    return getheight(clust.left) + getheight(clust.right)

# 计算深度
def getdepth(clust):
    if clust.left == None and clust.right == None:
        return 0
    return max(getdepth(clust.left), getdepth(clust.right)) + clust.distance

# 为每一个聚类生成一个图片 高度20像素，高度固定 IOError: decoder zip not available
def drawdendrogram(clust, labels, jpeg='clusters.jpg'):
    h = getheight(clust) * 20
    w = 1200
    depth = getdepth(clust)

    scaling = float(w - 150) / depth

    img = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.line((0, h / 2, 10, h / 2), fill=(255, 0, 0))

    drawnode(
        draw,
        clust,
        10,
        h / 2,
        scaling,
        labels,
        )
    img.save(jpeg, 'JPEG')

def drawnode(
    draw,
    clust,
    x,
    y,
    scaling,
    labels,
    ):
    if clust.id < 0:
        h1 = getheight(clust.left) * 20
        h2 = getheight(clust.right) * 20
        top = y - (h1 + h2) / 2
        bottom = y + (h1 + h2) / 2
        ll = clust.distance * scaling
        draw.line((x, top + h1 / 2, x, bottom - h2 / 2), fill=(255, 0, 0))

        draw.line((x, top + h1 / 2, x + ll, top + h1 / 2), fill=(255, 0, 0))

        draw.line((x, bottom - h2 / 2, x + ll, bottom - h2 / 2), fill=(255, 0,
                  0))

        drawnode(
            draw,
            clust.left,
            x + ll,
            top + h1 / 2,
            scaling,
            labels,
            )
        drawnode(
            draw,
            clust.right,
            x + ll,
            bottom - h2 / 2,
            scaling,
            labels,
            )
    else:
        draw.text((x + 5, y - 7), labels[clust.id], (0, 0, 0))

# 列和行互换  为了求列聚类 也就是列代表单词， 计算哪些单词市场会结合在一起使用
def rotatematrix(data):
    newdata = []
    for i in range(len(data[0])):
        newrow = [data[j][i] for j in range(len(data))]
        newdata.append(newrow)
    return newdata