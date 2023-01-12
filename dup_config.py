#!/usr/bin/env python3
import configparser
import os, logging
conf_file='{}/{}'.format(os.getcwd(),'config.ini')
def read_config(conf_file):   
    #Defaults
    config={
        'watchdog_device': None,
        'log_file': 'dupl.log',
        'bc_reader_port': '/dev/ttyACM0',
        'bc_timeout' : 1,
        'bc_regex': '^\d{7,9}',
        'api_request_string': 'https://arhivs.egl.local/api/does-repeat?request_number={}',
        'conn_error_sound': 'glassbreak_2.wav',
        'sample_already_scanned_sound': 'bleep_02.wav',
        'sample_not_scanned_sound' : 'pop3.wav'
        }
    
    cf = configparser.ConfigParser(allow_no_value=True)
    try:
        cf.read(conf_file)
        config['watchdog_device'] = cf.get('IFACE','watchdog_device')
        config['log_file'] = cf.get('IFACE','log_file')
        config['bc_reader_port'] = cf.get('IFACE','bc_reader_port')
        config['bc_timeout'] = cf.getint('IFACE','bc_timeout')
        config['bc_regex'] = cf.get('IFACE','bc_regex')

        config['api_request_string'] = cf.get('API','api_request_string')
        config['conn_error_sound'] = cf.get('SOUNDS','conn_error_sound')
        config['sample_already_scanned_sound'] = cf.get('SOUNDS','sample_already_scanned_sound')
        config['sample_not_scanned_sound'] = cf.get('SOUNDS','sample_not_scanned_sound')
    except Exception as e:
        logging.error('Error reading {}: {}'.format(conf_file,e))
    return(config)

def main():
    logging.basicConfig(level=logging.INFO,format='%(message)s')
    print(read_config('config.ini'))
if __name__ == '__main__':
    main()
