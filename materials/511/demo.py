import tempfile
from pathlib import Path
from export_jobs import serve_sync
from bulk_import import import_single
server=serve_sync()
try:
    with tempfile.TemporaryDirectory() as t:
        db=import_single('http://127.0.0.1:'+str(server.server_port)+'/all.ndjson',Path(t)/'warehouse.db');print(db.execute('select type,id from resource order by type').fetchall());db.close()
finally:server.shutdown();server.server_close()
