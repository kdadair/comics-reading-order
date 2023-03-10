import os, requests, re, argparse
from duckduckgo_search import ddg
from bs4 import BeautifulSoup
from time import sleep

# grab argument containing arguments
parser = argparse.ArgumentParser()

parser.add_argument('--issues_path', type=str, help='Path to text file containing issues')
parser.add_argument('--doc_title', type=str, nargs='?', default='Reading List', help='Desired title of HTML page. Optional.')
parser.add_argument('--file_name', type=str, nargs='?', default='readinglist', help='Desired name of file. Optional.')
parser.add_argument('--no_styling', action='store_true', default=False, help='Removes basic styling. Defaults to False.')
parser.add_argument('--verbose', action='store_true', default=False, help='Print logging. Defaults to False.')
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

def get_mu_hyperlink(issue_name):

	if issue_name:
		# sleep every iteration of the loop, because both Marvel and DuckDuckGo will get mad at you for bombarding them
		sleep(1)
		print(issue_name)
		search_string = f"{issue_name} site:marvel.com/comics/issue/"
		
		if args.verbose:
			print(search_string)
		
		ddg_results = ddg(search_string, max_results=10)

		# this stuff now breaks if you don't use the blessed format of BOOK #NUMBER (YEAR)
		book_words = [w.lower().replace('.', '') for w in issue_name.split(" ")[:-2]]
		issue_no = issue_name.split(" ")[-2][1:]
		year = issue_name.split(" ")[-1][1:-1]

		# now we assume failure if the below "algorithm" fails
		comic_url = None

		# marvel gets funky with issue zero, so hope for the best with the first result
		if issue_no == "0":
			comic_url = ddg_results[0]['href']
		else: # loop over the results and look for one with matching year and issue number
			for result in ddg_results:
				if args.verbose:
					print(result['href'])
				
				# get last bit of URL, and get the issue, year, and title out of it
				mu_slug = result['href'].split("/")[-1]
				mu_book_words = mu_slug.split('_')[:-2]
				mu_issue_no = mu_slug.split('_')[-1]
				mu_year = mu_slug.split('_')[-2]

				if issue_no == mu_issue_no and year == mu_year:
					for book_word in book_words:
						if book_word in mu_book_words:
							comic_url = result['href']
							break
					break
		
		digital_comic_id = None
		if comic_url:
			print(comic_url)

			response = requests.get(comic_url)
			soup = BeautifulSoup(response.content, 'html.parser')

			# loop through all <script> tags in the HTML page
			for script in soup.find_all('script'):
				script_text = str(script)

				# search for the digital comic id pattern in the script text
				match = re.search(r'digital_comic_id: "(\d+)"', script_text)

				# if the pattern is found, extract the digital comic id and break out of the loop
				if match:
					digital_comic_id = match.group(1)
					break
		
		if digital_comic_id:
			return f"<a href=https://read.marvel.com/#/book/{digital_comic_id}>{issue_name}</a><br>"
		else:
			return f"{issue_name} (URL not found)<br>"
	else:
		return '</p>\n<p>'

hyperlink_list = []

for issue in issues_list:
	issue_hyperlink = get_mu_hyperlink(issue)

	if issue_hyperlink:
		# add link to url list
		hyperlink_list.append(issue_hyperlink)

hyperlink_string = '\n'.join(hyperlink_list)

# optional styling, defaulted to on.
style = ""
if not args.no_styling:
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
		padding: 36px;
	}
	
	h1 {
		margin-top: 0;
		margin-bottom: 16px;
		font-size: 36px;
		font-weight: 700;
		color: #333333;
	}
	
	a {
		color: #1a0dab;
		text-decoration: none;
		border-bottom: 1px solid #1a0dab;
	}

	br {
		display: block;
		margin: 5px 0;
		content: " ";
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
	  	<p>
		{hyperlink_string}
		</p>
	</main>
  </body>
</html>
"""

filename = args.file_name

# write to file, overwriting if exists
f = open(f"{filename}.html", "w")
f.write(reading_list_content)
f.close()