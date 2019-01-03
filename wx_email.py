#!/home/tq/mywork/Wechat/bin/python3
# -*- coding: utf-8 -*-
from wxpy import *
from wxpy import get_wechat_logger
import re, os
import yagmail
yag = yagmail.SMTP( user="123@163.com", password="123", host='smtp.163.com')
contents = ['kindle attachments test']
bot = Bot(cache_path=True,console_qr = True)
bot.enable_puid()
my_friend = bot.friends().search('tq')[0]
byp = bot.friends().search('咕噜米')[0]
booksrc_dir = '/home/tq/mywork/Wechat/baiduyun/download/book'
reStr_search = re.compile('search')
reStr_send = re.compile('send')
files_list = []
for root, dirs, files in os.walk(booksrc_dir):
    for i in files:
        sfile = os.path.join(root, i)
        files_list.append(sfile)

#@bot.register()
#def just_print(msg):
#    print(msg)
@bot.register([my_friend,byp], TEXT)
def auto_reply(msg):
    booklist = []
    global book_sfile
    global booklist_dict
    # 回复消息内容和类型并发送邮件
    if msg.text == 'sendtq':
        yag.send('123@126.com', 'This mail come from yagmail', contents)
        yag.close()
        return '收到消息: {} ({}),and send the email'.format(msg.text, msg.type)
    if reStr_search.match(msg.text) is not None:
        booklist_dict = {}
        key_word = msg.text.split(' ')[1]
        print_f = ''
        for i in files_list:
            r = re.search(key_word, i)
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
        email = msg.text.split(' ')[2]
        book_num = msg.text.split(' ')[1]
        contents = [booklist_dict[book_num]]
        book_name = os.path.basename(booklist_dict[book_num])
        yag.send(email, 'This mail come from yagmail', contents)
        return '{0} has sent to email {1}'.format(book_name, email)
    else:
        return '收到消息: {} ({})'.format(msg.text, msg.type)

#embed()
bot.join()
