## nanoblog.py ##

A harshly minimalistic blogging tool.

A blog (or website in general) must consist of the following:

A directory containing:

* A file `config.txt` containing the website's info (this includes
  title, description, default author (maybe), FTP upload credentials)
* A file `template.html` containing HTML for each page
* A directory `source` containing source files (one for each .html file
  to be produced)
* A directory `html` where generated .html files will be put; anything
  else that must be uploaded should be put here as well

### Requirements ###

* Python 2.x 
* [The Markdown library](https://pypi.python.org/pypi/Markdown/)

