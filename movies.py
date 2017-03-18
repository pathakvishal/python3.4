from bs4 import BeautifulSoup
from robobrowser import RoboBrowser
import requests
import urllib.request

def get_movies(max_pages):
	page = 1
	while page <= max_pages:
		url = 'http://www.300mbfilms.co/tag/brip/page/1'
		source_code = requests.get(url)
		plain_text = source_code.text
		soup = BeautifulSoup(plain_text,'html.parser')
		for link in soup.findAll('h2',{'class':'title'}):
			title = link.string
			soup1 = BeautifulSoup(str(link), 'html.parser')
			movie_link = soup1.findAll('a')
			print(movie_link[0].get("href"))
			print(title)
			earn_url=get_earn_money_online_link(movie_link[0].get("href"))
			Dsource_code=enter_password(earn_url)
			download_links=get_download_links(Dsource_code)
			parse_links(download_links)# download movie automatically
		page += 1
'''
This function get the earn money online link
'''
def get_earn_money_online_link(url):
	source_code = requests.get(url)
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text,'html.parser')
	for link in soup.findAll('p',{'style':'text-align: center;'}):
		title = link.string
		if title == 'CLICK HERE TO Get links':
			soup1 = BeautifulSoup(str(link), 'html.parser')
			earn_link = soup1.findAll('a')
			print(earn_link[0].get("href"))
			return earn_link[0].get("href")

'''
This function enter password into earn money online and returns password protected(hidden) source code of the page.
'''
def enter_password(url):
	values = {'post_password':'300mbfilms','Submit':'Submit'}
	browser = RoboBrowser()
	browser.open(url)
	form = browser.get_form()
	form['post_password']='300mbfilms'
	browser.session.headers['Referer']=url
	response = browser.submit_form(form)
	#print(browser.parsed)
	return browser.parsed
'''
This function get the download links
'''
def get_download_links(source_code):
	soup = BeautifulSoup(str(source_code), 'html.parser')
	download_link = []
	#print(plain_text)
	for link in soup.findAll('a', {'rel': 'nofollow'}):
		mylinks=link.get("href")
		#print(mylinks)
		download_link.append(mylinks)
	return download_link

'''
To Do: Download movie automatically
'''
def parse_links(links):
	for link in links:
		str_link=str(link)
		list=str_link.split('=')
		name=list[1].split('.')
		if name[1] == 'solidfiles':
			print(list[1])
			browser=RoboBrowser()
			browser.open(list[1])
			form = browser.get_form()
			#print(form)
			browser.session.headers['Referer']=list[1]
			browser.submit_form(form)
			#print(browser.parsed)
			code = browser.parsed
			soup = BeautifulSoup(str(code), 'html.parser')
			for link in soup.findAll('a'):
				if link.string == 'click here':
					dl=link.get("href")
					dl_str=str(dl).split('/')
					print(dl_str[5]+"   Downloading...")
					urllib.request.urlretrieve(dl,dl_str[5])
				
			

'''
Argument: No. of pages of 300mbfilms you want download link for.
Warning: Only 720p and 1080p
'''
get_movies(1)
