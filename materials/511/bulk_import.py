import json,urllib.request,sqlite3
def import_single(url,path):
    with urllib.request.urlopen(url) as response:rows=[json.loads(s) for s in response.read().splitlines()]
    db=sqlite3.connect(path);db.execute('create table if not exists resource(type text,id text,body text,primary key(type,id))')
    with db:db.executemany('insert into resource values(?,?,?)',[(r['resourceType'],r['id'],json.dumps(r)) for r in rows])
    return db
