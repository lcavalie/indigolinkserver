# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#
#  indigolinkserver
#
#  Copyright (c) 2015 Konstantinos Vlassis. All rights reserved.
#
import devices
import globalVariables
import xmlproc
import postgresdata
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory, listenWS
from twisted.internet import task
from twisted.internet import reactor, ssl
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File
import sys
import base64

class MyServerProtocol(WebSocketServerProtocol):

    def broadcast(self):
	message = globalVariables.loopData
    	if message <> '':
    		# print message
		isBinary = False
		self.sendMessage(message, isBinary)

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))
        self.checkDevices = task.LoopingCall(self.broadcast)
        self.checkDevices.start(globalVariables.pollInterval)

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
	     #print("BINARY")
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))
	    processMessage(self, payload.decode('utf8'), isBinary)
	    #print ("TEXT")

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
	self.checkDevices.stop()

def processMessage(self, payload, isBinary):
	a = payload.split(':')

	if len(a) > 1:
		token = a[0].strip()
		command = a[1].strip()
		content = a[2].strip()
 
		userpass = globalVariables.remote_username + ":" + globalVariables.remote_password
		mytoken = base64.standard_b64encode(userpass)

		if token <> mytoken:
			self.sendClose()
			print("Invalid token, closing connection!")
			return

		msg = ""

		if command == "iam":
			msg = init_app_data()	

		elif command == "toggle":
			msg = xmlproc.toggleDevice(content)

		elif command == "reload":
			msg = xmlproc.reloadDevice(content)

		elif command == "graph":
			msg = postgresdata.getGraphData(content)
			
		elif command == "alarm":
			msg = '<devices>' + devices.alarmArm(content) + '</devices>'
		
		else:
		    print("Invalid command!")

		if isBinary:
			# something wrong?
			print("ERROR! Binary data!")
		else:
			self.sendMessage(msg, isBinary)

def init_app_data():
	# get the XML output with details for all the devices...
	devicesXML = devices.getDeviceList().replace(u'\xb0','')
	# Process the XML to fill the arrays with data
	xmlproc.loadDevicesXML(devicesXML)
	adata = devicesXML.decode("utf-8")
	bdata = adata.encode("ascii", "ignore")
	return bdata

def poll_data():
	bdata=''
	# get the XML output with details for all the devices...
	processDevices = devices.getDeviceList().replace(u'\xb0','')
	# Process the XML to fill the arrays with data
	devicesXML  = xmlproc.compareXML(processDevices)
	adata = devicesXML.decode("utf-8")
	bdata = adata.encode("ascii", "ignore")
	globalVariables.loopData = bdata

if __name__ == '__main__':

    log.startLogging(sys.stdout)

    init_app_data()

    contextFactory = ssl.DefaultOpenSSLContextFactory(globalVariables.localserver_key_path,globalVariables.localserver_crt_path)

    factory = WebSocketServerFactory(globalVariables.localserver_url, debug=False)
    factory.protocol = MyServerProtocol
    factory.setProtocolOptions(allowHixie76=True)
    listenWS(factory, contextFactory)
    
    event = task.LoopingCall(poll_data)
    event.start(globalVariables.pollInterval) 

    reactor.run()
