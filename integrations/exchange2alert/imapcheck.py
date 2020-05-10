import traceback
import sys
import platform
import time
import subprocess
import threading
import queue as Queue
import re
import logging as LOGging
import yaml
import os
from time import sleep
from alertaclient.api import Client
import eventlet
import email

__version__ = '1.0.0'

LOG = LOGging.getLogger('alerta.imap')
LOG.setLevel(LOGging.DEBUG)
LOG.addHandler(LOGging.StreamHandler())


SERVER_THREAD_COUNT = 20
LOOP_EVERY = 30

imapclient = eventlet.import_patched('imapclient')

def get_email_content(body):
	if body.is_multipart():
		item = dict()
		item["%s" % "From".upper()] = body['From'][:255]
		item["%s" % "To".upper()] = body['To'][:255]
		item["%s" % "Subject".upper()] = body['Subject'][:255]
		item["%s" % "Date".upper()] = body['Date'][:255]
		for part in body.walk():
			if (part.get_content_type() == 'text/html') and (part.get('Content-Disposition') is None):
				item["%s" % "Body".upper()] = part.get_payload()
				
				return item

class WorkerThread(threading.Thread):

    def __init__(self, api, queue):

        threading.Thread.__init__(self)
        LOG.debug('Initialising %s...', self.getName())

        self.last_event = {}
        self.queue = queue   # internal queue
        self.api = api               # message broker

    def run(self):

        while True:
            LOG.debug('Waiting on input queue...')
            item = self.queue.get()

            if not item:
                LOG.info('%s is shutting down.', self.getName())
                break

            environment, service, resource, retries, queue_time = item

            if time.time() - queue_time > LOOP_EVERY:
                LOG.warning('Loop exceeded', resource, int(time.time() - queue_time))
                self.queue.task_done()
                continue

            LOG.info('%s pinging %s...', self.getName(), resource)
            
            LOG.info('... script started')

         
                # Defaults
                
            self.queue.task_done()
            LOG.info('%s ping %s complete.', self.getName(), resource)

        self.queue.task_done()


class ImapDaemon(object):

    def __init__(self):

        self.shuttingdown = False

    def run(self):

        self.running = True

        # Create internal queue
        self.queue = Queue.Queue()

        self.api = Client('http://localhost:8080/api')

        # Start worker threads
        LOG.debug('Starting %s worker threads...', SERVER_THREAD_COUNT)
        for i in range(SERVER_THREAD_COUNT):
            w = WorkerThread(self.api, self.queue)
            try:
                w.start()
            except Exception as e:
                LOG.error('Worker thread #%s did not start: %s', i, e)
                continue
            LOG.info('Started worker thread: %s', w.getName())

        while not self.shuttingdown:
            try:
                while True:
                # <--- Start of configuration section
            
                    # Retrieve IMAP host - halt script if section 'imap' or value missing
                    try:
                        host = os.getenv("IMAP_HOST", "value does not exist") 
                        LOG.info(host)
                    except                  
                        print ("IMAP_HOST: " + value)
                        break
                    # Retrieve IMAP username - halt script if section 'imap' or value missing
                    try:
                        username = os.getenv("IMAP_USERNAME", "value does not exist") 
                        LOG.info(username)
                    except                  
                        print ("IMAP_USERNAME: " + value)
                        break
                    
                    # Retrieve IMAP password - halt script if missing
                   try:
                        password = os.getenv("IMAP_PASSWORD", "value does not exist") 
                        LOG.info(password)
                    except                  
                        print ("IMAP_PASS: " + value)
                        break
                    
                    # Retrieve IMAP SSL setting - warn if missing, halt if not boolean
                    try:
                        ssl = os.getenv("IMAP_SSL", "value does not exist") 
                        LOG.info(ssl)
                    except                  
                        print ("IMAP_SSL: " + value)
                        break
                    
                    # Retrieve IMAP folder to monitor - warn if missing
                    try:
                        folder = os.getenv("IMAP_FOLDER", "value does not exist") 
                        LOG.info(folder)
                    except                  
                        print ("IMAP_FOLDER: " + value)
                        break
                        
                    while True:
                        # <--- Start of IMAP server connection loop
                        
                        # Attempt connection to IMAP server
                        LOG.info('connecting to IMAP server - {0}'.format(host))
                        try:
                            server = imapclient.IMAPClient(host, use_uid=True, ssl=ssl)
                        except Exception:
                            # If connection attempt to IMAP server fails, retry
                            etype, evalue = sys.exc_info()[:2]
                            estr = traceback.format_exception_only(etype, evalue)
                            logstr = 'failed to connect to IMAP server - '
                            for each in estr:
                                logstr += '{0}; '.format(each.strip('\n'))
                            LOG.error(logstr)
                            sleep(10)
                            continue
                        LOG.info('server connection established')
                        
                        # Attempt login to IMAP server
                        LOG.info('logging in to IMAP server - {0}'.format(username))
                        try:
                            response = server.login(username, password)
                            LOG.info('login successful - {0}'.format(response))
                        except Exception:
                            # Halt script when login fails
                            etype, evalue = sys.exc_info()[:2]
                            estr = traceback.format_exception_only(etype, evalue)
                            logstr = 'failed to login to IMAP server - '
                            for each in estr:
                                logstr += '{0}; '.format(each.strip('\n'))
                            log.critical(logstr)
                            break
                        
                        # Select IMAP folder to monitor
                        LOG.info('selecting IMAP folder - {0}'.format(folder))
                        try:
                            response = server.select_folder(folder)
                            LOG.info('folder selected')
                        except Exception:
                            # Halt script when folder selection fails
                            etype, evalue = sys.exc_info()[:2]
                            estr = traceback.format_exception_only(etype, evalue)
                            logstr = 'failed to select IMAP folder - '
                            for each in estr:
                                logstr += '{0}; '.format(each.strip('\n'))
                            log.critical(logstr)
                            break
                        
                        # Retrieve and process all unread messages. Should errors occur due to loss of connection, attempt restablishing connection 
                        try:
                            response = server.search('UNSEEN')
                        except Exception:
                            continue
                        LOG.info('{0} unread messages seen - {1}'.format(
                            len(response), response
                            ))
                        
                        for each in response:
                            try:
                                response = server.fetch(each, ['RFC822'])
                            except Exception:
                                LOG.error('failed to fetch email - {0}'.format(each))
                                continue
                            mail_string = response[each][b'RFC822']
                            mail_decoded = email.message_from_bytes(mail_string)
                            
                            # print(mail_decoded)
                            
                            try:
                                output = get_email_content(mail_decoded)
                                text = "Mail Alert: " + output['FROM'] + output['BODY']
                                LOG.info('processing email {0} - {1}'.format(
                                    each, mail_decoded['subject']
                                    ))
                                try:
                                    self.api.send_alert(
                                        resource=output['FROM'],
                                        event='Mail',
                                        origin='Inbox',
                                        severity='major',
                                        environment='Production',
                                        service=['MailAlerter'],
                                        text='Problem Mail: ' + output['BODY'],
                                        event_type='serviceAlert',
                                    )
                                except Exception as e:
                                    LOG.warning('Failed to send alert: %s', e)
                            except Exception:
                                LOG.error('failed to process email {0}'.format(each))
                                raise
                                continue
                                
                        # End of IMAP server connection loop --->
                        break
                        
                    # End of configuration section --->
                    break
                    LOG.info('script stopped ...')

                time.sleep(LOOP_EVERY)

            except (KeyboardInterrupt, SystemExit):
                self.shuttingdown = True

        LOG.info('Shutdown request received...')
        self.running = False

        for i in range(SERVER_THREAD_COUNT):
            self.queue.put(None)
        w.join()


def main():
    imap = ImapDaemon()
    imap.run()

if __name__ == '__main__':
    main()
