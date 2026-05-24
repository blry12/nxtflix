# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcaddon, xbmcvfs
import os
import json
from acctmgr.modules import var
from acctmgr.modules import control
from acctmgr.modules import log_utils

# Variables
joinPath = os.path.join
dialog = xbmcgui.Dialog()
trakt_icon = joinPath(control.iconsPath(), 'trakt.png')

class tk_list():
    def create_list(self):
        locked = [] # List of previously added items
        if xbmcvfs.exists(var.tk_sync_list):
            try:
                with open(var.tk_sync_list, 'r') as f:
                    locked = json.load(f).get('addon_list', [])
            except Exception as e:
                log_utils.error(f"Failed to load Trakt sync list: {e}")
                locked = []

        menu = [] # List of supported add-ons
        def add_if(path, name):
            if xbmcvfs.exists(path) and name not in locked: # List only installed and not previously selected add-ons 
                menu.append(name)

        # NXTFlix Light & Forks
        add_if(var.chk_nxtflixlt,       'NXTFlix Light')
        add_if(var.chk_gears,       'The Gears')
        add_if(var.chk_red,         'Red Light')
        
        # Uniques
        add_if(var.chk_umb,         'Umbrella')
        #add_if(var.chk_seren,       'Seren')
        
        # Fen & Forks
        #add_if(var.chk_fen,         'Fen')
        add_if(var.chk_pov,         'POV')
        add_if(var.chk_coal,        'The Coalition')
        
        # Dradis & Forks
        #add_if(var.chk_dradis,      'Dradis')
        add_if(var.chk_genocide,    'Genocide')
        
        # Shadow & Forks
        add_if(var.chk_shadow,      'Shadow')
        add_if(var.chk_ghost,       'Ghost')
        add_if(var.chk_chains,      'The Chains')
        
        # Homelander & Forks
        add_if(var.chk_home,        'Homelander')
        add_if(var.chk_night,       'Nightwing')
        add_if(var.chk_absol,       'Jokers Absolution')
        #Scrubs V2 & Forks
        add_if(var.chk_scrubs,      'Scrubs V2')
        add_if(var.chk_redg,        'Gratis Red')
        # Others
        add_if(var.chk_crew,        'The Crew')
        add_if(var.chk_salts,       'SALTS')
        #add_if(var.chk_orion,       'Orion')
        #add_if(var.chk_gen,         'Genesis')
        #add_if(var.chk_sync,        'Syncher')
        add_if(var.chk_tmdbh,       'TMDb Helper')
        #add_if(var.chk_tkplay,      'Trakt Player')
        add_if(var.chk_trakt,       'Trakt Addon')

        if not menu:
            control.notification('NXTFlix Light', 'No supported add-ons found!', icon=trakt_icon)
            return

        try:
            dialog_select = dialog.multiselect('NXTFlix Light - Choose add-ons to sync with Trakt', menu) # Select add-ons
        except Exception as e:
            log_utils.error(f"Error displaying selection dialog: {e}")
            return

        if dialog_select is None:
            control.notification('NXTFlix Light', 'No Changes Made!', icon=trakt_icon)
            control.openSettings()
            return False

        # Build final list
        addon_list = locked[:] # keep locked items
        for i in dialog_select:
            addon_list.append(menu[i])

        if not xbmcvfs.exists(var.acctmgr_datapath):
            xbmcvfs.mkdirs(var.acctmgr_datapath)

        try:
            if not control.setting('trakt.token'):
                if not control.yesnoDialog('Your list has been updated![CR]Would you like to authorize Trakt and sync with supported add-ons?'):
                    control.notification('NXTFlix Light', 'Changes discarded.', icon=trakt_icon)
                    return False
            else:
                if not control.yesnoDialog('Your list has been updated![CR]Would you like to sync Trakt with supported add-ons?'):
                    control.notification('NXTFlix Light', 'Changes discarded.', icon=trakt_icon)
                    return False
                
        except Exception as e:
            log_utils.error(f"Error displaying yes/no dialog: {e}")
            return False

        try:
            with open(var.tk_sync_list, 'w') as synclist: # Save list
                json.dump({'addon_list': addon_list}, synclist, indent=4)
        except Exception as e:
            log_utils.error(f"Failed to save Trakt sync list: {e}")
            return False

        control.notification('NXTFlix Light', 'Trakt Sync List Saved!', icon=trakt_icon)
        return True
