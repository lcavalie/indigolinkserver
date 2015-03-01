# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#
#  indigolinkserver
#
#  Copyright (c) 2015 Konstantinos Vlassis. All rights reserved.
#
import globalVariables
import random
import time
from apns import APNs, Frame, Payload


def response_listener(error_response):
    print("client get error-response: " + str(error_response))
    
    
def sendNotification(deviceid):
	# send APN to device... 
	indx = globalVariables.myDeviceID.index(deviceid)
	
	message = "Sensor " + globalVariables.myDeviceName[indx] + " has been triggered at: " + globalVariables.myDeviceTime[indx]
	
	print message
	
	apns = APNs(use_sandbox=True, cert_file=globalVariables.apn_cert_file, key_file=globalVariables.apn_key_file, enhanced=True)

	# Send a notification
	token_hex = globalVariables.apn_test_token_hex
	
	#payload = Payload(alert=message, sound="default", badge=1)
	payload = Payload(alert=message, sound="default")
	identifier = random.getrandbits(32)
	apns.gateway_server.register_response_listener(response_listener)
	apns.gateway_server.send_notification(token_hex, payload, identifier=identifier)
	apns.gateway_server.force_close()
