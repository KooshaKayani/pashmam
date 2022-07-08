import tca9548a
from time import sleep
from PiicoDev_VEML6040 import PiicoDev_VEML6040
from PiicoDev_VL53L1X import PiicoDev_VL53L1X

try:
    Multiplexer = tca9548a.TCA9548A(0x70)
    for i in range(0,8):
        Multiplexer.set_channel(i,1)
    DistanceSensor = PiicoDev_VL53L1X()
    ColourSensor = PiicoDev_VEML6040()
except Exception as e:
    print("Sensor Import Error ",e)
Front_dis_chan = 6
Left_dis_chan = 7
Right_dis_chan = 5
LeftColour_chan= 0
RightColour_chan = 1

class SensorController:



    def __init__(self):
        self.idn = 0

    def Test(self,channel):
        return(Multiplexer.get_channel(channel))

    def Front_Distance(self, channel = Front_dis_chan):
        self.Close_All_Channels()
        Multiplexer.set_channel(channel,1)
        return DistanceSensor.read()

    def Left_Distance(self, channel = Left_dis_chan):
        self.Close_All_Channels()
        Multiplexer.set_channel(channel,1)
        return DistanceSensor.read()

    def Right_Distance(self, channel = Right_dis_chan):
        self.Close_All_Channels()
        Multiplexer.set_channel(channel,1)
        return DistanceSensor.read()

    def Left_Colour(self, channel = LeftColour_chan):
        self.Close_All_Channels()
        Multiplexer.set_channel(channel,1)
        return ColourSensor.readHSV()

    def Right_colour(self, channel = Right_dis_chan):
        self.Close_All_Channels()
        Multiplexer.set_channel(channel,1)
        return ColourSensor.readHSV()

    def Close_All_Channels(Self):
        for i in range(0,8):
            Multiplexer.set_channel(i,0)

