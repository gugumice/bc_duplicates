#!/usr/bin/env python3
import argparse
import logging
import requests, re, os
from requests.packages import urllib3

from subprocess import call
from dup_config import read_config
from bcr import bcr

wdObj=None
config=None
#Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#Start watchdog


def main():
    global wdObj

    parser = argparse.ArgumentParser(description='Find duplicate scans')
    parser.add_argument('-c','--config',
                        #type=argparse.FileType('r'),
                        type=str,
                        metavar='file',
                        help='Name config file. Default: config.ini',
                        default='config.ini'
                        )
    args = parser.parse_args()
    #Read from config file
    config = read_config(args.config)
    #Debug
    #print(config)

    #Assume all files are in working directory
    work_directory = os.getcwd()


    #Enable watchdog if not None
    if config['watchdog_device'] is not None:
        try:
            wdObj=open(config['watchdog_device'],'w')
            logging.info('Watchdog enabled on {}'.format(config['watchdog_device']))
        except Exception as e:
            logging.error(e)
    else:
        logging.info('Watchdog disabled')

    #Enable barcode reader obj
    b=bcr(port=config['bc_reader_port'], timeout = config['bc_timeout'])

    #Main loop-------------------------------------------------------------------------------------------------
    while b.running: 
        #Pat watchdog
        if wdObj is not None:
            print('1',file = wdObj, flush = True)
        
        bar_code = b.next()
        if bar_code is None:
            continue
        #Delete prefix if present
        if not bar_code[0].isnumeric():
            bar_code=bar_code[1:]
        #Check if parcode is valid
        req_code = re.search(config['bc_regex'] ,bar_code).group(0)
        #For testing take some old random value < 15000000
        #req_code = '16721710'
        if req_code is not None:
            #Form request string
            request_string = config['api_request_string'].format(req_code)
            response = requests.get(request_string,verify=False)
            if response.status_code != 200: #Bad response status
                try:
                    call(['aplay' '-q','{}/{}'.format(work_directory,config['conn_error_sound'])])
                except Exception as e:
                    logging.error('Error playing {}: {}'.format(config['conn_error_sound'],e))
                logging.error('Sample {}, Invalid response code: {}'.format(req_code,response.status_code))
            else:
                if response.text == '{"value": true}': #Sample already scanned
                    try:
                        call(['aplay', '-q','{}/{}'.format(work_directory,config['sample_already_scanned_sound'])])
                    except Exception as e:
                        logging.error('Error playing {}: {}'.format(config['sample_already_scanned_sound'],e))
                    logging.info('1,{} already scanned '.format(req_code))
                else: #Sample not scanned
                    try:
                        call(['aplay','-q','{}/{}'.format(work_directory,config['sample_not_scanned_sound'])])
                    except Exception as e:
                        logging.error('Error playing {}: {}'.format(config['sample_not_scanned_sound'],e))
                    logging.info('0, {} not scanned '.format(req_code))
    #End main loop -----------------------------------------------------------------------------------------------

if __name__ == "__main__":
    #logging.basicConfig(filename='/home/pi/dmitri.log',filemode='a',level=logging.INFO,format='%(message)s')
    logging.basicConfig(level=logging.INFO,format='%(message)s')
    try:
        main()
    except KeyboardInterrupt:
        if wdObj is not None:
            print('V',file = wdObj, flush = True)
            print("Disabling watchdog")
        print("\nExiting")