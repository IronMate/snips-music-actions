#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import spotify_controller
import configparser
import action_music as am



if __name__== "__main__":
    sc = spotify_controller.SpotifyController(am.read_configuration_file())

