import time
import serial
import sys


logo = (0xb8, 0xcc, 0xc2, 0xc9, 0xcd, 0xcc, 0xcc, 0xca, 0xc4, 0xb8, 0x8e, 0x99,
        0xb1, 0x83, 0x87, 0xc7, 0xa3, 0xb1, 0x99, 0x8e)
## Stratum0 e.V. Logo

class open:
    def __init__(self, serial, baud):
        self.ser = serial.Serial(serial, baud)

    def __del__(self):
        self.ser.close();

    def send(self, data):
        a = len(data);
        lengs = 9;
        if a<lengs:
            seld.ser.write(data)
            if __debug__:
                print data;
        else:
            for i in range(0,a,lengs):
                if __debug__:
                    print data[i:(i+lengs)]
                self.ser.write(data[i:(i+lengs)]);
                time.sleep(0.01);
    
            ## definiert eigenes Zeichen, 4 sind möglich
    def def_char(self, offset, data):
        self.send(("\x1b\x26\x01%c%c\x05") % ((offset&0xff), (offset&0xff)))
        time.sleep(0.01)
        for i in data:
            self.send(("%c")%i);
    
    def clear(self):
        self.send("\x0c\x0b");
            ##  definiert 4 eigen Zeichen für das Logo
            ##  addr ist die start adresse 0x21
    def def_logo(self, addr):
        teile = len(logo)/5;
        for i in range(0,teile):
            offset=i*5;
            temp = logo[offset:(offset+5)];
            self.def_char((addr+i),temp);
        self.send("\x1b\x25\x01"); # wechsel zu selbst definirten zeichen
    
    def logo(self):     ## TODO unguenstig adresse
        self.send("\x23\x24\x08\x08\x0a\x21\x22");

            ## set cursor to home
    def home(self):
        self.send("\x0b");
            ## set cursor to x,y min 1
    def set(self,x,y):
        if((1 <= x) & ( x <= 20) & ( y >= 1) & (y <= 2)):
            self.send("\x1f\x24" + ("%c%c") % (x,y));
            return 0;
        else:
            return -1;

            ## setzt Uhrzeit und zeigt Uhr in der unteren ziele an.
            ## die Uhr verschwindet sobald in die untere Zeile geschrieben wird
    def uhr(self,h,m):
        self.send(("\x1f\x54%c%c\x1f\x55") % (h,m));
            ## setzt Helligkeit 
    def bright(self,l):
        if((l <= 4) & (l >=1)):
            self.send(("\x1f\x58%c") % l);
            ## lest das Display blinken 
    def blink(self,inter):
        if((inter <= 255) & ( inter >= 0)):
            self.send(("\x1f\x45%c") % inter);
            ## Initialisierung des Displays
    def init(self):
        self.send("\x1b\x40");
