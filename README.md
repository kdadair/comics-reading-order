# comics-reading-order
A mediocre-yet-functional way to turn a list of Marvel issues into an HTML document of links to Marvel Unlimited, decently formatted.

First, you probably need to install [duckduckgo_search, credit to deedy5:](https://github.com/deedy5/duckduckgo_search)

```pip install -U duckduckgo_search```

Then, create a text file of the issues you want links for, in a format something like this, with series name, issue number, and year:

```
Dark Reign: New Nation #1 (2009)
Secret Warriors #1 (2009)
Secret Warriors #2 (2009)
Secret Warriors #3 (2009)
Secret Warriors #4 (2009)
Secret Warriors #5 (2009)
Secret Warriors #6 (2009)
Dark Reign: Fantastic Four #1 (2009)
Dark Reign: Fantastic Four #2 (2009)
Dark Reign: Fantastic Four #3 (2009)
Dark Reign: Fantastic Four #4 (2009)
Dark Reign: Fantastic Four #5 (2009)
Dark Reign: The Cabal #1 (2009)
```

Each of these lines ends up being its own duckduckgo search, with a ``` site:marvel.com/comics/issue/``` appended, so the more detail you include about the issue, the more likely you are to find the issue. The script assumes that the first result is right -- it's pretty dumb!

Just call from the command line, like so:

```python3 reading_order.py path/to/text/file.txt```

Doing so will produce a .html file in the current directory. It will overwrite the file if one exists in the directory.

Note: it's pretty slow, about a second per issue, because I have a ```sleep(1)``` in there, so as to not get rate-limited by either duckduckgo or Marvel, both of which happened to me in development.

Then, I typically serve that file with simpleHTTPserver:

```python3 -m http.server 8000```

<img src="https://user-images.githubusercontent.com/82833387/222652187-e552f765-2c8b-4fce-a12d-53d67e49b5d0.gif" width="400">
