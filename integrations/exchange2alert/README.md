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
To enable the script simply set `IMAP_CHECK=True` in environment or export it.


Add below listed environment variables to `alertad.conf` or export at the start in the following format:

 - IMAP_FREQ # Loop frequency.
 - IMAP_HOST
 - IMAP_USERNAME
 - IMAP_PASSWORD
 - IMAP_FOLDER # Inbox folder to look for.
 - IMAP_SSL = YES # For SSL Connection, is not necessary for no-ssl.

License
-------

Copyright (c) 2020 Burak Köseo?lu. Available under the MIT License.
