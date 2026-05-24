# -*- coding: utf-8 -*-
import xbmc, xbmcaddon
import os
import requests
import time
from acctmgr.modules import control
from acctmgr.modules import log_utils

# Variables
trakt_icon = control.joinPath(control.artPath(), 'trakt.png')

class Trakt():
	def __init__(self):
		self.api_endpoint = 'https://api.trakt.tv/%s'
		self.client_id = self.traktClientID()
		self.client_secret = self.traktClientSecret()
		self.expires_at = control.setting('trakt.expires')
		self.token = control.setting('trakt.token')

	def call(self, path, data=None, with_auth=True, method=None, return_str=False, suppress_error_notification=False):
		try:
			def error_notification(line1, error):
				if suppress_error_notification: return
				return control.notification(title='default', message='%s: %s' % (line1, error), icon=trakt_icon)

			def send_query():
				resp = None
				if with_auth:
					try:
						try:
							expires_at = float(control.setting('trakt.expires') or 0)
						except Exception as e:
							log_utils.error(f"Error converting expires_at to float: {e}")
							expires_at = 0

						if expires_at > 0 and time.time() >= expires_at:
							if not self.refresh_token():
								return None
					except Exception as e:
						log_utils.error(f"Error refreshing token: {e}")
						pass
					headers['Authorization'] = 'Bearer ' + (control.setting('trakt.token') or self.token)

				try:
					request_method = (method or ('POST' if data is not None else 'GET')).upper()
					if request_method == 'POST':
						resp = requests.post(self.api_endpoint % path, json=data, headers=headers, timeout=timeout)
					else:
						resp = requests.get(self.api_endpoint % path, headers=headers, timeout=timeout)
				except requests.exceptions.RequestException as e:
					error_notification('Trakt Error', str(e))
				except Exception as e:
					error_notification('', str(e))
				return resp

			timeout = 15.0
			headers = {'Content-Type': 'application/json', 'trakt-api-version': '2', 'trakt-api-key': self.traktClientID()}
			response = send_query()

			if not response:
				return None

			response.encoding = 'utf-8'
			if return_str:
				return response

			if response.status_code not in (200, 201):
				try:
					error_result = response.json()
				except Exception:
					try:
						error_result = response.text
					except Exception:
						error_result = ''
				log_utils.error(f"Trakt API {path} failed: HTTP {response.status_code} - {error_result}")
				return None

			try:
				result = response.json()
			except Exception as e:
				log_utils.error(f"Error parsing JSON response: {e}")
				result = None

			return result
		except Exception as e:
			log_utils.error(f"Trakt call failed: {e}")

	def get_device_code(self):
		data = {'client_id': self.traktClientID()}
		return self.call("oauth/device/code", data=data, with_auth=False, method='POST')

	def get_device_token(self, device_codes):
		try:
			data = {
				"code": device_codes["device_code"],
				"client_id": self.traktClientID(),
				"client_secret": self.traktClientSecret()
			}
			start = time.time()
			expires_in = int(device_codes.get('expires_in', 600))
			interval = max(int(device_codes.get('interval', 5)), 1)
			verification_url = control.lang(32513) % str(device_codes['verification_url'])
			user_code = control.lang(32514) % str(device_codes['user_code'])
			control.progressDialog.create(control.lang(32073), control.progress_line % (verification_url, user_code, ''))
			try:
				time_passed = 0
				while not control.progressDialog.iscanceled() and time_passed < expires_in:
					try:
						headers = {
							'Content-Type': 'application/json',
							'trakt-api-version': '2',
							'trakt-api-key': self.traktClientID()
						}
						response = requests.post(
							self.api_endpoint % "oauth/device/token",
							json=data,
							headers=headers,
							timeout=15.0
						)

						if response.status_code == 200:
							token_data = response.json()
							if token_data and token_data.get("access_token") and token_data.get("refresh_token"):
								return token_data
							return None

						if response.status_code == 400:
							try:
								error_data = response.json() or {}
							except Exception:
								error_data = {}

							error_code = error_data.get('error', '')
							if error_code == 'slow_down':
								interval += 5
							elif error_code in ('authorization_pending', 'authorization_declined', 'expired_token', 'access_denied'):
								if error_code in ('authorization_declined', 'expired_token', 'access_denied'):
									return None

							progress = int(100 * time_passed / expires_in)
							control.progressDialog.update(progress)
							control.sleep(interval * 1000)
						else:
							try:
								log_utils.log('Request Error: %s' % response.text, __name__, log_utils.LOGDEBUG)
							except Exception:
								pass
							progress = int(100 * time_passed / expires_in)
							control.progressDialog.update(progress)
							control.sleep(interval * 1000)

					except requests.RequestException as e:
						log_utils.log('Request Error: %s' % str(e), __name__, log_utils.LOGDEBUG)
						progress = int(100 * time_passed / expires_in)
						control.progressDialog.update(progress)
						control.sleep(interval * 1000)

					time_passed = time.time() - start
			finally:
				control.progressDialog.close()
			return None
		except Exception as e:
			log_utils.error(f"Trakt device token flow failed: {e}")

	def refresh_token(self):
		data = {
			"client_id": self.traktClientID(),
			"client_secret": self.traktClientSecret(),
			"redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
			"grant_type": "refresh_token",
			"refresh_token": control.setting('trakt.refresh')
		}

		response = self.call("oauth/token", data=data, with_auth=False, method='POST', return_str=True)
		try:
			code = str(response.status_code)
		except Exception as e:
			log_utils.error(f"Error extracting code: {e}")
			code = ''

		if not response:
			log_utils.log('Temporary Trakt Server Problems', level=log_utils.LOGWARNING)
			control.notification(title=32315, message=32685)
			return False

		try:
			response_text = response.text or ''
		except Exception:
			response_text = ''

		if code.startswith('5') or '<html' in response_text.lower():
			log_utils.log('Temporary Trakt Server Problems', level=log_utils.LOGWARNING)
			control.notification(title=32315, message=32685)
			return False
		elif response and code in ['423']:
			log_utils.log('Locked User Account - Contact Trakt Support', level=log_utils.LOGWARNING)
			control.notification(title=32315, message=32686)
			return False

		if response and code == '200':
			try:
				response = response.json()
			except Exception as e:
				log_utils.error(f"Error parsing refresh token response: {e}")
				return False

			if 'error' in response and response['error'] == 'invalid_grant':
				log_utils.log('Please Re-Authorize your Trakt Account', level=log_utils.LOGWARNING)
				control.notification(title=32315, message=32687)
				return False

			traktToken = response["access_token"]
			traktRefresh = response["refresh_token"]
			traktExpires = int(time.time()) + 86400
			control.setSetting('trakt.token', traktToken)
			control.setSetting('trakt.refresh', traktRefresh)
			control.setSetting('trakt.expires', str(traktExpires))
			self.token = traktToken
			self.expires_at = str(traktExpires or '')
			return True

		return False

	def auth(self):
		try:
			code = self.get_device_code()
			token = self.get_device_token(code)
			if token and token.get("access_token") and token.get("refresh_token"):
				expires_at = int(time.time()) + 86400
				control.setSetting('trakt.expires', str(expires_at))
				control.setSetting('trakt.token', token["access_token"])
				control.setSetting('trakt.refresh', token["refresh_token"])
				self.expires_at = str(expires_at)
				self.token = token["access_token"]
				control.sleep(1000)
				try:
					user = self.call("users/me", with_auth=True)
					control.setSetting('trakt.username', str(user['username']))
				except Exception as e:
					log_utils.error(f"Error fetching user info: {e}")
					pass
				control.notification(title='NXTFlix Light',message='Successfully Authorized!',icon=trakt_icon)
				return True
			control.notification(message=40075, icon=trakt_icon)
			return False
		except Exception as e:
			log_utils.error(f"Trakt auth failed: {e}")

	def revoke(self):
		data = {"token": control.setting('trakt.token')}
		try:
			self.call("oauth/revoke", data=data, with_auth=False, method='POST')
		except Exception as e:
			log_utils.error(f"Trakt revoke failed: {e}")
			pass
		control.setSetting('trakt.username', '')
		control.setSetting('trakt.expires', '')
		control.setSetting('trakt.token', '')
		control.setSetting('trakt.refresh', '')
		control.dialog.ok(control.lang(32315), control.lang(32314))

	def account_info(self):
		response = self.call("users/me", with_auth=True)
		return response

	def extended_account_info(self):
		account_info = self.call("users/settings", with_auth=True)

		if not account_info or not isinstance(account_info, dict) or 'user' not in account_info or 'ids' not in account_info.get('user', {}):
			try:
				if self.refresh_token():
					account_info = self.call("users/settings", with_auth=True)
			except Exception as e:
				log_utils.error(f"Trakt account settings retry failed: {e}")

		if not account_info or not isinstance(account_info, dict):
			return None, None
		if 'user' not in account_info or 'ids' not in account_info.get('user', {}):
			return None, None

		slug = account_info['user']['ids'].get('slug')
		if not slug:
			return None, None

		stats = self.call("users/%s/stats" % slug, with_auth=True)

		if not stats or not isinstance(stats, dict):
			try:
				if self.refresh_token():
					stats = self.call("users/%s/stats" % slug, with_auth=True)
			except Exception as e:
				log_utils.error(f"Trakt stats retry failed: {e}")

		if not stats or not isinstance(stats, dict):
			return None, None

		return account_info, stats

	def account_info_to_dialog(self):
		from datetime import datetime, timedelta
		try:
			account_info, stats = self.extended_account_info()
			if not account_info or not stats:
				control.dialog.ok(control.lang(32315), 'Failed to retrieve Trakt account information.')
				return

			username = account_info['user']['username']
			timezone = account_info['account']['timezone']
			joined = control.jsondate_to_datetime(account_info['user']['joined_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
			private = account_info['user']['private']
			vip = account_info['user']['vip']
			if vip:
				vip = '%s Years' % str(account_info['user']['vip_years'])

			total_given_ratings = stats['ratings']['total']

			movies_collected = stats['movies']['collected']
			movies_watched = stats['movies']['watched']
			movie_minutes = stats['movies']['minutes']

			if movie_minutes == 0:
				movies_watched_minutes = ['0 days', '0:00:00']
			elif movie_minutes < 1440:
				movies_watched_minutes = ['0 days', "{:0>8}".format(str(timedelta(minutes=movie_minutes)))]
			else:
				movies_watched_minutes = ("{:0>8}".format(str(timedelta(minutes=movie_minutes)))).split(', ')

			movies_watched_minutes = control.lang(40071) % (
				movies_watched_minutes[0],
				movies_watched_minutes[1].split(':')[0],
				movies_watched_minutes[1].split(':')[1]
			)

			shows_collected = stats['shows']['collected']
			shows_watched = stats['shows']['watched']

			episodes_watched = stats['episodes']['watched']
			episode_minutes = stats['episodes']['minutes']

			if episode_minutes == 0:
				episodes_watched_minutes = ['0 days', '0:00:00']
			elif episode_minutes < 1440:
				episodes_watched_minutes = ['0 days', "{:0>8}".format(str(timedelta(minutes=episode_minutes)))]
			else:
				episodes_watched_minutes = ("{:0>8}".format(str(timedelta(minutes=episode_minutes)))).split(', ')

			episodes_watched_minutes = control.lang(40071) % (
				episodes_watched_minutes[0],
				episodes_watched_minutes[1].split(':')[0],
				episodes_watched_minutes[1].split(':')[1]
			)

			heading = control.lang(32315)
			items = []
			items += [control.lang(40036) % username]
			items += [control.lang(40063) % timezone]
			items += [control.lang(40064) % joined]
			items += [control.lang(40065) % private]
			items += [control.lang(40066) % vip]
			items += [control.lang(40067) % str(total_given_ratings)]
			items += [control.lang(40068) % (movies_collected, movies_watched, movies_watched_minutes)]
			items += [control.lang(40069) % (shows_collected, shows_watched)]
			items += [control.lang(40070) % (episodes_watched, episodes_watched_minutes)]

			return control.selectDialog(items, heading)
		except Exception as e:
			log_utils.error(f"Trakt account dialog failed: {e}")
			return

	def traktClientID(self):
		traktId = 'ce7457fe1e42f09919b57171e9196109717474bad5b13b2a70959aef2f8e5624'
		return traktId

	def traktClientSecret(self):
		traktSecret = '004d641c35178c7d3c5798313919bec181e9a162bc84f16a2e78dc82a37150db'
		return traktSecret
