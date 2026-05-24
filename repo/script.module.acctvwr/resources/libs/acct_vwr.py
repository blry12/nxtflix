# -*- coding: utf-8 -*-
import xbmc, xbmcaddon, xbmcvfs
import json
import os
import sqlite3

from sqlite3 import Error
from xml.etree import ElementTree
from resources.libs.common.config import CONFIG
from resources.libs.common import logging

# Variables
amgr = 'NXTFlix Light ERROR'
translatePath = xbmcvfs.translatePath

# Auth cache
AUTH_CACHE = {}

# Realizer json Path
chkset_realx_json = translatePath('special://profile/addon_data/plugin.video.realizerx/rdauth.json')


ORDER = ['nxtflixlt',
         'gears',
         'redlt',
         #'fen',
         'umb',
         'pov',
         #'dradis',
         'genocide',
         'coal',    # Premiumize Only
         #'seren',
         'shadow',
         'ghost',
         'chains',
         'homelander',
         'nightwing',
         'absolution',
         'thecrew',
         'salts',
         #'orion',
         #'genesis',
         #'syncher',
         'scrubs',
         'gratisred',
         'otaku',
         'rurl',
         'tmdbhelper',
         #'tkplay',
         'trakt',
         'premx',   # Premiumize Only
         'realx',   # Real-Debrid Only
         'fentastic',
         'nimbus',
         'acctmgr']

ADDONS = {
    #NXTFlix Light
    'nxtflixlt': {
        'name'        : 'NXTFlix Light',
        'plugin'      : 'plugin.video.nxtflixlt',
        'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.nxtflixlt'),
        'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.nxtflixlt/resources/media/addon_icons/', 'fenlight_icon_01.png'),
        'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.nxtflixlt/resources/media/', 'fenlight_fanart2.jpg'),
        'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.nxtflixlt/databases', 'settings.db'),
        #TK
        'default_tk'  : 'trakt.token',
        'data_tk'     : [],
        #RD
        'default_rd'  : 'rd.token',
        'data_rd'     : [],
        #PM
        'default_pm'  : 'pm.token',
        'data_pm'     : [],
        #AD
        'default_ad'  : 'ad.token',
        'data_ad'     : [],
        #ED
        'default_ed'  : 'ed.token',
        'data_ed'     : [],
        #TB
        'default_tb'  : 'tb.token',
        'data_tb'     : [],
        #EN
        'default_en'  : 'easynews_password',
        'data_en'     : [],
    },

    #GEARS
    'gears': {
        'name'        : 'The Gears',
        'plugin'      : 'plugin.video.gears',
        'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.gears'),
        'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.gears/resources/media/addon_icons/', 'icon.png'),
        'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.gears/', 'fanart.jpg'),
        'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.gears/databases', 'settings.db'),
        #TK
        'default_tk'  : 'trakt.token',
        'data_tk'     : [],
        #RD
        'default_rd'  : 'rd.token',
        'data_rd'     : [],
        #PM
        'default_pm'  : 'pm.token',
        'data_pm'     : [],
        #AD
        'default_ad'  : 'ad.token',
        'data_ad'     : [],
        #ED
        'default_ed'  : 'ed.token',
        'data_ed'     : [],
        #TB
        'default_tb'  : 'tb.token',
        'data_tb'     : [],
        #OC
        #'default_oc'  : 'oc.token',
        #'data_oc'     : [],
        #EN
        'default_en'  : 'easynews_password',
        'data_en'     : [],
    },

    #RED LIGHT
    'redlt': {
        'name'        : 'Red Light',
        'plugin'      : 'plugin.video.redlight',
        'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.redlight'),
        'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.redlight/resources/media/addon_icons/', 'icon.png'),
        'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.redlight/resources/media/', 'fanart.jpg'),
        'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.redlight/databases', 'settings.db'),
        #TK
        'default_tk'  : 'trakt.token',
        'data_tk'     : [],
        #RD
        'default_rd'  : 'rd.token',
        'data_rd'     : [],
        #PM
        'default_pm'  : 'pm.token',
        'data_pm'     : [],
        #AD
        'default_ad'  : 'ad.token',
        'data_ad'     : [],
        #ED
        'default_ed'  : 'ed.token',
        'data_ed'     : [],
        #TB
        'default_tb'  : 'tb.token',
        'data_tb'     : [],
        #EN
        'default_en'  : 'easynews_password',
        'data_en'     : [],
    },
    
    #UMBRELLA
    'umb': {
        'name'        : 'Umbrella',
        'plugin'      : 'plugin.video.umbrella',
        'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella'),
        'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella', 'icon.png'),
        'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella', 'fanart.jpg'),
        'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.umbrella', 'settings.xml'),
        #TK
        'default_tk'  : 'trakt.user.token',
        'data_tk'     : ['trakt.user.token', 'trakt.user.name', 'trakt.token.expires', 'trakt.authed.clientid', 'trakt.refreshtoken', 'trakt.isauthed', 'indicators', 'trakt.scrobble', 'resume.source'],
        #MDB
        'default_mdb'  : 'mdblist.api',
        'data_mdb'     : ['mdblist.api'],
        #RD
        'default_rd'  : 'realdebridtoken',
        'data_rd'     : ['realdebridusername', 'realdebridtoken', 'realdebrid.clientid', 'realdebridsecret', 'realdebridrefresh', 'realdebrid.enable'],
        #PM
        'default_pm'  : 'premiumizetoken',
        'data_pm'     : ['premiumizeusername', 'premiumizetoken', 'premiumize.enable'],
        #AD
        'default_ad'  : 'alldebridtoken',
        'data_ad'     : ['alldebridusername', 'alldebridtoken', 'alldebrid.enable'],
        #ED
        'default_ed'  : 'easydebridtoken',
        'data_ed'     : ['easydebridtoken', 'easydebrid.enable'],
        #TB
        'default_tb'  : 'torboxtoken',
        'data_tb'     : ['torboxtoken', 'torbox.username', 'torbox.enable'],
        #OC
        #'default_oc'  : 'offcloudtoken',
        #'data_oc'     : ['offcloudtoken', 'offcloud.enable', 'offcloud.username'],
        #EN
        'default_en'  : 'easynews.password',
        'data_en'     : ['easynews.password', 'easynews.user', 'easynews.enable'],
    },

    #POV
    'pov': {
        'name'        : 'POV',
        'plugin'      : 'plugin.video.pov',
        'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.pov'),
        'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.pov', 'pov.png'),
        'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.pov', 'pov_fanart.png'),
        'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.pov', 'settings.xml'),
        #TK
        'default_tk'  : 'trakt.token',
        'data_tk'     : ['trakt.refresh', 'trakt.expires', 'trakt.token', 'trakt_user', 'trakt_indicators_active', 'watched_indicators'], # Trakt Client/Secret NOT required here for revoke due to default API keys being stored in the settings.xml
        #MDB
        'default_mdb'  : 'mdblist.token',
        'data_mdb'     : ['mdblist.token', 'mdblist_user', 'watched_indicators', 'mdbl_indicators_active'],
        #RD
        'default_rd'  : 'rd.token',
        'data_rd'     : ['rd.username', 'rd.token', 'rd.client_id', 'rd.refresh', 'rd.secret', 'rd.enabled'],
        #PM
        'default_pm'  : 'pm.token',
        'data_pm'     : ['pm.account_id', 'pm.token', 'pm.enabled'],
        #AD
        'default_ad'  : 'ad.token',
        'data_ad'     : ['ad.account_id', 'ad.enabled', 'ad.token'],
        #ED
        'default_ed'  : 'eb.token',
        'data_ed'     : ['ed.token', 'ed.account_id', 'ed.enabled'],
        #TB
        'default_tb'  : 'tb.token',
        'data_tb'     : ['tb.token', 'tb.account_id', 'tb.expires', 'tb.enabled'],
        #OC
        'default_oc'  : 'oc.token',
        'data_oc'     : ['oc.token', 'oc.account_id', 'oc.enabled'],
        #EN
        'default_en'  : 'easynews_password',
        'data_en'     : ['easynews_password', 'easynews_user', 'provider.easynews'],
    },

    #GENOCIDE
    'genocide': {
        'name'        : 'Genocide',
        'plugin'      : 'plugin.video.genocide',
        'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.genocide'),
        'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.genocide', 'icon.png'),
        'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.genocide', 'fanart.jpg'),
        'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.genocide', 'settings.xml'),
        #TK
        'default_tk'  : 'trakt.token',
        'data_tk'     : ['trakt.token', 'trakt.username', 'trakt.expires', 'trakt.refresh', 'trakt.isauthed', 'trakt_user'], # Trakt Client/Secret NOT required here for revoke due to default API keys being stored in the settings.xml
        #RD
        'default_rd'  : 'realdebrid.token',
        'data_rd'     : ['realdebrid.username', 'realdebrid.token', 'realdebrid.client_id', 'realdebrid.secret', 'realdebrid.refresh', 'realdebrid.enable'],
        #PM
        'default_pm'  : 'premiumize.token',
        'data_pm'     : ['premiumize.username', 'premiumize.token', 'premiumize.enable'],
        #AD
        'default_ad'  : 'alldebrid.token',
        'data_ad'     : ['alldebrid.username', 'alldebrid.token', 'alldebrid.enable'],
        #TB
        'default_tb'  : 'torbox.token',
        'data_tb'     : ['torbox.token', 'torbox.username', 'torbox.enable', 'torbox.expires'],
        #OC
        #'default_oc'  : 'offcloud.token',
        #'data_oc'     : ['offcloud.token', 'offcloud.username', 'offcloud.enable'],
        #EN
        'default_en'  : 'easynews_password',
        'data_en'     : ['easynews_password', 'easynews_user', 'provider.easynews'],
    },

    #THE COALITION
    'coal': {
        'name'        : 'The Coalition',
        'plugin'      : 'plugin.video.coalition',
        'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.coalition'),
        'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.coalition', 'icon.png'),
        'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.coalition', 'fanart.png'),
        'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.coalition', 'settings.xml'),
        #TK
        'default_tk'  : 'trakt.token',
        'data_tk'     : ['trakt.refresh', 'trakt.expires', 'trakt.token', 'trakt_user', 'trakt_indicators_active', 'watched_indicators'], # Trakt Client/Secret NOT required here for revoke due to default API keys being stored in the settings.xml
        #MDB
        'default_mdb'  : 'mdblist.token',
        'data_mdb'     : ['mdblist.token'],
        #PM
        'default_pm'  : 'pm.token',
        'data_pm'     : ['pm.account_id', 'pm.token', 'pm.enabled'],
    },

    #SHADOW
    'shadow': {
        'name'        : 'Shadow',
        'plugin'      : 'plugin.video.shadow',
        'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow'),
        'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow', 'icon.png'),
        'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow', 'fanart.jpg'),
        'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.shadow', 'settings.xml'),
        #TK
        'default_tk'  : 'trakt_access_token',
        'data_tk'     : ['trakt_expires_at', 'trakt_refresh_token', 'trakt_access_token'],
        #RD
        'default_rd'  : 'rd.auth',
        'data_rd'     : ['rd.auth', 'rd.client_id', 'rd.refresh', 'rd.secret', 'debrid_use', 'debrid_use_rd'],
        #PM
        'default_pm'  : 'premiumize.token',
        'data_pm'     : ['premiumize.token', 'debrid_use', 'debrid_use_pm'],
        #AD
        'default_ad'  : 'alldebrid.token',
        'data_ad'     : ['alldebrid.username', 'alldebrid.token', 'debrid_use_ad', 'debrid_use'],
        #TB
        'default_tb'  : 'tb.token',
        'data_tb'     : ['tb.token', 'tb.account_id', 'debrid_use_tr', 'debrid_use'],
    },

    #GHOST
    'ghost': {
        'name'        : 'Ghost',
        'plugin'      : 'plugin.video.ghost',
        'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.ghost'),
        'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.ghost', 'icon.png'),
        'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.ghost', 'fanart.jpg'),
        'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.ghost', 'settings.xml'),
        #TK
        'default_tk'  : 'trakt_access_token',
        'data_tk'     : ['trakt_expires_at', 'trakt_refresh_token', 'trakt_access_token'],
        #RD
        'default_rd'  : 'rd.auth',
        'data_rd'     : ['rd.auth', 'rd.client_id', 'rd.refresh', 'rd.secret', 'debrid_use', 'debrid_use_rd'],
        #PM
        'default_pm'  : 'premiumize.token',
        'data_pm'     : ['premiumize.token', 'debrid_use', 'debrid_use_pm'],
        #AD
        'default_ad'  : 'alldebrid.token',
        'data_ad'     : ['alldebrid.username', 'alldebrid.token', 'debrid_use_ad', 'debrid_use'],
        #TB
        'default_tb'  : 'tb.token',
        'data_tb'     : ['tb.token', 'tb.account_id', 'debrid_use_tr', 'debrid_use'],
    },

    #THE CHAINS
    'chains': {
        'name'        : 'The Chains',
        'plugin'      : 'plugin.video.thechains',
        'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.thechains'),
        'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.thechains', 'icon.png'),
        'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.thechains', 'fanart.jpg'),
        'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thechains', 'settings.xml'),
        #TK
        'default_tk'  : 'trakt_access_token',
        'data_tk'     : ['trakt_expires_at', 'trakt_refresh_token', 'trakt_access_token'],
        #RD
        'default_rd'  : 'rd.auth',
        'data_rd'     : ['rd.auth', 'rd.client_id', 'rd.refresh', 'rd.secret', 'debrid_use', 'debrid_use_rd'],
        #PM
        'default_pm'  : 'premiumize.token',
        'data_pm'     : ['premiumize.token', 'debrid_use', 'debrid_use_pm'],
        #AD
        'default_ad'  : 'alldebrid.token',
        'data_ad'     : ['alldebrid.username', 'alldebrid.token', 'debrid_use_ad', 'debrid_use'],
        #TB
        'default_tb'  : 'tb.token',
        'data_tb'     : ['tb.token', 'tb.account_id', 'debrid_use_tr', 'debrid_use'],
    },
    
    #HOMELANDER
    'homelander': {
        'name'        : 'Homelander',
        'plugin'      : 'plugin.video.homelander',
        'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.homelander'),
        'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.homelander', 'icon.png'),
        'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.homelander', 'fanart.jpg'),
        'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.homelander', 'settings.xml'),
        #TK
        'default_tk'  : 'trakt.token',
        'data_tk'     : ['trakt.authed', 'trakt.user', 'trakt.token', 'trakt.refresh', 'trakt.client_id', 'trakt.client_secret'],
    },

    #NIGHTWING
    'nightwing': {
        'name'        : 'Nightwing',
        'plugin'      : 'plugin.video.nightwing',
        'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.nightwing'),
        'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.nightwing', 'icon.png'),
        'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.nightwing', 'fanart.jpg'),
        'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.nightwing', 'settings.xml'),
        #TK
        'default_tk'  : 'trakt.token',
        'data_tk'     : ['trakt.authed', 'trakt.user', 'trakt.token', 'trakt.refresh', 'trakt.client_id', 'trakt.client_secret'],
    },

    #JOKERS ABSOLUTION
    'absolution': {
        'name'        : 'Jokers Absolution',
        'plugin'      : 'plugin.video.absolution',
        'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.absolution'),
        'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.absolution', 'icon.png'),
        'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.absolution', 'fanart.jpg'),
        'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.absolution', 'settings.xml'),
        #TK
        'default_tk'  : 'trakt.token',
        'data_tk'     : ['trakt.authed', 'trakt.user', 'trakt.token', 'trakt.refresh', 'trakt.client_id', 'trakt.client_secret'],
    },

    #THE CREW
    'thecrew': {
        'name'        : 'The Crew',
        'plugin'      : 'plugin.video.thecrew',
        'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.thecrew'),
        'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.thecrew', 'icon.png'),
        'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.thecrew', 'fanart.jpg'),
        'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thecrew', 'settings.xml'),
        #TK
        'default_tk'  : 'trakt.token',
        'data_tk'     : ['trakt.refresh', 'trakt.token', 'trakt.user'],
    },

    #SALTS
    'salts': {
        'name'        : 'SALTS',
        'plugin'      : 'plugin.video.salts',
        'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.salts'),
        'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.salts', 'icon.png'),
        'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.salts', 'fanart.jpg'),
        'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.salts', 'settings.xml'),
        #TK
        'default_tk'  : 'trakt_access_token',
        'data_tk'     : ['trakt_expires', 'trakt_refresh_token', 'trakt_access_token', 'trakt_enabled'],
        #RD
        'default_rd'  : 'realdebrid_token',
        'data_rd'     : ['realdebrid_token', 'realdebrid_refresh', 'realdebrid_expires', 'realdebrid_enabled'],
        #PM
        'default_pm'  : 'premiumize_token',
        'data_pm'     : ['premiumize_token', 'premiumize_enabled'],
        #AD
        'default_ad'  : 'alldebrid_token',
        'data_ad'     : ['alldebrid_token', 'alldebrid_enabled'],
    },

    #SCRUBS V2
    'scrubs': {
        'name'        : 'Scrubs V2',
        'plugin'      : 'plugin.video.scrubsv2',
        'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.scrubsv2'),
        'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.scrubsv2/resources/images', 'icon.png'),
        'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.scrubsv2/resources/images', 'fanart.jpg'),
        'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.scrubsv2', 'settings.xml'),
        #TK
        'default_tk'  : 'trakt.token',
        'data_tk'     : ['trakt.refresh', 'trakt.token', 'trakt.user', 'trakt.authed'],
    },

    #GRATIS RED
    'gratisred': {
        'name'        : 'Gratis Red',
        'plugin'      : 'plugin.video.gratisred',
        'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.gratisred'),
        'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.gratisred/resources/images', 'icon.png'),
        'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.gratisred/resources/images', 'fanart.jpg'),
        'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.gratisred', 'settings.xml'),
        #TK
        'default_tk'  : 'trakt.token',
        'data_tk'     : ['trakt.refresh', 'trakt.token', 'trakt.user', 'trakt.authed'],
    },

    #OTAKU
    'otaku': {
        'name'        : 'Otaku',
        'plugin'      : 'plugin.video.otaku',
        'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.otaku'),
        'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.otaku', 'icon.png'),
        'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.otaku', 'fanart.jpg'),
        'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.otaku', 'settings.xml'),
        #RD
        'default_rd'  : 'realdebrid.token',
        'data_rd'     : ['realdebrid.username', 'realdebrid.token', 'realdebrid.client_id', 'realdebrid.secret', 'realdebrid.refresh', 'realdebrid.enabled'],
        #PM
        'default_pm'  : 'premiumize.token',
        'data_pm'     : ['premiumize.username', 'premiumize.token', 'premiumize.enabled'],
        #AD
        'default_ad'  : 'alldebrid.token',
        'data_ad'     : ['alldebrid.username', 'alldebrid.token', 'alldebrid.enabled'],
        #ED
        'default_ed'  : 'eb.token',
        'data_ed'     : [],
        #TB
        'default_tb'  : 'torbox.token',
        'data_tb'     : ['torbox.token', 'torbox.username', 'torbox.enabled', 'torbox.auth.status'],
    },

    #RESOLVEURL
    'rurl': {
        'name'        : 'ResolveURL',
        'plugin'      : 'script.module.resolveurl',
        'path'        : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl'),
        'icon'        : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl', 'icon.png'),
        'fanart'      : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl', 'fanart.jpg'),
        'settings'    : os.path.join(CONFIG.ADDON_DATA, 'script.module.resolveurl', 'settings.xml'),
        #RD
        'default_rd'  : 'RealDebridResolver_token',
        'data_rd'     : ['RealDebridResolver_client_id', 'RealDebridResolver_client_secret', 'RealDebridResolver_refresh', 'RealDebridResolver_token', 'RealDebridResolver_cached_only'],
        #PM
        'default_pm'  : 'PremiumizeMeResolver_token',
        'data_pm'     : ['PremiumizeMeResolver_token', 'PremiumizeMeResolver_cached_only', 'premiumize.status'],
        #AD
        'default_ad'  : 'AllDebridResolver_token',
        'data_ad'     : ['AllDebridResolver_token', 'AllDebridResolver_cached_only'],
    },

    #TMDb HELPER
    'tmdbhelper': {
        'name'        : 'TMDb Helper',
        'plugin'      : 'plugin.video.themoviedb.helper',
        'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.themoviedb.helper'),
        'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.themoviedb.helper', 'icon.png'),
        'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.themoviedb.helper', 'fanart.jpg'),
        'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.themoviedb.helper', 'settings.xml'),
        #TK
        'default_tk'  : 'trakt_token',
        'data_tk'     : ['trakt_token'],
        #MDB
        'default_mdb'  : 'mdblist_apikey',
        'data_mdb'     : ['mdblist_apikey'],
    },

    #TRAKT ADDON
    'trakt': {
        'name'        : 'Trakt Add-on',
        'plugin'      : 'script.trakt',
        'path'        : os.path.join(CONFIG.ADDONS, 'script.trakt'),
        'icon'        : os.path.join(CONFIG.ADDONS, 'script.trakt', 'icon.png'),
        'fanart'      : os.path.join(CONFIG.ADDONS, 'script.trakt', 'fanart.jpg'),
        'settings'    : os.path.join(CONFIG.ADDON_DATA, 'script.trakt', 'settings.xml'),
        #TK
        'default_tk'  : 'authorization',
        'data_tk'     : ['authorization', 'user'],
    },

    #PREMIUMIZERX
    'premx': {
        'name'        : 'Premiumizer',
        'plugin'      : 'plugin.video.premiumizerx',
        'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizerx'),
        'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizerx', 'icon.png'),
        'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizerx', 'fanart.jpg'),
        'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.premiumizerx', 'settings.xml'),
        #PM
        'default_pm'  : 'premiumize.token',
        'data_pm'     : ['premiumize.status', 'premiumize.token', 'premiumize.refresh'],
    },

    #REALIZERX
    'realx': {
        'name'        : 'Realizer',
        'plugin'      : 'plugin.video.realizerx',
        'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.realizerx'),
        'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.realizerx', 'icon.png'),
        'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.realizerx', 'fanart.png'),
        'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.realizerx', 'rdauth.json'),
        #RD
        'default_rd'  : 'token',
        'data_rd'     : [],
    },

    #FENTASTIC
    'fentastic': {
        'name'        : 'FENtastic',
        'plugin'      : 'skin.fentastic',
        'path'        : os.path.join(CONFIG.ADDONS, 'skin.fentastic'),
        'icon'        : os.path.join(CONFIG.ADDONS, 'skin.fentastic', 'icon.png'),
        'fanart'      : os.path.join(CONFIG.ADDONS, 'skin.fentastic', 'fanart.png'),
        'settings'    : os.path.join(CONFIG.ADDON_DATA, 'skin.fentastic', 'settings.xml'),
        #MDB
        'default_mdb'  : 'mdblist_api_key',
        'data_mdb'     : [],
    },

    #NIMBUS
    'nimbus': {
        'name'        : 'Nimbus',
        'plugin'      : 'skin.nimbus',
        'path'        : os.path.join(CONFIG.ADDONS, 'skin.nimbus'),
        'icon'        : os.path.join(CONFIG.ADDONS, 'skin.nimbus', 'icon.png'),
        'fanart'      : os.path.join(CONFIG.ADDONS, 'skin.nimbus', 'fanart.png'),
        'settings'    : os.path.join(CONFIG.ADDON_DATA, 'skin.nimbus', 'settings.xml'),
        #MDB
        'default_mdb'  : 'mdblist_api_key',
        'data_mdb'     : [],
    },

    #ACCOUNT MANAGER - Revoke is handled in router.py
    'acctmgr': {
        'name'        : 'Account Manager Lite',
        'plugin'      : 'script.module.acctmgr',
        'path'        : os.path.join(CONFIG.ADDONS, 'script.module.acctmgr'),
        'icon'        : os.path.join(CONFIG.ADDONS, 'script.module.acctmgr', 'icon.png'),
        'fanart'      : os.path.join(CONFIG.ADDONS, 'script.module.acctmgr', 'fanart.png'),
        'settings'    : os.path.join(CONFIG.ADDON_DATA, 'script.module.acctmgr', 'settings.xml'),
        #TK
        'default_tk'  : 'trakt.token',
        'data_tk'     : [],
        #MDB
        'default_mdb'  : 'mdblist.apikey',
        'data_mdb'     : [],
        #RD
        'default_rd'  : 'realdebrid.token',
        'data_rd'     : [],
        #PM
        'default_pm'  : 'premiumize.token',
        'data_pm'     : [],
        #AD
        'default_ad'  : 'alldebrid.token',
        'data_ad'     : [],
        #ED
        'default_ed'  : 'easydebrid.token',
        'data_ed'     : [],
        #TB
        'default_tb'  : 'torbox.token',
        'data_tb'     : [],
        #OC
        'default_oc'  : 'offcloud.token',
        'data_oc'     : [],
        #EN
        'default_en'  : 'easynews.password',
        'data_en'     : [],
    },
}
            
# Helpers
def get_addon_by_id(id):
    try:
        return xbmcaddon.Addon(id=id)
    except Exception:
        return None

def addon_installed(who):
    info = ADDONS.get(who)
    if not info:
        return False

    plugin_id = info.get('plugin')
    if not plugin_id:
        return False

    try:
        return get_addon_by_id(plugin_id) is not None
    except Exception:
        return False

def is_authorized_value(val):
    return bool(val) and str(val).strip().lower() not in ('', '0', 'none', 'null', 'empty_setting') # Added '0' due to Fen/Forks default setting being 0

def open_settings(who):  # Open add-on settings / skin settings
    info = ADDONS.get(who)
    if not info:
        return

    try:
        # Skins
        if who in ('fentastic', 'nimbus'):
            xbmc.executebuiltin('ActivateWindowAndFocus(skinsettings)')
            return

        # Standard add-ons
        addon = get_addon_by_id(info.get('plugin'))
        if addon:
            addon.openSettings()

    except Exception as e:
        xbmc.log(f"{amgr}: open_settings failed [{who}] - {e}", xbmc.LOGERROR)

def chk_sql_auth(db, key, return_value=False): # Check if a setting exists. If True, return the actual value
    if not key:
        return '' if return_value else False

    try:
        conn = sqlite3.connect(db, timeout=3)
        cur = conn.cursor()
        cur.execute(
            "SELECT setting_value FROM settings WHERE setting_id = ?", (key,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        value = row[0] if row else ''
        if return_value:
            return value
        return is_authorized_value(value)
    except Exception:
        return '' if return_value else False
      
def load_am_lite_tokens(): # Load NXTFlix Light tokens for all services
    path = xbmcvfs.translatePath('special://profile/addon_data/script.module.acctmgr/settings.xml')
    tokens = { 'tk': {}, 'rd': {}, 'mdb': {}, 'pm': {}, 'ad': {}, 'ed': {}, 'tb': {}, 'oc': {}, 'en': {} }

    if os.path.exists(path):
        try:
            tree = ElementTree.parse(path)
            root = tree.getroot()

            # Define which keys belong to which service
            service_keys = {
                'tk': ['trakt.token'],
                'rd': ['realdebrid.token'],
                'mdb': ['mdblist.apikey'],
                'pm': ['premiumize.token'],
                'ad': ['alldebrid.token'],
                'ed': ['easydebrid.token'],
                'tb': ['torbox.token'],
                'oc': ['offcloud.token'],
                'en': ['easynews.password'],
            }

            for setting in root.findall('setting'):
                key = setting.attrib.get('id')
                value = setting.text or ''
                for service, keys in service_keys.items():
                    if key in keys:
                        tokens[service][key] = value

        except Exception:
            xbmc.log('NXTFlix Light: Failed to read service tokens from settings.xml', xbmc.LOGERROR)

    return tokens

AM_LITE_TOKENS = load_am_lite_tokens()

# Service-specific token dictionaries
TK_TOKENS  = {}
RD_TOKENS  = {}
MDB_TOKENS = {}
PM_TOKENS  = {}
AD_TOKENS  = {}
ED_TOKENS  = {}
TB_TOKENS  = {}
OC_TOKENS  = {}
EN_TOKENS  = {}

SERVICE_MAP = {
    'tk':  TK_TOKENS,
    'rd':  RD_TOKENS,
    'mdb': MDB_TOKENS,
    'pm':  PM_TOKENS,
    'ad':  AD_TOKENS,
    'ed':  ED_TOKENS,
    'tb':  TB_TOKENS,
    'oc':  OC_TOKENS,
    'en':  EN_TOKENS,
}

# Populate tokens for each add-on and service using default keys
for addon_id, info in ADDONS.items():
    settings_path = info.get('settings')
    if not settings_path or not os.path.exists(settings_path):
        continue

    # Load key/value pairs from the add-on settings
    kv = {}
    if settings_path.endswith('.db'): # Add-ons setting Databases
        conn = sqlite3.connect(settings_path)
        cur = conn.cursor()
        cur.execute("SELECT setting_id, setting_value FROM settings")
        rows = cur.fetchall()
        conn.close()
        kv = {r[0]: r[1] for r in rows}

    elif settings_path.endswith('.xml'): # Add-ons using settings.xml
        tree = ElementTree.parse(settings_path)
        root = tree.getroot()
        kv = {s.attrib.get('id'): s.text or '' for s in root.findall('setting')}

    elif settings_path.endswith('.json'): # Add-ons using json
        with open(settings_path) as f:
            kv = json.load(f)

    # Only store default key per service
    for service, dict_ref in SERVICE_MAP.items():
        default_key = info.get(f'default_{service}')
        if default_key:
            val = kv.get(default_key, '')

            # Handle JSON blob add-ons
            if addon_id in ('tmdbhelper', 'trakt') and service == 'tk' and val:
                try:
                    val_unescaped = val.replace('&quot;', '"')
                    val = json.loads(val_unescaped).get('access_token','')
                except Exception:
                    val = ''

            dict_ref[addon_id] = {default_key: val}

# Check Authorization
def _addon_user_service(addon_id, service, token_dict):
    info = ADDONS.get(addon_id, {})
    default_key = info.get(f'default_{service}')
    if not default_key:
        return False

    acctmgr_info = ADDONS.get('acctmgr', {})
    am_key = acctmgr_info.get(f'default_{service}')
    if not am_key:
        return False

    addon_val = token_dict.get(addon_id, {}).get(default_key, '')
    am_val = AM_LITE_TOKENS.get(service, {}).get(am_key, '')

    return is_authorized_value(addon_val) and str(addon_val).strip() == str(am_val).strip()


# Return TRUE if add-on tokens match NXTFlix Light, else return FALSE
def addon_user_trakt(addon_id):
    return _addon_user_service(addon_id, 'tk', TK_TOKENS)

def addon_user_rd(addon_id):
    return _addon_user_service(addon_id, 'rd', RD_TOKENS)

def addon_user_mdb(addon_id):
    return _addon_user_service(addon_id, 'mdb', MDB_TOKENS)

def addon_user_pm(addon_id):
    return _addon_user_service(addon_id, 'pm', PM_TOKENS)

def addon_user_ad(addon_id):
    return _addon_user_service(addon_id, 'ad', AD_TOKENS)

def addon_user_ed(addon_id):
    return _addon_user_service(addon_id, 'ed', ED_TOKENS)

def addon_user_tb(addon_id):
    return _addon_user_service(addon_id, 'tb', TB_TOKENS)

def addon_user_oc(addon_id):
    return _addon_user_service(addon_id, 'oc', OC_TOKENS)

def addon_user_en(addon_id):
    return _addon_user_service(addon_id, 'en', EN_TOKENS)

# Revoke Handler
def addon_it(do, who='all', services=('tk','mdb','rd','pm','ad','ed','tb','oc','en'), force=True):
    #do: 'wipeaddon'
    #who: addon key or 'all'
    #Force: ignore token match and wipe all

    if who == 'all':
        targets = ORDER
    else:
        targets = (who,)

    for addon in targets:
        if addon not in ADDONS:
            continue

        # Skip uninstalled addons unless managed
        if addon not in ('nxtflixlt', 'gears', 'redlt', 'realx', 'fentastic', 'nimbus', 'acctmgr') and not addon_installed(addon):
            xbmc.log(f"NXTFlix Light: Skip revoke [{addon}] - addon not installed", xbmc.LOGINFO)
            continue

        for service in services:
            check_func = globals().get(f'addon_user_{service}')
            if force or (check_func and check_func(addon)):
                wipe_addons(do, addon, service)

# Revoke Add-ons
def wipe_addons(do, who, service):
    info = ADDONS.get(who)
    if not info:
        return

    settings = info.get('settings', '')
    data = info.get(f'data_{service}', [])

    # Skip the below list of add-ons
    if who in ('nxtflixlt', 'gears', 'redlt', 'fentastic', 'nimbus', 'acctmgr'):
        return

    if not settings:
        xbmc.log(f"{amgr}: wipe_addons skipped [{who}] - no settings path", xbmc.LOGINFO)
        return

    try:
        if settings.endswith('.json'):
            if os.path.exists(settings):
                with open(settings, 'w') as f:
                    f.write('{}')
            return

        if not os.path.exists(settings):
            xbmc.log(f"{amgr}: wipe_addons skipped [{who}] - settings not found", xbmc.LOGINFO)
            return

        if os.path.getsize(settings) == 0:
            xbmc.log(f"{amgr}: wipe_addons skipped [{who}] - settings file is empty", xbmc.LOGINFO)
            return

        tree = ElementTree.parse(settings)
        root = tree.getroot()

        removed = False
        for setting in list(root.findall('setting')):
            if setting.attrib.get('id') in data:
                root.remove(setting)
                removed = True

        if removed:
            tree.write(settings)

    except Exception as e:
        xbmc.log(f"{amgr}: wipe_addons failed [{who}/{service}] - {e}", xbmc.LOGERROR)

'''#FEN
'fen': {
    'name'        : 'Fen',
    'plugin'      : 'plugin.video.fen',
    'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.fen'),
    'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.fen/resources/media/', 'fen_icon.png'),
    'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.fen/resources/media/', 'fen_fanart.png'),
    'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.fen', 'settings.xml'),
    #TK
    'default_tk'  : 'trakt.token',
    'data_tk'     : ['trakt.refresh', 'trakt.expires', 'trakt.token', 'trakt.user', 'trakt.indicators_active', 'watched_indicators'],
    #RD
    'default_rd'  : 'rd.token',
    'data_rd'     : ['rd.client_id', 'rd.refresh', 'rd.secret', 'rd.token', 'rd.account_id', 'rd.enabled'],
    #PM
    'default_pm'  : 'pm.token',
    'data_pm'     : ['pm.token', 'pm.account_id', 'pm.enabled'],
    #AD
    'default_ad'  : 'ad.token',
    'data_ad'     : ['ad.token', 'ad.enabled', 'ad.account_id'],
    #EN
    'default_en'  : 'easynews_password',
    'data_en'     : ['easynews_password', 'easynews_user', 'provider.easynews'],
},

#SEREN
'seren': {
    'name'        : 'Seren',
    'plugin'      : 'plugin.video.seren',
    'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.seren'),
    'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.seren/resources/images', 'ico-seren-3.png'),
    'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.seren/resources/images', 'fanart-seren-3.png'),
    'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'settings.xml'),
    #TK
    'default_tk'  : 'trakt.auth',
    'data_tk'     : ['trakt.auth', 'trakt.refresh', 'trakt.username', 'trakt.expires'],
    #RD
    'default_rd'  : 'rd.auth',
    'data_rd'     : ['rd.auth', 'rd.client_id', 'rd.refresh', 'rd.secret', 'rd.username', 'realdebrid.enabled', 'realdebrid.premiumstatus'],
    #PM
    'default_pm'  : 'premiumize.token',
    'data_pm'     : ['premiumize.enabled', 'premiumize.username', 'premiumize.token', 'premiumize.premiumstatus'],
    #AD
    'default_ad'  : 'alldebrid.apikey',
    'data_ad'     : ['alldebrid.enabled', 'alldebrid.username', 'alldebrid.apikey', 'alldebrid.premiumstatus'],
},

#DRADIS
'dradis': {
    'name'        : 'Dradis',
    'plugin'      : 'plugin.video.dradis',
    'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.dradis'),
    'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.dradis', 'icon.png'),
    'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.dradis', 'fanart.jpg'),
    'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.dradis', 'settings.xml'),
    #TK
    'default_tk'  : 'trakt.token',
    'data_tk'     : ['trakt.token', 'trakt.username', 'trakt.expires', 'trakt.refresh', 'trakt.isauthed', 'trakt_user'], # Trakt Client/Secret NOT required here for revoke due to default API keys being stored in the settings.xml
    #MDB
    'default_mdb'  : 'mdblist.token',
    'data_mdb'     : ['mdblist.token', 'mdblist.username'],
    #RD
    'default_rd'  : 'realdebrid.token',
    'data_rd'     : ['realdebrid.username', 'realdebrid.token', 'realdebrid.client_id', 'realdebrid.secret', 'realdebrid.refresh', 'realdebrid.enable'],
    #PM
    'default_pm'  : 'premiumize.token',
    'data_pm'     : ['premiumize.username', 'premiumize.token', 'premiumize.enable'],
    #AD
    'default_ad'  : 'alldebrid.token',
    'data_ad'     : ['alldebrid.username', 'alldebrid.token', 'alldebrid.enable'],
    #TB
    'default_tb'  : 'torbox.token',
    'data_tb'     : ['torbox.token', 'torbox.username', 'torbox.enable', 'torbox.expires'],
    #OC
    'default_oc'  : 'offcloud.token',
    'data_oc'     : ['offcloud.token', 'offcloud.username', 'offcloud.enable'],
    #EN
    'default_en'  : 'easynews_password',
    'data_en'     : ['easynews_password', 'easynews_user', 'provider.easynews'],
},
    
#ORION
'orion': {
    'name'        : 'Orion',
    'plugin'      : 'plugin.video.orion',
    'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.orion'),
    'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.orion', 'icon.png'),
    'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.orion', 'fanart.jpg'),
    'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.orion', 'settings.xml'),
    #TK
    'default_tk'  : 'trakt_token',
    'data_tk'     : ['trakt_refresh', 'trakt_token', 'trakt_enabled'],
    #RD
    'default_rd'  : 'rd_token',
    'data_rd'     : ['rd_token', 'rd_refresh', 'rd_enabled'],
    #PM
    'default_pm'  : 'pm_token',
    'data_pm'     : ['pm_token', 'pm_enabled'],
    #AD
    'default_ad'  : 'ad_token',
    'data_ad'     : ['ad_token', 'ad_enabled'],
    #TB
    'default_tb'  : 'tb_token',
    'data_tb'     : ['tb_token', 'tb_enabled'],
},

#GENESIS
'genesis': {
    'name'        : 'Genesis',
    'plugin'      : 'plugin.video.genesis',
    'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.genesis'),
    'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.genesis', 'icon.png'),
    'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.genesis', 'fanart.jpg'),
    'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.genesis', 'settings.xml'),
    #TK
    'default_tk'  : 'trakt.token',
    'data_tk'     : ['trakt.refresh', 'trakt.token', 'trakt.user'],
    #RD
    'default_rd'  : 'realdebrid_token',
    'data_rd'     : ['realdebrid_token', 'realdebrid_refresh', 'realdebrid_tokenExpireIn'],
    #PM
    'default_pm'  : 'premiumize_token',
    'data_pm'     : ['premiumize_token', 'premiumize_user'],
    #AD
    'default_ad'  : 'alldebrid_api_key',
    'data_ad'     : ['alldebrid_api_key', 'alldebrid_username'],
    #TB
    'default_tb'  : 'torbox_api_key',
    'data_tb'     : ['torbox_api_key'],
},

#SYNCHER
'syncher': {
    'name'        : 'Syncher',
    'plugin'      : 'plugin.video.syncher',
    'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.syncher'),
    'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.syncher', 'icon.png'),
    'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.syncher', 'fanart.jpg'),
    'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.syncher', 'settings.xml'),
    #TK
    'default_tk'  : 'trakt.token',
    'data_tk'     : ['trakt.refresh', 'trakt.token', 'trakt.user'],
    #RD
    'default_rd'  : 'rd.token',
    'data_rd'     : ['rd.token', 'rd.refresh', 'rd.enabled'],
    #PM
    'default_pm'  : 'pm.token',
    'data_pm'     : ['pm.token', 'pm.enabled'],
    #AD
    'default_ad'  : 'ad.apikey',
    'data_ad'     : ['ad.apikey', 'ad.enabled'],
    #TB
    'default_tb'  : 'tb.apikey',
    'data_tb'     : ['tb.apikey', 'tb.enabled'],
},

#TRAKT PLAYER
'tkplay': {
    'name'        : 'Trakt Player',
    'plugin'      : 'plugin.video.trakt_player',
    'path'        : os.path.join(CONFIG.ADDONS, 'plugin.video.trakt_player'),
    'icon'        : os.path.join(CONFIG.ADDONS, 'plugin.video.trakt_player', 'icon.png'),
    'fanart'      : os.path.join(CONFIG.ADDONS, 'plugin.video.trakt_player', 'fanart.jpg'),
    'settings'    : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.trakt_player', 'settings.xml'),
    #TK
    'default_tk'  : 'trakt_access_token',
    'data_tk'     : ['trakt_refresh_token', 'trakt_access_token', 'trakt_auth_done'],
    #RD
    'default_rd'  : 'rd_access_token',
    'data_rd'     : ['rd_access_token', 'rd_refresh_token', 'rd_auth_done'],
    #PM
    'default_pm'  : 'pm_access_token',
    'data_pm'     : ['pm_access_token', 'pm_auth_done'],
    #AD
    'default_ad'  : 'ad_api_key',
    'data_ad'     : ['ad_api_key', 'ad_auth_done'],
    #TB
    'default_tb'  : 'tb_api_key',
    'data_tb'     : ['tb_api_key', 'tb_auth_done'],
},
'''
