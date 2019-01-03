#!/home/tq/mywork/Wechat/bin/python3
# -*- coding: utf-8 -*-
from wxpy import *
from wxpy import get_wechat_logger
import re, os
import yagmail
yag = yagmail.SMTP( user="123@163.com", password="123", host='smtp.163.com')
contents = ['kindle attachments test']
bot = Bot(cache_path=True,console_qr = True)
bot.enable_puid('wxpy_puid.pkl')
tq = bot.friends().search(puid='33ed3109')[0]
byp = bot.friends().search(puid='d37e829b')[0]
booksrc_dir = '/home/tq/mywork/Wechat/baiduyun/download/book'
reStr_search = re.compile('search')
reStr_send = re.compile('send')
reStr_email = re.compile('^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$')
files_list = []
for root, dirs, files in os.walk(booksrc_dir):
    for i in files:
        sfile = os.path.join(root, i)
        files_list.append(sfile)

#@bot.register()
#def just_print(msg):
#    print(msg)
@bot.register([tq,byp], TEXT)
def auto_reply(msg):
    # 搜索资源
    if reStr_search.match(msg.text) is not None:
        booklist = []
        global book_sfile
        global booklist_dict
        booklist_dict = {}
        key_word = msg.text.split(' ')[1]
        if len(msg.text.split(' ')) > 2:
            return '一次只可以搜索一本书的资源，不要贪心哦。\n回复：“search 书名” 来查找资源'
        else:
            print_f = ''
            for i in files_list:
                book_name = os.path.basename(i)
                r = re.search(key_word, book_name)
                if r is not None:
                    booklist.append(i)
                    #book_name = os.path.basename(i)
                    #book_sfile = i
            booklist_len = len(booklist)
            if len(booklist) == 0:
                return 'sorry, no resourse found'
            else:
                for j in range(len(booklist)):
                    booklist_names = os.path.basename(booklist[j])
                    print_f = print_f + str(j+1) + '.' + booklist_names + '\n'
                    booklist_dict[str(j+1)] = booklist[j]
                print_f = print_f + '回复：“send 序号 email” 来获取资源'
                return print_f
            #return booklist_dict
    if reStr_send.match(msg.text) is not None:
        if len(msg.text.split(' ')) == 3 and msg.text.split(' ')[1].isdigit()==True:
            email = msg.text.split(' ')[2]
            book_num = msg.text.split(' ')[1]
            if reStr_email.match(email) is not None and int(book_num) < len(booklist_dict):
                contents = [booklist_dict[book_num]]
                book_name = os.path.basename(booklist_dict[book_num])
                msg.sender.send('发送中，请稍后...')
                yag.send(email, 'This mail come from yagmail', contents)
                return '{0} has sent to email {1}'.format(book_name, email)
            else:
                return 'email格式或序号有误\n回复：“send 序号 email” 来获取资源'
        else:
            return '格式输入有误\n回复：“send 序号 email” 来获取资源'
    else:
        return '收到消息: {} ({})\n回复：“search 书名” 查找资源'.format(msg.text, msg.type)

embed()
#bot.join()

# 获得一个专用 Logger
# 当不设置 `receiver` 时，会将日志发送到随后扫码登陆的微信的"文件传输助手"
#logger = get_wechat_logger(receiver='wxpy.pkl')

# 发送警告
#logger.warning('这是一条 WARNING 等级的日志，你收到了吗？')
