import os.path
import re
import lxml.etree
import requests
# 使用session和服务器进行绘话
s = requests.Session()

old_url='https://sundan.com/gallery-145.html'
new_url='https://sundan.com/gallery-ajax_get_goods.html'
#请求头的搭建
headers={
    'Referer': 'https://sundan.com',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}
s.get(old_url, headers=headers, verify=False)
# 家电类的编号 int型
cat_id=145
# 页面 int型
page=1
# post的请求参数
data={
    'cat_id':145,
    'virtual_cat_id':'',
    'orderBy':'',
    'showtype':'grid',
    'city_id':524,
    'page':2
}
# 得到商品的大页面
html = s.post(new_url,data=data,headers=headers,verify=False).text
my_tree= lxml.etree.HTML(html)
# 提取该页面的连接
li_list = my_tree.xpath("//*[@class=\"gallery-grid\"]//ul//li//div[3]//a/@href")  # 全部商品大模块

# 循环每一个商品连接  开爬
print(li_list)
for li in li_list:
    new_url_link = "https://sundan.com" + li
    # 打开商品html
    new_html = requests.get(new_url_link, headers=headers, verify=False).text

    #正则提取价格标题
    myrearch=re.findall( r"var newHst = (.*)\'viewTime\'\:\+new Date()",new_html,re.DOTALL)
    # 空列表就进入下一次循环
    if myrearch == []:
        continue
    goodList=re.findall( r"\:\'(.*)\'\,",myrearch[0][0])
    # 空列表就进入下一次循环
    if goodList == []:
        continue

    img_url_list=[]
    # 判断商品价格
    if float(str(goodList[3].split('￥')[1]))<3000:
        title=goodList[1]
        img=goodList[2]
        print(img)
        price=goodList[3].split('￥')[1]
        # 得到商品信息
        info='价格：'+str(price)+"\n"+'标题：'+title
        # 查看价格
        print(goodList[3].split('￥')[1])
        # 抓取所有图片链接
        new_tree= lxml.etree.HTML(new_html)
        treeList=new_tree.xpath("//*[@id=\"product_album\"]//div[2]//div[2]/ul")
        for i in range(len(treeList)):
            img1=treeList[i].xpath('li[1]/div[2]/a/@href')
            img_url_list.append(img1)
            img2=treeList[i].xpath('li[2]/div[2]/a/@href')
            img_url_list.append(img2)
            img3 =treeList[i].xpath('li[3]/div[2]/a/@href')
            img_url_list.append(img3)
            img4 =treeList[i].xpath('li[4]/div[2]/a/@href')
            img_url_list.append(img4)
            img5 =treeList[i].xpath('li[5]/div[2]/a/@href')
            img_url_list.append(img5)
            img6 =treeList[i].xpath('li[6]/div[2]/a/@href')
            img_url_list.append(img6)
            img7 =treeList[0].xpath('li[7]/div[2]/a/@href')
            img_url_list.append(img7)

#存储商品的信息和图片
        # 标题去掉空格，防止找不到文件路径
        title1 = ''.join(title.split(' '))
        path=r"./sundan"+ str(cat_id) +"/" + title1 + "/img"
        # 判断文件夹是否存在，存在进入下一次循环
        if os.path.exists(path):
            continue

        os.makedirs("./sundan"+ str(cat_id) +"/" + title1 + "/img")
        with open("./sundan"+ str(cat_id) +"/" + title1 + "/info.txt", "w", encoding="utf-8") as mfile:
                mfile.write(info)

        for j in range(len(img_url_list)):
            #不为空则下载图片
            if img_url_list[j] != []:
                with open("./sundan"+ str(cat_id) +"/"+ title1 + "/img/" + str(j) + ".jpg", "wb") as mfile_img:
                        mfile_img.write(requests.get(img_url_list[j][0],verify=False).content)


