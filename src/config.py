__author__ = 'myhay'

import ConfigParser

class ConfigFile:
    def __init__(self,time_to_start,clients_number,sound_folder,number_sounds):
        self.time_to_start = time_to_start
        self.clients_number = clients_number
        self.sound_folder = sound_folder
        self.number_sounds = number_sounds
        self.Sound_List_Pos = []

    def add_sound(self,filename,posX,posY):
        self.Sound_List_Pos.append( (filename,(posX,posY)))



def createConfigFile(configFileName = "../config/example.cfg"):
    config = ConfigParser.RawConfigParser()

    # When adding sections or items, add them in the reverse order of
    # how you want them to be displayed in the actual file.
    # In addition, please note that using RawConfigParser's and the raw
    # mode of ConfigParser's respective set functions, you can assign
    # non-string values to keys internally, but will receive an error
    # when attempting to write to a file or when you get it in non-raw
    # mode. SafeConfigParser does not allow such assignments to take place.
    config.add_section('Server')
    config.set('Server', 'time_to_start', '10')
    config.set('Server', 'clients_number', '30')

    config.add_section('Sound')
    config.set('Sound', 'sound_folder', './../bin/sound/')
    config.set('Sound', 'number_sounds', '4')


    config.add_section('Sound_List')
    config.set('Sound_List', 'file_name1', "001_piano.wav")
    config.set('Sound_List', 'file_name2', "voz4408.wav")
    config.set('Sound_List', 'file_name3', "001_bajo.wav")
    config.set('Sound_List', 'file_name4', "001_bateriabuena.wav")

    # Writing our configuration file to 'example.cfg'
    with open(configFileName, 'wb') as configfile:
        config.write(configfile)

    return True


def readConfigFile(configFileName = "../config/default.cfg"):
    config = ConfigParser.RawConfigParser()
    config.read(configFileName)

    time_to_start = config.getint('Server', 'time_to_start')
    clients_number = config.getint('Server', 'clients_number')


    sound_folder = config.get('Sound', 'sound_folder')
    number_sounds = config.getint('Sound', 'number_sounds')

    configResult = ConfigFile(time_to_start, clients_number, sound_folder, number_sounds)

    path_items = config.items( "Sound_List" )
    for key, songName in path_items:
        #do something with path
        #print key, songName
        configResult.add_sound(songName,0,11)

    return configResult

#createConfigFile("../config/default.cfg")

c = readConfigFile()
for songPos in c.Sound_List_Pos:
    print songPos[0], songPos[1][0], songPos[1][1]