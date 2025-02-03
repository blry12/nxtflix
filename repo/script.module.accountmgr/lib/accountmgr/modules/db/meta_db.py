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

########################## NXTFlix Light OMDb Metadata #########################
def connect_omdb_nxtflixlt(conn, setting):
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
        xbmc.log('%s: Meta_db OMDb Auth Failed!' % var.amgr, xbmc.LOGINFO)
        pass

########################## NXTFlix Light TMDb Metadata #########################
def connect_tmdb_nxtflixlt(conn, setting):
    try:
        # Update settings database
        tmdb_api = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        
        cur = conn.cursor()
        cur.execute(tmdb_api, setting)
        conn.commit()
        cur.close()
    except:
        xbmc.log('%s: Meta_db TMDb Auth Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
'''########################## Afnxtflixity Metadata #########################
def connect_meta_afnxtflix(conn, setting):
    try:
        # Update settings database
        omdb_api = '''''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?''''''

        cur = conn.cursor()
        cur.execute(omdb_api, setting)
        conn.commit()
        cur.close()
    except:
        xbmc.log('%s: Meta_db Auth Failed!' % var.amgr, xbmc.LOGINFO)
        pass'''

    
#################### Auth NXTFlix Light OMDb Metadata ###################
def auth_nxtflixlt_omdb():
    try:
        # Create database connection
        conn = create_conn(var.nxtflixlt_settings_db)
        with conn:
            connect_omdb_nxtflixlt(conn, (your_omdb_api, 'omdb_api'))
    except:
        xbmc.log('%s: Meta_db OMDb NXTFlix Light Failed!' % var.amgr, xbmc.LOGINFO)
        pass

#################### Auth NXTFlix Light TMDb Metadata ###################
def auth_nxtflixlt_tmdb():
    try:
        # Create database connection
        conn = create_conn(var.nxtflixlt_settings_db)
        with conn:
            connect_tmdb_nxtflixlt(conn, (your_tmdb_api, 'tmdb_api'))
    except:
        xbmc.log('%s: Meta_db TMDb NXTFlix Light Failed!' % var.amgr, xbmc.LOGINFO)
        pass


'''#################### Auth afnxtflixityt Metadata ###################
    def auth_afnxtflix_meta():
    try:
        # Create database connection
        conn = create_conn(var.afnxtflix_settings_db)
        with conn:
            connect_meta_afnxtflix(conn, (your_omdb_api, 'omdb_api'))
    except:
        xbmc.log('%s: Meta_db afnxtflixity Failed!' % var.amgr, xbmc.LOGINFO)
        pass'''
