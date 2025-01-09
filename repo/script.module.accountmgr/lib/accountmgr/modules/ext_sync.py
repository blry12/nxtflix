import xbmc, xbmcaddon
import xbmcvfs
import os

from pathlib import Path
from accountmgr.modules import control
from accountmgr.modules import ext_db
from libs.common import var

char_remov = ["'", ",", ")","("]

class Auth:
        def ext_auth(self):

        #nxtflix
                try:
                        if xbmcvfs.exists(var.chk_nxtflix) and xbmcvfs.exists(var.chkset_nxtflix) and xbmcvfs.exists(var.chk_coco): #Check that the addon and external provider are installed
                                addon = xbmcaddon.Addon("plugin.video.nxtflix")
                                chk_auth = addon.getSetting("external_scraper.module")
                                if chk_auth == 'script.module.cocoscrapers':
                                        pass
                                else:
                                        addon.setSetting("provider.external", 'true')
                                        addon.setSetting("external_scraper.name", 'CocoScrapers Module')
                                        addon.setSetting("external_scraper.module", 'script.module.cocoscrapers')
                except:
                        xbmc.log('%s: nxtflix Ext Provider Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
 
        #NXTFlix Light
                try:
                        if xbmcvfs.exists(var.chk_nxtflixlt) and xbmcvfs.exists(var.chkset_nxtflixlt) and xbmcvfs.exists(var.chk_coco): #Check that the addon and external provider are installed
                            
                            #Create database connection
                            from accountmgr.modules import ext_db
                            conn = ext_db.create_conn(var.nxtflixlt_settings_db)
                            
                            #Get add-on settings to compare
                            with conn:
                                cursor = conn.cursor()
                                cursor.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('external_scraper.module',))
                                auth_ext = cursor.fetchone()
                                chk_auth_nxtflixlt = str(auth_ext)
                                cursor.close()
                                
                                #Clean up database results
                                for char in char_remov:
                                    chk_auth_nxtflixlt = chk_auth_nxtflixlt.replace(char, "")
                                    
                                if not chk_auth_nxtflixlt == 'script.module.cocoscrapers': #If external provider is set, authorization is skipped
                                    
                                    #Write settings to database
                                    from accountmgr.modules import ext_db
                                    ext_db.auth_nxtflixlt_ext()
                                    var.remake_settings()
                except:
                        xbmc.log('%s: NXTFlix Light Ext Provider Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Umbrella
                try:
                        if xbmcvfs.exists(var.chk_umb) and xbmcvfs.exists(var.chkset_umb) and xbmcvfs.exists(var.chk_coco):
                                addon = xbmcaddon.Addon("plugin.video.umbrella")
                                chk_auth = addon.getSetting("external_provider.module")
                                if chk_auth == 'script.module.cocoscrapers':
                                        pass
                                else:
                                        addon.setSetting("provider.external.enabled", 'true')
                                        addon.setSetting("external_provider.name", 'cocoscrapers')
                                        addon.setSetting("external_provider.module", 'script.module.cocoscrapers')
                except:
                        xbmc.log('%s: Umbrella Ext Provider Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Infinity
                try:
                        if xbmcvfs.exists(var.chk_infinity) and xbmcvfs.exists(var.chkset_infinity) and xbmcvfs.exists(var.chk_coco):
                                addon = xbmcaddon.Addon("plugin.video.infinity")
                                chk_auth = addon.getSetting("external_provider.module")
                                if chk_auth == 'script.module.cocoscrapers':
                                        pass
                                else:
                                        addon.setSetting("provider.external.enabled", 'true')
                                        addon.setSetting("external_provider.name", 'cocoscrapers')
                                        addon.setSetting("external_provider.module", 'script.module.cocoscrapers')
                except:
                        xbmc.log('%s: Infinity Ext Provider Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
