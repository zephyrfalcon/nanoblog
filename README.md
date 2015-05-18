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

* take all posts in the source directory (containing Markdown and some
  metadata), and generate HTML files from them
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
* let you mark posts as "private" so they won't be built or uploaded (write your
  post in a different directory, then move it to the source directory when ready)
* have rich metadata for posts; no author, last date/time updated, tags,
  etc
* keep track of which generated files have changed (i.e. it uploads
  everything, all the time)
* provide you with professional-looking HTML or CSS to start with
* provide you with a GUI or web interface (everything is done via the
  command line)
* well-refactored source code (it was intended to get a blog going real
  quick)

### Requirements ###

* Python 2.x
* [The Markdown library](https://pypi.python.org/pypi/Markdown/)

### How to use ###

* "Install" NanoBlog by checking it out from the git repository, then
  put it somewhere in your user directory. It may be useful to create a
  globally accessible script that runs `python /path/to/nanoblog.py
  "$@"`.

* Create a directory for your blog, say `myblog`.

* Enter that directory and create subdirectories `source` and `html`.

* Copy `sample-template.html` from the NanoBlog source directory to your
  blog directory, and call it `template.html`. Do the same with
  `sample-config.txt` vs `config.txt`.

* Edit your new config file and template to your liking.

* When you want to write a new blog post, enter your blog directory and
  do `nanoblog edit foo`, where `foo` is the name of the new file
  containing the post. (`nanoblog` is assumed to be the name of the
  script created in step #1.) This will create a file `source/foo.txt`,
  and run your editor on it.

* When you want to edit an existing blog post, do the same: `nanoblog
  edit foo`. NanoBlog will not overwrite existing posts.

* When you want to generate HTML file, do `nanoblog build`.

* When you want to upload the contents of the `html` directory
  (including any non-HTML files you might have put there, like
  stylesheets etc) to your FTP server (as configured in `config.txt`),
  do `nanoblog upload`.

* That's pretty much it.

