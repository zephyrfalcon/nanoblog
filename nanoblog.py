# nanoblog.py

import ftplib
import os
import sys
import markdown

__usage__ = """\
nanoblog.py command [args...]

Commands:
    build
    upload
    edit <filename>
    create <filename>
    list

"""

class NanoBlog:

    def __init__(self, dir):
        self.dir = os.path.abspath(dir)
        print "NanoBlog running in:", self.dir
        self.config = self._read_config()
        self.template = self._read_template()

    def _read_config(self):
        config = {}
        path = os.path.join(self.dir, "config.txt")
        with open(path, "r") as f:
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
        with open(path, "r") as f:
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
            print fn, meta['created']
        print "%d file(s)" % len(filenames)

    def cmd_build(self):
        path = os.path.join(self.dir, "source")
        filenames = [fn for fn in os.listdir(path) if fn.endswith(".txt")]
        for fn in filenames:
            print "Writing: %s..." % fn,
            full_path = os.path.join(path, fn)
            meta, data = self.read_source_file(full_path)
            md_data = markdown.markdown(data)
            temp = self.template
            # all of these are optional, in theory:
            temp = temp.replace('<**TITLE**>', meta['title'])
            temp = temp.replace('<**BODY**>', md_data)
            temp = temp.replace('<**CREATED**>', meta['created'])
            temp = temp.replace('<**MODIFIED**>', meta['modified'])
            out_path = os.path.join(self.dir, "html", fn.replace(".txt", ".html"))
            with open(out_path, 'w') as g:
                g.write(temp)
            print "OK"
        print "All done"

    def cmd_upload(self):
        path = os.path.join(self.dir, "html")
        filenames = os.listdir(path)

        print "Connecting to: %s..." % self.config['ftp_server'], 
        ftp = ftplib.FTP()
        port = int(self.config['ftp_port'])
        ftp.connect(self.config['ftp_server'], port)
        print "OK"

        try:
            print ftp.getwelcome()
            ftp.login(self.config['ftp_login'], self.config['ftp_password'])
            ftp.set_pasv("ON" if self.config['ftp_mode'] == "PASV" else "OFF")

            print "Moving to %s..." % self.config['ftp_dir']
            ftp.cwd(self.config['ftp_dir'])

            for fn in filenames:
                print "Uploading: %s..." % fn,
                full_path = os.path.join(path, fn)
                with open(full_path, 'rb') as f:
                    ftp.storbinary("STOR " + fn, f)
                print "OK"

        finally:
            print ftp.quit()

if __name__ == "__main__":

    if not sys.argv[1:]:
        print >> sys.stderr, __usage__
        sys.exit(1)

    cmd, rest = sys.argv[1], sys.argv[2:]
    print (cmd, rest)

    nanoblog = NanoBlog(".")
    f = getattr(nanoblog, "cmd_" + cmd)
    f()

