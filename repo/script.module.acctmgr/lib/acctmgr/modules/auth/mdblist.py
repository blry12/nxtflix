# -*- coding: utf-8 -*-
"""
	Account Manager
"""
import xbmc, xbmcgui, xbmcaddon
import json
import urllib.parse
import urllib.request
from acctmgr.modules import control

# Variables
mdb_icon = control.joinPath(control.artPath(), 'mdblist.png')
ADDON_ID = "script.module.acctmgr"
ADDON_NAME = "NXTFlix Light"
API_BASE = "https://api.mdblist.com"


class MDBListAuth:
    def __init__(self):
        self.addon = xbmcaddon.Addon(ADDON_ID)

    def _get_setting(self, key):
        try:
            return self.addon.getSetting(key)
        except Exception:
            return ""

    def _set_setting(self, key, value):
        try:
            self.addon.setSetting(key, value if value is not None else "")
            return True
        except Exception as e:
            xbmc.log(f"{ADDON_NAME}: MDBList setSetting failed for [{key}] - {e}", xbmc.LOGERROR)
            return False

    def _request_json(self, url, timeout=10):
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Kodi NXTFlix Light",
                "Accept": "application/json",
            }
        )

        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = getattr(resp, "status", 200)
            body = resp.read().decode("utf-8", "replace")

        try:
            data = json.loads(body) if body else {}
        except Exception:
            data = {}

        return status, data, body

    def fetch_user(self, api_key): # Validate key and return MDBList username
        api_key = (api_key or "").strip()
        if not api_key:
            return False, "Missing API key", None

        url = f"{API_BASE}/user?apikey={urllib.parse.quote(api_key)}"

        try:
            status, data, raw = self._request_json(url)
        except Exception as e:
            xbmc.log(f"{ADDON_NAME}: MDBList request failed - {e}", xbmc.LOGERROR)
            return False, f"Request failed: {e}", None

        if status != 200:
            message = None
            if isinstance(data, dict):
                message = data.get("error") or data.get("message") or data.get("detail")

            if not message:
                message = f"HTTP {status}"

            xbmc.log(
                f"{ADDON_NAME}: MDBList auth failed - status={status} response={raw}",
                xbmc.LOGERROR
            )
            return False, message, None

        username = ""
        if isinstance(data, dict):
            username = (data.get("username") or "").strip()

        if not username:
            xbmc.log(
                f"{ADDON_NAME}: MDBList auth succeeded but no username returned: {raw}",
                xbmc.LOGERROR
            )
            return False, "Username not returned by MDBList", None

        return True, "OK", username

    def authorize(self, api_key=None):
        if not api_key:
            keyboard = xbmc.Keyboard("", "Enter MDBList API Key")
            keyboard.doModal()
            if not keyboard.isConfirmed():
                return False
            api_key = keyboard.getText()

        api_key = (api_key or "").strip()
        if not api_key:
            xbmcgui.Dialog().notification(ADDON_NAME, "MDBList API key is empty", mdb_icon, 3000)
            return False

        ok, msg, username = self.fetch_user(api_key)
        if not ok:
            xbmcgui.Dialog().notification(ADDON_NAME, f"MDBList auth failed: {msg}", mdb_icon, 3000)
            return False

        wrote_key = self._set_setting("mdblist.apikey", api_key)
        wrote_user = self._set_setting("mdblist.username", username)

        if not (wrote_key and wrote_user):
            xbmcgui.Dialog().notification(ADDON_NAME, "MDBList settings write failed", mdb_icon, 3000)
            return False

        xbmc.log(f"{ADDON_NAME}: MDBList authorized successfully - username={username}", xbmc.LOGINFO)
        control.notification(title='NXTFlix Light',message='Successfully Authorized!',icon=mdb_icon)
        return True
