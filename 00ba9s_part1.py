programme_to_run = 1
#0 = facebook
#1 = vinted

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as Options
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
import undetected_chromedriver as uc
import os
import shutil
import sys
import time
import re
import json
import io
import base64
import threading
import subprocess
import hashlib
import concurrent.futures
from queue import Queue
import queue
import pygame
import pyautogui
import requests
from bs4 import BeautifulSoup
import webbrowser
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, send_file
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pyngrok import ngrok
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from urllib.parse import urlencode
from datetime import datetime
import logging
from ultralytics import YOLO
import random
import torch
from threading import Thread, Lock, Event
import time
import random
import threading
import tempfile
import pyautogui
import speech_recognition as sr
import socket
import json
import subprocess
import pyautogui
from scipy import signal
import wave


purchase_unsuccessful_wait_time = 900

VM_DRIVER_USE = True
google_login = True

# tests whether the listing is suitable for buying based on URL rather than scanning
TEST_WHETHER_SUITABLE = False
TEST_SUITABLE_URLS = [
    'https://www.vinted.co.uk/items/6963376052-nintendo-switch?referrer=catalog',
    'https://www.vinted.co.uk/items/6963025596-nintendo-switch-oled-model-the-legend-of-zelda-tears-of-the-kingdom-edition?referrer=catalog',
    'https://www.vinted.co.uk/items/6970192196-nintendo-switch-lite-in-grey?referrer=catalog'
]

# tests the number of listings found by the search
TEST_NUMBER_OF_LISTINGS = False

#tests the bookmark functionality
BOOKMARK_TEST_MODE = False
BOOKMARK_TEST_URL = "https://www.vinted.co.uk/items/7050671534-yoshimoto-nara-shirt?referrer=catalog"
BOOKMARK_TEST_USERNAME = "leah_lane" 

#tests the buying functionality
BUYING_TEST_MODE = False
BUYING_TEST_URL = "https://www.vinted.co.uk/items/6966124363-mens-t-shirt-bundle-x-3-ml?homepage_session_id=932d30be-02f5-4f54-9616-c412dd6e9da2"

#tests both the bookmark and buying functionality
TEST_BOOKMARK_BUYING_FUNCTIONALITY = False
TEST_BOOKMARK_BUYING_URL = "https://www.vinted.co.uk/items/6996290195-cider-with-rosie-pretty-decor-book?referrer=catalog"

PRICE_THRESHOLD = 30.0  # Minimum price threshold - items below this won't detect Nintendo Switch classes
NINTENDO_SWITCH_CLASSES = [
    'controller','tv_black', 
    'tv_white', 'comfort_h',
    'comfort_h_joy', 'switch_box', 'switch', 'switch_in_tv',
]

VINTED_SHOW_ALL_LISTINGS = True
print_debug = False
print_images_backend_info = False
test_bookmark_function = False
bookmark_listings = True
click_pay_button_final_check = True
test_bookmark_link = "https://www.vinted.co.uk/items/4402812396-paper-back-book?referrer=catalog"
bookmark_stopwatch_length = 540
buying_driver_click_pay_wait_time = 7.5
actually_purchase_listing = True
wait_for_bookmark_stopwatch_to_buy = False
test_purchase_not_true = False #uses the url below rather than the one from the web page
test_purchase_url = "https://www.vinted.co.uk/items/6963326227-nintendo-switch-1?referrer=catalog"
#sold listing: https://www.vinted.co.uk/items/6900159208-laptop-case
should_send_fail_bookmark_notification = True


purchase_unsuccessful_detected_urls = {}  # Track URLs waiting for "Purchase unsuccessful" detection
# Config
PROFILE_DIR = "Default"
PERMANENT_USER_DATA_DIR = r"C:\VintedScraper_Default2"
#"C:\VintedScraper_Default" - first one
#"C:\VintedScraper_Backup" - second one
BASE_URL = "https://www.vinted.co.uk/catalog"
SEARCH_QUERY = "nintendo switch"
PRICE_FROM = 10
PRICE_TO = 510
CURRENCY = "GBP"
ORDER = "newest_first"

# Where to dump your images
DOWNLOAD_ROOT = "vinted_photos"

# Suppress verbose ultralytics logging
logging.getLogger('ultralytics').setLevel(logging.WARNING)

# --- Object Detection Configuration ---
#pc
#MODEL_WEIGHTS = r"C:\Users\ZacKnowsHow\Downloads\best.pt"
#laptop
MODEL_WEIGHTS = r"C:\Users\ZacKnowsHow\Downloads\best.pt"
CLASS_NAMES = [
   '1_2_switch', 'animal_crossing', 'arceus_p', 'bow_z', 'bros_deluxe_m', 'comfort_h',
   'comfort_h_joy', 'controller', 'crash_sand', 'dance', 'diamond_p', 'evee',
   'fifa_23', 'fifa_24', 'gta', 'just_dance', 'kart_m', 'kirby',
   'lets_go_p', 'links_z', 'lite', 'lite_box', 'luigis', 'mario_maker_2',
   'mario_sonic', 'mario_tennis', 'minecraft', 'minecraft_dungeons', 'minecraft_story', 'miscellanious_sonic',
   'odyssey_m', 'oled', 'oled_box', 'oled_in_tv', 'other_mario', 'party_m',
   'rocket_league', 'scarlet_p', 'shield_p', 'shining_p', 'skywards_z', 'smash_bros',
   'snap_p', 'splatoon_2', 'splatoon_3', 'super_m_party', 'super_mario_3d', 'switch',
   'switch_box', 'switch_in_tv', 'switch_screen', 'switch_sports', 'sword_p', 'tears_z',
   'tv_black', 'tv_white', 'violet_p'
]

GENERAL_CONFIDENCE_MIN = 0.5
HIGHER_CONFIDENCE_MIN = 0.55
HIGHER_CONFIDENCE_ITEMS = { 'controller': HIGHER_CONFIDENCE_MIN, 'tv_white': HIGHER_CONFIDENCE_MIN, 'tv_black': HIGHER_CONFIDENCE_MIN }

####VINTED ^^^^

SCRAPER_USER_DATA_DIR = r"C:\FacebookScraper_ScraperProfile"
#default

MESSAGING_USER_DATA_DIR = r"C:\FacebookScraper_MessagingProfile"
#profile 2


app = Flask(__name__, template_folder='templates')

limiter = Limiter(get_remote_address, app=app, default_limits=["10 per second", "100 per minute"])

#logging.basicConfig(level=logging.DEBUG)
#logging.getLogger('selenium').setLevel(logging.DEBUG)
#logging.getLogger('urllib3').setLevel(logging.DEBUG)
#logging.getLogger('selenium').setLevel(logging.WARNING)
#logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('ultralytics').setLevel(logging.WARNING)

search_query = "nintendo switch"
ngrok.set_auth_token('2roTu5SuJVRTFYSd2d1JBTyhjXA_5qNzmjZBn5EHVA2dwMfrZ')

request_queue = Queue()
website_price = 0
website_price_adjusted = website_price
message_1 = f'still available? im london based, happy to pay {website_price_adjusted} + shipping upfront if you can post. thanks'
adjusted_message_1 = f'still available? i know you said collection but im london based, happy to pay {website_price_adjusted} + shipping upfront if you can post. thanks'

General_Confidence_Min = 0.5
Higher_Confidence_Min = 0.55
Higher_Confidence_Items = {'controller': Higher_Confidence_Min, 'tv_white': Higher_Confidence_Min, 'tv_black': Higher_Confidence_Min}
max_posting_age_minutes = 48000
min_price = 14
max_price = 500
element_exractor_timeout = 0.85
price_mulitplier = 1
visible_listings_scanned = 0
SD_card_price = 0

app.secret_key = "facebook1967"
PIN_CODE = 14346
#pc
OUTPUT_FILE_PATH = r"C:\users\zacknowshow\Downloads\SUITABLE_LISTINGS.txt"
#laptop
#OUTPUT_FILE_PATH = r"C:\Users\zacha\Downloads\SUITABLE_LISTINGS.txt"

recent_listings = {
    'listings': [],
    'current_index': 0
}

review_min = 3
REFRESH_AND_RESCAN = True  # Set to False to disable refresh functionality
MAX_LISTINGS_VINTED_TO_SCAN = 5  # Maximum listings to scan before refresh
wait_after_max_reached_vinted = 0  # Seconds to wait between refresh cycles (5 minutes)
VINTED_SCANNED_IDS_FILE = "vinted_scanned_ids.txt"
FAILURE_REASON_LISTED = True
REPEAT_LISTINGS = True
LOCK_POSITION = True
SHOW_ALL_LISTINGS = False
SHOW_PARTIALLY_SUITABLE = False
setup_website = False
send_message = True
current_listing_url = ""
send_notification = True
request_processing_event = threading.Event()

GAME_CLASSES = [
   '1_2_switch', 'animal_crossing', 'arceus_p', 'bow_z', 'bros_deluxe_m', 'crash_sand',
   'dance', 'diamond_p', 'evee', 'fifa_23', 'fifa_24', 'gta','just_dance', 'kart_m', 'kirby',
   'lets_go_p', 'links_z', 'luigis', 'mario_maker_2', 'mario_sonic', 'mario_tennis', 'minecraft',
   'minecraft_dungeons', 'minecraft_story', 'miscellanious_sonic', 'odyssey_m', 'other_mario',
   'party_m', 'rocket_league', 'scarlet_p', 'shield_p', 'shining_p', 'skywards_z', 'smash_bros',
   'snap_p', 'splatoon_2', 'splatoon_3', 'super_m_party', 'super_mario_3d', 'switch_sports',
   'sword_p', 'tears_z', 'violet_p'
]


title_must_contain = ["nintendo", "pokemon", "zelda", "mario", "animal crossing", "minecraft", 'oled', 'lite', 'pokémon', 'switch game',
                    'switch bundle', 'nintendo bundle', 'switch with games', 'modded switch']
title_forbidden_words = ['unofficial', 'keyboard', 'mouse', 'ps4', 'ps5', 'sold', 'organizer', 'holder', 'joy con', 'gift', 'read des'
                        'joycon', 'snes', 'gamecube', 'n64', 'damaged', 'circuit', 'kart live', 'ds', 'tablet only', 'ringfit', 'ring fit'
                        'repair', '™', 'each', 'empty game', 'just game case', 'empty case', 'arcade', 'wii', 'tv frame', 'joy-con',
                        'for parts', 'won’t charge', 'spares & repair', 'xbox', 'prices in description', 'collector set', 'collectors set'
                        'read description', 'joy pads', 'spares and repairs', 'neon', 'spares or repairs', 'dock cover', '3d print']
description_forbidden_words = ['faulty', 'not post', 'jailbreak', 'scam', 'visit us', 'opening hours', 'open 7 days', 'am - ',
                                'store', 'telephone', 'email', 'call us', '+44', '07', 'kart live', 'circuit', '.shop', 'our website',
                                'website:', 'empty game', 'just game case', 'empty case', 'each', 'spares and repairs', 'prices are',
                                'tablet only', 'not charge', 'stopped charging', 'doesnt charge', 'individually priced', 'per game', 
                                'https', 'case only', 'shop', 'spares or repairs', 'dock cover', '3d print', 'spares & repair',
                                'error code', 'will not connect']
#pc
CONFIG_FILE = r"C:\Users\ZacKnowsHow\Downloads\square_configuratgion.json"
#laptop
#CONFIG_FILE = r"C:\Users\zacha\Downloads\square_configuratgion.json"


model_weights = r"C:\Users\ZacKnowsHow\Downloads\best.pt"
class_names = [
   '1_2_switch', 'animal_crossing', 'arceus_p', 'bow_z', 'bros_deluxe_m', 'comfort_h',
   'comfort_h_joy', 'controller', 'crash_sand', 'dance', 'diamond_p', 'evee',
   'fifa_23', 'fifa_24', 'gta', 'just_dance', 'kart_m', 'kirby',
   'lets_go_p', 'links_z', 'lite', 'lite_box', 'luigis', 'mario_maker_2',
   'mario_sonic', 'mario_tennis', 'minecraft', 'minecraft_dungeons', 'minecraft_story', 'miscellanious_sonic',
   'odyssey_m', 'oled', 'oled_box', 'oled_in_tv', 'other_mario', 'party_m',
   'rocket_league', 'scarlet_p', 'shield_p', 'shining_p', 'skywards_z', 'smash_bros',
   'snap_p', 'splatoon_2', 'splatoon_3', 'super_m_party', 'super_mario_3d', 'switch',
   'switch_box', 'switch_in_tv', 'switch_screen', 'switch_sports', 'sword_p', 'tears_z',
   'tv_black', 'tv_white', 'violet_p'
]
mutually_exclusive_items = ['switch', 'oled', 'lite', 'switch_box', 'oled_box', 'lite_box', 'switch_in_tv', 'oled_in_tv']
capped_classes = [
   '1_2_switch', 'animal_crossing', 'arceus_p', 'bow_z', 'bros_deluxe_m', 'comfort_h',
   'crash_sand', 'dance', 'diamond_p', 'evee', 'fifa_23', 'fifa_24',
   'gta', 'just_dance', 'kart_m', 'kirby', 'lets_go_p', 'links_z',
   'luigis', 'mario_maker_2', 'mario_sonic', 'mario_tennis', 'minecraft', 'minecraft_dungeons',
   'minecraft_story', 'miscellanious_sonic', 'odyssey_m', 'oled_in_tv', 'party_m', 'rocket_league',
   'scarlet_p', 'shield_p', 'shining_p', 'skywards_z', 'smash_bros', 'snap_p',
   'splatoon_2', 'splatoon_3', 'super_m_party', 'super_mario_3d', 'switch_in_tv', 'switch_sports',
   'sword_p', 'tears_z', 'tv_black', 'tv_white', 'violet_p'
]
BANNED_PRICES = {
    59.00,
    49.00,
    17.00
}
MESSAGE_2_WORDS = {
    'cash only', 'must collect', 'only cash', 'no post', 'no delivery', 'pickup only', 'collect only',
    'pick up only', 'cash on collection', 'cash on pick up', 'cash on pickup', 'cash collection',
    'cash collect', 'cash pick up', 'cash pickup', 'i'
}

SD_CARD_WORD = {'sd card', 'sdcard', 'sd', 'card', 'memory card', 'memorycard', 'micro sd', 'microsd',
                'memory card', 'memorycard', 'sandisk', '128gb', '256gb', 'game'}

sd_card_revenue = 5

current_listing_price = "0"
duplicate_counter = 0
scanned_urls = []
current_listing_title = "No title"
current_listing_description = "No description"
current_listing_join_date = "No join date"
current_detected_items = "None"
current_expected_revenue= "0"
current_profit = "0"
current_suitability = "Suitability unknown"
current_listing_images = []
current_bounding_boxes = {}
suitable_listings = []
current_listing_index = 0
miscellaneous_games_price = 5
vinted_scraper_instance = None

BASE_PRICES = {
   '1_2_switch': 6.5, 'animal_crossing': 24, 'arceus_p': 27.5, 'bow_z': 28, 'bros_deluxe_m': 23.5,
   'comfort_h': 6,
   'controller': 8.5, 'crash_sand': 11, 'diamond_p': 26, 'evee': 25, 'fifa_23': 7.5, 'fifa_24': 14,
   'gta': 21, 'just_dance': 5, 'kart_m': 22, 'kirby': 29, 'lets_go_p': 25, 'links_z': 26,
   'lite': 52, 'luigis': 20, 'mario_maker_2': 19, 'mario_sonic': 14, 'mario_tennis': 12,
   'minecraft': 14,
   'minecraft_dungeons': 13, 'minecraft_story': 55, 'miscellanious_sonic': 15, 'odyssey_m': 23,
   'oled': 142, 'other_mario': 20,
   'party_m': 27, 'rocket_league': 13, 'scarlet_p': 26.5, 'shield_p': 25.5, 'shining_p': 25,
   'skywards_z': 26,
   'smash_bros': 24.5, 'snap_p': 19, 'splatoon_2': 7.5, 'splatoon_3': 25, 'super_m_party': 19.5,
   'super_mario_3d': 51,
   'switch': 64, 'switch_sports': 19, 'sword_p': 20, 'tears_z': 29, 'tv_black': 14.5, 'tv_white': 20.5,
   'violet_p': 26
}
scanned_unique_ids = set()

# Vinted-specific filtering variables (independent from Facebook)
vinted_title_must_contain = ["nintendo", "pokemon", "zelda", "mario", "animal crossing", "minecraft", 'oled', 'lite', 'pokémon', 'switch game',
                            'switch bundle', 'nintendo bundle', 'switch with games', 'modded switch']

vinted_title_forbidden_words = ['box only', 'unofficial', 'keyboard', 'mouse', 'ps4', 'ps5', 'sold', 'organizer', 'holder', 'joy con', 'gift', 'read des'
                               'joycon', 'snes', 'gamecube', 'n64', 'damaged', 'circuit', 'kart live', 'tablet only', 'ringfit', 'ring fit'
                               'repair', '™', 'each', 'empty game', 'just game case', 'empty case', 'arcade', 'wii', 'tv frame', 'joy-con',
                               'for parts', 'wont charge', 'spares & repair', 'xbox', 'prices in description', 'collector set', 'collectors set'
                                'joy pads', 'spares and repairs', 'neon', 'spares or repairs', 'dock cover', '3d print']

vinted_description_forbidden_words = ['faulty', 'jailbreak', 'visit us', 'opening hours', 'open 7 days', 
                                     'telephone', 'call us', '+44', '07', 'kart live', '.shop', 'our website',
                                     'website:', 'empty game', 'just game case', 'empty case', 'each', 'spares and repairs', 'prices are',
                                     'tablet only', 'not charge', 'stopped charging', 'doesnt charge', 'individually priced', 'per game',
                                     'https', 'case only', 'spares or repairs', 'dock cover', '3d print', 'spares & repair',
                                     'error code', 'will not connect']

vinted_min_price = 14
vinted_max_price = 500
vinted_banned_prices = {59.00, 49.00, 17.00}

if VM_DRIVER_USE:
    
    # Try to import noisereduce for advanced noise reduction
    try:
        import noisereduce as nr
        HAS_NOISEREDUCE = True
        print("noisereduce available - enhanced noise reduction enabled")
    except ImportError:
        HAS_NOISEREDUCE = False
        print("noisereduce not available - install with: pip install noisereduce")
    
    try:
        import pyaudiowpatch as pyaudio
        HAS_PYAUDIO = True
    except ImportError:
        HAS_PYAUDIO = False
        print("pyaudiowpatch not available - install with: pip install PyAudioWPatch")


def send_keypress_with_pyautogui(key, hold_time=None):
    """Send keypress using PyAutoGUI"""
    try:
        # Add human-like delay before keystroke
        time.sleep(random.uniform(0.05, 0.15))
        
        # Press the key
        pyautogui.press(key)
        
        # Optional hold time (though press() doesn't support hold)
        if hold_time:
            time.sleep(hold_time)
        else:
            time.sleep(random.uniform(0.05, 0.12))
        
        print(f"PyAutoGUI pressed key: {key}")
        return True
        
    except Exception as e:
        print(f"PyAutoGUI keystroke failed for {key}: {e}")
        return False

def clear_browser_data(vm_ip_address="192.168.56.101"):
    """
    Clear browser data before main execution using same VM profile
    """
    print("=" * 50)
    print("CLEARING BROWSER DATA...")
    print("=" * 50)
    
    clear_driver = None
    
    try:
        print("Step 1: Setting up temporary driver for data clearing...")
        
        # Use same Chrome options as main driver for consistency
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--user-data-dir=C:\VintedScraper_Default_Bookmark')
        chrome_options.add_argument('--profile-directory=Profile 4')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--force-device-scale-factor=1')
        chrome_options.add_argument('--high-dpi-support=1')
        chrome_options.add_argument('--remote-debugging-port=9223')  # Different port from main
        chrome_options.add_argument('--remote-allow-origins=*')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        
        # Create driver connection
        clear_driver = webdriver.Remote(
            command_executor=f'http://{vm_ip_address}:4444',
            options=chrome_options
        )
        
        print(f"✓ Temporary driver created successfully (Session: {clear_driver.session_id})")
        
        print("Step 2: Navigating to Chrome settings...")
        clear_driver.get("chrome://settings/clearBrowserData")
        print("✓ Navigated to clear browser data page")
        
        print("Step 3: Waiting for page to load...")
        time.sleep(2)  # Wait for Shadow DOM to initialize
        
        print("Step 4: Accessing Shadow DOM to find clear button...")
        
        # JavaScript to navigate Shadow DOM and click the clear button
        shadow_dom_script = """
        function findAndClickClearButton() {
            // Multiple strategies to find the clear button in Shadow DOM
            
            // Strategy 1: Direct access via settings-ui
            let settingsUi = document.querySelector('settings-ui');
            if (settingsUi && settingsUi.shadowRoot) {
                let clearBrowserData = settingsUi.shadowRoot.querySelector('settings-main')?.shadowRoot
                    ?.querySelector('settings-basic-page')?.shadowRoot
                    ?.querySelector('settings-section[section="privacy"]')?.shadowRoot
                    ?.querySelector('settings-clear-browsing-data-dialog');
                
                if (clearBrowserData && clearBrowserData.shadowRoot) {
                    let clearButton = clearBrowserData.shadowRoot.querySelector('#clearButton');
                    if (clearButton) {
                        console.log('Found clear button via strategy 1');
                        clearButton.click();
                        return true;
                    }
                }
            }
            
            // Strategy 2: Search all shadow roots recursively
            function searchShadowRoots(element) {
                if (element.shadowRoot) {
                    let clearButton = element.shadowRoot.querySelector('#clearButton');
                    if (clearButton) {
                        console.log('Found clear button via recursive search');
                        clearButton.click();
                        return true;
                    }
                    
                    // Search nested shadow roots
                    let shadowElements = element.shadowRoot.querySelectorAll('*');
                    for (let el of shadowElements) {
                        if (searchShadowRoots(el)) return true;
                    }
                }
                return false;
            }
            
            let allElements = document.querySelectorAll('*');
            for (let el of allElements) {
                if (searchShadowRoots(el)) return true;
            }
            
            // Strategy 3: Look for cr-button elements in shadow roots
            function findCrButton(element) {
                if (element.shadowRoot) {
                    let crButtons = element.shadowRoot.querySelectorAll('cr-button');
                    for (let btn of crButtons) {
                        if (btn.id === 'clearButton' || btn.textContent.includes('Delete data')) {
                            console.log('Found cr-button via strategy 3');
                            btn.click();
                            return true;
                        }
                    }
                    
                    let shadowElements = element.shadowRoot.querySelectorAll('*');
                    for (let el of shadowElements) {
                        if (findCrButton(el)) return true;
                    }
                }
                return false;
            }
            
            for (let el of allElements) {
                if (findCrButton(el)) return true;
            }
            
            console.log('Clear button not found in any shadow root');
            return false;
        }
        
        return findAndClickClearButton();
        """
        
        # Execute the Shadow DOM navigation script
        result = clear_driver.execute_script(shadow_dom_script)
        
        if result:
            print("✓ Successfully clicked clear data button via Shadow DOM!")
            print("Step 5: Waiting for data clearing to complete...")
            time.sleep(2)  # Wait for clearing process
            print("✓ Browser data clearing completed successfully!")
        else:
            print("✗ Failed to find clear button in Shadow DOM")
            
            # Fallback: Try to trigger clear via keyboard shortcut
            print("Attempting fallback: Ctrl+Shift+Delete shortcut...")
            try:
                from selenium.webdriver.common.keys import Keys
                body = clear_driver.find_element(By.TAG_NAME, "body")
                body.send_keys(Keys.CONTROL + Keys.SHIFT + Keys.DELETE)
                time.sleep(1)
                # Try to press Enter to confirm
                body.send_keys(Keys.ENTER)
                time.sleep(1)
                print("✓ Fallback keyboard shortcut attempted")
            except Exception as fallback_error:
                print(f"✗ Fallback also failed: {fallback_error}")
        
    except Exception as e:
        print(f"✗ Browser data clearing failed: {str(e)}")
        print("Continuing with main execution anyway...")
        import traceback
        traceback.print_exc()
    
    finally:
        if clear_driver:
            try:
                print("Step 6: Closing temporary driver...")
                clear_driver.quit()
                print("✓ Temporary driver closed successfully")
            except Exception as e:
                print(f"Warning: Failed to close temporary driver: {e}")
        
        print("=" * 50)
        print("BROWSER DATA CLEAR COMPLETE")
        print("=" * 50)
        time.sleep(0.5)  # Brief pause before continuing

def setup_driver(vm_ip_address="192.168.56.101"):
    
    # Session cleanup (existing code)
    try:
        import requests
        status_response = requests.get(f"http://{vm_ip_address}:4444/status", timeout=5)
        status_data = status_response.json()
        
        if 'value' in status_data and 'nodes' in status_data['value']:
            for node in status_data['value']['nodes']:
                if 'slots' in node:
                    for slot in node['slots']:
                        if slot.get('session'):
                            session_id = slot['session']['sessionId']
                            print(f"Found existing session: {session_id}")
                            delete_response = requests.delete(
                                f"http://{vm_ip_address}:4444/session/{session_id}",
                                timeout=10
                            )
                            print(f"Cleaned up session: {session_id}")
    
    except Exception as e:
        print(f"Session cleanup failed: {e}")
    
    # Chrome options for the VM instance (existing code continues...)
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--user-data-dir=C:\VintedScraper_Default_Bookmark')
    chrome_options.add_argument('--profile-directory=Profile 4')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # VM-specific optimizations

    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')

    
    print(f"Chrome options configured: {len(chrome_options.arguments)} arguments")
    
    driver = None
    
    try:
        print("Attempting to connect to remote WebDriver...")
        
        driver = webdriver.Remote(
            command_executor=f'http://{vm_ip_address}:4444',
            options=chrome_options
        )
        
        print(f"✓ Successfully created remote WebDriver connection")
        print(f"Session ID: {driver.session_id}")
        
        print("Applying stealth modifications...")
        stealth_script = """
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
        Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
        window.chrome = {runtime: {}};
        Object.defineProperty(navigator, 'permissions', {get: () => ({query: () => Promise.resolve({state: 'granted'})})});
        
        Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 4});
        Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});
        Object.defineProperty(screen, 'colorDepth', {get: () => 24});
        """
        driver.execute_script(stealth_script)
        print("✓ Stealth script applied successfully")
        
        print(f"✓ Successfully connected to VM Chrome with clean profile")
        return driver
        
    except Exception as e:
        print(f"✗ Failed to connect to VM WebDriver")
        print(f"Error: {str(e)}")
        
        if driver:
            try:
                driver.quit()
            except:
                pass
        
        return None
    
def handle_datadome_audio_captcha(driver):
    """Enhanced function to handle DataDome audio captcha with nested iframes"""
    print("Attempting to handle DataDome audio captcha...")
    
    try:
        # Wait a bit for any dynamic content to load
        time.sleep(random.uniform(2, 4))
        
        # Check for "x new messages" element first to see if captcha is present
        max_checks = 6  # Check for about 30 seconds total (6 checks * 5 seconds each)
        check_count = 0
        
        while check_count < max_checks:
            print(f"Check {check_count + 1}/{max_checks}: Looking for 'new messages' element...")
            
            try:
                # Look for the "x new messages" element
                messages_element = driver.find_element(
                    By.CSS_SELECTOR, 
                    'a[data-testid="header-conversations-button"]'
                )
                print("Found 'new messages' element - no captcha present!")
                print("Returning 'no_captcha' - should NOT start audio detection")
                return "no_captcha"  # No captcha to solve
                
            except:
                print("'New messages' element not found, checking for captcha iframe...")
                
                # Step 1: Find and switch to the main DataDome captcha iframe
                iframe_selectors = [
                    "iframe[src*='captcha']",  # This was the working one from your logs
                    "iframe[src*='datadome']",
                    "iframe[id*='datadome']",
                    "iframe[class*='datadome']",
                    "iframe[title*='captcha']",
                    "iframe[title*='DataDome']"
                ]
                
                iframe_found = False
                for selector in iframe_selectors:
                    try:
                        iframe = driver.find_element(By.CSS_SELECTOR, selector)
                        print(f"Found captcha iframe with selector: {selector}")
                        driver.switch_to.frame(iframe)
                        iframe_found = True
                        break
                    except:
                        continue
                
                if iframe_found:
                    # Found captcha iframe, break out of the checking loop and proceed with captcha
                    break
                else:
                    print(f"No captcha iframe found in check {check_count + 1}")
                    check_count += 1
                    if check_count < max_checks:
                        print("Waiting 5 seconds before next check...")
                        time.sleep(5)
                    continue
        
        if check_count >= max_checks:
            print("No captcha found after all checks - assuming no captcha needed")
            return "no_captcha"
        
        # Step 2: Click the initial audio button (captcha__audio__button)
        print("Switched to captcha iframe, looking for initial audio button...")
        
        try:
            initial_audio_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "captcha__audio__button"))
            )
            
            print("Found initial audio button with ID: captcha__audio__button")
            
            # Enhanced clicking with human-like behavior
            human_like_delay()
            
            # Scroll element into view if needed
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", initial_audio_element)
            time.sleep(random.uniform(0.5, 1))
            
            # Move and click
            action = move_to_element_naturally(driver, initial_audio_element)
            time.sleep(random.uniform(0.2, 0.5))
            action.click().perform()
            
            print("Successfully clicked initial audio button!")
            
            # Step 3: Wait for nested iframe or audio play button to appear
            time.sleep(random.uniform(2, 4))
            
            # Step 4: Look for the audio play button (could be in nested iframe or same iframe)
            print("Looking for audio captcha play button...")
            
            # First try to find it in the current iframe context
            play_button_selectors = [
                ".audio-captcha-play-button",
                "button[class*='audio-captcha-play-button']",
                "button[name='Listen to the numbers to write']",
                "button[title='Listen to the numbers to write']",
                "[class*='play-button']",
                "[class*='audio'][class*='play']"
            ]
            
            play_button_found = False
            for selector in play_button_selectors:
                try:
                    play_element = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    
                    print(f"Found play button with selector: {selector}")
                    
                    # Enhanced clicking with human-like behavior
                    human_like_delay()
                    
                    # Scroll element into view
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", play_element)
                    time.sleep(random.uniform(0.5, 1))
                    
                    # Move and click with natural behavior
                    action = move_to_element_naturally(driver, play_element)
                    time.sleep(random.uniform(0.3, 0.7))
                    action.click().perform()
                    
                    print("Successfully clicked audio play button!")
                    play_button_found = True
                    break
                    
                except Exception as e:
                    print(f"Play button selector {selector} failed: {e}")
                    continue
            
            # Step 5: If not found in current iframe, check for nested iframes
            if not play_button_found:
                print("Play button not found in current iframe, checking for nested iframes...")
                
                try:
                    # Look for any nested iframes within the current captcha iframe
                    nested_iframes = driver.find_elements(By.TAG_NAME, "iframe")
                    print(f"Found {len(nested_iframes)} nested iframes")
                    
                    for i, nested_iframe in enumerate(nested_iframes):
                        try:
                            print(f"Trying nested iframe {i}...")
                            driver.switch_to.frame(nested_iframe)
                            
                            # Try to find the play button in this nested iframe
                            for selector in play_button_selectors:
                                try:
                                    play_element = WebDriverWait(driver, 3).until(
                                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                                    )
                                    
                                    print(f"Found play button in nested iframe {i} with selector: {selector}")
                                    
                                    # Enhanced clicking
                                    human_like_delay()
                                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", play_element)
                                    time.sleep(random.uniform(0.5, 1))
                                    
                                    action = move_to_element_naturally(driver, play_element)
                                    time.sleep(random.uniform(0.3, 0.7))
                                    action.click().perform()
                                    
                                    print("Successfully clicked audio play button in nested iframe!")
                                    driver.switch_to.default_content()
                                    return True
                                    
                                except:
                                    continue
                            
                            # Switch back to parent iframe if button not found in this nested iframe
                            driver.switch_to.parent_frame()
                            
                        except Exception as e:
                            print(f"Error with nested iframe {i}: {e}")
                            try:
                                driver.switch_to.parent_frame()
                            except:
                                # If parent_frame fails, go back to main iframe
                                driver.switch_to.default_content()
                                for selector in iframe_selectors:
                                    try:
                                        iframe = driver.find_element(By.CSS_SELECTOR, selector)
                                        driver.switch_to.frame(iframe)
                                        break
                                    except:
                                        continue
                            continue
                
                except Exception as e:
                    print(f"Error searching nested iframes: {e}")
            
            driver.switch_to.default_content()
            return play_button_found
            
        except Exception as e:
            print(f"Failed to find or click initial audio button: {e}")
            driver.switch_to.default_content()
            return False
        
    except Exception as e:
        print(f"Error in handle_datadome_audio_captcha: {e}")
        driver.switch_to.default_content()
        return False

def wait_and_click(driver, by, value, timeout=10):
    """Wait for element and click with human-like behavior"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        
        # Random delay before interaction
        human_like_delay()
        
        # Move to element naturally
        action = move_to_element_naturally(driver, element)
        
        # Random pause before clicking
        time.sleep(random.uniform(0.1, 0.3))
        
        # Perform the click
        action.click().perform()
        
        print(f"Clicked element: {value}")
        return True
        
    except TimeoutException:
        print(f"Element not found: {value}")
        return False

def human_typing_delay():
    """Simulate realistic human typing delays"""
    return random.uniform(0.08, 0.25)

def human_like_delay():
    """Random delay to mimic human behavior"""
    time.sleep(random.uniform(0.5, 2.0))

def move_to_element_naturally(driver, element):
    """Move mouse to element with slight randomness"""
    action = ActionChains(driver)
    
    # Add small random offset to make it more natural
    offset_x = random.randint(-3, 3)
    offset_y = random.randint(-3, 3)
    
    # Move to element with slight offset, then to exact element
    action.move_to_element_with_offset(element, offset_x, offset_y)
    time.sleep(random.uniform(0.1, 0.3))
    action.move_to_element(element)
    time.sleep(random.uniform(0.2, 0.5))
    return action

def main_vm_driver():
    """
    MODIFIED: Main VM driver function that handles login AND bookmarking
    THIS ALL OCCURS IN THE VM - BOTH LOGIN AND BOOKMARKING
    """
    # VM IP address - change this to your VM's IP
    vm_ip_address = "192.168.56.101"  # Replace with your actual VM IP
    
    # Clear browser data first using same VM profile
    clear_browser_data(vm_ip_address)
    
    # Small delay before creating main driver
    time.sleep(1)
    
    driver = setup_driver(vm_ip_address)
    
    if not driver:
        print("Failed to create VM driver - exiting")
        return
    
    detector = None
    
    try:
        print("=" * 60)
        print("STEP 1: EXECUTING ALL VM_DRIVER_USE FUNCTIONALITY")
        print("=" * 60)
        
        print("Navigating to vinted.co.uk...")
        driver.get("https://vinted.co.uk")
        
        # Random delay after page load
        human_like_delay()
        
        # Wait for and accept cookies
        print("Waiting for cookie consent button...")
        if wait_and_click(driver, By.ID, "onetrust-accept-btn-handler", 15):
            print("Cookie consent accepted")
        else:
            print("Cookie consent button not found, continuing...")
        
        # Small delay after cookie acceptance
        time.sleep(random.uniform(1, 2))
        
        # Click Sign up | Log in button
        print("Looking for Sign up | Log in button...")
        signup_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="header--login-button"]'))
        )
        
        human_like_delay()
        action = move_to_element_naturally(driver, signup_button)
        time.sleep(random.uniform(0.1, 0.3))
        action.click().perform()
        print("Clicked Sign up | Log in button")
        
        # Wait for the login/signup modal to appear
        time.sleep(random.uniform(1, 2))
        
        if google_login:
            print("Using Google login...")
            # Click Continue with Google
            google_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="google-oauth-button"]'))
            )
            
            human_like_delay()
            action = move_to_element_naturally(driver, google_button)
            time.sleep(random.uniform(0.1, 0.3))
            action.click().perform()
            print("Clicked Continue with Google")
            
        else:
            print("Using email login...")
            
            # Click "Log in" text
            login_text = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'web_ui__Text__underline') and text()='Log in']"))
            )
            
            human_like_delay()
            action = move_to_element_naturally(driver, login_text)
            time.sleep(random.uniform(0.1, 0.3))
            action.click().perform()
            print("Clicked Log in")
            
            # Wait a bit for the form to update
            time.sleep(random.uniform(0.5, 1))
            
            # Click "email" text
            email_text = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'web_ui__Text__underline') and text()='email']"))
            )
            
            human_like_delay()
            action = move_to_element_naturally(driver, email_text)
            time.sleep(random.uniform(0.1, 0.3))
            action.click().perform()
            print("Clicked email")
            
            # Wait a bit for the form to update
            time.sleep(random.uniform(0.5, 1))
            
            # Click Continue button
            continue_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']//span[text()='Continue']"))
            )
            
            human_like_delay()
            action = move_to_element_naturally(driver, continue_button)
            time.sleep(random.uniform(0.1, 0.3))
            action.click().perform()
            print("Clicked Continue")
        
        # Wait a bit for any redirects or page loads after login flow
        time.sleep(random.uniform(3, 5))
        
        # Handle captcha using only the working method
        result = handle_datadome_audio_captcha(driver)

        if result == "no_captcha":
            print("No captcha present - login successful!")
            print("=" * 60)
            print("STEP 1 COMPLETE: VM_DRIVER_USE FUNCTIONALITY FINISHED")
            print("=" * 60)
            
        elif result == True:
            print("Audio captcha button clicked successfully!")
            print("="*60)
            print("STARTING AUDIO DETECTION...")
            print("="*60)
            
            # Initialize and start audio detection with driver reference
            if HAS_PYAUDIO:
                detector = AudioNumberDetector(driver=driver)
                detector.start_listening()
                
                # WAIT FOR AUDIO DETECTION TO COMPLETE
                print("Waiting for audio detection to complete...")
                while detector.is_running:
                    time.sleep(1)
                    
                print("Audio detection completed!")
            else:
                print("ERROR: Cannot start audio detection - pyaudiowpatch not available")
                return
        else:
            print("Failed to click audio captcha button")
            return
        
        # ========================================
        # STEP 2: NOW START BOOKMARKING IN THE VM
        # ========================================
        print("=" * 60)
        print("STEP 2: STARTING VM BOOKMARKING PROCESS")
        print("THIS ALL OCCURS IN THE VM!")
        print("=" * 60)
        
        # Store the main tab handle
        main_tab = driver.current_window_handle
        print(f"Main tab stored: {main_tab}")
        
        # Start the VM bookmarking process
        start_vm_bookmarking_process(driver, main_tab)
        
        print("Script completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\nStopping script...")
        if detector:
            detector.stop()
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if detector:
            try:
                detector.stop()
            except:
                pass
        # Keep browser open - do not close driver automatically
        print("VM driver remaining open for manual inspection...")
        pass

def start_vm_bookmarking_process(driver, main_tab):
    """
    Updated to use the ultra-fast streamlined version
    """
    print("🔖 VM BOOKMARK: Starting ultra-fast bookmarking process...")
    
    # Your test URL and username
    test_url = "https://www.vinted.co.uk/items/7059487716-2-x-wolves-croc-charm-bundle-new?referrer=catalog"
    test_username = "test_user"
    
    try:
        success = execute_vm_bookmark_enhanced_fast(driver, main_tab, test_url, test_username)
        
        if success:
            print("✅ VM BOOKMARK: Ultra-fast bookmark process completed successfully")
        else:
            print("❌ VM BOOKMARK: Ultra-fast bookmark process failed")
            
    except Exception as e:
        print(f"❌ VM BOOKMARK ERROR: {e}")

def execute_vm_bookmark(driver, main_tab, listing_url, username):
    """
    MODIFIED: Execute bookmark functionality within the VM
    THIS REPLICATES YOUR EXISTING BOOKMARK LOGIC BUT USES THE VM DRIVER
    """
    print(f"🔖 VM EXECUTING: Bookmarking {listing_url}")
    print(f"👤 VM USERNAME: {username}")
    
    try:
        # STEP 1: Open new tab for bookmarking (just like your existing logic)
        print("🔖 VM: Opening new tab for bookmark process...")
        driver.execute_script("window.open('');")
        bookmark_tab = driver.window_handles[-1]
        driver.switch_to.window(bookmark_tab)
        print("✅ VM: New bookmark tab opened")
        
        # STEP 2: Navigate to the listing URL
        print(f"🔖 VM: Navigating to {listing_url}")
        driver.get(listing_url)
        
        # Wait for page to load
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print("✅ VM: Page loaded successfully")
        except TimeoutException:
            print("❌ VM: Timeout waiting for page to load")
            return False
        
        # STEP 3: Execute the first buy sequence (replicating your existing logic)
        print("🔖 VM: Starting first buy sequence...")
        first_sequence_success = enhanced_execute_vm_first_buy_sequence(driver)
        
        if not first_sequence_success:
            print("❌ VM: First buy sequence failed")
            return False
        
        # STEP 4: Execute the second sequence with monitoring
        print("🔖 VM: Starting second sequence with monitoring...")
        second_sequence_success = execute_vm_second_sequence(driver, listing_url, username)
        
        if second_sequence_success:
            print("✅ VM: Both sequences completed successfully")
            return True
        else:
            print("❌ VM: Second sequence failed")
            return False
            
    except Exception as e:
        print(f"❌ VM BOOKMARK EXECUTION ERROR: {e}")
        return False
        
    finally:
        # Clean up bookmark tab and return to main tab
        try:
            if len(driver.window_handles) > 1:
                driver.close()  # Close current bookmark tab
                driver.switch_to.window(main_tab)  # Return to main tab
                print("✅ VM: Returned to main tab")
        except Exception as cleanup_error:
            print(f"⚠️ VM CLEANUP ERROR: {cleanup_error}")

def find_buy_button_with_shadow_dom_support(driver, timeout=5):
    """
    ULTRA FAST: Force Click primary method with minimal fallbacks
    """
    print("🔍 ULTRA FAST: Finding buy button...")
    
    # SPEED: Primary selector that works (Force Click compatible)
    shadow_dom_search_script = """
    function findBuyButtonUltraFast() {
        // PRIMARY: Direct testid selector (this worked in your log)
        try {
            const btn = document.querySelector('button[data-testid="item-buy-button"]');
            if (btn) {
                btn.setAttribute('data-vinted-found', 'primary');
                console.log('PRIMARY: Found via data-testid');
                return { found: true, method: 'primary_testid' };
            }
        } catch (e) {}
        
        // FALLBACK 1: Any button with buy in testid
        try {
            const btn = document.querySelector('button[data-testid*="buy"]');
            if (btn) {
                btn.setAttribute('data-vinted-found', 'fallback1');
                console.log('FALLBACK1: Found via testid wildcard');
                return { found: true, method: 'fallback1_testid' };
            }
        } catch (e) {}
        
        // FALLBACK 2: Quick button scan
        const buttons = document.querySelectorAll('button');
        for (let i = 0; i < Math.min(buttons.length, 10); i++) {
            const btn = buttons[i];
            const testId = btn.getAttribute('data-testid') || '';
            const text = (btn.textContent || '').toLowerCase();
            
            if (testId.includes('buy') || text.includes('buy now') || text.includes('buy')) {
                btn.setAttribute('data-vinted-found', 'fallback2');
                console.log('FALLBACK2: Found via scan');
                return { found: true, method: 'fallback2_scan' };
            }
        }
        
        return { found: false };
    }
    return findBuyButtonUltraFast();
    """
    
    try:
        search_result = driver.execute_script(shadow_dom_search_script)
        
        if search_result.get('found'):
            print(f"✅ ULTRA FAST: Buy button found via {search_result.get('method')}")
            buy_button = driver.find_element(By.CSS_SELECTOR, '[data-vinted-found]')
            return buy_button
        else:
            print("❌ ULTRA FAST: No buy button found")
            return None
            
    except Exception as e:
        print(f"❌ ULTRA FAST: Search failed: {e}")
        return None


def click_buy_button_force_method(driver, buy_button):
    """
    MINIMAL FIX: Handle stale element reference in fallback
    """
    print("🔄 FORCE CLICK: Using successful method...")
    
    try:
        # PREVIOUS METHOD@ FROM WHAT I CANT TELL NOT WORKING
        #driver.execute_script("arguments[0].disabled=false; arguments[0].click();", buy_button)
        #print("✅ FORCE CLICK: Primary method successful")
        
        # Quick success check
        #time.sleep(0.5)  # Minimal wait
        #print('initial click, 0.5s wait done')
        #current_url = driver.current_url
        
        #if 'checkout' in current_url or 'payment' in current_url:
        #    return True
        #else:
        #print("⚠️ FORCE CLICK: No navigation detected, trying fallback...")
        
        # MINIMAL FIX: Re-find the buy button instead of using stale element
        try:
            # Re-find the buy button (it may have changed after the first click)
            fresh_buy_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="item-buy-button"]')
            driver.execute_script("arguments[0].click();", fresh_buy_button)

            try:

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-testid="single-checkout-order-summary-purchase-button"]'))
                )
                print('Pay button found, continuing')
            except TimeoutException:
                
                print('Error: Pay button not found within 10 seconds')

            return 'checkout' in driver.current_url or 'payment' in driver.current_url
        
        except Exception as refind_error:
            print(f"❌ FORCE CLICK: Could not re-find buy button: {refind_error}")
            return False
            
    except Exception as e:
        print(f"❌ FORCE CLICK: Failed - {e}")
        return False


def wait_for_pay_button_with_timeout(driver, timeout=8):
    """
    Wait up to 8 seconds for pay button, continue immediately when found
    """
    print(f"💳 PAY BUTTON WAIT: Waiting up to {timeout} seconds for pay button...")
    
    start_time = time.time()
    check_interval = 0.2  # Check every 200ms
    
    while time.time() - start_time < timeout:
        try:
            pay_button = driver.find_element(By.CSS_SELECTOR, 
                'button[data-testid="single-checkout-order-summary-purchase-button"]')
            
            if pay_button:
                elapsed = time.time() - start_time
                print(f"✅ PAY BUTTON FOUND: Found after {elapsed:.2f} seconds!")
                return pay_button
                
        except:
            pass  # Button not found yet
        
        time.sleep(check_interval)
    
    print(f"❌ PAY BUTTON TIMEOUT: Not found after {timeout} seconds")
    return None

def handle_shipping_options(driver, pay_button):
    """
    FIXED: Handle pickup/postage sequence like the original bookmarking
    This replicates the logic from execute_first_buy_sequence
    """
    print("🚢 SHIPPING: Starting pickup/postage sequence...")
    
    try:
        # Check if we're on the shipping selection page
        # Look for "Ship to pick-up point" option
        try:
            pickup_element = driver.find_element(
                By.XPATH, 
                '//h2[@class="web_ui__Text__text web_ui__Text__title web_ui__Text__left" and text()="Ship to pick-up point"]'
            )
            print("📦 SHIPPING: Found 'Ship to pick-up point' option")
            
            # Check if pickup is currently selected by looking for aria-checked="true"
            try:
                pickup_selected_element = driver.find_element(
                    By.XPATH, 
                    '//div[@data-testid="delivery-option-pickup" and @aria-checked="true"]'
                )
                pickup_is_selected = True
                print("📦 SHIPPING: Pick-up point is currently selected")
            except:
                pickup_is_selected = False
                print("🏠 SHIPPING: Ship to home is currently selected")
            
            # If pickup is selected, check for "Choose a pick-up point" message
            if pickup_is_selected:
                try:
                    choose_pickup_element = driver.find_element(
                        By.XPATH,
                        '//h2[@class="web_ui__Text__text web_ui__Text__title web_ui__Text__left" and text()="Choose a pick-up point"]'
                    )
                    
                    print("⚠️ SHIPPING: 'Choose a pick-up point' message found - need to switch to Ship to home")
                    
                    # Click "Ship to home" to avoid the pickup point selection
                    try:
                        ship_home_element = driver.find_element(
                            By.XPATH,
                            '//h2[@class="web_ui__Text__text web_ui__Text__title web_ui__Text__left" and text()="Ship to home"]'
                        )
                        ship_home_element.click()
                        print("🏠 SHIPPING: Successfully switched to 'Ship to home'")
                        
                        # Wait for the page to update (0.3 seconds like in original code)
                        time.sleep(2)
                        
                        # Re-find the pay button after shipping change
                        print("🔍 SHIPPING: Re-finding pay button after shipping change...")
                        new_pay_button = wait_for_pay_button_with_timeout(driver, timeout=5)
                        
                        if new_pay_button:
                            print("✅ SHIPPING: Pay button re-found after shipping change")
                            return new_pay_button
                        else:
                            print("⚠️ SHIPPING: Could not re-find pay button, using original")
                            return pay_button
                            
                    except Exception as switch_error:
                        print(f"❌ SHIPPING: Could not switch to Ship to home: {switch_error}")
                        return pay_button
                        
                except:
                    # No "Choose a pick-up point" message, pickup is ready
                    print("✅ SHIPPING: Pick-up point is ready (no selection required)")
                    return pay_button
            else:
                # Ship to home is already selected
                print("✅ SHIPPING: Ship to home already selected - no changes needed")
                return pay_button
                
        except:
            # No shipping options found, might already be on payment page
            print("ℹ️ SHIPPING: No shipping options found - might already be on payment page")
            return pay_button
            
    except Exception as shipping_error:
        print(f"❌ SHIPPING ERROR: {shipping_error}")
        print("🔄 SHIPPING: Continuing with original pay button")
        return pay_button

def find_buy_button_traditional_fallback(driver):
    """
    FAST: Traditional search with aggressive timeouts
    """
    print("🔄 FALLBACK: Starting FAST traditional search...")
    
    # SPEED: Most likely selectors first
    fast_selectors = [
        'button[data-testid="item-buy-button"]',
        '//button[@data-testid="item-buy-button"]',
        'button.web_ui__Button__primary[data-testid="item-buy-button"]',
        '//button[contains(@class, "web_ui__Button__primary")]//span[text()="Buy now"]',
        '[role="button"][data-testid*="buy"]'
    ]
    
    for i, selector in enumerate(fast_selectors):
        try:
            print(f"🔍 FALLBACK: Selector {i+1}/{len(fast_selectors)}")
            
            # SPEED: Aggressive 2-second timeout per selector
            if selector.startswith('//'):
                element = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
            else:
                element = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
            
            print(f"✅ FALLBACK: Found with selector {i+1}")
            return element
            
        except TimeoutException:
            continue  # SPEED: No logging for timeouts
        except:
            continue  # SPEED: Skip failed selectors immediately
    
    print("❌ FALLBACK: No buy button found")
    return None

def handle_payment_page_logic(driver):
    """
    ULTRA FAST: Payment page with minimal delays
    """
    print("💳 VM FIRST: ULTRA FAST payment handling...")
    
    # SPEED: Quick pay button find
    try:
        pay_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 
                'button[data-testid="single-checkout-order-summary-purchase-button"]'))
        )
        
        # SPEED: Immediate click
        pay_button.click()
        print("💳 VM FIRST: Pay button clicked")
        
        # CRITICAL: Your exact timing requirement
        time.sleep(0.25)
        
        # CRITICAL: Close tab immediately
        driver.close()
        
        # Return to main tab
        if len(driver.window_handles) > 0:
            driver.switch_to.window(driver.window_handles[0])
            print("✅ VM FIRST: Back to main tab")
        
        return True
        
    except Exception as e:
        print(f"❌ VM FIRST: Payment failed - {e}")
        return False


def debug_page_structure_fast(driver):
    """
    FAST: Quick page analysis for debugging
    """
    debug_script = """
    function quickAnalysis() {
        const buttons = document.querySelectorAll('button, [role="button"]');
        const shadowRoots = Array.from(document.querySelectorAll('*')).filter(el => el.shadowRoot);
        
        return {
            url: window.location.href,
            readyState: document.readyState,
            buttonCount: buttons.length,
            shadowCount: shadowRoots.length,
            topButtons: Array.from(buttons).slice(0, 5).map(btn => ({
                text: btn.textContent?.trim() || '',
                testId: btn.getAttribute('data-testid') || '',
                className: btn.className || ''
            }))
        };
    }
    return quickAnalysis();
    """
    
    try:
        analysis = driver.execute_script(debug_script)
        print(f"🔍 FAST DEBUG: {analysis['buttonCount']} buttons, {analysis['shadowCount']} shadow roots on {analysis['url']}")
        if analysis['topButtons']:
            for i, btn in enumerate(analysis['topButtons']):
                print(f"  Button {i+1}: '{btn['text'][:20]}' testId='{btn['testId']}'")
    except Exception as debug_error:
        print(f"❌ FAST DEBUG: {debug_error}")


def execute_vm_bookmark_enhanced_fast(driver, main_tab, listing_url, username):
    """
    STREAMLINED: Ultra-fast bookmark execution with fixed second sequence
    """
    print(f"🚀 VM ULTRA FAST: Bookmarking {listing_url[:50]}...")
    
    try:
        # SPEED: Quick tab creation
        driver.execute_script("window.open('');")
        bookmark_tab = driver.window_handles[-1]
        driver.switch_to.window(bookmark_tab)
        
        # SPEED: Fast navigation
        driver.get(listing_url)
        WebDriverWait(driver, 3).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        
        # SPEED: Minimal wait
        time.sleep(0.5)
        
        # Execute ultra-fast first sequence
        first_success = enhanced_execute_vm_first_buy_sequence(driver)
        
        if not first_success:
            print("❌ VM ULTRA FAST: First sequence failed")
            return False
        
        # FIXED: Execute second sequence with proper buy button click
        second_success = execute_vm_second_sequence(driver, listing_url, username)
        
        if second_success:
            print("🎉 VM ULTRA FAST: Bookmark completed successfully!")
            return True
        else:
            print("❌ VM ULTRA FAST: Second sequence failed")
            return False
            
    except Exception as e:
        print(f"❌ VM ULTRA FAST: Error - {e}")
        return False
        
    finally:
        # Quick cleanup
        try:
            if len(driver.window_handles) > 1:
                driver.close()
                driver.switch_to.window(main_tab)
        except:
            pass


def execute_critical_pay_sequence(driver, pay_button):
    """
    Execute the critical 0.25s wait + close sequence
    """
    try:
        print("💳 VM FIRST: Executing critical pay sequence...")
        
        # Click the pay button
        pay_button.click()
        print("✅ VM FIRST: Pay button clicked")
        
        # CRITICAL: Exact 0.25 second wait
        time.sleep(0.25)
        
        # CRITICAL: Close tab immediately
        driver.close()
        
        # Return to main tab
        if len(driver.window_handles) > 0:
            driver.switch_to.window(driver.window_handles[0])
            print("✅ VM FIRST: Back to main tab")
        
        return True
        
    except Exception as e:
        print(f"❌ VM FIRST: Critical sequence failed - {e}")
        return False

def enhanced_execute_vm_first_buy_sequence(driver):
    """
    ULTRA FAST: Streamlined first sequence using proven Force Click method
    """
    print("🔖 VM FIRST: ULTRA FAST first sequence...")
    
    # SPEED: Quick buy button detection
    buy_button = find_buy_button_with_shadow_dom_support(driver, timeout=5)
    
    if buy_button is None:
        print("❌ VM FIRST: No buy button found")
        return False
    
    # SPEED: Use the proven Force Click method immediately
    if not click_buy_button_force_method(driver, buy_button):
        print("❌ VM FIRST: Force click failed")
        return False
    
    # SPEED: Quick payment page handling
    return handle_payment_page_logic(driver)


def execute_vm_second_sequence(driver, listing_url, username):
    """
    MINIMAL FIX: Re-find buy button instead of using potentially stale element
    """
    print("🔖 VM SECOND: Starting FIXED second sequence...")
    
    try:
        # Open new tab for second sequence
        driver.execute_script("window.open('');")
        second_tab = driver.window_handles[-1]
        driver.switch_to.window(second_tab)
        print("✅ VM SECOND: New tab opened")
        
        # Navigate to listing
        driver.get(listing_url)
        WebDriverWait(driver, 5).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        print("✅ VM SECOND: Navigated to listing")
        
        # MINIMAL FIX: Find buy button fresh (don't reuse from first tab)
        print("🔄 VM SECOND: Finding buy button on second tab...")
        
        try:
            # Find buy button fresh on this tab
            buy_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="item-buy-button"]')
            print("✅ VM SECOND: Buy button found on second tab")
            
            # Click it using JavaScript (most reliable)
            driver.execute_script("arguments[0].disabled=false; arguments[0].click();", buy_button)
            print("✅ VM SECOND: Buy button clicked on second tab")
            
        except Exception as buy_error:
            print(f"❌ VM SECOND: Buy button click failed: {buy_error}")
            return False
        
        # Look for 'Processing payment' message
        print("🔍 VM SECOND: Looking for 'Processing payment' message...")
        processing_found = check_for_processing_payment(driver)
        
        if processing_found:
            print("🎉 VM SECOND: 'Processing payment' found - bookmark successful!")
            return True
        else:
            print("⚠️ VM SECOND: No 'Processing payment' found")
            return False
        
    except Exception as e:
        print(f"❌ VM SECOND: Error - {e}")
        return False
    
    finally:
        # Clean up second tab
        try:
            if len(driver.window_handles) > 1:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
        except:
            pass

def check_for_processing_payment(driver):
    """
    CONTINUOUS: Check for 'Processing payment' message with 10-second timeout
    """
    print("🔍 VM SECOND: Continuously checking for 'Processing payment'...")
    
    processing_selectors = [
        "//h2[text()='Processing payment']",
        "//h2[@class='web_ui__Text__text web_ui__Text__title web_ui__Text__left' and text()='Processing payment']",
        "//*[contains(text(), 'Processing payment')]",
        "//*[contains(text(), \"We've reserved this item for you until your payment finishes processing\")]"
    ]
    
    # CONTINUOUS checking with 10-second timeout
    for selector in processing_selectors:
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, selector))
            )
            print("✅ VM SECOND: 'Processing payment' message found instantly!")
            return True
        except TimeoutException:
            continue
    
    print("❌ VM SECOND: 'Processing payment' message not found after 10 seconds")
    return False


def wait_for_purchase_unsuccessful(driver, listing_url, username):
    """
    FAST: Wait for 'Purchase unsuccessful' message
    """
    print("⏳ VM SECOND: Waiting for 'Purchase unsuccessful' message...")
    
    # Register this URL for monitoring (from your existing global system)
    global purchase_unsuccessful_detected_urls
    purchase_unsuccessful_detected_urls[listing_url] = {
        'waiting': True,
        'start_time': time.time()
    }
    
    unsuccessful_selectors = [
        "//h2[text()='Purchase unsuccessful']",
        "//h2[@class='web_ui__Text__text web_ui__Text__title web_ui__Text__left web_ui__Text__warning' and text()='Purchase unsuccessful']",
        "//*[contains(text(), 'Purchase unsuccessful')]"
    ]
    
    # Wait up to 30 seconds for 'Purchase unsuccessful'
    for attempt in range(30):  # 30 seconds total
        for selector in unsuccessful_selectors:
            try:
                element = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                print("🎯 VM SECOND: 'Purchase unsuccessful' detected!")
                
                # Signal to buying drivers
                if listing_url in purchase_unsuccessful_detected_urls:
                    purchase_unsuccessful_detected_urls[listing_url]['waiting'] = False
                
                return True
                
            except TimeoutException:
                continue
        
        print(f"⏳ VM SECOND: Waiting... attempt {attempt + 1}/30")
        time.sleep(1)
    
    print("⏰ VM SECOND: Timeout waiting for 'Purchase unsuccessful'")
    return False

def check_vm_processing_payment(driver):
    """
    Check for processing payment message in VM
    """
    processing_selectors = [
        "//h2[@class='web_ui__Text__text web_ui__Text__title web_ui__Text__left' and text()='Processing payment']",
        "//h2[contains(@class, 'web_ui__Text__title') and text()='Processing payment']",
        "//span[contains(text(), \"We've reserved this item for you until your payment finishes processing\")]",
        "//*[contains(text(), 'Processing payment')]"
    ]
    
    for selector in processing_selectors:
        try:
            element = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, selector))
            )
            print("🎉 VM: Processing payment message found!")
            return True
        except TimeoutException:
            continue
    
    print("❌ VM: Processing payment message not found")
    return False

def execute_vm_messages_sequence(driver, listing_url, username):
    """
    Execute messages sequence in VM (your existing logic)
    """
    print("📧 VM MESSAGES: Starting messages sequence...")
    
    try:
        # Open messages tab
        driver.execute_script("window.open('');")
        messages_tab = driver.window_handles[-1]
        driver.switch_to.window(messages_tab)
        
        # Navigate to messages
        driver.get(listing_url)
        
        # Look for messages button
        messages_selectors = [
            "a[data-testid='header-conversations-button']",
            "a[href='/inbox'][data-testid='header-conversations-button']",
        ]
        
        messages_found = False
        for selector in messages_selectors:
            try:
                messages_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                messages_button.click()
                print("✅ VM MESSAGES: Messages button clicked")
                messages_found = True
                break
            except TimeoutException:
                continue
        
        if messages_found:
            # Search for username (your existing logic)
            search_vm_username(driver, username, listing_url)
        
        # Clean up messages tab
        driver.close()
        if len(driver.window_handles) > 0:
            driver.switch_to.window(driver.window_handles[0])
        
        return True
        
    except Exception as messages_error:
        print(f"❌ VM MESSAGES ERROR: {messages_error}")
        return False

def search_vm_username(driver, username, listing_url):
    """
    Search for username in VM messages (your existing logic)
    """
    if not username:
        print("❌ VM USERNAME: No username provided")
        time.sleep(3)
        return
    
    print(f"🔍 VM USERNAME: Searching for {username}")
    time.sleep(2)  # Wait for messages to load
    
    try:
        username_element = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, f"//h2[contains(@class, 'web_ui') and contains(@class, 'Text') and contains(@class, 'title') and text()='{username}']"))
        )
        
        print(f"⚠️ VM USERNAME: Found {username} in messages - possible accidental purchase!")
        username_element.click()
        time.sleep(3)
        
        # If username found, this indicates accidental purchase
        print("❌ VM: ABORT - username found in messages")
        return False
        
    except TimeoutException:
        print(f"✅ VM USERNAME: {username} not found in messages - bookmark likely successful!")
        return True
    except Exception as search_error:
        print(f"❌ VM USERNAME SEARCH ERROR: {search_error}")
        return True  # Continue anyway

class AudioNumberDetector:
    def __init__(self, driver=None):
        self.driver = driver
        if not HAS_PYAUDIO:
            print("ERROR: pyaudiowpatch not available - audio detection will not work")
            return
            
        self.recognizer = sr.Recognizer()
        
        # Enhanced recognizer settings
        self.recognizer.energy_threshold = 200
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.5
        self.recognizer.phrase_threshold = 0.2
        self.recognizer.non_speaking_duration = 0.3
        
        self.is_running = False
        
        # Enhanced audio settings for better quality
        self.CHUNK = 2048
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        
        self.p = pyaudio.PyAudio()
        self.audio_queue = queue.Queue()
        
        # Audio processing parameters
        self.buffer_duration = 40
        self.overlap_duration = 2
        
        # Number collection
        self.collected_numbers = []
        self.target_count = 6
        self.numbers_lock = threading.Lock()
        self.complete_sequence = ""
        
        print(f"Buffer duration: {self.buffer_duration}s, Overlap: {self.overlap_duration}s")
        print(f"Will stop after collecting {self.target_count} numbers in sequence")

    def get_default_speakers(self):
        """Get the default speakers/output device for loopback capture"""
        try:
            wasapi_info = self.p.get_host_api_info_by_type(pyaudio.paWASAPI)
            default_speakers = self.p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
            
            if not default_speakers["isLoopbackDevice"]:
                for loopback in self.p.get_loopback_device_info_generator():
                    if default_speakers["name"] in loopback["name"]:
                        default_speakers = loopback
                        break
            
            print(f"Found system audio device: {default_speakers['name']}")
            return default_speakers
            
        except Exception as e:
            print(f"Error finding speakers: {e}")
            return None
    
    def extract_numbers_sequence(self, text):
        """Extract numbers from text in the correct sequence"""
        word_to_num = {
            'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
            'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
            'ten': '10', 'eleven': '11', 'twelve': '12', 'thirteen': '13',
            'fourteen': '14', 'fifteen': '15', 'sixteen': '16', 'seventeen': '17',
            'eighteen': '18', 'nineteen': '19', 'twenty': '20', 'thirty': '30',
            'forty': '40', 'fifty': '50', 'sixty': '60', 'seventy': '70',
            'eighty': '80', 'ninety': '90', 'hundred': '100'
        }
        
        words = text.lower().replace(',', '').replace('.', '').split()
        numbers = []
        
        for word in words:
            if word in word_to_num:
                numbers.append(word_to_num[word])
            elif word.isdigit():
                numbers.append(word)
            elif re.match(r'^\d+$', word):
                for digit in word:
                    numbers.append(digit)
        
        digit_matches = re.findall(r'\b\d\b', text)
        all_numbers = numbers + digit_matches
        
        # Remove the duplicate filtering - keep all numbers in sequence
        valid_numbers = []
        for num in all_numbers:
            if num.isdigit() and len(num) == 1:
                valid_numbers.append(num)
        
        return valid_numbers
    
    def find_complete_sequence(self, text):
        """Try to find a complete 6-digit sequence"""
        text_clean = re.sub(r'[^\w\s]', ' ', text.lower())
        numbers = self.extract_numbers_sequence(text)
        
        if len(numbers) == 6:
            return ''.join(numbers)
        
        sequence_patterns = [r'(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)']
        
        word_to_num = {
            'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
            'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'
        }
        
        for pattern in sequence_patterns:
            matches = re.findall(pattern, text_clean)
            for match in matches:
                sequence = []
                for word in match:
                    if word in word_to_num:
                        sequence.append(word_to_num[word])
                    elif word.isdigit() and len(word) == 1:
                        sequence.append(word)
                
                if len(sequence) == 6:
                    return ''.join(sequence)
        
        return None

    def input_captcha_solution(self, sequence):
        """Input the 6-digit sequence into the captcha form using trusted events"""
        if not self.driver or not sequence or len(sequence) != 6:
            print("Cannot input solution: missing driver or invalid sequence")
            return False
        
        print(f"Starting to input captcha solution: {sequence}")
        
        try:
            # Navigate to the correct iframe (same as before)
            self.driver.switch_to.default_content()
            
            iframe_selectors = [
                "iframe[src*='captcha']",
                "iframe[src*='datadome']",
                "iframe[id*='datadome']",
                "iframe[class*='datadome']",
                "iframe[title*='captcha']",
                "iframe[title*='DataDome']"
            ]
            
            iframe_found = False
            for selector in iframe_selectors:
                try:
                    iframe = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    print(f"Found main iframe with selector: {selector}")
                    self.driver.switch_to.frame(iframe)
                    iframe_found = True
                    break
                except TimeoutException:
                    continue
            
            if not iframe_found:
                print("Could not find captcha iframe for input")
                return False
            
            # Find input fields
            input_selectors = [
                "input.audio-captcha-inputs",
                "input[class*='audio-captcha-inputs']",
                "input[data-index='1']",
                "input[maxlength='1'][inputmode='numeric']",
                "input[data-form-type='other'][maxlength='1']"
            ]
            
            input_found = False
            first_input = None
            
            for selector in input_selectors:
                try:
                    first_input = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    print(f"Found first input field with selector: {selector}")
                    input_found = True
                    break
                except TimeoutException:
                    continue
            
            # Check nested iframes if not found
            if not input_found:
                print("Input fields not found in current iframe, checking nested iframes...")
                
                try:
                    nested_iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
                    print(f"Found {len(nested_iframes)} nested iframes")
                    
                    for i, nested_iframe in enumerate(nested_iframes):
                        try:
                            print(f"Trying nested iframe {i}...")
                            self.driver.switch_to.frame(nested_iframe)
                            
                            for selector in input_selectors:
                                try:
                                    first_input = WebDriverWait(self.driver, 3).until(
                                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                                    )
                                    print(f"Found first input field in nested iframe {i} with selector: {selector}")
                                    input_found = True
                                    break
                                except:
                                    continue
                            
                            if input_found:
                                break
                            
                            self.driver.switch_to.parent_frame()
                            
                        except Exception as e:
                            print(f"Error with nested iframe {i}: {e}")
                            try:
                                self.driver.switch_to.parent_frame()
                            except:
                                self.driver.switch_to.default_content()
                                for sel in iframe_selectors:
                                    try:
                                        iframe = self.driver.find_element(By.CSS_SELECTOR, sel)
                                        self.driver.switch_to.frame(iframe)
                                        break
                                    except:
                                        continue
                            continue
                
                except Exception as e:
                    print(f"Error searching nested iframes for inputs: {e}")
            
            if not input_found or not first_input:
                print("Could not find input fields")
                self.driver.switch_to.default_content()
                return False
            
            print("Starting to input digits using native Selenium methods...")
            
            # Click on the first input field
            time.sleep(random.uniform(0.5, 1.0))
            
            # Scroll into view
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", first_input)
            time.sleep(random.uniform(0.3, 0.6))

            action = ActionChains(self.driver)


            # Click with ActionChains (this generates trusted events)


            offset_x = random.randint(-2, 2)
            offset_y = random.randint(-2, 2)

            action.move_to_element_with_offset(first_input, offset_x, offset_y)
            time.sleep(random.uniform(0.2, 0.4))
            action.move_to_element(first_input)
            time.sleep(random.uniform(0.1, 0.3))
            action.click().perform()
            
            print("Clicked on first input field")


            # Input each digit using send_keys (generates TRUSTED events)
            # Input each digit using PyAutoGUI
            for i, digit in enumerate(sequence):
                print(f"Inputting digit {i+1}: {digit}")
                
                if digit == '1':
                    time.sleep(2.3)
                
                # Random delay before typing
                time.sleep(random.uniform(0.2, 0.6))
                
                # Use PyAutoGUI instead of Windows API
                if not send_keypress_with_pyautogui(digit):
                    print(f"Failed to send PyAutoGUI keystroke for digit: {digit}")
                
                time.sleep(random.uniform(0.3, 0.4))
                
                print(f"Typed digit: {digit}")
                
                # If not the last digit, move to next field with arrow key
                if i < len(sequence) - 1:
                    time.sleep(random.uniform(0.2, 0.6))
                    
                    # Use PyAutoGUI for arrow key
                    if not send_keypress_with_pyautogui('right'):
                        print(f"Failed to send PyAutoGUI RIGHT key")
                    
                    print(f"Moved to next input field")
                    time.sleep(random.uniform(0.05, 0.25))

            print("All digits entered successfully!")
                
                # Wait a moment for any validation
            time.sleep(random.uniform(1.0, 2.0))
                
                # Find and click the Verify button (same as before)
            print("Looking for Verify button...")
            
            verify_button_selectors = [
                "button.audio-captcha-submit-button",
                "button[class*='audio-captcha-submit-button']",
                "button.push-button.no-margin",
                "button[role='button'][class*='submit']",
                "button:contains('Verify')",
                "//button[contains(@class, 'audio-captcha-submit-button')]",
                "//button[text()='Verify']",
                "//button[contains(text(), 'Verify')]"
            ]
            
            verify_button = None
            for selector in verify_button_selectors:
                try:
                    if selector.startswith("//"):
                        verify_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        verify_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    print(f"Found Verify button with selector: {selector}")
                    break
                except TimeoutException:
                    continue
            
            if not verify_button:
                print("Verify button not found, trying to find any submit-like button...")
                try:
                    all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
                    for button in all_buttons:
                        button_text = button.text.lower().strip()
                        button_class = button.get_attribute("class") or ""
                        
                        if ("verify" in button_text or 
                            "submit" in button_text or 
                            "confirm" in button_text or
                            "submit" in button_class.lower() or
                            "verify" in button_class.lower()):
                            verify_button = button
                            print(f"Found potential verify button: text='{button_text}', class='{button_class}'")
                            break
                except Exception as e:
                    print(f"Error searching for buttons: {e}")
            
            if verify_button:
                # Wait a moment before clicking verify
                time.sleep(random.uniform(0.5, 1.0))
