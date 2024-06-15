import xbmc, xbmcaddon, xbmcgui
import xbmcvfs
import os

addon_icon = 'special://home/addons/plugin.program.maxql/icon.png'

class full_hd:
    def fullhd_config():
        try:
            addon = xbmcvfs.translatePath('special://home/addons/plugin.video.seren/')
            file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.seren/settings.xml')

            if xbmcvfs.exists(addon) and xbmcvfs.exists(file):

                res = '0'
                addon = xbmcaddon.Addon("plugin.video.seren")
                addon.setSetting("general.maxResolution", res)
        except:
                pass
            
        try:
            addon = xbmcvfs.translatePath('special://home/addons/plugin.video.fen/')
            file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.fen/settings.xml')

            if xbmcvfs.exists(addon) and xbmcvfs.exists(file):

                res = 'SD, 720p, 1080p, 4K'
                addon = xbmcaddon.Addon("plugin.video.fen")
                addon.setSetting("results_quality_movie", res)
                addon.setSetting("results_quality_episode", res)
                addon.setSetting("autoplay_quality_movie", res)
                addon.setSetting("autoplay_quality_episode", res)
        except:
                pass
                
        try:
            addon = xbmcvfs.translatePath('special://home/addons/plugin.video.NXTFlix/')
            file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.NXTFlix/settings.xml')

            if xbmcvfs.exists(addon) and xbmcvfs.exists(file):

                res = 'SD, 720p, 1080p, 4K'
                uhd = '4K'
                addon = xbmcaddon.Addon("plugin.video.NXTFlix")
                addon.setSetting("results_quality_movie", res)
                addon.setSetting("results_quality_episode", res)
                addon.setSetting("autoplay_quality_movie", res)
                addon.setSetting("autoplay_quality_episode", res)
                addon.setSetting("filter_hevc.max_quality", uhd)
                addon.setSetting("filter_hevc.max_autoplay_quality", uhd)  
                ftr = ''
                addon = xbmcaddon.Addon("plugin.video.NXTFlix")
                addon.setSetting("filter_audio", ftr)
                vd = '0'
                addon = xbmcaddon.Addon("plugin.video.NXTFlix")
                addon.setSetting("filter_dv", vd)
              
        except:
                pass               
            
        xbmcgui.Dialog().notification('MaxQL', 'Shield Pro with Dolby Vision Edition Enabled!', addon_icon, 3000)
