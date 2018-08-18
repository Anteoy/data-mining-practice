#!/usr/bin/python
# -*- coding: utf-8 -*-
import feedparser
import re

# 返回一个RSS订阅源的标题和此订阅源包含单词计数情况的字典
def getwordcounts(url):
    # 解析订阅源
    d = feedparser.parse(url)
    # 单词计数
    wc = {}
    # 循环遍历所有文章条目
    for e in d.entries:
        # 有摘要就使用摘要 否则使用描述
        if 'summary' in e:
            summary = e.summary
        else:
            summary = e.description
        # 提取一个单词列表
        words = getwords(e.title + ' '+ summary)
        for word in words:
            # 不知道这句是否有必要
            wc.setdefault(word,0)
            wc[word]+=1
    return d.feed.title,wc
# 提取一个单词列表
def getwords(html):
    # 去除html标签
    # sub是substitute的所写，表示替换
    txt = re.compile(r'<[^>]+>').sub('',html)
    # 利用所有非字母字符拆分出单词
    words = re.compile(r'[^A-Z^a-z]+').split(txt)
    # 小写
    return [word.lower() for word in words if word != '']

# 统计所有单词和出现次数
apcount = {}
# 存储getwordcounts的每个博客的标题和同级结果
wordcounts = {}

feedlist = [line for line in file('feedlist.txt')]
for feedurl in feedlist:
    title,wc = getwordcounts(feedurl)
    wordcounts[title] = wc
    for word,count in wc.items():
        # 如果键不存在于字典中，将会添加键并将值设为默认值
        apcount.setdefault(word,0)
        if count > 1:
            apcount[word]+=1
# 塞选平均单词占比的范围在wordlist 0.1 到 0.5 之间的单词作为最终来统计的
# 最终的单词list
wordlist = []
for (w, bc) in apcount.items():
    frac = float(bc) / len(feedlist)
    if frac > 0.1 and frac < 0.5:
        wordlist.append(w)

# 生成清洗后的数据文件
out = file('blogdata.txt', 'w')
out.write('Blog')
for word in wordlist:
    out.write('\t%s' % word)
# 换行
out.write('\n')
for (blog, wc) in wordcounts.items():
    # 标题和单词统计
    print blog
    out.write(blog)
    for word in wordlist:
        if word in wc:
            # 写入这个word在此博客出现的次数
            out.write('\t%d' % wc[word])
        # 不需要统计这个word
        else:
            out.write('\t0')
    out.write('\n')