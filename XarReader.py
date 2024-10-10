from HTMLParser import HTMLParser
from math import radians

### This parser is used to scrape the animation data from the blocks of Choregraphe. It is not meant to be used for any other .xar file, despite its name. ###
### These files can be found in C:\Program Files (x86)\Softbank Robotics\Choregraphe Suite <version>\share\choregraphe\libraries\box\Animation on windows. ###

class XarReader(HTMLParser):
    """
    Reads a .xar file and saves the resulting Bezier interpolation data, which you can get with .get_data()
    """
    def __init__(self, path, spf=0.04):
        with open(path, "r") as f:
            s = f.read()

        self.reset()
        self.curract = ""
        self.cursor = -1
        self.spf = spf

        self.joints = []
        self.angles = []
        self.times = []

        self.feed(s)
    def handle_starttag(self, tag, attrs):
        if(tag == "actuatorcurve"):
            self.joints.append(attrs[1][1])
            self.cursor += 1
            self.angles.append([])
            self.times.append([])
        elif(tag == "key"):
            time = float(attrs[0][1])*self.spf
            self.times[self.cursor].append(time)

            angle = radians(float(attrs[1][1]))
            self.angles[self.cursor].append(angle)
    def handle_endtag(self, tag):
        pass
    def handle_data(self, data):
        pass
    def get_data(self):
        return [self.joints, self.times, self.angles]