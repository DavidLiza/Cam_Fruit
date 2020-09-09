# -*- coding: utf-8 -*-
__author__ = "Sebastian Estupiñan"
__copyright__ = "Copyright 2019, Ojo Biometrico"
__credits__ = ["Sebastian Estupiñan"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Sebastian Estupiñan"
__email__ = "sestupinan@identica-sa.com"
__status__ = "Production"

import os
import logging
import logging.config
import yaml

def configure_logger(name):
    my_path = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(my_path, 'config.yaml'), 'r') as f:
        config = yaml.safe_load(f.read())
        config['handlers']['file']['filename'] = os.path.join(os.path.dirname(__file__), 'log', config['handlers']['file']['filename'])
        logging.config.dictConfig(config)
    return logging.getLogger(name)


if __name__ == "__main__":
     my_path = os.path.abspath(os.path.dirname(__file__))
     print (my_path)