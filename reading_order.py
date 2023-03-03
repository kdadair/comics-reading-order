import sys, requests
from duckduckgo_search import ddg
from time import sleep

# grab argument containing path to text file
path = sys.argv[1]
issues_text = open(path).read()

# left this here for debugging and as a hint for how to format the text file
# issues_text = """Secret Warriors #1 (2009)
# Secret Warriors #2 (2009)
# Secret Warriors #3 (2009)
# Secret Warriors #4 (2009)
# Secret Warriors #5 (2009)
# Secret Warriors #6 (2009)"""

issues_list = issues_text.split("\n")

#instantiating top of HTML document
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

	# sleep every iteration of the loop, because both Marvel and DuckDuckGo will get mad at you for bomarding them
	sleep(1)
	print(issue)
	marvel_url = ddg(issue + " site:marvel.com/comics/issue/", max_results=1)[0]['href']
	print(marvel_url)

	marvel_text = requests.get(marvel_url).text

	# look for the javascript that has the digital comic id, which we use to build the link into Marvel Unlimited
	start_index = marvel_text.find('digital_comic_id:')
	substring = marvel_text[start_index:start_index+50]

	# get down to just the id, there's probably a better way of doing this
	start_num = substring.find('"')
	end_num = substring.find(',')
	issue_id = substring[start_num+1:end_num-1]

	# add link to document
	reading_list_content += '<p><a href="https://read.marvel.com/#/book/' +issue_id + '">' + issue + '</a></p>\n'

# finish html doc
reading_list_content += """
  </body>
</html>
"""

# write to file, overwriting if exists
f = open("readinglist.html", "w")
f.write(reading_list_content)
f.close()