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

NanoBlog does:

* take all posts in the source directory, and generate HTML files from
  them
* create an index page (consisting of a list of all posts, ordered by
  date)
* use your favorite editor to let you create/edit posts
* set the correct date(s) in newly created or edited posts
* upload your HTML files (and anything else in the html directory, so
  beware ;-) to your FTP server

NanoBlog does not:

* create directories for you
* have a "preview" option (point your browser to the generated .html
  file instead)
* let you mark posts as "private" (write your post in a different
  directory, then move it to the source directory when ready)
* keep track of which generated files have changed (i.e. it uploads
  everything, all the time)
* provide you with professional-looking HTML or CSS to start with
* provide you with a GUI or web interface (everything is done via the
  command line)

### Requirements ###

* Python 2.x
* [The Markdown library](https://pypi.python.org/pypi/Markdown/)

### How to use ###

...

