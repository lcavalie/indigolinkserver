# -*- coding: utf-8 -*-
#
#  indigolinkserver
#
#  Copyright (c) 2015 Konstantinos Vlassis. All rights reserved.
#
# 
# DO NOT EDIT (BEGIN)
# -------------------------------------------------- 
myDeviceID=[]
myDeviceSensorValue=[]
myDeviceIsOn=[]
myDeviceTime=[]
myDeviceType=[]
myDeviceName=[]
myDeviceOnOff=[]
myDeviceRawState=[]
myDeviceMeterValue=[]
myDeviceGroup=[]
myDevicePath=[]
alarmArmed = False
loopData = ''
# DO NOT EDIT (END)
# --------------------------------------------------
# the following are configuration parameters that need
# to be changed per your configurations of
# indigo server and local computer config

# indigo server parameters
indigoserver_url = 'http://192.168.1.1:8176'
indigoserver_u = 'username'
indigoserver_p = 'password'

# remote client (ihpone) credentials to accept:
remote_username = 'username'
remote_password = 'password'

# indigolink server parameters
# the IP & Port will be used by the iphone app
localserver_url = 'wss://192.168.1.1:6035'

pollInterval = 5

localserver_key_path = 'ssl/server.key'
localserver_crt_path = 'ssl/server.crt'

# postgredql config
pg_db='indigoDB'
pg_user='username'
pg_pwd='password'
pg_host='localhost'
pg_port='5432'

# Apple APN config
apn_cert_file='ssl/indigolinkCert.pem'
apn_key_file='ssl/indigolinkKey.pem'

apn_test_token_hex = 'your_device_token_goes_here'