# -*- coding: utf-8 -*-
import xbmc, xbmcaddon, xbmcgui
import xbmcvfs
import os

from acctmgr.modules import var
from acctmgr.modules import control
from acctmgr.modules import log_utils
from acctmgr.modules.db import chk_auth_db
from acctmgr.modules.db import offcloud_db

# Variables
exists = xbmcvfs.exists

class Auth:
    def offcloud_auth(self):

        # ========================= NXTFlix Light Variables =========================
        acctmgr = xbmcaddon.Addon("script.module.acctmgr")
        your_username = acctmgr.getSetting("offcloud.userid")
        your_token = acctmgr.getSetting("offcloud.token")
        master_token = your_token

        '''
        # ========================= NXTFlix Light =========================
        try:
            if exists(var.chk_nxtflixlt):
                if not exists(var.chkset_nxtflixlt):
                    control.remake_settings(var.nxtflixlt_id, var.nxtflixlt_name)
                    xbmc.sleep(500)

                if exists(var.chkset_nxtflixlt):
                    settings_db = var.nxtflixlt_settings_db
                    chk_auth = chk_auth_db.chk_auth(settings_db, "oc.token")

                    if chk_auth != master_token:
                        offcloud_db.auth(settings_db)
                        xbmc.sleep(300)
                        control.remake_settings(var.nxtflixlt_id, var.nxtflixlt_name)
        except Exception as e:
            log_utils.error("NXTFlix Light OffCloud Failed")

        # ========================= Gears =========================
        try:
            if exists(var.chk_gears):
                if not exists(var.chkset_gears):
                    control.remake_settings(var.gears_id, var.gears_name)
                    xbmc.sleep(500)

                if exists(var.chkset_gears):
                    settings_db = var.gears_settings_db
                    chk_auth = chk_auth_db.chk_auth(settings_db, "oc.token")

                    if chk_auth != master_token:
                        offcloud_db.auth(settings_db)
                        xbmc.sleep(300)
                        control.remake_settings(var.gears_id, var.gears_name)
        except Exception as e:
            log_utils.error("Gears OffCloud Failed")

        # ========================= Umbrella =========================
        try:
            if exists(var.chk_umb) and exists(var.chkset_umb):
                addon = xbmcaddon.Addon("plugin.video.umbrella")
                chk_auth = addon.getSetting("offcloudtoken")
                if chk_auth != master_token:
                    for k, v in {
                        "offcloud.username": your_username,
                        "offcloudtoken": your_token,
                        "offcloud.enable": "true",
                    }.items():
                        addon.setSetting(k, v)
        except Exception as e:
            log_utils.error("Umbrella OffCloud Failed")'''

        # ========================= POV =========================
        try:
            if exists(var.chk_pov) and exists(var.chkset_pov):
                addon = xbmcaddon.Addon("plugin.video.pov")
                chk_auth = addon.getSetting("oc.token")
                if chk_auth != master_token:
                    for k, v in {
                        "oc.account_id": your_username,
                        "oc.token": your_token,
                        "oc.enabled": "true",
                    }.items():
                        addon.setSetting(k, v)
                    xbmc.sleep(200)
                    #control.remake_pov_settings
        except Exception as e:
            log_utils.error(f"POV OffCloud Failed: {e}")

        # ========================= Dradis / Genocide =========================
        addons = [
            ("Dradis",   "plugin.video.dradis",   var.chk_dradis,   var.chkset_dradis),
            #("Genocide", "plugin.video.genocide", var.chk_genocide, var.chkset_genocide),
        ]

        for name, plugin, chk_addon, chk_setting in addons:
            try:
                if exists(chk_addon) and exists(chk_setting):
                    addon = xbmcaddon.Addon(plugin)
                    chk_auth = addon.getSetting("offcloud.token")
                    if chk_auth != master_token:
                        for k, v in {
                            "offcloud.username": your_username,
                            "offcloud.token": your_token,
                            "offcloud.enabled": "true",
                        }.items():
                            addon.setSetting(k, v)
            except Exception as e:
                log_utils.error(f"{name} OffCloud Failed: {e}")
