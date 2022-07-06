import pygame

from json import load as json_load
from random import choice


class ResourceHandler:
    _COLORKEY = (0, 0, 0)
    _BASE_VOLUME = 0.5

    def __init__(self, assets_path: str):
        """
        Class used to access all data
        Must be created only once
        """

        self.path = assets_path
        self.images = {}
        self.sounds = {}
        self.data = {}

        self.shaders = {}

        self.pre_init()

    def pre_init(self):
        """pre_init to search system variables like screen size"""
        self.load_data()

    def init(self):
        """init to search images and sounds. Must be called after the window as been initialized"""
        self.load_sounds()
        self.load_images()

    def load_data(self):
        with open(f"{self.path}/data/data_index.json") as data_index_file:
            data_index_dict = json_load(data_index_file)

        self.extract_data_dictionary(data_index_dict, f"{self.path}/data/")

    def load_sounds(self):
        with open(f"{self.path}/sounds/sound_index.json") as sound_json_file:
            sound_json_dict = json_load(sound_json_file)

        self.extract_sound_dictionary(sound_json_dict, f"{self.path}/sounds/")

    def load_images(self):
        with open(f"{self.path}/images/image_index.json") as image_json_file:
            image_json_dict = json_load(image_json_file)

        self.extract_image_dictionary(image_json_dict, f"{self.path}/images/")

    def extract_data_dictionary(self, dictionary: dict, path: str, receiving_dict: dict = None):
        if receiving_dict is None:
            receiving_dict = self.data

        for key in dictionary:
            if type(dictionary[key]) == str:
                data_file = open(path+dictionary[key])
                receiving_dict[key] = json_load(data_file)
                data_file.close()
            else:
                new_path = path + key + "/"
                receiving_dict[key] = {}
                self.extract_data_dictionary(dictionary[key], new_path, receiving_dict[key])

    def extract_sound_dictionary(self, dictionary: dict, path: str, receiving_dict: dict = None):
        if receiving_dict is None:
            receiving_dict = self.sounds

        for key in dictionary:
            if type(dictionary[key]) == str:
                receiving_dict[key] = pygame.mixer.Sound(path+dictionary[key])
                receiving_dict[key].set_volume(self._BASE_VOLUME)
            else:
                new_path = path + key + "/"
                receiving_dict[key] = {}
                self.extract_sound_dictionary(dictionary[key], new_path, receiving_dict[key])

    def extract_image_dictionary(self, dictionary: dict, path: str, receiving_dict: dict = None):
        if receiving_dict is None:
            receiving_dict = self.images

        for key in dictionary:
            if type(dictionary[key]) == str:
                new_img = pygame.image.load(path+dictionary[key]).convert()
                new_img.set_colorkey(self._COLORKEY)
                receiving_dict[key] = new_img

            else:
                new_path = path + key + "/"
                receiving_dict[key] = {}
                self.extract_image_dictionary(dictionary[key], new_path, receiving_dict[key])

    def fetch_sound(self, keys=()):
        sub_dict = self.sounds
        for key in keys:
            if type(sub_dict[key]) == dict:
                sub_dict = sub_dict[key]
            else:
                return sub_dict[key]

        while True:
            keys = list(sub_dict.keys())
            key = choice(keys)
            if type(sub_dict[key]) == dict:
                sub_dict = sub_dict[key]
            else:
                return sub_dict[key]

    def fetch_data(self, keys=()):
        sub_dict = self.data
        for key in keys:
            sub_dict = sub_dict[key]
        return sub_dict

    def play_sound(self, keys=(), channel=None):
        if channel:
            channel.play(self.fetch_sound(keys))
            return None
        return self.fetch_sound(keys).play()


if __name__ == '__main__':
    x = ResourceHandler("../../assets")
