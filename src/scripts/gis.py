#!/usr/bin/env python
# coding: utf-8

# sen giderken adımlarını sayarım, heyhat
# ne yazık, seni yanlış tanıdım sanırım

from geopy.geocoders import Nominatim

geocoder = Nominatim("ist.gezmelik.services")


def find_location(place: str) -> dict:
    location = geocoder.geocode(place)
    if (location):
        return {
            'adres': location.address,
            'geo_x': location.latitude,
            'geo_y': location.longitude
        }
    else:
        return False


def routing(pos_a: tuple, pos_b: tuple, vhcl: str) -> dict:
    return None
