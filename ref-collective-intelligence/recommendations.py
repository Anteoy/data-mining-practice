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
