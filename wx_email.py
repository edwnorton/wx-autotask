#!/home/tq/mywork/Wechat/bin/python3
# -*- coding: utf-8 -*-
from wxpy import *
from wxpy import get_wechat_logger
import re, os, sys
import time
from datetime import datetime
import yagmail
import functools
import django

# 引用django的model模块
sys.path.insert(0, '/home/tq/py_env/django/mysite')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
from polls.models import BookList

# 邮件功能
yag = yagmail.SMTP( user="@163.com", password="", host='smtp.163.com')
contents = ['kindle attachments test']

# 生成微信对象
bot = Bot(cache_path=True,console_qr = True)
bot.enable_puid('wxpy_puid.pkl')
tq = bot.friends().search(puid='33ed3109')[0]
byp = bot.friends().search(puid='d37e829b')[0]
cj = bot.friends().search(puid='df441588')[0]

booksrc_dir = '/home/tq/mywork/Wechat/baiduyun/download/book'
reStr_search = re.compile('search')
reStr_send = re.compile('send')
reStr_email = re.compile('^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$')
files_list = []
time_period = 10

def period_calculate():
    """
    时间调用周期生成器
    """
    global time_period
    call_after = 0
    while True:
        call_before = time.time()
        yield call_after
        time_period = time.time() - call_before
    return

r = period_calculate() # 调用时间周期生成器

def calculate_period(func):
    """
    函数调用时间计算装饰器
    """
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        next(r)
        print('time_period:{0}'.format(time_period))
        return func(*args, **kw)
    return wrapper

@calculate_period
def func_test():
    return time_period

@bot.register([tq, byp, cj], TEXT)
def auto_reply(msg):
    if func_test()<5:
        return '调用检测...你太快了，五秒后重试'
    if reStr_search.match(msg.text) is not None:
        booklist_info = [] 
        booklist = []
        global book_sfile
        global booklist_location
        global booklist_dict
        booklist_dict = {}
        key_word = msg.text.split(' ')[1]
        if len(msg.text.split(' ')) > 2:
            return '一次只可以搜索一本书的资源，不要贪心哦。\n回复：“search 书名” 来查找资源'
        else:
            a = BookList.objects.filter(bookname__icontains=key_word)
            print_f = ''
            if a.exists():
                booklist_info = [(i.bookname, i.location, i.path) for i in a]
                booklist = [i[0] for i in booklist_info]
                booklist_location= [i[1] for i in booklist_info]
                booklist_len = len(booklist)
                for j in range(len(booklist)):
                    booklist_names = os.path.basename(booklist[j])
                    print_f = print_f + str(j+1) + '.' + booklist_names + '\n'
                    booklist_dict[str(j+1)] = os.path.join(booklist_info[j][2],booklist_info[j][0])
                print_f = print_f + '回复：“send 序号 email” 来获取资源'
                return print_f
            else:
                return 'sorry, no resourse found,请尝试换一个关键字查找'
    if reStr_send.match(msg.text) is not None:
        if len(msg.text.split(' ')) == 3 and msg.text.split(' ')[1].isdigit()==True:
            email = msg.text.split(' ')[2]
            book_num = msg.text.split(' ')[1]
            if reStr_email.match(email) is not None and int(book_num)-1 < len(booklist_dict):
                if booklist_location[int(book_num)-1] == '1':
                    contents = [booklist_dict[book_num]]
                    book_name = os.path.basename(booklist_dict[book_num])
                    msg.sender.send('发送中，请稍后...')
                    yag.send(email, 'This mail come from yagmail', contents)
                    return '{0} has sent to email {1}'.format(book_name, email)
                if booklist_location[int(book_num)-1] == '2':
                    book_name = os.path.basename(booklist_dict[book_num])
                    return '{0} 资源马上更新，敬请期待...'.format(book_name)
            else:
                return 'email格式或序号有误\n回复：“send 序号 email” 来获取资源'
        else:
            return '格式输入有误\n回复：“send 序号 email” 来获取资源'
    else:
        return '收到消息: {} ({})\n回复：“search 书名” 查找资源'.format(msg.text, msg.type)

embed()
#bot.join()

