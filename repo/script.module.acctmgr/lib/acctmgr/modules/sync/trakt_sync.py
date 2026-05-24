# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcaddon, xbmcvfs
import os
import time
import json

from acctmgr.modules import var
from acctmgr.modules import control
from acctmgr.modules import log_utils
from acctmgr.modules.db import chk_auth_db
from acctmgr.modules.db import trakt_db

# Variables
joinPath = os.path.join
exists = xbmcvfs.exists
translatePath = xbmcvfs.translatePath
addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon = xbmcaddon.Addon(addon_id)
addoninfo = addon.getAddonInfo

# Sync Helpers
def refresh_sync(mode, chk_auth, token):
    if mode == "auth":
        return True
    return chk_auth != str(token)

def authorize(mode):
    return mode == "auth"

class Auth:
    def am_trakt(self):
        acctmgr = xbmcaddon.Addon("script.module.acctmgr")
        your_token = acctmgr.getSetting("trakt.token")
        your_username = acctmgr.getSetting("trakt.username")
        your_refresh = '1'
        your_expires = acctmgr.getSetting("trakt.expires")
        try:
            your_expires_int = int(float(your_expires or 0))
        except Exception as e:
            log_utils.error(f"Error converting trakt.expires: {e}")
            your_expires_int = 0
        return your_token, your_username, your_refresh, str(your_expires_int)

    def trakt_auth(self, mode="refresh"):
        your_token, your_username, your_refresh, your_expires = self.am_trakt()
        master_token = your_token

        if not exists(var.tk_sync_list):
            return

        try:
            with open(var.tk_sync_list, "r") as synclist:
                current = json.load(synclist)["addon_list"]
        except Exception as e:
            log_utils.error(f"Error reading sync list: {e}")
            return

        # ===================== Copy Addon Data (settings.xml) =====================
        addons = (
            ("Shadow",        var.chk_shadow, var.shadow_ud,  var.chkset_shadow,  var.shadow),
            ("Ghost",         var.chk_ghost,  var.ghost_ud,   var.chkset_ghost,   var.ghost),
            ("The Chains",    var.chk_chains, var.chains_ud,  var.chkset_chains,  var.chains),
            ("Homelander",    var.chk_home,   var.home_ud,    var.chkset_home,    var.home),
            ("Nightwing",     var.chk_night,  var.night_ud,   var.chkset_night,   var.night),
            ("Absolution",    var.chk_absol,  var.absol_ud,   var.chkset_absol,   var.absol),
            ("The Crew",      var.chk_crew,   var.crew_ud,    var.chkset_crew,    var.crew),
            ("SALTS",         var.chk_salts,  var.salts_ud,   var.chkset_salts,   var.salts),
            #("Orion",        var.chk_orion,  var.orion_ud,   var.chkset_orion,   var.orion),
            #("Genesis",      var.chk_gen,    var.gen_ud,     var.chkset_gen,     var.gen),
            #("Syncher",      var.chk_sync,   var.sync_ud,    var.chkset_sync,    var.sync),
            ("Scrubs V2",     var.chk_scrubs, var.scrubs_ud,  var.chkset_scrubs,  var.scrubs),
            ("Gratis Red",    var.chk_redg,   var.redg_ud,    var.chkset_redg,    var.redg),
            ("TMDb Helper",   var.chk_tmdbh,  var.tmdbh_ud,   var.chkset_tmdbh,   var.tmdbh),
            #("Trakt Player", var.chk_tkplay, var.tkplay_ud,  var.chkset_tkplay,  var.tkplay),
            ("Trakt",         var.chk_trakt,  var.trakt_ud,   var.chkset_trakt,   var.trakt),
        )

        for name, chk_addon, ud_path, chk_setting, base_path in addons:
            try:
                control.copy_addon_settings(name, chk_addon, ud_path, chk_setting, base_path)
            except Exception as e:
                log_utils.error(f"Error copying settings for {name}: {e}")
                
        # ========================= NXTFlix Light / The Gears / Red Light =========================
        # ========================== API Keys applied to settings.db ==========================

        addons = (
            ("NXTFlix Light", "NXTFlix Light", var.chk_nxtflixlt, var.chkset_nxtflixlt, var.nxtflixlt_settings_db, control.remake_nxtflixlt_settings, var.path_nxtflixlt_service, control.remake_nxtflixlt_trakt_cache),
            ("The Gears", "The Gears", var.chk_gears, var.chkset_gears, var.gears_settings_db, control.remake_gears_settings, var.path_gears_service, control.remake_gears_trakt_cache),
            ("Red Light", "Red Light", var.chk_red, var.chkset_red, var.red_settings_db, control.remake_red_settings, var.path_red_service, control.remake_redlt_trakt_cache),
        )

        for current_name, addon_name, chk_path, chkset_path, settings_db, remake_settings_func, service_path, remake_cache_func in addons:
            try:
                if current_name in current and exists(chk_path):

                    if not exists(chkset_path):
                        remake_settings_func()
                        xbmc.sleep(500)

                    if exists(chkset_path):
                        chk_auth = chk_auth_db.chk_auth(settings_db, "trakt.token")

                        if refresh_sync(mode, chk_auth, master_token):
                            trakt_db.auth(settings_db)
                            remake_settings_func()

                            patched, msg = control.startup_patch(service_path, addon_name=addon_name)
                            if not patched:
                                log_utils.log(f"{addon_name} startup patch failed, msg={msg}", level=log_utils.LOGERROR)

                            if authorize(mode):
                                xbmc.sleep(300)
                                remake_cache_func()

            except Exception as e:
                log_utils.error(f"{current_name} Trakt Failed: {e}")

        # ========================= Umbrella =========================
        try:
            if "Umbrella" in current and exists(var.chk_umb) and exists(var.chkset_umb):
                addon = xbmcaddon.Addon("plugin.video.umbrella")
                chk_auth = addon.getSetting("trakt.user.token")
                if refresh_sync(mode, chk_auth, master_token):
                    with open(var.path_umb, "r") as f:
                        data = f.read()

                    patched_keys = False
                    if var.umb_client in data or var.umb_secret in data:
                        data = data.replace(var.umb_client, var.client_am).replace(var.umb_secret, var.secret_am)
                        with open(var.path_umb, "w") as f:
                            f.write(data)
                        patched_keys = True
                    elif var.client_am in data and var.secret_am in data:
                        patched_keys = True

                    if not patched_keys:
                        log_utils.log("Umbrella Trakt keys NOT patched")

                    patched, msg = control.startup_patch(var.path_umb_service, addon_name="Umbrella")
                    if not patched:
                        log_utils.log(f"Umbrella startup patch failed, msg={msg}", level=log_utils.LOGERROR)

                    for k, v in {
                        "trakt.user.name": your_username,
                        "trakt.user.token": your_token,
                        "trakt.refreshtoken": your_refresh,
                        "trakt.token.expires": your_expires,
                        "trakt.authed.clientid": var.client_am,
                        "indicators": "Trakt",
                        "trakt.isauthed": "true",
                        "trakt.scrobble": "true",
                        "indicators.alt": "1",
                        "scrobble.source": "1",
                        "resume.source": "1",
                    }.items():
                        addon.setSetting(k, v)
        except Exception as e:
            log_utils.error(f"Umbrella Trakt Failed: {e}")

        '''# ========================= Seren =========================
        try:
            if "Seren" in current and exists(var.chk_seren) and exists(var.chkset_seren):
                addon = xbmcaddon.Addon("plugin.video.seren")
                chk_auth = addon.getSetting("trakt.auth")
                if refresh_sync(mode, chk_auth, master_token):
                    with open(var.path_seren, "r") as f:
                        data = f.read()

                    patched_keys = False
                    if var.seren_client in data or var.seren_secret in data:
                        data = data.replace(var.seren_client, var.client_am).replace(var.seren_secret, var.secret_am)
                        with open(var.path_seren, "w") as f:
                            f.write(data)
                        patched_keys = True
                    elif var.client_am in data and var.secret_am in data:
                        patched_keys = True

                    if not patched_keys:
                        log_utils.log("Seren Trakt keys NOT patched")

                    patched, msg = control.startup_patch(var.path_seren_service)
                    if not patched:
                        log_utils.log(f"Seren startup patch failed, msg={msg}", level=log_utils.LOGERROR)

                    your_expires_str = str(int(float(your_expires)))
                    for k, v in {
                        "trakt.auth": your_token,
                        "trakt.username": your_username,
                        "trakt.refresh": your_refresh,
                        "trakt.expires": your_expires_str,
                    }.items():
                        addon.setSetting(k, v)
        except Exception as e:
            log_utils.error(f"Seren Trakt Failed: {e}")

        # ========================= Fen =========================
        try:
            if "Fen" in current and exists(var.chk_fen) and exists(var.chkset_fen):
                addon = xbmcaddon.Addon("plugin.video.fen")
                chk_auth = addon.getSetting("trakt.token")
                if refresh_sync(mode, chk_auth, master_token):
                    with open(var.path_fen, "r") as f:
                        data = f.read()

                    patched_keys = False
                    if var.fen_client in data or var.fen_secret in data:
                        data = data.replace(var.fen_client, var.client_am).replace(var.fen_secret, var.secret_am)
                        with open(var.path_fen, "w") as f:
                            f.write(data)
                        patched_keys = True
                    elif var.client_am in data and var.secret_am in data:
                        patched_keys = True

                    if not patched_keys:
                        log_utils.log("Fen Trakt keys NOT patched")

                    patched, msg = control.startup_patch(var.path_fen_service)
                    if not patched:
                        log_utils.log(f"Fen startup patch failed, msg={msg}", level=log_utils.LOGERROR)

                    for k, v in {
                        "trakt.token": your_token,
                        "trakt.user": your_username,
                        "trakt.refresh": your_refresh,
                        "trakt.expires": your_expires,
                        "trakt.indicators_active": "true",
                        "watched_indicators": "1",
                    }.items():
                        addon.setSetting(k, v)

                    if authorize(mode):
                        control.remake_fen_trakt_cache()
        except Exception as e:
            log_utils.error(f"Fen Trakt Failed: {e}")'''

        # ========================== POV ==========================
        # ============ API Keys applied to settings.xml ===========
        try:
            if "POV" in current and exists(var.chk_pov) and exists(var.chkset_pov):
                addon = xbmcaddon.Addon("plugin.video.pov")
                chk_auth = addon.getSetting("trakt.token")
                if refresh_sync(mode, chk_auth, master_token):
                    patched, msg = control.startup_patch(var.path_pov_service)
                    if not patched:
                        log_utils.log(f"POV startup patch failed, msg={msg}", level=log_utils.LOGERROR)
                    for k, v in {
                        "trakt.client_id": var.client_am,
                        "trakt.client_secret": var.secret_am,
                        "trakt.token": your_token,
                        "trakt_user": your_username,
                        "trakt.refresh": your_refresh,
                        "trakt.expires": your_expires,
                        "trakt_indicators_active": "true",
                        "watched_indicators": "1",
                    }.items():
                        addon.setSetting(k, v)
                    #control.remake_pov_settings()
                    xbmc.sleep(500)
                    control.remake_pov_trakt_cache()
        except Exception as e:
            log_utils.error(f"POV Trakt Failed: {e}")

        # ===================== The Coalition =====================
        # ============ API Keys applied to settings.xml ===========
        try:
            if "The Coalition" in current and exists(var.chk_coal) and exists(var.chkset_coal):
                addon = xbmcaddon.Addon("plugin.video.coalition")
                chk_auth = addon.getSetting("trakt.token")
                if refresh_sync(mode, chk_auth, master_token):
                    patched, msg = control.startup_patch(var.path_coal_service)
                    if not patched:
                        log_utils.log(f"The Coalition startup patch failed, msg={msg}", level=log_utils.LOGERROR)
                    for k, v in {
                        "trakt.client_id": var.client_am,
                        "trakt.client_secret": var.secret_am,
                        "trakt.token": your_token,
                        "trakt_user": your_username,
                        "trakt.refresh": your_refresh,
                        "trakt.expires": your_expires,
                        "trakt_indicators_active": "true",
                        "watched_indicators": "1",
                    }.items():
                        addon.setSetting(k, v)
                    if authorize(mode):
                        #control.remake_coal_settings()
                        xbmc.sleep(500)
                        control.remake_coal_trakt_cache()
        except Exception as e:
            log_utils.error(f"The Coalition Trakt Failed: {e}")
            
        # =================== Dradis / Genocide ===================
        # ============ API Keys applied to settings.xml ===========
        addons = [
            #("Dradis",        "plugin.video.dradis",    var.chk_dradis, var.chkset_dradis, var.path_dradis_service),
            ("Genocide",      "plugin.video.genocide",  var.chk_genocide, var.chkset_genocide, var.path_genocide_service),
        ]
        for name, plugin, chk_addon, chk_setting, path_service in addons:
            try:
                if name in current and exists(chk_addon) and exists(chk_setting):
                    addon = xbmcaddon.Addon(plugin)
                    chk_auth = addon.getSetting("trakt.token")
                    if refresh_sync(mode, chk_auth, master_token):
                        patched, msg = control.startup_patch(path_service)
                        if not patched:
                            log_utils.log(f"{name} startup patch failed, msg={msg}", level=log_utils.LOGERROR)
                        expires = int(time.time() + (8 * 86400))
                        for k, v in {
                            "trakt.client_id": var.client_am,
                            "trakt.client_secret": var.secret_am,
                            "trakt.username": your_username,
                            "trakt.token": your_token,
                            "trakt.refresh": your_refresh,
                            "trakt.expires": str(expires),
                            "trakt.isauthed": "true",
                        }.items():
                            addon.setSetting(k, v)
            except Exception as e:
                log_utils.error(f"{name} Trakt Failed: {e}")

        # ========================= Shadow / Ghost =========================
        # ==================================================================
        # ============== Start-up Service Patch NOT Required ===============
        addons = [
            ("Shadow", "plugin.video.shadow", var.chk_shadow, var.shadow_ud, var.chkset_shadow, var.shadow),
            ("Ghost",  "plugin.video.ghost",  var.chk_ghost,  var.ghost_ud,  var.chkset_ghost,  var.ghost),
            ("The Chains",  "plugin.video.thechains",  var.chk_chains,  var.chains_ud,  var.chkset_chains,  var.chains), 
        ]

        for name, plugin, chk_addon, ud_path, chk_setting, base_path in addons:
            try:
                if name in current and exists(chk_addon):
                    addon = xbmcaddon.Addon(plugin)
                    chk_auth = addon.getSetting("trakt_access_token")

                    if refresh_sync(mode, chk_auth, master_token):
                        for k, v in {
                            "trakt_access_token": your_token,
                            "trakt_refresh_token": your_refresh,
                            "trakt_expires_at": your_expires,
                        }.items():
                            addon.setSetting(k, v)

                        if name == "Shadow":
                            path = var.path_shadow
                            old_client = var.shadow_client
                            old_secret = var.shadow_secret
                        elif name == "Ghost":
                            path = var.path_ghost
                            old_client = var.ghost_client
                            old_secret = var.ghost_secret
                        elif name == "The Chains":
                            path = var.path_chains
                            old_client = var.thechains_client
                            old_secret = var.thechains_secret

                        try:
                            with open(path, "r", encoding="utf-8") as f:
                                data = f.read()

                            patched = False
                            if old_client in data or old_secret in data:
                                data = data.replace(old_client, var.client_am).replace(old_secret, var.secret_am)
                                with open(path, "w", encoding="utf-8") as f:
                                    f.write(data)
                                patched = True
                            elif var.client_am in data and var.secret_am in data:
                                patched = True

                            if not patched:
                                log_utils.log(f"{name}: Trakt keys NOT patched")

                        except Exception as e:
                            log_utils.error(f"{name} Trakt API keys patch failed: {e}")

            except Exception as e:
                log_utils.error(f"{name} Trakt Failed: {e}")


        # ============= Homelander / Nightwing / Jokers Absolution =============
        # =================== API Keys applied to settings.xml =================
        addons = [
            ("Homelander",        "plugin.video.homelander", var.chk_home,  var.home_ud,  var.chkset_home,  var.home, var.path_home_service),
            ("Nightwing",         "plugin.video.nightwing",  var.chk_night, var.night_ud, var.chkset_night, var.night, var.path_night_service),
            ("Jokers Absolution", "plugin.video.absolution", var.chk_absol, var.absol_ud, var.chkset_absol, var.absol, var.path_absol_service),
        ]

        for name, plugin, chk_addon, ud_path, chk_setting, base_path, path_service in addons:
            try:
                if name in current and exists(chk_addon):
                    addon = xbmcaddon.Addon(plugin)
                    chk_auth = addon.getSetting("trakt.token")
                    if refresh_sync(mode, chk_auth, master_token):
                        patched, msg = control.startup_patch(path_service)
                        if not patched:
                            log_utils.log(f"{name} startup patch failed, msg={msg}", level=log_utils.LOGERROR)
                        for k, v in {
                            "trakt.user": your_username,
                            "trakt.token": your_token,
                            "trakt.refresh": your_refresh,
                            "trakt.authed": "yes",
                            "trakt.client_id": var.client_am,
                            "trakt.client_secret": var.secret_am,
                        }.items():
                            addon.setSetting(k, v)
            except Exception as e:
                log_utils.error(f"{name} Trakt Failed: {e}")

        # ========================= The Crew =========================
        try:
            if "The Crew" in current:
                if exists(var.chk_crew) and exists(var.chkset_crew):
                    addon = xbmcaddon.Addon("plugin.video.thecrew")
                    chk_auth = addon.getSetting("trakt.token")
                    if refresh_sync(mode, chk_auth, master_token):
                        with open(var.path_crew, "r") as f:
                            data = f.read()

                        patched_keys = False
                        if var.crew_client in data or var.crew_secret in data:
                            data = data.replace(var.crew_client, var.client_am).replace(var.crew_secret, var.secret_am)
                            with open(var.path_crew, "w") as f:
                                f.write(data)
                            patched_keys = True

                        elif var.client_am in data and var.secret_am in data:
                            patched_keys = True

                        if not patched_keys:
                            log_utils.log("The Crew Trakt keys NOT patched")

                        patched, msg = control.startup_patch(var.path_crew_service)
                        if not patched:
                            log_utils.log(f"The Crew startup patch failed, msg={msg}", level=log_utils.LOGERROR)

                        for k, v in {
                            "trakt.user": your_username,
                            "trakt.token": your_token,
                            "trakt.refresh": your_refresh,
                        }.items():
                            addon.setSetting(k, v)
        except Exception as e:
            log_utils.error(f"The Crew Trakt Failed: {e}")

        # ========================= SALTS =========================
        try:
            if "SALTS" in current:
                if exists(var.chk_salts) and exists(var.chkset_salts):
                    addon = xbmcaddon.Addon("plugin.video.salts")
                    chk_auth = addon.getSetting("trakt_access_token")
                    if refresh_sync(mode, chk_auth, master_token):
                        with open(var.path_salts, "r") as f:
                            data = f.read()

                        patched_keys = False
                        if var.salts_client in data or var.salts_secret in data:
                            data = data.replace(var.salts_client, var.client_am).replace(var.salts_secret, var.secret_am)
                            with open(var.path_salts, "w") as f:
                                f.write(data)
                            patched_keys = True
                        elif var.client_am in data and var.secret_am in data:
                            patched_keys = True

                        if not patched_keys:
                            log_utils.log("SALTS Trakt keys NOT patched")

                        patched, msg = control.startup_patch(var.path_salts_service)
                        if not patched:
                            log_utils.log(f"SALTS startup patch failed, msg={msg}", level=log_utils.LOGERROR)

                        for k, v in {
                            "trakt_access_token": your_token,
                            "trakt_refresh_token": your_refresh,
                            "trakt_expires": your_expires,
                            "trakt_enabled": "true",
                        }.items():
                            addon.setSetting(k, v)
        except Exception as e:
            log_utils.error(f"SALTS Trakt Failed: {e}")

        '''# ========================= Orion =========================
        try:
            if "Orion" in current:
                if exists(var.chk_orion) and exists(var.chkset_orion):
                    addon = xbmcaddon.Addon("plugin.video.orion")
                    chk_auth = addon.getSetting("trakt_token")
                    if refresh_sync(mode, chk_auth, master_token):
                        with open(var.path_orion, "r") as f:
                            data = f.read()

                        patched_keys = False
                        if var.orion_client in data or var.orion_secret in data:
                            data = data.replace(var.orion_client, var.client_am).replace(var.orion_secret, var.secret_am)
                            with open(var.path_orion, "w") as f:
                                f.write(data)
                            patched_keys = True
                        elif var.client_am in data and var.secret_am in data:
                            patched_keys = True

                        if not patched_keys:
                            log_utils.log("Orion Trakt keys NOT patched")

                        for k, v in {
                            "trakt_token": your_token,
                            "trakt_refresh": your_refresh,
                            "trakt_enabled": "true",
                        }.items():
                            addon.setSetting(k, v)
        except Exception as e:
            log_utils.error(f"Orion Trakt Failed: {e}")

        # ========================= Genesis =========================
        try:
            if "Genesis" in current:
                if exists(var.chk_gen) and exists(var.chkset_gen):
                    addon = xbmcaddon.Addon("plugin.video.genesis")
                    chk_auth = addon.getSetting("trakt.token")
                    if refresh_sync(mode, chk_auth, master_token):
                        with open(var.path_gen, "r") as f:
                            data = f.read()

                        patched_keys = False
                        if var.genesis_client in data or var.genesis_secret in data:
                            data = data.replace(var.genesis_client, var.client_am).replace(var.genesis_secret, var.secret_am)
                            with open(var.path_gen, "w") as f:
                                f.write(data)
                            patched_keys = True
                        elif var.client_am in data and var.secret_am in data:
                            patched_keys = True

                        if not patched_keys:
                            log_utils.log("Genesis Trakt keys NOT patched")

                        patched, msg = control.startup_patch(var.path_gen_service)
                        if not patched:
                            log_utils.log(f"Genesis startup patch failed, msg={msg}", level=log_utils.LOGERROR)

                        for k, v in {
                            "trakt.user": your_username,
                            "trakt.token": your_token,
                            "trakt.refresh": your_refresh,
                        }.items():
                            addon.setSetting(k, v)
        except Exception as e:
            log_utils.error(f"Genesis Trakt Failed: {e}")

        # ========================= Syncher =========================
        try:
            if "Syncher" in current:
                if exists(var.chk_sync) and exists(var.chkset_sync):
                    addon = xbmcaddon.Addon("plugin.video.syncher")
                    chk_auth = addon.getSetting("trakt.token")
                    if refresh_sync(mode, chk_auth, master_token):
                        with open(var.path_sync, "r") as f:
                            data = f.read()

                        patched_keys = False
                        if var.syncher_client in data or var.syncher_secret in data:
                            data = data.replace(var.syncher_client, var.client_am).replace(var.syncher_secret, var.secret_am)
                            with open(var.path_sync, "w") as f:
                                f.write(data)
                            patched_keys = True
                        elif var.client_am in data and var.secret_am in data:
                            patched_keys = True

                        if not patched_keys:
                            log_utils.log("Syncher Trakt keys NOT patched")

                        for k, v in {
                            "trakt.user": your_username,
                            "trakt.token": your_token,
                            "trakt.refresh": your_refresh,
                        }.items():
                            addon.setSetting(k, v)
        except Exception as e:
            log_utils.error(f"Syncher Trakt Failed: {e}")'''

        # ========================= Scrubs V2 =========================
        try:
            if "Scrubs V2" in current:
                if exists(var.chk_scrubs) and exists(var.chkset_scrubs):
                    addon = xbmcaddon.Addon("plugin.video.scrubsv2")
                    chk_auth = addon.getSetting("trakt.token")
                    if refresh_sync(mode, chk_auth, master_token):
                        with open(var.path_scrubs, "r") as f:
                            data = f.read()

                        patched_keys = False
                        if var.scrubs_client in data or var.scrubs_secret in data:
                            data = data.replace(var.scrubs_client, var.client_am).replace(var.scrubs_secret, var.secret_am)
                            with open(var.path_scrubs, "w") as f:
                                f.write(data)
                            patched_keys = True
                        elif var.client_am in data and var.secret_am in data:
                            patched_keys = True

                        if not patched_keys:
                            log_utils.log("Scrubs V2 Trakt keys NOT patched")

                        patched, msg = control.startup_patch(var.path_scrubs_service)
                        if not patched:
                            log_utils.log(f"Scrubs V2 startup patch failed, msg={msg}", level=log_utils.LOGERROR)

                        for k, v in {
                            "trakt.user": your_username,
                            "trakt.token": your_token,
                            "trakt.refresh": your_refresh,
                            "trakt.authed": "yes",
                        }.items():
                            addon.setSetting(k, v)
        except Exception as e:
            log_utils.error(f"Scrubs V2 Trakt Failed: {e}")

        # ========================= Gratis Red =========================
        try:
            if "Gratis Red" in current:
                if exists(var.chk_redg) and exists(var.chkset_redg):
                    addon = xbmcaddon.Addon("plugin.video.gratisred")
                    chk_auth = addon.getSetting("trakt.token")
                    if refresh_sync(mode, chk_auth, master_token):
                        with open(var.path_redg, "r") as f:
                            data = f.read()

                        patched_keys = False
                        if var.redg_client in data or var.redg_secret in data:
                            data = data.replace(var.redg_client, var.client_am).replace(var.redg_secret, var.secret_am)
                            with open(var.path_redg, "w") as f:
                                f.write(data)
                            patched_keys = True
                        elif var.client_am in data and var.secret_am in data:
                            patched_keys = True

                        if not patched_keys:
                            log_utils.log("Gratis Red Trakt keys NOT patched")

                        patched, msg = control.startup_patch(var.path_redg_service)
                        if not patched:
                            log_utils.log(f"Gratis Red startup patch failed, msg={msg}", level=log_utils.LOGERROR)

                        for k, v in {
                            "trakt.user": your_username,
                            "trakt.token": your_token,
                            "trakt.refresh": your_refresh,
                            "trakt.authed": "yes",
                        }.items():
                            addon.setSetting(k, v)
        except Exception as e:
            log_utils.error(f"Gratis Red Trakt Failed: {e}")

        # ========================= TMDb Helper =========================
        try:
            if "TMDb Helper" in current and exists(var.chk_tmdbh):
                addon = xbmcaddon.Addon("plugin.video.themoviedb.helper")
                chk_auth = addon.getSetting("trakt_token")

                if refresh_sync(mode, chk_auth, master_token):
                    with open(var.path_tmdbh, "r") as f:
                        data = f.read()

                    patched_keys = False
                    if var.tmdbh_client in data or var.tmdbh_secret in data:
                        # Replace old keys
                        data = data.replace(var.tmdbh_client, var.client_am).replace(var.tmdbh_secret, var.secret_am)
                        with open(var.path_tmdbh, "w") as f:
                            f.write(data)
                        patched_keys = True
                    elif var.client_am in data and var.secret_am in data:
                        # Keys are already correct
                        patched_keys = True

                    if not patched_keys:
                        log_utils.log("TMDbH Trakt keys NOT patched")

                    patched, msg = control.startup_patch(var.path_tmdbh_service)
                    if not patched:
                        log_utils.log(f"TMDbH startup patch failed, msg={msg}", level=log_utils.LOGERROR)

                    expires_int = int(float(your_expires or 0))
                    tmdbh_data = (
                        '{"access_token":"%s","token_type":"bearer",'
                        '"expires_in":7776000,"refresh_token":"%s",'
                        '"scope":"public","created_at":%s}'
                        % (your_token, your_refresh, expires_int)
                    )

                    addon.setSettingString("trakt_token", tmdbh_data)
                    addon.setSetting("startup_notifications", "false")
        except Exception as e:
            log_utils.error(f"TMDBh Trakt Failed: {e}")

        '''# ========================= Trakt Player =========================
        try:
            if "Trakt Player" in current:
                if exists(var.chk_tkplay) and exists(var.chkset_tkplay):
                    addon = xbmcaddon.Addon("plugin.video.trakt_player")
                    chk_auth = addon.getSetting("trakt_access_token")
                    if refresh_sync(mode, chk_auth, master_token):
                        with open(var.path_tkplay, "r") as f:
                            data = f.read()

                        patched_keys = False
                        if var.tkplay_client in data or var.tkplay_secret in data:
                            data = data.replace(var.tkplay_client, var.client_am).replace(var.tkplay_secret, var.secret_am)
                            with open(var.path_tkplay, "w") as f:
                                f.write(data)
                            patched_keys = True
                        elif var.client_am in data and var.secret_am in data:
                            patched_keys = True

                        if not patched_keys:
                            log_utils.log("Trakt Player Trakt keys NOT patched")

                        patched, msg = control.startup_patch(var.path_tkplay_service)
                        if not patched:
                            log_utils.log(f"Trakt Player startup patch failed, msg={msg}", level=log_utils.LOGERROR)

                        for k, v in {
                            "trakt_access_token": your_token,
                            "trakt_refresh_token": your_refresh,
                            "trakt_auth_done": "true",
                        }.items():
                            addon.setSetting(k, v)
        except Exception as e:
            log_utils.error(f"Trakt Player Trakt Failed: {e}")'''

        # ========================= Trakt Addon =========================
        try:
            if "Trakt Addon" in current and exists(var.chk_trakt) and exists(var.chkset_trakt):
                addon = xbmcaddon.Addon("script.trakt")
                chk_auth = addon.getSetting("trakt_token")

                if refresh_sync(mode, chk_auth, master_token):
                    with open(var.path_trakt, "r") as f:
                        data = f.read()

                    patched_keys = False
                    if var.trakt_client_obs_str in data or var.trakt_secret_obs_str in data:
                        data = data.replace(var.trakt_client_obs_str, var.client_am_obs_str).replace(var.trakt_secret_obs_str, var.secret_am_obs_str)
                        with open(var.path_trakt, "w") as f:
                            f.write(data)
                        patched_keys = True
                    elif var.client_am_obs_str in data and var.secret_am_obs_str in data:
                        patched_keys = True

                    if not patched_keys:
                        log_utils.log("Trakt Addon Trakt keys NOT patched")

                    patched, msg = control.startup_patch(var.path_trakt_service)
                    if not patched:
                        log_utils.log(f"Trakt Add-on startup patch failed, msg={msg}", level=log_utils.LOGERROR)

                    expires_int = int(float(your_expires or 0))
                    trakt_data = (
                        '{"access_token":"%s","token_type":"bearer",'
                        '"expires_in":7776000,"refresh_token":"%s",'
                        '"scope":"public","created_at":%s}'
                        % (your_token, your_refresh, expires_int)
                    )

                    addon.setSetting("user", your_username)
                    addon.setSetting("authorization", trakt_data)
        except Exception as e:
            log_utils.error(f"Trakt Addon Trakt Failed: {e}")
