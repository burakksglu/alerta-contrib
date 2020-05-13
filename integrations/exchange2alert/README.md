IMAP Mailbox Check Integration
==================

Monitor exchange inbox availability using IMAP and generate alerts on unread mails.

For help, join [![Gitter chat](https://badges.gitter.im/alerta/chat.png)](https://gitter.im/alerta/chat)

Installation
------------

Clone the GitHub repo and run:

    $ python setup.py install

Or, to install remotely from GitHub run:

    $ pip install git+https://github.com/burakksglu/alerta-contrib.git#subdirectory=integrations/exchange2alert

Configuration
-------------

Add below listed environment variables to `alertad.cof` or export at start in the following format:

 - IMAP_HOST
 - IMAP_USERNAME
 - IMAP_PASSWORD
 - IMAP_FOLDER 
 - IMAP_SSL = YES # For SSL Connection, is not necessary for no-ssl.

License
-------

Copyright (c) 2014-2016 Nick Satterly. Available under the MIT License.
