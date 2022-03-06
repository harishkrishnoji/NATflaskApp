import os
import json
import subprocess
from gitlab_helper import GitLab_Client
from sqlite_helper import WriteToDB

filename = [
"OFD_CheckPoint.json",
"OFD_PaloAlto.json",
"OFS_CheckPoint.json",
"OFS_PaloAlto_AZLower.json",
"OFS_PaloAlto_AZUpper.json",
"OFS_PaloAlto_Corp.json",
"OFS_PaloAlto_Lowers.json",
"OFS_PaloAlto_Main.json",
"OFS_PaloAlto_Virtual.json"]

gb = GitLab_Client(filepath="fw-nat/OFS_PaloAlto_Lowers.json", token="a6JRJoWise3vAJJ_zghm")
sq_db = WriteToDB("global")

def db_fun(f):
    print("Inserting to local DB")
    for i in f:
        sq_db.insert_row(i)

def fileSizeCheck():
    print("Performing file check")
    nfile_size = os.path.getsize('global_nat.db')
    ofile_size = os.path.getsize('/appserver/natdata/db/ofs_cp_nat.db')
    print(f"Old file size: {ofile_size}; New file size : {nfile_size}")
    if nfile_size >= ofile_size:
        print("Moving new file to container DB")
        subprocess.run(["mv","global_nat.db","/appserver/natdata/db/"])
        subprocess.run(["/appserver/natdata/docker-compose","down"])
        subprocess.run(["/appserver/natdata/docker-compose","up","--build"])


if __name__ == "__main__":
    for fn in filename:
        print(f"Pulling file from Git : {fn}")
        gb.filepath = f"fw-nat/{fn}"
        f = gb.get_file()
        jf = json.loads(f.decode())
        db_fun(jf)
    fileSizeCheck()
