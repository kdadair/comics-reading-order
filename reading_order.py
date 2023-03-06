import os, requests, re, argparse
from duckduckgo_search import ddg
from bs4 import BeautifulSoup
from time import sleep

# grab argument containing arguments
parser = argparse.ArgumentParser()

parser.add_argument('--issues_path', type=str, help='Path to text file containing issues')
parser.add_argument('--doc_title', type=str, nargs='?', default='Reading List', help='Desired title of HTML page. Optional.')
parser.add_argument('--file_name', type=str, nargs='?', default='readinglist', help='Desired name of file. Optional.')
parser.add_argument('--styling', action='store_true', default=True, help='Apply some basic styling. Defaults to true.')
args = parser.parse_args()

path = os.path.expanduser(args.issues_path)
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
	
	if digital_comic_id:
		return f"<li><a href=https://read.marvel.com/#/book/{digital_comic_id}>{issue_name}</a></li>"
	else:
		return None

hyperlink_list = []

for issue in issues_list:

	# sleep every iteration of the loop, because both Marvel and DuckDuckGo will get mad at you for bombarding them
	sleep(1)
	print(issue)
	marvel_url = ddg(f"{issue} site:marvel.com/comics/issue/", max_results=1)[0]['href']
	print(marvel_url)

	issue_url = get_mu_url(marvel_url, issue)

	if issue_url:
		# add link to url list
		hyperlink_list.append(issue_url)

hyperlink_string = '\n'.join(hyperlink_list)

# optional styling, defaulted to on.
style = None
if args.styling:
	style = """<style>
	/* Modern layout */
	body {
		font-family: 'Roboto', sans-serif;
		margin: 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		min-height: 100vh;
		background-color: #f7f7f7;
	}
	
	main {
		flex: 1;
		padding: 24px;
	}
	
	h1 {
		margin-top: 0;
		margin-bottom: 16px;
		font-size: 36px;
		font-weight: 700;
		color: #333333;
	}
	
	ul {
		list-style-type: none;
		margin: 0;
		padding: 0;
	}
	
	li {
		margin-bottom: 16px;
	}
	
	a {
		color: #1a0dab;
		text-decoration: none;
		border-bottom: 1px solid #1a0dab;
	}
	
	a:hover {
		background-color: #f2f2f2;
		border-bottom: none;
	}
	</style>"""


title = args.doc_title

#create html document
reading_list_content = f"""
<!DOCTYPE html>
<html lang="pl">
  <head>
	<meta charset="utf-8" />
	<title>{title}</title>
	{style}
  </head>
  <body>
	<main>
	  <h1>{title}</h1>
		<ul>
		{hyperlink_string}
		</ul>
	</main>
  </body>
</html>
"""

filename = args.file_name

# write to file, overwriting if exists
f = open(f"{filename}.html", "w")
f.write(reading_list_content)
f.close()