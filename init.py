#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import spotify_controller
import configparser

def read_configuration_file():
    try:
        cp = configparser.ConfigParser()
        with io.open("config.ini", encoding="utf-8") as f:
            cp.read_file(f)
        return {section: {option_name: option for option_name, option in cp.items(section)}
                for section in cp.sections()}
    except (IOError, configparser.Error):
        return dict()


if __name__== "__main__":
    sc = spotify_controller.SpotifyController(am.read_configuration_file())

