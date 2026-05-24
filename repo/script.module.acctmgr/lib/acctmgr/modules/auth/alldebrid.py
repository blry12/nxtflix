# -*- coding: utf-8 -*-
import xbmc
import requests
from acctmgr.modules import control
from acctmgr.modules import log_utils

# Variables
base_url_v4  = 'https://api.alldebrid.com/v4/'
base_url_41  = 'https://api.alldebrid.com/v4.1/'
user_agent = 'Account%20Manager%20for%20Kodi'
ad_icon = control.joinPath(control.artPath(), 'alldebrid.png')

class AllDebrid:
	name = "AllDebrid"

	def __init__(self):
		self.token = control.setting('alldebrid.token')
		self.timeout = 15.0
		self.pin = None
		self.check_url = None
		self.user_url = None

	def _headers(self):
		return {
			"User-Agent": user_agent,
			"Authorization": f"Bearer {self.token}" if self.token else ""
		}

	def _get(self, endpoint, params=None):
		if not self.token:
			return None

		url = base_url_41 + endpoint
		params = params or {}

		try:
			r = requests.get(
				url,
				headers=self._headers(),
				params=params,
				timeout=self.timeout
			)
			result = r.json()
			if result.get("status") == "success":
				return result.get("data")
		except Exception as e:
			log_utils.error(f"AllDebrid API GET failed: {e}")
		return None

	def auth(self):
		import time

		self.token = ""
		self.pin = None
		self.check_url = None
		self.user_url = None

		# Request PIN
		try:
			r = requests.get(
				base_url_v4 + "pin/get",
				params={"agent": user_agent},
				timeout=self.timeout
			)
			payload = r.json()
		except Exception as e:
			log_utils.error(f"AllDebrid pin/get request failed: {e}")
			return False

		if payload.get("status") != "success":
			return False

		data = payload.get("data", {})
		self.pin = data.get("pin")
		self.check_url = data.get("check_url")
		self.user_url = data.get("user_url") or "https://alldebrid.com/pin/"

		if not self.pin or not self.check_url:
			return False

		# Show progress dialog
		control.progressDialog.create(control.lang(40056))
		control.progressDialog.update(
			0,
			control.progress_line % (
				control.lang(32513) % self.user_url,
				control.lang(32514) % self.pin,
				'',
			),
		)

		start = time.time()
		timeout = data.get("expires_in", 300)

		while not self.token and time.time() - start < timeout:
			if control.progressDialog.iscanceled():
				break
			self.auth_loop()
			time.sleep(5)

		try:
			control.progressDialog.close()
		except Exception as e:
			log_utils.error(f"AllDebrid progressDialog close failed: {e}")

		if not self.token:
			return False

		account = self.account_info()
		if account and "user" in account:
			control.setSetting(
				"alldebrid.username",
				str(account["user"].get("username", ""))
			)

		control.notification(title='NXTFlix Light',message='Successfully Authorized!',icon=ad_icon)
		return True

	def auth_loop(self):
		try:
			r = requests.get(self.check_url, timeout=self.timeout)
			result = r.json()
		except Exception as e:
			log_utils.error(f"AllDebrid pin/check request failed: {e}")
			return

		data = result.get("data", {}) if isinstance(result, dict) else {}

		api_key = data.get("apikey")
		if api_key:
			self.token = str(api_key)
			control.setSetting("alldebrid.token", self.token)
			xbmc.log("AM-LITE: AllDebrid token acquired", xbmc.LOGINFO)

	def revoke(self):
		control.setSetting("alldebrid.username", "")
		control.setSetting("alldebrid.token", "")

	def account_info(self):
		return self._get("user")

	def account_info_to_dialog(self):
		from datetime import datetime
		try:
			data = self.account_info()
			if not data or "user" not in data:
				return

			user = data["user"]
			username = user.get("username", "")
			email = user.get("email", "")
			status = "Premium" if user.get("isPremium") else "Not Active"
			expires = datetime.fromtimestamp(user["premiumUntil"])
			days_remaining = (expires - datetime.today()).days

			items = [
				control.lang(40036) % username,
				control.lang(40035) % email,
				control.lang(40037) % status,
				control.lang(40041) % expires,
				control.lang(40042) % days_remaining,
			]
			return control.selectDialog(items, "AllDebrid")
		except Exception as e:
			log_utils.error(f"AllDebrid account_info_to_dialog failed: {e}")
			return
