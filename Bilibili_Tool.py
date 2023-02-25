import requests
import re

def get_recommends(bv):                                                       #得到推荐视频列表
    url = 'https://www.bilibili.com/video/' + bv
    headers = {
        'user-agent': 'xxxxxxxx'
    }
    resp = requests.get(url = url, headers = headers)
    obj1 = re.compile(r"bvid\"\:\"(?P<bv>.*?)\"", re.S)
    res = obj1.finditer(resp.text)
    recommend = []
    for i in res:
        recommend.append(i.group("bv"))
    recommend = list(set(recommend))
    recommend.remove(bv)
    return recommend

def get_title(bv):
    url = 'https://www.bilibili.com/video/' + bv
    resp = requests.get(url)
    obj = re.compile(r"<title data-vue-meta=\"true\">(?P<bv>.*?)\_哔哩哔哩\_", re.S)
    res = obj.finditer(resp.text)
    for i in res:
        return i.group("bv")

def judge(mid):
    if target_search(mid) != 0:
        return True
    return False

def target_search(mid):
    r = requests.get('https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?visitor_uid=0&host_uid=' + mid + '&offset_dynamic_id=0&need_top=1&platform=web')
    res = r.text
    return res.count('抽奖')


count = 0
target_searchs = []
print(' ')
for i in range(60):     #评论页数上限
    pages = i
    r = requests.get('https://api.bilibili.com/x/v2/reply/main?&jsonp=jsonp&next=' + str(pages) + '&type=1&oid=851427447&mode=3&plat=1&_=1647250934016')
    obj1 = re.compile(r"{\"mid\"\:\"(?P<mid>.*?)\",\"uname\"\:\"(?P<uname>.*?)\"\,\"sex.*?\"message\"\:\"(?P<reply>.*?)\"", re.S)
    res = obj1.finditer(r.text)
    for i in res:
        if judge(i.group("mid")):
            info = (i.group("reply") + '-----' + i.group("uname") + '-----' + i.group("mid") + '-----' + '该用户主页抽奖关键字数量为:' + str (target_search(i.group("mid"))))
            if info not in target_searchs:
                target_searchs.append(info)
                count += 1
    for i in target_searchs:
        print(i)
print('首页有抽奖信息的用户共有 ' + str(count) + '个')
