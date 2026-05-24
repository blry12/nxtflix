# -*- coding: utf-8 -*-
import xbmc, xbmcaddon, xbmcvfs
import json
import os

from acctmgr.modules import control
from acctmgr.modules import var
from acctmgr.modules import log_utils
from acctmgr.modules.db import chk_auth_db
from acctmgr.modules.db import debrid_db

# Variables
joinPath = os.path.join
exists = xbmcvfs.exists

class Auth:
    def realdebrid_auth(self):

        # ========================= NXTFlix Light Variables =========================
        acctmgr = xbmcaddon.Addon("script.module.acctmgr")
        your_rd_username = acctmgr.getSetting("realdebrid.username")
        your_rd_token = acctmgr.getSetting("realdebrid.token")
        your_rd_client_id = acctmgr.getSetting("realdebrid.client_id")
        your_rd_refresh = acctmgr.getSetting("realdebrid.refresh")
        your_rd_secret = acctmgr.getSetting("realdebrid.secret")
        rd_master_token = your_rd_token

        # =================== Copy Addon Data (settings.xml) ==================
        addons = [
            ("Shadow",        var.chk_shadow, var.shadow_ud,  var.chkset_shadow,  var.shadow),
            ("Ghost",         var.chk_ghost,  var.ghost_ud,   var.chkset_ghost,   var.ghost),
            ("The Chains",    var.chk_chains, var.chains_ud,  var.chkset_chains,  var.chains),
            ("Otaku",         var.chk_otaku,  var.otaku_ud,   var.chkset_otaku,   var.otaku),
            ("SALTS",         var.chk_salts,  var.salts_ud,   var.chkset_salts,   var.salts),
            #("Orion",        var.chk_orion,  var.orion_ud,   var.chkset_orion,   var.orion),
            #("Genesis",      var.chk_gen,    var.gen_ud,     var.chkset_gen,     var.gen),
            #("Syncher",      var.chk_sync,   var.sync_ud,    var.chkset_sync,    var.sync),
            ("Otaku",         var.chk_otaku,  var.otaku_ud,   var.chkset_otaku,   var.otaku),
            #("Trakt Player", var.chk_tkplay, var.tkplay_ud,  var.chkset_tkplay,  var.tkplay),
            ("Realizer",      var.chk_realx,  var.realx_ud,   var.chkset_realx,   var.realx),
            ("ResolveURL",    var.chk_rurl,   var.rurl_ud,    var.chkset_rurl,    var.rurl),
        ]

        for name, chk_addon, ud_path, chk_setting, base_path in addons:
            control.copy_addon_settings(
                name,
                chk_addon,
                ud_path,
                chk_setting,
                base_path
            )

        # ========================= NXTFlix Light / The Gears / Red Light =========================
        addons = (
            ("NXTFlix Light", var.chk_nxtflixlt, var.chkset_nxtflixlt, var.nxtflixlt_settings_db, control.remake_nxtflixlt_settings),
            ("Gears", var.chk_gears, var.chkset_gears, var.gears_settings_db, control.remake_gears_settings),
            ("Red Light", var.chk_red, var.chkset_red, var.red_settings_db, control.remake_red_settings),
        )

        for addon_name, chk_path, chkset_path, settings_db, remake_func in addons:
            try:
                if exists(chk_path):

                    if not exists(chkset_path):
                        remake_func()
                        xbmc.sleep(500)

                    if exists(chkset_path):
                        chk_auth = chk_auth_db.chk_auth(settings_db, "rd.token")

                        if chk_auth != rd_master_token:
                            debrid_db.auth_rd(settings_db)

                            chk_auth_pm = chk_auth_db.chk_auth(settings_db, "pm.token")
                            if chk_auth_pm not in ('empty_setting', '', None):
                                debrid_db.enable_pm(settings_db)
                            else:
                                debrid_db.disable_pm(settings_db)

                            chk_auth_ad = chk_auth_db.chk_auth(settings_db, "ad.token")
                            if chk_auth_ad not in ('empty_setting', '', None):
                                debrid_db.enable_ad(settings_db)
                            else:
                                debrid_db.disable_ad(settings_db)

                            xbmc.sleep(200)
                            remake_func()

            except Exception as e:
                log_utils.error(f"{addon_name} Real-Debrid Failed: {e}")

        # ========================= Umbrella =========================
        try:
            if exists(var.chk_umb) and exists(var.chkset_umb):
                addon = xbmcaddon.Addon("plugin.video.umbrella")
                chk_auth = addon.getSetting("realdebridtoken")
                chk_auth_pm = addon.getSetting("premiumizetoken")
                chk_auth_ad = addon.getSetting("alldebridtoken")
                if chk_auth != rd_master_token:
                    for k, v in {
                        "realdebridusername": your_rd_username,
                        "realdebridtoken": your_rd_token,
                        "realdebrid.clientid": your_rd_client_id,
                        "realdebridrefresh": your_rd_refresh,
                        "realdebridsecret": your_rd_secret,
                        "realdebrid.enable": "true",
                        "premiumize.enable": "true" if chk_auth_pm else "false",
                        "alldebrid.enable": "true" if chk_auth_ad else "false",
                    }.items():
                        addon.setSetting(k, v)
        except Exception as e:
            log_utils.error(f"Umbrella Real-Debrid Failed: {e}")

        # ========================= Fen / POV =========================
        for addon_id, chk_addon, chk_settings, label, rd_user_key, remake_settings in (
            #("plugin.video.fen", var.chk_fen, var.chkset_fen, "Fen", "rd.account_id", None),
            ("plugin.video.pov", var.chk_pov, var.chkset_pov, "POV", "rd.username", control.remake_pov_settings),
        ):
            try:
                if exists(chk_addon) and exists(chk_settings):
                    addon = xbmcaddon.Addon(addon_id)

                    chk_auth_rd = addon.getSetting("rd.token")
                    chk_auth_pm = addon.getSetting("pm.token")
                    chk_auth_ad = addon.getSetting("ad.token")

                    if chk_auth_rd != rd_master_token:
                        settings = {
                            rd_user_key:      your_rd_username,
                            "rd.token":       your_rd_token,
                            "rd.client_id":   your_rd_client_id,
                            "rd.refresh":     your_rd_refresh,
                            "rd.secret":      your_rd_secret,
                            "rd.enabled":     "true",
                            "pm.enabled":     "true" if chk_auth_pm else "false",
                            "ad.enabled":     "true" if chk_auth_ad else "false",
                        }

                        for k, v in settings.items():
                            addon.setSetting(k, v)

                        if remake_settings:
                            xbmc.sleep(200)
                            #remake_settings()

            except Exception as e:
                log_utils.error(f"{label} Real-Debrid Failed: {e}")

        '''# ========================= Seren =========================
        try:
            if exists(var.chk_seren) and exists(var.chkset_seren):
                addon = xbmcaddon.Addon("plugin.video.seren")
                chk_auth = addon.getSetting("rd.auth")
                chk_auth_pm = addon.getSetting("premiumize.token")
                chk_auth_ad = addon.getSetting("alldebrid.apikey")
                if chk_auth != rd_master_token:
                    for k, v in {
                        "rd.username": your_rd_username,
                        "rd.auth": your_rd_token,
                        "rd.client_id": your_rd_client_id,
                        "rd.refresh": your_rd_refresh,
                        "rd.secret": your_rd_secret,
                        "realdebrid.premiumstatus": "Premium",
                        "realdebrid.enabled": "true",
                        "premiumize.enabled": "true" if chk_auth_pm else "false",
                        "alldebrid.enabled": "true" if chk_auth_ad else "false",
                    }.items():
                        addon.setSetting(k, v)
        except Exception as e:
            log_utils.error("Seren Real-Debrid Failed")'''

        # =============== Dradis / Genocide ===============
        addons = [
            #("Dradis",   "plugin.video.dradis",   var.chk_dradis,   var.chkset_dradis),
            ("Genocide", "plugin.video.genocide", var.chk_genocide, var.chkset_genocide),
        ]

        for name, plugin, chk_addon, chk_setting in addons:
            try:
                if exists(chk_addon) and exists(chk_setting):
                    addon = xbmcaddon.Addon(plugin)
                    chk_auth = addon.getSetting("realdebrid.token")
                    if chk_auth != rd_master_token:
                        for k, v in {
                            "realdebrid.username": your_rd_username,
                            "realdebrid.token": your_rd_token,
                            "realdebrid.client_id": your_rd_client_id,
                            "realdebrid.refresh": your_rd_refresh,
                            "realdebrid.secret": your_rd_secret,
                            "realdebrid.enable": "true",
                        }.items():
                            addon.setSetting(k, v)
            except Exception as e:
                log_utils.error(f"{name} Real-Debrid Failed: {e}")

        # =============== Shadow / Ghost / The Chains ===============
        addons = [
            ("Shadow",     "plugin.video.shadow",    var.chk_shadow,  var.shadow_ud,  var.chkset_shadow,  var.shadow),
            ("Ghost",      "plugin.video.ghost",     var.chk_ghost,   var.ghost_ud,   var.chkset_ghost,   var.ghost),
            ("The Chains", "plugin.video.thechains", var.chk_chains,  var.chains_ud,  var.chkset_chains,  var.chains),
        ]

        for name, plugin, chk_addon, ud_path, chk_setting, base_path in addons:
            try:
                if exists(chk_addon):
                    addon = xbmcaddon.Addon(plugin)
                    chk_auth = addon.getSetting("rd.auth")
                    chk_auth_pm = addon.getSetting("premiumize.token")
                    chk_auth_ad = addon.getSetting("alldebrid.token")
                    if chk_auth != rd_master_token:
                        for k, v in {
                            "debrid_use": "true",
                            "debrid_use_rd": "true",
                            "rd.auth": your_rd_token,
                            "rd.client_id": your_rd_client_id,
                            "rd.refresh": your_rd_refresh,
                            "rd.secret": your_rd_secret,
                            "debrid_use_pm": "true" if chk_auth_pm else "false",
                            "debrid_use_ad": "true" if chk_auth_ad else "false",
                        }.items():
                            addon.setSetting(k, v)
            except Exception as e:
                log_utils.error(f"{name} Real-Debrid Failed: {e}")

        # ========================= SALTS =========================
        try:
            if exists(var.chk_salts):
                addon = xbmcaddon.Addon("plugin.video.salts")
                chk_auth = addon.getSetting("realdebrid_token")
                if chk_auth != rd_master_token:
                    for k, v in {
                        "realdebrid_token": your_rd_token,
                        "realdebrid_refresh": your_rd_refresh,
                        #"realdebrid_expires": your_rd_expires,
                        "realdebrid_enabled": "true",
                    }.items():
                        addon.setSetting(k, v)
        except Exception as e:
            log_utils.error(f"SALTS Real-Debrid Failed: {e}")

        '''# ========================= Orion =========================
        try:
            if exists(var.chk_orion):
                addon = xbmcaddon.Addon("plugin.video.orion")
                chk_auth = addon.getSetting("rd_token")
                if chk_auth != rd_master_token:
                    for k, v in {
                        "rd_token": your_rd_token,
                        "rd_refresh": your_rd_refresh,
                        "rd_enabled": "true",
                    }.items():
                        addon.setSetting(k, v)
        except Exception as e:
            log_utils.error("Orion Real-Debrid Failed")

        # ========================= Genesis =========================
        try:
            if exists(var.chk_gen):
                addon = xbmcaddon.Addon("plugin.video.genesis")
                chk_auth = addon.getSetting("realdebrid_token")
                if chk_auth != rd_master_token:
                    for k, v in {
                        "realdebrid_token": your_rd_token,
                        "realdebrid_refresh": your_rd_refresh,
                        #"realdebrid_tokenExpireIn": your_rd_expires,
                        "realdebrid_auth": "true",
                    }.items():
                        addon.setSetting(k, v)
        except Exception as e:
            log_utils.error("Genesis Real-Debrid Failed")

        # ========================= Syncher =========================
        try:
            if exists(var.chk_sync):
                addon = xbmcaddon.Addon("plugin.video.syncher")
                chk_auth = addon.getSetting("rd.token")
                if chk_auth != rd_master_token:
                    for k, v in {
                        "rd.token": your_rd_token,
                        "rd.refresh": your_rd_refresh,
                        #"rd.expiry": your_rd_expires,
                        "rd.enabled": "true",
                    }.items():
                        addon.setSetting(k, v)
        except Exception as e:
            log_utils.error("Syncher Real-Debrid Failed")'''

        # ========================= Otaku =========================
        try:
            if exists(var.chk_otaku):
                addon = xbmcaddon.Addon("plugin.video.otaku")
                chk_auth = addon.getSetting("realdebrid.token")
                if chk_auth != rd_master_token:
                    for k, v in {
                        "realdebrid.username": your_rd_username,
                        "realdebrid.client_id": your_rd_client_id,
                        "realdebrid.token": your_rd_token,
                        "realdebrid.refresh": your_rd_refresh,
                        "realdebrid.secret": your_rd_secret,
                        "realdebrid.enabled": "true",
                    }.items():
                        addon.setSetting(k, v)
        except Exception as e:
            log_utils.error(f"Otaku Real-Debrid Failed: {e}")

        '''# ========================= Trakt Player =========================
        try:
            if exists(var.chk_tkplay):
                addon = xbmcaddon.Addon("plugin.video.trakt_player")
                chk_auth = addon.getSetting("rd_access_token")
                if chk_auth != rd_master_token:
                    for k, v in {
                        "rd_access_token": your_rd_token,
                        "rd_refresh_token": your_rd_refresh,
                        "rd_auth_done": "true",
                    }.items():
                        addon.setSetting(k, v)
        except Exception as e:
            log_utils.error("Trakt Player Real-Debrid Failed")'''

        # ========================= Realizer =========================
        try:
            if exists(var.chk_realx):
                if not exists(var.chkset_realx_json):
                    xbmcvfs.copy(joinPath(var.realx_json), joinPath(var.chkset_realx_json))
                if exists(var.chkset_realx) and exists(var.chkset_realx_json):
                    with open(var.chkset_realx_json) as r:
                        data = json.load(r)
                        chk_auth = data.get('token')
                    if chk_auth != rd_master_token:
                        rdauth = {
                            'client_id': acctmgr.getSetting('realdebrid.client_id'),
                            'client_secret': acctmgr.getSetting('realdebrid.secret'),
                            'token': acctmgr.getSetting('realdebrid.token'),
                            'refresh_token': acctmgr.getSetting('realdebrid.refresh'),
                            'added': '202312010243'
                        }
                        with open(var.chkset_realx_json, 'w') as w:
                            json.dump(rdauth, w)
        except Exception as e:
            log_utils.error(f"Realizer Real-Debrid Failed: {e}")
            
        # ========================= ResolveURL =========================
        try:
            if exists(var.chk_rurl):
                addon = xbmcaddon.Addon("script.module.resolveurl")
                chk_auth = addon.getSetting("RealDebridResolver_token")
                if chk_auth != rd_master_token:
                    for k, v in {
                        "RealDebridResolver_login": your_rd_username,
                        "RealDebridResolver_token": your_rd_token,
                        "RealDebridResolver_client_id": your_rd_client_id,
                        "RealDebridResolver_refresh": your_rd_refresh,
                        "RealDebridResolver_client_secret": your_rd_secret,
                        "RealDebridResolver_cached_only": "true",
                    }.items():
                        addon.setSetting(k, v)
        except Exception as e:
            log_utils.error(f"ResolveURL Real-Debrid Failed: {e}")
