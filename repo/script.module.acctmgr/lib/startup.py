# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcaddon, xbmcvfs
import os
import time
import json
import hashlib

from acctmgr.modules import var
from acctmgr.modules import control
from acctmgr.modules import log_utils

def am_masters(): # NXTFlix Light token variables
	acctmgr = xbmcaddon.Addon("script.module.acctmgr")
	mdb_master_token = acctmgr.getSetting("mdblist.apikey")
	rd_master_token = acctmgr.getSetting("realdebrid.token")
	pm_master_token = acctmgr.getSetting("premiumize.token")
	ad_master_token = acctmgr.getSetting("alldebrid.token")
	tb_master_token = acctmgr.getSetting("torbox.token")
	#ed_master_token = acctmgr.getSetting("easydebrid.token")
	#oc_master_token = acctmgr.getSetting("offcloud.token")
	en_master_user = acctmgr.getSetting("easynews.username")
	en_master_pass = acctmgr.getSetting("easynews.password")

	return mdb_master_token, rd_master_token, pm_master_token, ad_master_token, tb_master_token, en_master_user, en_master_pass

mdb_master_token, rd_master_token, pm_master_token, ad_master_token, tb_master_token, en_master_user, en_master_pass = am_masters()

def ScraperCheck(): # Check for installed scraper packages and update AML settings accordingly
	for addon_id, setting_id in (
		('script.module.cocoscrapers',   "ext.provider_coco"),
                ('script.module.gearsscrapers',  "ext.provider_gears"),
		('script.module.magneto',        "ext.provider_mag"),
		('script.module.viperscrapers',  "ext.provider_vip"),
	):
		value = 'true' if xbmc.getCondVisibility(f'System.HasAddon({addon_id})') else 'false'
		control.setSetting(setting_id, value)
		
def am_trakt_startup_begin(): # Mark Trakt startup as NOT ready immediately on every Kodi startup.
	try:
		acctmgr = xbmcaddon.Addon("script.module.acctmgr")
		acctmgr.setSetting("am_trakt_ready", "false")
		acctmgr.setSetting("am_last_prepare", "0")
		xbmc.log('NXTFlix Light: Trakt startup state set to NOT READY', xbmc.LOGINFO)
	except Exception:
		log_utils.error("NXTFlix Light Trakt startup begin FAILED")

def am_trakt_startup_complete(): # Mark Trakt startup as READY only after refresh/sync has completed safely.
	try:
		acctmgr = xbmcaddon.Addon("script.module.acctmgr")
		acctmgr.setSetting("am_last_prepare", str(int(time.time())))
		acctmgr.setSetting("am_trakt_ready", "true")
		xbmc.log('NXTFlix Light: Trakt startup state set to READY', xbmc.LOGINFO)
	except Exception:
		log_utils.error("NXTFlix Light Trakt startup complete FAILED")

def am_trakt_startup_fail(): # Leave startup state as NOT ready when refresh/sync fails.
	try:
		acctmgr = xbmcaddon.Addon("script.module.acctmgr")
		acctmgr.setSetting("am_trakt_ready", "false")
		acctmgr.setSetting("am_last_prepare", "0")
		xbmc.log('NXTFlix Light: Trakt startup FAILED - remaining NOT READY', xbmc.LOGINFO)
	except Exception:
		log_utils.error("NXTFlix Light Trakt startup fail FAILED")

def startup_wait(timeout=30): # Wait until Kodi finishes loading addons/services
	start = time.time()
	monitor = xbmc.Monitor()

	while not monitor.abortRequested():
		if time.time() - start > timeout:
			break
		xbmc.sleep(500)

def get_trakt_token(): # Read current NXTFlix Light token
	try:
		return control.setting('trakt.token') or ''
	except Exception:
		return ''

def ensure_defaults(): # Check if Trakt is authed. If not, ensure API keys/services are set to default.
	try:
		token = get_trakt_token()
		if not token:
			xbmc.log('NXTFlix Light: No Trakt auth found - resetting services to defaults', xbmc.LOGINFO)
			control.unpatch_all_services()
			#control.apply_default_trakt_api_keys_db() # NO LONGER USED (See control.py)
			control.apply_default_trakt_api_keys()
			return False
		return True
	except Exception:
		log_utils.error("NXTFlix Light ensure_defaults at startup FAILED")
		return False
	
def get_trakt_expires(): # Read trakt expires
	try:
		raw = control.setting('trakt.expires') or '0'
		expires = int(float(raw))
	except Exception:
		expires = 0

	now = int(time.time())

	if expires > 2000000000000:
		expires = int(expires / 1000)

	if 0 < expires < 1000000000:
		expires = now + expires

	if expires > 0:
		control.setSetting('trakt.expires', str(expires))

	return expires

def trakt_refresh(): # Refresh Trakt token if expired or near expiry
	token = get_trakt_token()
	if not token:
		xbmc.log('NXTFlix Light: No Trakt token present - skipping refresh', xbmc.LOGINFO)
		return 'missing'

	now = int(time.time())
	expires = get_trakt_expires()

	if expires > 0 and now < (expires - 4500): # Skip refresh if token is still valid with more than 1.25hrs remaining
		return 'valid'

	xbmc.log('NXTFlix Light: Trakt token expired or near expiry - refreshing', xbmc.LOGINFO)

	try:
		from acctmgr.modules.auth import trakt
		trakt.Trakt().refresh_token()
	except Exception:
		log_utils.error("Trakt token refresh FAILED")
		return 'failed'

	xbmc.sleep(1500) # Allow Kodi to flush updated settings

	new_token = get_trakt_token()
	new_expires = get_trakt_expires()

	if not new_token:
		xbmc.log('NXTFlix Light: Trakt refresh completed but token is still blank', xbmc.LOGERROR)
		return 'failed'

	if new_expires > 0 and int(time.time()) >= (new_expires - 1800):
		xbmc.log('NXTFlix Light: Trakt refresh completed but expiry is still invalid/near expiry', xbmc.LOGERROR)
		return 'failed'

	xbmc.log('NXTFlix Light: Trakt token refreshed successfully', xbmc.LOGINFO)
	return 'refreshed'

def startup_tk_sync(mode="refresh"): # Sync Trakt tokens to add-ons
	if not get_trakt_token():
		xbmc.log('NXTFlix Light: Trakt sync skipped - no master token present', xbmc.LOGINFO)
		return False

	try:
		from acctmgr.modules.sync import trakt_sync
		trakt_sync.Auth().trakt_auth(mode=mode)
		xbmc.log('NXTFlix Light: Trakt token synced to add-ons', xbmc.LOGINFO)
		return True
	except Exception:
		log_utils.error("Trakt sync FAILED")
		return False

def TraktStartup():
        
	# Startup flow:
	# 1. Force NOT ready
	# 2. Wait for Kodi startup
	# 3. Refresh if needed
	# 4. Sync only when safe
	# 5. Mark READY only when safe

	am_trakt_startup_begin()
	startup_wait()

	if not ensure_defaults(): # If Trakt NOT authed, end Trakt startup flow
                am_trakt_startup_complete()
                return

	status = trakt_refresh()

	if status == 'failed':
		xbmc.log('NXTFlix Light: Startup refresh failed - leaving Trakt NOT READY', xbmc.LOGERROR)
		am_trakt_startup_fail()
		return

	if status == 'refreshed':
		sync_ok = startup_tk_sync(mode="refresh")
	elif status == 'valid':
		sync_ok = startup_tk_sync(mode="startup")
	elif status == 'missing':
		sync_ok = True
	else:
		sync_ok = False

	if not sync_ok:
		xbmc.log('NXTFlix Light: Startup sync failed - leaving Trakt NOT READY', xbmc.LOGERROR)
		am_trakt_startup_fail()
		return

	am_trakt_startup_complete()
		
def SyncManager():  # Auto-sync credentials with recently installed/supported addons
	try:
		if control.setting('sync.mdb.service')=='true' and mdb_master_token:
			from acctmgr.modules.sync import mdblist_sync
			mdblist_sync.Auth().mdblist_auth()
	except Exception:
		log_utils.error("Startup MDBList Startup Sync FAILED")
		
	try:
		if control.setting('sync.rd.service')=='true' and rd_master_token:
			from acctmgr.modules.sync import debrid_rd
			debrid_rd.Auth().realdebrid_auth()
	except Exception:
		log_utils.error("Startup Real-Debrid Startup Sync FAILED")
	
	try:
		if control.setting('sync.pm.service')=='true' and pm_master_token:
			from acctmgr.modules.sync import debrid_pm
			debrid_pm.Auth().premiumize_auth()
	except Exception:
		log_utils.error("Startup Premiumize Startup Sync FAILED")

	try:
		if control.setting('sync.ad.service')=='true' and ad_master_token:
			from acctmgr.modules.sync import debrid_ad 
			debrid_ad.Auth().alldebrid_auth()
	except Exception:
		log_utils.error("Startup All-Debrid Startup Sync FAILED")

	'''try:	
		if control.setting('sync.ed.service')=='true' and ed_master_token:
			from acctmgr.modules.sync import easydebrid_sync
			easydebrid_sync.Auth().easydebrid_auth()
	except Exception:
		log_utils.error("Startup Easy-Debrid Startup Sync FAILED")'''

	try:	
		if control.setting('sync.tb.service')=='true' and tb_master_token:
			from acctmgr.modules.sync import torbox_sync
			torbox_sync.Auth().torbox_auth()
	except Exception:
		log_utils.error("Startup Torbox Startup Sync FAILED")

	'''try:	
		if control.setting('sync.oc.service')=='true' and oc_master_token:
			from acctmgr.modules.sync import offcloud_sync
			offcloud_sync.Auth().offcloud_auth()
	except Exception:
		log_utils.error("Startup OffCloud Startup Sync FAILED")'''

	try:	
		if control.setting('sync.en.service')=='true' and en_master_user and en_master_pass:
			from acctmgr.modules.sync import easynews_sync
			easynews_sync.Auth().easynews_auth()
	except Exception:
		log_utils.error("Startup Easynews Startup Sync FAILED")
		
def compute_file_hash(path): # Compute a simple hash of a file's contents to detect changes
	if not os.path.exists(path):
		return None
	try:
		with open(path, "rb") as f:
			return hashlib.md5(f.read()).hexdigest()
	except Exception as e:
		xbmc.log(f"APIManager: Error hashing {path} - {e}", xbmc.LOGERROR)
		return None

def run_addon_updates():  # Start add-on update check
	control.autoupdate_on() # Enable auto-updates
	xbmc.sleep(1500)
	xbmc.executebuiltin('UpdateAddonRepos()')  # Update repos/add-ons
	
def StartupManager():  # Compare and restore Trakt API keys / Run add-on updates
	monitor = xbmc.Monitor()
	start_time = time.time()
	api_timeout = start_time + 180  # Run Startup Manager for 3 min
	addon_updates_started = False
	addon_updates_seen = False
	addon_updates_finished = False
	quiet_cycles = 0

	last_hashes = {}  # Track last state of each add-on service
	service_paths = [
		var.path_nxtflixlt_service,
		var.path_gears_service,
                var.path_red_service,
		var.path_umb_service,
		#var.path_seren_service,
		#var.path_fen_service,
		var.path_pov_service,
		var.path_coal_service,
		#var.path_dradis_service,
		var.path_genocide_service,
		var.path_home_service,
		var.path_night_service,
		var.path_absol_service,
		var.path_crew_service,
		var.path_salts_service,
		#var.path_gen_service,
		var.path_scrubs_service,
                var.path_redg_service,
		var.path_tmdbh_service,
		#var.path_tkplay_service,
		var.path_trakt_service,
	]

	while not monitor.abortRequested() and time.time() <= api_timeout:
		if control.setting('api.service') == 'true' and get_trakt_token(): # Start API check
			if control.setting('api.stop') == 'true':
				control.setSetting('api.stop', 'false')
				break

			changed = False
			for path in service_paths:
				current_hash = compute_file_hash(path)
				if last_hashes.get(path) != current_hash:
					last_hashes[path] = current_hash
					changed = True

			if changed:  # Only start sync if a service file has changed
				from acctmgr.modules.sync import api_sync
				try:
					api_sync.check_api()
				except Exception as e:
					xbmc.log(f"APIManager: api_sync.check_api failed - {e}", xbmc.LOGERROR)

		if not addon_updates_started and get_trakt_token(): # Start add-on updates
			run_addon_updates()
			addon_updates_started = True

		if addon_updates_started and not addon_updates_finished:
			update_count = xbmc.getInfoLabel('System.AddonUpdateCount') # Count updates

			try:
				update_count = int(update_count or 0)
			except Exception:
				update_count = 0

			if update_count > 0:
				addon_updates_seen = True
				quiet_cycles = 0
			elif addon_updates_seen:
				quiet_cycles += 1

			if addon_updates_seen and quiet_cycles >= 6: # After count reaches 0 wait before exiting
				addon_updates_finished = True

		xbmc.sleep(500)  # Run every 500ms			
				
def AddonCheckUpdate(): # NXTFlix Light Update Notification
	if control.setting('check_for_update')=='true':
		xbmc.log('NXTFlix Light: Addon checking available updates', xbmc.LOGINFO)
		try:
			import re
			import requests
			repo_xml = requests.get('https://raw.githubusercontent.com/Zaxxon709/zaxxon/main/zips/script.module.acctmgr/addon.xml', timeout=10)
			if repo_xml.status_code != 200:
				return xbmc.log('NXTFlix Light: Could not connect to remote repo XML: status code = %s' % repo_xml.status_code, xbmc.LOGINFO)
			repo_version = re.search(r'<addon id=\"script.module.acctmgr\".*version=\"(\d*\.\d*\.\d*)\"', repo_xml.text, re.I).group(1)
			local_version = control.addonVersion()[:5]
			def check_version_numbers(current, new):
				current = current.split('.')
				new = new.split('.')
				step = 0
				for i in current:
					if int(new[step]) > int(i): return True
					if int(i) > int(new[step]): return False
					if int(i) == int(new[step]):
						step += 1
						continue
				return False
			if check_version_numbers(local_version, repo_version):
				while control.condVisibility('Library.IsScanningVideo'):
					control.sleep(10000)
				xbmc.log('NXTFlix Light: A newer version is available. Installed Version: v%s' % (local_version), xbmc.LOGINFO)
				control.notification(message=control.lang(32072) % repo_version, time=5000)
			return xbmc.log('NXTFlix Light: Addon update check complete', xbmc.LOGINFO)
		except Exception:
			log_utils.error("Addon update check failed")

def trakt_refresh_monitor(interval=300): # Trakt background monitor loop to refresh/sync Trakt when needed. Checks every 5 minutes
	monitor = xbmc.Monitor()
	xbmc.log('NXTFlix Light: Starting Trakt refresh monitor loop', xbmc.LOGINFO)

	while not monitor.abortRequested():
		try:
			token = get_trakt_token()

			if token:
				status = trakt_refresh()

				if status == 'refreshed':
					xbmc.log('NXTFlix Light: Background Trakt refresh succeeded - syncing add-ons', xbmc.LOGINFO)
					startup_tk_sync(mode="refresh")
				elif status == 'failed':
					xbmc.log('NXTFlix Light: Background Trakt refresh failed', xbmc.LOGERROR)
		except Exception:
			log_utils.error("NXTFlix Light Trakt refresh monitor FAILED")

		if monitor.waitForAbort(interval):
			break

	xbmc.log('NXTFlix Light: Trakt refresh monitor loop stopped', xbmc.LOGINFO)
       
# START SERVICES
ScraperCheck()
TraktStartup()
SyncManager()
StartupManager()
AddonCheckUpdate()
trakt_refresh_monitor()
