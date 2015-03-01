Compatibility

The indigolink server has been written with Python 2.7.

In order for the indigolink server to connect to the indigo domotics software and to respond to the indigolink app the appropriate ports need to be opened on your firewall/router.

The indigolink server uses the indigo domotis REST API to communicate with the Z-Wave devices.

Requirements

To use the indigolink server you need to have:
- the indigo domotics software installed & running on your Mac (tested with 6.0.20) 
- the indigo domotics SQL Logger plugin enabled and using a PostgreSQL database (tested with 9.4.1)

Dependencies

The indigolink server reuires:
- Twisted
- Autobahn
- PyAPNs
- psycopg2

Configuration

Everything you need to change is located in the globalVariables.py file.

For SSL to work you need to have your own key and crt files to be used by the indigolink server.

For notifications to work (APN) you will need to go through the (usual) process to get your pem files from Apple.

To run the server from the command line use: python indigolinkserver.py

License

Licensed under the Apache License, Version 2.0.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
