#!/usr/bin/env python3
#Sound files from https://www.freespecialeffects.co.uk/

from bcr import bcr
import logging, re, requests, os
from subprocess import call
#Watchdog device name - Node: WD disabled 
WD=None
#WD='/dev/watchdog'
#WD object
wdObj=None
bc_regex = '^\d{7,9}'
api_request_string = 'https://arhivs.egl.local/api/does-repeat?request_number={}'
conn_error_sound='glassbreak_2.wav'
sample_already_scanned_sound = 'bleep_02.wav'
sample_not_scanned_sound = 'pop3.wav'

def start_watchog(watchdog_device):
    dev=None
    if watchdog_device is not None:
        try:
            dev=open(watchdog_device,'w')
        except Exception as e:
            logging.info(e)
    logging.info("Watchdog {}".format('enabled' if dev is not None else 'disabled'))
    return(dev)

def main():
    b=bcr()
    work_directory = os.getcwd()
    while b.running:
        bar_code = b.next()
        if bar_code is None:
            continue
        #Delete prefix if present
        if not bar_code[0].isnumeric():
            bar_code=bar_code[1:]
        #Check if parcode is valid
        req_code = re.search(bc_regex ,bar_code).group(0)
        #For testing take some old random value < 15000000
        #req_code = '16721710'
        if req_code is not None:
            #Form request string
            request_string = api_request_string.format(req_code)
            response = requests.get(request_string,verify=False)
            if response.status_code != 200: #Bad response status
                call(['aplay','{}/{}'.format(work_directory,conn_error_sound)])
                logging.error('Sample {}, Invalid response code: {}'.format(req_code,response.status_code))
            else:
                if response.text == '{"value": true}': #Sample already scanned
                    call(['aplay','{}/{}'.format(work_directory,sample_already_scanned_wav)])
                    logging.info('1,{} already scanned '.format(req_code))
                else: #Sample not scanned
                    call(['aplay','{}/{}'.format(work_directory,sample_not_scanned_wav)])
                    logging.info('0, {} not scanned '.format(req_code))

if __name__ == "__main__":
    #logging.basicConfig(filename='/home/pi/dmitri.log',filemode='a',level=logging.INFO,format='%(message)s')
    logging.basicConfig(level=logging.INFO,format='%(message)s')
    try:
        main()
    except KeyboardInterrupt:
        if wdObj is not None:
            print('V',file = wdObj, flush = True)
        print("\nExiting")
