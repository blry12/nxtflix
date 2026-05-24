# -*- coding: utf-8 -*-
import xbmc, xbmcaddon, xbmcvfs
import json
import os

from acctmgr.modules import var
from acctmgr.modules import log_utils
from acctmgr.modules import control

# Variables
exists = xbmcvfs.exists
translatePath = xbmcvfs.translatePath

def get_trakt_sync_list():
    if not exists(var.tk_sync_list):
        return []
    try:
        with open(var.tk_sync_list, "r") as f:
            return json.load(f).get("addon_list", [])
    except Exception as e:
        log_utils.error(f"Error reading trakt sync list: {e}")
        return []

def check_api():
    
    current = get_trakt_sync_list()

    # ================= NXTFlix Light / The Gears / Red Light =================
    patches = (
        ("NXTFlix Light", var.chk_nxtflixlt, var.path_nxtflixlt_service, "NXTFlix Light"),
        ("The Gears" or "Gears", var.chk_gears, var.path_gears_service, "The Gears"),
        ("Red Light", var.chk_red, var.path_red_service, "Red Light"),
    )

    for name, check_path, service_path, addon_name in patches:
        if name in current and exists(check_path):
            patched, msg = control.startup_patch(service_path, addon_name=addon_name)

    # ================= Umbrella =================
    if "Umbrella" in current and exists(var.chk_umb):
        try:
            patched, msg = control.startup_patch(var.path_umb_service, addon_name="Umbrella")
            with open(var.path_umb, 'r') as f:
                data = f.read()
            new_data = None
            if var.client_am in data:
                pass
            else:
                new_data = data.replace(var.umb_client, var.client_am).replace(var.umb_secret, var.secret_am)
            if new_data is not None:
                with open(var.path_umb, 'w') as f:
                    f.write(new_data)
        except Exception as e:
            log_utils.error(f"Umbrella API Failed: {e}")

    '''# ================= Seren =================
    if "Seren" in current and exists(var.chk_seren):
        try:
            patched, msg = control.startup_patch(var.path_seren_service)
            with open(var.path_seren,'r') as f:
                data = f.read()
            new_data = None
            if var.client_am in data:
                pass
            else:
                new_data = data.replace(var.seren_client, var.client_am).replace(var.seren_secret, var.secret_am)
            if new_data is not None:
                with open(var.path_seren, 'w') as f:
                    f.write(new_data)
        except Exception as e:
            log_utils.error(f"Seren API Failed: {e}")

    # ================= Fen =================
    if "Fen" in current and exists(var.chk_fen):
        try:
            patched, msg = control.startup_patch(var.path_fen_service)
            with open(var.path_fen, 'r') as f:
                data = f.read()
            new_data = None
            if var.client_am in data:
                pass
            else:
                new_data = data.replace(var.fen_client, var.client_am).replace(var.fen_secret, var.secret_am)
            if new_data is not None:
                with open(var.path_fen, 'w') as f:
                    f.write(new_data)
        except Exception as e:
            log_utils.error(f"Fen API Failed: {e}")'''

    # ================= POV / The Coalition / Dradis / Genocide / Homelander / Nightwing / Jokers Absolution =================
    patches = (
        ("POV", var.chk_pov, var.path_pov_service, "POV"),
        ("The Coalition", var.chk_coal, var.path_coal_service, "The Coalition"),
        #("Dradis", var.chk_dradis, var.path_dradis_service, "Dradis"),
        ("Genocide", var.chk_genocide, var.path_genocide_service, "Genocide"),
        ("Homelander", var.chk_home, var.path_home_service, "Homelander"),
        ("Nightwing", var.chk_night, var.path_night_service, "Nightwing"),
        ("Jokers Absolution", var.chk_absol, var.path_absol_service, "Jokers Absolution"),
    )

    for name, check_path, service_path, addon_name in patches:
        if name in current and exists(check_path):
            patched, msg = control.startup_patch(service_path, addon_name=addon_name)
        
    # ================= Shadow =================
    if "Shadow" in current and exists(var.chk_shadow):
        try:
            with open(var.path_shadow, 'r') as f:
                data = f.read()
            new_data = None
            if var.client_am in data:
                pass
            else:
                new_data = data.replace(var.shadow_client, var.client_am).replace(var.shadow_secret, var.secret_am)
            if new_data is not None:
                with open(var.path_shadow, 'w') as f:
                    f.write(new_data)
        except Exception as e:
            log_utils.error(f"Shadow API Failed: {e}")

    # ================= Ghost =================
    if "Ghost" in current and exists(var.chk_ghost):
        try:
            with open(var.path_ghost, 'r') as f:
                data = f.read()
            new_data = None
            if var.client_am in data:
                pass
            else:
                new_data = data.replace(var.ghost_client, var.client_am).replace(var.ghost_secret, var.secret_am)
            if new_data is not None:
                with open(var.path_ghost, 'w') as f:
                    f.write(new_data)
        except Exception as e:
            log_utils.error(f"Ghost API Failed: {e}")

    # ================= The Chains =================
    if "The Chains" in current and exists(var.chk_chains):
        try:
            with open(var.path_chains, 'r') as f:
                data = f.read()
            new_data = None
            if var.client_am in data:
                pass
            else:
                new_data = data.replace(var.thechains_client, var.client_am).replace(var.thechains_secret, var.secret_am)
            if new_data is not None:
                with open(var.path_chains, 'w') as f:
                    f.write(new_data)
        except Exception as e:
            log_utils.error(f"The Chains API Failed: {e}")

    # ================= The Crew =================
    if "The Crew" in current and exists(var.chk_crew):
        try:
            patched, msg = control.startup_patch(var.path_crew_service, addon_name="The Crew")
            with open(var.path_crew, 'r') as f:
                data = f.read()
            new_data = None
            if var.client_am in data:
                pass
            else:
                new_data = data.replace(var.crew_client, var.client_am).replace(var.crew_secret, var.secret_am)
            if new_data is not None:
                with open(var.path_crew, 'w') as f:
                    f.write(new_data)
        except Exception as e:
            log_utils.error(f"The Crew API Failed: {e}")

    # ================= SALTS =================
    if "SALTS" in current and exists(var.chk_salts):
        try:
            patched, msg = control.startup_patch(var.path_salts_service, addon_name="SALTS")
            with open(var.path_salts, 'r') as f:
                data = f.read()
            new_data = None
            if var.client_am in data:
                pass
            else:
                new_data = data.replace(var.salts_client, var.client_am).replace(var.salts_secret, var.secret_am)
            if new_data is not None:
                with open(var.path_salts, 'w') as f:
                    f.write(new_data)
        except Exception as e:
            log_utils.error(f"SALTS API Failed: {e}")

    '''# ================= Orion =================
    if "Orion" in current and exists(var.chk_orion):
        try:
            with open(var.path_orion, 'r') as f:
                data = f.read()
            new_data = None
            if var.client_am in data:
                pass
            else:
                new_data = data.replace(var.orion_client, var.client_am).replace(var.orion_secret, var.secret_am)
            if new_data is not None:
                with open(var.path_orion, 'w') as f:
                    f.write(new_data)
        except Exception as e:
            log_utils.error(f"Orion API Failed: {e}")

    # ================= Genesis =================
    if "Genesis" in current and exists(var.chk_gen):
        try:
            with open(var.path_gen, 'r') as f:
                data = f.read()
            new_data = None
            if var.client_am in data:
                pass
            else:
                new_data = data.replace(var.genesis_client, var.client_am).replace(var.genesis_secret, var.secret_am)
            if new_data is not None:
                with open(var.path_gen, 'w') as f:
                    f.write(new_data)
        except Exception as e:
            log_utils.error(f"Genesis API Failed: {e}")

    # ================= Syncher =================
    if "Syncher" in current and exists(var.chk_sync):
        try:
            with open(var.path_sync, 'r') as f:
                data = f.read()
            new_data = None
            if var.client_am in data:
                pass
            else:
                new_data = data.replace(var.syncher_client, var.client_am).replace(var.syncher_secret, var.secret_am)
            if new_data is not None:
                with open(var.path_sync, 'w') as f:
                    f.write(new_data)
        except Exception as e:
            log_utils.error(f"Syncher API Failed: {e}")'''

    # ================= Scrubs V2 =================
    if "Scrubs V2" in current and exists(var.chk_scrubs):
        try:
            patched, msg = control.startup_patch(var.path_scrubs_service, addon_name="Scrubs V2")
            with open(var.path_scrubs, 'r') as f:
                data = f.read()
            new_data = None
            if var.client_am in data:
                pass
            else:
                new_data = data.replace(var.scrubs_client, var.client_am).replace(var.scrubs_secret, var.secret_am)
            if new_data is not None:
                with open(var.path_scrubs, 'w') as f:
                    f.write(new_data)
        except Exception as e:
            log_utils.error(f"Scrubs V2 API Failed: {e}")

    # ================= Gratis Red =================
    if "Gratis Red" in current and exists(var.chk_redg):
        try:
            patched, msg = control.startup_patch(var.path_redg_service, addon_name="Gratis Red")
            with open(var.path_redg, 'r') as f:
                data = f.read()
            new_data = None
            if var.client_am in data:
                pass
            else:
                new_data = data.replace(var.redg_client, var.client_am).replace(var.redg_secret, var.secret_am)
            if new_data is not None:
                with open(var.path_redg, 'w') as f:
                    f.write(new_data)
        except Exception as e:
            log_utils.error(f"Gratis Red API Failed: {e}")

    # ================= TMDbH =================
    if "TMDb Helper" in current and exists(var.chk_tmdbh):
        try:
            patched, msg = control.startup_patch(var.path_tmdbh_service, addon_name="TMDb Helper")
            with open(var.path_tmdbh, 'r') as f:
                data = f.read()
            new_data = None
            if var.client_am in data:
                pass
            else:
                new_data = data.replace(var.tmdbh_client, var.client_am).replace(var.tmdbh_secret, var.secret_am)
            if new_data is not None:
                with open(var.path_tmdbh, 'w') as f:
                    f.write(new_data)
        except Exception as e:
            log_utils.error(f"TMDbH API Failed: {e}")

    '''# ================= Trakt Player =================
    if "Trakt Player" in current and exists(var.chk_tkplay):
        try:
            patched, msg = control.startup_patch(var.path_tkplay_service)
            with open(var.path_tkplay, 'r') as f:
                data = f.read()
            new_data = None
            if var.client_am in data:
                pass
            else:
                new_data = data.replace(var.tkplay_client, var.client_am).replace(var.tkplay_secret, var.secret_am)
            if new_data is not None:
                with open(var.path_tkplay, 'w') as f:
                    f.write(new_data)
        except Exception as e:
            log_utils.error(f"Trakt Player API Failed: {e}")'''

    # ================= Trakt Add-on =================
    if "Trakt Addon" in current and exists(var.chk_trakt):
        try:
            patched, msg = control.startup_patch(var.path_trakt_service, addon_name="Trakt Add-on")
            with open(var.path_trakt, 'r') as f:
                data = f.read()
            new_data = None
            if var.client_am in data:
                pass
            else:
                new_data = data.replace(var.trakt_client_obs_str, var.client_am_obs_str).replace(var.trakt_secret_obs_str, var.secret_am_obs_str)
            if new_data is not None:
                with open(var.path_trakt, 'w') as f:
                    f.write(new_data)
        except Exception as e:
            log_utils.error(f"Trakt Add-on API Failed: {e}")
