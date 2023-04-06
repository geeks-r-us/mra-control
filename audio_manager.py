import pyudev

class audio_device:
    def __init__(self):
        self.audio_device = None
        self.usb_device = None
    
    def get_name(self):
        name = ""
        try:
            name = self.audio_device.properties['ID_MODEL_ENC'].encode().decode("unicode-escape")
        except KeyError as ex:
            pass

        try:
            name = self.audio_device.properties['ID_MODEL_FROM_DATABASE']
        except KeyError:
            pass
        
        return name


class audio_manager:
    def enumerate_sounddevices():
        audio_devices = []
        context = pyudev.Context()
        for device in context.list_devices(subsystem='sound', TAGS=':seat:'):
            audio_dev = audio_device()
            audio_dev.audio_device = device
            audio_devices.append(audio_dev)

        for device in context.list_devices(subsystem='hidraw'):
            for audio_dev in audio_devices:
                if audio_dev.audio_device.properties['ID_BUS'] == 'usb':
                    if audio_dev.audio_device.parent.parent == device.parent.parent.parent:
                        audio_dev.usb_device = device

        return audio_devices

    