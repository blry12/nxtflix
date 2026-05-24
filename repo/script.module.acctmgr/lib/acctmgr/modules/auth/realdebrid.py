# -*- coding: utf-8 -*-
import json
import requests
import xbmc
import xbmcaddon
import xbmcgui
from requests.adapters import HTTPAdapter
from acctmgr.modules import control
from acctmgr.modules import log_utils

# Variables
FormatDateTime = "%Y-%m-%dT%H:%M:%S.%fZ"
rest_base_url = 'https://api.real-debrid.com/rest/1.0/'
oauth_base_url = 'https://api.real-debrid.com/oauth/v2/'
device_code_url = 'device/code?%s'
credentials_url = 'device/credentials?%s'
rd_icon = control.joinPath(control.artPath(), 'realdebrid.png')

class RealDebrid:
	name = "Real-Debrid"

	def __init__(self):
		self.token = control.setting('realdebrid.token')
		self.client_ID = control.setting('realdebrid.client_id')
		if self.client_ID == '':
			self.client_ID = 'X245A4XAIBGVM'
		self.secret = control.setting('realdebrid.secret')
		self.device_code = ''
		self.auth_timeout = 0
		self.auth_step = 0

	def _get(self, url, fail_check=False, token_ck=False):
		try:
			original_url = url
			url = rest_base_url + url
			if self.token == '':
				log_utils.log('No Real Debrid Token Found', __name__, log_utils.LOGDEBUG)
				return None
			if '?' not in url:
				url += "?auth_token=%s" % self.token
			else:
				url += "&auth_token=%s" % self.token
			response = requests.get(url, timeout=15).json()
			if 'bad_token' in str(response) or 'Bad Request' in str(response):
				if not fail_check:
					if self.refresh_token() and token_ck:
						return
					response = self._get(original_url, fail_check=True)
			return response
		except Exception as e:
			log_utils.error(f"RealDebrid GET failed: {e}")
		return None

	def _post(self, url, data):
		original_url = url
		url = rest_base_url + url
		if self.token == '':
			log_utils.log('No Real Debrid Token Found', __name__, log_utils.LOGDEBUG)
			return None
		if '?' not in url:
			url += "?auth_token=%s" % self.token
		else:
			url += "&auth_token=%s" % self.token
		response = requests.post(url, data=data, timeout=15).text
		if 'bad_token' in response or 'Bad Request' in response:
			self.refresh_token()
			response = self._post(original_url, data)
		elif 'error' in response:
			response = json.loads(response)
			control.notification(title='default', message=response.get('error'), icon=rd_icon)
			return None
		try:
			return json.loads(response)
		except Exception as e:
			log_utils.error(f"RealDebrid POST failed to parse response: {e}")
			return response

	def auth_loop(self):
		control.sleep(self.auth_step * 1000)
		url = 'client_id=%s&code=%s' % (self.client_ID, self.device_code)
		url = oauth_base_url + credentials_url % url
		try:
			response = json.loads(requests.get(url).text)
		except Exception as e:
			log_utils.error(f"RealDebrid auth_loop failed: {e}")
			return

		if 'error' in response:
			return
		else:
			try:
				control.progressDialog.close()
				self.client_ID = response['client_id']
				self.secret = response['client_secret']
			except Exception as e:
				log_utils.error(f"RealDebrid auth_loop response handling failed: {e}")
				control.okDialog(title='default', message=control.lang(40019))
			return

	def auth(self):
		import time

		self.secret = ''
		self.client_ID = 'X245A4XAIBGVM'
		self.device_code = ''
		self.auth_timeout = 0
		self.auth_step = 0

		try:
			url = 'client_id=%s&new_credentials=yes' % self.client_ID
			url = oauth_base_url + device_code_url % url
			response = json.loads(requests.get(url).text)
		except Exception as e:
			log_utils.error(f"RealDebrid device code request failed: {e}")
			control.notification(title='default', message=control.lang(40019), icon=rd_icon)
			return False

		try:
			user_code = response['user_code']
			self.device_code = response['device_code']
			self.auth_timeout = int(response['expires_in'])
			self.auth_step = int(response['interval'])
		except Exception as e:
			log_utils.error(f"RealDebrid device code parse failed: {e}")
			return False

		try:
			control.progressDialog.create(control.lang(40055))
		except Exception as e:
			log_utils.error(f"RealDebrid progress dialog creation failed: {e}")
			control.progressDialog.create("Real-Debrid Authorization")

		control.progressDialog.update(
			-1,
			control.progress_line % (control.lang(32513) % 'https://real-debrid.com/device',
									 control.lang(32514) % user_code, '')
		)

		start = time.time()
		timeout = self.auth_timeout or 300

		while self.secret == '':
			if control.progressDialog.iscanceled():
				try:
					control.progressDialog.close()
				except Exception as e:
					log_utils.error(f"RealDebrid progress dialog close failed: {e}")
				return False

			if time.time() - start > timeout:
				try:
					control.progressDialog.close()
				except Exception as e:
					log_utils.error(f"RealDebrid progress dialog close failed (timeout): {e}")
				control.notification('Real-Debrid', 'Authorization timed out', icon=rd_icon)
				return False

			self.auth_loop()

		try:
			control.progressDialog.close()
		except Exception as e:
			log_utils.error(f"RealDebrid progress dialog close failed: {e}")

		success, error = self.get_token()
		if not success:
			return False

		control.notification(title='NXTFlix Light',message='Successfully Authorized!',icon=rd_icon)
		return True

	def account_info(self):
		return self._get('user')

	def account_info_to_dialog(self):
		from datetime import datetime
		import time
		try:
			userInfo = self.account_info()
			try:
				expires = datetime.strptime(userInfo['expiration'], FormatDateTime)
			except Exception as e:
				log_utils.error(f"RealDebrid date parse failed: {e}")
				expires = datetime(*(time.strptime(userInfo['expiration'], FormatDateTime)[0:6]))
			days_remaining = (expires - datetime.today()).days
			expires = expires.strftime("%A, %B %d, %Y")
			items = []
			items += [control.lang(40035) % userInfo['email']]
			items += [control.lang(40036) % userInfo['username']]
			items += [control.lang(40037) % userInfo['type'].capitalize()]
			items += [control.lang(40041) % expires]
			items += [control.lang(40042) % days_remaining]
			items += [control.lang(40038) % userInfo['points']]
			return control.selectDialog(items, 'Real-Debrid')
		except Exception as e:
			log_utils.error(f"RealDebrid account dialog failed: {e}")
		return

	def refresh_token(self):
		try:
			self.client_ID = control.setting('realdebrid.client_id')
			self.secret = control.setting('realdebrid.secret')
			self.device_code = control.setting('realdebrid.refresh')
			if not self.client_ID or not self.secret or not self.device_code:
				return False
			log_utils.log(
				'Refreshing Expired Real Debrid Token: | %s | %s |' % (self.client_ID, self.device_code),
				__name__, log_utils.LOGDEBUG
			)
			success, error = self.get_token()
			if not success:
				if not 'Temporarily Down For Maintenance' in str(error):
					if error and any(value == error.get('error_code') for value in [9, 12, 13, 14]):
						self.revoke()
						control.notification(message='Real-Debrid Auth revoked due to:  %s' % error.get('error'), icon=rd_icon)
				log_utils.log('Unable to Refresh Real Debrid Token: %s' % (error.get('error') if error else ''), level=log_utils.LOGWARNING)
				return False
			else:
				log_utils.log('Real Debrid Token Successfully Refreshed', level=log_utils.LOGDEBUG)
				return True
		except Exception as e:
			log_utils.error(f"RealDebrid refresh failed: {e}")
			return False

	def get_token(self):
		try:
			url = oauth_base_url + 'token'
			postData = {
				'client_id': self.client_ID,
				'client_secret': self.secret,
				'code': self.device_code,
				'grant_type': 'http://oauth.net/grant_type/device/1.0'
			}
			response = requests.post(url, data=postData)

			if '[204]' in str(response):
				return False, str(response)
			if 'Temporarily Down For Maintenance' in response.text:
				control.notification(message='Real-Debrid Temporarily Down For Maintenance', icon=rd_icon)
				log_utils.log('Real-Debrid Temporarily Down For Maintenance', level=log_utils.LOGWARNING)
				return False, response.text
			else:
				response = response.json()

			if 'error' in str(response):
				log_utils.log('response=%s' % str(response), __name__)
				message = response.get('error')
				control.notification(message=message, icon=rd_icon)
				log_utils.log('Real-Debrid Error:  %s' % message, level=log_utils.LOGWARNING)
				return False, response

			self.token = response['access_token']
			control.sleep(500)
			account_info = self.account_info()
			username = account_info['username']
			control.setSetting('realdebrid.username', username)
			control.setSetting('realdebrid.client_id', self.client_ID)
			control.setSetting('realdebrid.secret', self.secret)
			control.setSetting('realdebrid.token', self.token)
			control.setSetting('realdebrid.refresh', response['refresh_token'])
			return True, None
		except Exception as e:
			log_utils.error(f'Real Debrid Authorization Failed: {e}')
			return False, None

	def revoke(self):
		try:
			control.setSetting('realdebrid.client_id', '')
			control.setSetting('realdebrid.secret', '')
			control.setSetting('realdebrid.token', '')
			control.setSetting('realdebrid.refresh', '')
			control.setSetting('realdebrid.username', '')
			control.dialog.ok(control.lang(40058), control.lang(32314))
		except Exception as e:
			log_utils.error(f"RealDebrid revoke failed: {e}")
