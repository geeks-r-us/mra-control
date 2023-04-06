import hid
from enum import Enum
from audio_manager import audio_manager

class Gain (Enum):
    GAIN25_6dB = 0
    GAIN31_6dB = 2
    GAIN35_6dB = 1
    GAIN37_6dB = 3

    def __str__(self):
        return self.name
    
    @staticmethod
    def from_string(s):
        try:
            return Gain[s]
        except KeyError:
            raise ValueError()

class mra_device:
    __device = None
    __bitmask = 0b00001111 # currently the GPIO 0-3 outputs // 4 - 7 inputs
    __states =  0b00000000 # inital states of GPIOs

    def __init__(self, vid, pid, serial):
        self.__device = hid.Device(vid, pid)
   
    def __init__(self, path):
        self.__device = hid.Device(path=str.encode(path))

    def __del__(self):
        self.__device.close()

    def __modifyBit( self, input,  position,  bitstate):
        mask = 1 << position
        return (input & ~mask) | ((bitstate << position) & mask)

    def set_gpio(self, num, state):
        self.__states = self.__modifyBit(self.__states, num - 1, state)
        try:
            data = bytes([0,0,self.__bitmask,self.__states,0])
            self.__device.write(data)
            data = self.__device.read(5,10)
        except hid.DeviceError as e:
            print(f"Error setting GPIO: {e}")
        except IndexError as e:
            print(f"Invalid GPIO number: {e}")  

    def mute(self, state):
        output = 0 if state else 1
        self.set_gpio(4, output)

    def standby(self, state):
        output = 0 if state else 1
        self.set_gpio(3, output)

    def set_gain(self, gain : Gain):
        self.set_gpio(1, gain.value & (1 << 0))
        self.set_gpio(2, (gain.value & (1 << 1)) >> 1)
    
def main(args):
    if args.command == 'list':
        list = audio_manager.enumerate_sounddevices()
        for device in list:
            if device.usb_device is not None:
                print(f'Name: {device.get_name()} \t {device.usb_device.device_node}')
        
    elif args.command == 'control':
        device = mra_device(path=args.path[0])
        
        if args.standby is not None:
            print("Standby: " + str(args.standby))
            device.standby(args.standby)
        
        if args.mute is not None:
            print("Mute: " + str(args.mute))
            device.mute(args.mute)

        if args.gain is not None:
            print("Gain: " + str(args.gain))
            device.set_gain(args.gain)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='control a geeks-r-us audio module')
    subparsers = parser.add_subparsers(dest='command')

    # Subparser for the list command
    list_parser = subparsers.add_parser('list', help='lists available modules')

    # Subparser for the main command
    main_parser = subparsers.add_parser('control', help='control a geeks-r-us audio module')
    main_parser.add_argument('--standby', default=False, type=lambda x: (str(x).lower() == 'true'), help='turns audio module standby on / off')
    main_parser.add_argument('--mute', default=False, type=lambda x: (str(x).lower() == 'true'), help='mutes / unmutes the module')
    main_parser.add_argument('--gain', type=Gain.from_string, choices=list(Gain), help='sets the gain level of the module')
    main_parser.add_argument('path', type=str, nargs=1, help='path of the audio module' )

    args = parser.parse_args()

    main(args)
    quit()
