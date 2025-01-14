# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 16:33:41 2019

@author: IronMate
"""

import spotipy
import spotipy.oauth2 as oauth
import re

_re_compiled = re.compile("'name':\s'(.*?)'|'name':\s\"(.*?)\"")
_auth_finder = re.compile("code=(.*?)$", re.MULTILINE)


class SpotifyController:

    def __init__(self, config):
        if(config == None):
            self.user = input("User: ")
            self.id = input("ID: ")
            self.secret = input("Secret: ")
            self.device = input("Device: ")
        else:    
            self.user = config['secret']['user']
            self.id = config['secret']['id']
            self.secret = config['secret']['secret']
            self.device = config['secret']['device']
        self.url ='http://localhost/'
        self.scope= 'user-library-read playlist-read-private playlist-read-collaborative user-modify-playback-state user-read-currently-playing user-read-playback-state'
        self.spo = oauth.SpotifyOAuth(client_id=self.id,client_secret=self.secret,redirect_uri=self.url,scope=self.scope,cache_path=".cache-{}".format(self.user))
        self.sp = spotipy.Spotify(auth=self.get_token())
        
    def spot(self, token):
        self.token = token
        self.sp = spotipy.Spotify(auth=token)
        return self.sp

    def refresh_token(self):
        cached_token = self.spo.get_cached_token()
        is_it_expired = self.spo.is_token_expired(cached_token)
        if is_it_expired is True:
            refreshed_token = cached_token['refresh_token']
            new_token = self.spo.refresh_access_token(refreshed_token)  
            self.sp = spotipy.Spotify(auth=new_token)
            return new_token

    def get_token(self):
        token_info = self.spo.get_cached_token()
        if token_info:
            access_token = token_info['access_token']
            return access_token
        else:
            print("New One")
            auth = self.spo.get_authorize_url()
            print(auth)
            auth_url = input('Click the link above and copy and paste the url here: ')
            _re_auth = re.findall(_auth_finder, auth_url)
            access_token = self.spo.get_access_token(_re_auth[0])
            return access_token

    def get_sp(self):
        return self.sp
    
    def pause(self):
        self.sp.pause_playback()

    def next_track(self):
        self.sp.next_track()
        
    def previous_track(self):
        self.sp.previous_track()
        
    def start(self):
        self.sp.start_playback(device_id=self.device)
    
    def volume(self,level):
        if level>=100:
            level =100
        self.sp.volume(level)
