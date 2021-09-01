# -*- coding: UTF-8 -*-
import  requests
from lxml import etree
import sys
import re
import os
import json
from html.parser import HTMLParser
import html

def cha(l,n,headers):

    cont=requests.get(l,headers=headers).content
    dot=etree.HTML(cont.decode("utf-8","ignore").encode("utf-8","ignore").decode('utf-8'))
    intex=etree.tostring(dot[1][5],encoding="utf-8").decode()
    inner=re.findall(r'\"content\"\:\".*?\",\"firstImage\"\:',intex)
    inner=re.sub('"content":"','',inner[0])
    inner=re.sub('","firstImage":','',inner)
    html_data = html.unescape('<div id="textinf">'+inner+'</div>')
    fi=etree.HTML(html_data.encode("utf-8","ignore").decode('utf-8'))
    inner=fi.xpath('//p/text()')

    title=re.findall(r'\"title\"\:\".*?\",\"type\"\:',intex)
    title=re.sub('"title":"','',title[0])
    title=re.sub('","type":','',title)

    aut=re.findall(r'\"blogNickName\"\:\".*?\",\"bigAvaImg\"',intex)
    aut=re.sub('"blogNickName":"','',aut[0])
    aut=re.sub('","bigAvaImg"','',aut)
    title=title+'-'+aut

    if inner==[] or title==[]:
        print('default')
    else:
        title=str(n).zfill(3)+' '+title
        title=ti=re.sub('/', '_', title)
        title=re.sub(r'\\', '_', title)
        title=re.sub('\|', '_', title)
        title=re.sub('\*','',title)
        title=re.sub('&','&amp;',title)
        print(title)
        fo=open(title+'.txt','w',encoding='utf-8')
        fo.write(title+'\n')
        for l in inner:
            fo.write(l.strip()+'\n')
        fo.close()

def chapters(l,n,headers):
    
    cont=requests.get(l,headers=headers).content
    dot=etree.HTML(cont.decode("utf-8","ignore").encode("utf-8","ignore").decode('utf-8'))
    intex=etree.tostring(dot[1][5],encoding="utf-8").decode()
    inner=re.findall(r'\"content\"\:\".*?\",\"firstImage\"\:',intex)
    inner=re.sub('"content":"','',inner[0])
    inner=re.sub('","firstImage":','',inner)
    html_data = html.unescape('<div id="textinf">'+inner+'</div>')
    fi=etree.HTML(html_data.encode("utf-8","ignore").decode('utf-8'))
    inner=etree.tostring(fi.xpath('//div[@id="textinf"]')[0]).decode('utf-8')
    inner=re.sub(r'\\n','\n',inner)
    inner=re.sub('\"\\\&quot;','\"',inner)
    inner=re.sub('\\\&quot;\"','\"',inner)

    title=re.findall(r'\"title\"\:\".*?\",\"type\"\:',intex)
    title=re.sub('"title":"','',title[0])
    title=re.sub('","type":','',title)
    
    aut=re.findall(r'\"blogNickName\"\:\".*?\",\"bigAvaImg\"',intex)
    aut=re.sub('"blogNickName":"','',aut[0])
    aut=re.sub('","bigAvaImg"','',aut)
    
    if inner==[] or title==[]:
        print('default')
    else:
        #intex=re.sub(r'<h5.*?>','<h2><a href="'+l+'">',intex)
        #intex=re.sub('</h5>','</a></h2>',intex)
        intex='<h2><a href="'+l+'">'+title+'</a></h2>'+inner
        title=title+'-'+aut
        title=str(n).zfill(3)+' '+title
        title=ti=re.sub('/', '_', title)
        title=re.sub(r'\\', '_', title)
        title=re.sub('\|', '_', title)
        title=re.sub('\*','',title)
        title=re.sub('&','&amp;',title)
        title=re.sub('[\/:*?"<>|]','_',title)
        title=re.sub('\n','_',title)
        print(title)

        fo=open(title+'.xhtml','w',encoding='utf-8')
        fo.write('''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
  <title></title>
  <link href="../Styles/stylesheet.css" type="text/css" rel="stylesheet"/>
</head>
<body>''')
        fo.write(intex)
        fo.write('</body></html>')
        fo.close()

def textF(l,n,headers,fo):
    cont=requests.get(l,headers=headers).content
    dot=etree.HTML(cont.decode("utf-8","ignore").encode("utf-8","ignore").decode('utf-8'))
    intex=etree.tostring(dot[1][5],encoding="utf-8").decode()
    inner=re.findall(r'\"content\"\:\".*?\",\"firstImage\"\:',intex)
    inner=re.sub('"content":"','',inner[0])
    inner=re.sub('","firstImage":','',inner)
    html_data = html.unescape('<div id="textinf">'+inner+'</div>')
    fi=etree.HTML(html_data.encode("utf-8","ignore").decode('utf-8'))
    inner=fi.xpath('//p/text()')

    title=re.findall(r'\"title\"\:\".*?\",\"type\"\:',intex)
    title=re.sub('"title":"','',title[0])
    title=re.sub('","type":','',title)

    aut=re.findall(r'\"blogNickName\"\:\".*?\",\"bigAvaImg\"',intex)
    aut=re.sub('"blogNickName":"','',aut[0])
    aut=re.sub('","bigAvaImg"','',aut)
    title=title+'-'+aut
    
    print(title)
    fo.write(title+'、\r\n')
    fo.write('<a>'+l+'</a>\r\n')
    for l in inner:
        fo.write(l.strip()+'\n')

#获取一些LOFTER页面所有网址
'''
urls=[]
links=[]
urls.append('https://i.lofter.com/search?q=o')#可添加多个页面
for url in urls:
    cont=requests.get(url,headers=headerPC).content
    dot=etree.HTML(cont)
    
    #作者主页、搜索页
    links+=dot.xpath('//h2/a/@href')
    
    #归档页
    links+=dot.xpath('//li/a/@href')
    
    for i in links:
        print(i)
'''

links=[]
#手机ua
headers={'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36'}
#电脑ua
headerPC={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}

ti=input("\r\n请输入文章名：")
fo=open(ti+'.txt','w',encoding='utf-8')
path=os.getcwd()
if os.path.exists(ti):
    os.chdir(ti)
else:
    os.mkdir(ti)
    os.chdir(ti)
while(1):
    print("\r\n请输入网址：")
    i=input()
    while i.strip()!='':
        links.append(i)
        i=input()
    links.reverse()
    for i in range(len(links)):
        #cha(links[i],i,headers)#每一个网址一个txt文件
        chapters(links[i],i,headers)#便于制作epub
        #textF(links[i],i,headers,fo)#将所有txt合并在一个文件里
    print('\r\n所有章节下载完成！')
os.chdir(path)
