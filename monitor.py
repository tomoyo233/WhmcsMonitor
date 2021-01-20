import time
from urllib.parse import quote
import requests

header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
# 修改字符串为监控地址,由于默认语言的不同，可以通过网址追加&language=english进行英语显示
url = 'https://www.anlancloud.com/cart.php?a=add&pid=1&language=english'
# 修改字符串为whmcs默认语言的无货显示字符,英语:'Out of Stock' 
outstock = 'Out of Stock'
#在有货时继续进行监控 True or False
continuous = True
# 监控时间间隔
sleep = 300
# TG机器人配置
bottoken = ''
chatid = ''


def tg_bot(bottoken, chatid, url):
    text = '您关注的商品上货了\n购买地址为:{}'.format(url)
    text = quote(text)
    path = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(bottoken, chatid, text)
    requests.get(path)


while True:
    response = requests.get(url=url, headers=header)
    if outstock.encode('UTF-8') in response.content:
        print('现在时间：{t}\n商品地址：{u}\n状态：无货\n将在{s}秒后进行下一次检查'.format(t=time.strftime('%H:%M:%S'), s=sleep,u=url))
        print("*" * 30)
        time.sleep(sleep)
    else:
        print('上货了!!!买买买!!!')
        print('现在时间：{t}\n商品地址：{u}\n状态：有货'.format(t=time.strftime('%H:%M:%S'),u=url))
        print("*" * 30)
        tg_bot(bottoken, chatid, url)
        if continuous:
            print('商品有货，程序将进行一小时的休眠')
            time.sleep(3600)
        else:
            print('程序结束')
            break
