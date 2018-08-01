import requests
from bs4 import BeautifulSoup
import pymysql


def get_links(url):
	job_titles = []
	job_links = []
	response = requests.get(url)
	response.encoding = response.apparent_encoding
	bs_obj = BeautifulSoup(response.text,'html.parser')
	for links in bs_obj.find(class_ = 'dw_table').findAll('p', class_='t1 '):
	    job_titles.append(links.find('a')['title'])
	    job_links.append(links.find('a')['href'])
	return job_titles,job_links



url_0 = 'https://search.51job.com/list/040000,000000,0000,00,9,99,python,2,'
url = url_0 + '1.html'
job_titles,job_links = get_links(url)
for i in range(0,len(job_titles)):
    print(job_titles[i] + " : " + job_links[i])