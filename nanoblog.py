#!/usr/bin/env python3 nanoblog.py

import codecs
import datetime
import ftplib
import os
import sys
import io 
import markdown

__usage__ = """\
nanoblog.py command [args...]

Commands:
    build             Generate HTML files from source.
    upload            Upload contents of HTML directory to server.
    edit <filename>   Create or edit the given post.
    list              Show all existing posts.

"""

EXTENSIONS = ["markdown.extensions.tables"]

class NanoBlog:

    def __init__(self, dir):
        self.dir = os.path.abspath(dir)
        print("NanoBlog running in:", self.dir)
        self.config = self._read_config()
        self.template = self._read_template()

    def _read_config(self):
        config = {}
        path = os.path.join(self.dir, "config.txt")
        with codecs.open(path, "r", 'utf-8') as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip() # remove trailing \n and such
            if not line.strip(): continue # empty
            name, value = line.split('=', 1)
            config[name] = value
        return config

    def _read_template(self):
        path = os.path.join(self.dir, "template.html")
        data = open(path, "r").read()
        return data

    def read_source_file(self, name):
        if not name.endswith(".txt"):
            name = name + ".txt"
        path = os.path.join(self.dir, name)
        with codecs.open(path, "r", "utf-8") as f:
            lines = f.readlines() # keep trailing "\n"
        meta = {}
        cutoff = 0
        for idx, line in enumerate(lines):
            line = line.rstrip()
            if line == "---":
                cutoff = idx
                break
            if not line.strip(): continue
            if not "=" in line: continue
            name, value = line.split('=', 1)
            meta[name] = value
        data = ''.join(lines[cutoff+1:])
        return (meta, data)

    def cmd_list(self):
        path = os.path.join(self.dir, "source")
        filenames = [fn for fn in os.listdir(path) if fn.endswith(".txt")]
        for fn in filenames:
            full_path = os.path.join(path, fn)
            meta, _ = self.read_source_file(full_path)
            print(fn, "\t::", meta['created'], "::", meta['title'])
        print("%d file(s)" % len(filenames))

    def cmd_build(self):
        path = os.path.join(self.dir, "source")
        filenames = [fn for fn in os.listdir(path) if fn.endswith(".txt")]
        index_info = []
        for fn in filenames:
            print("Writing: %s..." % fn, end='')
            full_path = os.path.join(path, fn)
            meta, data = self.read_source_file(full_path)
            md_data = markdown.markdown(data, extensions=EXTENSIONS)
            temp = self.template
            index_info.append([fn, meta['title'], meta['created']])
            # all of these are optional, in theory:
            temp = temp.replace('<**NAME**>', self.config['name'])
            temp = temp.replace('<**TITLE**>', meta['title'])
            temp = temp.replace('<**BODY**>', md_data)
            temp = temp.replace('<**CREATED**>', meta['created'][:10])
            out_path = os.path.join(self.dir, "html", fn.replace(".txt", ".html"))
            with codecs.open(out_path, 'w', "utf-8") as g:
                g.write(temp)
            print("OK")
        self._create_index_page(index_info)
        print("All done")

    def _create_index_page(self, index_info):
        print("Writing: index.html...", end='')
        index_info.sort(key=lambda x: x[2])
        index_info.reverse()
        sio = io.StringIO()
        sio.write('<table id="nb_index_table">\n')
        for (filename, title, created) in index_info:
            sio.write("<tr>\n")
            sio.write('<td class="nb_created">{0}</td>\n'.format(created[:10]))
            sio.write('<td class="nb_title"><a href="{0}">{1}</a></td>\n'.format(
                filename.replace(".txt", ".html"), title))
            sio.write("</tr>\n")
        sio.write("</table>\n")

        temp = self.template
        temp = temp.replace("<**NAME**>", self.config['name'])
        temp = temp.replace("<**TITLE**>", "contents")
        temp = temp.replace("<**BODY**>", sio.getvalue())
        temp = temp.replace("<**CREATED**>",
                datetime.datetime.today().isoformat()[:10])
        out_path = os.path.join(self.dir, "html", "index.html")
        with codecs.open(out_path, 'w', 'utf-8') as g:
            g.write(temp)
        print("OK")

    def cmd_upload(self):
        path = os.path.join(self.dir, "html")
        filenames = os.listdir(path)

        print("Connecting to: %s..." % self.config['ftp_server'], end='')
        ftp = ftplib.FTP()
        port = int(self.config['ftp_port'])
        ftp.connect(self.config['ftp_server'], port)
        print("OK")

        try:
            print(ftp.getwelcome())
            ftp.login(self.config['ftp_login'], self.config['ftp_password'])
            ftp.set_pasv("ON" if self.config['ftp_mode'] == "PASV" else "OFF")

            print("Moving to %s..." % self.config['ftp_dir'])
            ftp.cwd(self.config['ftp_dir'])

            for fn in filenames:
                full_path = os.path.join(path, fn)
                if os.path.isdir(full_path): continue # skip directories
                print("Uploading: %s..." % fn, end='')
                with open(full_path, 'rb') as f:  # don't use codecs here
                    ftp.storbinary("STOR " + fn, f)
                print("OK")

        finally:
            try:
                print(ftp.quit())
            except:
                pass
            print("All done")

    def cmd_edit(self, filename):
        if not filename.endswith(".txt"):
            filename = filename + ".txt"
        post_path = os.path.join(self.dir, "source", filename)
        # if the file doesn't exist yet, create it
        if not os.path.exists(post_path):
            now = datetime.datetime.today()
            t9 = now.timetuple()
            ds = "%04d-%02d-%02d %02d:%02d:%02d" % t9[:6]
            temp_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),
                                     "sample-post.txt")
            post_template = open(temp_path).read()
            post_template = post_template.replace("1900-01-01 00:00:00", ds)
            with codecs.open(post_path, 'w', 'utf-8') as f:
                f.write(post_template)
        print("Starting editor...")
        os.system("{0} {1}".format(self.config['editor'], post_path))

if __name__ == "__main__":

    if not sys.argv[1:]:
        print(__usage__, file=sys.stderr)
        sys.exit(1)

    cmd, rest = sys.argv[1], sys.argv[2:]

    nanoblog = NanoBlog(".")
    try:
        f = getattr(nanoblog, "cmd_" + cmd)
    except AttributeError:
        print("Unknown command:", cmd, file=sys.stderr)
    else:
        f(*rest)

