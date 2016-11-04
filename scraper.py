import requests, re
import bs4
import types

urlBase = "http://www-inst.eecs.berkeley.edu/~cs61a/fa15/"
r = requests.get(urlBase)

soup = bs4.BeautifulSoup(r.text, 'html.parser')

homework_links_raw = soup.find_all("a", string=re.compile("Homework"))

homework_links_filtered = list(set([homework_link["href"] for homework_link in homework_links_raw if re.compile("(lab/|hw/)").search(homework_link["href"])]))
#homework_links_filtered.remove('lab/lab00/')

homework_pages = [bs4.BeautifulSoup(requests.get(urlBase + homework_link).text, 'html.parser') for homework_link in homework_links_filtered]

url = "http://www-inst.eecs.berkeley.edu/~cs61a/fa15/hw/hw01/"
r2 = requests.get(url)
homework_page = bs4.BeautifulSoup(r2.text, 'html.parser')

def iterate():
    # for homework_page in homework_pages:
    code_snippets = homework_page.find_all("pre")#homework_page.find("div", class_="col-md-9").child
    if code_snippets != None:

        print("\n---- BUILDING CODE ----\n")
        for snippet in code_snippets:
            # print(snippet.text + "\n\n")
            if "python3" not in snippet.text and ("*** YOUR CODE HERE ***" in snippet.text or "_____" in snippet.text):
                try:
                    exec(snippet.text.replace('_____', '5')) #completely random
                except SyntaxError as e:
                    print("Did nothing for this code snippet --> " + str(e))

        scope = dict(locals())
        print("\n---- LOCAL DOC TESTS FOR PAGE ----\n")
        for var in scope:
            # print(var); 
            if (isinstance(scope[var], types.FunctionType)): #and scope[var].__doc__ != "*** YOUR CODE HERE ***"):
                if scope[var].__doc__ != None:
                    print(var + ": " + scope[var].__doc__ + "\n")
                else:
                    print(var + ": None\n")
	#homework_questions = homework_page.find_all("h3", class_="question")
	#print(homework_questions)


iterate()