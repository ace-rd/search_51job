import requests
from bs4 import BeautifulSoup
import pymysql


def page_parser(url):
	response = requests.get(url)
	response.encoding = response.apparent_encoding
	bs_obj = BeautifulSoup(response.text,'html.parser')
	return bs_obj


def get_links(bs_obj):
	job_titles = []
	job_links = []
	for links in bs_obj.find(class_ = 'dw_table').findAll('p', class_='t1 '):
	    job_titles.append(links.find('a')['title'])
	    job_links.append(links.find('a')['href'])
	return job_titles,job_links


def get_text(link):
	bs_obj = page_parser(link)
	txs = ""
	bms = bs_obj.find('div', class_="bmsg job_msg inbox").findAll('p',class_=False)
	for tx in bms:
		txs = txs + tx.text
	return txs

url_0 = 'https://search.51job.com/list/040000,000000,0000,00,9,99,python,2,'
url = url_0 + '1.html'
job_titles,job_links = get_links(page_parser(url))
for i in range(0,len(job_titles)):
    print(job_titles[i] + " : " + job_links[i])
    print(get_text(job_links[i]))
    print('-'*50)