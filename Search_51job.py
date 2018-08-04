import requests
from bs4 import BeautifulSoup
import pymysql


def page_parser(url):
	response = requests.get(url)
	response.encoding = response.apparent_encoding
	bs_obj = BeautifulSoup(response.text,'html.parser')
	return bs_obj


def get_info(bs_obj):
	job_titles = []
	job_ttllnk = []
	job_company = []
	job_cpnlnk = []
	job_area = []
	for links in bs_obj.find(class_ = 'dw_table').findAll('p', class_='t1 '):
	    job_titles.append(links.find('a')['title'])
	    job_ttllnk.append(links.find('a')['href'])
	    job_company.append(links.parent.find(class_='t2').find('a')['title'])
	    job_cpnlnk.append(links.parent.find(class_='t2').find('a')['href'])
	    job_area.append(links.parent.find(class_='t3').text)
	return job_titles,job_ttllnk, job_company, job_cpnlnk, job_area


def get_text(link):
	bs_obj = page_parser(link)
	txs = ""
	bms = bs_obj.find('div', class_="bmsg job_msg inbox").findAll('p',class_=False)
	for tx in bms:
		txs = txs + tx.text
	return txs

def create_table():
	sql = """CREATE TABLE `jobs` (
		`id` int(10) NOT NULL AUTO_INCREMENT,
		`title` char(100) NOT NULL,
		`titlelink` char(200) DEFAULT NULL,
		`conpany` char(100) DEFAULT NULL,
		`conpanylink` char(200) DEFAULT NULL,
		`area` char(20) DEFAULT NULL,
		`text` varchar(2000) DEFAULT NULL,
		PRIMARY KEY (`id`)
		) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
	cursor.execute(sql)
	print("Created table Successfull.")

def insert_data(job_titles, job_ttllnk, job_company, job_cpnlnk, job_area,job_texts):
	sql = "INSERT INTO jobs(`title`, `titlelink`, `conpany`, `conpanylink`, \
	    	`area`, `text`) VALUES ('%s', '%s','%s','%s','%s','%s')" \
	    	%(job_titles, job_ttllnk, job_company, job_cpnlnk, job_area, job_texts)
	try:
	    cursor.execute(sql)
	    conn.commit()
	    print(job_titles + " --- 已添加")
	except:
	    conn.rollback()
	    print(job_titles + " 发生错误，未添加")


url_0 = 'https://search.51job.com/list/040000,000000,0000,00,9,99,python,2,'
url = url_0 + '1.html'
job_titles, job_ttllnk, job_company, job_cpnlnk, job_area = get_info(page_parser(url))
user = input("please input your mysql username:")
psw = input("please input your mysql password:")

conn = pymysql.connect("localhost",user, psw ,"scraping")
cursor = conn.cursor()

for i in range(0,len(job_titles)):
	job_texts = get_text(job_ttllnk[i])
	# insert_data(job_titles[i], job_ttllnk[i], job_company[i], job_cpnlnk[i], job_area[i], job_texts)
	print(job_titles[i] + "(" + job_area[i] + ") : " + job_ttllnk[i])
	print(job_company[i] + " : " + job_cpnlnk[i])
	print(get_text(job_ttllnk[i]))
	print('-'*50)

conn.close()














