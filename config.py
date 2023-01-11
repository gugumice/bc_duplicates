#!/usr/bin/env python3
import configparser
import os, logging
conf_file='{}/{}'.format(os.getcwd(),'config.ini')
def read_config(conf_file):   
    #Defaults
    config={
        'wdObj': None,
        'bc_regex': '^\d{7,9}',
        'api_request_string': 'https://arhivs.egl.local/api/does-repeat?request_number={}',
        'conn_error_sound': 'glassbreak_2.wav',
        'sample_already_scanned_sound': 'bleep_02.wav',
        'sample_not_scanned_sound' : 'pop3.wav'
        }
    
    cf = configparser.ConfigParser(allow_no_value=True)
    try:
        cf.read(conf_file)
        
    except Exception as e:
        logging.error(e)
    return(config)

def main():
    print(read_config('config.ini'))
if __name__ == '__main__':
    main()
