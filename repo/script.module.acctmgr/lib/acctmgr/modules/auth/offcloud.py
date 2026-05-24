# -*- coding: utf-8 -*-
import time
import requests
import xbmc
import xbmcgui
from requests.adapters import HTTPAdapter

from acctmgr.modules import control
from acctmgr.modules import log_utils


# Variables
OFFCLOUD_ICON = control.joinPath(control.artPath(), "offcloud.png")

BASE_HOST = "https://offcloud.com"
API_BASE = f"{BASE_HOST}/api"
OAUTH_DEVICE_CODE_URL = f"{BASE_HOST}/oauth/device/code"
OAUTH_TOKEN_URL = f"{BASE_HOST}/oauth/token"
ACTIVATE_URL = "https://offcloud.com/activate"

TIMEOUT = 10.0

session = requests.Session()
session.mount("https://offcloud.com", HTTPAdapter(max_retries=1, pool_maxsize=20))


class Offcloud:
    def auth(self):
        # Already authorizedcheck
        if control.setting("offcloud.token"):
            control.notification(message="Offcloud is already authorized!",icon=OFFCLOUD_ICON)
            return False

        # Request device code
        try:
            resp = session.post(OAUTH_DEVICE_CODE_URL, timeout=TIMEOUT)
            resp.raise_for_status()
            result = resp.json()

            device_code = result.get("device_code")
            user_code = result.get("user_code")
            verification_uri = result.get("verification_uri") or ACTIVATE_URL
            interval = int(result.get("interval", 5))
            expires_in = int(result.get("expires_in", 600))

            if not device_code or not user_code:
                raise Exception(f"Unexpected response: {result}")

        except Exception as e:
            log_utils.error(f"Offcloud device code request failed: {e}")
            control.notification(message="Offcloud authorization failed!",icon=OFFCLOUD_ICON)
            return False

        # Progress dialog
        progress = xbmcgui.DialogProgress()
        progress.create("Offcloud Authorization",f"Go to:\n{verification_uri}\n\n"f"Enter code:\n{user_code}\n\n""Waiting for authorization...")

        # Poll for access token
        data = {"device_code": device_code,"grant_type": "urn:ietf:params:oauth:grant-type:device_code",}

        token = None
        start = time.monotonic()
        end = start + expires_in

        try:
            while time.monotonic() < end:

                if progress.iscanceled() or xbmc.Monitor().abortRequested():
                    progress.close()
                    control.notification(message="Offcloud authorization cancelled!",icon=OFFCLOUD_ICON)
                    return False

                remaining = int(end - time.monotonic())
                mins, secs = divmod(max(0, remaining), 60)
                pct = int(100 * (1.0 - (remaining / float(expires_in)))) if expires_in else 0

                progress.update(pct,f"Go to: {verification_uri}[CR]"f"Enter code: {user_code}[CR]"f"Remaining: {mins:02d}:{secs:02d}")

                try:
                    r = session.post(OAUTH_TOKEN_URL, json=data, timeout=TIMEOUT)
                    if r.ok:
                        j = r.json()
                        token = j.get("access_token")
                        if token:
                            break
                except Exception:
                    pass

                control.sleep(interval * 1000)

        finally:
            progress.close()

        if not token:
            control.notification(message="Offcloud authorization timed out!",icon=OFFCLOUD_ICON)
            return False

        # Validate token
        try:
            r = session.get(f"{API_BASE}/account/info",params={"key": token},timeout=TIMEOUT)
            r.raise_for_status()
            info = r.json()

            username = (info.get("username") or info.get("email") or str(info.get("user_id", "Offcloud")))

        except Exception as e:
            log_utils.error(f"Offcloud token validation failed: {e}")
            control.notification(message="Offcloud authorization failed (token invalid).",icon=OFFCLOUD_ICON)
            return False

        # Save token & userid
        control.setSetting("offcloud.token", token)
        control.setSetting("offcloud.userid", str(username))

        control.notification(title="NXTFlix Light",message="Successfully Authorized!",icon=OFFCLOUD_ICON)
        return True
