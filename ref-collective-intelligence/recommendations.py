#coding=utf-8
critics={
    'Lisa Rose':{
        'Lady in the Water':2.5,
        'Snakes on a Plane':3.5,
        'Just My Luck':3.0,
        'Superman Returns':3.5,
        'You,Me and Dupree':2.5,
        'The Night Listener':3.0
        },
    'Gene Seymour':{
        'Lady in the Water':3.0,
        'Snakes on a Plane':3.5,
        'Just My Luck':1.5,
        'Superman Returns':5.0,
        'The Night Listener':3.0,
        'You,Me and Dupree':3.5        
        },
    'Michael Phillips':{
        'Lady in the Water':2.5,
        'Snakes on a Plane':3.0,
        'Superman Returns':3.5,
        'The Night Listener':4.0
        },
    'Claudia Puig':{
        'Snakes on a Plane':3.5,
        'Just My Luck':3.0,
        'The Night Listener':4.5,        
        'Superman Returns':4.0,
        'You,Me and Dupree':2.5,
        },
    'Mick LaSalle':{
        'Lady in the Water':3.0,
        'Snakes on a Plane':4.0,
        'Just My Luck':2.0,
        'Superman Returns':3.0,
        'The Night Listener':3.0,        
        'You,Me and Dupree':2.0
        },
    'Jack Matthews':{
        'Lady in the Water':3.0,
        'Snakes on a Plane':4.0,
        'The Night Listener':3.0,        
        'Superman Returns':5.0,
        'You,Me and Dupree':3.5
        },
    'Toby':{
        'Snakes on a Plane':4.5,
        'You,Me and Dupree':1.0,
        'Superman Returns':4.0
        }
    }

from math import sqrt

# 返回一个有关person1 与 person2的基于距离的相似度评价
def sim_distance(prefs,person1,person2):
    # 有共同的评价item
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1
    #如果两者没有共同item 
    if len(si) == 0:
        return 0

    sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2) for item in prefs[person1] if item in prefs[person2]])
    return 1/(1+sqrt(sum_of_squares))

# 返回p1 和 p2的皮尔逊相关系数
def sim_pearson(prefs,p1,p2):
    # 得到双方都曾评价过的物品列表
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]: 
            si[item] = 1
    # 元素个数
    n = len(si)

    if n == 0 :
        return 1
    # 分别对两者的所有偏好直接求和
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    # 分别对两者的所有偏好先求平方，再求和
    sum1Sq = sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it],2) for it in si])

    # 两者对应的评价相乘，再求和
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    # 计算皮尔逊值
    num  = pSum - (sum1*sum2/n)
    den = sqrt((sum1Sq - pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den == 0:
        return 0
    r = num/den
    return r

# $ python
# Python 2.7.12 (default, Nov 20 2017, 18:23:56) 
# [GCC 5.4.0 20160609] on linux2
# Type "help", "copyright", "credits" or "license" for more information.
# >>> from recommendations import *
# >>> print sim_pearson(critics,'Lisa Rose','Gene Seymour')
# 0.396059017191

# 从字段中返回最为匹配的人
# 入参person为需要找到和此人类似的
# 返回结果的个数和相似度函数为可选参数
def topMatches(prefs,person,n=5,similarity=sim_pearson):
    # 列表推导式
    scores = [
        (similarity(prefs,person,other))
        for other in prefs if other != person
    ]

    #对列表进行排序，评价值最高者排在最前面
    scores.sort()
    scores.reverse()
    # 截取到n
    return scores[0:n]
# >>> from recommendations import *
# >>> topMatches(critics,'Toby',n=3)
# [0.9912407071619299, 0.9244734516419049, 0.8934051474415647]

# 利用所有他人评价值的加权平均 为某人提供建议 对欧几里德距离评价和皮尔逊相关度评价都适用
def getRecommendations(prefs,person,similarity=sim_pearson):
    # 每个商品加权权值的累积和
    totals = {}
    # 原始相似度和
    simSums = {}
    for other in prefs:
        # 排除和自己比较
        if other == person:
            continue
        sim=similarity(prefs,person,other)

        # 忽略评价值为0或者小于0的情况
        if sim <= 0 :
            continue
        for item in prefs[other]:
            # 只对自己还未曾看过的影片进行评价
            if item not in prefs[person] or prefs[person][item] == 0:
                # 相似度×评价值
                # 如果键不存在于字典中，将会添加键并将值设为默认值
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
                #相似度之和
                simSums.setdefault(item,0)
                simSums[item]+=sim

    # 建立一个归一化的列表 
    # rankings key为分数，value为name 
    rankings = [(total/simSums[item],item) for item ,total in totals.items()]

    # 返回经过排序的列表
    rankings.sort()
    rankings.reverse()
    return rankings
# >>> from recommendations import *
# >>> getRecommendations(critics,'Toby')
# [(3.3477895267131013, 'The Night Listener'), (2.8325499182641614, 'Lady in the Water'), (2.5309807037655645, 'Just My Luck')]
# >>> 

# 上面是人相管理的推荐 而下面的 商品相似度推荐和上面是相通的 只需要把字典的k v转换一下就可以了
def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
            # 将物品和人员对掉
            result[item][person]=prefs[person][item]
    return result
# >>> from recommendations import *
# >>> movies= transformPrefs(critics)
# >>> topMatches(movies,'Superman Returns')
# [0.6579516949597695, 0.4879500364742689, 0.11180339887498941, -0.1798471947990544, -0.42289003161103106]

