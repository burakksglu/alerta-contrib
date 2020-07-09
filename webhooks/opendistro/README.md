OpenDistro Webhook
================

Receive [OpenDistro](https://opendistro.github.io/for-elasticsearch/) trigger actions via webhooks.

For help, join [![Gitter chat](https://badges.gitter.im/alerta/chat.png)](https://gitter.im/alerta/chat)

Installation
------------

Clone the GitHub repo and run:

```plain
python setup.py install
```

Or, to install remotely from GitHub run:

```plain
pip install git+https://github.com/alerta/alerta-contrib.git#subdirectory=webhooks/opendistro
```

**Note:** If Alerta is installed in a python virtual environment then plugins
need to be installed into the same environment for Alerta to dynamically
discover them.

Configuration
-------------

### Alerta

The custom webhook will be auto-detected and added to the list of available API endpoints. Tested on docker environment.

### Example Destination settings on OpenDistro 
--------------
```
Destination:
    Name: <Name for destination>
    Type: Custom Webhook

Settings:
* Define endpoint by custom attributes URL
    Type: <Protocol>
    Host: <Hostname/IP>
    Port: <Port>
    Path: api/webhooks/opendistro

Headers:
    Content-Type: application/json
    X-API-Key: <Api Key>
```

License
-------

Copyright (c) 2020 Burak Köseoglu Available under the MIT License.
