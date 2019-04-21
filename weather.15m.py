#!/usr/bin/python2
# -*- coding: utf-8 -*-
"""Docstring"""

# -----------------------------------------------------------------------------------
# Based on Daniel Seripap Weather script for BitBar (https://getbitbar.com/plugins/Weather/ForecastIO/weather.15m.py)
# Homepage: https://github.com/fadeouter/argosWeather
# -----------------------------------------------------------------------------------

import os
import json
import urllib2
import base64
import time
import socket
from time import strftime
import datetime
from random import randint

# appearance
svgtextcolor = '#fff'       # set #444 for light theme
highlight = '#fff'          # set #555 for light theme
cloudopacity = '0.8'        # set 0.8~1 for dark theme, 0.15 for light
font = 'Ubuntu'             # my recommendation is to use Ubuntu font
mainiconfontcolor = '#ccc'  # color for text of panel icon

# scale factor for your DPI
scale = '1'

# get yours at https://darksky.net/dev
api_key = ''

# set to si for metric, leave blank for imperial
units = 'si'

# manual location if you won't use autolocation
man_loc = ''

# manual name for location
man_name = ''

# location examples:
# where cold -54.281,-36.5088
# where always strong wind -49.3501,70.219
# sahara desert 28.0437,9.5411
# somewhere in caribbean 16.2706,-61.5058
# place with undetectable address (to check addr. detection) 72.5507,104.2769
# SEATTLE 47.6038,-122.3301
# LILLE 50.6305,3.0706


scale = float(scale)
imageHeight = str(int(20 * scale))
imageWidth = str(int(420 * scale))
graphHeight = str(int(175 * scale))
graphWidth = str(int(460 * scale))
iconHeight = str(int(30 * scale))
hostname = "api.darksky.net"
port = "80"

def get_location():
    try:
        if man_loc != '':
            loc = man_loc
            location = google_loc(loc)
        else:
            location = ipinfo_loc()
            if 'city' in location:
                if location['city'] == '':
                    loc = location['loc']
                    location = google_loc(loc)
                else:
                    loc = str(location['loc'].encode('UTF-8'))
                    location = str(location['city'].encode('UTF-8'))
        return {"loc": loc, "city": location}
    except:
        return ' '

def google_loc(loc):
    try:
        location = json.load(urllib2.urlopen('https://maps.googleapis.com/maps/api/geocode/json?latlng=' + loc + '&sensor=true'))
        if location['status'] == 'OK':
            for item in range(5):
                if str(location['results'][0]['address_components'][item]['types'][0].encode('UTF-8')) == 'locality':
                    return str(location['results'][0]['address_components'][item]['long_name'].encode('UTF-8'))
        else:
            return 'Middle of Nowhere'
    except:
        return 'Middle of Nowhere'

def ipinfo_loc():
    try:
        location = json.load(urllib2.urlopen('https://ipinfo.io/json'))
        return location
    except:
        return ' '

svgsnippet = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 135.46667 135.46667" height="80" width="80">'
clearday = '<g transform="matrix(13.26575 0 0 13.36122 -29.237 -209.878)"><ellipse ry="3.773" rx="3.8" cy="20.777" cx="7.31" fill="#ffd739"/><path d="M9.914 23.543a3.797 3.797 0 0 1-3.372.925 3.872 3.872 0 0 1-2.032-1.14c4.924 2.637 7.302-2.108 5.548-5.155.435.462.734 1.002.898 1.569a3.75 3.75 0 0 1-1.042 3.8z" fill-opacity=".157"/></g>'
clearnight = '<path d="M113.693 46.177c11.977 25.084 1.206 55.198-24.06 67.262-25.264 12.064-55.455 1.509-67.432-23.575 9.136 5.668 20.278 10.647 28.116 11.41 31.333 3.053 52.868-17.354 48.022-50.824-1.338-9.236-6.672-18.856-13.38-29.991 12.202 4.266 22.745 13.175 28.734 25.718z" fill="#ffd739"/><path d="M63.012 43.273L51.084 31.652 39.24 43.432l7.367-14.934-14.864-7.623 16.48 2.391L50.88 6.774l2.818 16.412 16.506-2.57-14.738 7.753zm-32.92 26.414l-7.177-6.992-7.124 7.088 4.431-8.985-8.942-4.586 9.915 1.438 1.598-9.922 1.696 9.874 9.93-1.546-8.867 4.665zm.072-26.34l-5.725-5.578-5.684 5.654 3.536-7.168-7.134-3.659 7.91 1.148 1.275-7.916 1.352 7.878 7.922-1.234-7.073 3.721z" opacity=".755" fill="#999"/>'
rain = '<g><path d="M50.451 29.485c-13.4-10.02-30.044 2.235-23.562 16.175-25.324-2.05-25.555 31.19-4.915 33.75 6.148-.039 86.997-.499 86.997-.499 25.737.076 26.81-41.704-2.845-41.26 8.443-35.78-54.129-44.673-55.675-8.166z" fill="#bbbbbb"/><path d="M26.255 74.463c-13.765.513-16.778-3.997-18.612-8.004 1.504 6.711 6.873 12.025 14.331 12.95 6.148-.039 86.997-.499 86.997-.499 14.838.038 21.478-13.826 18.758-25.494-.049 5.642-3.024 19.864-17.017 20.185-13.994.32-84.457.862-84.457.862z" fill-opacity=".181"/></g><path d="M32.3 83.03s2.296 15.254-.335 18.952c-2.632 3.698-8.247 4.327-11.24 2.969-2.994-1.358-5.081-5.418-3.626-9.896 1.455-4.478 15.2-12.025 15.2-12.025zm35.928 0s2.296 15.254-.335 18.952c-2.632 3.698-8.247 4.327-11.24 2.969-2.994-1.358-5.081-5.418-3.626-9.896 1.455-4.478 15.2-12.025 15.2-12.025zm35.928 0s2.296 15.254-.335 18.952c-2.632 3.698-8.247 4.327-11.24 2.969-2.994-1.358-5.081-5.418-3.626-9.896 1.455-4.478 15.2-12.025 15.2-12.025zm-58.655 23.771s2.296 15.254-.335 18.952c-2.632 3.698-8.247 4.327-11.24 2.97-2.994-1.359-5.08-5.419-3.626-9.897 1.455-4.478 15.2-12.025 15.2-12.025zm35.929 0s2.295 15.254-.336 18.952c-2.632 3.698-8.247 4.327-11.24 2.97-2.994-1.359-5.08-5.419-3.626-9.897 1.455-4.478 15.2-12.025 15.2-12.025z" fill="#647dff"/>'
snow = '<g><path d="M50.451 29.485c-13.4-10.02-30.044 2.235-23.562 16.175-25.324-2.05-25.555 31.19-4.915 33.75 6.148-.039 86.997-.499 86.997-.499 25.737.076 26.81-41.704-2.845-41.26 8.443-35.78-54.129-44.673-55.675-8.166z" fill="#bbbbbb"/><path d="M26.255 74.463c-13.765.513-16.778-3.997-18.612-8.004 1.504 6.711 6.873 12.025 14.331 12.95 6.148-.039 86.997-.499 86.997-.499 14.838.038 21.478-13.826 18.758-25.494-.049 5.642-3.024 19.864-17.017 20.185-13.994.32-84.457.862-84.457.862z" fill-opacity=".181"/></g><path d="M31.805 84.09v20.458m-8.858-15.343l17.717 10.228m0-10.228L22.947 99.433M67.733 84.09v20.458m-8.858-15.343l17.717 10.228m0-10.228L58.875 99.433m44.786-15.343v20.458m-8.858-15.343l17.716 10.228m0-10.228L94.803 99.433M49.77 107.3v20.457m-8.859-15.343l17.717 10.228m0-10.228L40.91 122.642M85.697 107.3v20.457m-8.858-15.343l17.717 10.228m0-10.228l-17.717 10.228" stroke-width="3.2" fill="#657eff" stroke="#657eff" stroke-linecap="round"/>'
sleet = '<path d="M50.451 29.485c-13.4-10.02-30.044 2.235-23.562 16.175-25.324-2.05-25.555 31.19-4.915 33.75 6.148-.039 86.997-.499 86.997-.499 25.737.076 26.81-41.704-2.845-41.26 8.443-35.78-54.129-44.673-55.675-8.166z" fill="#bbbbbb"/><path d="M26.255 74.463c-13.765.513-16.778-3.997-18.612-8.004 1.504 6.711 6.873 12.025 14.331 12.95 6.148-.039 86.997-.499 86.997-.499 14.838.038 21.478-13.826 18.758-25.494-.049 5.642-3.024 19.864-17.017 20.185-13.994.32-84.457.862-84.457.862z" fill-opacity=".181"/><ellipse ry="7.967" rx="7.81" cy="117.528" cx="85.697" fill="#657eff"/><ellipse ry="7.967" rx="7.81" cy="117.528" cx="49.769" fill="#657eff"/><ellipse ry="7.967" rx="7.81" cy="94.319" cx="31.805" fill="#657eff"/><ellipse ry="7.967" rx="7.81" cy="94.319" cx="67.733" fill="#657eff"/><ellipse ry="7.967" rx="7.81" cy="94.319" cx="103.661" fill="#657eff"/>'
wind = '<path d="M20.437 71.367v51.42s-.003 4.179 4.276 4.192c4.262.013 4.277-4.19 4.277-4.19V71.366z" fill="gray"/><path d="M20.437 8.488c64.003 6.99 55.815 66.215 0 77.132m14.88-38.566c0 21.3-6.662 38.566-14.88 38.566S5.557 68.353 5.557 47.055c0-21.3 6.662-38.566 14.88-38.566s14.88 17.266 14.88 38.566z" fill="#ccc"/><path d="M20.437 85.62s15.337-10.547 14.88-38.566c-.477-29.298-14.88-38.566-14.88-38.566l32.862 6.427c27.444 6.428 27.444 57.85 0 64.277z" fill="#f55"/><path d="M53.358 79.192s12.782-8.79 12.402-32.137c-.398-24.415-12.4-32.138-12.4-32.138l27.384 6.427c21.908 6.428 21.908 44.994 0 51.422z" fill="#ccc"/><path d="M80.743 72.765s10.225-7.032 9.92-25.711c-.318-19.532-9.92-25.71-9.92-25.71l21.908 6.427c16.43 4.82 16.43 33.745 0 38.566z" fill="#f55"/><path d="M102.65 66.337s7.67-5.274 7.44-19.283c-.237-14.649-7.44-19.283-7.44-19.283l16.43 4.82c14.422 3.71 14.458 23.982 0 28.925z" fill="#ccc"/>'
fog = '<g id="fog"><defs><linearGradient xlink:href="#a" id="b" gradientUnits="userSpaceOnUse" gradientTransform="matrix(.85376 0 0 .96041 -12.027 2.291)" x1="47.923" y1="72.413" x2="47.914" y2="62.985"/><linearGradient id="a"><stop offset="0" stop-color="#9f9f9f" stop-opacity="0"/><stop offset=".5" stop-color="#bbbbbb"/><stop offset="1" stop-color="#9f9f9f" stop-opacity="0"/></linearGradient></defs><path d="M24.934 72.323s-.758-1.013-.758-1.954c0-.94 1.316-1.055 1.316-1.996 0-.94-1.11-1.034-1.11-1.974 0-.941 1.364-1.118 1.364-2.059 0-.94-1.828-1.995-1.828-1.995h8.376s1.471 1.054 1.471 1.995c0 .94-1.47 1.055-1.47 1.996 0 .94 1.233 1.055 1.233 1.995 0 .941-1.453 1.055-1.453 1.996 0 .94 1.69 1.996 1.69 1.996z" fill="url(#b)" transform="matrix(12.62853 0 0 10.11348 -296.492 -613.244)"/></g>'
cloudy = '<g><path d="M49.999 54.124c-13.75-10.282-30.83 2.293-24.178 16.598-25.986-2.105-26.224 32.006-5.044 34.631 6.31-.039 89.272-.51 89.272-.51 26.41.077 27.512-42.795-2.919-42.34 8.664-36.716-55.545-45.84-57.131-8.38z" fill="#bbbbbb"/><path d="M25.17 100.278c-14.125.526-17.217-4.102-19.099-8.214 1.544 6.887 7.053 12.34 14.706 13.288 6.31-.039 89.272-.51 89.272-.51 15.226.038 22.04-14.188 19.249-26.161-.05 5.789-3.103 20.383-17.462 20.712-14.36.329-86.666.885-86.666.885z" fill-opacity=".181"/></g>'
partlycloudyday = '<g transform="translate(27.943 -132.12) scale(9.17795)"><ellipse ry="3.773" rx="3.8" cy="20.777" cx="7.31" fill="#ffd739"/><path d="M9.914 23.543a3.797 3.797 0 0 1-3.372.925 3.872 3.872 0 0 1-2.032-1.14c4.924 2.637 7.302-2.108 5.548-5.155.435.462.734 1.002.898 1.569a3.75 3.75 0 0 1-1.042 3.8z" fill-opacity=".157"/></g><g><path d="M49.999 63.709c-13.75-10.282-30.83 2.293-24.178 16.598-25.986-2.105-26.224 32.006-5.044 34.632 6.31-.04 89.272-.511 89.272-.511 26.41.078 27.512-42.795-2.919-42.34 8.664-36.716-55.545-45.84-57.131-8.38z" fill="#bbbbbb"/><path d="M25.17 109.863c-14.125.526-17.217-4.102-19.099-8.214 1.544 6.888 7.053 12.34 14.706 13.289 6.31-.04 89.272-.511 89.272-.511 15.226.039 22.04-14.188 19.249-26.161-.05 5.789-3.103 20.383-17.462 20.712-14.36.33-86.666.885-86.666.885z" fill-opacity=".181"/></g>'
partlycloudynight = '<path d="M123.374 35.376c8.14 17.34.581 38.044-16.883 46.243-17.466 8.2-38.223.788-46.364-16.551 6.27 3.947 13.927 7.428 19.324 7.99 21.58 2.245 36.512-11.72 33.324-34.807-.88-6.37-4.513-13.024-9.086-20.728 8.39 2.996 15.615 9.182 19.685 17.853z" fill="#ffd739"/><path d="M123.374 35.376c8.14 17.34.581 38.044-16.883 46.243-17.466 8.2-38.223.788-46.364-16.551 8.328 10.437 14.89 12.954 19.962 14.888 24.978 9.53 49.357-10.676 43.49-37.883-2.873-13.324-13.333-20.608-19.89-24.55 8.39 2.996 15.615 9.182 19.685 17.853z" fill-opacity=".081"/><path d="M6.255 63.636l6.62-7.4-7.319-6.756 9.084 4.01 4.164-9.048-1.006 9.878 9.892 1.163-9.705 2.096 1.95 9.767-4.993-8.582zm17.012-18.508l1.019-7.426-7.433-1.14 7.378-1.325-1.214-7.422 3.54 6.608 6.683-3.448-5.19 5.41 5.345 5.29-6.748-3.264zm14.124 8.955l1.574-5.52-5.512-1.666 5.736-.21-.12-5.758 1.973 5.392 5.439-1.893-4.52 3.542 3.483 4.587-4.765-3.203z" opacity=".755" fill="#999"/><g><path d="M49.999 63.709c-13.75-10.282-30.83 2.293-24.178 16.598-25.986-2.105-26.224 32.006-5.044 34.632 6.31-.04 89.272-.511 89.272-.511 26.41.078 27.512-42.795-2.919-42.34 8.664-36.716-55.545-45.84-57.131-8.38z" fill="#bbbbbb"/><path d="M25.17 109.863c-14.125.526-17.217-4.102-19.099-8.214 1.544 6.888 7.053 12.34 14.706 13.289 6.31-.04 89.272-.511 89.272-.511 15.226.039 22.04-14.188 19.249-26.161-.05 5.789-3.103 20.383-17.462 20.712-14.36.33-86.666.885-86.666.885z" fill-opacity=".181"/></g>'
uvindex = '<defs><linearGradient id="a"><stop offset="0" stop-color="#323232"/><stop offset="1" stop-color="#868686"/></linearGradient><linearGradient xlink:href="#a" id="b" gradientUnits="userSpaceOnUse" x1="121.588" y1="-335.117" x2="121.587" y2="-263.852"/></defs><path d="M21.104-331.904c15.15-2.82 34.298-2.237 50.466-1.844 16.167.393 31.945 3.773 39.449 4.795 7.504 1.022 5.872 1.073 10.519 1.053a5.06 5.06 0 0 1 .099 0c4.647.02 3.015-.031 10.519-1.053 7.503-1.022 23.281-4.402 39.449-4.795 16.167-.393 35.316-.975 50.466 1.844.233 4.992.501 8.471.42 13.61-5.74 3.514-.904 29.833-10.326 41.28-5.327 6.473-12.679 9.53-16.787 10.51-14.676 3.505-27.854 3.771-42.11-.613-5.332-1.85-11.6-5.035-15.637-11.41-6.245-9.863-8.933-17.612-11.026-31.121-.439-2.837-1.231-3.936-5.018-4.015-3.786.079-4.578 1.178-5.018 4.015-2.093 13.509-4.78 21.258-11.025 31.12-4.038 6.376-10.305 9.561-15.638 11.411-14.255 4.384-27.433 4.118-42.11.613-4.107-.98-11.46-4.037-16.786-10.51-9.422-11.447-4.586-37.766-10.326-41.28-.082-5.139.187-8.618.42-13.61z" fill="url(#b)" transform="translate(-7.178 251.93) scale(.61611)"/>'
humidity = '<path d="M67.733 5.556s-46.166 59.37-38.938 93.24c3.968 18.591 23.528 31.114 38.938 31.114 15.41 0 34.97-12.523 38.938-31.115C113.9 64.926 67.733 5.556 67.733 5.556z" fill="#647dff"/><path d="M67.733 5.556S100.31 44.71 93.781 94.207c-2.211 16.772-6.623 25.13-26.048 35.703 15.41 0 34.97-12.523 38.938-31.115C113.9 64.926 67.733 5.556 67.733 5.556z" fill-opacity=".089"/>'
visibility = '<defs><linearGradient id="b"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient><linearGradient id="a"><stop offset="0"/><stop offset="1" stop-opacity="0"/></linearGradient><linearGradient xlink:href="#a" id="c" x1="67.735" y1="129.225" x2="67.543" y2="43.913" gradientUnits="userSpaceOnUse" gradientTransform="matrix(1.07912 0 0 .92375 -5.156 8.471)"/><linearGradient xlink:href="#b" id="d" x1="67.693" y1="126.569" x2="67.41" y2="49.508" gradientUnits="userSpaceOnUse"/></defs><path d="M4.611 135.286c-.158-.027-.5-.31-.58-.48-.1-.214-.122-.601-.051-.884 30.952-84.685 0 0 30.511-84.43a.907.907 0 0 1 .44-.255c.182-.054 3.524-.06 32.447-.06 28.958 0 32.265.006 32.451.06.247.072.472.25.537.422 9.38 25.362 19.07 51.617 29.2 78.975 1.82 4.915 1.93 5.23 1.954 5.57.02.289.008.397-.062.562-.099.236-.392.484-.618.523-.157.026-126.067.024-126.228-.002zm66.805-9.231c-.34-13.212-.476-18.267-.497-18.528l-.026-.323h-3.269c-2.573 0-3.274.01-3.29.049-.025.054-.388 19.23-.365 19.262.007.011 1.689.015 3.736.01l3.723-.01zm-.764-28.79c-.013-.21-.035-.867-.049-1.46-.014-.592-.086-3.36-.16-6.15-.075-2.79-.136-5.147-.136-5.239v-.166h-5.583v.401c0 .221-.021 1.468-.046 2.772-.089 4.532-.183 9.657-.183 9.94v.283h6.181l-.024-.382zm-.55-20.526c-.016-.361-.068-2.207-.116-4.103a699.784 699.784 0 0 0-.118-4.26l-.03-.813h-2.397c-2.252 0-2.397.004-2.397.069l-.091 4.73c-.05 2.563-.09 4.745-.091 4.847v.186h5.266l-.028-.656zm-.391-14.435c0-.048-.041-1.524-.091-3.28a304.33 304.33 0 0 1-.09-3.672l-.001-.48h-4.256v.264c-.001.146-.032 1.763-.068 3.594-.037 1.831-.068 3.404-.068 3.496l-.001.167h4.576l-.001-.089z" fill="url(#c)"/><path d="M65.273 54.872h4.256l.183 7.52h-4.576zm-.25 12.677l4.815.014.291 9.832h-5.268zm-.299 16.701h5.582l.37 13.396h-6.181zm-.428 22.92l6.696-.038.436 19.38-.003.003h-7.463z" fill="url(#d)"/>'
temperature = 'PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMzUuNDY2NjcgMTM1LjQ2NjY3IiBoZWlnaHQ9IjgwIiB3aWR0aD0iODAiPjxkZWZzPjxtYXJrZXIgb3JpZW50PSJhdXRvIiBpZD0iYiIgb3ZlcmZsb3c9InZpc2libGUiPjxwYXRoIGQ9Ik0uOTggMGExIDEgMCAxIDEtMiAwIDEgMSAwIDAgMSAyIDB6IiBmaWxsPSIjZjU1IiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIHN0cm9rZT0iI2Y1NSIgc3Ryb2tlLXdpZHRoPSIuMjY3Ii8+PC9tYXJrZXI+PG1hcmtlciBvcmllbnQ9ImF1dG8iIGlkPSJhIiBvdmVyZmxvdz0idmlzaWJsZSI+PHBhdGggZD0iTS45OCAwYTEgMSAwIDEgMS0yIDAgMSAxIDAgMCAxIDIgMHoiIGZpbGw9IiNjY2MiIGZpbGwtcnVsZT0iZXZlbm9kZCIgc3Ryb2tlPSIjY2NjIiBzdHJva2Utd2lkdGg9Ii4yNjciLz48L21hcmtlcj48L2RlZnM+PGcgc3Ryb2tlLXdpZHRoPSIxNC43NzkiPjxwYXRoIGQ9Ik02Ni4zNzggMTEyLjU5NmMuMDEzLTMxLjcyNi4wMjctNS42My4wNC05NS4yMzUiIGZpbGw9IiNjY2MiIHN0cm9rZT0iI2NjYyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBtYXJrZXItc3RhcnQ9InVybCgjYSkiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xLjE4MiAtNC42ODcpIHNjYWxlKDEuMDM4MjQpIi8+PHBhdGggZD0iTTY2LjM3OCAxMTIuNTk2Yy4wMi0xNi4zMzguMDQtMi45LjA2LTQ5LjA0MyIgZmlsbD0iI2Y1NSIgc3Ryb2tlPSIjZjU1IiBtYXJrZXItc3RhcnQ9InVybCgjYikiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xLjE4MiAtNC42ODcpIHNjYWxlKDEuMDM4MjQpIi8+PC9nPjwvc3ZnPgo='
nodata = 'PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMzUuNDY2NjcgMTM1LjQ2NjY3IiBoZWlnaHQ9IjgwIiB3aWR0aD0iODAiPjxnPjxwYXRoIGQ9Ik00OS45OTkgNTQuMTI0Yy0xMy43NS0xMC4yODItMzAuODMgMi4yOTMtMjQuMTc4IDE2LjU5OC0yNS45ODYtMi4xMDUtMjYuMjI0IDMyLjAwNi01LjA0NCAzNC42MzEgNi4zMS0uMDM5IDg5LjI3Mi0uNTEgODkuMjcyLS41MSAyNi40MS4wNzcgMjcuNTEyLTQyLjc5NS0yLjkxOS00Mi4zNCA4LjY2NC0zNi43MTYtNTUuNTQ1LTQ1Ljg0LTU3LjEzMS04LjM4eiIgZmlsbD0iI2JiYmJiYiIvPjxwYXRoIGQ9Ik0yNS4xNyAxMDAuMjc4Yy0xNC4xMjUuNTI2LTE3LjIxNy00LjEwMi0xOS4wOTktOC4yMTQgMS41NDQgNi44ODcgNy4wNTMgMTIuMzQgMTQuNzA2IDEzLjI4OCA2LjMxLS4wMzkgODkuMjcyLS41MSA4OS4yNzItLjUxIDE1LjIyNi4wMzggMjIuMDQtMTQuMTg4IDE5LjI0OS0yNi4xNjEtLjA1IDUuNzg5LTMuMTAzIDIwLjM4My0xNy40NjIgMjAuNzEyLTE0LjM2LjMyOS04Ni42NjYuODg1LTg2LjY2Ni44ODV6IiBmaWxsLW9wYWNpdHk9Ii4xODEiLz48L2c+PHRleHQgeD0iNzAiIHk9IjExMCIgZmlsbD0iIzIyMiIgZm9udC1zaXplPSIxMjAiIHN0cm9rZT0iI0ZGRkZGRiIgc3Ryb2tlLXdpZHRoPSI1IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiAgICBmb250LWZhbWlseT0iVWJ1bnR1IiBmb250LXdlaWdodD0iNzAwIj48dHNwYW4+PzwvdHNwYW4+PC90ZXh0Pjwvc3ZnPg=='

def get_wx_icon(icon_code):
    if icon_code == 'clear-day':
        icon = clearday
    elif icon_code == 'clear-night':
        icon = clearnight
    elif icon_code == 'rain':
        icon = rain
    elif icon_code == 'snow':
        icon = snow
    elif icon_code == 'sleet':
        icon = sleet
    elif icon_code == 'wind':
        icon = wind
    elif icon_code == 'fog':
        icon = fog
    elif icon_code == 'cloudy':
        icon = cloudy
    elif icon_code == 'partly-cloudy-day':
        icon = partlycloudyday
    elif icon_code == 'partly-cloudy-night':
        icon = partlycloudynight
    else:
        icon = ''
    return icon

if units == 'si':
    unit = 'C'
    distance = 'm/s'
    distance_short = 'km'
    distance_convert = float(1.0)
else:
    unit = 'F'
    distance = 'mph'
    distance_short = 'mi'
    distance_convert = float(0.44704)

def get_wx():

    if api_key == "":
        return False
    location = get_location()
    if location is False:
        return False
    try:
        if 'loc' in location:
            wx = json.load(urllib2.urlopen('https://api.darksky.net/forecast/' + api_key + '/' + location['loc'] + '?units=' + units + "&v=" + str(randint(0, 100))))
        else:
            return False
    except urllib2.HTTPError:
        return False
#
# determine color of wind indicators and text alert about high wind
#
    def wind_alert(speed):
        if (speed * distance_convert) > 50.0:
            colour = 'red'
            outline = 'red'
            definition = 'Hurricane'
            separator = '   •   '
        elif (speed * distance_convert) > 20.8:
            colour = 'orangered'
            outline = 'orangered'
            definition = 'Gale'
            separator = '   •   '
        elif (speed * distance_convert) > 13.9:
            colour = 'darkorange'
            outline = 'darkorange'
            definition = 'High wind'
            separator = '   •   '
        elif (speed * distance_convert) > 10.8:
            colour = 'orange'
            outline = 'orange'
            definition = 'Strong breeze'
            separator = '   •   '
        elif (speed * distance_convert) > 8.0:
            colour = 'gold'
            outline = 'none'
            definition = 'Fresh breeze'
            separator = '   •   '
        elif (speed * distance_convert) > 5.5:
            colour = '#D8D742'
            outline = 'none'
            definition = 'Moderate breeze'
            separator = '   •   '
        else:
            colour = '#AAAAAA'
            outline = 'none'
            definition = ''
            separator = ''
        return {'colour':colour, 'outline':outline, 'definition':definition, 'separator':separator}

    try:
        wd = {}
        wd['hourlyMin'] = {}
        wd['dailyMin'] = {}
        wd['dailyMax'] = {}
# dummy output (to not break svg generation if some data is not present)
        wd['temperature'] = '-'
        wd['condition'] = '-'
        wd['windSpeed'] = '-'
        wd['windGust'] = ''
# generate current data
        if 'currently' in wx:
            for item in wx['currently']:
                if item == 'temperature':
                    wd['temperature'] = str(int(round(wx['currently']['temperature'])))
                    wd['lentemp'] = str(len(wd['temperature']))
                    # offset for city name and condition text, depended of temperature length
                    wd['lentempoffset'] = str(26.5 + (len(wd['temperature']) * 6.5))
                elif item == 'icon':
                    wd['icon'] = get_wx_icon(str(wx['currently']['icon']))
                    wd['status'] = str(wx['currently']['icon'])
                elif item == 'summary':
                    wd['condition'] = str(wx['currently']['summary'].encode('utf-8'))
                elif item == 'windSpeed':
                    wd['windSpeed'] = str(wx['currently']['windSpeed'])
                    wd["windClass"] = wind_alert(wx['currently']['windSpeed'])
                elif item == 'windSpeed':
                    wd['windGust'] = '/' + str(wx['currently']['windGust'])
                elif item == 'windBearing':
                    wd['windBearing'] = str(wx['currently']['windBearing'])
                elif item == 'humidity':
                    wd['humidity'] = str(int(round(wx['currently']['humidity'] * 100)))
                elif item == 'dewPoint':
                    wd['dewPoint'] = str(wx['currently']['dewPoint'])
                elif item == 'visibility':
                    wd['visibility'] = str(int(round(wx['currently']['visibility'])))
                elif item == 'uvIndex':
                    wd['uvindex'] = str(wx['currently']['uvIndex'])
                elif item == 'pressure':
                    wd['pressure'] = str(int(round(wx['currently']['pressure'])))
# determine pressure symbol
                    wd['pr_symbol'] = ''
                    if int(wd['pressure']) < 1009:
                        wd['pr_symbol'] = '<path fill="CornflowerBlue" d="M-0.5 1.3l-1 1.5-1-1.5z"/>'
                    elif int(wd['pressure']) > 1016:
                        wd['pr_symbol'] = '<path fill="tomato" d="M-0.5 1.3l-1 1.5-1-1.5z" transform="translate(-3,4) rotate(180)"/>'
                    else:
                        wd['pr_symbol'] = '<circle r="0.8" fill="#aaaaaa" transform="translate(-1.45,2.2)"/>'
                elif item == 'apparentTemperature':
                    wd['apparentTemperature'] = str(int(round(wx['currently']['apparentTemperature']))) + '°' + unit
                elif item == 'cloudCover':
                    wd['cloudCover'] = str(int(round(wx['currently']['cloudCover'] * 100)))
        if man_name != '':
            wd['city'] = man_name
        elif 'city' in location:
            wd['city'] = location['city']
            wd['loc'] = location['loc']
# calculate max and min temperature for a week and how shrink/extend temp. bars
        if 'temperatureMax' in wx['daily']['data'][0] and 'temperatureMin' in wx['daily']['data'][0]:
            for item in range(8):
                wd['dailyMin'][item] = int(round(wx['daily']['data'][item]['temperatureMin']))
                wd['dailyMax'][item] = int(round(wx['daily']['data'][item]['temperatureMax']))
            maxdaily = float(max(wd["dailyMax"].values()))
            mindaily = float(min(wd["dailyMin"].values()))
            offset = float(30 / abs(maxdaily - mindaily))
# generate daily data
        for item in range(8):
            if 'time' in wx['daily']['data'][0]:
                wd["dday{0}".format(item)] = str((datetime.datetime.fromtimestamp(wx['daily']['data'][item]['time'])).strftime('%-d, %a'))
            if 'icon' in wx['daily']['data'][0]:
                wd["dicon{0}".format(item)] = get_wx_icon(str(wx['daily']['data'][item]['icon']))
            if 'temperatureMax' in wx['daily']['data'][0] and 'temperatureMin' in wx['daily']['data'][0]:
                wd["dmax{0}".format(item)] = str(int(round(wx['daily']['data'][item]['temperatureMax']))) + '°'
                wd["dmaxpos{0}".format(item)] = str((int(round(wx['daily']['data'][item]['temperatureMax'])) - mindaily) * offset)
                wd["dmin{0}".format(item)] = str(int(round(wx['daily']['data'][item]['temperatureMin']))) + '°'
                wd["dminpos{0}".format(item)] = str((int(round(wx['daily']['data'][item]['temperatureMin'])) - mindaily) * offset)
                minmax = int(round(wx['daily']['data'][item]['temperatureMax'])) - (round(wx['daily']['data'][item]['temperatureMin']))
# replace minimum temp. value with ellipsis on temp. bar if it is very shrinked 
                if float(3.75) > float(offset) and minmax < 3:
                    wd["dmin{0}".format(item)] = '<tspan font-size="1.5">…</tspan>'
            if 'pressure' in wx['daily']['data'][0]:
                wd["dpr{0}".format(item)] = str(int(round(wx['daily']['data'][item]['pressure'])))
                wd['pr_symbol{0}'.format(item)] = ''
                if int(wd["dpr{0}".format(item)]) < 1009:
                    wd['pr_symbol{0}'.format(item)] = '<path fill="CornflowerBlue" d="M-0.5 1.3l-1 1.5-1-1.5z"/>'
                elif int(wd["dpr{0}".format(item)]) > 1016:
                    wd['pr_symbol{0}'.format(item)] = '<path fill="tomato" d="M-0.5 1.3l-1 1.5-1-1.5z" transform="translate(-3,4) rotate(180)"/>'
                else:
                    wd['pr_symbol{0}'.format(item)] = '<circle r="0.8" fill="#aaaaaa" transform="translate(-1.45,2.2)"/>'
            if 'windBearing' in wx['daily']['data'][0]:
                wd["windBearing{0}".format(item)] = str(wx['daily']['data'][item]['windBearing'])
            if 'windGust' in wx['daily']['data'][0]:
                wd["windGust{0}".format(item)] = str(wx['daily']['data'][item]['windGust'])
            else:
                wd["windGust{0}".format(item)] = '-'
            if 'windSpeed' in wx['daily']['data'][0]:
                wd["windSpeed{0}".format(item)] = str(wx['daily']['data'][item]['windSpeed'])
                wd["windClass{0}".format(item)] = wind_alert(wx['daily']['data'][item]['windSpeed'])
            if 'summary' in wx['daily']['data'][0]:
                wd["ds{0}".format(item)] = str(wx['daily']['data'][item]['summary'].encode('utf-8'))
            if 'sunriseTime' in wx['daily']['data'][0] and 'sunsetTime' in wx['daily']['data'][0]:
                wd["dsr{0}".format(item)] = str((datetime.datetime.fromtimestamp(wx['daily']['data'][item]['sunriseTime'])).strftime('%-H:%M'))
                wd["dst{0}".format(item)] = str((datetime.datetime.fromtimestamp(wx['daily']['data'][item]['sunsetTime'])).strftime('%-H:%M'))
            if 'moonPhase' in wx['daily']['data'][0]:
                wd["moonPhase{0}".format(item)] = float(wx['daily']['data'][item]['moonPhase'])
                if wd["moonPhase{0}".format(item)] > 0.75:
                    wd["moonPhaseSymbol{0}".format(item)] = '<span color="#a88c00">🌘</span>   <span color="'+highlight+'" font="10">'+ str(wd["moonPhase{0}".format(item)]) + '</span>   •   <span color="'+highlight+'">Waning Crescent</span>'
                if wd["moonPhase{0}".format(item)] == 0.75:
                    wd["moonPhaseSymbol{0}".format(item)] = '<span color="#a88c00">🌗</span>   <span color="'+highlight+'" font="10">'+ str(wd["moonPhase{0}".format(item)]) + '</span>   •   <span color="'+highlight+'">Last Quarter</span>'
                if wd["moonPhase{0}".format(item)] > 0.5:
                    wd["moonPhaseSymbol{0}".format(item)] = '<span color="#a88c00">🌖</span>   <span color="'+highlight+'" font="10">'+ str(wd["moonPhase{0}".format(item)]) + '</span>   •   <span color="'+highlight+'">Waning Gibbous</span>'
                elif wd["moonPhase{0}".format(item)] == 0.5:
                    wd["moonPhaseSymbol{0}".format(item)] = '<span color="#a88c00">🌕</span>   <span color="'+highlight+'" font="10">'+ str(wd["moonPhase{0}".format(item)]) + '</span>   •   <span color="'+highlight+'">Full</span>'
                elif wd["moonPhase{0}".format(item)] > 0.25:
                    wd["moonPhaseSymbol{0}".format(item)] = '<span color="#a88c00">🌔</span>   <span color="'+highlight+'" font="10">'+ str(wd["moonPhase{0}".format(item)]) + '</span>   •   <span color="'+highlight+'">Waxing Gibbous</span>'
                elif wd["moonPhase{0}".format(item)] == 0.25:
                    wd["moonPhaseSymbol{0}".format(item)] = '<span color="#a88c00">🌓</span>   <span color="'+highlight+'" font="10">'+ str(wd["moonPhase{0}".format(item)]) + '</span>   •   <span color="'+highlight+'">First Quarter</span>'
                elif wd["moonPhase{0}".format(item)] > 0:
                    wd["moonPhaseSymbol{0}".format(item)] = '<span color="#a88c00">🌒</span>   <span color="'+highlight+'" font="10">'+ str(wd["moonPhase{0}".format(item)]) + '</span>   •   <span color="'+highlight+'">Waxing Crescent</span>'
                elif wd["moonPhase{0}".format(item)] == 0:
                    wd["moonPhaseSymbol{0}".format(item)] = '🌑   <span color="'+highlight+'" font="10">New</span>'
            if 'apparentTemperatureMin' in wx['daily']['data'][0] and 'apparentTemperatureMax' in wx['daily']['data'][0]:
                wd["apparentTemperatureMin{0}".format(item)] = str(int(round(wx['daily']['data'][item]['apparentTemperatureMin'])))
                wd["apparentTemperatureMax{0}".format(item)] = str(int(round(wx['daily']['data'][item]['apparentTemperatureMax'])))
            if 'dewPoint' in wx['daily']['data'][0]:
                wd["dewPoint{0}".format(item)] = str(int(wx['daily']['data'][item]['dewPoint'])) + '°'
            if 'humidity' in wx['daily']['data'][0]:
                wd["humidity{0}".format(item)] = str(int(float(wx['daily']['data'][item]['humidity'] * 100))) + '%'
            if 'cloudCover' in wx['daily']['data'][0]:
                wd["cloudCover{0}".format(item)] = str(int(float(wx['daily']['data'][item]['cloudCover'] * 100))) + '%'
            if 'uvIndex' in wx['daily']['data'][0]:
                wd["uvIndex{0}".format(item)] = str(wx['daily']['data'][item]['uvIndex'])
#
# generate hourly data
#
        if 'temperature' in wx['hourly']['data'][0]:
            for item in range(24):
                wd['hourlyMin'][item] = int(round(wx['hourly']['data'][item]['temperature']))
            minhourly = float(min(wd['hourlyMin'].values()))
            maxhourly = float(max(wd['hourlyMin'].values()))
            hourlyOffset = 1
            if (maxhourly - minhourly) > 17:
                hourlyOffset = float(17.0 / (maxhourly - minhourly))
        for item in range(24):
            if 'icon' in wx['hourly']['data'][0]:
                wd["icon{0}".format(item)] = get_wx_icon(str(wx['hourly']['data'][item]['icon']))
                wd["status{0}".format(item)] = str(wx['hourly']['data'][item]['icon'])
            if 'temperature' in wx['hourly']['data'][0]:
                wd['t{0}'.format(item)] = str(int(round(wx['hourly']['data'][item]['temperature'])))
                wd['tr{0}'.format(item)] = str((float(float(wx['hourly']['data'][item]['temperature']) - minhourly) * hourlyOffset) + 1.0)
            if 'time' in wx['hourly']['data'][0]:
                wd['h{0}'.format(item)] = str((datetime.datetime.fromtimestamp(wx['hourly']['data'][item]['time'])).strftime('%-H'))
            if 'uvIndex' in wx['hourly']['data'][0]:
                wd['uvi{0}'.format(item)] = str(int(wx['hourly']['data'][item]['uvIndex']))
                wd['uvcol{0}'.format(item)] = 'orangered'
                if wd['uvi{0}'.format(item)] <= '8':
                    wd['uvcol{0}'.format(item)] = 'orange'
                if wd['uvi{0}'.format(item)] <= '6':
                    wd['uvcol{0}'.format(item)] = 'wheat'
                wd['uv{0}'.format(item)] = str(int(wx['hourly']['data'][item]['uvIndex']) * 1.81)
            if 'precipProbability' in wx['hourly']['data'][0]:
        #        wd['op{0}'.format(item)] = str((wx['hourly']['data'][item]['precipProbability'] * 1.5 - 0.5) * .5 + .5)
                wd['p{0}'.format(item)] = str(wx['hourly']['data'][item]['precipProbability'] * 10)
            if 'precipIntensity' in wx['hourly']['data'][0]:
                wd['op{0}'.format(item)] = str(wx['hourly']['data'][item]['precipIntensity'] * .3 + .3)
        #        wd['p{0}'.format(item)] = str(wx['hourly']['data'][item]['precipIntensity'] * 1.2)
            if 'cloudCover' in wx['hourly']['data'][0]:
                wd['cl{0}'.format(item)] = str(wx['hourly']['data'][item]['cloudCover'] * 20)
    except KeyError:
        return False

    return wd

def gen_svg():

    wd = get_wx()
    svg = {}
    svg['clouds'] = ''
    svg['uvindex'] = ''
    svg['rain'] = ''
    svg['temp'] = ''
    svg['text'] = ''
    svg['now'] = ''
    svg['header'] = '<svg xmlns="http://www.w3.org/2000/svg" width="920px" height="350px" viewBox="0 0 115 43.75">\
    <g font-family="'+font+',sans-serif" style="font-weight:normal" fill="#555555" transform="translate(0,43.75) scale(1, -1)">\
    <g id="graphs" transform="translate(0,5)">'
# generate uvindex graph
    if 'uvi0' in wd:
        svg['uvindex'] = '\
    <linearGradient id="uv" x1="0" x2="0" y1="0" y2="1"> \
    <stop offset="0%" stop-color="yellow"/> \
    <stop offset="54%" stop-color="yellow"/> \
    <stop offset="54%" stop-color="orange"/> \
    <stop offset="72%" stop-color="orange"/> \
    <stop offset="72%" stop-color="orangered"/> \
    <stop offset="100%" stop-color="orangered"/> \
    </linearGradient>\
    \
    <path fill="url(#uv)" stroke="none" opacity="0.2" stroke-linejoin="round" d="M -5,0 L -5,'+wd['uv0']+' \
        0,'+wd['uv0']+' 5,'+wd['uv1']+' 10,'+wd['uv2']+', 15,'+wd['uv3']+' 20,'+wd['uv4']+' \
     25,'+wd['uv5']+' 30,'+wd['uv6']+' 35,'+wd['uv7']+' 40,'+wd['uv8']+' 45,'+wd['uv9']+' \
     50,'+wd['uv10']+' 55,'+wd['uv11']+' 60,'+wd['uv12']+' 65,'+wd['uv13']+' 70,'+wd['uv14']+' \
     75,'+wd['uv15']+' 80,'+wd['uv16']+' 85,'+wd['uv17']+' 90,'+wd['uv18']+' 95,'+wd['uv19']+' \
    100,'+wd['uv20']+' 105,'+wd['uv21']+' 110,'+wd['uv22']+' 115,'+wd['uv23']+' 120,'+wd['uv23']+' 120,0, 125,0 125,20 130,20, 130,0" />'
    if 'p0' in wd:
# generate rain graph
        svg['rain'] = '\
    <linearGradient id="raingrad" x1="0" x2="1" y1="0" y2="0"> \
    <stop offset="0%" stop-opacity="'+wd['op0']+'" stop-color="#03A9F4"/> \
    <stop offset="4.16%" stop-opacity="'+wd['op1']+'" stop-color="#03A9F4"/> \
    <stop offset="8.333%" stop-opacity="'+wd['op2']+'" stop-color="#03A9F4"/> \
    <stop offset="12.5%" stop-opacity="'+wd['op3']+'" stop-color="#03A9F4"/> \
    <stop offset="16.666%" stop-opacity="'+wd['op4']+'" stop-color="#03A9F4"/> \
    <stop offset="20.76%" stop-opacity="'+wd['op5']+'" stop-color="#03A9F4"/> \
    <stop offset="25%" stop-opacity="'+wd['op6']+'" stop-color="#03A9F4"/> \
    <stop offset="29.16%" stop-opacity="'+wd['op7']+'" stop-color="#03A9F4"/> \
    <stop offset="37.46%" stop-opacity="'+wd['op8']+'" stop-color="#03A9F4"/> \
    <stop offset="41.666%" stop-opacity="'+wd['op9']+'" stop-color="#03A9F4"/> \
    <stop offset="45.82%" stop-opacity="'+wd['op10']+'" stop-color="#03A9F4"/> \
    <stop offset="50%" stop-opacity="'+wd['op11']+'" stop-color="#03A9F4"/> \
    <stop offset="54.16%" stop-opacity="'+wd['op12']+'" stop-color="#03A9F4"/> \
    <stop offset="58.333%" stop-opacity="'+wd['op13']+'" stop-color="#03A9F4"/> \
    <stop offset="62.49%" stop-opacity="'+wd['op14']+'" stop-color="#03A9F4"/> \
    <stop offset="66.333%" stop-opacity="'+wd['op15']+'" stop-color="#03A9F4"/> \
    <stop offset="70.44%" stop-opacity="'+wd['op16']+'" stop-color="#03A9F4"/> \
    <stop offset="74.666%" stop-opacity="'+wd['op17']+'" stop-color="#03A9F4"/> \
    <stop offset="78.8%" stop-opacity="'+wd['op18']+'" stop-color="#03A9F4"/> \
    <stop offset="83%" stop-opacity="'+wd['op19']+'" stop-color="#03A9F4"/> \
    <stop offset="87.16%" stop-opacity="'+wd['op20']+'" stop-color="#03A9F4"/> \
    <stop offset="91.333%" stop-opacity="'+wd['op21']+'" stop-color="#03A9F4"/> \
    <stop offset="95.5%" stop-opacity="'+wd['op22']+'" stop-color="#03A9F4"/> \
    <stop offset="100%" stop-opacity="'+wd['op23']+'" stop-color="#03A9F4"/> \
    </linearGradient>\
    \
    <g transform="scale(1,2)">\
    <path fill="#ffffff" stroke="none" d="M 0,-0.01 L \
        0,'+wd['p0']+' 5,'+wd['p1']+' 10,'+wd['p2']+', 15,'+wd['p3']+' 20,'+wd['p4']+' \
     25,'+wd['p5']+' 30,'+wd['p6']+' 35,'+wd['p7']+' 40,'+wd['p8']+' 45,'+wd['p9']+' \
     50,'+wd['p10']+' 55,'+wd['p11']+' 60,'+wd['p12']+' 65,'+wd['p13']+' 70,'+wd['p14']+' \
     75,'+wd['p15']+' 80,'+wd['p16']+' 85,'+wd['p17']+' 90,'+wd['p18']+' 95,'+wd['p19']+' \
    100,'+wd['p20']+' 105,'+wd['p21']+' 110,'+wd['p22']+' 115,'+wd['p23']+' 115,-0.01" />\
    <path fill="url(#raingrad)" stroke="none" d="M 0,-0.01 L \
        0,'+wd['p0']+' 5,'+wd['p1']+' 10,'+wd['p2']+', 15,'+wd['p3']+' 20,'+wd['p4']+' \
     25,'+wd['p5']+' 30,'+wd['p6']+' 35,'+wd['p7']+' 40,'+wd['p8']+' 45,'+wd['p9']+' \
     50,'+wd['p10']+' 55,'+wd['p11']+' 60,'+wd['p12']+' 65,'+wd['p13']+' 70,'+wd['p14']+' \
     75,'+wd['p15']+' 80,'+wd['p16']+' 85,'+wd['p17']+' 90,'+wd['p18']+' 95,'+wd['p19']+' \
    100,'+wd['p20']+' 105,'+wd['p21']+' 110,'+wd['p22']+' 115,'+wd['p23']+' 115,-0.01" /></g>'
# generate cloud graph
    if 'cl0' in wd:
        svg['clouds'] = '\
    <path fill="'+svgtextcolor+'" opacity="'+cloudopacity+'" stroke="none" d="M 0,0 L \
        0,'+wd['cl0']+' 5,'+wd['cl1']+' 10,'+wd['cl2']+', 15,'+wd['cl3']+' 20,'+wd['cl4']+' \
     25,'+wd['cl5']+' 30,'+wd['cl6']+' 35,'+wd['cl7']+' 40,'+wd['cl8']+' 45,'+wd['cl9']+' \
     50,'+wd['cl10']+' 55,'+wd['cl11']+' 60,'+wd['cl12']+' 65,'+wd['cl13']+' 70,'+wd['cl14']+' \
     75,'+wd['cl15']+' 80,'+wd['cl16']+' 85,'+wd['cl17']+' 90,'+wd['cl18']+' 95,'+wd['cl19']+' \
    100,'+wd['cl20']+' 105,'+wd['cl21']+' 110,'+wd['cl22']+' 115,'+wd['cl23']+' 115,0" />'
# generate temperature graph
    if 'tr0' in wd:
        svg['temp'] = '\
    <path fill="none" stroke="indianred" stroke-width="0.8" d="M -5,0 L -5,'+wd['tr0']+' \
        0,'+wd['tr0']+' 5,'+wd['tr1']+' 10,'+wd['tr2']+', 15,'+wd['tr3']+' 20,'+wd['tr4']+' \
     25,'+wd['tr5']+' 30,'+wd['tr6']+' 35,'+wd['tr7']+' 40,'+wd['tr8']+' 45,'+wd['tr9']+' \
     50,'+wd['tr10']+' 55,'+wd['tr11']+' 60,'+wd['tr12']+' 65,'+wd['tr13']+' 70,'+wd['tr14']+' \
     75,'+wd['tr15']+' 80,'+wd['tr16']+' 85,'+wd['tr17']+' 90,'+wd['tr18']+' 95,'+wd['tr19']+' \
    100,'+wd['tr20']+' 105,'+wd['tr21']+' 110,'+wd['tr22']+' 115,'+wd['tr23']+' 120,'+wd['tr23']+' 120,0" /> \
    \
    \
    \
    \
    <g stroke-width=".2" font-size="3" style="font-weight:700;font-family:'+font+',Roboto,Cantarell,sans-serif" transform="translate(113.5,2)    scale(-1, 1)" fill="'+ svgtextcolor +'"> \
     <text x="5" y="'+wd['tr22']+'"    transform="rotate(180 5 '+wd['tr22']+')">\
     <tspan text-anchor="middle">' + wd['t22'] + '°</tspan>\
     </text> \
     <text x="20" y="'+wd['tr19']+'" transform="rotate(180 20 '+wd['tr19']+')"> \
        <tspan text-anchor="middle">' + wd['t19'] + '°</tspan> \
     </text> \
     <text x="35" y="'+wd['tr16']+'" transform="rotate(180 35 '+wd['tr16']+')"> \
        <tspan text-anchor="middle">' + wd['t16'] + '°</tspan> \
     </text> \
     <text x="50" y="'+wd['tr13']+'" transform="rotate(180 50 '+wd['tr13']+')"> \
        <tspan text-anchor="middle">' + wd['t13'] + '°</tspan> \
     </text> \
     <text x="65" y="'+wd['tr10']+'" transform="rotate(180 65 '+wd['tr10']+')"> \
        <tspan text-anchor="middle">' + wd['t10'] + '°</tspan> \
     </text> \
     <text x="80" y="'+wd['tr7']+'" transform="rotate(180 80 '+wd['tr7']+')"> \
        <tspan text-anchor="middle">' + wd['t7'] + '°</tspan> \
     </text> \
     <text x="95" y="'+wd['tr4']+'" transform="rotate(180 95 '+wd['tr4']+')"> \
        <tspan text-anchor="middle">' + wd['t4'] + '°</tspan> \
     </text> \
     <text x="110" y="'+wd['tr1']+'" transform="rotate(180 110 '+wd['tr1']+')"> \
        <tspan text-anchor="middle">' + wd['t1'] + '°</tspan> \
     </text> \
    </g>\
    </g>'
# generate main text section
    if 'temperature' in wd:
        svg['text'] = '\
    <g id="current-icon" transform="translate(1.5,42.5) scale(0.095, -0.095)">' + wd['icon'] + '</g> \
    \
    <g id="main-text" transform="translate(0,45) scale(1, -1)" fill="'+ svgtextcolor +'"> \
        <text x="18" y="13" font-size="13"> \
            <tspan word-spacing="0" font-family="'+font+' Mono, monospace" style="font-weight:normal">' + wd['temperature'] + '°</tspan> \
        </text> \
        <text x="'+wd['lentempoffset']+'" y="8" font-size="5px"> \
            <tspan word-spacing="0" style="font-weight:700">' + wd['city'] +'</tspan> \
        </text> \
        <text x="'+wd['lentempoffset']+'" y="13" font-size="4.5px"> \
            <tspan word-spacing="0">' + wd['condition'] + '<g visibility="hidden">' + wd["windClass"]['separator'] + wd["windClass"]['definition'] + '</g></tspan> \
        </text>\
        \
        \
        <g transform="translate(102,2)"> \
        <rect x="-5" y="0.5" height="14.5" width="0.2" fill="'+ svgtextcolor +'" opacity="0.2" /> \
        <text x="1" y="3" fill="'+ svgtextcolor +'" font-size="3">'+ wd['pressure']+'<tspan font-size="2.5">mb</tspan></text>' + wd['pr_symbol'] + '\
        \
        \
        <polygon stroke="' + wd["windClass"]['outline'] + '" stroke-width="0.5" fill="' + wd["windClass"]['colour'] + '" points="1.5,0 0,3 1.5,2.5 3,3" transform="translate(-2.5, 6)    rotate('+ wd["windBearing"] +' 1.2 1.5) scale(0.8,1)"/>\
        <text x="1.2" y="8.5" fill="'+ svgtextcolor +'"  font-size="3">' + wd["windSpeed"] + wd['windGust'] + '<tspan font-size="2.5">' + distance + '</tspan></text>\
        \
        \
        <g transform="translate(-2.8,11.7) scale(0.02, 0.02)"> '+humidity+' </g> \
        <text x="1.2" y="14" fill="'+ svgtextcolor +'"   font-size="3">'+ wd['humidity']+'%</text></g> \
        \
        \
    <g stroke-width=".2" font-size="3.3" fill="'+ svgtextcolor +'" transform="translate(-1.5,44.5)"> \
     <text x="5" y="0"><tspan text-anchor="middle">' + wd['h1'] + '</tspan></text> \
     <text x="20" y="0"> <tspan text-anchor="middle">' + wd['h4'] + '</tspan></text> \
     <text x="35" y="0"> <tspan text-anchor="middle">' + wd['h7'] + '</tspan></text> \
     <text x="50" y="0"> <tspan text-anchor="middle">' + wd['h10'] + '</tspan></text> \
     <text x="65" y="0"> <tspan text-anchor="middle">' + wd['h13'] + '</tspan></text> \
     <text x="80" y="0"> <tspan text-anchor="middle">' + wd['h16'] + '</tspan></text> \
     <text x="95" y="0"> <tspan text-anchor="middle">' + wd['h19'] + '</tspan></text> \
     <text x="110" y="0"> <tspan text-anchor="middle">' + wd['h22'] + '</tspan></text> \
    </g>\
    </g>\
    </g>\
    </svg>'
# generate separate images with daily conditions
    wd['dday0'] = '<tspan style="font-weight:bold">Today</tspan>'
    if 'dmin0' in wd:
        for item in range(8):
            svg['day{0}'.format(item)] = '<svg xmlns="http://www.w3.org/2000/svg" width="810px" height="40px" viewBox="0 0 101.25 5"><g font-size="3.1" fill="'+ svgtextcolor +'" font-family="'+font+'">\
            \
            \
            <g transform="translate(0,0.5)">\
            <text x="0.1" y="3">'+wd['dday{0}'.format(item)]+'</text> \
            <g transform="translate(16,-0.5) scale(0.035, 0.035)"> '+wd['dicon{0}'.format(item)]+' </g> \
            <g transform="translate(28.5,0)" font-weight="700" font-size="2.8" fill="#333">\
                <path fill="none" stroke="rgba(0,0,0,.2)" stroke-linecap="round" stroke-width="3.8" d="M'+wd['dminpos{0}'.format(item)]+',2 '+wd['dmaxpos{0}'.format(item)]+',2" transform="translate(0.3,0.3)"/>\
                \
                <path fill="none" stroke="wheat" stroke-linecap="round" stroke-width="3.8" d="M'+wd['dminpos{0}'.format(item)]+',2 '+wd['dmaxpos{0}'.format(item)]+',2"/>\
                \
                <text x="'+wd['dminpos{0}'.format(item)]+'" y="3" transform="translate(-0.5,0)" text-anchor="start"> '+wd['dmin{0}'.format(item)]+'</text> \
                \
                <linearGradient id="overlay" x1="0" x2="1" y1="0" y2="0"> \
                <stop offset="0%" stop-opacity="0" stop-color="wheat"/> \
                <stop offset="40%" stop-opacity="1" stop-color="wheat"/> \
                <stop offset="100%" stop-opacity="1" stop-color="wheat"/> \
                </linearGradient>\
                \
                <rect fill="url(#overlay)" height="3.5" width="5.5" x="'+ wd['dmaxpos{0}'.format(item)] +'" y="0.3" transform="translate(-4.6,0)"/>\
                \
                <text x="'+ wd['dmaxpos{0}'.format(item)] +'" y="3" text-anchor="end" transform="translate(1,0)">'+ wd['dmax{0}'.format(item)] +'</text> \
                \
                \
            </g>\
            \
            <g transform="translate(68,0)"> \
            <text x="0" y="3" fill="'+ svgtextcolor +'">'+ wd['dpr{0}'.format(item)]+'<tspan font-size="2.5">mb</tspan></text>' + wd['pr_symbol{0}'.format(item)] + '</g>\
            \
            <polygon stroke="' + wd["windClass{0}".format(item)]['outline'] + '" stroke-width="0.5" fill="' + wd["windClass{0}".format(item)]['colour'] + '" points="1.5,0 0,3 1.5,2.5 3,3" transform="translate(84, 0.5)    rotate('+ wd["windBearing{0}".format(item)] +' 1.2 1.5) scale(0.8,1)"/>\
            <text x="88" y="3" fill="'+ svgtextcolor +'">' + wd["windSpeed{0}".format(item)] + '<tspan font-size="2.5">' + distance + '</tspan></text>\
            \
            </g></g></svg>'
#
# concatenate svg sections and convert to base64
#
    svg['base'] = base64.b64encode(bytes(svg['header'] + svg['clouds'] + svg['uvindex'] + svg['rain'] + svg['temp'] + svg['text']))
    for item in range(8):
        svg["day{0}".format(item)] = base64.b64encode(bytes(svg["day{0}".format(item)]))
#
# generate base64 icons for daily section 
#
    clearday_b64 = base64.b64encode(bytes(svgsnippet + clearday + '</svg>'))
    clearnight_b64 = base64.b64encode(bytes(svgsnippet + clearnight + '</svg>'))
    cloudy_b64 = base64.b64encode(bytes(svgsnippet + cloudy + '</svg>'))
    wind_b64 = base64.b64encode(bytes(svgsnippet + wind + '</svg>'))
    uvindex_b64 = base64.b64encode(bytes(svgsnippet + uvindex + '</svg>'))
    humidity_b64 = base64.b64encode(bytes(svgsnippet + humidity + '</svg>'))
#
# print daily section
#
    if 'base' in svg:
        print '| imageHeight="' + graphHeight + '" imageWidth="' + graphWidth + '" image=' + svg['base']
    if 'day0' in svg:
        print "---"
        for item in range(8):
            print '| imageHeight="' + imageHeight + '" imageWidth="' + imageWidth + '" image=' + svg['day{0}'.format(item)]
            if 'ds0' in wd:
                print '--'+wd['ds{0}'.format(item)] + '|imageHeight=' + imageHeight + ' image=' + base64.b64encode(bytes(svgsnippet + wd['dicon{0}'.format(item)] + '</svg>'))
            if wd["apparentTemperatureMin{0}".format(item)] != wd["dmin{0}".format(item)] or wd["apparentTemperatureMax{0}".format(item)] != wd["dmax{0}".format(item)]:
                print '--'+wd["apparentTemperatureMin{0}".format(item)] + '° ⁓ ' +wd["apparentTemperatureMax{0}".format(item)] + '°   <span color="'+highlight+'" font="10">Apparent temperature</span> | imageHeight=' + imageHeight + ' image=' + temperature
            if 'windSpeed0' in wd:
                print '--'+ wd["windClass{0}".format(item)]['definition'] + wd["windClass{0}".format(item)]['separator'] + wd["windSpeed{0}".format(item)] + '<span font="9"> ' + distance + '</span><span color="'+highlight+'" font="10">   Wind speed</span>   •   ' + wd["windGust{0}".format(item)] + '<span font="9"> ' + distance + '</span><span color="'+highlight+'" font="10">   Gusts</span>| imageHeight=' + imageHeight + ' image=' + wind_b64
            if 'cloudCover0' in wd and 'uvIndex0' in wd:
                print '--'+wd["cloudCover{0}".format(item)] + '   <span color="'+highlight+'" font="10">Cloud cover</span>   •   '+wd["uvIndex{0}".format(item)] + '   <span color="'+highlight+'" font="10">UV Index</span> | imageHeight=' + imageHeight + ' image=' + uvindex_b64
            elif 'cloudCover0' in wd:
                print '--'+wd["cloudCover{0}".format(item)] + '   <span color="'+highlight+'" font="10">Cloud cover</span>| imageHeight=' + imageHeight + ' image=' + cloudy_b64
            if 'dewPoint0' in wd and 'humidity0' in wd:
                print '--'+wd["humidity{0}".format(item)] + '   <span color="'+highlight+'" font="10">Humidity </span>   •   ' +wd["dewPoint{0}".format(item)] + '   <span color="'+highlight+'" font="10">Dew point</span>| imageHeight=' + imageHeight + ' image=' + humidity_b64
            if 'dsr0' in wd and 'dst0' in wd:
                print '--'+wd['dsr{0}'.format(item)]+'  •  '+wd['dst{0}'.format(item)] + '   <span color="'+highlight+'" font="10">Sunrise and sunset time</span>| imageHeight=' + imageHeight + ' image=' + clearday_b64
            if 'moonPhaseSymbol0' in wd:
                print '--' + wd["moonPhaseSymbol{0}".format(item)] + '| imageHeight=' + imageHeight + ' image=' + clearnight_b64
#
# print info section
#
    timestamp = strftime("%H:%M")
#
    print '<span color="'+highlight+'">Last update: ' +timestamp + '</span>| iconName=view-more-horizontal-symbolic'
    print '--Update| refresh=true iconName=view-refresh-symbolic'
    print '--Web forecast for ' + wd['city'] + '| iconName=web-browser-symbolic href=https://darksky.net/forecast/' + wd['loc'] + '/si24/en'
    print '--Powered by DarkSky | iconName=web-browser-symbolic href=https://darksky.net/poweredby/?ref=argosWeather'

def print_main():

    wd = get_wx()

    if wd is False:
        print '| imageHeight=' + imageHeight + ' image=' + nodata
        print '---'
        print 'No API data | refresh=true iconName=view-refresh-symbolic'
        print 'Check DarkSky status | href=http://status.darksky.net/ iconName=web-browser-symbolic'
        return False
#
# determine if script will show next weather condition alongside current
#
    conditions = set(["rain", "snow", "sleet", "fog"])
    if 'icon' in wd and 'temperature' in wd:
        if wd['status1'] in conditions and wd['status'] != wd['status1']:
            nextCondition = wd['t1']
            nextIcon = wd['icon1']
            nextConditionSymbol = '→'
        elif wd['status2'] in conditions and wd['status'] != wd['status2']:
            nextCondition = wd['t2']
            nextIcon = wd['icon2']
            nextConditionSymbol = '⇉'
        elif wd['status3'] in conditions and wd['status'] != wd['status3']:
            nextCondition = wd['t3']
            nextIcon = wd['icon3']
            nextConditionSymbol = '⇶'
        # test 
        elif wd['status'] == '123':
            wd['temperature'] = '000'
            nextCondition = '-000'
            nextIcon = wd['icon3']
            nextConditionSymbol = '→'
        # test
        else:
            nextCondition = ''
            nextIcon = ''
            nextConditionSymbol = ''

    lentemp = int((len(wd['temperature']) * 24) - 10)
    if nextCondition:
        lentemp2 = int(145 + (len(nextCondition) * 24))
    else:
        lentemp2 = 0
    translate = int(300 + (len(wd['temperature']) * 50))
#
# generate system bar icon
#
    mainIconWidth = str(int(120 + lentemp + lentemp2))
    mainIcon = base64.b64encode(bytes('<svg xmlns="http://www.w3.org/2000/svg" height="80" width="'+mainIconWidth+'"><g fill="'+mainiconfontcolor+'" font-family="'+font+' Mono,monospace" font-weight="900" font-size="100"><g transform="scale(.5,.5) translate(0,15)">'+wd['icon']+'<text font-size="100" x="155" y="95" xml:space="preserve">'+wd['temperature']+'°<tspan font-size="20"> </tspan>'+nextConditionSymbol+'   '+nextCondition+'°</text>\
    \
    <g transform="translate('+str(translate)+',0)">' + nextIcon +'</g>\
    \
    </g></g></svg>'))

    print '| imageHeight='+iconHeight+' image=' + mainIcon
    print '---'
#
    gen_svg()
#
# check if internet connection is present. new way.
#
def ping():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((hostname, int(port)))
        s.shutdown(2)
        return True
    except:
        return False

def checks():

    check = True

    ping_1 = ping()
    if ping_1 is False:
        time.sleep(10)
        ping_2 = ping()
        if ping_2 is False:
            time.sleep(10)
            ping_3 = ping()
            if ping_3 is False:
                print '| imageHeight=' + imageHeight + ' image=' + nodata
                print '---'
                print 'No Internet connection | iconName=dialog-warning-symbolic'
        	print 'Check DarkSky status | href=http://status.darksky.net/ iconName=web-browser-symbolic'
                check = False
#
    if api_key == '':
        print '| imageHeight='+imageHeight+' image=' + nodata
        print '---'
        print 'Missing API key'
        print 'Get an API Key | href=https://darksky.net/dev'
        check = False
#
    if check is True:
# if checks are passed, go to main
        print_main()
    else:
        print 'Refresh | refresh=true iconName=view-refresh-symbolic'

checks()
