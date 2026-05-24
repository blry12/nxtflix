# -*- coding: utf-8 -*-
import xbmc, xbmcaddon, xbmcvfs
import json
import os

from acctmgr.modules import control
from acctmgr.modules import var
from acctmgr.modules import log_utils

# Variables
joinPath = os.path.join
exists = xbmcvfs.exists

class Auth:
    def mdblist_auth(self):

        # ========================= NXTFlix Light Variables =========================
        acctmgr = xbmcaddon.Addon("script.module.acctmgr")
        your_mdb_username = acctmgr.getSetting("mdblist.username")
        your_mdb_apikey = acctmgr.getSetting("mdblist.apikey")
        mdb_master_apikey = your_mdb_apikey

        '''# =================== Copy Addon Data (settings.xml) ==================
        addons = [
            ("Shadow",       var.chk_shadow, var.shadow_ud,  var.chkset_shadow,  var.shadow),
            ("Ghost",        var.chk_ghost,  var.ghost_ud,   var.chkset_ghost,   var.ghost),
            ("The Chains",   var.chk_chains, var.chains_ud,  var.chkset_chains,  var.chains),
            ("Otaku",        var.chk_otaku,  var.otaku_ud,   var.chkset_otaku,   var.otaku),
            ("SALTS",        var.chk_salts,  var.salts_ud,   var.chkset_salts,   var.salts),
            #("Orion",        var.chk_orion,  var.orion_ud,   var.chkset_orion,   var.orion),
            #("Genesis",      var.chk_gen,    var.gen_ud,     var.chkset_gen,     var.gen),
            #("Syncher",      var.chk_sync,   var.sync_ud,    var.chkset_sync,    var.sync),
            ("Otaku",        var.chk_otaku,  var.otaku_ud,   var.chkset_otaku,   var.otaku),
            #("Trakt Player", var.chk_tkplay, var.tkplay_ud,  var.chkset_tkplay,  var.tkplay),
            ("Realizer",     var.chk_realx,  var.realx_ud,   var.chkset_realx,   var.realx),
            ("ResolveURL",   var.chk_rurl,   var.rurl_ud,    var.chkset_rurl,    var.rurl),
        ]

        for name, chk_addon, ud_path, chk_setting, base_path in addons:
            control.copy_addon_settings(
                name,
                chk_addon,
                ud_path,
                chk_setting,
                base_path
            )'''

        # ============================= Umbrella / Dradis / POV / Coalition / TMDbH =============================
        for addon_id, chk_addon, chk_settings, label, mdb_user_key, mdb_api_key, indicators_act, wtch_indicators, remake_settings in (
            ("plugin.video.umbrella",          var.chk_umb,    var.chkset_umb,    "Umbrella",   None,               "mdblist.api",    None,                     None,                 None),
            #("plugin.video.dradis",            var.chk_dradis, var.chkset_dradis, "Dradis",     "mdblist.username", "mdblist.token",  None,                     None,                 None),
            ("plugin.video.pov",               var.chk_pov,    var.chkset_pov,    "POV",        "mdblist_user",     "mdblist.token",  "mdbl_indicators_active", "watched_indicators", control.remake_pov_settings),
            ("plugin.video.coalition",         var.chk_coal,   var.chkset_coal,   "Coalition",  None,               "mdblist.token",  None,                     None,                 control.remake_coal_settings),
            ("plugin.video.themoviedb.helper", var.chk_tmdbh,  var.chkset_tmdbh,  "TMDbH",      None,               "mdblist_apikey", None,                     None,                 None),
        ):
            try:
                if not (exists(chk_addon) and exists(chk_settings)):
                    continue

                addon = xbmcaddon.Addon(addon_id)

                current_token = addon.getSetting(mdb_api_key) if mdb_api_key else ""

                if current_token == mdb_master_apikey:
                    continue  # Already authed, skip

                settings = {}

                if mdb_api_key:
                    settings[mdb_api_key] = your_mdb_apikey

                if mdb_user_key:
                    settings[mdb_user_key] = your_mdb_username

                if indicators_act:
                    settings[indicators_act] = "true"

                if wtch_indicators:
                    settings[wtch_indicators] = "2"

                for k, v in settings.items():
                    addon.setSetting(k, v)

                if remake_settings:
                    xbmc.sleep(200)
                    #remake_settings()

            except Exception as e:
                log_utils.error(f"{label} MDBList Failed: {e}")

        # ============================= FENtastic / Nimbus =============================
        try:
            json_query = xbmc.executeJSONRPC(
                '{"jsonrpc":"2.0","method":"Settings.GetSettingValue","params":{"setting":"lookandfeel.skin"},"id":1}'
            )
            json_query = json.loads(json_query)

            skin_chk = ""
            if "result" in json_query and "value" in json_query["result"]:
                skin_chk = json_query["result"]["value"]
                
            # FENtastic
            if skin_chk == "skin.fentastic" and xbmcvfs.exists(var.chk_fentastic) and xbmcvfs.exists(var.chkset_fentastic):
                with open(var.path_fentastic, "r", encoding="utf-8") as f:
                    data = f.read()

                if mdb_master_apikey not in data:
                    xbmc.executebuiltin('Skin.SetString(mdblist_api_key,{})'.format(your_mdb_apikey))

            # Nimbus
            elif skin_chk == "skin.nimbus" and xbmcvfs.exists(var.chk_nimbus) and xbmcvfs.exists(var.chkset_nimbus):
                with open(var.path_nimbus, "r", encoding="utf-8") as f:
                    data = f.read()

                if mdb_master_apikey not in data:
                    xbmc.executebuiltin('Skin.SetString(mdblist_api_key,{})'.format(your_mdb_apikey))

        except Exception as e:
            log_utils.error(f"Skin MDBList Failed: {e}")
