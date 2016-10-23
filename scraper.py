import requests, re
import bs4

urlBase = "http://www-inst.eecs.berkeley.edu/~cs61a/fa15/"
r = requests.get(urlBase)

soup = bs4.BeautifulSoup(r.text, 'html.parser')

homework_links_raw = soup.find_all("a", string=re.compile("Homework"))

homework_links_filtered = list(set([homework_link["href"] for homework_link in homework_links_raw if re.compile("(lab/|hw/)").search(homework_link["href"])]))
#homework_links_filtered.remove('lab/lab00/')

homework_pages = [bs4.BeautifulSoup(requests.get(urlBase + homework_link).text, 'html.parser') for homework_link in homework_links_filtered]

for homework_page in homework_pages:
	block_children = homework_page.find("div", class_="col-md-9").child
	#homework_questions = homework_page.find_all("h3", class_="question")
	#print(homework_questions)


