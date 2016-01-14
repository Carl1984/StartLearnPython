from bs4 import BeautifulSoup
import urllib.request
import html.parser as h


class MyHTMLParser(h.HTMLParser):
    a_t=False
    htmlcontent = ''
    irow = 0
    lastrow = 0
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for attr in attrs:
                if str(attr[1]).strip() == 'articalContent':
                    self.a_t=True
                elif str(attr[1]).strip() == 'shareUp':
                    self.a_t=False
    def handle_endtag(self, tag):
        if tag == "p":
            if self.a_t==True:
                self.htmlcontent  = self.htmlcontent + '\n'
                self.irow = self.irow + 1
        if tag == "div":
            if self.a_t==True:
                self.htmlcontent  = self.htmlcontent + '\n'
                self.irow = self.irow + 1
    def handle_data(self, data):
        if self.a_t is True:
           if (str(data).strip() != '') and (str(data).strip() != '\n'):
            if self.irow ==0:
                self.lastrow = self.irow
                self.htmlcontent  = self.htmlcontent + '  ' +str(data).strip(' ').strip('\n')
            elif self.lastrow < self.irow:
                self.lastrow = self.irow
                self.htmlcontent  = self.htmlcontent + '  ' +str(data).strip(' ').strip('\n')
            else:
                self.htmlcontent  = self.htmlcontent + str(data).strip(' ')
        else:
            pass
def downloadwebpage(url,name):
    '''
    url= str0[str0.find(r'href="')+6:str0.find(r'html">')+4]
    print (url)
    title=str0[str0.find(r'html">')+6:str0.find(r'</a>')]
    print (title)
    '''
    #url = 'http://blog.sina.com.cn/s/blog_4701280b01000ce8.html'

    page  = urllib.request.urlopen(url)
    content1 = page.read()
    zcontent = content1.decode('utf_8')
    newcontent = zcontent[zcontent.find(r'<body>'):zcontent.find(r'</body>')]
    soup = BeautifulSoup(newcontent,"html.parser")
    textcontent = soup.find('div' ,id="sina_keyword_ad_area2").get_text()
    '''
    m=MyHTMLParser()
    m.feed(zcontent)
    m.close()
    page.close()
    #print (m.htmlcontent)
'''
    file2 = open (name + '.txt','w',encoding='utf_8')
    file2.write(textcontent)
    file2.close()

def getarticlelist():
    url='http://blog.sina.com.cn/s/articlelist_1191258123_0_1.html'
    url='http://blog.sina.com.cn/s/articlelist_1191258123_0_7.html'
    page = urllib.request.urlopen(url)
    content1 = page.read().decode('utf_8')
    title1 = content1.find(r'<a title="')
    href = content1.find(r'href="',title1)
    html = content1.find(r'html">',href)
    i = 0
    while href!=-1 and html!=-1 and i < 5:
        url1=content1[href+6:html+4]
        name=url1[-26:]
        i = i+1
        title1 = content1.find(r'<a title="',html)
        href = content1.find(r'href="',title1)
        html = content1.find(r'html">',href)
        downloadwebpage(url1,name)
    else:
        pass
    downloadwebpage(url1,name)

getarticlelist()
