#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from hermes_python.hermes import Hermes, MqttOptions
import spotify_controller
import toml
import io

USERNAME_INTENTS = "IronMate"
MQTT_BROKER_ADDRESS = "localhost:1883"
MQTT_USERNAME = None
MQTT_PASSWORD = None

def read_configuration_file():
    try:
        cp = configparser.ConfigParser()
        with io.open("config.ini", encoding="utf-8") as f:
            cp.read_file(f)
        return {section: {option_name: option for option_name, option in cp.items(section)}
                for section in cp.sections()}
    except (IOError, configparser.Error):
        return dict()

def add_prefix(intent_name):
    return USERNAME_INTENTS + ":" + intent_name

def intent_callback_play(hermes, intent_message):
    sp.start()
    hermes.publish_end_session(intent_message.session_id, "")


def intent_callback_pause(hermes, intent_message):
    sp.pause()
    hermes.publish_end_session(intent_message.session_id, "")


def intent_callback_next(hermes, intent_message):
    sp.next_track()
    hermes.publish_end_session(intent_message.session_id, "")
   
def intent_callback_previous(hermes, intent_message):
    sp.previous_track()
    hermes.publish_end_session(intent_message.session_id, "")
   
   
if __name__ == "__main__":
    sp = spotify_controller.SpotifyController(read_configuration_file())

    snips_config = toml.load('/etc/snips.toml')
    if 'mqtt' in snips_config['snips-common'].keys():
        MQTT_BROKER_ADDRESS = snips_config['snips-common']['mqtt']
    if 'mqtt_username' in snips_config['snips-common'].keys():
        MQTT_USERNAME = snips_config['snips-common']['mqtt_username']
    if 'mqtt_password' in snips_config['snips-common'].keys():
        MQTT_PASSWORD = snips_config['snips-common']['mqtt_password']
    mqtt_opts = MqttOptions(username=MQTT_USERNAME, password=MQTT_PASSWORD, broker_address=MQTT_BROKER_ADDRESS)

    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intent(add_prefix("play"), intent_callback_play)
        h.subscribe_intent(add_prefix("pause"), intent_callback_pause)
        h.subscribe_intent(add_prefix("next"), intent_callback_next)
        h.subscribe_intent(add_prefix("previous"), intent_callback_previous)
        h.start()
