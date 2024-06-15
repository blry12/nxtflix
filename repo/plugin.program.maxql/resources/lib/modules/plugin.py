import xbmc
import xbmcplugin
import xbmcaddon
import sys
import os
from .params import Params
from .menu import main_menu

handle = int(sys.argv[1])

def router(paramstring):

    p = Params(paramstring)
    xbmc.log(str(p.get_params()),xbmc.LOGDEBUG)

    mode = p.get_mode()
    
    xbmcplugin.setContent(handle, 'files')

    if mode is None:
        main_menu()
        
    elif mode == 1:
        from resources.lib.modules import HD
        HD.hd.hd_config()

    elif mode == 2:
        from resources.lib.modules import UHD
        UHD.full_hd.fullhd_config()
        
    elif mode == 3:
        from resources.lib.modules import enable_dv
        enable_dv.dv.dv_enable()

    elif mode == 4:
        from resources.lib.modules import disable_dv
        disable_dv.dv.dv_disable()
        
    elif mode == 5:
        from resources.lib.modules import disable_at
        disable_at.at.at_disable()

    elif mode == 6:
        from resources.lib.modules import enable_3d
        enable_3d.three_d.threed_enable()

    elif mode == 7:
        from resources.lib.modules import disable_3d
        disable_3d.three_d.threed_disable()

    elif mode == 8:
        from resources.lib.modules import autoplay_enable
        autoplay_enable.ap_enable.enable()

    elif mode == 9:
        from resources.lib.modules import autoplay_disable
        autoplay_disable.ap_disable.disable()        

    xbmcplugin.endOfDirectory(handle)
