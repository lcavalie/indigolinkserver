# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#
#  indigolinkserver
#
#  Copyright (c) 2015 Konstantinos Vlassis. All rights reserved.
#
import globalVariables
import devices
import requests
import math
import sendAlert
import postgresdata
from requests.auth import HTTPDigestAuth
from decimal import Decimal

def loadDevicesXML(devicesXML):

	# Parse the XML and se the globalVariables matrix elements for use...

	import xml.etree.ElementTree as ET
	devroot = ET.fromstring(devicesXML)

	i=0
	for child in devroot.iter('device'):
		# loop to set arrays
	
		devName = child.find('name').text
		globalVariables.myDeviceName.append(devName)
		
		devID = child.find('id').text
		globalVariables.myDeviceID.append(devID)
		
		globalVariables.myDeviceTime.append(child.find('lastChangedRFC822').text)
		globalVariables.myDeviceOnOff.append(child.find('typeSupportsOnOff').text)
		
		devType = child.find('type').text
		globalVariables.myDeviceType.append(devType)
		
		if devType.find("TZ88E") > 0:
			# connect to postgres and get the meter value...
			globalVariables.myDeviceMeterValue.append(postgresdata.getPowerMeter(devID))
		else:
			#no value, just put ERROR...
			globalVariables.myDeviceMeterValue.append('ERROR')
			
		globalVariables.myDevicePath.append(child.find('path').text)
		
		element = None 
		element = child.find('isOn')

		if element is None:
			globalVariables.myDeviceIsOn.append('ERROR')
		else:
			globalVariables.myDeviceIsOn.append(element.text)

		element = child.find('sensorValue')
		
		if element is None:
			globalVariables.myDeviceSensorValue.append('ERROR')
		else:
			globalVariables.myDeviceSensorValue.append(element.text)
			
		element = child.find('displayRawState')

		if element is None:
			globalVariables.myDeviceRawState.append('ERROR')
		else:			
			globalVariables.myDeviceRawState.append(element.text)
			
		# put the device in a group...
		globalVariables.myDeviceGroup.append('0')
		
		if ('Relay Power Switch' in devType or 'Relay Power Switch' in devName):
			globalVariables.myDeviceGroup[i]='1'
			
		if ('Appliance Module' in devType or 'Appliance Module' in devName):
			globalVariables.myDeviceGroup[i]='2'
		
		if 'Temperature' in devName:
			globalVariables.myDeviceGroup[i]='5'
		
		if 'Luminance' in devName:
			globalVariables.myDeviceGroup[i]='7'
			
		if ('Smoke' in devType or 'Carbon' in devType):
			if 'Temperature' in devName:
				globalVariables.myDeviceGroup[i] = '5'
			elif 'Tamper' in devName:
				globalVariables.myDeviceGroup[i] = '6'
			else:
				globalVariables.myDeviceGroup[i] = '6'

		if ('Motion' in devType or 'Motion' in devName):
			if 'Temperature' in devName:
				globalVariables.myDeviceGroup[i] = '5'
			elif 'Tamper' in devName:
				globalVariables.myDeviceGroup[i] = '3'
			elif 'Luminance' in devName:
				globalVariables.myDeviceGroup[i] = '7'
			else:
				globalVariables.myDeviceGroup[i] = '3'

		if ('Door Sensor' in devName or 'Window Sensor' in devName or 'Window Sensor' in devType):
			if 'Temperature' in devName:
				globalVariables.myDeviceGroup[i] = '5'
			elif 'Tamper' in devName:
				globalVariables.myDeviceGroup[i] = '4'
			elif 'Luminance' in devName:
				globalVariables.myDeviceGroup[i] = '7'
			else:
				globalVariables.myDeviceGroup[i] = '4'
				
		i += 1	


def compareXML(processDevices):

	myCompDeviceID=[]
	myCompDeviceSensorValue=[]
	myCompDeviceTime=[]
	myCompDeviceIsOn= []
	myCompDeviceType=[]
	myCompDeviceName=[]
	myCompDeviceOnOff=[]
	myCompDeviceRawState=[]
	myCompDeviceMeterValue=[]

	rXML=''
	r2XML=''
	myXML = ''
	cRtrn = '\n'

	addXML = False
	
	import xml.etree.ElementTree as ET2
	devroot = ET2.fromstring(processDevices)

	i=0
	for child in devroot.iter('device'):
		# loop to set arrays
	
		devID = child.find('id').text
		myCompDeviceID.append(devID)
		
		myCompDeviceName.append(child.find('name').text)
		
		devType = child.find('type').text
		myCompDeviceType.append(devType)
		
		if devType.find("TZ88E") > 0:
			# connect to postgres and get the meter value...
			myCompDeviceMeterValue.append(postgresdata.getPowerMeter(devID))
		else:
			#no value, just put ERROR...
			myCompDeviceMeterValue.append('ERROR')
		
		myCompDeviceOnOff.append(child.find('typeSupportsOnOff').text)
		myCompDeviceTime.append(child.find('lastChangedRFC822').text)
		

		element = None 
		element = child.find('isOn')

		if element is None:
			myCompDeviceIsOn.append('ERROR')
		else:
			myCompDeviceIsOn.append(element.text)

		element = child.find('sensorValue')
		
		if element is None:
			myCompDeviceSensorValue.append('ERROR')
		else:
			myCompDeviceSensorValue.append(element.text)

		element = child.find('displayRawState')

		if element is None:
			myCompDeviceRawState.append('ERROR')
		else:
			myCompDeviceRawState.append(child.find('displayRawState').text)
		
		i += 1

	# compare with global variable arrays

	for myDevice in myCompDeviceID:
		indx = myCompDeviceID.index(myDevice)
		gindx = globalVariables.myDeviceID.index(myDevice)
		
		if indx <> gindx:
			# device added or deleted... 
			print 'Device new/deleted?:' + myDevice
			
			# stop and reload ALL devices...

			# get the XML output with details for all the devices...
			devicesXML = devices.getDeviceList().replace(u'\xb0','')
			# Process the XML to fill the arrays with data
			loadDevicesXML(devicesXML)

			return devicesXML

			break

		else:
			# device found, compare values
			addXML = True
			
			if (globalVariables.myDeviceSensorValue[gindx] <> myCompDeviceSensorValue[indx] or globalVariables.myDeviceIsOn[gindx] <> myCompDeviceIsOn[indx] or globalVariables.myDeviceMeterValue[gindx] <> myCompDeviceMeterValue[indx]):
				# update global array with new value
				
				globalVariables.myDeviceIsOn[gindx] = myCompDeviceIsOn[indx]
				globalVariables.myDeviceTime[gindx] = myCompDeviceTime[indx]
				globalVariables.myDeviceType[gindx] = myCompDeviceType[indx]
				globalVariables.myDeviceOnOff[gindx] = myCompDeviceOnOff[indx]
				globalVariables.myDeviceName[gindx] = myCompDeviceName[indx]
				
				# send notification to connected devices with the change...
				
				r2XML = '<device>' + cRtrn
				r2XML += '<name>' + myCompDeviceName[indx] + '</name>' + cRtrn
				r2XML += '<id>' + myCompDeviceID[indx] + '</id>' + cRtrn
				
				if myCompDeviceIsOn[indx] <> 'ERROR':
					r2XML += '<isOn>' + myCompDeviceIsOn[indx] + '</isOn>' + cRtrn
					if myCompDeviceIsOn[indx] == "True":
						# check if we need to send an alert...
						checkNotification(myDevice)
				
				r2XML += '<lastChangedRFC822>' + myCompDeviceTime[indx] + '</lastChangedRFC822>' + cRtrn
				r2XML += '<typeSupportsOnOff>' + myCompDeviceOnOff[indx] + '</typeSupportsOnOff>' + cRtrn
				r2XML += '<type>' + myCompDeviceType[indx] + '</type>' + cRtrn
				
				if myCompDeviceType[indx].find("TZ88E") > 0:
					oldvalue = Decimal(globalVariables.myDeviceMeterValue[gindx])
					newvalue = Decimal(myCompDeviceMeterValue[indx])

					tempdiff = math.fabs(newvalue - oldvalue)
			
					print myCompDeviceName[indx] + 'difference: ' + str(tempdiff)
					
					globalVariables.myDeviceMeterValue[gindx] = myCompDeviceMeterValue[indx]
					
					r2XML += '<meterValue>' + myCompDeviceMeterValue[indx] + '</meterValue>' + cRtrn
					
				else:
					r2XML += '<meterValue>ERROR</meterValue>' + cRtrn
				
				if myCompDeviceSensorValue[indx] <> 'ERROR':

					oldvalue = Decimal(globalVariables.myDeviceRawState[gindx])
					newvalue = Decimal(myCompDeviceRawState[indx])

					tempdiff = math.fabs(newvalue - oldvalue)
			
					#print myCompDeviceName[indx] + 'difference: ' + str(tempdiff)
					
					if tempdiff >= 0.5:
						r2XML += '<sensorValue>' + myCompDeviceSensorValue[indx] + '</sensorValue>' + cRtrn

						globalVariables.myDeviceSensorValue[gindx] = myCompDeviceSensorValue[indx]
						globalVariables.myDeviceRawState[gindx] = myCompDeviceRawState[indx]

						addXML = True
					else:	
						addXML = False
				
				else:
					addXML = True

				r2XML += '</device>' + cRtrn

				if addXML == True:
					rXML += r2XML

	if rXML <> '':			
		myXML = '<deviceChanges>' + rXML + '</deviceChanges>'
	
	return myXML


def toggleDevice(deviceid):
	

	gindx = globalVariables.myDeviceID.index(deviceid)

	url = globalVariables.indigoserver_url + globalVariables.myDevicePath[gindx] + '?toggle=1&_method=put'

	r = requests.get(url, auth=HTTPDigestAuth(globalVariables.indigoserver_u, globalVariables.indigoserver_p))
	
	tempXML = devices.addMeterValue(r.text)

	deviceListXML = '<devices>' + tempXML + '</devices>'

	adata = deviceListXML.decode("utf-8")
	bdata = adata.encode("ascii", "ignore")

	#print bdata
	return bdata


def reloadDevice(deviceid):
	

	gindx = globalVariables.myDeviceID.index(deviceid)

	url = globalVariables.indigoserver_url + globalVariables.myDevicePath[gindx]

	r = requests.get(url, auth=HTTPDigestAuth(globalVariables.indigoserver_u, globalVariables.indigoserver_p))
	
	tempXML = devices.addMeterValue(r.text)

	deviceListXML = '<devices>' + tempXML + '</devices>'

	adata = deviceListXML.decode("utf-8")
	bdata = adata.encode("ascii", "ignore")

	#print bdata
	return bdata


def checkNotification(deviceid):
	
	# check device type/function
	indx = globalVariables.myDeviceID.index(deviceid)
	
	check1 = ['smoke', 'carbon']
	check2 = ['temperature']
	
	alertSend = False
	
	#check device type, first check for smoke alarms that will always send alerts!
	
	myDeviceType = globalVariables.myDeviceType[indx].lower()
	myDeviceName = globalVariables.myDeviceName[indx].lower()
	
	if any(x in myDeviceType for x in check1):
		# this is a smoke or monoxide sensor...
		
		if any(y in myDeviceName for y in check2):
			alertSend = False
		else:
			alertSend = True
			
	
	else:
		# check of alarm is armed...
		
		if globalVariables.alarmArmed == True:
		
		# check for Motion and Door/Window Sensors...
		
			check3 = ['motion', 'door', 'window']
			
			if any(z in myDeviceType for z in check3):
				# sensor(s) breached, send alert to user!
				alertSend = True

	if alertSend == True:
		sendAlert.sendNotification(deviceid)		




	