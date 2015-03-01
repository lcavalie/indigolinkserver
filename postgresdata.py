# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#
#  indigolinkserver
#
#  Copyright (c) 2015 Konstantinos Vlassis. All rights reserved.
#
import globalVariables
import json
import psycopg2
from psycopg2.extras import RealDictCursor
import datetime
from json import JSONEncoder


def getPowerMeter(deviceid):
    # connect and get the data...
    conn = psycopg2.connect(database=globalVariables.pg_db, user=globalVariables.pg_user, password=globalVariables.pg_pwd, host=globalVariables.pg_host, port=globalVariables.pg_port)
    
    cur = conn.cursor()
    cur.execute("SELECT id, curenergylevel FROM device_history_" + deviceid + " order by id desc limit 1")
    
    rows = cur.fetchall()
    
    conn.close()
    
    for row in rows:
        return str(row[1])
    

def getGraphData(deviceid):
    
    indx = globalVariables.myDeviceID.index(deviceid)
    
    devgroup = globalVariables.myDeviceGroup[indx]
    
    conn = psycopg2.connect(database=globalVariables.pg_db, user=globalVariables.pg_user, password=globalVariables.pg_pwd, host=globalVariables.pg_host, port=globalVariables.pg_port)

    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    mydate = datetime.datetime.now()
    
    dateToday = mydate.strftime("%Y/%m/%d")
    
    endDate = mydate + datetime.timedelta(days=1)

    dateTmrw = endDate.strftime("%Y/%m/%d")
    
    myColumn = ""
    
    if devgroup == '2':
        myColumn = "curenergylevel"
    elif devgroup == '5' or devgroup == '7':
        myColumn = "sensorvalue"
        
    mySQL = "SELECT id, ts, " + myColumn + " as sensorvalue FROM device_history_" + deviceid + " WHERE ts between '" + dateToday + "' and '" + dateTmrw + "' order by id"

    cur.execute(mySQL)
    
    res = json.dumps(cur.fetchall(), cls=DateEncoder)
    
    conn.close()
    
    cRtrn = '\n'

    graphXML = '<graphdata>'
    graphXML += '<deviceid>' + deviceid + '</deviceid>'
    graphXML += '<jsondata>' + res + '</jsondata>'
    graphXML += '</graphdata>' + cRtrn

    adata = graphXML.decode("utf-8")
    bdata = adata.encode("ascii", "ignore")
    
    return bdata    
    
class DateEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        return JSONEncoder.default(self, obj)