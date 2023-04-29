import os
from PIL import Image
import sys
from random import choice


class FileManager:
    PATH_TO_STATIC = '/home/funeralclown/yarmarka/static' if sys.platform == 'linux' else 'C:\\Users\\svr01\\PycharmProjects\\yarmarka\\static\\'

    def __init__(self, path: str):
        self.path_link = path
        self.path = path.lstrip("&").replace("&", "/").replace("&&", "/")
        self.path_back = '&'.join(self.path.split("/")[:-1])
        self.path_back = self.path_back if self.path_back else 'gallery'

        self.s_path = f'{FileManager.PATH_TO_STATIC}/{self.path}'

        self.name = str(self.path.split('/')[-1])

        self.dirs = sorted(list(os.walk(self.s_path))[0][1])
        self.img = self.__sort_files(list(os.walk(self.s_path))[0][2])

        self.catalog = self.__create_catalog()
        self.catalog_list = list(self.catalog.keys())
        self.inf = {
            'name': self.name,
            'path': f'{self.path.replace("/", "&")}'
        }

    def add_img(self, files, resize=True):
        if isinstance(files, list):
            for file in files:
                if file.filename:
                    path_to_img = f'{self.s_path}/{file.filename.lower()}'
                    with open(path_to_img, 'wb') as img:
                        img.write(file.read())
                    if resize:
                        with Image.open(path_to_img) as img:
                            img.load()
                            size = img.width if img.width > img.height else img.height
                            proportion = size / 1000
                            proportion = proportion if proportion > 1 else 1
                            img = img.resize((round(img.width / proportion),
                                              round(img.height / proportion)))
                            img.save(path_to_img)

    def create_dir(self, name):
        os.mkdir(f'{self.s_path}/{name}')

    def del_dir(self):
        os.rmdir(f'{self.s_path}')
        self.inf['path'] = '&'.join(self.inf['path'].split('&')[:-1])

    def del_img(self, name):
        os.remove(f'{self.s_path}/{name}')

    def __create_catalog(self):
        catalog = {}
        for dir_child in self.dirs:
            catalog[dir_child] = {'path': f'{self.path.replace("/", "&")}&{dir_child}',
                                  'preview': self.__get_preview(dir_child),
                                  'preview_link': f'{self.path}/{dir_child}',
                                  'count': self.__get_count_files(dir_child)}
        return catalog

    def __sort_files(self, files):
        formats = {'jpg', 'jpeg', 'png', 'webp', 'arw'}
        return [f for f in files if f.split('.')[-1] in formats]

    def __get_preview(self, dir):
        for_choice = self.__sort_files(list(os.walk(f'{self.s_path}/{dir}'))[0][2])
        preview = choice(for_choice) if for_choice else  ''
        return preview

    def __get_count_files(self, dir):
        return len(list(os.walk(f'{self.s_path}/{dir}'))[0][2])



