#!/usr/bin/env python3
#https://arhivs.egl.local/api/does-repeat?12345678
#request_number=XXXXXXX
#https://arhivs.egl.local/api/does-repeat-ui
import serial
import logging
class bcr(object):
    def __init__(self,port='/dev/ttyACM0',timeout=1):
        self.bc=None
        self.running=False
        try:
            self.bc=serial.Serial(port=port,timeout=timeout)
            self.running=True
        except Exception as e:
            logging.error('{}'.format(e))
    def next(self):
        try:
            buffer=self.bc.readline()
            barcode=buffer.decode('UTF-8').strip() 
        except Exception as e:
            logging.error(e)
            self.running=False
        return(barcode if len(barcode)>0 else None)
def main():
    b=bcr()
    while b.running:
        bar_code=b.next()
        if bar_code is None:
            continue
        print(bar_code)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting")
