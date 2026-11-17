import json
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from threading import Thread
DATA=[{'resourceType':'Patient','id':'p1','name':'甲'},{'resourceType':'Observation','id':'o1','subject':'p1','value':7}]
def serve_sync():
    """A synchronous source fixture. Async job state/freeze/cancel are new work."""
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path!='/all.ndjson':self.send_error(404);return
            body=('\n'.join(json.dumps(x,ensure_ascii=False) for x in DATA)+'\n').encode()
            self.send_response(200);self.send_header('Content-Type','application/fhir+ndjson');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
        def log_message(self,*args):pass
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler);Thread(target=server.serve_forever,daemon=True).start();return server
