__author__ = 'myhay'

import ConfigParser

class ConfigFile:
    def __init__(self, time_to_start, clients_number, sound_folder, number_sounds):
        self.time_to_start = time_to_start
        self.clients_number = clients_number
        self.sound_folder = sound_folder
        self.number_sounds = number_sounds
        self.Sound_List_Pos = []
        self.clientPos = ()
        self.inicialSongPos = ()

    def add_sound(self, filename, posx, posy):
        self.Sound_List_Pos.append( (filename,(posx,posy)))

    def set_client_pos(self, posx, posy):
        self.clientPos = (posx, posy)

    def set_sound_inicial_pos(self, posx, posy):
        self.inicialSongPos = (posx, posy)



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

    config.add_section('ClientPos')
    config.set('ClientPos', 'posx', '6')
    config.set('ClientPos', 'posy', '5')

    config.add_section('SoundPos')
    config.set('SoundPos', 'posx', '11')
    config.set('SoundPos', 'posy', '0')

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

    config_result = ConfigFile(time_to_start, clients_number, sound_folder, number_sounds)

    client_pos = (config.getint('ClientPos', 'posx'), config.getint('ClientPos', 'posy'))
    config_result.set_client_pos(client_pos[0], client_pos[1])

    sound_pos = (config.getint('SoundPos', 'posx'), config.getint('SoundPos', 'posy'))
    config_result.set_sound_inicial_pos(sound_pos[0], sound_pos[1])

    path_items = config.items("Sound_List")
    for key, songName in path_items:
        config_result.add_sound(songName, sound_pos[0], sound_pos[1])

    return config_result

#createConfigFile("../config/default.cfg")

c = readConfigFile()
#for songPos in c.Sound_List_Pos:
#    print songPos[0], songPos[1][0], songPos[1][1]

#print c.Sound_List_Pos[0][0]