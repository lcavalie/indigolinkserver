# -*- coding: utf-8 -*-
#
#  indigolinkserver
#
#  Copyright (c) 2015 Konstantinos Vlassis. All rights reserved.
#
import urllib
import requests
import globalVariables
import postgresdata

# Starting API devices call
deviceListXML = ''

def getDeviceList():
	from requests.auth import HTTPDigestAuth
	url = globalVariables.indigoserver_url + '/devices.xml'

	r = requests.get(url, auth=HTTPDigestAuth(globalVariables.indigoserver_u, globalVariables.indigoserver_p))

	deviceListXML = r.text

	# Parse the DeviceList XML

	import xml.etree.ElementTree as ET
	root = ET.fromstring(deviceListXML)

	deviceDetailsXML = '<devices>'	
	
	for child in root:
		#print child.text, ':', child.get('href') 
		# loop to get each device info from the API
		device_url = globalVariables.indigoserver_url + child.get('href')
		device_path = child.get('href')

		dev_rq = requests.get(device_url, auth=HTTPDigestAuth(globalVariables.indigoserver_u, globalVariables.indigoserver_p))

		tempXML = addPathElement(dev_rq.text, device_path)
		
		deviceDetailsXML += addMeterValue(tempXML)

	# end of loop, add anything more and close the XML...
	
	deviceDetailsXML += alarmArm("status") + '</devices>'
	
	return deviceDetailsXML
		
# End API devices call

def addPathElement(myXML, device_url):
	import xml.etree.ElementTree as ET

	newXML = myXML.replace(u'\xb0','')
	devroot = ET.fromstring(newXML)

	new_el = ET.Element("path")
	new_el.text = device_url
	devroot.insert(0, new_el)

	return ET.tostring(devroot)

def addMeterValue(myXML):

	import xml.etree.ElementTree as ET

	newXML = myXML.replace(u'\xb0','')
	devroot = ET.fromstring(newXML)

	for child in devroot.iter('device'):
		devID = child.find('id').text
		devType = child.find('type').text
		
		new_el = ET.Element("meterValue")
		
		if devType.find("TZ88E") > 0:
			new_el.text = postgresdata.getPowerMeter(devID)
		else:
			new_el.text = "ERROR"
			
		devroot.insert(0, new_el)

		return ET.tostring(devroot)

def alarmArm(status):
	
	if status == 'On':
		#set alarm on
		globalVariables.alarmArmed = True
	elif status == 'Off':
		#set alarm off
		globalVariables.alarmArmed = False
	else:
		if globalVariables.alarmArmed == True:
			status = 'On'
		else:
			status = 'Off'
	
	# create the XML to send...
	cRtrn = '\n'
	
	alarmXML = '<device>'
	alarmXML += '<name>Alarm</name>' 
	alarmXML += '<id>0</id>' 
	alarmXML += '<isOn>' + status + '</isOn>' 
	alarmXML += '<typeSupportsOnOff>True</typeSupportsOnOff>' 
	alarmXML += '<lastChangedRFC822>ERROR</lastChangedRFC822>' 
	alarmXML += '<path>ERROR</path>' 
	alarmXML += '<type>Alarm</type>'
	alarmXML += '</device>' + cRtrn
	
	adata = alarmXML.decode("utf-8")
	bdata = adata.encode("ascii", "ignore")
	
	return bdata
