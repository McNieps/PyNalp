import pygame

from json import load as json_load
from random import choice
from typing import Dict, Union


class ResourceHandler:
    """
    Class used to access all data
    """

    path: str = ""

    images: Dict[str, Union[pygame.Surface, Dict]] = {}
    sounds: Dict[str, Union[pygame.mixer.Sound, Dict]] = {}
    data: Dict[str, Dict[str, Dict[str, Union[int, float, str, tuple[int, int], bool]]]] = {}
    fonts: Dict[Union[str, None], Dict[int, pygame.font.Font]] = {}

    pre_initialized: bool = False
    initialized: bool = False

    @classmethod
    def pre_init(cls,
                 path: str = None):
        """pre_init to search system variables like screen size"""

        if path is not None:
            cls.path = path.lstrip("/")

        cls._load_data()

        cls.pre_initialized = True

    @classmethod
    def init(cls):
        """init to search images and sounds. Must be called after the window as been initialized"""

        cls.fonts[None] = {10: pygame.font.Font(None, 10)}
        cls._load_sounds()
        cls._load_images()

        cls.initialized = True

    @classmethod
    def _load_data(cls):

        with open(f"{cls.path}/data/data_index.json") as data_index_file:
            data_index_dict = json_load(data_index_file)

        cls._extract_data_dictionary(data_index_dict, f"{cls.path}/data/")

    @classmethod
    def _load_sounds(cls):

        with open(f"{cls.path}/sounds/sound_index.json") as sound_json_file:
            sound_json_dict = json_load(sound_json_file)

        cls._extract_sound_dictionary(sound_json_dict, f"{cls.path}/sounds/")

    @classmethod
    def _load_images(cls):

        with open(f"{cls.path}/images/image_index.json") as image_json_file:
            image_json_dict = json_load(image_json_file)

        cls._extract_image_dictionary(image_json_dict, f"{cls.path}/images/")

    @classmethod
    def _extract_data_dictionary(cls,
                                 dictionary: dict,
                                 path: str,
                                 receiving_dict: dict = None):

        if receiving_dict is None:
            receiving_dict = cls.data

        for key in dictionary:
            if type(dictionary[key]) == str:
                data_file = open(path+dictionary[key])
                receiving_dict[key] = json_load(data_file)
                data_file.close()
            else:
                new_path = path + key + "/"
                receiving_dict[key] = {}
                cls._extract_data_dictionary(dictionary[key], new_path, receiving_dict[key])

    @classmethod
    def _extract_sound_dictionary(cls,
                                  dictionary: dict,
                                  path: str,
                                  receiving_dict: dict = None):

        volume = cls.data["sys"]["audio"]["base_volume"]

        if receiving_dict is None:
            receiving_dict = cls.sounds

        for key in dictionary:
            if type(dictionary[key]) == str:
                receiving_dict[key] = pygame.mixer.Sound(path+dictionary[key])
                receiving_dict[key].set_volume(volume)
            else:
                new_path = path + key + "/"
                receiving_dict[key] = {}
                cls._extract_sound_dictionary(dictionary[key], new_path, receiving_dict[key])

    @classmethod
    def _extract_image_dictionary(cls,
                                  dictionary: dict,
                                  path: str,
                                  receiving_dict: dict = None):

        if receiving_dict is None:
            receiving_dict = cls.images

        for key in dictionary:
            if type(dictionary[key]) == str:
                new_img = pygame.image.load(path+dictionary[key]).convert_alpha()
                # new_img.set_colorkey(self._COLORKEY)
                receiving_dict[key] = new_img

            else:
                new_path = path + key + "/"
                receiving_dict[key] = {}
                cls._extract_image_dictionary(dictionary[key], new_path, receiving_dict[key])

    @classmethod
    def _fetch_sound(cls,
                     keys=()):

        sub_dict = cls.sounds
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

    @classmethod
    def play_sound(cls,
                   keys=(),
                   channel=None):

        if channel:
            channel.play(cls._fetch_sound(keys))
            return None
        return cls._fetch_sound(keys).play()

    @classmethod
    def render_text(cls,
                    text: str,
                    color: tuple[int, int, int] = (255, 255, 255),
                    font_name: str = None,
                    font_size: int = 10,
                    antialias: bool = False) -> pygame.Surface:

        if font_name not in cls.fonts:
            cls.fonts[font_name] = {font_size: pygame.font.Font(f"{cls.path}/fonts/{font_name}.ttf", font_size)}

        elif font_size not in cls.fonts[font_name]:
            if font_name is None:
                cls.fonts[font_name][font_size] = pygame.font.Font(None, font_size)
            else:
                cls.fonts[font_name][font_size] = pygame.font.Font(f"{cls.path}/fonts/{font_name}.ttf", font_size)

        return cls.fonts[font_name][font_size].render(text, antialias, color)


if __name__ == '__main__':
    ResourceHandler.path = "../../../assets"
    ResourceHandler.pre_init()
