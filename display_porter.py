#!/usr/bin/python3
# import epd7in5b
# import epd7in5b_V2
import requests
import sys
import os
import re
import time
import json
import datetime
from pyquery import PyQuery
from PIL import Image, ImageDraw, ImageFont

libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd7in5b_V2

class Porter:

    def __init__(self) -> None:
        self.epd = epd7in5b_V2.EPD()
        self.epd_width = 800
        self.epd_height = 480
        self.epd.init()

    def query_porter(self):
        pq = PyQuery(requests.get("http://porter.arcade.ch").content)
        self.raw_response = str(pq('p'))
        self.format_text()

    def format_text(self):
        self.raw_response = self.raw_response.replace("<p>", "")
        self.raw_response = self.raw_response.replace("</p>", "")
        self.raw_response = self.raw_response.replace("\t", "          ")
        self.response = re.sub(
            r" Gi1\/0\/[0-9][ ]", r"\g<0>  ", self.raw_response)
        # print(self.response)

    def print_screen(self):
        self.epd.Clear()
        out = Image.new(
            "1", (self.epd_height, self.epd_width), (255))
        out2 = Image.new(
            "1", (self.epd_height, self.epd_width), (255))
        fnt = ImageFont.truetype("Roboto/Font.ttc", 15)
        fnt_big = ImageFont.truetype("Roboto/Font.ttc", 28)
        d = ImageDraw.Draw(out)
        # d.multiline_text((10, 50), self.response, font=fnt, fill=(0))
        d.text((10, 50), "Test 12345 VVV", font = fnt_big, fill = (0))
        # d.text((100, 20), "Test", font = fnt, fill = 0)
        # d.chord((200, 50, 250, 100), 0, 360, fill = 0)
        self.epd.display(self.epd.getbuffer(out), self.epd.getbuffer(out2))
        time.sleep(300)


screen = Porter()
while True:
    screen.query_porter()
    screen.print_screen()
