 # -*- coding: utf-8 -*-
from verify_library import *
import BaseHTTPServer
import json
from functools import partial
import threading

def update(post_data):
    try:
        repository_data = json.loads(post_data)
        url = repository_data.get("repository").get("url")
        is_push = "pusher" in repository_data.keys()
        clone_url = url + ".git"

        if (is_push):
            if not is_already_cloned(clone_url):
                print clone(clone_url)
                config_properties(clone_url)
            else:
                update_repo(clone_url)

            run_sonar(clone_url)

    except (AttributeError, ValueError):
        print "It's not a valid Github Webhooks json object!"

class HooksHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self.send_response(200, "OK")
        self.end_headers()
        self.finish()
        
        thread = threading.Thread(target=partial(update, post_data))
        thread.start()
        print "Thread started!"

    def do_GET(self):
        self.send_response(200, "OK")
        self.end_headers()
        self.wfile.write("SI1 webhooks server is up!")
        self.finish()

    def finish(self):
        if not self.wfile.closed:
            self.wfile.flush()
        self.wfile.close()
        self.rfile.close()
        self.connection.close()
