"""Externally controlled HTTP scenarios, not an ExportJobs implementation.
It serves static checked-in files. No cohort generation/freeze/job persistence/cancel arbitration.
"""
from pathlib import Path
import hashlib,json,threading
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
class ScenarioSource:
    def __init__(self):
        self.scenario='pending';self.events=[];owner=self;root=Path(__file__).with_name('fixtures')
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                owner.events.append([self.path,owner.scenario])
                if self.path=='/status':
                    if owner.scenario=='pending':code=202;body={'status':'running'}
                    elif owner.scenario=='cancelled':code=409;body={'resourceType':'OperationOutcome','status':'cancelled'}
                    else:
                        code=200;output=[]
                        for kind in ['Patient','Observation']:
                            path=root/(kind+'.ndjson');data=path.read_bytes();output.append({'type':kind,'url':'/files/'+path.name,'count':len(data.splitlines()),'sha256':hashlib.sha256(data).hexdigest()})
                        errors=[]
                        if owner.scenario=='partial':
                            data=(root/'errors.ndjson').read_bytes();errors=[{'url':'/files/errors.ndjson','count':1,'sha256':hashlib.sha256(data).hexdigest()}]
                        body={'status':'success','job_id':'fixture-job','cohort':['p1'],'output':output,'error':errors}
                    data=json.dumps(body).encode();self.send_response(code);self.send_header('Content-Type','application/json')
                    if code==202:self.send_header('Retry-After','1')
                elif self.path.startswith('/files/'):
                    name=self.path.split('/')[-1]
                    if name not in ['Patient.ndjson','Observation.ndjson','errors.ndjson']:
                        self.send_error(404);return
                    actual='Observation-truncated.ndjson' if owner.scenario=='truncated' and name=='Observation.ndjson' else name
                    data=(root/actual).read_bytes();self.send_response(200);self.send_header('Content-Type','application/fhir+ndjson')
                else:self.send_error(404);return
                self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
            def log_message(self,*args):pass
        self.server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=self.server.serve_forever,daemon=True).start()
    @property
    def url(self):return 'http://127.0.0.1:'+str(self.server.server_port)
    def select(self,scenario):
        if scenario not in ['pending','complete','partial','cancelled','truncated']:raise ValueError('unknown fixture scenario')
        self.scenario=scenario
    def close(self):self.server.shutdown();self.server.server_close()
