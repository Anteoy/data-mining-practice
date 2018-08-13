import feedparser
import re

# 返回一个RSS订阅源的标题和包含单词计数情况的字典
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