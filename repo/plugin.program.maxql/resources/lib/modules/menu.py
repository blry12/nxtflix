import sys
import json
import xbmc
import xbmcplugin
from .utils import add_dir

addon_fanart = 'special://home/addons/plugin.program.maxql/icons/fanart.jpg'
HD_icon = 'special://home/addons/plugin.program.maxql/icons/HD.png'
UHD1_icon = 'special://home/addons/plugin.program.maxql/icons/UHD1.png'
DVA_icon = 'special://home/addons/plugin.program.maxql/icons/DVA.png'
dvoff_icon = 'special://home/addons/plugin.program.maxql/icons/dvoff.png'
atoff_icon = 'special://home/addons/plugin.program.maxql/icons/atoff.png'
threedon_icon = 'special://home/addons/plugin.program.maxql/icons/threedon.png'
threedoff_icon = 'special://home/addons/plugin.program.maxql/icons/threedoff.png'
auon_icon = 'special://home/addons/plugin.program.maxql/icons/auon.png'
auoff_icon = 'special://home/addons/plugin.program.maxql/icons/auoff.png'

handle = int(sys.argv[1])

def main_menu():
    xbmcplugin.setPluginCategory(handle, 'Main Menu')

    add_dir('1080P Edition - Best for Firestick/GoogleTV cast 1080p Devices','',1,HD_icon,addon_fanart,isFolder=True)
    
    add_dir('4K Edition - Best for GoogleTV Cast 4K/Firestick 4K/4K Devices','',2,UHD1_icon,addon_fanart,isFolder=True)

    add_dir('Dolby Vision/Atmos Edition - Best for Shield Pro/Fire Cube/High-end Devices','',3,DVA_icon,addon_fanart,isFolder=True)
    
    add_dir('Disable Dolby Vision Only','',4,dvoff_icon,addon_fanart,isFolder=True)
    
    add_dir('Disable Dolby Atmos Only','',5,atoff_icon,addon_fanart,isFolder=True)   

    add_dir('Enable 3D Results','',6,threedon_icon,addon_fanart,isFolder=True)

    add_dir('Disable 3D Results','',7,threedoff_icon,addon_fanart,isFolder=True)

    add_dir('Enable Auto-Play','',8,auon_icon,addon_fanart,isFolder=True)

    add_dir('Disable Auto-Play','',9,auoff_icon,addon_fanart,isFolder=True)    


