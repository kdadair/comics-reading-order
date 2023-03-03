import sys, os
from duckduckgo_search import ddg
import requests
from time import sleep

path = sys.argv[1]
issues_text = open(path).read()


# issues_text = """Secret Warriors #1 (2009)
# Secret Warriors #2 (2009)
# Secret Warriors #3 (2009)
# Secret Warriors #4 (2009)
# Secret Warriors #5 (2009)
# Secret Warriors #6 (2009)"""

issues_list = issues_text.split("\n")

reading_list_content = """
<!DOCTYPE html>
<html lang="pl">
  <head>
	<meta charset="utf-8" />
	<title>Reading List</title>
  </head>
  <body>
	<h1>Reading List</h1>\n"""

for issue in issues_list:
	sleep(1)
	print(issue)
	marvel_url = ddg(issue + " site:marvel.com/comics/issue/", max_results=1)[0]['href']
	print(marvel_url)

	marvel_text = requests.get(marvel_url).text

	start_index = marvel_text.find('digital_comic_id:')

	substring = marvel_text[start_index:start_index+50]
	start_num = substring.find('"')
	end_num = substring.find(',')

	issue_id = substring[start_num+1:end_num-1]

	reading_list_content += '<p><a href="https://read.marvel.com/#/book/' +issue_id + '">' + issue + '</a></p>\n'
	
reading_list_content += """
  </body>
</html>
"""

f = open("readinglist.html", "w")
f.write(reading_list_content)
f.close()