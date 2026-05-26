# -*- coding: utf-8 -*-
import os
import shutil
import xbmc, xbmcaddon, xbmcgui, xbmcvfs
import sqlite3
import zipfile
import tempfile
import xml.etree.ElementTree as ET

dialog = xbmcgui.Dialog()
translatePath = xbmcvfs.translatePath
addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon = xbmcaddon.Addon(addon_id)
addon_info = addon.getAddonInfo
addon_path = translatePath(addon_info('path'))
addon_data = translatePath('special://profile/addon_data/')
addon_icon = translatePath('special://home/addons/script.fentastic.helper/resources/icon.png')

#Skin Backup/Restore Variables
db_dst_dir = xbmcvfs.translatePath("special://profile/addon_data/script.fentastic.helper/")
home = translatePath('special://home/')
user_path = os.path.join(home, 'userdata/')
data_path = os.path.join(user_path, 'addon_data/')
skin_path = translatePath('special://skin/')
skin = ET.parse(os.path.join(skin_path, 'addon.xml'))
root = skin.getroot()
skin_id = root.attrib['id']

#GUI/FAV Variables
gui_file = 'guisettings.xml'
fav_file = 'favourites.xml'

#Menu/Widget Default Configs
dst_cfg = os.path.join(skin_path, 'xml/')
dst_db = os.path.join(addon_data, 'script.fentastic.helper/')

fen_cfg = os.path.join(skin_path, 'resources/default_configs/Fen_Light_Basic/menus_widgets/')
fen_db = os.path.join(skin_path, 'resources/default_configs/Fen_Light_Basic/database/')

fen_tk_cfg = os.path.join(skin_path, 'resources/default_configs/Fen_Light_Trakt/menus_widgets/')
fen_tk_db = os.path.join(skin_path, 'resources/default_configs/Fen_Light_Trakt/database/')

fen_anime_cfg = os.path.join(skin_path, 'resources/default_configs/Fen_Light_Anime/menus_widgets/')
fen_anime_db = os.path.join(skin_path, 'resources/default_configs/Fen_Light_Anime/database/')

red_cfg = os.path.join(skin_path, 'resources/default_configs/Red_Light_Basic/menus_widgets/')
red_db = os.path.join(skin_path, 'resources/default_configs/Red_Light_Basic/database/')

red_tk_cfg = os.path.join(skin_path, 'resources/default_configs/Red_Light_Trakt/menus_widgets/')
red_tk_db = os.path.join(skin_path, 'resources/default_configs/Red_Light_Trakt/database/')

red_anime_cfg = os.path.join(skin_path, 'resources/default_configs/Red_Light_Anime/menus_widgets/')
red_anime_db = os.path.join(skin_path, 'resources/default_configs/Red_Light_Anime/database/')

pov_cfg = os.path.join(skin_path, 'resources/default_configs/POV_Basic/menus_widgets/')
pov_db = os.path.join(skin_path, 'resources/default_configs/POV_Basic/database/')

pov_tk_cfg = os.path.join(skin_path, 'resources/default_configs/POV_Trakt/menus_widgets/')
pov_tk_db = os.path.join(skin_path, 'resources/default_configs/POV_Trakt/database/')

pov_anime_cfg = os.path.join(skin_path, 'resources/default_configs/POV_Anime/menus_widgets/')
pov_anime_db = os.path.join(skin_path, 'resources/default_configs/POV_Anime/database/')

umb_cfg = os.path.join(skin_path, 'resources/default_configs/Umbrella_Basic/menus_widgets/')
umb_db = os.path.join(skin_path, 'resources/default_configs/Umbrella_Basic/database/')

umb_tk_cfg = os.path.join(skin_path, 'resources/default_configs/Umbrella_Trakt/menus_widgets/')
umb_tk_db = os.path.join(skin_path, 'resources/default_configs/Umbrella_Trakt/database/')

gears_cfg = os.path.join(skin_path, 'resources/default_configs/The_Gears_Basic/menus_widgets/')
gears_db = os.path.join(skin_path, 'resources/default_configs/The_Gears_Basic/database/')

gears_tk_cfg = os.path.join(skin_path, 'resources/default_configs/The_Gears_Trakt/menus_widgets/')
gears_tk_db = os.path.join(skin_path, 'resources/default_configs/The_Gears_Trakt/database/')

tmdbh_cfg = os.path.join(skin_path, 'resources/default_configs/TMDbH/menus_widgets/')
tmdbh_db = os.path.join(skin_path, 'resources/default_configs/TMDbH/database/')


# -------------------------------------------------
# HELPERS
# -------------------------------------------------
#Open Kodi keyboard and return input
def get_keyboard_text(default=""):
    kb = xbmc.Keyboard(default, "Enter name for your backup")
    kb.doModal()
    if kb.isConfirmed():
        text = kb.getText().strip()
        return text if text else None
    return None

#Create directory if it doesn't exist
def ensure_dir(path):
    if not xbmcvfs.exists(path):
        xbmcvfs.mkdirs(path)

#Copy file
def copy_file(src, dst):
    try:
        ensure_dir(os.path.dirname(dst))
        xbmcvfs.copy(src, dst)
    except Exception as e:
        dialog.notification("Backup Error", str(e), xbmcgui.NOTIFICATION_ERROR, 3000)

# Check if an addon is installed
def addon_installed(addon_id):
    """Return True if addon is installed."""
    try:
        xbmcaddon.Addon(addon_id)
        return True
    except:
        return False

# Copy all files from source to destination
def copy_all_files(src_dir, dst_dir):
    """
    Copy all files from src_dir to dst_dir.
    Overwrites existing files with the same name.
    """
    # Make sure destination exists
    os.makedirs(dst_dir, exist_ok=True)

    # Loop through items in source directory
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dst_path = os.path.join(dst_dir, item)

        # Copy only files (skip subdirectories)
        if os.path.isfile(src_path):
            shutil.copy2(src_path, dst_path)
            
# Delete files starting with
def delete_files_starting_with(directory, prefix):
    """
    Delete all files in `directory` whose filenames start with
    """
    # Ensure directory ends with slash
    if not directory.endswith(("/", "\\")):
        directory += "/"

    # List the directory contents
    try:
        dirs, files = xbmcvfs.listdir(directory)
    except Exception as e:
        xbmc.log(f"Error reading directory: {e}", xbmc.LOGERROR)
        return

    # Loop through files and delete those starting with prefix
    for file_name in files:
        if file_name.startswith(prefix):
            full_path = os.path.join(directory, file_name)
            xbmcvfs.delete(full_path)


# -------------------------------------------------
# SET BACKUP DIRECTORY
# -------------------------------------------------
def choose_backup_directory():
	default_path = xbmcvfs.translatePath("special://home/backups/FENtastic_Plus/")
	current_path = xbmc.getInfoLabel("Skin.String(backup_directory)")

	if not current_path:
		current_path = default_path

	path = xbmcgui.Dialog().browseSingle(
		3,
		"Choose Backup Directory",
		"files",
		defaultt=current_path
	)

	if not path:
		return

	xbmc.executebuiltin('Skin.SetString(backup_directory,"%s")' % path)

	dialog.ok("FENtastic Plus","Backup directory saved.[CR][CR]""Location:[CR][COLOR=gold]%s[/COLOR]" % os.path.normpath(path))


def get_backup_directory():
	path = xbmc.getInfoLabel("Skin.String(backup_directory)")

	if path:
		return path

	return xbmcvfs.translatePath("special://home/backups/FENtastic_Plus/")


def get_backup_subdir(folder_name):
	path = os.path.join(get_backup_directory(), folder_name)
	ensure_dir(path)
	return path


# -------------------------------------------------
# GUI & FAVS BACKUP/RESTORE FUNCTIONS
# -------------------------------------------------
#Backup GUI settings
def backup_gui():
    gui_save = get_backup_subdir("gui_bkup")
    selection = xbmcgui.Dialog().yesno("FENtastic Plus","Are you sure?")
    if selection == 1:
        ensure_dir(gui_save)
        if os.path.exists(os.path.join(user_path, gui_file)) and os.path.exists(os.path.join(gui_save)):
            try:
                xbmcvfs.copy(os.path.join(user_path, gui_file), os.path.join(gui_save, gui_file))
            except Exception as e:
                xbmc.log('Failed to backup %s. Reason: %s' % (os.path.join(gui_save, gui_file), e), xbmc.LOGINFO)
        dialog.notification("FENtastic Plus", "Backup Complete", addon_icon, 3000)
    elif selection == 0:
        return

#Restore GUI settings              
def restore_gui():
    gui_save = get_backup_subdir("gui_bkup")
    selection = xbmcgui.Dialog().yesno("FENtastic Plus","Are you sure?")
    if selection == 1:
        if os.path.exists(os.path.join(gui_save, gui_file)):
            try:
                xbmcvfs.copy(os.path.join(gui_save, gui_file), os.path.join(user_path, gui_file))
            except Exception as e:
                xbmc.log('Failed to restore %s. Reason: %s' % (os.path.join(user_path, gui_file), e), xbmc.LOGINFO)
        dialog.ok('FENtastic Plus', 'To save changes you now need to force close Kodi.\n\nPress OK to force close Kodi.')
        os._exit(1)
    elif selection == 0:
        return

#Backup Favourites
def backup_favs():
    fav_save = get_backup_subdir("favs_bkup")
    selection = xbmcgui.Dialog().yesno("FENtastic Plus","Are you sure?")
    if selection == 1:
        ensure_dir(fav_save)
        if os.path.exists(os.path.join(user_path, fav_file)) and os.path.exists(os.path.join(fav_save)):
            try:
                xbmcvfs.copy(os.path.join(user_path, fav_file), os.path.join(fav_save, fav_file))
            except Exception as e:
                xbmc.log('Failed to backup %s. Reason: %s' % (os.path.join(fav_save, fav_file), e), xbmc.LOGINFO)
        dialog.notification("FENtastic Plus", "Backup Complete", addon_icon, 3000)
    elif selection == 0:
        return

#Restore Favourites              
def restore_favs():
    fav_save = get_backup_subdir("favs_bkup")
    selection = xbmcgui.Dialog().yesno("FENtastic Plus","Are you sure?")
    if selection == 1:
        if os.path.exists(os.path.join(fav_save, fav_file)):
            try:
                xbmcvfs.copy(os.path.join(fav_save, fav_file), os.path.join(user_path, fav_file))
            except Exception as e:
                xbmc.log('Failed to restore %s. Reason: %s' % (os.path.join(user_path, fav_file), e), xbmc.LOGINFO)
        dialog.ok('FENtastic Plus', 'To save changes you now need to force close Kodi.\n\nPress OK to force close Kodi.')
        os._exit(1)
    elif selection == 0:
        return

#Restore skin settings
def restore_skin(skin_save):
    selection = xbmcgui.Dialog().yesno("FENtastic Plus", "Restore the default skin settings.\nAre you sure?")
    if selection == 1:
        if os.path.exists(os.path.join(data_path, skin_id)):
            base_path = translatePath('special://home/addons/skin.fentastic/')
            src = os.path.join(base_path,'resources','default_colors','fentastic_plus','defaults.xml')
            dst = os.path.join(base_path,'colors','defaults.xml')
            try:
                shutil.copytree(skin_save,os.path.join(data_path, skin_id),dirs_exist_ok=True)
                copy_file(src, dst)
            except Exception as e:
                xbmc.log('Failed to restore %s. Reason: %s' %(os.path.join(data_path, skin_id), e),xbmc.LOGINFO)
        dialog.notification("FENtastic Plus", "Restore Complete", addon_icon, 3000)
        dialog.ok('FENtastic Plus', 'To save changes you now need to force close Kodi.\n\nPress OK to force close Kodi.')
        os._exit(1)
    elif selection == 0:
            return


# -------------------------------------------------
# USER-CONFIG BACKUP FUNCTION
# -------------------------------------------------
def backup_config():
    backup_name = get_keyboard_text()
    if not backup_name:
        dialog.ok("Backup Canceled", "No backup name was entered.")
        return

    base_backup_dir = get_backup_subdir("User_Configs")
    backup_dir = os.path.join(base_backup_dir, backup_name)
    skin_backup_dir = os.path.join(backup_dir, "skin_files")
    skin_settings_backup_dir = os.path.join(backup_dir, "skin_settings")

    for d in (skin_backup_dir, skin_settings_backup_dir):
        ensure_dir(d)

    # Paths
    xml_dir = xbmcvfs.translatePath("special://skin/xml/")
    db_src = xbmcvfs.translatePath("special://profile/addon_data/script.fentastic.helper/cpath_cache.db")

    # Backup Menus/Widgets
    for file in xbmcvfs.listdir(xml_dir)[1]:
        if "script-fentastic" in file.lower():
            src = os.path.join(xml_dir, file)
            dst = os.path.join(skin_backup_dir, file)
            copy_file(src, dst)

    # Backup database
    if xbmcvfs.exists(db_src):
        copy_file(db_src, os.path.join(backup_dir, "cpath_cache.db"))

    # Backup skin settings   
    if os.path.exists(os.path.join(data_path, skin_id)) and os.path.exists(os.path.join(skin_settings_backup_dir)):
        try:
            shutil.copytree(os.path.join(data_path, skin_id), os.path.join(skin_settings_backup_dir, skin_id), dirs_exist_ok=True)
        except Exception as e:
                xbmc.log('Failed to backup %s. Reason: %s' % (os.path.join(skin_settings_backup_dir, skin_id), e), xbmc.LOGINFO)

    display_path = os.path.normpath(backup_dir)

    dialog.ok(
        "Backup Completed",
        f"Backup saved as: [COLOR=gold]{backup_name}[/COLOR][CR]"
        f"Location:[CR][COLOR=gold]{display_path}[/COLOR]"
    )


# -------------------------------------------------
# USER-CONFIG RESTORE FUNCTION
# -------------------------------------------------
def restore_config():
    base_backup_dir = get_backup_subdir("User_Configs")
    if not xbmcvfs.exists(base_backup_dir):
        dialog.ok("Restore Error", "No backups directory found.")
        return

    # List backup folders
    folders = xbmcvfs.listdir(base_backup_dir)[0]

    if not folders:
        dialog.ok("Restore Error", "No backups available.")
        return

    # User selects a backup
    index = dialog.select("Choose Backup To Restore", folders)
    if index < 0:
        return

    selected_backup = folders[index]
    backup_path = os.path.join(base_backup_dir, selected_backup)
    skin_backup_path = os.path.join(backup_path, "skin_files/")
    skin_settings_backup_path = os.path.join(backup_path, "skin_settings/")

    # Restore skin XML files
    xml_dir = xbmcvfs.translatePath("special://skin/xml/")

    delete_files_starting_with(dst_cfg, 'script-fentastic')
    
    if xbmcvfs.exists(skin_backup_path):
        for file in xbmcvfs.listdir(skin_backup_path)[1]:
            src = os.path.join(skin_backup_path, file)
            dst = os.path.join(xml_dir, file)
            copy_file(src, dst)

    #Restore skin settings            
    if os.path.exists(os.path.join(data_path, skin_id)):
        try:
            shutil.copytree(os.path.join(skin_settings_backup_path, skin_id), os.path.join(data_path, skin_id), dirs_exist_ok=True)
        except Exception as e:
            xbmc.log('Failed to restore %s. Reason: %s' % (os.path.join(data_path, skin_id), e), xbmc.LOGINFO)

    #Restore database
    ensure_dir(db_dst_dir)
    db_src = os.path.join(backup_path, "cpath_cache.db")
    if xbmcvfs.exists(db_src):
        copy_file(db_src, os.path.join(db_dst_dir, "cpath_cache.db"))
    
    dialog.ok("Restore Complete", f"Restored backup:   [COLOR=gold]{selected_backup}[/COLOR]")
    xbmc.executebuiltin("ReloadSkin()")


# -------------------------------------------------
# USER-CONFIG IMPORT FUNCTION
# -------------------------------------------------
def import_config():
    zip_path = dialog.browseSingle(1,"Select FENtastic Plus Backup ZIP","local",".zip",False,False)

    if not zip_path:
        return

    if not zip_path.lower().endswith(".zip"):
        dialog.ok("Import Error", "Selected file is not a ZIP archive.")
        return

    base_backup_dir = get_backup_subdir("User_Configs")
    ensure_dir(base_backup_dir)

    temp_dir = tempfile.mkdtemp()

    try:
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(temp_dir)
    except Exception as e:
        dialog.ok("Import Error", f"Failed to extract ZIP:\n{e}")
        shutil.rmtree(temp_dir, ignore_errors=True)
        return

    items = os.listdir(temp_dir)
    if not items:
        dialog.ok("Import Error", "ZIP archive is empty.")
        shutil.rmtree(temp_dir, ignore_errors=True)
        return

    # Determine backup root
    if (len(items) == 1 and os.path.isdir(os.path.join(temp_dir, items[0]))):
        backup_root = os.path.join(temp_dir, items[0])
        backup_name = items[0]
    else:
        backup_root = temp_dir
        backup_name = os.path.splitext(os.path.basename(zip_path))[0]

    # Check backup structure
    required_paths = [os.path.join(backup_root, "skin_files"),os.path.join(backup_root, "skin_settings"),os.path.join(backup_root, "cpath_cache.db"),]

    for path in required_paths:
        if not os.path.exists(path):
            dialog.ok("Import Error","Invalid backup structure.\n\n""The ZIP must contain:\n""- skin_files/\n""- skin_settings/\n""- cpath_cache.db")
            shutil.rmtree(temp_dir, ignore_errors=True)
            return

    final_dst = os.path.join(base_backup_dir, backup_name)

    if os.path.exists(final_dst):
        overwrite = dialog.yesno("Backup Exists",f"A backup named '{backup_name}' already exists.\n\nOverwrite it?")
        if not overwrite:
            shutil.rmtree(temp_dir, ignore_errors=True)
            return
        shutil.rmtree(final_dst, ignore_errors=True)

    try:
        shutil.move(backup_root, final_dst)
    except Exception as e:
        dialog.ok("Import Error", f"Failed to save backup:\n{e}")
        shutil.rmtree(temp_dir, ignore_errors=True)
        return
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    # Ask to restore immediately
    if dialog.yesno("Import Complete",f"Backup '{backup_name}' imported successfully.\n\nRestore it now?"):
        restore_config()


# -------------------------------------------------
# USER-CONFIG EXPORT FUNCTION
# -------------------------------------------------
def export_config():
    base_backup_dir = get_backup_subdir("User_Configs")
    if not xbmcvfs.exists(base_backup_dir):
        dialog.ok("Export Error", "No backups directory found.")
        return

    backups = xbmcvfs.listdir(base_backup_dir)[0]
    if not backups:
        dialog.ok("Export Error", "No backups available to export.")
        return

    index = dialog.select("Select Backup To Export", backups)
    if index < 0:
        return

    backup_name = backups[index]
    backup_path = os.path.join(base_backup_dir, backup_name)

    # Confirm restore compatible structure
    required = [os.path.join(backup_path, "skin_files"),os.path.join(backup_path, "skin_settings"),os.path.join(backup_path, "cpath_cache.db"),]

    for path in required:
        if not os.path.exists(path):
            dialog.ok("Export Error","Selected backup is not compatible with restore_config().")
            return

    dest_dir = dialog.browse(3,"Choose Export Location","files","",False,False) # Select directory

    if not dest_dir:
        return

    if not dest_dir.endswith(("/", "\\")):
        dest_dir += "/"

    zip_path = os.path.join(dest_dir, f"{backup_name}.zip")

    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for root, _, files in os.walk(backup_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, base_backup_dir)
                    z.write(full_path, rel_path)

    except Exception as e:
        dialog.ok("Export Error", f"Failed to create ZIP:\n{e}")
        return

    dialog.notification("FENtastic Plus",f"Backup exported as:\n{backup_name}.zip",addon_icon,3000)


# -------------------------------------------------
# Enable All Main Menu Toggles
# -------------------------------------------------
def enable_all_home_menu_toggles():
    """
    Enables ALL home menu items based on the logic used in skinsettings.xml.
    Movies/TV use inverted logic; Custom1-6 use normal logic.
    """
    # Movies & TV shows
    inverted_settings = [
        "HomeMenuNoMoviesButton",
        "HomeMenuNoTVShowsButton",
    ]

    # Custom1–Custom6
    normal_settings = [
        "HomeMenuNoCustom1Button",
        "HomeMenuNoCustom2Button",
        "HomeMenuNoCustom3Button",
        "HomeMenuNoCustom4Button",
        "HomeMenuNoCustom5Button",
        "HomeMenuNoCustom6Button",
    ]

    # Music-Weather
    other_inverted_settings = [
        "HomeMenuNoMusicButton",
        "HomeMenuNoMusicVideoButton",
        "HomeMenuNoTVButton",
        "HomeMenuNoRadioButton",
        "HomeMenuNoPicturesButton",
        "HomeMenuNoVideosButton",
        "HomeMenuNoGamesButton",
        "HomeMenuNoWeatherButton",
    ]

    # Movies & TV Shows
    for setting in inverted_settings:
        is_set = xbmc.getCondVisibility(f"Skin.HasSetting({setting})")

        # If disabled. Enable it by resetting
        if is_set:
            xbmc.executebuiltin(f"Skin.Reset({setting})")
            xbmc.sleep(50)
        else:
            xbmc.log(f"Already ENABLED, skipping.", xbmc.LOGINFO)

    # CUSTOM 1–6
    for setting in normal_settings:
        is_set = xbmc.getCondVisibility(f"Skin.HasSetting({setting})")

        # If disabled. Enable it by setting true
        if not is_set:
            xbmc.executebuiltin(f"Skin.SetBool({setting})")
            xbmc.sleep(50)
        else:
            xbmc.log(f"Already ENABLED, skipping.", xbmc.LOGINFO)

    # Music - Weather
    for setting in other_inverted_settings:
        is_set = xbmc.getCondVisibility(f"Skin.HasSetting({setting})")
        
        # If enabled. Disable it by resetting
        if not is_set:
            xbmc.executebuiltin(f"Skin.SetBool({setting})")
            xbmc.sleep(50)
        else:
            xbmc.log(f"Already DISABLED, skipping.", xbmc.LOGINFO)


# -------------------------------------------------
# Main Menu Labels
# -------------------------------------------------
def load_all_menu_labels():
    """
    Reads all main menu labels from cpath_cache.db and assigns them
    to Skin.String() values for use in XML.
    """

    db_path = translatePath(
        "special://profile/addon_data/script.fentastic.helper/cpath_cache.db"
    )

    if not xbmcvfs.exists(db_path):
        return

    # DB main-menu key - Skin.String key - default label
    MENU_MAP = {
        "movie":   ("MenuMovieLabelDB",   "Movies"),
        "tvshow":  ("MenuTVShowLabelDB",  "TV Shows"),
        "custom1": ("MenuCustom1LabelDB", "Custom 1"),
        "custom2": ("MenuCustom2LabelDB", "Custom 2"),
        "custom3": ("MenuCustom3LabelDB", "Custom 3"),
        "custom4": ("MenuCustom4LabelDB", "Custom 4"),
        "custom5": ("MenuCustom5LabelDB", "Custom 5"),
        "custom6": ("MenuCustom6LabelDB", "Custom 6"),
    }

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        for key, (skin_key, default_label) in MENU_MAP.items():
            # This matches rows like "movie.main_menu", "tvshow.main_menu", "custom1.main_menu", etc.
            setting_key = f"{key}.main_menu"

            cur.execute(
                "SELECT cpath_header FROM custom_paths WHERE cpath_setting = ? LIMIT 1",
                (setting_key,)
            )
            row = cur.fetchone()

            if row and row[0]:
                label = row[0]
                source = "DB"
            else:
                label = default_label
                source = "DEFAULT"

            safe = label.replace('"', "'")
            xbmc.executebuiltin(f'Skin.SetString({skin_key},"{safe}")')

        conn.close()

    except Exception as e:
        xbmc.log(f"DB Error loading menu labels: {e}", xbmc.LOGERROR)

        
# -------------------------------------------------
# Select Pre-Made Configurations
# -------------------------------------------------
def pre_config_dialog():
    """
    Shows only config modes for addons actually installed.
    """

    menu = []
    modes = []

    def add_separator(title):
        menu.append(f"[COLOR dimgray]──────── {title} ────────[/COLOR]")
        modes.append(None)

    # Fen Light
    if addon_installed("plugin.video.fenlight"):
        add_separator("Fen Light")
        for config in ("Basic", "Trakt", "Anime"):
            label = f"Fen Light {config}"
            menu.append(label)
            modes.append(label)

    # Red Light
    if addon_installed("plugin.video.redlight"):
        add_separator("Red Light")
        for config in ("Basic", "Trakt", "Anime"):
            label = f"Red Light {config}"
            menu.append(label)
            modes.append(label)

    # POV
    if addon_installed("plugin.video.pov"):
        add_separator("POV")
        for config in ("Basic", "Trakt", "Anime"):
            label = f"POV {config}"
            menu.append(label)
            modes.append(label)

    # Umbrella
    if addon_installed("plugin.video.umbrella"):
        add_separator("Umbrella")
        for config in ("Basic", "Trakt"):
            label = f"Umbrella {config}"
            menu.append(label)
            modes.append(label)

    # The Gears
    if addon_installed("plugin.video.gears"):
        add_separator("The Gears")
        for config in ("Basic", "Trakt"):
            label = f"The Gears {config}"
            menu.append(label)
            modes.append(label)

    # TMDb Helper
    if (
        addon_installed("plugin.video.themoviedb.helper")
        and any(addon_installed(a) for a in [
            "plugin.video.fenlight",
            "plugin.video.umbrella",
            "plugin.video.pov"
        ])
    ):
        add_separator("TMDb Helper")
        menu.append("TMDb Helper")
        modes.append("TMDb Helper")

    # Nothing installed
    if not menu:
        xbmcgui.Dialog().ok(
            "FENtastic Plus",
            "No supported addons are installed.\nNothing to configure."
        )
        return

    # Let user choose
    while True:
        choice = xbmcgui.Dialog().select(
            "Choose Pre-Configuration",
            menu
        )

        if choice == -1:
            return

        # Ignore separators
        if modes[choice] is None:
            continue

        run_pre_config_mode(modes[choice])
        break

def run_pre_config_mode(mode):
    # Ask the user to confirm before applying
    confirm = xbmcgui.Dialog().yesno(
        "FENtastic Plus",
        f"Are you sure you want to apply the '[COLOR gold]{mode}[/COLOR]' pre-configuration?\n\n"
        "This will overwrite your current menu/widgets configuration.",
        nolabel="No",
        yeslabel="Yes"
    )

    if not confirm:
        return
    
    if mode == "Fen Light Basic":
        delete_files_starting_with(dst_cfg, 'script-fentastic')
        enable_all_home_menu_toggles()
        xbmc.executebuiltin('Skin.SetString(current_search_provider,"1")')
        copy_all_files(fen_cfg, dst_cfg)
        copy_all_files(fen_db, dst_db)

    elif mode == "Fen Light Trakt":
        delete_files_starting_with(dst_cfg, 'script-fentastic')
        enable_all_home_menu_toggles()
        xbmc.executebuiltin('Skin.SetString(current_search_provider,"1")')
        copy_all_files(fen_tk_cfg, dst_cfg)
        copy_all_files(fen_tk_db, dst_db)

    elif mode == "Fen Light Anime":
        delete_files_starting_with(dst_cfg, 'script-fentastic')
        enable_all_home_menu_toggles()
        xbmc.executebuiltin('Skin.SetString(current_search_provider,"1")')
        copy_all_files(fen_anime_cfg, dst_cfg)
        copy_all_files(fen_anime_db, dst_db)

    if mode == "Red Light Basic":
        delete_files_starting_with(dst_cfg, 'script-fentastic')
        enable_all_home_menu_toggles()
        xbmc.executebuiltin('Skin.SetString(current_search_provider,"5")')
        copy_all_files(red_cfg, dst_cfg)
        copy_all_files(red_db, dst_db)

    elif mode == "Red Light Trakt":
        delete_files_starting_with(dst_cfg, 'script-fentastic')
        enable_all_home_menu_toggles()
        xbmc.executebuiltin('Skin.SetString(current_search_provider,"5")')
        copy_all_files(red_tk_cfg, dst_cfg)
        copy_all_files(red_tk_db, dst_db)

    elif mode == "Red Light Anime":
        delete_files_starting_with(dst_cfg, 'script-fentastic')
        enable_all_home_menu_toggles()
        xbmc.executebuiltin('Skin.SetString(current_search_provider,"5")')
        copy_all_files(red_anime_cfg, dst_cfg)
        copy_all_files(red_anime_db, dst_db)

    elif mode == "POV Basic":
        delete_files_starting_with(dst_cfg, 'script-fentastic')
        enable_all_home_menu_toggles()
        xbmc.executebuiltin('Skin.SetString(current_search_provider,"3")')
        copy_all_files(pov_cfg, dst_cfg)
        copy_all_files(pov_db, dst_db)

    elif mode == "POV Trakt":
        delete_files_starting_with(dst_cfg, 'script-fentastic')
        enable_all_home_menu_toggles()
        xbmc.executebuiltin('Skin.SetString(current_search_provider,"3")')
        copy_all_files(pov_tk_cfg, dst_cfg)
        copy_all_files(pov_tk_db, dst_db)

    elif mode == "POV Anime":
        delete_files_starting_with(dst_cfg, 'script-fentastic')
        enable_all_home_menu_toggles()
        xbmc.executebuiltin('Skin.SetString(current_search_provider,"3")')
        copy_all_files(pov_anime_cfg, dst_cfg)
        copy_all_files(pov_anime_db, dst_db)

    elif mode == "Umbrella Basic":
        delete_files_starting_with(dst_cfg, 'script-fentastic')
        enable_all_home_menu_toggles()
        xbmc.executebuiltin('Skin.SetString(current_search_provider,"2")')
        copy_all_files(umb_cfg, dst_cfg)
        copy_all_files(umb_db, dst_db)

    elif mode == "Umbrella Trakt":
        delete_files_starting_with(dst_cfg, 'script-fentastic')
        enable_all_home_menu_toggles()
        xbmc.executebuiltin('Skin.SetString(current_search_provider,"2")')
        copy_all_files(umb_tk_cfg, dst_cfg)
        copy_all_files(umb_tk_db, dst_db)

    elif mode == "The Gears Basic":
        delete_files_starting_with(dst_cfg, 'script-fentastic')
        enable_all_home_menu_toggles()
        xbmc.executebuiltin('Skin.SetString(current_search_provider,"4")')
        copy_all_files(gears_cfg, dst_cfg)
        copy_all_files(gears_db, dst_db)

    elif mode == "The Gears Trakt":
        delete_files_starting_with(dst_cfg, 'script-fentastic')
        enable_all_home_menu_toggles()
        xbmc.executebuiltin('Skin.SetString(current_search_provider,"4")')
        copy_all_files(gears_tk_cfg, dst_cfg)
        copy_all_files(gears_tk_db, dst_db)

    elif mode == "TMDb Helper":
        delete_files_starting_with(dst_cfg, 'script-fentastic')
        enable_all_home_menu_toggles()
        xbmc.executebuiltin('Skin.SetString(current_search_provider,"0")')
        copy_all_files(tmdbh_cfg, dst_cfg)
        copy_all_files(tmdbh_db, dst_db)

    load_all_menu_labels()
    xbmc.executebuiltin('Skin.SetBool(noiconsilhouettes)')
    xbmc.executebuiltin("ReloadSkin()")
    xbmcgui.Dialog().notification("FENtastic Plus", f"{mode} config applied!", addon_icon, 3000)
