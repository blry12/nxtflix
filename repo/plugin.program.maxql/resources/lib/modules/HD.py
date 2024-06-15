import xbmc, xbmcaddon, xbmcgui
import xbmcvfs
import os

addon_icon = 'special://home/addons/plugin.program.maxql/icon.png'

class hd:
    def hd_config():
        
        try:
            addon = xbmcvfs.translatePath('special://home/addons/plugin.video.seren/')
            file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.seren/settings.xml')
            if xbmcvfs.exists(addon) and xbmcvfs.exists(file):
                
                res = '1'
                addon = xbmcaddon.Addon("plugin.video.seren")
                addon.setSetting("general.maxResolution", res)
        except:
                pass
                
        try:
            addon = xbmcvfs.translatePath('special://home/addons/plugin.video.afm/')
            file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.afm/settings.xml')

            if xbmcvfs.exists(addon) and xbmcvfs.exists(file):

                res = 'SD, 720p, 1080p'
                hd = '1080p' 
                addon = xbmcaddon.Addon("plugin.video.afm")
                addon.setSetting("results_quality_movie", res)
                addon.setSetting("results_quality_episode", res)
                addon.setSetting("autoplay_quality_movie", res)
                addon.setSetting("autoplay_quality_episode", res)
                addon.setSetting("filter_hevc.max_quality", hd)
                addon.setSetting("filter_hevc.max_autoplay_quality", hd)   
                ftr = 'ATMOS, TRUEHD, DTS-HD MA, DTS-HD, 8CH, 7CH'
                addon = xbmcaddon.Addon("plugin.video.afm")
                addon.setSetting("filter_audio", ftr)
                ftr = '1'
                addon = xbmcaddon.Addon("plugin.video.afm")
                addon.setSetting("filter_dv", ftr)           
        except:
                pass                
            
        xbmcgui.Dialog().notification('MaxQL', 'Firestick Edition Enabled!', addon_icon, 3000)
