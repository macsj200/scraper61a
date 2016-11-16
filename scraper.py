import requests, re
import bs4
import types

#for sanity in case something goes wrong
def tree(root, branches=[]):
    for branch in branches:
        assert is_tree(branch), 'branches must be trees'
    return {'<root>': root, '<branches>': branches}

def root(tree):
    return tree['<root>']

def branches(tree):
    return tree['<branches>']

def is_tree(tree):
    if type(tree) != dict or '<root>' not in tree or '<branches>' not in tree:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True

def is_leaf(tree):
    return not branches(tree)

numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])

urlBase = "http://www-inst.eecs.berkeley.edu/~cs61a/fa15/"
r = requests.get(urlBase)

soup = bs4.BeautifulSoup(r.text, 'html.parser')

homework_links_raw = soup.find_all("a", string=re.compile("Homework|Lab"))

homework_links_filtered = list(set([homework_link["href"] for homework_link in homework_links_raw if re.compile("(lab/|hw/)").search(homework_link["href"])])) #lab/|
#homework_links_filtered.remove('lab/lab00/')

homework_pages = [bs4.BeautifulSoup(requests.get(urlBase + homework_link).text, 'html.parser') for homework_link in homework_links_filtered]

url = "http://www-inst.eecs.berkeley.edu/~cs61a/fa15/hw/hw05/"
r2 = requests.get(url)
homework_page = bs4.BeautifulSoup(r2.text, 'html.parser')

#gets the title of a page by finding the first h1 tag
def getTitle(page):
    titles = page.find_all("h1")
    return titles[0].text if len(titles) != 0 else "~ No Title"
    # for t in titles:
        # print("TITLE: ", t.text)


#iterates through all pages and outputs their values
def iterate(homework_page):
    # for homework_page in homework_pages:
    
    code_snippets = homework_page.find_all("pre")#homework_page.find("div", class_="col-md-9").child
    if code_snippets != None:
        print(">>>>>>>> ON PAGE:", getTitle(homework_page), "<<<<<<<<")

        print("\n---- BUILDING CODE ----\n")
        for snippet in code_snippets:
            # print(snippet.text + "\n\n")
            # execute the code in the pages to build it into the local scope
            if "python3" not in snippet.text: #and ("*** YOUR CODE HERE ***" in snippet.text or "_____" in snippet.text):
                try:

                    exec(snippet.text.replace('_____', '5')) #completely random
                except Exception as e:
                    print("Did nothing for this code snippet --> " + str(e))

        scope = dict(locals())
        print("\n---- LOCAL DOC TESTS FOR PAGE ----\n")
        for var in scope:
            # print the doctests for all the compiled functions from pervious part (if they exist)
            if (isinstance(scope[var], types.FunctionType)): #and scope[var].__doc__ != "*** YOUR CODE HERE ***"):
                if scope[var].__doc__ != None:
                    print(var + ": " + scope[var].__doc__ + "\n")
                else:
                    print(var + ": None\n")
	#homework_questions = homework_page.find_all("h3", class_="question")
	#print(homework_questions)

#this part gets rid of duplicates
homework_dict = {}
for page in homework_pages:
    homework_dict[getTitle(page)] = page
homework_pages = homework_dict.values()
#sort by title for convenience
homework_pages = sorted(homework_pages, key=getTitle)

#do the work
for page in homework_pages:
    iterate(page)

