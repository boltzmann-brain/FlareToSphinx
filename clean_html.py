from bs4 import BeautifulSoup
import sys

old_html = open(sys.argv[1], "r") #, encoding="utf-8")
old_data = old_html.read()
old_data = old_data.replace('&#160;', ' ') # replace non-breaking spaces as REST/Pandoc don't like them.

#for hrefs that don't begin with "http", replace ending "htm" with "html"
#Replacement code also accounts for links to headers within topics (that end with 'htm#Something')
#This preserves links within project, as Sphinx generates files with "html" extension, whereas Flare does 'htm'.
soup = BeautifulSoup(old_data, 'html.parser')
for a in soup.findAll('a', href=True):
	if ((a['href'][:4] != 'http') and (a['href'][-3:] == 'htm')):
		a['href'] += 'l'
	elif ((a['href'][:4] != 'http') and ('.htm#' in a['href'])):
		a['href'] = a['href'].replace('.htm', '.html')

new_file = open(sys.argv[1], "w")
new_file.write(str(soup))
new_file.close()

