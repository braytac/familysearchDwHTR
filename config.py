import configparser

class Configurations:

    def __init__(self):
        self.config_parser = configparser.ConfigParser()

    def create(self):
            # creo archivo conf si no existe
            self.config_parser['DEFAULT'] = {'username': '',
                                'password': '',
                                'defaut_file': 'record-image_.jpg',
                                'workdir': '',
                                'microfilm': 'https://www.familysearch.org/ark:/61903/3:1:3QSQ-G92H-L4DZ?i=2&cat=25735',
                                'hold_imgs': '1'
                                }

            with open('config.ini', 'w') as configfile:
                self.config_parser.write(configfile)


    def read(self):
        try:
            # Leo archivo existente
            self.config_parser.read('config.ini')

            user = self.config_parser['DEFAULT']['username']
            passw = self.config_parser['DEFAULT']['password']
            jpgfile = self.config_parser['DEFAULT']['defaut_file']
            workdir = self.config_parser['DEFAULT']['workdir']
            microfilm = self.config_parser['DEFAULT']['microfilm']
            hold_imgs = self.config_parser['DEFAULT']['hold_imgs']

            return user, passw, jpgfile, microfilm, workdir, hold_imgs

        except:
            self.create()
            return self.read()

    def update(self, user, passw, jpgfile, microfilm, workdir, hold_imgs):

        self.config_parser['DEFAULT'] = {'username': user,
                                        'password': passw,
                                        'defaut_file': jpgfile,
                                        'workdir': workdir,
                                        'microfilm': microfilm,
                                        'hold_imgs': hold_imgs
                                        }

        with open('config.ini', 'w') as configfile:
            self.config_parser.write(configfile)

