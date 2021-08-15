#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52
# modified by reaitten/orsixtyone
# about cmd to do
__version__ = "1.4.0 - dev"
import logging
import os
import time
import dotenv

from logging.handlers import RotatingFileHandler
from collections import defaultdict
from sys import exit
from pyrogram import Client
from pyrogram.raw import functions, types
from pyrogram.raw.base import BotCommand

from tgtlg.bot_utils.bot_cmds import BotCommands

if os.path.exists("log.txt"):
    with open("log.txt", "r+") as f_d:
        f_d.truncate(0)

# the logging things
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            "log.txt", maxBytes=50000000, backupCount=10
        ),
        logging.StreamHandler(),
    ],
)
logging.getLogger("pyrogram").setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.INFO)
logging.getLogger("PIL").setLevel(logging.INFO)

LOGGER = logging.getLogger(__name__)

user_specific_config=dict()

dotenv.load_dotenv("config.env")

# checking compulsory variable
for imp in ["TG_BOT_TOKEN", "APP_ID", "API_HASH", "OWNER_ID", "AUTH_CHANNEL"]:
    try:
        value = os.environ[imp]
        if not value:
            raise KeyError
    except KeyError:
        LOGGER.critical(f"Oh...{imp}  is missing from config.env ... fill that")
        exit()

# The Telegram API things
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
APP_ID = int(os.environ.get("APP_ID", ""))
API_HASH = os.environ.get("API_HASH")
OWNER_ID = int(os.environ.get("OWNER_ID", "539295917"))

# Get these values from my.telegram.org
# to store the channel ID who are authorized to use the bot
AUTH_CHANNEL = [int(x) for x in os.environ.get("AUTH_CHANNEL", "539295917").split()]

# the download location, where the HTTP Server runs
DOWNLOAD_LOCATION = "./Downloads"
# Telegram maximum file upload size
MAX_FILE_SIZE = 50000000
TG_MAX_FILE_SIZE = 2097152000
FREE_USER_MAX_FILE_SIZE = 50000000
AUTH_CHANNEL.append(539295917)
AUTH_CHANNEL.append(OWNER_ID)
# chunk size that should be used with requests
CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", "128"))
# default thumbnail to be used in the videos
DEF_THUMB_NAIL_VID_S = os.environ.get(
    "DEF_THUMB_NAIL_VID_S", "https://orsixtyone.cf/images/cover.png"
)
# maximum message length in Telegram
MAX_MESSAGE_LENGTH = 4096
# set timeout for subprocess
PROCESS_MAX_TIMEOUT = 3600
#
SP_LIT_ALGO_RITH_M = os.environ.get("SP_LIT_ALGO_RITH_M", "hjs")
ARIA_TWO_STARTED_PORT = int(os.environ.get("ARIA_TWO_STARTED_PORT", "6800"))
EDIT_SLEEP_TIME_OUT = int(os.environ.get("EDIT_SLEEP_TIME_OUT", "15"))
MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START = int(
    os.environ.get("MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START", 300)
)
MAX_TG_SPLIT_FILE_SIZE = int(os.environ.get("MAX_TG_SPLIT_FILE_SIZE", "2097152000"))
# add config vars for the display progress
FINISHED_PROGRESS_STR = os.environ.get("FINISHED_PROGRESS_STR", "█")
UN_FINISHED_PROGRESS_STR = os.environ.get("UN_FINISHED_PROGRESS_STR", "░")
# add offensive API
TG_OFFENSIVE_API = os.environ.get("TG_OFFENSIVE_API", None)
CUSTOM_FILE_NAME = os.environ.get("CUSTOM_FILE_NAME", "")
# commands to be moved to tgtlg/bot_utils/bot_cmds.py. here to-
'''
LEECH_COMMAND = os.environ.get("LEECH_COMMAND", "leech")
LEECH_UNZIP_COMMAND = os.environ.get("LEECH_UNZIP_COMMAND", "extract")
LEECH_ZIP_COMMAND = os.environ.get("LEECH_ZIP_COMMAND", "archive")
GLEECH_COMMAND = os.environ.get("GLEECH_COMMAND", "gleech")
GLEECH_UNZIP_COMMAND = os.environ.get("GLEECH_UNZIP_COMMAND", "gextract")
GLEECH_ZIP_COMMAND = os.environ.get("GLEECH_ZIP_COMMAND", "garchive")
CLONE_COMMAND_G = os.environ.get("CLONE_COMMAND_G", "gclone")
TELEGRAM_LEECH_COMMAND = os.environ.get("TELEGRAM_LEECH_COMMAND", "tleech")
TELEGRAM_LEECH_UNZIP_COMMAND = os.environ.get("TELEGRAM_LEECH_UNZIP_COMMAND", "textract")
CANCEL_COMMAND_G = os.environ.get("CANCEL_COMMAND_G", "cancel")
YTDL_COMMAND = os.environ.get("YTDL_COMMAND", "ytdl")
GYTDL_COMMAND = os.environ.get("GYTDL_COMMAND", "gytdl")
PYTDL_COMMAND = os.environ.get("PYTDL_COMMAND", "pytdl")
GPYTDL_COMMAND = os.environ.get("GPYTDL_COMMAND", "gpytdl")
TOGGLE_VID = os.environ.get("TOGGLE_VID", "toggledvid")
TOGGLE_DOC = os.environ.get("TOGGLE_DOC", "toggledoc")
GET_SIZE_G = os.environ.get("GET_SIZE_G", "getsize")
STATUS_COMMAND = os.environ.get("STATUS_COMMAND", "status")
SAVE_THUMBNAIL = os.environ.get("SAVE_THUMBNAIL", "savethumb")
CLEAR_THUMBNAIL = os.environ.get("CLEAR_THUMBNAIL", "clearthumb")
LOG_COMMAND = os.environ.get("LOG_COMMAND", "log")
UPLOAD_COMMAND = os.environ.get("UPLOAD_COMMAND", "upload")
RENEWME_COMMAND = os.environ.get("RENEWME_COMMAND", "renewme")
RENAME_COMMAND = os.environ.get("RENAME_COMMAND", "rename")
'''
# here
RCLONE_CONFIG = os.environ.get("RCLONE_CONFIG", "")
DESTINATION_FOLDER = os.environ.get("DESTINATION_FOLDER", "")
INDEX_LINK = os.environ.get("INDEX_LINK", "")
UPLOAD_AS_DOC = os.environ.get("UPLOAD_AS_DOC", "False")

BOT_START_TIME = time.time()
# dict to control uploading and downloading
gDict = defaultdict(lambda: [])
# user settings dict #ToDo
user_settings = defaultdict(lambda: {})
gid_dict = defaultdict(lambda: [])

app = Client(
    ':memory:',
    bot_token=TG_BOT_TOKEN,
    api_id=APP_ID,
    api_hash=API_HASH,
    workers=343,
)

def multi_rclone_init():
    if not os.path.exists("rclone.conf") and RCLONE_CONFIG:  # you never know
        LOGGER.critical("found rclone config in variables, but could not find rclone.conf. Upload rclone.conf to root directory of repo!")
        exit()
    if not os.path.exists("rclone_bak.conf") and os.path.exists("rclone.conf"):  # backup rclone.conf file
        with open("rclone_bak.conf", "w+", newline="\n", encoding="utf-8") as fole:
            with open("rclone.conf", "r") as f:
                fole.write(f.read())
        LOGGER.info("rclone.conf backuped to rclone_bak.conf!")

def bcmds(app):
    botcmds = [
    types.BotCommand(command=f'{BotCommands.StartCommand}', description='Get Start Msg'),
    types.BotCommand(command=f'{BotCommands.HelpCommand}', description='Get Detailed Help'),
    types.BotCommand(command=f'{BotCommands.LeechCommand}', description='Start Leeching'),
    types.BotCommand(command=f'{BotCommands.ArchiveCommand}', description='Archive Leech'),
    types.BotCommand(command=f'{BotCommands.ExtractCommand}', description='Extract Leech'),
    types.BotCommand(command=f'{BotCommands.RcloneLeechCommand}', description='Leech & Upload to Drive'),
    types.BotCommand(command=f'{BotCommands.RcloneLeechArchiveCommand}', description='Leech, Archive, & Upload to Drive'),
    types.BotCommand(command=f'{BotCommands.RcloneLeechExtractCommand}', description='Leech, Extract, & Upload to Drive'),
    types.BotCommand(command=f'{BotCommands.CloneCommand}', description='Clone GDrive Files'),
    types.BotCommand(command=f'{BotCommands.TelegramLeechCommand}', description='Leech Telegram Files & Upload to Drive'),
    types.BotCommand(command=f'{BotCommands.TelegramLeechExtractCommand}', description='Leech Telegram Files, Extract, & Upload to Drive'),
    types.BotCommand(command=f'{BotCommands.CancelCommand}', description='Cancel Leech'),
    types.BotCommand(command=f'{BotCommands.YoutubeDownloaderCommand}', description='Leech YT Videos, & supported Links'),
    types.BotCommand(command=f'{BotCommands.PlaylistYoutubeDownloaderCommand}', description='Leech YT Playlists'),
    types.BotCommand(command=f'{BotCommands.RcloneYoutubeDownloaderCommand}', description='Leech YT Videos, supported Links, and Upload to Drive'),
    types.BotCommand(command=f'{BotCommands.RclonePlaylistYoutubeDownloaderCommand}', description='Leech YT Playlists, and Upload to Drive'),
    types.BotCommand(command=f'{BotCommands.StatusCommand}', description='Check Status'),
    types.BotCommand(command=f'{BotCommands.SaveThumbnailCommand}', description='Save Image for Thumbnail'),
    types.BotCommand(command=f'{BotCommands.ClearThumbnailCommand}', description='Clear Saved Thumbnail'),
    types.BotCommand(command=f'{BotCommands.RenameCommand}', description='Rename Telegram Files'),
    types.BotCommand(command=f'{BotCommands.ReNewMeCommand}', description='Clear bugged downloads'),
    types.BotCommand(command=f'{BotCommands.SearchHelpCommand}', description='Search for Torrents'),
    types.BotCommand(command=f'{BotCommands.NyaasiCommand}', description='Search On Nyaa.si'),
    types.BotCommand(command=f'{BotCommands.SukebeiCommand}', description='Search On Sukebei (+18)'),
    types.BotCommand(command=f'{BotCommands.ToggleVideoCommand}', description='Upload as a Video'),
    types.BotCommand(command=f'{BotCommands.ToggleDocumentCommand}', description='Upload as a Document'),
    types.BotCommand(command=f'{BotCommands.RcloneConfigCommand}', description='Change rclone Config'),
    types.BotCommand(command=f'{BotCommands.GetRcloneSizeCommand}', description='Get Rclone Destination Folder Size'),
    types.BotCommand(command=f'{BotCommands.LogCommand}', description='Get Logs')
    ]
    app.send(functions.bots.SetBotCommands(commands=botcmds))
    LOGGER.info("Added Bot CMDS!")

multi_rclone_init()

'''
    BotCommand(f'/start','Get Start Msg'),
    BotCommand(f'/help','Get Detailed Help'),
    BotCommand(f'{LEECH_COMMAND}','Start Leeching'),
    BotCommand(f'{LEECH_ZIP_COMMAND}','Archive Leech'),
    BotCommand(f'{LEECH_UNZIP_COMMAND}','Extract Leech'),
    BotCommand(f'{GLEECH_COMMAND}','Leech & Upload to Drive'),
    BotCommand(f'{GLEECH_ZIP_COMMAND}','Leech, Archive, & Upload to Drive'),
    BotCommand(f'{GLEECH_UNZIP_COMMAND}','Leech, Extract, & Upload to Drive'),
    BotCommand(f'{CLONE_COMMAND_G}','Clone GDrive Files'),
    BotCommand(f'{TELEGRAM_LEECH_COMMAND}','Leech Telegram Files & Upload to Drive'),
    BotCommand(f'{TELEGRAM_LEECH_UNZIP_COMMAND}','Leech Telegram Files, Extract, & Upload to Drive'),
    BotCommand(f'{CANCEL_COMMAND_G}','Cancel Leech'),
    BotCommand(f'{YTDL_COMMAND}','Leech YT Videos, & supported Links'),
    BotCommand(f'{PYTDL_COMMAND}','Leech YT Playlists'),
    BotCommand(f'{GYTDL_COMMAND}','Leech YT Videos, supported Links, and Upload to Drive'),
    BotCommand(f'{GPYTDL_COMMAND}','Leech YT Playlists, and Upload to Drive'),
    BotCommand(f'{STATUS_COMMAND}','Check Status'),
    BotCommand(f'{SAVE_THUMBNAIL}','Save Image for Thumbnail'),
    BotCommand(f'{CLEAR_THUMBNAIL}','Clear Saved Thumbnail'),
    BotCommand(f'{RENAME_COMMAND}','Rename Telegram Files'),
    BotCommand(f'{RENEWME_COMMAND}','Clear bugged downloads'),
    BotCommand(f'{TOGGLE_VID}','Upload as a Video'),
    BotCommand(f'{TOGGLE_DOC}','Upload as a Document'),
    BotCommand(f'/rclone','Change rclone Config'),
    BotCommand(f'{GET_SIZE_G}','Start Leeching'),
    BotCommand(f'{LOG_COMMAND}','Start Leeching')]
'''