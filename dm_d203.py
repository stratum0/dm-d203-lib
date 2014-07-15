import time
import serial
import string
import sys


logo = (0xb8, 0xcc, 0xc2, 0xc9, 0xcd, 0xcc, 0xcc, 0xca, 0xc4, 0xb8, 0x8e, 0x99,
        0xb1, 0x83, 0x87, 0xc7, 0xa3, 0xb1, 0x99, 0x8e)
## Stratum0 e.V. Logo

class Kassendisplay:
    def __init__(self, path, baud):
        self.ser = serial.Serial(path, baud)

    def __del__(self):
        self.ser.close()

    def send(self, data):
        """send arbitary data"""
        a = len(data)
        lengs = 9
        if a<lengs:
            self.ser.write(data)
        else:
            for i in range(0,a,lengs):
                self.ser.write(data[i:(i+lengs)])
                time.sleep(0.01)
    
    def def_char(self, offset, data):
        """defines a single char in the user codepage"""
        self.send(("\x1b\x26\x01%c%c\x05") % ((offset&0xff), (offset&0xff)))
        time.sleep(0.01)
        for i in data:
            self.send(("%c")%i)
    
    def clear(self):
        """clear the screen"""
        self.send("\x0c\x0b")

    def def_logo(self, addr):
        """replaces 4 chars in the code page with the S0 logo starting at addr"""
        teile = len(logo)/5
        for i in range(0,teile):
            offset=i*5
            temp = logo[offset:(offset+5)]
            self.def_char((addr+i),temp)
        self.send("\x1b\x25\x01")
    
    def logo(self):
        """prints the S0 logo"""
        self.def_logo(0x21)
        self.send("\x21\x22\x08\x08\x0a\x23\x24")
        self.reset_codepage()

    def reset_codepage(self):
        """resets the codepage"""
        self.send('\x1b%\x00')

    def full_logo(self):
        """prints our logo and title"""
        self.def_logo(0x21)
        self.clear()
        self.send('!"Stratum 0  Hacker-#$space Braunschweig')
        self.reset_codepage()

    def home(self):
        """sets the cursor to 1,1"""
        self.send("\x0b")

    def set_cursor(self,x,y):
        """sets the cursor position"""
        if 1 <= x <= 20 and y in [1,2]:
            self.send("\x1f\x24%c%c" % (x,y))
        else:
            raise ValueError('cursor position must be between 1,20 and 1,2')

    def print_clock(self,h,m):
        """prints the time"""
        self.send(("\x1f\x54%c%c\x1f\x55") % (h,m))

    def bright(self,l):
        """set the brightness of the display"""
        if 1 <= l <= 4:
            self.send("\x1f\x58%c" % l)
        else:
            raise ValueError('brightness values have to be between 1 and 4')

    def blink(self,inter):
        """makes the display blink with the given period"""
        if 0 <= inter <= 255:
            self.send("\x1f\x45%c" % inter)
        else:
            raise ValueError('blink values have to be between 0 and 255')

    def init(self):
        """initializes the display"""
        self.send("\x1b\x40")

    def open_close(self, is_open, name='', t=None):
        """prints an open/close message"""
        if t is None:
            t = time.localtime()
        self.clear()
        self.logo()
        self.set_cursor(4,1)
        if is_open:
            self.send('auf %s' % string.rjust(name, 13)[:13])
        else:
            self.send('geschlossen')
        self.set_cursor(4,2)
        self.send(time.strftime('seit %d.%m. %H:%M', t))

