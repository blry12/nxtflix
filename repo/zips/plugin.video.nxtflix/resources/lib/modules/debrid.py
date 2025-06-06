# -*- coding: utf-8 -*-
from caches.debrid_cache import debrid_cache
from apis.real_debrid_api import RealDebridAPI
from apis.premiumize_api import PremiumizeAPI
from apis.alldebrid_api import AllDebridAPI
from modules import kodi_utils
from modules.utils import make_thread_list
from modules.settings import enabled_debrids_check, authorized_debrid_check
# logger = kodi_utils.logger

show_busy_dialog, hide_busy_dialog, notification = kodi_utils.show_busy_dialog, kodi_utils.hide_busy_dialog, kodi_utils.notification
Thread, get_setting = kodi_utils.Thread, kodi_utils.get_setting
debrid_list = [('Real-Debrid', 'rd'), ('Premiumize.me', 'pm'), ('AllDebrid', 'ad')]
debrid_list_modules = [('Real-Debrid', RealDebridAPI), ('Premiumize.me', PremiumizeAPI), ('AllDebrid', AllDebridAPI)]

def debrid_enabled():
	return [i[0] for i in debrid_list if enabled_debrids_check(i[1])]

def debrid_authed():
	return [i[0] for i in debrid_list if authorized_debrid_check(i[1])]

def manual_add_magnet_to_cloud(params):
	show_busy_dialog()
	function = [i[1] for i in debrid_list_modules if i[0] == params['provider']][0]
	result = function().create_transfer(params['magnet_url'])
	function().clear_cache()
	hide_busy_dialog()
	if result == 'failed': notification(32490)
	else: notification(32576)

def query_local_cache(hash_list):
	return debrid_cache.get_many(hash_list) or []

def add_to_local_cache(hash_list, debrid):
	debrid_cache.set_many(hash_list, debrid)

def cached_check(hash_list, cached_hashes, debrid):
	cached_list = [i[0] for i in cached_hashes if i[1] == debrid and i[2] == 'True']
	unchecked_list = [i for i in hash_list if not any([h for h in cached_hashes if h[0] == i and h[1] == debrid])]
	return cached_list, unchecked_list

def RD_check(hash_list, cached_hashes):
	return hash_list

def PM_check(hash_list, cached_hashes):
	cached_hashes, unchecked_hashes = cached_check(hash_list, cached_hashes, 'pm')
	if unchecked_hashes:
		results = PremiumizeAPI().check_cache(unchecked_hashes)
		if results:
			cached_append = cached_hashes.append
			process_list = []
			process_append = process_list.append
			try:
				results = results['response']
				for c, h in enumerate(unchecked_hashes):
					cached = 'False'
					try:
						if results[c] is True:
							cached_append(h)
							cached = 'True'
					except: pass
					process_append((h, cached))
			except:
				for i in unchecked_hashes: process_append((i, 'False'))
			add_to_local_cache(process_list, 'pm')
	return cached_hashes

def AD_check(hash_list, cached_hashes):
	cached_hashes, unchecked_hashes = cached_check(hash_list, cached_hashes, 'ad')
	if unchecked_hashes:
		results = AllDebridAPI().check_cache(unchecked_hashes)
		if results:
			cached_append = cached_hashes.append
			process_list = []
			process_append = process_list.append
			try:
				results = results['magnets']
				for i in results:
					cached = 'False'
					try:
						if i['instant'] == True:
							cached_append(i['hash'])
							cached = 'True'
					except: pass
					process_append((i['hash'], cached))
			except:
				for i in unchecked_hashes: process_append((i, 'False'))
			add_to_local_cache(process_list, 'ad')
	return cached_hashes
