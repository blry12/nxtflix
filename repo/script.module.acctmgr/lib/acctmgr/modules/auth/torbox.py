# -*- coding: utf-8 -*-
import xbmc
import xbmcgui
import json
import urllib.request
import urllib.error
import urllib.parse

from acctmgr.modules import control
from acctmgr.modules import log_utils

# TorBox API
API_BASE = "https://api.torbox.app"
USER_PATH = "/v1/api/user/me"
DEVICE_START_PATH = "/v1/api/user/auth/device/start"
DEVICE_TOKEN_PATH = "/v1/api/user/auth/device/token"
DEVICE_URL = "https://torbox.app/oauth/device"

torbox_icon = control.joinPath(control.artPath(), "torbox.png")
torbox_bdr = control.joinPath(control.addonPath(), "resources", "images", "white.png")
torbox_qr = control.joinPath(control.addonPath(), "resources", "images", "torbox_qr.png")
torbox_bg = control.joinPath(control.addonPath(), "resources", "images", "dialog_background.png")

class TorboxAuthDialog(xbmcgui.WindowXMLDialog):
	def __init__(self, *args, **kwargs):
		self.user_code = kwargs.get("user_code")
		self.bg_image = kwargs.get("bg_image")
		self.qr_image = kwargs.get("qr_image")
		self.bdr_image = kwargs.get("bdr_image")
		self.is_active = True
		super(TorboxAuthDialog, self).__init__()

	def onInit(self):
		self.setProperty("user_code", self.user_code)
		self.setProperty("bg_image", self.bg_image)
		self.setProperty("qr_image", self.qr_image)
		self.setProperty("bdr_image", self.bdr_image)

	def onClick(self, controlId):
		self.is_active = False
		self.close()

	def onAction(self, action):
		if action.getId() in [10, 13, 92]:
			self.is_active = False
			self.close()

class Torbox:
	def auth(self):
		def _json_request(url, data=None, timeout=10):
			headers = {
				"User-Agent": "Kodi/21 acctmgr",
				"Accept": "application/json"
			}

			if data is not None:
				data = json.dumps(data).encode("utf-8")
				headers["Content-Type"] = "application/json"

			req = urllib.request.Request(url, data=data, headers=headers)
			response = urllib.request.urlopen(req, timeout=timeout)
			return json.loads(response.read().decode("utf-8"))

		def _first_value(payload, keys):
			data = payload.get("data") if isinstance(payload, dict) else {}
			for source in (data, payload):
				if not isinstance(source, dict):
					continue
				for key in keys:
					value = source.get(key)
					if value:
						return value
			return ""

		try:
			start_url = f"{API_BASE}{DEVICE_START_PATH}?{urllib.parse.urlencode({'app': 'Account Manager Lite'})}"
			start_payload = _json_request(start_url)

			device_code = _first_value(start_payload, ("device_code", "deviceCode", "device", "code"))
			user_code = _first_value(start_payload, ("user_code", "userCode", "pin", "code"))
			interval = int(_first_value(start_payload, ("interval",)) or 5)

			if not device_code or not user_code:
				log_utils.error(f"TorBox device auth invalid start response: {start_payload}")
				control.notification(message="TorBox Authorization Failed",icon=torbox_icon)
				return False

			dialog = TorboxAuthDialog(
				"torbox_auth.xml",
				str(control.addonPath()),
				"default",
				user_code=user_code,
                                bg_image=torbox_bg,
				qr_image=torbox_qr,
                                bdr_image=torbox_bdr
			)

			dialog.show()

			api = ""

			for i in range(120):
				if not dialog.is_active:
					del dialog
					control.notification(message="TorBox authorization cancelled!",icon=torbox_icon)
					return False

				try:
					token_payload = _json_request(
						f"{API_BASE}{DEVICE_TOKEN_PATH}",
						{"device_code": device_code},
						timeout=3
					)

					api = _first_value(token_payload, ("token", "access_token", "api_key", "apiKey", "api_token", "apiToken"))

					if api:
						dialog.close()
						del dialog
						break

				except urllib.error.HTTPError as e:
					if e.code not in (400, 401, 403, 404):
						try:
							body = e.read().decode("utf-8", errors="ignore")
							log_utils.error(f"TorBox device token HTTP {e.code}: {body}")
						except Exception:
							log_utils.error(f"TorBox device token HTTP {e.code}")
				except Exception as e:
					log_utils.error(f"TorBox device token check failed: {e}")

				xbmc.sleep(interval * 1000)

			if not api:
				if dialog.is_active:
					dialog.close()
				del dialog
				control.notification(message="TorBox Authorization Timed Out",icon=torbox_icon)
				return False

			api = api.strip().replace("\n", "").replace("\r", "")
			if not api:
				control.notification(message="TorBox authorization failed!",icon=torbox_icon)
				return False

			url = f"{API_BASE}{USER_PATH}"
			req = urllib.request.Request(url)

			req.add_header("Authorization", f"Bearer {api}")
			req.add_header("User-Agent", "Kodi/21 acctmgr")
			req.add_header("Accept", "application/json")

			response = urllib.request.urlopen(req, timeout=10)
			payload = json.loads(response.read().decode("utf-8"))

			data = payload.get("data") or {}

			acct_id = data.get("id") or ""
			is_subscribed = data.get("is_subscribed")
			plan = data.get("plan")
			expires = data.get("premium_expires_at")

			# Determine account status
			if is_subscribed is True or expires:
				auth_status = "Premium"
			elif plan == 1:
				auth_status = "Basic"
			else:
				auth_status = "Authorized"

			# Set AML Settings
			control.setSetting("torbox.token", api)
			control.setSetting("torbox.acct_id", str(acct_id))
			control.setSetting("torbox.auth_status", auth_status)

			control.notification(title="NXTFlix Light",message="Successfully Authorized!",icon=torbox_icon)

			return True

		except urllib.error.HTTPError as e:
			if e.code == 401:
				control.notification(message="TorBox Authorization Failed (Invalid API Key)",icon=torbox_icon)
			elif e.code == 403:
				control.notification(message="TorBox Authorization Failed (Forbidden)",icon=torbox_icon)
			else:
				control.notification(message=f"TorBox Authorization Failed (HTTP {e.code})",icon=torbox_icon)

			try:
				body = e.read().decode("utf-8", errors="ignore")
				log_utils.error(f"TorBox auth HTTP {e.code}: {body}")
			except Exception:
				log_utils.error(f"TorBox auth HTTP {e.code}")

			return False

		except Exception as e:
			log_utils.error(f"TorBox authorization failed: {e}")
			control.notification(message="TorBox Authorization Failed",icon=torbox_icon)
			return False

	def revoke(self):
		if not control.okDialog("TorBox", "Revoke TorBox Authorization?"):
			return

		control.setSetting("torbox.token", "")
		control.setSetting("torbox.acct_id", "")
		control.setSetting("torbox.auth_status", "")

		control.notification("TorBox Authorization Revoked",icon=torbox_icon)
