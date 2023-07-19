# import epd7in5b
# import epd7in5b_V2
import requests
import sys
import re
import json
import datetime
from pyquery import PyQuery
from PIL import Image, ImageDraw, ImageFont


class Porter:

    def __init__(self) -> None:
        # self.epd = epd7in5b_V2.EPD()
        self.epd_width = 800
        self.epd_height = 480

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
        out = Image.new(
            "RGB", (self.epd_width, self.epd_height), (255, 255, 255))
        fnt = ImageFont.truetype("Roboto/Roboto-Light.ttf", 11)
        d = ImageDraw.Draw(out)
        d.multiline_text((100, 20), self.response, font=fnt, fill=(0, 0, 0))
        # self.epd.display(self.response)
        # out.save("test.png")


screen = Porter()
screen.query_porter()
screen.print_screen()
