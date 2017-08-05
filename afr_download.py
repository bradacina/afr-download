import urllib2
import unicodedata

from lxml.cssselect import CSSSelector
import html5lib

class AfrDownload:
    def __init__(self):
        self.headerSelector = CSSSelector('header.article__header > h1')
        self.articleSelector = CSSSelector('div.cq-article-content-paras.section > p')

    def downloadArticle(self,url):
        f = urllib2.urlopen(url)

        document = html5lib.parse(f, treebuilder='lxml',
                          encoding=f.info().getparam("charset"),
                          namespaceHTMLElements=False)

        headers = self.headerSelector(document)

        if len(headers) != 1:
            raise RuntimeError( 'Error: did not find exactly 1 header')

        title = headers[0].text

        articles = self.articleSelector(document)

        textList = [x for a in articles for x in a.itertext()]

        asciiText = [unicodedata.normalize('NFKD', unicode(t)).encode('ascii')
                     for t in textList]

        joinedArticle = ''.join(asciiText)
        
        titleAndArticle = ": ".join([title, joinedArticle])
        return titleAndArticle.replace('\\', '')
