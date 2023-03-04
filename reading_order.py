import sys, requests, re
from duckduckgo_search import ddg
from bs4 import BeautifulSoup
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

def get_mu_url(comic_url, issue_name):
	response = requests.get(comic_url)
	soup = BeautifulSoup(response.content, 'html.parser')

	# loop through all <script> tags in the HTML page
	for script in soup.find_all('script'):
		script_text = str(script)

		digital_comic_id = ""

		# search for the digital comic id pattern in the script text
		match = re.search(r'digital_comic_id: "(\d+)"', script_text)

		# if the pattern is found, extract the digital comic id and break out of the loop
		if match:
			digital_comic_id = match.group(1)
			break
		else:
			return None

	return f"<a href=https://read.marvel.com/#/book/{digital_comic_id}>{issue_name}</a>"

hyperlink_list = []

for issue in issues_list:

	# sleep every iteration of the loop, because both Marvel and DuckDuckGo will get mad at you for bombarding them
	sleep(1)
	print(issue)
	marvel_url = ddg(f"{issue} site:marvel.com/comics/issue/", max_results=1)[0]['href']
	print(marvel_url)

	issue_url = get_mu_url(marvel_url)

	# add link to url list
	hyperlink_list.append(issue_url)

hyperlink_string = '\n'.join(hyperlink_list)

#create html document
reading_list_content = f"""
<!DOCTYPE html>
<html lang="pl">
  <head>
	<meta charset="utf-8" />
	<title>Reading List</title>
  </head>
  <body>
	<h1>Reading List</h1>\n
	{hyperlink_string}
  </body>
</html>
"""

# write to file, overwriting if exists
f = open("readinglist.html", "w")
f.write(reading_list_content)
f.close()