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
            addon = xbmcvfs.translatePath('special://home/addons/plugin.video.nxtflix/')
            file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.nxtflix/settings.xml')

            if xbmcvfs.exists(addon) and xbmcvfs.exists(file):

                res = 'SD, 720p, 1080p, 4K'
                uhd = '4K'
                addon = xbmcaddon.Addon("plugin.video.nxtflix")
                addon.setSetting("results_quality_movie", res)
                addon.setSetting("results_quality_episode", res)
                addon.setSetting("autoplay_quality_movie", res)
                addon.setSetting("autoplay_quality_episode", res)
                addon.setSetting("filter_hevc.max_quality", uhd)
                addon.setSetting("filter_hevc.max_autoplay_quality", uhd) 
                ftr = 'ATMOS, TRUEHD, DTS-HD MA, DTS-HD, 8CH, 7CH'
                addon = xbmcaddon.Addon("plugin.video.nxtflix")
                addon.setSetting("filter_audio", ftr)
                ftr = '1'
                addon = xbmcaddon.Addon("plugin.video.nxtflix")
                addon.setSetting("filter_dv", ftr) 
                fsen= '0'
                addon.setSetting("results.filter_size_method", fsen) 
                hdr= '0'
                addon.setSetting("filter_hdr", hdr)                 
                
        except:
                pass               
            
        xbmcgui.Dialog().notification('MaxQL', '4K Edition Enabled!', addon_icon, 3000)
