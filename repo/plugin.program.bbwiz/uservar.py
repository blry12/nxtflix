import os, xbmc, xbmcaddon
import binascii
#########################################################
### User Edit Variables #################################
#########################################################
# Enable/Disable the text file caching with 'Yes' or 'No' and age being how often it rechecks in minutes
CACHETEXT      = 'Yes'
CACHEAGE       = 30
ADDON_ID       = xbmcaddon.Addon().getAddonInfo('id')
ADDONTITLE     = 'Bradleys Builds GUI WIZARD'
BUILDERNAME    = 'Bradleys Builds'
#########################Make sure to change the repo to yours!!!!
EXCLUDES       = [ADDON_ID, 'roms', 'My_Builds', 'backupdir', 'script.module.kodi-six', 'script.module.six']
BUILDFILE      = 'https://the666mafia.com/txt/bbgui_builds.txt'
UPDATECHECK    = 0
APKFILE        = 'https://'
YOUTUBETITLE   = 'FTG Help Videos' 
YOUTUBEFILE    = 'https://'
ADDONFILE      = 'https://'
ADVANCEDFILE   = 'https://'
ROMPACK        = 'https://'
EMUAPKS        = 'https://'
ADDONPACK      = 'https://'
PATH           = xbmcaddon.Addon().getAddonInfo('path')
ART            = os.path.join(PATH, 'resources', 'art')

#########################################################
### THEMING MENU ITEMS ##################################
#########################################################

##Alway test to see the color combo!!

#### NEW GUI THEME ###################################
# Choose from the following 
# Only these colors avalable
# white , blue , orange , black , red , purple , pink , lime , cyan, green
#Button focus color
FOCUS_BUTTON_COLOR = 'black'
EXIT_BUTTON_COLOR = 'red'
#Highlight outline for lists
HIGHLIGHT_LIST = 'button_focus'
##No TXT file Banner
NO_TXT_FILE = 'orange'

############################################
############################################
### The full list of colors for below can found @ https://forum.kodi.tv/showthread.php?tid=210837

#Top Main buttons
MAIN_BUTTONS_TEXT = 'black'
#All other buttons
OTHER_BUTTONS_TEXT = 'black'
#all list text color
##FYI any color placed in the txt file will overide this
LIST_TEXT = 'black'


#Description text title color
DES_T_COLOR = 'black'
#Description color
DESCOLOR = 'black'

#Wizard title name and verion color
WIZTITLE = 'Bradleys Builds GUI WIZARD'
WIZTITLE_COLOR = 'black'
VERTITLE_COLOR = 'black'
VER_NUMBER_COLOR = 'black'
############################################################

## The colors and theme below is still used for the pop up dialogs
##Alway test to see the color combo
# You can edit these however you want, just make sure that you have a %s in each of the
# THEME's so it grabs the text from the menu item
COLOR1         = 'blue'
COLOR2         = 'red'
COLOR3         = 'red'
COLOR4         = 'snow'
COLOR5         = 'lime'
# Primary menu items   / %s is the menu item and is required
THEME1         = '[COLOR '+COLOR4+']%s[/COLOR]'
# Build Names          / %s is the menu item and is required
THEME2         = '[COLOR '+COLOR4+']%s[/COLOR]'
# Alternate items      / %s is the menu item and is required
THEME3         = '[COLOR '+COLOR3+']%s[/COLOR]'
# Current Build Header / %s is the menu item and is required
THEME4         = '[COLOR '+COLOR3+']Current Build:[/COLOR] [COLOR '+COLOR3+']%s[/COLOR]'
# Current Theme Header / %s is the menu item and is required
THEME5         = '[COLOR '+COLOR3+']Current Theme:[/COLOR] [COLOR '+COLOR3+']%s[/COLOR]'
THEME6         = '[COLOR '+COLOR3+'][B]%s[/B][/COLOR]'



#########################################################
# If you want to use locally stored icons the place them in the Resources/Art/
# folder of the wizard then use os.path.join(ART, 'imagename.png')
# do not place quotes around os.path.join
# Example:  ICONMAINT     = os.path.join(ART, 'mainticon.png')
#           ICONSETTINGS  = 'https://'
# Leave as https:// for default icon
ICONBUILDS     = 'https://'
ICONMAINT      = 'https://'
ICONAPK        = 'https://'
ICONADDONS     = 'https://'
ICONYOUTUBE    = 'https://'
ICONSAVE       = 'https://'
ICONTRAKT      = 'https://'
ICONREAL       = 'https://'
ICONLOGIN      = 'https://'
ICONCONTACT    = 'https://'
ICONSETTINGS   = 'https://'
# Hide the ====== seperators 'Yes' or 'No'
HIDESPACERS    = 'No'
# Character used in seperator
SPACER         = '~'

# Message for Contact Page
# Enable 'Contact' menu item 'Yes' hide or 'No' dont hide
HIDECONTACT    = 'No'
# You can add \n to do line breaks
CONTACT        = ''
#Images used for the contact window.  https:// for default icon and fanart
CONTACTICON    = os.path.join(ART, 'icon.png')
CONTACTFANART  = 'https://'
#########################################################

#########################################################
### AUTO UPDATE #########################################
########## FOR THOSE WITH NO REPO #######################
# Enable Auto Update 'Yes' or 'No'
AUTOUPDATE     = 'yes'
# Url to wizard version
WIZARDFILE     = 'https://the666mafia.com/wizards/plugin.program.bbwiz.zip'
#########################################################

#########################################################
### AUTO INSTALL ########################################
########## REPO IF NOT INSTALLED ########################
# Enable Auto Install 'Yes' or 'No'
AUTOINSTALL    = 'No'
# Addon ID for the repository
REPOID         = ''
# Url to Addons.xml file in your repo folder(this is so we can get the latest version)
REPOADDONXML   = 'https://'
# Url to folder zip is located in
REPOZIPURL     =  'https://'
#########################################################

#########################################################
### NOTIFICATION WINDOW##################################
#########################################################
# Enable Notification screen Yes or No
ENABLE         = 'Yes'
# Url to notification file
NOTIFICATION   = 'https://the666mafia.com/txt/bbnotify.txt'
# Use either 'Text' or 'Image'
HEADERTYPE     = 'Text'
# Font size of header
FONTHEADER     = 'Font13'
HEADERMESSAGE  = 'Bradleys Builds GUI WIZARD'
# url to image if using Image 424x180
HEADERIMAGE    = ''
# Font for Notification Window
FONTSETTINGS   = 'Font12'
# Background for Notification Window
BACKGROUND     = 'https://'
BACKGROUND2     = os.path.join(ART, 'ContentPanel.png')
BACKGROUND3     = os.path.join(ART, 'ContentPanel.png')
############################    #############################