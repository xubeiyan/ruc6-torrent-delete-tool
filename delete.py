#-*- coding:utf-8 -*-
# 使用requests库（url请求）
import requests
# 使用lxml库（解析爬到的内容）
from lxml import html
# 品知登录地址
pinzhi_bbs_login_url = 'http://bt.ruc6.edu.cn/b/member.php?mod=logging&action=login&loginsubmit=yes&frommessage&inajax=1'
pinzhi_bt_login_url = 'http://bt.ruc6.edu.cn/takelogin.php'

# 漫版板块ID
anime_forum_ids = '1600,1601,1602,1603,1604,1605,1606'

# 品知删种地址
pinzhi_list_to_delete_url = "http://bt.ruc6.edu.cn/app/listtorrent.php?t="
pinzhi_takedelete_url = "http://bt.ruc6.edu.cn/takedelete.php"

# 用户名和密码（这里需要你去填写）
username = '乙津梦'
password = 'abcde'

# 登入bbs和bt各需要的信息
bbs_login_post = {
	'username': username,
	'password': password,
	'quickforward':'yes',
	'handlekey':'ls'
}
bt_login_post = {
	'username': username,
	'password': password,
	'cookie_time': 86400,
	'submitbutton': '提 交'
}
# 向takelogin.php提交登录信息时必须Referer是http://bt.ruc6.edu.cn/login.php，不然他会认为你是错误请求让你登录
bt_login_headers = {
	'Referer': 'http://bt.ruc6.edu.cn/login.php'
}
# 删种请求data
delete_data = {
	'tid': '0',
	'reason': '死种 deleted by bot of ototsu yume',
	'selectreason': '',
	'uploaded': '',
	'ban_up_time': '0',
	'sendreasonpm': '1',
	'topicsubmit': '确定删除'
	
}
print u'---------------------------------------'.encode('gbk')
print u'  品知人大删种工具 ver0.0.1 by 乙津梦  '.encode('gbk')
print u'---------------------------------------'.encode('gbk')
# 使用Session
s = requests.Session()
bbs_login_request = s.post(pinzhi_bbs_login_url, bbs_login_post)
# print bbs_login_request.cookies
bt_login_request = s.post(pinzhi_bt_login_url, bt_login_post, headers=bt_login_headers, cookies=bbs_login_request.cookies)
# 该页面未指定编码，这个sb的requests库会指定为ISO-8859-1，所以要手动指定一下，下同
bbs_login_request.encoding = 'utf-8'
bt_login_request.encoding = 'utf-8'
# print bt_login_request.text.encode('gbk')

# 请求列表
r = requests.get(pinzhi_list_to_delete_url + anime_forum_ids)
r.encoding = 'utf-8' 

# 使用XPath截取适当的部分，这里是a href部分和td中的torrentlast部分
tree = html.fromstring(r.text)
links = tree.xpath('//a/@href')
last_date = tree.xpath('//td[@class="torrentlast"]/text()')
delete_links = []
for link in links:
	if link.find('delete.php') > 0:
		delete_links.append(link.split('=')[1])
		
# 输出即将删除的种子
print u'待删除的种子如下，请确认时间是否小于清理死种时间：'.encode('gbk')
#print delete_links
#print last_date
if (len(delete_links) == len(last_date)):
	for link in delete_links:
		print u'种子id:'.encode('gbk') + link + u' 最后活动时间:'.encode('gbk') + last_date[delete_links.index(link)]


length = len(delete_links)
input = raw_input(u'删除'.encode('gbk') + str(length) + u'个种子, 输入乙津梦喜欢说的一句话(hentaisandane,un,hentaisan)确认删除:'.encode('gbk'))

if input != 'hentaisandane,un,hentaisan':
	print '...'
	exit();
	
# 删除种子，分别向takedelete.php提交需要删除的种子id，返回
for tid in delete_links:
	delete_data['tid'] = tid
	delete_request = s.post(pinzhi_takedelete_url, delete_data, cookies = bt_login_request.cookies)
	delete_request.encoding = 'utf-8'
	tree = html.fromstring(delete_request.text)
	message = tree.xpath('//div[@id="message"]/h1/text()')
	print u'种子id:'.encode('gbk') + tid + ' ' + message[0]
	


