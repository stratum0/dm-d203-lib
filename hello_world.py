#!/usr/bin/env python

import dm_d203
from time import sleep

c = dm_d203.Kassendisplay("/dev/ttyUSB0", 9600)
c.init()

c.full_logo()
sleep(2)

c.clear()
c.send("Hello World!")
