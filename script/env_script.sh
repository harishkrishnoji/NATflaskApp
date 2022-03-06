#!/bin/bash
scl enable rh-python38 bash
/opt/rh/rh-python38/root/usr/bin/python3 /appserver/natdata/script/db_update.py > /var/log/natDBUpdate.log 2>&1