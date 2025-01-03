import xbmc, xbmcaddon
import sqlite3
import xbmcvfs
import os
from libs.common import var
from sqlite3 import Error

#Account Manager Metadata
accountmgr = xbmcaddon.Addon("script.module.accountmgr")
your_omdb_api = accountmgr.getSetting("omdb.api.key")
your_tmdb_api = accountmgr.getSetting("tmdb.api.key")

###################### Connect to Database ######################
def create_conn(db_file):
    try:
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

        return conn
    except:
        xbmc.log('%s: Meta_db Connect Failed!' % var.amgr, xbmc.LOGINFO)
        pass

########################## NXTFlix Light Metadata #########################
def connect_meta_nxtflixlt(conn, setting):
    try:
        # Update settings database
        omdb_api = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''

        tmdb_api = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        
        cur = conn.cursor()
        cur.execute(omdb_api, setting)
        cur.execute(tmdb_api, setting)
        conn.commit()
        cur.close()
    except:
        xbmc.log('%s: Meta_db Auth Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
########################## Affenity Metadata #########################
def connect_meta_affen(conn, setting):
    try:
        # Update settings database
        omdb_api = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''

        cur = conn.cursor()
        cur.execute(omdb_api, setting)
        conn.commit()
        cur.close()
    except:
        xbmc.log('%s: Meta_db Auth Failed!' % var.amgr, xbmc.LOGINFO)
        pass

    
#################### Auth NXTFlix Light Metadata ###################
def auth_nxtflixlt_meta():
    try:
        # Create database connection
        conn = create_conn(var.nxtflixlt_settings_db)
        with conn:
            connect_meta_nxtflixlt(conn, (your_omdb_api, 'omdb_api'))
            connect_meta_nxtflixlt(conn, (your_tmdb_api, 'tmdb_api'))
    except:
        xbmc.log('%s: Meta_db NXTFlix Light Failed!' % var.amgr, xbmc.LOGINFO)
        pass



#################### Auth afFENityt Metadata ###################
def auth_affen_meta():
    try:
        # Create database connection
        conn = create_conn(var.affen_settings_db)
        with conn:
            connect_meta_affen(conn, (your_omdb_api, 'omdb_api'))
    except:
        xbmc.log('%s: Meta_db afFENity Failed!' % var.amgr, xbmc.LOGINFO)
        pass
