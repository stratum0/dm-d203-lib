import time
import serial
import sys


logo = (0xb8, 0xcc, 0xc2, 0xc9, 0xcd, 0xcc, 0xcc, 0xca, 0xc4, 0xb8, 0x8e, 0x99,
        0xb1, 0x83, 0x87, 0xc7, 0xa3, 0xb1, 0x99, 0x8e)

class open:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 19200)

    def __del__(self):
        self.ser.close();

    def send(self, data):
        a = len(data);
        lengs = 9;
        global ser;
        for i in range(0,a,lengs):
            print data[i:(i+lengs)]
            self.ser.write(data[i:(i+lengs)]);
            time.sleep(0.01);
    
    def def_char(self, offset, data):
        self.send("\x1b\x26\x01"); #Define user-defined characters;
        self.send(("%c") % (offset&0xff));
        self.send(("%c") % (offset&0xff));
        self.send("\x05");
        for i in data:
            self.send(("%c")%i);
    
    def clear(self):
        self.send("\x0c\x0b");
    
    def def_logo(self):
        teile = len(logo)/5;
        for i in range(0,teile):
            offset=i*5;
            temp = logo[offset:(offset+5)];
            self.def_char((0x21+i),temp);
        self.send("\x1b\x25\x01");
    
    def logo(self):
        self.send("\x23\x24\x08\x08\x0a\x21\x22");

    def home(self):
        self.send("\x0b");

    def set(self,x,y):
        if((1 <= x) & ( x <= 20) & ( y >= 1) & (y <= 2)):
            self.send("\x1f\x24" + ("%c%c") % (x,y));
            return 0;
        else:
            return -1;
    def uhr(self,h,m):
        self.send(("\x1f\x54%c%c\x1f\x55") % (h,m));
    def bright(self,l):
        if((l <= 4) & (l >=1)):
            self.send(("\x1f\x58%c") % l);
    def blink(self,inter):
        if((inter <= 255) & ( inter >= 0)):
            self.send(("\x1f\x45%c") % inter);

