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
BOOKMARK_TEST_URL = "https://www.vinted.co.uk/items/7037950664-racer-jacket?referrer=catalog"
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
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # VM-specific optimizations
    chrome_options.add_argument('--force-device-scale-factor=1')
    chrome_options.add_argument('--high-dpi-support=1')
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_argument('--remote-allow-origins=*')
    chrome_options.add_argument('--disable-features=VizDisplayCompositor')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--allow-running-insecure-content')

    
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
    """Main VM driver function"""
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
            print("Script completed successfully without needing captcha solving.")
        elif result == True:
            print("Audio captcha button clicked successfully!")
            print("="*60)
            print("STARTING AUDIO DETECTION...")
            print("="*60)
            
            # Initialize and start audio detection with driver reference
            if HAS_PYAUDIO:
                detector = AudioNumberDetector(driver=driver)
                detector.start_listening()
            else:
                print("ERROR: Cannot start audio detection - pyaudiowpatch not available")
        else:
            print("Failed to click audio captcha button")
        
        print("Script completed!")
        
        # Keep browser open for a bit to see the result
        time.sleep(10)
        
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
        # Uncomment the next line if you want to close the browser automatically
        # driver.quit()
        pass

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
                
                # Scroll into view
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", verify_button)
                time.sleep(random.uniform(0.3, 0.6))
                
                # Human-like click with ActionChains (generates trusted events)
                action = ActionChains(self.driver)
                offset_x = random.randint(-3, 3)
                offset_y = random.randint(-3, 3)
                action.move_to_element_with_offset(verify_button, offset_x, offset_y)
                time.sleep(random.uniform(0.2, 0.4))
                action.move_to_element(verify_button)
                time.sleep(random.uniform(0.2, 0.5))
                action.click().perform()
                
                print("Successfully clicked Verify button!")
                
                # Wait to see the result
                time.sleep(random.uniform(2.0, 4.0))
                
                self.driver.switch_to.default_content()
                return True
                
            else:
                print("Could not find Verify button")
                self.driver.switch_to.default_content()
                return False
                
        except Exception as e:
            print(f"Error inputting captcha solution: {e}")
            import traceback
            traceback.print_exc()
            try:
                self.driver.switch_to.default_content()
            except:
                pass
            return False

    def preprocess_audio(self, audio_data, sample_rate):
        """Enhanced audio preprocessing for better recognition"""
        audio_np = np.frombuffer(audio_data, dtype=np.int16)
        
        if self.CHANNELS == 2:
            audio_np = audio_np.reshape(-1, 2).mean(axis=1).astype(np.int16)
        
        if np.max(np.abs(audio_np)) > 0:
            audio_np = audio_np.astype(np.float32)
            audio_np = audio_np / np.max(np.abs(audio_np)) * 0.8
        
        nyquist = sample_rate / 2
        high_cutoff = 100
        high = high_cutoff / nyquist
        b, a = signal.butter(2, high, btype='high')
        audio_np = signal.filtfilt(b, a, audio_np)
        
        low_cutoff = 8000
        low = low_cutoff / nyquist
        b, a = signal.butter(2, low, btype='low')
        audio_np = signal.filtfilt(b, a, audio_np)
        
        if HAS_NOISEREDUCE:
            try:
                noise_sample_length = min(sample_rate, len(audio_np) // 4)
                if len(audio_np) > noise_sample_length * 2:
                    audio_np = nr.reduce_noise(
                        y=audio_np, 
                        sr=sample_rate,
                        stationary=False,
                        prop_decrease=0.8
                    )
            except Exception as e:
                print(f"Noise reduction failed: {e}")
        
        pre_emphasis = 0.97
        audio_np = np.append(audio_np[0], audio_np[1:] - pre_emphasis * audio_np[:-1])
        
        if np.max(np.abs(audio_np)) > 0:
            audio_np = audio_np / np.max(np.abs(audio_np)) * 0.9
        
        audio_np = (audio_np * 32767).astype(np.int16)
        return audio_np.tobytes()
    
    def process_audio_data(self, audio_data):
        """Process audio data and extract numbers"""
        try:
            audio_np = np.frombuffer(audio_data, dtype=np.int16)
            volume = np.sqrt(np.mean(audio_np**2))
            max_volume = np.max(np.abs(audio_np))
            
            print(f"Audio volume: {volume:.1f}, max: {max_volume}")
            
            if volume < 8:
                print("Audio too quiet, skipping...")
                return
            
            processed_audio = self.preprocess_audio(audio_data, self.RATE)
            
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                wf = wave.open(tmp_file.name, 'wb')
                wf.setnchannels(1)
                wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(processed_audio)
                wf.close()
                
                try:
                    with sr.AudioFile(tmp_file.name) as source:
                        self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                        audio = self.recognizer.record(source)
                        
                        print("Attempting speech recognition...")
                        
                        text = None
                        try:
                            # Try with show_all=True to get confidence scores and alternatives
                            result = self.recognizer.recognize_google(audio, language='en-US', show_all=True)
                            if isinstance(result, dict) and 'alternative' in result:
                                # Get the most confident result
                                text = result['alternative'][0]['transcript']
                                print(f"Google Recognition (detailed): '{text}'")
                                
                                # Also check other alternatives for better matches
                                for alt in result['alternative'][:3]:  # Check top 3 alternatives
                                    alt_text = alt['transcript']
                                    alt_numbers = self.extract_numbers_sequence(alt_text)
                                    if len(alt_numbers) >= 6:
                                        text = alt_text
                                        print(f"Using alternative with more numbers: '{text}'")
                                        break
                            else:
                                text = self.recognizer.recognize_google(audio, language='en-US', show_all=False)
                                print(f"Google Recognition: '{text}'")
                                
                        except (sr.UnknownValueError, sr.RequestError):
                            print("Google recognition failed, trying Sphinx...")
                            try:
                                text = self.recognizer.recognize_sphinx(audio)
                                print(f"Sphinx Recognition: '{text}'")
                            except:
                                print("Sphinx recognition also failed")
                        
                        if text:
                            timestamp = time.strftime("%H:%M:%S")
                            
                            # Try to find complete sequence
                            complete_seq = self.find_complete_sequence(text)
                            if complete_seq and len(complete_seq) == 6:
                                with self.numbers_lock:
                                    self.complete_sequence = complete_seq
                                    print(f"\n[{timestamp}] *** COMPLETE SEQUENCE FOUND: {complete_seq} ***")
                                    print(f"[{timestamp}] From text: '{text}'")
                                    print("="*60)
                                    print(f"SUCCESS! Complete 6-digit sequence: {complete_seq}")
                                    print("="*60)
                                    
                                    # Input the sequence into the captcha form
                                    if self.input_captcha_solution(complete_seq):
                                        print("Successfully inputted captcha solution!")
                                    else:
                                        print("Failed to input captcha solution")
                                    
                                    self.stop()
                                    return
                            
                            # Otherwise collect individual numbers
                            numbers = self.extract_numbers_sequence(text)
                            if numbers:
                                with self.numbers_lock:
                                    new_numbers = []
                                    for num in numbers:
                                        if len(self.collected_numbers) < self.target_count:
                                            self.collected_numbers.append(num)
                                            new_numbers.append(num)
                                    
                                    if new_numbers:
                                        print(f"[{timestamp}] NEW NUMBERS: {' '.join(new_numbers)}")
                                        print(f"[{timestamp}] Full text: '{text}'")
                                        print(f"[{timestamp}] Sequence so far ({len(self.collected_numbers)}/{self.target_count}): {' '.join(self.collected_numbers)}")
                                    
                                    if len(self.collected_numbers) >= self.target_count:
                                        final_sequence = ''.join(self.collected_numbers[:self.target_count])
                                        print("\n" + "="*60)
                                        print(f"SUCCESS! Collected {self.target_count} numbers:")
                                        print(f"FINAL SEQUENCE: {final_sequence}")
                                        print("="*60)
                                        
                                        # Input the sequence into the captcha form
                                        if self.input_captcha_solution(final_sequence):
                                            print("Successfully inputted captcha solution!")
                                        else:
                                            print("Failed to input captcha solution")
                                        
                                        self.stop()
                                        return
                            else:
                                print(f"[{timestamp}] No numbers found in: '{text}'")
                        
                finally:
                    try:
                        os.unlink(tmp_file.name)
                    except:
                        pass
                        
        except Exception as e:
            print(f"Audio processing error: {e}")
    
    def audio_processor_thread(self):
        """Background thread to process audio chunks"""
        while self.is_running:
            try:
                if not self.audio_queue.empty():
                    audio_data = self.audio_queue.get(timeout=1)
                    processor = threading.Thread(target=self.process_audio_data, args=(audio_data,), daemon=True)
                    processor.start()
                else:
                    time.sleep(0.1)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Processor thread error: {e}")
    
    def start_listening(self):
        """Start capturing system audio output"""
        default_speakers = self.get_default_speakers()
        
        if not default_speakers:
            print("Could not find system speakers!")
            return
        
        try:
            stream = self.p.open(
                format=self.FORMAT,
                channels=int(default_speakers["maxInputChannels"]),
                rate=int(default_speakers["defaultSampleRate"]),
                input=True,
                input_device_index=default_speakers["index"],
                frames_per_buffer=self.CHUNK
            )
            
            print(f"Listening to PC system audio... Press Ctrl+C to stop.")
            print("Looking for 6-digit number sequence...")
            print("-" * 60)
            
            self.is_running = True
            
            # Start processor threads
            for i in range(2):
                processor = threading.Thread(target=self.audio_processor_thread, daemon=True)
                processor.start()
                print(f"Started audio processor thread {i+1}")
            
            audio_buffer = b""
            buffer_size = self.RATE * self.buffer_duration * 2
            overlap_size = self.RATE * self.overlap_duration * 2
            
            while self.is_running:
                try:
                    data = stream.read(self.CHUNK, exception_on_overflow=False)
                    audio_buffer += data
                    
                    with self.numbers_lock:
                        if len(self.collected_numbers) >= self.target_count or self.complete_sequence:
                            break
                    
                    if len(audio_buffer) >= buffer_size:
                        print(f"Processing {self.buffer_duration}s audio chunk...")
                        
                        if self.audio_queue.qsize() < 3:
                            self.audio_queue.put(audio_buffer[:buffer_size])
                        else:
                            print("Audio queue full, skipping chunk...")
                            
                        audio_buffer = audio_buffer[-overlap_size:]
                        
                except Exception as e:
                    print(f"Stream error: {e}")
                    break
            
            stream.stop_stream()
            stream.close()
            
        except Exception as e:
            print(f"Error starting capture: {e}")

    def stop(self):
        """Stop the transcriber"""
        self.is_running = False
        self.p.terminate()

def debug_function_call(func_name, line_number=None):
    """Debug function to track where errors occur"""
    if print_debug:
        print(f"DEBUG: Entering function {func_name}" + (f" at line {line_number}" if line_number else ""))

# Vinted profit suitability ranges (same structure as Facebook but independent variables)
def check_vinted_profit_suitability(listing_price, profit_percentage):
    if 10 <= listing_price < 16:
        return 100 <= profit_percentage <= 600
    elif 16 <= listing_price < 25:
        return 50 <= profit_percentage <= 400
    elif 25 <= listing_price < 50:
        return 37.5 <= profit_percentage <= 550
    elif 50 <= listing_price < 100:
        return 35 <= profit_percentage <= 500
    elif listing_price >= 100:
        return 30 <= profit_percentage <= 450
    else:
        return False

@app.route("/", methods=["GET", "POST"])
def index():
    # Remove the 'self' parameter and access global variables instead
    global recent_listings, current_listing_title, current_listing_price, current_listing_description
    global current_listing_join_date, current_detected_items, current_profit, current_listing_images
    global current_listing_url
    
    if "authenticated" in session:
        return render_main_page()  # Call the standalone function
    
    if request.method == "POST":
        entered_pin = request.form.get("pin")
        if int(entered_pin) == PIN_CODE:
            session["authenticated"] = True
            return redirect(url_for("index"))
        else:
            return '''
            <html>
            <head>
                <title>Enter PIN</title>
            </head>
            <body>
                <h2>Enter 5-digit PIN to access</h2>
                <p style="color: red;">Incorrect PIN</p>
                <form method="POST">
                    <input type="password" name="pin" maxlength="5" required>
                    <button type="submit">Submit</button>
                </form>
            </body>
            </html>
            '''
    
    return '''
    <html>
    <head>
        <title>Enter PIN</title>
    </head>
    <body>
        <h2>Enter 5-digit PIN to access</h2>
        <form method="POST">
            <input type="password" name="pin" maxlength="5" required>
            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    '''

@app.route("/logout")
def logout():
    session.pop("authenticated", None)
    return redirect(url_for("index"))

@app.route('/static/icon.png')
def serve_icon():
    #pc
    #return send_file(r"C:\Users\ZacKnowsHow\Downloads\icon_2 (1).png", mimetype='image/png')
    #laptop
    return send_file(r"C:\Users\ZacKnowsHow\Downloads\icon_2.png", mimetype='image/png')

@app.route('/change_listing', methods=['POST'])
def change_listing():
    direction = request.form.get('direction')
    total_listings = len(recent_listings['listings'])
    
    if direction == 'next':
        recent_listings['current_index'] = (recent_listings['current_index'] + 1) % total_listings
    elif direction == 'previous':
        recent_listings['current_index'] = (recent_listings['current_index'] - 1) % total_listings
    
    current_listing = recent_listings['listings'][recent_listings['current_index']]
    
    # Convert images to base64
    processed_images_base64 = []
    for img in current_listing['processed_images']:
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        processed_images_base64.append(img_str)
    
    return jsonify({
        'title': current_listing['title'],
        'description': current_listing['description'],
        'join_date': current_listing['join_date'],
        'price': current_listing['price'],
        'expected_revenue': current_listing['expected_revenue'],
        'profit': current_listing['profit'],
        'detected_items': current_listing['detected_items'],
        'processed_images': processed_images_base64,
        'bounding_boxes': current_listing['bounding_boxes'],
        'url': current_listing['url'],
        'suitability': current_listing['suitability'],
        'current_index': recent_listings['current_index'] + 1,
        'total_listings': total_listings
    })

@app.route('/vinted-button-clicked', methods=['POST'])
def vinted_button_clicked():
    """Handle Vinted scraper button clicks with enhanced functionality"""
    if print_debug:
        print("DEBUG: Received a Vinted button-click POST request")
    
    # Get the listing URL and action from the form data
    url = request.form.get('url')
    action = request.form.get('action')
    
    if not url:
        print("ERROR: No URL provided in Vinted button click")
        return 'NO URL PROVIDED', 400
    
    try:
        # Print the appropriate message based on the action
        if action == 'buy_yes':
            print(f'✅ VINTED YES BUTTON: User wishes to buy listing: {url}')
            
            # Access the Vinted scraper instance and trigger enhanced button functionality
            if 'vinted_scraper_instance' in globals():
                vinted_scraper_instance.vinted_button_clicked_enhanced(url)
            else:
                print("WARNING: No Vinted scraper instance found")
                print(f'Vinted button clicked on listing: {url}')
                with open('vinted_clicked_listings.txt', 'a') as f:
                    f.write(f"{action}: {url}\n")
                    
        elif action == 'buy_no':
            print(f'❌ VINTED NO BUTTON: User does not wish to buy listing: {url}')
            # DO NOT CALL vinted_button_clicked_enhanced - just print message
            # No navigation should happen for "No" button
        else:
            print(f'🔘 VINTED BUTTON: Unknown action "{action}" for listing: {url}')
        
        return 'VINTED BUTTON CLICK PROCESSED', 200
        
    except Exception as e:
        print(f"ERROR processing Vinted button click: {e}")
        return 'ERROR PROCESSING REQUEST', 500


# Replace the render_main_page function starting at line ~465 with this modified version

def render_main_page():
    try:
        # Access global variables
        global current_listing_title, current_listing_price, current_listing_description
        global current_listing_join_date, current_detected_items, current_profit
        global current_listing_images, current_listing_url, recent_listings
        if print_debug:
            print("DEBUG: render_main_page called")
            print(f"DEBUG: recent_listings has {len(recent_listings.get('listings', []))} listings")
            print(f"DEBUG: current_listing_title = {current_listing_title}")
            print(f"DEBUG: current_listing_price = {current_listing_price}")

        # Ensure default values if variables are None or empty
        title = str(current_listing_title or 'No Title Available')
        price = str(current_listing_price or 'Price: £0.00')
        description = str(current_listing_description or 'No Description Available')
        detected_items = str(current_detected_items or 'No items detected')
        profit = str(current_profit or 'Profit: £0.00')
        join_date = str(current_listing_join_date or 'No Join Date Available')
        listing_url = str(current_listing_url or 'No URL Available')

        # Create all_listings_json - this is crucial for the JavaScript
        all_listings_json = "[]" # Default empty array
        if recent_listings and 'listings' in recent_listings and recent_listings['listings']:
            try:
                listings_data = []
                for listing in recent_listings['listings']:
                    # Convert images to base64
                    processed_images_base64 = []
                    if 'processed_images' in listing and listing['processed_images']:
                        for img in listing['processed_images']:
                            try:
                                processed_images_base64.append(base64_encode_image(img))
                            except Exception as img_error:
                                print(f"Error encoding image: {img_error}")

                    listings_data.append({
                        'title': str(listing.get('title', 'No Title')),
                        'description': str(listing.get('description', 'No Description')),
                        'join_date': str(listing.get('join_date', 'No Date')),
                        'price': str(listing.get('price', '0')),
                        'profit': float(listing.get('profit', 0)),
                        'detected_items': str(listing.get('detected_items', 'No Items')),
                        'processed_images': processed_images_base64,
                        'url': str(listing.get('url', 'No URL')),
                        'suitability': str(listing.get('suitability', 'Unknown'))
                    })
                all_listings_json = json.dumps(listings_data)
                if print_debug:
                    print(f"DEBUG: Created JSON for {len(listings_data)} listings")
            except Exception as json_error:
                print(f"ERROR creating listings JSON: {json_error}")
                all_listings_json = "[]"

        # Convert current images to base64 for web display
        image_html = ""
        if current_listing_images:
            image_html = "<div class='image-container'>"
            try:
                for img in current_listing_images:
                    buffered = io.BytesIO()
                    img.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    image_html += f'''
                    <div class="image-wrapper">
                        <img src="data:image/png;base64,{img_str}" alt="Listing Image">
                    </div>
                    '''
                image_html += "</div>"
            except Exception as img_error:
                print(f"Error processing current images: {img_error}")
                image_html = "<p>Error loading images</p>"
        else:
            image_html = "<p>No images available</p>"

        # Return the complete HTML with NEW top bar layout and stopwatch functionality
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
            <link rel="apple-touch-icon" href="/static/icon.png">
            <link rel="icon" type="image/png" href="/static/icon.png">
            <meta name="apple-mobile-web-app-capable" content="yes">
            <meta name="apple-mobile-web-app-status-bar-style" content="black">
            <meta name="apple-mobile-web-app-title" content="Marketplace Scanner">
            <title>Marketplace Scanner</title>
            <style>
                * {{
                    box-sizing: border-box;
                    margin: 0;
                    padding: 0;
                }}
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
                    background-color: #f0f0f0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    margin: 0;
                    padding: 0;
                    line-height: 1.6;
                    touch-action: manipulation;
                    overscroll-behavior-y: none;
                }}
                .container {{
                    background-color: white;
                    padding: 25px;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    text-align: center;
                    width: 100%;
                    max-width: 375px;
                    margin: 0 auto;
                    position: relative;
                    height: calc(100vh - 10px);
                    overflow-y: auto;
                }}
                
                /* NEW: Top bar styles */
                .top-bar {{
                    display: flex;
                    gap: 5px;
                    margin-bottom: 15px;
                    justify-content: space-between;
                }}
                
                .top-bar-item {{
                    flex: 1;
                    padding: 8px 4px;
                    border-radius: 8px;
                    font-size: 12px;
                    font-weight: bold;
                    color: white;
                    text-align: center;
                    min-height: 40px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }}
                
                .refresh-button {{
                    background-color: #4CAF50;
                    cursor: pointer;
                    transition: all 0.2s ease;
                    border: none;
                    touch-action: manipulation;
                    -webkit-tap-highlight-color: transparent;
                }}
                
                .refresh-button:hover {{
                    background-color: #45a049;
                    transform: translateY(-1px);
                }}
                
                .refresh-button:active {{
                    transform: translateY(0);
                }}
                
                .listing-counter {{
                    background-color: #2196F3;
                }}
                
                .stopwatch-display {{
                    background-color: #FF9800;
                    font-family: monospace;
                }}
                
                .custom-button {{
                    width: 100%;
                    padding: 12px;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    font-size: 16px;
                    font-weight: bold;
                    touch-action: manipulation;
                    -webkit-tap-highlight-color: transparent;
                    cursor: pointer;
                    transition: all 0.2s ease;
                }}
                .custom-button:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                }}
                .custom-button:active {{
                    transform: translateY(0);
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .section-box, .financial-row, .details-row {{
                    border: 1px solid black;
                    border-radius: 5px;
                    margin-bottom: -1px;
                }}
                .section-box {{
                    padding: 10px;
                }}
                .financial-row, .details-row {{
                    display: flex;
                    justify-content: space-between;
                }}
                .financial-item, .details-item {{
                    flex: 1;
                    padding: 10px;
                    border-right: 1px solid black;
                    font-weight: bold;
                    font-size: 19px;
                }}
                .financial-item:last-child, .details-item:last-child {{
                    border-right: none;
                }}
                .content-title {{
                    color: rgb(173, 13, 144);
                    font-weight: bold;
                    font-size: 1.6em;
                }}
                .content-price {{
                    color: rgb(19, 133, 194);
                    font-weight: bold;
                }}
                .content-description {{
                    color: #006400;
                    font-weight: bold;
                }}
                .content-profit {{
                    color: rgb(186, 14, 14);
                    font-weight: bold;
                }}
                .content-join-date {{
                    color: #4169E1;
                    font-weight: bold;
                }}
                .content-detected-items {{
                    color: #8B008B;
                    font-weight: bold;
                }}
                .image-container {{
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: center;
                    align-items: center;
                    gap: 10px;
                    max-height: 335px;
                    overflow-y: auto;
                    padding: 10px;
                    background-color: #f9f9f9;
                    border: 1px solid black;
                    border-radius: 10px;
                    margin-bottom: 10px;
                }}
                .image-wrapper {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    max-width: 100%;
                    max-height: 200px;
                    overflow: hidden;
                }}
                .image-wrapper img {{
                    max-width: 100%;
                    max-height: 100%;
                    object-fit: contain;
                }}
                .listing-url {{
                    font-size: 10px;
                    word-break: break-all;
                    border: 1px solid black;
                    border-radius: 5px;
                    padding: 5px;
                    margin-top: 10px;
                    font-weight: bold;
                }}
                .single-button-container {{
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                    margin: 15px 0;
                }}
                .open-listing-button {{
                    background-color: #28a745;
                    font-size: 18px;
                    padding: 15px;
                }}
                
                /* Buy decision buttons */
                .buy-decision-container {{
                    display: flex;
                    gap: 10px;
                    margin: 15px 0;
                }}
                .buy-yes-button {{
                    background-color: #28a745;
                    flex: 1;
                    padding: 15px;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 8px;
                    color: white;
                    border: none;
                    cursor: pointer;
                    transition: all 0.2s ease;
                    touch-action: manipulation;
                    -webkit-tap-highlight-color: transparent;
                }}
                .buy-yes-button:hover {{
                    background-color: #218838;
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                }}
                .buy-yes-button:active {{
                    transform: translateY(0);
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .buy-no-button {{
                    background-color: #dc3545;
                    flex: 1;
                    padding: 15px;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 8px;
                    color: white;
                    border: none;
                    cursor: pointer;
                    transition: all 0.2s ease;
                    touch-action: manipulation;
                    -webkit-tap-highlight-color: transparent;
                }}
                .buy-no-button:hover {{
                    background-color: #c82333;
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                }}
                .buy-no-button:active {{
                    transform: translateY(0);
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                
                /* Confirmation button styles */
                .confirmation-container {{
                    display: none;
                    flex-direction: column;
                    gap: 10px;
                    margin: 15px 0;
                }}
                
                .confirmation-text {{
                    color: #333;
                    font-weight: bold;
                    font-size: 14px;
                    margin-bottom: 10px;
                    text-align: center;
                }}
                
                .confirmation-buttons {{
                    display: flex;
                    gap: 10px;
                }}
                
                .confirm-yes-button {{
                    background-color: #28a745;
                    flex: 1;
                    padding: 15px;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 8px;
                    color: white;
                    border: none;
                    cursor: pointer;
                    transition: all 0.2s ease;
                    touch-action: manipulation;
                    -webkit-tap-highlight-color: transparent;
                }}
                
                .confirm-no-button {{
                    background-color: #6c757d;
                    flex: 1;
                    padding: 15px;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 8px;
                    color: white;
                    border: none;
                    cursor: pointer;
                    transition: all 0.2s ease;
                    touch-action: manipulation;
                    -webkit-tap-highlight-color: transparent;
                }}
                
                .confirm-yes-button:hover {{
                    background-color: #218838;
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                }}
                
                .confirm-no-button:hover {{
                    background-color: #5a6268;
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                }}
                
                .confirm-yes-button:active, .confirm-no-button:active {{
                    transform: translateY(0);
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
            </style>
            <script>
                const allListings = {all_listings_json};
                let currentListingIndex = 0;
                let stopwatchIntervals = {{}};
                console.log('All listings loaded:', allListings);
                console.log('Number of listings:', allListings.length);

                function refreshPage() {{
                    location.reload();
                }}

                function updateStopwatch() {{
                    if (allListings.length === 0) return;
                    
                    const currentListing = allListings[currentListingIndex];
                    const currentUrl = currentListing.url;
                    const stopwatchElement = document.querySelector('.stopwatch-display');
                    
                    if (stopwatchElement) {{
                        // Check if this URL has an active stopwatch
                        // This would need to be populated from the Python backend
                        // For now, show placeholder text
                        stopwatchElement.textContent = 'No stopwatch - listing unbookmarked';
                    }}
                }}

                function updateListingDisplay(index) {{
                    if (allListings.length === 0) {{
                        console.log('No listings available');
                        return;
                    }}
                    if (index < 0) index = allListings.length - 1;
                    if (index >= allListings.length) index = 0;
                    currentListingIndex = index;
                    const listing = allListings[index];
                    console.log('Updating to listing:', listing);

                    // Update content
                    const titleEl = document.querySelector('.content-title');
                    const priceEl = document.querySelector('.content-price');
                    const profitEl = document.querySelector('.content-profit');
                    const joinDateEl = document.querySelector('.content-join-date');
                    const detectedItemsEl = document.querySelector('.content-detected-items');
                    const descriptionEl = document.querySelector('.content-description');
                    const urlEl = document.querySelector('.content-url');
                    const counterEl = document.querySelector('.listing-counter');

                    if (titleEl) titleEl.textContent = listing.title;
                    if (priceEl) priceEl.textContent = 'Price: £' + listing.price;
                    if (profitEl) profitEl.textContent = `Profit: £${{listing.profit.toFixed(2)}}`;
                    if (joinDateEl) joinDateEl.textContent = listing.join_date;
                    if (detectedItemsEl) detectedItemsEl.textContent = listing.detected_items;
                    if (descriptionEl) descriptionEl.textContent = listing.description;
                    if (urlEl) urlEl.textContent = listing.url;
                    if (counterEl) counterEl.textContent = `${{currentListingIndex + 1}} of ${{allListings.length}}`;

                    // Update images
                    const imageContainer = document.querySelector('.image-container');
                    if (imageContainer) {{
                        imageContainer.innerHTML = '';
                        listing.processed_images.forEach(imgBase64 => {{
                            const imageWrapper = document.createElement('div');
                            imageWrapper.className = 'image-wrapper';
                            const img = document.createElement('img');
                            img.src = `data:image/png;base64=${{imgBase64}}`;
                            img.alt = 'Listing Image';
                            imageWrapper.appendChild(img);
                            imageContainer.appendChild(imageWrapper);
                        }});
                    }}
                    
                    // Update stopwatch
                    updateStopwatch();
                    
                    // Reset confirmation dialog state
                    hideConfirmation();
                }}

                function changeListingIndex(direction) {{
                    if (direction === 'next') {{
                        updateListingDisplay(currentListingIndex + 1);
                    }} else if (direction === 'previous') {{
                        updateListingDisplay(currentListingIndex - 1);
                    }}
                }}

                // Single button function to open listing directly
                function openListing() {{
                    var urlElement = document.querySelector('.content-url');
                    var url = urlElement ? urlElement.textContent.trim() : '';
                    
                    if (url && url !== 'No URL Available') {{
                        console.log('Opening listing:', url);
                        window.open(url, '_blank');
                    }} else {{
                        alert('No valid URL available for this listing');
                    }}
                }}
                
                // Confirmation dialog functions
                function showConfirmation(message, confirmCallback, cancelCallback) {{
                    const buyDecisionContainer = document.querySelector('.buy-decision-container');
                    const confirmationContainer = document.querySelector('.confirmation-container');
                    
                    if (buyDecisionContainer) buyDecisionContainer.style.display = 'none';
                    if (confirmationContainer) {{
                        confirmationContainer.style.display = 'flex';
                        
                        const confirmationText = confirmationContainer.querySelector('.confirmation-text');
                        if (confirmationText) confirmationText.textContent = message;
                        
                        const confirmYesBtn = confirmationContainer.querySelector('.confirm-yes-button');
                        const confirmNoBtn = confirmationContainer.querySelector('.confirm-no-button');
                        
                        if (confirmYesBtn) {{
                            confirmYesBtn.onclick = function() {{
                                confirmCallback();
                                hideConfirmation();
                            }};
                        }}
                        
                        if (confirmNoBtn) {{
                            confirmNoBtn.onclick = function() {{
                                cancelCallback();
                                hideConfirmation();
                            }};
                        }}
                    }}
                }}
                
                function hideConfirmation() {{
                    const buyDecisionContainer = document.querySelector('.buy-decision-container');
                    const confirmationContainer = document.querySelector('.confirmation-container');
                    
                    if (buyDecisionContainer) buyDecisionContainer.style.display = 'flex';
                    if (confirmationContainer) confirmationContainer.style.display = 'none';
                }}

                // Buy decision functions with confirmation
                function buyYes() {{
                    showConfirmation(
                        'Are you sure you want to buy this listing?',
                        function() {{
                            var urlElement = document.querySelector('.content-url');
                            var url = urlElement ? urlElement.textContent.trim() : '';
                            
                            if (url && url !== 'No URL Available') {{
                                console.log('User confirmed: wants to buy listing: ' + url);
                                
                                fetch('/vinted-button-clicked', {{
                                    method: 'POST',
                                    headers: {{
                                        'Content-Type': 'application/x-www-form-urlencoded',
                                    }},
                                    body: `url=${{encodeURIComponent(url)}}&action=buy_yes`
                                }})
                                .then(response => {{
                                    if (response.ok) {{
                                        console.log('Vinted YES button confirmed and sent successfully');
                                    }} else {{
                                        console.error('Failed to process Vinted YES button');
                                    }}
                                }})
                                .catch(error => {{
                                    console.error('Error with Vinted YES button:', error);
                                }});
                            }} else {{
                                console.log('User confirmed: wants to buy listing but no URL available');
                            }}
                        }},
                        function() {{
                            console.log('User cancelled buying decision');
                        }}
                    );
                }}

                function buyNo() {{
                    showConfirmation(
                        'Are you sure you don\\'t want to buy this listing?',
                        function() {{
                            var urlElement = document.querySelector('.content-url');
                            var url = urlElement ? urlElement.textContent.trim() : '';
                            
                            if (url && url !== 'No URL Available') {{
                                console.log('User confirmed: does not want to buy listing: ' + url);
                                
                                fetch('/vinted-button-clicked', {{
                                    method: 'POST',
                                    headers: {{
                                        'Content-Type': 'application/x-www-form-urlencoded',
                                    }},
                                    body: `url=${{encodeURIComponent(url)}}&action=buy_no`
                                }})
                                .then(response => {{
                                    if (response.ok) {{
                                        console.log('Vinted NO button confirmed and sent successfully');
                                    }} else {{
                                        console.error('Failed to process Vinted NO button');
                                    }}
                                }})
                                .catch(error => {{
                                    console.error('Error with Vinted NO button:', error);
                                }});
                            }} else {{
                                console.log('User confirmed: does not want to buy listing but no URL available');
                            }}
                        }},
                        function() {{
                            console.log('User cancelled buying decision');
                        }}
                    );
                }}

                // Initialize display on page load
                window.onload = () => {{
                    console.log('Page loaded, initializing display');
                    if (allListings.length > 0) {{
                        updateListingDisplay(0);
                    }} else {{
                        console.log('No listings to display');
                    }}
                    
                    // Start stopwatch update interval
                    setInterval(updateStopwatch, 1000);
                }};
            </script>
        </head>
        <body>
            <div class="container listing-container">
                <!-- NEW: Top bar with three colored rectangles -->
                <div class="top-bar">
                    <button class="top-bar-item refresh-button" onclick="refreshPage()">
                        Refresh Page
                    </button>
                    <div class="top-bar-item listing-counter" id="listing-counter">
                        1 of 1
                    </div>
                    <div class="top-bar-item stopwatch-display" id="stopwatch-display">
                        No stopwatch - listing unbookmarked
                    </div>
                </div>
                
                <div class="section-box">
                    <p><span class="content-title">{title}</span></p>
                </div>
                <div class="financial-row">
                    <div class="financial-item">
                        <p><span class="content-price">{price}</span></p>
                    </div>
                    <div class="financial-item">
                        <p><span class="content-profit">{profit}</span></p>
                    </div>
                </div>
                <div class="section-box">
                    <p><span class="content-description">{description}</span></p>
                </div>
                
                <!-- Single button for opening listing -->
                <div class="single-button-container">
                    <button class="custom-button open-listing-button" onclick="openListing()">
                        Open Listing in New Tab
                    </button>
                </div>
                
                <!-- Buy decision buttons -->
                <div class="buy-decision-container">
                    <button class="buy-yes-button" onclick="buyYes()">
                        Yes - Buy now
                    </button>
                    <button class="buy-no-button" onclick="buyNo()">
                        No - Do not purchase
                    </button>
                </div>
                
                <!-- Confirmation dialog (initially hidden) -->
                <div class="confirmation-container">
                    <div class="confirmation-text">
                        Are you sure?
                    </div>
                    <div class="confirmation-buttons">
                        <button class="confirm-yes-button">
                            Yes
                        </button>
                        <button class="confirm-no-button">
                            No
                        </button>
                    </div>
                </div>
                
                <div class="details-row">
                    <div class="details-item">
                        <p><span class="content-detected-items">{detected_items}</span></p>
                    </div>
                </div>
                <div class="image-container">
                    {image_html}
                </div>
                <div class="details-item">
                    <p><span class="content-join-date">{join_date}</span></p>
                </div>
                <div class="navigation-buttons">
                    <button onclick="changeListingIndex('previous')" class="custom-button" style="background-color: #666;">Previous</button>
                    <button onclick="changeListingIndex('next')" class="custom-button" style="background-color: #666;">Next</button>
                </div>
                <div class="listing-url" id="listing-url">
                    <p><span class="header">Listing URL: </span><span class="content-url">{listing_url}</span></p>
                </div>
            </div>
        </body>
        </html>
        '''
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR in render_main_page: {e}")
        print(f"Traceback: {error_details}")
        return f"<html><body><h1>Error in render_main_page</h1><pre>{error_details}</pre></body></html>"

def base64_encode_image(img):
    """Convert PIL Image to base64 string, resizing if necessary"""
    max_size = (200, 200)
    img.thumbnail(max_size, Image.LANCZOS)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


class VintedScraper:

    def restart_driver_if_dead(self, driver):
        """If driver is dead, create a new one. That's it."""
        try:
            driver.current_url  # Simple test
            return driver  # Driver is fine
        except:
            print("🔄 Driver crashed, restarting...")
            try:
                driver.quit()
            except:
                pass
            return self.setup_driver()
    # Add this method to the VintedScraper class
    def send_pushover_notification(self, title, message, api_token, user_key):
        """
        Send a notification via Pushover
        :param title: Notification title
        :param message: Notification message
        :param api_token: Pushover API token
        :param user_key: Pushover user key
        """
        try:
            url = "https://api.pushover.net/1/messages.json"
            payload = {
                "token": api_token,
                "user": user_key,
                "title": title,
                "message": message
            }
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                print(f"Notification sent successfully: {title}")
            else:
                print(f"Failed to send notification. Status code: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error sending Pushover notification: {str(e)}")

    def fetch_price(self, class_name):
        if class_name in ['lite_box', 'oled_box', 'oled_in_tv', 'switch_box', 'switch_in_tv', 'other_mario']:
            return None
        price = BASE_PRICES.get(class_name, 0)
        delivery_cost = 5.0 if class_name in ['lite', 'oled', 'switch'] else 3.5
        final_price = price + delivery_cost
        return final_price
    def fetch_all_prices(self):
        all_prices = {class_name: self.fetch_price(class_name) for class_name in class_names if self.fetch_price(class_name) is not None}
        all_prices.update({
            'lite_box': all_prices.get('lite', 0) * 1.05, 
            'oled_box': all_prices.get('oled', 0) + all_prices.get('comfort_h', 0) + all_prices.get('tv_white', 0) - 15, 
            'oled_in_tv': all_prices.get('oled', 0) + all_prices.get('tv_white', 0) - 10, 
            'switch_box': all_prices.get('switch', 0) + all_prices.get('comfort_h', 0) + all_prices.get('tv_black', 0) - 5, 
            'switch_in_tv': all_prices.get('switch', 0) + all_prices.get('tv_black', 0) - 3.5, 
            'other_mario': 22.5,
            'anonymous_games': 5  # Add price for anonymous games
        })
        return all_prices
    def __init__(self):

        # Initialize pygame-related variables similar to FacebookScraper
        global current_listing_title, current_listing_description, current_listing_join_date, current_listing_price
        global current_expected_revenue, current_profit, current_detected_items, current_listing_images
        global current_bounding_boxes, current_listing_url, current_suitability, suitable_listings
        global current_listing_index, recent_listings
        
        # **CRITICAL FIX: Initialize recent_listings for website navigation**
        recent_listings = {
            'listings': [],
            'current_index': 0
        }
        
        # Initialize all current listing variables
        current_listing_title = "No title"
        current_listing_description = "No description"
        current_listing_join_date = "No join date"
        current_listing_price = "0"
        current_expected_revenue = "0"
        current_profit = "0"
        current_detected_items = "None"
        current_listing_images = []
        current_bounding_boxes = {}
        current_listing_url = ""
        current_suitability = "Suitability unknown"
        suitable_listings = []
        current_listing_index = 0
        self.monitoring_threads_active = threading.Event()

        self.vinted_button_queue = queue.Queue()
        self.vinted_processing_active = threading.Event()  # To track if we're currently processing
        self.main_driver = None
        self.persistent_buying_driver = None
        self.main_tab_handle = None
        self.clicked_yes_listings = set()
        self.bookmark_timers = {}
        self.buying_drivers = {}  # Dictionary to store drivers {1: driver_object, 2: driver_object, etc.}
        self.driver_status = {}   # Track driver status {1: 'free'/'busy', 2: 'free'/'busy', etc.}
        self.driver_lock = threading.Lock()  # Thread safety for driver management
        # Check if CUDA is available
        
        print(f"CUDA available: {torch.cuda.is_available()}")
        print(f"GPU name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'No GPU'}")

        # Load model with explicit GPU usage
        if torch.cuda.is_available():
            model = YOLO(MODEL_WEIGHTS).cuda()  # Force GPU
            print("✅ YOLO model loaded on GPU")
        else:
            model = YOLO(MODEL_WEIGHTS).cpu()   # Fallback to CPU
            print("⚠️ YOLO model loaded on CPU (no CUDA available)")

        # Initialize all driver slots as not created
        for i in range(1, 6):  # Drivers 1-5
            self.buying_drivers[i] = None
            self.driver_status[i] = 'not_created'

        self.bookmark_driver_threads = {}  # Track threads for each driver
        self.bookmark_driver_locks = {}    # Lock for each driver
        
        # Initialize locks for each bookmark driver
        for i in range(5):
            self.bookmark_driver_locks[i] = threading.Lock()


        self.current_bookmark_driver_index = 0
        self.bookmark_driver_configs = [
            {
                'user_data_dir': 'C:\\VintedScraper_Default_Bookmark',
                'profile_directory': 'Profile 4'
            },
            {
                'user_data_dir': 'C:\\VintedScraper_Default2_Bookmark', 
                'profile_directory': 'Profile 17'
            },
            {
                'user_data_dir': 'C:\\VintedScraper_Default3_Bookmark',
                'profile_directory': 'Profile 6' 
            },
            {
                'user_data_dir': 'C:\\VintedScraper_Default4_Bookmark',
                'profile_directory': 'Profile 12'
            },
            {
                'user_data_dir': 'C:\\VintedScraper_Default5_Bookmark',
                'profile_directory': 'Profile 18'
            }
        ]
        self.current_bookmark_driver = None
        self.shutdown_event = threading.Event()


    def cleanup_all_bookmark_threads(self):
        """
        Clean up all bookmark driver threads when program exits
        """
        print("🧹 CLEANUP: Stopping all bookmark driver threads...")
        
        active_threads = []
        for driver_index, thread in self.bookmark_driver_threads.items():
            if thread and thread.is_alive():
                active_threads.append((driver_index + 1, thread))
        
        if active_threads:
            print(f"🧹 CLEANUP: Found {len(active_threads)} active bookmark threads")
            
            # Give threads 10 seconds to finish naturally
            print("⏳ CLEANUP: Waiting 10 seconds for threads to complete...")
            for driver_num, thread in active_threads:
                thread.join(timeout=10)
                if thread.is_alive():
                    print(f"⚠️ CLEANUP: BookmarkDriver-{driver_num} still running after timeout")
                else:
                    print(f"✅ CLEANUP: BookmarkDriver-{driver_num} completed")
        
        print("✅ CLEANUP: Bookmark thread cleanup completed")

    def bookmark_driver_threaded(self, listing_url, username=None):
        """
        THREADED VERSION: Run each bookmark driver in its own thread
        """
        # Get the next available driver index (cycle through 0-4)
        with threading.Lock():  # Ensure thread-safe driver selection
            driver_index = self.current_bookmark_driver_index
            self.current_bookmark_driver_index = (self.current_bookmark_driver_index + 1) % 5
        
        # Start the bookmark process in a separate thread for this driver
        thread_name = f"BookmarkDriver-{driver_index + 1}"
        bookmark_thread = threading.Thread(
            target=self._bookmark_driver_thread_worker,
            args=(driver_index, listing_url, username),
            name=thread_name
        )
        bookmark_thread.daemon = True
        bookmark_thread.start()
        
        # Track the thread
        self.bookmark_driver_threads[driver_index] = bookmark_thread
        
        print(f"🧵 BOOKMARK: Started {thread_name} for URL: {listing_url[:50]}...")
        return True

    def _bookmark_driver_thread_worker(self, driver_index, listing_url, username):
        """
        Worker function that runs in each bookmark driver thread
        """
        thread_name = f"BookmarkDriver-{driver_index + 1}"
        
        with self.bookmark_driver_locks[driver_index]:
            print(f"🔖 {thread_name}: Starting bookmark process...")
            
            try:
                # Create driver for this specific thread
                config = self.bookmark_driver_configs[driver_index]
                driver = self._create_bookmark_driver(config, driver_index)
                
                if driver is None:
                    print(f"❌ {thread_name}: Failed to create driver")
                    return
                
                # Execute the bookmark process using existing logic
                step_log = self._initialize_step_logging()
                step_log['driver_number'] = driver_index + 1
                
                # Validate inputs
                if not self._validate_bookmark_inputs(listing_url, username, step_log):
                    print(f"❌ {thread_name}: Input validation failed")
                    return
                
                # Execute bookmark sequences
                success = self._execute_bookmark_sequences_with_monitoring(
                    driver, listing_url, username, step_log
                )
                
                if success:
                    print(f"✅ {thread_name}: Bookmark process completed successfully")
                else:
                    print(f"❌ {thread_name}: Bookmark process failed")
                    
            except Exception as e:
                print(f"❌ {thread_name}: Thread error: {e}")
                import traceback
                traceback.print_exc()
                
            finally:
                # Clean up driver
                try:
                    if 'driver' in locals() and driver:
                        driver.quit()
                        print(f"🗑️ {thread_name}: Driver cleaned up")
                except Exception as cleanup_error:
                    print(f"⚠️ {thread_name}: Cleanup error: {cleanup_error}")
                
                print(f"🏁 {thread_name}: Thread completed")

    def _create_bookmark_driver(self, config, driver_index):
        """
        Create a bookmark driver with the specified configuration
        """
        try:
            # Ensure ChromeDriver is cached
            if not hasattr(self, '_cached_chromedriver_path'):
                self._cached_chromedriver_path = ChromeDriverManager().install()
            
            service = Service(self._cached_chromedriver_path, log_path=os.devnull)
            
            chrome_opts = Options()
            chrome_opts.add_argument(f"--user-data-dir={config['user_data_dir']}")
            chrome_opts.add_argument(f"--profile-directory={config['profile_directory']}")
            chrome_opts.add_argument("--no-sandbox")
            chrome_opts.add_argument("--headless")
            chrome_opts.add_argument("--disable-dev-shm-usage")
            chrome_opts.add_argument("--disable-gpu")
            chrome_opts.add_argument("--window-size=800,600")
            chrome_opts.add_argument("--log-level=3")
            chrome_opts.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
            chrome_opts.add_experimental_option('useAutomationExtension', False)
            
            # Create the driver
            driver = webdriver.Chrome(service=service, options=chrome_opts)
            
            # Set timeouts
            driver.implicitly_wait(1)
            driver.set_page_load_timeout(8)
            driver.set_script_timeout(3)
            
            print(f"✅ DRIVER {driver_index + 1}: Created successfully")
            return driver
            
        except Exception as e:
            print(f"❌ DRIVER {driver_index + 1}: Creation failed: {e}")
            return None
                
    def get_next_bookmark_driver(self):
        """
        Get the current ready bookmark driver (already created and waiting)
        If no driver exists (first call), create the first one
        """
        # If no driver exists yet (program startup), create the first one
        if self.current_bookmark_driver is None:
            print(f"🚀 CYCLING: Creating FIRST bookmark driver {self.current_bookmark_driver_index + 1}/5")
            config = self.bookmark_driver_configs[self.current_bookmark_driver_index]
            
            try:
                # Ensure ChromeDriver is cached
                if not hasattr(self, '_cached_chromedriver_path'):
                    self._cached_chromedriver_path = ChromeDriverManager().install()
                
                service = Service(self._cached_chromedriver_path, log_path=os.devnull)
                
                chrome_opts = Options()
                chrome_opts.add_argument(f"--user-data-dir={config['user_data_dir']}")
                chrome_opts.add_argument(f"--profile-directory={config['profile_directory']}")
                chrome_opts.add_argument("--no-sandbox")
                chrome_opts.add_argument("--disable-dev-shm-usage")
                chrome_opts.add_argument("--disable-gpu")
                chrome_opts.add_argument("--window-size=800,600")
                chrome_opts.add_argument("--log-level=3")
                chrome_opts.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
                chrome_opts.add_experimental_option('useAutomationExtension', False)
                
                # Create the driver
                self.current_bookmark_driver = webdriver.Chrome(service=service, options=chrome_opts)
                
                # Set timeouts
                self.current_bookmark_driver.implicitly_wait(1)
                self.current_bookmark_driver.set_page_load_timeout(8)
                self.current_bookmark_driver.set_script_timeout(3)
                
                # DON'T navigate anywhere - leave it blank as requested
                print(f"✅ CYCLING: First driver {self.current_bookmark_driver_index + 1}/5 created and ready (blank page)")
                
            except Exception as e:
                print(f"❌ CYCLING: Failed to create first bookmark driver: {e}")
                return None
        
        # Return the current ready driver (either just created or already waiting from previous close)
        print(f"📋 CYCLING: Using ready driver {self.current_bookmark_driver_index + 1}/5")
        return self.current_bookmark_driver

    def close_current_bookmark_driver(self):
        """
        Close the current bookmark driver, advance to next index, and IMMEDIATELY open the next driver
        """
        if self.current_bookmark_driver is not None:
            try:
                print(f"🗑️ CYCLING: Closing bookmark driver {self.current_bookmark_driver_index + 1}")
                self.current_bookmark_driver.quit()
                time.sleep(0.5)  # Brief pause for cleanup
                print(f"✅ CYCLING: Closed bookmark driver {self.current_bookmark_driver_index + 1}")
            except Exception as e:
                print(f"⚠️ CYCLING: Error closing driver {self.current_bookmark_driver_index + 1}: {e}")
            finally:
                self.current_bookmark_driver = None
        
        # Advance to next driver (cycle back to 0 after 4)
        self.current_bookmark_driver_index = (self.current_bookmark_driver_index + 1) % 5
        
        # IMMEDIATELY open the next driver and keep it ready
        print(f"🚀 CYCLING: IMMEDIATELY opening next driver {self.current_bookmark_driver_index + 1}/5")
        next_config = self.bookmark_driver_configs[self.current_bookmark_driver_index]
        
        try:
            # Ensure ChromeDriver is cached
            if not hasattr(self, '_cached_chromedriver_path'):
                self._cached_chromedriver_path = ChromeDriverManager().install()
            
            service = Service(self._cached_chromedriver_path, log_path=os.devnull)
            
            chrome_opts = Options()
            chrome_opts.add_argument(f"--user-data-dir={next_config['user_data_dir']}")
            chrome_opts.add_argument(f"--profile-directory={next_config['profile_directory']}")
            chrome_opts.add_argument("--no-sandbox")
            chrome_opts.add_argument("--disable-dev-shm-usage")
            chrome_opts.add_argument("--disable-gpu")
            chrome_opts.add_argument("--window-size=800,600")
            chrome_opts.add_argument("--log-level=3")
            chrome_opts.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
            chrome_opts.add_experimental_option('useAutomationExtension', False)
            
            # Create the NEXT driver immediately
            self.current_bookmark_driver = webdriver.Chrome(service=service, options=chrome_opts)
            
            # Set timeouts
            self.current_bookmark_driver.implicitly_wait(1)
            self.current_bookmark_driver.set_page_load_timeout(8)
            self.current_bookmark_driver.set_script_timeout(3)
            
            # DON'T navigate anywhere - leave it blank as requested
            print(f"✅ CYCLING: Driver {self.current_bookmark_driver_index + 1}/5 is now open and ready (blank page)")
            
        except Exception as e:
            print(f"❌ CYCLING: Failed to open next driver {self.current_bookmark_driver_index + 1}: {e}")
            self.current_bookmark_driver = None
    def get_available_driver(self):
        """
        FIXED: Find and reserve the first available driver with proper initialization
        Driver 1 uses the persistent_buying_driver, drivers 2-5 are created on demand
        """
        with self.driver_lock:
            for driver_num in range(1, 6):  # Check drivers 1-5
                # Skip drivers that are currently busy
                if self.driver_status[driver_num] == 'busy':
                    continue
                    
                # Reserve this driver slot
                self.driver_status[driver_num] = 'busy'
                
                # SPECIAL HANDLING FOR DRIVER 1 - use persistent_buying_driver
                if driver_num == 1:
                    print(f"🚗 DRIVER 1: Using persistent buying driver")
                    
                    # Check if persistent driver exists and is alive
                    if self.persistent_buying_driver is None or self.is_persistent_driver_dead():
                        print(f"🚗 DRIVER 1: Persistent driver is dead, recreating...")
                        if not self.setup_persistent_buying_driver():
                            print(f"❌ DRIVER 1: Failed to recreate persistent driver")
                            self.driver_status[driver_num] = 'not_created'
                            continue
                    
                    print(f"✅ RESERVED: Persistent buying driver (driver 1)")
                    return driver_num, self.persistent_buying_driver
                    
                # For drivers 2-5, create on demand as before
                else:
                    if self.buying_drivers[driver_num] is None or self.is_driver_dead(driver_num):
                        print(f"🚗 CREATING: Buying driver {driver_num}")
                        new_driver = self.setup_buying_driver(driver_num)
                        
                        if new_driver is None:
                            print(f"❌ FAILED: Could not create buying driver {driver_num}")
                            self.driver_status[driver_num] = 'not_created'
                            continue
                            
                        self.buying_drivers[driver_num] = new_driver
                        print(f"✅ CREATED: Buying driver {driver_num} successfully")
                    
                    print(f"✅ RESERVED: Buying driver {driver_num}")
                    return driver_num, self.buying_drivers[driver_num]
            
            print("❌ ERROR: All 5 buying drivers are currently busy")
            return None, None
    
    def is_persistent_driver_dead(self):
        """
        Check if the persistent buying driver is dead/unresponsive
        """
        if self.persistent_buying_driver is None:
            return True
            
        try:
            # Try to access current_url to test if driver is alive
            _ = self.persistent_buying_driver.current_url
            return False
        except:
            print(f"💀 DEAD: Persistent buying driver is unresponsive")
            return True

    def is_driver_dead(self, driver_num):
        """
        Check if a driver is dead/unresponsive
        """
        if self.buying_drivers[driver_num] is None:
            return True
            
        try:
            # Try to access current_url to test if driver is alive
            _ = self.buying_drivers[driver_num].current_url
            return False
        except:
            print(f"💀 DEAD: Driver {driver_num} is unresponsive")
            return True

    def release_driver(self, driver_num):
        """
        FIXED: Release a driver back to the free pool with special handling for driver 1
        """
        with self.driver_lock:
            print(f"🔓 RELEASING: Buying driver {driver_num}")
            
            if driver_num == 1:
                # Driver 1 is the persistent driver - keep it alive, just mark as free
                self.driver_status[driver_num] = 'not_created'  # Allow it to be reused
                print(f"🔄 KEPT ALIVE: Persistent buying driver (driver 1) marked as available")
            else:
                # For drivers 2-5, close them after use
                if self.buying_drivers[driver_num] is not None:
                    try:
                        print(f"🗑️ CLOSING: Buying driver {driver_num}")
                        self.buying_drivers[driver_num].quit()
                        
                        # Wait a moment for cleanup
                        time.sleep(0.5)
                        
                        self.buying_drivers[driver_num] = None
                        self.driver_status[driver_num] = 'not_created'
                        print(f"✅ CLOSED: Buying driver {driver_num}")
                    except Exception as e:
                        print(f"⚠️ WARNING: Error closing driver {driver_num}: {e}")
                        self.buying_drivers[driver_num] = None
                        self.driver_status[driver_num] = 'not_created'

    def start_bookmark_stopwatch(self, listing_url):
        """
        Start a stopwatch for a successfully bookmarked listing
        MODIFIED: Now tracks bookmark start time for wait_for_bookmark_stopwatch_to_buy functionality
        """
        print(f"⏱️ STOPWATCH: Starting timer for {listing_url}")
        
        # NEW: Track the start time for this listing
        if not hasattr(self, 'bookmark_start_times'):
            self.bookmark_start_times = {}
        
        # Record when the bookmark timer started
        self.bookmark_start_times[listing_url] = time.time()
        print(f"⏱️ RECORDED: Bookmark start time for {listing_url}")
        
        def stopwatch_timer():
            time.sleep(bookmark_stopwatch_length)
            print(f'LISTING {listing_url} HAS BEEN BOOKMARKED FOR {bookmark_stopwatch_length} SECONDS!')
            
            # Clean up the timer reference
            if listing_url in self.bookmark_timers:
                del self.bookmark_timers[listing_url]
                
            # Clean up the start time reference
            if hasattr(self, 'bookmark_start_times') and listing_url in self.bookmark_start_times:
                del self.bookmark_start_times[listing_url]
        
        # Start the timer thread
        timer_thread = threading.Thread(target=stopwatch_timer)
        timer_thread.daemon = True
        timer_thread.start()
        
        # Store reference to track active timers
        self.bookmark_timers[listing_url] = timer_thread

    def cleanup_bookmark_timers(self):
        """
        Clean up any remaining bookmark timers when shutting down
        """
        print(f"🧹 CLEANUP: Stopping {len(self.bookmark_timers)} active bookmark timers")
        self.bookmark_timers.clear()  # Timer threads are daemon threads, so they'll stop automatically

    def run_pygame_window(self):
        global LOCK_POSITION, current_listing_index, suitable_listings
        screen, clock = self.initialize_pygame_window()
        rectangles = [pygame.Rect(*rect) for rect in self.load_rectangle_config()] if self.load_rectangle_config() else [
            pygame.Rect(0, 0, 240, 180), pygame.Rect(240, 0, 240, 180), pygame.Rect(480, 0, 320, 180),
            pygame.Rect(0, 180, 240, 180), pygame.Rect(240, 180, 240, 180), pygame.Rect(480, 180, 320, 180),
            pygame.Rect(0, 360, 240, 240), pygame.Rect(240, 360, 240, 120), pygame.Rect(240, 480, 240, 120),
            pygame.Rect(480, 360, 160, 240), pygame.Rect(640, 360, 160, 240)
        ]
        fonts = {
            'number': pygame.font.Font(None, 24),
            'price': pygame.font.Font(None, 36),
            'title': pygame.font.Font(None, 40),
            'description': pygame.font.Font(None, 28),
            'join_date': pygame.font.Font(None, 28),
            'revenue': pygame.font.Font(None, 36),
            'profit': pygame.font.Font(None, 36),
            'items': pygame.font.Font(None, 30),
            'click': pygame.font.Font(None, 28),
            'suitability': pygame.font.Font(None, 28),
            'reviews': pygame.font.Font(None, 28),
            'exact_time': pygame.font.Font(None, 22)  # NEW: Font for exact time display
        }
        dragging = False
        resizing = False
        drag_rect = None
        drag_offset = (0, 0)
        resize_edge = None

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:
                        LOCK_POSITION = not LOCK_POSITION
                    elif event.key == pygame.K_RIGHT:
                        if suitable_listings:
                            current_listing_index = (current_listing_index + 1) % len(suitable_listings)
                            self.update_listing_details(**suitable_listings[current_listing_index])
                    elif event.key == pygame.K_LEFT:
                        if suitable_listings:
                            current_listing_index = (current_listing_index - 1) % len(suitable_listings)
                            self.update_listing_details(**suitable_listings[current_listing_index])
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        # Check if rectangle 4 was clicked
                        if rectangles[3].collidepoint(event.pos):
                            if suitable_listings and 0 <= current_listing_index < len(suitable_listings):
                                current_url = suitable_listings[current_listing_index].get('url')
                                if current_url:
                                    try:
                                        import webbrowser
                                        webbrowser.open(current_url)
                                    except Exception as e:
                                        print(f"Failed to open URL: {e}")
                        elif not LOCK_POSITION:
                            for i, rect in enumerate(rectangles):
                                if rect.collidepoint(event.pos):
                                    if event.pos[0] > rect.right - 10 and event.pos[1] > rect.bottom - 10:
                                        resizing = True
                                        drag_rect = i
                                        resize_edge = 'bottom-right'
                                    else:
                                        dragging = True
                                        drag_rect = i
                                        drag_offset = (rect.x - event.pos[0], rect.y - event.pos[1])
                                    break
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        dragging = False
                        resizing = False
                        drag_rect = None
            
            # Handle dragging and resizing
            if dragging and drag_rect is not None:
                rectangles[drag_rect].x = pygame.mouse.get_pos()[0] + drag_offset[0]
                rectangles[drag_rect].y = pygame.mouse.get_pos()[1] + drag_offset[1]
            elif resizing and drag_rect is not None:
                if resize_edge == 'bottom-right':
                    width = max(pygame.mouse.get_pos()[0] - rectangles[drag_rect].left, 20)
                    height = max(pygame.mouse.get_pos()[1] - rectangles[drag_rect].top, 20)
                    rectangles[drag_rect].size = (width, height)
            
            screen.fill((204, 210, 255))
            for i, rect in enumerate(rectangles):
                pygame.draw.rect(screen, (0, 0, 0), rect, 2)
                number_text = fonts['number'].render(str(i + 1), True, (255, 0, 0))
                number_rect = number_text.get_rect(topright=(rect.right - 5, rect.top + 5))
                screen.blit(number_text, number_rect)

                if i == 2:  # Rectangle 3 (index 2) - Title
                    self.render_text_in_rect(screen, fonts['title'], current_listing_title, rect, (0, 0, 0))
                elif i == 1:  # Rectangle 2 (index 1) - Price
                    self.render_text_in_rect(screen, fonts['price'], current_listing_price, rect, (0, 0, 255))
                elif i == 7:  # Rectangle 8 (index 7) - Description
                    self.render_multiline_text(screen, fonts['description'], current_listing_description, rect, (0, 0, 0))
                elif i == 8:  # Rectangle 9 (index 8) - CHANGED: Now shows exact time instead of upload date
                    time_label = "Appended:"
                    self.render_text_in_rect(screen, fonts['exact_time'], f"{time_label}\n{current_listing_join_date}", rect, (0, 128, 0))  # Green color for time
                elif i == 4:  # Rectangle 5 (index 4) - Expected Revenue
                    self.render_text_in_rect(screen, fonts['revenue'], current_expected_revenue, rect, (0, 128, 0))
                elif i == 9:  # Rectangle 10 (index 9) - Profit
                    self.render_text_in_rect(screen, fonts['profit'], current_profit, rect, (128, 0, 128))
                elif i == 0:  # Rectangle 1 (index 0) - Detected Items
                    self.render_multiline_text(screen, fonts['items'], current_detected_items, rect, (0, 0, 0))
                elif i == 10:  # Rectangle 11 (index 10) - Images
                    self.render_images(screen, current_listing_images, rect, current_bounding_boxes)
                elif i == 3:  # Rectangle 4 (index 3) - Click to open
                    click_text = "CLICK TO OPEN LISTING IN CHROME"
                    self.render_text_in_rect(screen, fonts['click'], click_text, rect, (255, 0, 0))
                elif i == 5:  # Rectangle 6 (index 5) - Suitability Reason
                    self.render_text_in_rect(screen, fonts['suitability'], current_suitability, rect, (255, 0, 0) if "Unsuitable" in current_suitability else (0, 255, 0))
                elif i == 6:  # Rectangle 7 (index 6) - Seller Reviews
                    self.render_text_in_rect(screen, fonts['reviews'], current_seller_reviews, rect, (0, 0, 128))  # Dark blue color

            screen.blit(fonts['title'].render("LOCKED" if LOCK_POSITION else "UNLOCKED", True, (255, 0, 0) if LOCK_POSITION else (0, 255, 0)), (10, 10))

            if suitable_listings:
                listing_counter = fonts['number'].render(f"Listing {current_listing_index + 1}/{len(suitable_listings)}", True, (0, 0, 0))
                screen.blit(listing_counter, (10, 40))

            pygame.display.flip()
            clock.tick(30)

        self.save_rectangle_config(rectangles)
        pygame.quit()
        
    def base64_encode_image(self, img):
        """Convert PIL Image to base64 string, resizing if necessary"""
        # Resize image while maintaining aspect ratio
        max_size = (200, 200)
        img.thumbnail(max_size, Image.LANCZOS)
        
        # Convert to base64
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()

    def render_images(self, screen, images, rect, bounding_boxes):
        if not images:
            return

        num_images = len(images)
        if num_images == 1:
            grid_size = 1
        elif 2 <= num_images <= 4:
            grid_size = 2
        else:
            grid_size = 3

        cell_width = rect.width // grid_size
        cell_height = rect.height // grid_size

        for i, img in enumerate(images):
            if i >= grid_size * grid_size:
                break
            row = i // grid_size
            col = i % grid_size
            img = img.resize((cell_width, cell_height))
            img_surface = pygame.image.fromstring(img.tobytes(), img.size, img.mode)
            screen.blit(img_surface, (rect.left + col * cell_width, rect.top + row * cell_height))

        # Display suitability reason
        if FAILURE_REASON_LISTED:
            font = pygame.font.Font(None, 24)
            suitability_text = font.render(current_suitability, True, (255, 0, 0) if "Unsuitable" in current_suitability else (0, 255, 0))
            screen.blit(suitability_text, (rect.left + 10, rect.bottom - 30))

    def initialize_pygame_window(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption("Facebook Marketplace Scanner")
        return screen, pygame.time.Clock()

    def load_rectangle_config(self):
        return json.load(open(CONFIG_FILE, 'r')) if os.path.exists(CONFIG_FILE) else None

    def save_rectangle_config(self, rectangles):
        json.dump([(rect.x, rect.y, rect.width, rect.height) for rect in rectangles], open(CONFIG_FILE, 'w'))
        
    def render_text_in_rect(self, screen, font, text, rect, color):
        words = text.split()
        lines = []
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_width, _ = font.size(test_line)
            if test_width <= rect.width - 10:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        if current_line:
            lines.append(' '.join(current_line))

        total_height = sum(font.size(line)[1] for line in lines)
        if total_height > rect.height:
            scale_factor = rect.height / total_height
            new_font_size = max(1, int(font.get_height() * scale_factor))
            try:
                font = pygame.font.Font(None, new_font_size)  # Use default font
            except pygame.error:
                print(f"Error creating font with size {new_font_size}")
                return  # Skip rendering if font creation fail

        y = rect.top + 5
        for line in lines:
            try:
                text_surface = font.render(line, True, color)
                text_rect = text_surface.get_rect(centerx=rect.centerx, top=y)
                screen.blit(text_surface, text_rect)
                y += font.get_linesize()
            except pygame.error as e:
                print(f"Error rendering text: {e}")
                continue  # Skip this line if rendering fails

    def extract_price(self, text):
        import re
        """
        Extracts a float from a string like '£4.50' or '4.50 GBP'
        Returns 0.0 if nothing is found or text is None
        """
        if not text:
            return 0.0
        match = re.search(r"[\d,.]+", text)
        if match:
            return float(match.group(0).replace(",", ""))
        return 0.0
    
    def render_multiline_text(self, screen, font, text, rect, color):
        # Convert dictionary to formatted string if need
        if isinstance(text, dict):
            text_lines = []
            for key, value in text.items():
                text_lines.append(f"{key}: {value}")
            text = '\n'.join(text_lines)
        
        # Rest of the existing function remains the same
        words = text.split()
        lines = []
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_width, _ = font.size(test_line)
            if test_width <= rect.width - 20:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        if current_line:
            lines.append(' '.join(current_line))

        total_height = sum(font.size(line)[1] for line in lines)
        if total_height > rect.height:
            scale_factor = rect.height / total_height
            new_font_size = max(1, int(font.get_height() * scale_factor))
            try:
                font = pygame.font.Font(None, new_font_size)  # Use default font
            except pygame.error:
                print(f"Error creating font with size {new_font_size}")
                return  # Skip rendering if font creation fails

        y_offset = rect.top + 10
        for line in lines:
            try:
                text_surface = font.render(line, True, color)
                text_rect = text_surface.get_rect(centerx=rect.centerx, top=y_offset)
                screen.blit(text_surface, text_rect)
                y_offset += font.get_linesize()
                if y_offset + font.get_linesize() > rect.bottom - 10:
                    break
            except pygame.error as e:
                print(f"Error rendering text: {e}")
                continue  # Skip this line if rendering fails
        


    def bookmark_stopwatch_wrapper(self, func_name, tab_open_func, *args, **kwargs):
        """
        Wrapper function that times bookmark operations from tab open to ctrl+w
        """
        import time
        
        # Start timing when tab is opened
        start_time = time.time()
        print(f"⏱️ STOPWATCH START: {func_name} - Tab opening...")
        
        try:
            # Execute the tab opening and bookmark operation
            result = tab_open_func(*args, **kwargs)
            
            # Stop timing immediately after the 0.25s wait and ctrl+w
            end_time = time.time()
            elapsed = end_time - start_time
            
            print(f"⏱️ STOPWATCH END: {func_name} completed in {elapsed:.3f} seconds")
            return result
            
        except Exception as e:
            end_time = time.time()
            elapsed = end_time - start_time
            print(f"⏱️ STOPWATCH END: {func_name} failed after {elapsed:.3f} seconds - {e}")
            raise
    def update_listing_details(self, title, description, join_date, price, expected_revenue, profit, detected_items, processed_images, bounding_boxes, url=None, suitability=None, seller_reviews=None):
        global current_listing_title, current_listing_description, current_listing_join_date, current_listing_price
        global current_expected_revenue, current_profit, current_detected_items, current_listing_images 
        global current_bounding_boxes, current_listing_url, current_suitability, current_seller_reviews

        # Close and clear existing images
        if 'current_listing_images' in globals():
            for img in current_listing_images:
                try:
                    img.close()  # Explicitly close the image
                except Exception as e:
                    print(f"Error closing image: {str(e)}")
            current_listing_images.clear()

        if processed_images:
            for img in processed_images:
                try:
                    img_copy = img.copy()  # Create a fresh copy
                    current_listing_images.append(img_copy)
                except Exception as e:
                    print(f"Error copying image: {str(e)}")
        
        # Store bounding boxes with more robust handling
        current_bounding_boxes = {
            'image_paths': bounding_boxes.get('image_paths', []) if bounding_boxes else [],
            'detected_objects': bounding_boxes.get('detected_objects', {}) if bounding_boxes else {}
        }

        # Handle detected_items for Box 1 - show raw detected objects with counts
        if isinstance(detected_items, dict):
            # Format as "item_name: count" for items with count > 0
            formatted_detected_items = {}
            for item, count in detected_items.items():
                try:
                    count_int = int(count) if isinstance(count, str) else count
                    if count_int > 0:
                        formatted_detected_items[item] = str(count_int)
                except (ValueError, TypeError):
                    continue
            
            if not formatted_detected_items:
                formatted_detected_items = {"no_items": "No items detected"}
        else:
            formatted_detected_items = {"no_items": "No items detected"}

        # FIXED: Use the join_date parameter directly instead of generating new timestamp
        # The join_date parameter now contains the stored timestamp from when item was processed
        stored_append_time = join_date if join_date else "No timestamp"

        # Explicitly set the global variables
        current_detected_items = formatted_detected_items
        current_listing_title = title[:50] + '...' if len(title) > 50 else title
        current_listing_description = description[:200] + '...' if len(description) > 200 else description if description else "No description"
        current_listing_join_date = stored_append_time  # FIXED: Use stored timestamp, not current time
        current_listing_price = f"Price:\n£{float(price):.2f}" if price else "Price:\n£0.00"
        current_expected_revenue = f"Rev:\n£{expected_revenue:.2f}" if expected_revenue else "Rev:\n£0.00"
        current_profit = f"Profit:\n£{profit:.2f}" if profit else "Profit:\n£0.00"
        current_listing_url = url
        current_suitability = suitability if suitability else "Suitability unknown"
        current_seller_reviews = seller_reviews if seller_reviews else "No reviews yet"

    def handle_post_payment_logic(self, driver, driver_num, url):
        """
        Handle the logic after payment is clicked - check for success/errors
        """
        print(f"💳 DRIVER {driver_num}: Handling post-payment logic...")
        
        max_attempts = 250
        attempt = 0
        purchase_successful = False
        
        while not purchase_successful and attempt < max_attempts:
            attempt += 1
            
            if attempt % 10 == 0:  # Print progress every 10 attempts
                print(f"💳 DRIVER {driver_num}: Payment attempt {attempt}/{max_attempts}")
            
            # Check for error first (appears quickly)
            try:
                error_element = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, 
                        "//span[contains(text(), \"Sorry, we couldn't process your payment\")]"))
                )
                
                if error_element:
                    print(f"❌ DRIVER {driver_num}: Payment error detected, retrying...")
                    
                    # Click OK to dismiss error
                    try:
                        ok_button = WebDriverWait(driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(.//text(), 'OK, close')]"))
                        )
                        ok_button.click()
                        print(f"✅ DRIVER {driver_num}: Error dismissed")
                    except:
                        print(f"⚠️ DRIVER {driver_num}: Could not dismiss error")
                    
                    # Wait and try to click pay again
                    time.sleep(buying_driver_click_pay_wait_time)
                    
                    # Re-find and click pay button
                    try:
                        pay_button = driver.find_element(By.CSS_SELECTOR, 
                            'button[data-testid="single-checkout-order-summary-purchase-button"]')
                        pay_button.click()
                    except:
                        print(f"❌ DRIVER {driver_num}: Could not re-click pay button")
                        break
                    
                    continue
            
            except TimeoutException:
                pass  # No error found, continue
            
            # Check for success
            try:
                success_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, 
                        "//h2[text()='Purchase successful']"))
                )
                
                if success_element:
                    print(f"🎉 DRIVER {driver_num}: PURCHASE SUCCESSFUL!")
                    purchase_successful = True
                    
                    # Send success notification
                    try:
                        self.send_pushover_notification(
                            "Vinted Purchase Successful",
                            f"Successfully purchased: {url}",
                            'aks3to8guqjye193w7ajnydk9jaxh5',
                            'ucwc6fi1mzd3gq2ym7jiwg3ggzv1pc'
                        )
                    except Exception as notification_error:
                        print(f"⚠️ DRIVER {driver_num}: Notification failed: {notification_error}")
                    
                    break
            
            except TimeoutException:
                # No success message yet, continue trying
                continue
        
        if not purchase_successful:
            print(f"❌ DRIVER {driver_num}: Purchase failed after {attempt} attempts")
        
        # Clean up
        try:
            driver.close()
            if len(driver.window_handles) > 0:
                driver.switch_to.window(driver.window_handles[0])
        except:
            pass
        
        self.release_driver(driver_num)
        print(f"✅ DRIVER {driver_num}: Post-payment cleanup completed")


    def monitor_for_purchase_unsuccessful(self, url, driver, driver_num, pay_button):
        """
        Monitor for "Purchase unsuccessful" detection from bookmark driver and click pay immediately
        """
        print(f"🔍 DRIVER {driver_num}: Starting 'Purchase unsuccessful' monitoring for {url[:50]}...")
        
        start_time = time.time()
        check_interval = 0.1  # Check every 100ms for ultra-fast response
        timeout = 25 * 60  # 25 minutes timeout
        
        global purchase_unsuccessful_detected_urls
        
        try:
            while True:
                elapsed = time.time() - start_time
                
                # Check timeout
                if elapsed >= timeout:
                    print(f"⏰ DRIVER {driver_num}: Monitoring timeout after {elapsed/60:.1f} minutes")
                    break
                
                # Check if driver is still alive
                try:
                    driver.current_url
                except:
                    print(f"💀 DRIVER {driver_num}: Driver died during monitoring")
                    break
                
                # CRITICAL: Check if "Purchase unsuccessful" was detected
                if url in purchase_unsuccessful_detected_urls:
                    entry = purchase_unsuccessful_detected_urls[url]
                    if not entry.get('waiting', True):  # Flag changed by bookmark driver
                        print(f"🎯 DRIVER {driver_num}: 'Purchase unsuccessful' detected! CLICKING PAY NOW!")
                        
                        # IMMEDIATELY click pay button
                        try:
                            # Try multiple click methods for maximum reliability
                            pay_clicked = False
                            
                            # Method 1: Standard click
                            try:
                                pay_button.click()
                                pay_clicked = True
                                print(f"✅ DRIVER {driver_num}: Pay clicked using standard method")
                            except:
                                # Method 2: JavaScript click
                                try:
                                    driver.execute_script("arguments[0].click();", pay_button)
                                    pay_clicked = True
                                    print(f"✅ DRIVER {driver_num}: Pay clicked using JavaScript")
                                except:
                                    # Method 3: Force enable and click
                                    try:
                                        driver.execute_script("""
                                            arguments[0].disabled = false;
                                            arguments[0].click();
                                        """, pay_button)
                                        pay_clicked = True
                                        print(f"✅ DRIVER {driver_num}: Pay clicked using force method")
                                    except Exception as final_error:
                                        print(f"❌ DRIVER {driver_num}: All pay click methods failed: {final_error}")
                            
                            if pay_clicked:
                                print(f"💳 DRIVER {driver_num}: Payment initiated successfully!")
                                
                                # Continue with existing purchase logic
                                self.handle_post_payment_logic(driver, driver_num, url)
                            
                            break  # Exit monitoring loop
                            
                        except Exception as click_error:
                            print(f"❌ DRIVER {driver_num}: Error clicking pay button: {click_error}")
                            break
                
                # Sleep briefly before next check
                time.sleep(check_interval)
        
        except Exception as monitoring_error:
            print(f"❌ DRIVER {driver_num}: Monitoring error: {monitoring_error}")
        
        finally:
            # Clean up monitoring entry
            if url in purchase_unsuccessful_detected_urls:
                del purchase_unsuccessful_detected_urls[url]
            
            print(f"🧹 DRIVER {driver_num}: Monitoring cleanup completed")


    def process_single_listing_with_driver_modified(self, url, driver_num, driver):
        """
        MODIFIED: Process listing that immediately navigates to buy page and waits for "Purchase unsuccessful"
        """
        print(f"🔥 DRIVER {driver_num}: Starting MODIFIED processing of {url[:50]}...")
        
        try:
            # Driver health check
            try:
                current_url = driver.current_url
                print(f"✅ DRIVER {driver_num}: Driver alive")
            except Exception as e:
                print(f"❌ DRIVER {driver_num}: Driver is dead: {str(e)}")
                return
            
            # Open new tab
            try:
                driver.execute_script("window.open('');")
                new_tab = driver.window_handles[-1]
                driver.switch_to.window(new_tab)
                print(f"✅ DRIVER {driver_num}: New tab opened")
            except Exception as e:
                print(f"❌ DRIVER {driver_num}: Failed to open new tab: {str(e)}")
                return
            
            # Navigate to URL
            actual_url = test_purchase_url if test_purchase_not_true else url
            
            navigation_success = False
            for nav_attempt in range(3):
                try:
                    driver.get(actual_url)
                    WebDriverWait(driver, 8).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                    navigation_success = True
                    print(f"✅ DRIVER {driver_num}: Navigation successful")
                    break
                except Exception as nav_error:
                    print(f"❌ DRIVER {driver_num}: Navigation attempt {nav_attempt+1} failed: {str(nav_error)}")
                    if nav_attempt < 2:
                        time.sleep(1)
            
            if not navigation_success:
                print(f"❌ DRIVER {driver_num}: All navigation attempts failed")
                try:
                    driver.close()
                    if len(driver.window_handles) > 0:
                        driver.switch_to.window(driver.window_handles[0])
                except:
                    pass
                return
            
            # Click Buy now button
            buy_button_clicked = False
            buy_selectors = [
                'button[data-testid="item-buy-button"]',
                'button.web_ui__Button__button.web_ui__Button__filled.web_ui__Button__default.web_ui__Button__primary.web_ui__Button__truncated',
                '//button[@data-testid="item-buy-button"]',
                '//button[contains(@class, "web_ui__Button__primary")]//span[text()="Buy now"]'
            ]
            
            for selector in buy_selectors:
                try:
                    if selector.startswith('//'):
                        buy_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        buy_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    
                    # Try multiple click methods
                    for click_method in ['standard', 'javascript']:
                        try:
                            if click_method == 'standard':
                                buy_button.click()
                            else:
                                driver.execute_script("arguments[0].click();", buy_button)
                            
                            buy_button_clicked = True
                            print(f"✅ DRIVER {driver_num}: Buy button clicked using {click_method}")
                            break
                        except Exception as click_error:
                            continue
                    
                    if buy_button_clicked:
                        break
                        
                except Exception as selector_error:
                    continue
            
            if not buy_button_clicked:
                print(f"❌ DRIVER {driver_num}: Could not click buy button - item likely sold")
                try:
                    driver.close()
                    if len(driver.window_handles) > 0:
                        driver.switch_to.window(driver.window_handles[0])
                except:
                    pass
                return
            
            # MODIFIED: Find and store pay button location BUT DON'T CLICK YET
            print(f"🔍 DRIVER {driver_num}: Finding pay button (but not clicking yet)...")
            
            pay_button = None
            pay_selectors = [
                'button[data-testid="single-checkout-order-summary-purchase-button"]',
                '//button[@data-testid="single-checkout-order-summary-purchase-button"]'
            ]
            
            for selector in pay_selectors:
                try:
                    if selector.startswith('//'):
                        pay_button = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, selector))
                        )
                    else:
                        pay_button = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                    
                    print(f"✅ DRIVER {driver_num}: Pay button found and stored")
                    break
                    
                except Exception as selector_error:
                    continue
            
            if not pay_button:
                print(f"❌ DRIVER {driver_num}: Could not find pay button")
                try:
                    driver.close()
                    if len(driver.window_handles) > 0:
                        driver.switch_to.window(driver.window_handles[0])
                except:
                    pass
                return
            
            # MODIFIED: Register this URL for "Purchase unsuccessful" monitoring
            global purchase_unsuccessful_detected_urls
            purchase_unsuccessful_detected_urls[url] = {
                'driver': driver,
                'driver_num': driver_num,
                'pay_button': pay_button,
                'waiting': True,
                'start_time': time.time()
            }
            
            print(f"🔍 DRIVER {driver_num}: Registered for 'Purchase unsuccessful' monitoring")
            print(f"⏱️ DRIVER {driver_num}: Will wait for bookmark driver to detect 'Purchase unsuccessful'")
            
            # Start monitoring thread for this specific URL
            monitoring_thread = threading.Thread(
                target=self.monitor_for_purchase_unsuccessful,
                args=(url, driver, driver_num, pay_button)
            )
            monitoring_thread.daemon = True
            monitoring_thread.start()
            
        except Exception as critical_error:
            print(f"❌ DRIVER {driver_num}: Critical error: {str(critical_error)}")
            # Clean up
            try:
                driver.close()
                if len(driver.window_handles) > 0:
                    driver.switch_to.window(driver.window_handles[0])
            except:
                pass
            self.release_driver(driver_num)

    def process_single_listing_with_driver(self, url, driver_num, driver):
        """
        ENHANCED: Process a single listing using the specified driver with robust error handling,
        success rate logging, selector alternatives, and failure fast-path
        """
        
        # SUCCESS RATE LOGGING - Track exactly where and when things break
        process_log = {
            'start_time': time.time(),
            'url': url,
            'driver_num': driver_num,
            'steps_completed': [],
            'failures': [],
            'success': False,
            'critical_operations': []
        }
        
        def log_step(step_name, success=True, error_msg=None, duration=None):
            """Log each step for debugging and success rate analysis"""
            elapsed = duration if duration else time.time() - process_log['start_time']
            
            if success:
                process_log['steps_completed'].append(f"{step_name} - {elapsed:.2f}s")
                if print_debug:
                    print(f"✅ DRIVER {driver_num}: {step_name}")
            else:
                process_log['failures'].append(f"{step_name}: {error_msg} - {elapsed:.2f}s")
                print(f"❌ DRIVER {driver_num}: {step_name} - {error_msg}")
        
        def log_final_result():
            """Log comprehensive results for success rate analysis"""
            total_time = time.time() - process_log['start_time']
            print(f"\n📊 PROCESSING ANALYSIS - Driver {driver_num}")
            print(f"🔗 URL: {url[:60]}...")
            print(f"⏱️  Total time: {total_time:.2f}s")
            print(f"✅ Steps completed: {len(process_log['steps_completed'])}")
            print(f"❌ Failures: {len(process_log['failures'])}")
            print(f"🏆 Overall success: {'YES' if process_log['success'] else 'NO'}")
            
            if process_log['failures'] and print_debug:
                print("🔍 FAILURE DETAILS:")
                for failure in process_log['failures'][:5]:  # Show first 5 failures
                    print(f"  • {failure}")

        # SELECTOR ALTERNATIVES - Multiple backup selectors for each critical element
        SELECTOR_SETS = {

            'purchase_unsuccessful': [
                 "//h2[@class='web_uiTexttext web_uiTexttitle web_uiTextleft web_uiTextwarning' and text()='Purchase unsuccessful']",
                "//div[@class='web_uiCelltitle'][@data-testid='conversation-message--status-message--title']//h2[@class='web_uiTexttext web_uiTexttitle web_uiTextleft web_uiTextwarning' and text()='Purchase unsuccessful']",
                "//div[@class='web_uiCellheading']//div[@class='web_uiCelltitle'][@data-testid='conversation-message--status-message--title']//h2[@class='web_uiTexttext web_uiTexttitle web_uiTextleft web_uiTextwarning' and text()='Purchase unsuccessful']",
                "//*[contains(@class, 'web_uiTextwarning') and text()='Purchase unsuccessful']",
                "//*[text()='Purchase unsuccessful']"
            ],
            
            'buy_button': [
                'button[data-testid="item-buy-button"]',
                'button.web_ui__Button__button.web_ui__Button__filled.web_ui__Button__default.web_ui__Button__primary.web_ui__Button__truncated',
                'button.web_ui__Button__button[data-testid="item-buy-button"]',
                '//button[@data-testid="item-buy-button"]',
                '//button[contains(@class, "web_ui__Button__primary")]//span[text()="Buy now"]',
                '//span[text()="Buy now"]/parent::button'
            ],
            
            'pay_button': [
                'button[data-testid="single-checkout-order-summary-purchase-button"]',
                'button[data-testid="single-checkout-order-summary-purchase-button"].web_ui__Button__primary',
                '//button[@data-testid="single-checkout-order-summary-purchase-button"]',
                'button.web_ui__Button__primary[data-testid*="purchase"]',
                '//button[contains(@data-testid, "purchase-button")]',
                '//button[contains(@class, "web_ui__Button__primary")]'
            ],
            
            'ship_to_home': [
                '//h2[@class="web_ui__Text__text web_ui__Text__title web_ui__Text__left" and text()="Ship to home"]',
                '//h2[contains(@class, "web_ui__Text__title") and text()="Ship to home"]',
                '//h2[text()="Ship to home"]',
                '//*[text()="Ship to home"]'
            ],
            
            'ship_to_pickup': [
                '//h2[@class="web_ui__Text__text web_ui__Text__title web_ui__Text__left" and text()="Ship to pick-up point"]',
                '//h2[contains(@class, "web_ui__Text__title") and text()="Ship to pick-up point"]',
                '//h2[text()="Ship to pick-up point"]',
                '//*[text()="Ship to pick-up point"]'
            ],
            
            'success_message': [
                "//h2[@class='web_ui__Text__text web_ui__Text__title web_ui__Text__left' and text()='Purchase successful']",
                "//h2[contains(@class, 'web_ui__Text__title') and text()='Purchase successful']",
                "//h2[text()='Purchase successful']",
                "//*[contains(text(), 'Purchase successful')]"
            ],
            
            'error_modal': [
                "//span[@class='web_ui__Text__text web_ui__Text__body web_ui__Text__left web_ui__Text__format']//span[@class='web_ui__Text__text web_ui__Text__body web_ui__Text__left' and contains(text(), 'Sorry, we couldn')]",
                "//span[@data-testid='checkout-payment-error-modal--body']",
                "//div[@data-testid='checkout-payment-error-modal--overlay']",
                "//span[contains(text(), \"Sorry, we couldn't process your payment\")]",
                "//*[contains(text(), 'Some of the items belong to another purchase')]"
            ],
            
            'ok_button': [
                "//button[@data-testid='checkout-payment-error-modal-action-button']",
                "//button//span[@class='web_ui__Button__label' and text()='OK, close']",
                "//button[contains(.//text(), 'OK, close')]",
                "//button[contains(@class, 'web_ui__Button__primary')]",
                "//*[text()='OK, close']"
            ]
        }
        
        def try_selectors_fast_fail(driver, selector_set_name, operation='find', timeout=3, click_method='standard'):
            """
            FAILURE FAST-PATH - Try selectors with quick timeouts and fail quickly
            Returns (element, selector_used) or (None, None) if all fail
            """
            selectors = SELECTOR_SETS.get(selector_set_name, [])
            if not selectors:
                log_step(f"no_selectors_{selector_set_name}", False, "No selectors defined")
                return None, None
            
            for i, selector in enumerate(selectors):
                try:
                    if print_debug:
                        print(f"🔍 DRIVER {driver_num}: Trying selector {i+1}/{len(selectors)} for {selector_set_name}")
                    
                    # Use appropriate locator strategy
                    if selector.startswith('//'):
                        if operation == 'click':
                            element = WebDriverWait(driver, timeout).until(
                                EC.element_to_be_clickable((By.XPATH, selector))
                            )
                        else:
                            element = WebDriverWait(driver, timeout).until(
                                EC.presence_of_element_located((By.XPATH, selector))
                            )
                    else:
                        if operation == 'click':
                            element = WebDriverWait(driver, timeout).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                            )
                        else:
                            element = WebDriverWait(driver, timeout).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                            )
                    
                    # If we need to click, try the requested click method(s)
                    if operation == 'click':
                        click_methods = ['standard', 'javascript', 'actionchains'] if click_method == 'all' else [click_method]
                        
                        for method in click_methods:
                            try:
                                if method == 'standard':
                                    element.click()
                                elif method == 'javascript':
                                    driver.execute_script("arguments[0].click();", element)
                                elif method == 'actionchains':
                                    from selenium.webdriver.common.action_chains import ActionChains
                                    ActionChains(driver).move_to_element(element).click().perform()
                                
                                log_step(f"click_{selector_set_name}_{method}", True)
                                break
                            except Exception as click_error:
                                log_step(f"click_{selector_set_name}_{method}_attempt", False, str(click_error))
                                continue
                        else:
                            continue  # All click methods failed, try next selector
                    
                    log_step(f"selector_{selector_set_name}_success", True, f"Used #{i+1}: {selector[:30]}...")
                    return element, selector
                    
                except TimeoutException:
                    log_step(f"selector_{selector_set_name}_{i+1}_timeout", False, f"Timeout after {timeout}s")
                    continue
                except Exception as e:
                    log_step(f"selector_{selector_set_name}_{i+1}_error", False, str(e)[:100])
                    continue
            
            log_step(f"all_selectors_{selector_set_name}_failed", False, f"All {len(selectors)} selectors failed")
            return None, None

        # START OF MAIN PROCESSING LOGIC
        start_time = time.time()
        log_step("processing_started", True)
        
        try:
            print(f"🔥 DRIVER {driver_num}: Starting robust processing of {url[:50]}...")
            
            # DRIVER HEALTH CHECK - Verify driver is alive before using it
            try:
                current_url = driver.current_url
                log_step("driver_health_check", True, f"Driver alive: {current_url[:30]}...")
            except Exception as e:
                log_step("driver_health_check", False, f"Driver is dead: {str(e)}")
                log_final_result()
                return
            
            # TAB MANAGEMENT - Open new tab for processing
            try:
                stopwatch_start = time.time()
                print("⏱️ STOPWATCH: Starting timer for new tab and navigation...")
                driver.execute_script("window.open('');")
                new_tab = driver.window_handles[-1]
                driver.switch_to.window(new_tab)
                log_step("new_tab_opened", True, f"Total tabs: {len(driver.window_handles)}")
            except Exception as e:
                log_step("new_tab_creation", False, str(e))
                log_final_result()
                return

            # URL HANDLING - Support test mode
            if test_purchase_not_true:
                actual_url = test_purchase_url
                log_step("test_mode_url", True, f"Using test URL: {actual_url}")
            else:
                actual_url = url
                log_step("normal_url", True)
            
            # NAVIGATION - Navigate to listing with retry logic
            navigation_success = False
            for nav_attempt in range(3):  # Try up to 3 times
                try:
                    log_step(f"navigation_attempt_{nav_attempt+1}", True)
                    driver.get(actual_url)
                    
                    # Wait for page to load with timeout
                    WebDriverWait(driver, 8).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                    navigation_success = True
                    log_step("navigation_success", True)
                    break
                    
                except TimeoutException:
                    log_step(f"navigation_timeout_{nav_attempt+1}", False, "Page load timeout")
                    if nav_attempt < 2:  # Not the last attempt
                        time.sleep(1)
                        continue
                except Exception as nav_error:
                    log_step(f"navigation_error_{nav_attempt+1}", False, str(nav_error))
                    if nav_attempt < 2:  # Not the last attempt
                        time.sleep(1)
                        continue

            if not navigation_success:
                log_step("navigation_final_failure", False, "All navigation attempts failed")
                try:
                    driver.close()
                    if len(driver.window_handles) > 0:
                        driver.switch_to.window(driver.window_handles[0])
                except:
                    pass
                log_final_result()
                return

            # BUY BUTTON DETECTION - Look for Buy now button with multiple selectors
            buy_button, buy_selector = try_selectors_fast_fail(
                driver, 'buy_button', operation='click', timeout=10, click_method='all'
            )
            
            if not buy_button:
                log_step("buy_button_not_found", False, "Item likely sold or unavailable")
                try:
                    driver.close()
                    if len(driver.window_handles) > 0:
                        driver.switch_to.window(driver.window_handles[0])
                except:
                    pass
                log_final_result()
                return

            log_step("buy_button_clicked", True, f"Used: {buy_selector[:30]}...")
            process_log['critical_operations'].append("buy_button_clicked")

            # PURCHASE FLOW BRANCHING - Different logic based on actually_purchase_listing
            if actually_purchase_listing:
                log_step("purchase_mode_enabled", True, "Starting actual purchase process")
                
                # SHIPPING SELECTION - Click "Ship to home" first if available
                ship_home_element, ship_home_selector = try_selectors_fast_fail(
                    driver, 'ship_to_home', operation='click', timeout=15, click_method='all'
                )
                
                if ship_home_element:
                    log_step("ship_to_home_clicked", True)
                    time.sleep(2)  # Brief wait as requested
                else:
                    log_step("ship_to_home_not_found", False, "Continuing without shipping selection")
                
                # PAY BUTTON DETECTION - Look for pay button
                pay_button, pay_selector = try_selectors_fast_fail(
                    driver, 'pay_button', operation='find', timeout=15
                )
                
                if not pay_button:
                    log_step("pay_button_not_found", False, "Payment interface not available")
                    try:
                        driver.close()
                        if len(driver.window_handles) > 0:
                            driver.switch_to.window(driver.window_handles[0])
                    except:
                        pass
                    log_final_result()
                    return

                log_step("pay_button_found", True)
                process_log['critical_operations'].append("pay_button_found")

                # PURCHASE LOOP - Attempt purchase with error handling
                purchase_successful = False
                max_attempts = 250
                attempt = 0
                
                while not purchase_successful and attempt < max_attempts:
                    attempt += 1
                    elapsed_time = time.time() - start_time
                    
                    # Check timeout
                    if elapsed_time >= bookmark_stopwatch_length:
                        log_step("purchase_timeout", False, f"Timeout after {elapsed_time:.1f}s")
                        break
                    
                    if print_debug:
                        print(f"💳 DRIVER {driver_num}: Purchase attempt {attempt}")
                    
                    # CLICK PAY BUTTON
                    pay_clicked = False
                    for click_method in ['standard', 'javascript']:
                        try:
                            # Re-find pay button for each attempt (DOM may change)
                            current_pay_button = driver.find_element(By.CSS_SELECTOR, 
                                'button[data-testid="single-checkout-order-summary-purchase-button"]'
                            )
                            
                            if click_method == 'standard':
                                current_pay_button.click()
                            else:
                                driver.execute_script("arguments[0].click();", current_pay_button)
                            
                            log_step(f"pay_click_attempt_{attempt}_{click_method}", True)
                            pay_clicked = True
                            break
                            
                        except Exception as click_error:
                            log_step(f"pay_click_attempt_{attempt}_{click_method}", False, str(click_error))
                            continue
                    
                    if not pay_clicked:
                        log_step(f"pay_click_failed_attempt_{attempt}", False, "All click methods failed")
                        break
                    
                    # CHECK FOR ERROR OR SUCCESS
                    # First check for quick error (appears fast)
                    error_found = False
                    error_element, error_selector = try_selectors_fast_fail(
                        driver, 'error_modal', operation='find', timeout=10
                    )
                    
                    if error_element:
                        log_step(f"payment_error_detected_attempt_{attempt}", True, f"Using: {error_selector[:30]}...")
                        error_found = True
                        
                        # Wait before clicking OK
                        if print_debug:
                            print(f"⏳ DRIVER {driver_num}: Waiting {buying_driver_click_pay_wait_time}s before clicking OK")
                        time.sleep(buying_driver_click_pay_wait_time)
                        
                        # CLICK OK BUTTON
                        ok_element, ok_selector = try_selectors_fast_fail(
                            driver, 'ok_button', operation='click', timeout=5, click_method='all'
                        )
                        
                        if ok_element:
                            log_step(f"ok_button_clicked_attempt_{attempt}", True)
                        else:
                            log_step(f"ok_button_not_found_attempt_{attempt}", False, "Could not dismiss error")
                        
                        # Wait before retry
                        time.sleep(buying_driver_click_pay_wait_time)
                        continue
                    
                    # If no error, check for success (takes longer)
                    remaining_time = bookmark_stopwatch_length - (time.time() - start_time)
                    if remaining_time <= 0:
                        log_step("success_check_timeout", False, "No time remaining for success check")
                        break
                    
                    success_timeout = min(15, remaining_time)
                    success_element, success_selector = try_selectors_fast_fail(
                        driver, 'success_message', operation='find', timeout=success_timeout
                    )
                    
                    if success_element:
                        log_step("purchase_successful", True, f"Using: {success_selector[:30]}...")
                        purchase_successful = True
                        process_log['success'] = True
                        process_log['critical_operations'].append("purchase_completed")
                        
                        # Send notification
                        notification_title = "Vinted Purchase Successful"
                        notification_message = f"Successfully purchased: {url}"
                        
                        try:
                            self.send_pushover_notification(
                                notification_title,
                                notification_message,
                                'aks3to8guqjye193w7ajnydk9jaxh5',
                                'ucwc6fi1mzd3gq2ym7jiwg3ggzv1pc'
                            )
                            log_step("success_notification_sent", True)
                        except Exception as notification_error:
                            log_step("success_notification_failed", False, str(notification_error))
                        
                        break
                    else:
                        log_step(f"success_not_found_attempt_{attempt}", False, f"Timeout after {success_timeout}s")
                        break
                
                # Final purchase result
                total_elapsed = time.time() - start_time
                if purchase_successful:
                    log_step("purchase_flow_completed", True, f"Success after {attempt} attempts in {total_elapsed:.2f}s")
                else:
                    log_step("purchase_flow_failed", False, f"Failed after {attempt} attempts in {total_elapsed:.2f}s")

            else:
                log_step("legacy_shipping_mode", True, "Using original shipping alternation logic")
                
                # LEGACY SHIPPING FLOW - Original alternating click logic
                try:
                    pickup_element, pickup_selector = try_selectors_fast_fail(
                        driver, 'ship_to_pickup', operation='find', timeout=10
                    )
                    
                    if pickup_element:
                        log_step("shipping_page_loaded", True)
                        first_click_time = time.time()
                        
                        log_step("alternating_clicks_started", True, f"Duration: {bookmark_stopwatch_length}s")
                        
                        while True:
                            if time.time() - first_click_time >= bookmark_stopwatch_length:
                                log_step("alternating_clicks_timeout", True, "Time limit reached")
                                break
                            
                            # Click pickup point
                            pickup_clicked, _ = try_selectors_fast_fail(
                                driver, 'ship_to_pickup', operation='click', timeout=2, click_method='standard'
                            )
                            
                            if pickup_clicked:
                                log_step("pickup_point_clicked", True)
                            else:
                                log_step("pickup_point_click_failed", False, "Could not click pickup point")
                            
                            time.sleep(buying_driver_click_pay_wait_time)
                            
                            if time.time() - first_click_time >= bookmark_stopwatch_length:
                                break
                            
                            # Click ship to home
                            home_clicked, _ = try_selectors_fast_fail(
                                driver, 'ship_to_home', operation='click', timeout=2, click_method='standard'
                            )
                            
                            if home_clicked:
                                log_step("ship_to_home_clicked", True)
                            else:
                                log_step("ship_to_home_click_failed", False, "Could not click ship to home")
                            
                            time.sleep(buying_driver_click_pay_wait_time)
                        
                        log_step("legacy_shipping_completed", True)
                        process_log['success'] = True
                        
                    else:
                        log_step("shipping_page_not_loaded", False, "Could not find shipping options")
                        
                except Exception as shipping_error:
                    log_step("legacy_shipping_error", False, str(shipping_error))

        except Exception as critical_error:
            log_step("critical_processing_error", False, str(critical_error))
            import traceback
            if print_debug:
                print(f"🔥 DRIVER {driver_num}: Critical error traceback:")
                traceback.print_exc()

        finally:
            # CLEANUP - Always clean up tab and release driver
            cleanup_start = time.time()
            
            try:
                # Close processing tab
                driver.close()
                log_step("processing_tab_closed", True)
                
                # Return to main tab
                if len(driver.window_handles) > 0:
                    driver.switch_to.window(driver.window_handles[0])
                    log_step("returned_to_main_tab", True)
                
            except Exception as cleanup_error:
                log_step("cleanup_error", False, str(cleanup_error))
            
            # Calculate final timing
            total_time = time.time() - start_time
            cleanup_time = time.time() - cleanup_start
            
            log_step("processing_completed", True, f"Total: {total_time:.2f}s, Cleanup: {cleanup_time:.2f}s")
            
            # Log comprehensive results
            log_final_result()
            
            # ALWAYS release the driver
            self.release_driver(driver_num)
            log_step("driver_released", True)


    # Supporting helper function for better timeout management
    def calculate_dynamic_timeout(base_timeout, elapsed_time, max_total_time):
        """
        Calculate dynamic timeout based on elapsed time and maximum allowed time
        """
        remaining_time = max_total_time - elapsed_time
        return min(base_timeout, max(1, remaining_time * 0.5))  # Use half of remaining time, minimum 1s
    def cleanup_processed_images(self, processed_images):

        for img in processed_images:
            try:
                img.close()
                del img
            except:
                pass
        processed_images.clear()
        import gc
        gc.collect()  # Force garbage collection
        
    def cleanup_all_buying_drivers(self):
        """
        FIXED: Clean up all buying drivers when program exits
        """
        print("🧹 CLEANUP: Closing all buying drivers")
        
        with self.driver_lock:
            for driver_num in range(1, 6):
                if self.buying_drivers[driver_num] is not None:
                    try:
                        print(f"🗑️ CLEANUP: Closing buying driver {driver_num}")
                        self.buying_drivers[driver_num].quit()
                        time.sleep(0.2)  # Brief pause between closures
                        print(f"✅ CLEANUP: Closed buying driver {driver_num}")
                    except Exception as e:
                        print(f"⚠️ CLEANUP: Error closing driver {driver_num}: {e}")
                    finally:
                        self.buying_drivers[driver_num] = None
                        self.driver_status[driver_num] = 'not_created'
        
        print("✅ CLEANUP: All buying drivers closed")

    def check_all_drivers_health(self):
        """
        Check the health of all active drivers and recreate dead ones
        Call this periodically if needed
        """
        with self.driver_lock:
            for driver_num in range(1, 6):
                if self.buying_drivers[driver_num] is not None and self.driver_status[driver_num] != 'busy':
                    if self.is_driver_dead(driver_num):
                        print(f"💀 HEALTH: Driver {driver_num} is dead, marking for recreation")
                        try:
                            self.buying_drivers[driver_num].quit()
                        except:
                            pass
                        self.buying_drivers[driver_num] = None
                        self.driver_status[driver_num] = 'not_created'


    def vinted_button_clicked_enhanced(self, url):
        """
        MODIFIED: Enhanced button click handler that immediately opens buying driver on "yes"
        """
        print(f"🔘 VINTED BUTTON: Processing {url}")
        
        # Check if already clicked to prevent duplicates
        if url in self.clicked_yes_listings:
            print(f"🔄 VINTED BUTTON: Listing {url} already processed, ignoring")
            return
        
        # Mark as clicked immediately to prevent race conditions
        self.clicked_yes_listings.add(url)
        
        # MODIFIED: Immediately start buying process when user clicks yes
        print(f"🚀 IMMEDIATE: Starting buying process for {url}")
        
        # Get available driver
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            driver_num, driver = self.get_available_driver()
            
            if driver is not None:
                # Successfully got a driver, process in separate thread
                processing_thread = threading.Thread(
                    target=self.process_single_listing_with_driver_modified,
                    args=(url, driver_num, driver)
                )
                processing_thread.daemon = True
                processing_thread.start()
                return
            
            # No driver available, wait and retry
            retry_count += 1
            print(f"❌ RETRY {retry_count}/{max_retries}: All drivers busy, waiting 2 seconds...")
            time.sleep(2)
        
        # If we get here, all retries failed
        print(f"❌ FAILED: Could not get available driver after {max_retries} retries")
        self.clicked_yes_listings.discard(url)


    def process_vinted_button_queue(self):
        """
        ULTRA-FAST queue processor using persistent driver with tabs
        """
        self.vinted_processing_active.set()
        
        # Ensure persistent driver is ready
        if not self.setup_persistent_buying_driver():
            print("❌ QUEUE: Cannot process - persistent driver setup failed")
            self.vinted_processing_active.clear()
            return
        
        print("🚀 QUEUE: Starting ultra-fast processing...")
        
        while not self.vinted_button_queue.empty():
            try:
                url = self.vinted_button_queue.get_nowait()
                self.handle_single_vinted_button_request_fast(url)
                self.vinted_button_queue.task_done()
            except queue.Empty:
                break
            except Exception as e:
                print(f"❌ QUEUE: Error processing request: {e}")
                continue
        
        print("✅ QUEUE: All requests processed!")
        self.vinted_processing_active.clear()

    def handle_single_vinted_button_request_fast(self, url):
        """
        ULTRA-FAST single request handler with button clicking functionality
        FIXED: Updated Buy now button selectors and added fallback methods
        """
        import time
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException, NoSuchElementException
        
        start_time = time.time()
        
        try:
            # Verify driver is still alive
            self.persistent_buying_driver.current_url
    

            print(f"🔥 FAST: Processing {url}")
            
            # Open new tab
            self.persistent_buying_driver.execute_script("window.open('');")
            new_tab = self.persistent_buying_driver.window_handles[-1]
            self.persistent_buying_driver.switch_to.window(new_tab)
            
            # Navigate to URL
            self.persistent_buying_driver.get(url)
            
            # Wait for page to load
            print("⏱️ FAST: Waiting for page to load...")
            time.sleep(2)
            
            # FIXED: Updated Buy now button selectors
            print("🔘 FAST: Looking for Buy now button...")
            
            # Try multiple selectors based on the HTML you provided
            buy_selectors = [
                # Your exact HTML structure
                'button[data-testid="item-buy-button"]',
                # Alternative selectors that match the class structure
                'button.web_ui__Button__button.web_ui__Button__filled.web_ui__Button__default.web_ui__Button__primary.web_ui__Button__truncated',
                'button.web_ui__Button__button[data-testid="item-buy-button"]',
                # Broader selectors as fallbacks
                'button[data-testid="item-buy-button"] span.web_ui__Button__label',
                'button:has(span.web_ui__Button__label:contains("Buy now"))',
                'button .web_ui__Button__label:contains("Buy now")',
                # XPath selectors for more precise matching
                '//button[@data-testid="item-buy-button"]',
                '//button[contains(@class, "web_ui__Button__primary")]//span[text()="Buy now"]',
                '//span[text()="Buy now"]/ancestor::button'
            ]
            
            buy_button = None
            used_selector = None
            
            for selector in buy_selectors:
                try:
                    print(f"🔍 FAST: Trying selector: {selector}")
                    
                    if selector.startswith('//'):
                        # XPath selector
                        buy_button = WebDriverWait(self.persistent_buying_driver, 2).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        # CSS selector
                        buy_button = WebDriverWait(self.persistent_buying_driver, 2).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    
                    used_selector = selector
                    print(f"✅ FAST: Found Buy now button with selector: {selector}")
                    break
                    
                except TimeoutException:
                    print(f"❌ FAST: Selector failed: {selector}")
                    continue
                except Exception as e:
                    print(f"❌ FAST: Selector error: {selector} - {e}")
                    continue
            
            if buy_button:
                try:
                    # Try multiple click methods
                    print(f"🔘 FAST: Attempting to click Buy now button...")
                    
                    # Method 1: Standard click
                    try:
                        buy_button.click()
                        print("✅ FAST: Standard click successful")
                    except Exception as e:
                        print(f"❌ FAST: Standard click failed: {e}")
                        
                        # Method 2: JavaScript click
                        try:
                            self.persistent_buying_driver.execute_script("arguments[0].click();", buy_button)
                            print("✅ FAST: JavaScript click successful")
                        except Exception as e:
                            print(f"❌ FAST: JavaScript click failed: {e}")
                            
                            # Method 3: ActionChains click
                            try:
                                from selenium.webdriver.common.action_chains import ActionChains
                                ActionChains(self.persistent_buying_driver).move_to_element(buy_button).click().perform()
                                print("✅ FAST: ActionChains click successful")
                            except Exception as e:
                                print(f"❌ FAST: ActionChains click failed: {e}")
                                raise Exception("All click methods failed")
                    
                    # Wait for next page to load - look for "Ship to pick-up point"
                    print("🔍 FAST: Waiting for shipping page to load...")
                    try:
                        pickup_point_header = WebDriverWait(self.persistent_buying_driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, '//h2[@class="web_ui__Text__text web_ui__Text__title web_ui__Text__left" and text()="Ship to pick-up point"]'))
                        )
                        print("✅ FAST: Shipping page loaded")
                        
                        # Record the time when the first click happens
                        first_click_time = time.time()
                        
                        # Start the alternating clicking loop
                        print("🔄 FAST: Starting alternating click sequence...")
                        
                        while True:
                            # Check if bookmark_stopwatch_length time has elapsed
                            if time.time() - first_click_time >= bookmark_stopwatch_length:
                                print(f"⏰ FAST: {bookmark_stopwatch_length} seconds elapsed, stopping clicks")
                                break
                            
                            # Click "Ship to pick-up point"
                            try:
                                pickup_point = self.persistent_buying_driver.find_element(
                                    By.XPATH, 
                                    '//h2[@class="web_ui__Text__text web_ui__Text__title web_ui__Text__left" and text()="Ship to pick-up point"]'
                                )
                                pickup_point.click()
                                print("📦 FAST: Clicked 'Ship to pick-up point'")
                            except (NoSuchElementException, Exception) as e:
                                print(f"⚠️ FAST: Could not click 'Ship to pick-up point': {e}")
                            
                            # Wait the specified time
                            time.sleep(buying_driver_click_pay_wait_time)
                            
                            # Check time again before next click
                            if time.time() - first_click_time >= bookmark_stopwatch_length:
                                print(f"⏰ FAST: {bookmark_stopwatch_length} seconds elapsed, stopping clicks")
                                break
                            
                            # Click "Ship to home"
                            try:
                                ship_to_home = self.persistent_buying_driver.find_element(
                                    By.XPATH, 
                                    '//h2[@class="web_ui__Text__text web_ui__Text__title web_ui__Text__left" and text()="Ship to home"]'
                                )
                                ship_to_home.click()
                                print("🏠 FAST: Clicked 'Ship to home'")
                            except (NoSuchElementException, Exception) as e:
                                print(f"⚠️ FAST: Could not click 'Ship to home': {e}")
                            
                            # Wait the specified time
                            time.sleep(buying_driver_click_pay_wait_time)
                    
                    except TimeoutException:
                        print("⚠️ FAST: Timeout waiting for shipping page to load")
                    except Exception as e:
                        print(f"❌ FAST: Error during shipping page interaction: {e}")
                except Exception as click_e:
                    print(f"❌ FAST: Error clicking Buy now button: {click_e}")
            else:
                print("⚠️ FAST: Buy now button not found with any selector")
                # DEBUGGING: Print page source snippet to help diagnose
                try:
                    page_source = self.persistent_buying_driver.page_source
                    if 'Buy now' in page_source:
                        print("🔍 FAST: 'Buy now' text found in page source")
                        # Find the button element in page source
                        import re
                        button_pattern = r'<button[^>]*Buy now[^>]*</button>'
                        matches = re.findall(button_pattern, page_source, re.IGNORECASE | re.DOTALL)
                        for i, match in enumerate(matches[:3]):  # Show first 3 matches
                            print(f"🔍 FAST: Button HTML {i+1}: {match[:200]}...")
                    else:
                        print("❌ FAST: 'Buy now' text not found in page source")
                        
                        # Check if page loaded properly
                        if 'vinted' in self.persistent_buying_driver.current_url:
                            print("✅ FAST: On Vinted page")
                            print(f"🔍 FAST: Current URL: {self.persistent_buying_driver.current_url}")
                            print(f"🔍 FAST: Page title: {self.persistent_buying_driver.title}")
                        else:
                            print("❌ FAST: Not on Vinted page")
                            
                except Exception as debug_e:
                    print(f"❌ FAST: Debug info collection failed: {debug_e}")
            
            # Close the tab
            self.persistent_buying_driver.close()
            
            # Switch back to main tab
            self.persistent_buying_driver.switch_to.window(self.main_tab_handle)
            
            elapsed = time.time() - start_time
            print(f"✅ FAST: Completed in {elapsed:.2f} seconds")
            
        except Exception as e:
            print(f"❌ FAST: Error processing {url}: {e}")
            
            # Try to recover by switching back to main tab
            try:
                if self.main_tab_handle in self.persistent_buying_driver.window_handles:
                    self.persistent_buying_driver.switch_to.window(self.main_tab_handle)
            except:
                pass

    def cleanup_persistent_buying_driver(self):
        """
        Clean up the persistent buying driver when program exits
        """
        if self.persistent_buying_driver is not None:
            try:
                self.persistent_buying_driver.quit()
                print("🔒 CLEANUP: Persistent buying driver closed")
            except:
                pass
            finally:
                self.persistent_buying_driver = None
                self.main_tab_handle = None
    
    def setup_driver(self):
        """
        Enhanced Chrome driver setup with better stability and crash prevention
        """
        chrome_opts = Options()
        
        # Basic preferences
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_values.popups": 0,
            "download.prompt_for_download": False,
        }
        options = Options()
        options.add_experimental_option("prefs", prefs)
        #options.add_argument("--headless")


        options.add_argument("--max_old_space_size=4096")  # Prevent memory crashes
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-ipc-flooding-protection")
        options.add_argument("--memory-pressure-off")  # Critical for long-running
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=800,600")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--remote-debugging-port=0")
        options.add_argument("--log-level=3")
        options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument(f"--user-data-dir={PERMANENT_USER_DATA_DIR}")
        options.add_argument(f"--profile-directory=Default")
        try:
            service = Service(
                ChromeDriverManager().install(),
                log_path=os.devnull  # Suppress driver logs
            )
            
            # Add service arguments for additional stability
            service_args = [
                '--verbose=false',
                '--silent',
                '--log-level=3'
            ]
            
            print("🚀 Starting Chrome driver with enhanced stability settings...")
            driver = webdriver.Chrome(service=service, options=options)
            
            # Set timeouts
            driver.implicitly_wait(10)
            driver.set_page_load_timeout(30)
            driver.set_script_timeout(30)
            
            print("✅ Chrome driver initialized successfully")
            return driver
            
        except Exception as e:
            print(f"❌ CRITICAL: Chrome driver failed to start: {e}")
            print("Troubleshooting steps:")
            print("1. Ensure all Chrome instances are closed")
            print("2. Check Chrome and ChromeDriver versions")
            print("3. Verify user data directory permissions")
            print("4. Try restarting the system")
            
            # Try fallback options
            print("⏳ Attempting fallback configuration...")
            
            # Fallback: Remove problematic arguments
            fallback_opts = Options()
            fallback_opts.add_experimental_option("prefs", prefs)
            #fallback_opts.add_argument("--headless")
            fallback_opts.add_argument("--no-sandbox")
            fallback_opts.add_argument("--disable-dev-shm-usage")
            fallback_opts.add_argument("--disable-gpu")
            fallback_opts.add_argument("--remote-debugging-port=0")
            fallback_opts.add_argument(f"--user-data-dir={PERMANENT_USER_DATA_DIR}")
            fallback_opts.add_argument(f"--profile-directory=Default")
            #profile 2 = pc
            #default = laptop
            
            try:
                fallback_driver = webdriver.Chrome(service=service, options=fallback_opts)
                print("✅ Fallback Chrome driver started successfully")
                return fallback_driver
            except Exception as fallback_error:
                print(f"❌ Fallback also failed: {fallback_error}")
                raise Exception(f"Could not start Chrome driver: {e}")
            

    def setup_buying_driver(self, driver_num):
        """
        FIXED: Setup a specific buying driver with better error handling and unique directories
        """
        try:
            print(f"🚗 SETUP: Creating buying driver {driver_num}")
            
            # Ensure ChromeDriver is cached
            if not hasattr(self, '_cached_chromedriver_path'):
                self._cached_chromedriver_path = ChromeDriverManager().install()
            
            service = Service(self._cached_chromedriver_path, log_path=os.devnull)
            
            chrome_opts = Options()
            
            # CRITICAL FIX: Each driver gets its own UNIQUE directory to prevent conflicts
            user_data_dir = f"C:\\VintedBuyer{driver_num}"  # Add timestamp for uniqueness
            chrome_opts.add_argument(f"--user-data-dir={user_data_dir}")
            chrome_opts.add_argument("--profile-directory=Default")
            
            # FIXED: Better stability options
            chrome_opts.add_argument("--no-sandbox")
            chrome_opts.add_argument("--disable-dev-shm-usage")
            chrome_opts.add_argument("--disable-gpu")
            chrome_opts.add_argument("--disable-extensions")
            chrome_opts.add_argument("--disable-plugins")
            chrome_opts.add_argument("--disable-images")  # Speed optimization
            chrome_opts.add_argument("--window-size=800,600")
            chrome_opts.add_argument("--log-level=3")
            chrome_opts.add_argument("--disable-web-security")
            chrome_opts.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
            chrome_opts.add_experimental_option('useAutomationExtension', False)
            
            # Create the driver
            driver = webdriver.Chrome(service=service, options=chrome_opts)
            
            # FIXED: Set appropriate timeouts for buying process
            driver.implicitly_wait(2)
            driver.set_page_load_timeout(15)  # Increased for stability
            driver.set_script_timeout(10)
            
            # CRITICAL FIX: Navigate to vinted.co.uk and WAIT for it to fully load
            print(f"🏠 NAVIGATE: Driver {driver_num} going to vinted.co.uk")
            driver.get("https://www.vinted.co.uk")
            
            # Wait for page to load completely before marking as ready
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                print(f"✅ SUCCESS: Buying driver {driver_num} fully loaded and ready")
            except TimeoutException:
                print(f"⚠️ WARNING: Driver {driver_num} loaded but page may not be fully ready")
            
            return driver
            
        except Exception as e:
            print(f"❌ ERROR: Failed to create buying driver {driver_num}: {e}")
            return None
            

    def extract_vinted_price(self, text):
        """
        Enhanced price extraction for Vinted that handles various price formats
        """
        debug_function_call("extract_vinted_price")
        import re  # FIXED: Import re at function level
        
        if not text:
            return 0.0
        
        # Remove currency symbols and extra text, extract number
        cleaned_text = re.sub(r'[^\d.,]', '', str(text))
        if not cleaned_text:
            return 0.0
            
        # Handle comma as decimal separator (European format)
        if ',' in cleaned_text and '.' not in cleaned_text:
            cleaned_text = cleaned_text.replace(',', '.')
        elif ',' in cleaned_text and '.' in cleaned_text:
            # Assume comma is thousands separator
            cleaned_text = cleaned_text.replace(',', '')
        
        try:
            return float(cleaned_text)
        except ValueError:
            return 0.0
        
    def detect_console_keywords_vinted(self, listing_title, listing_description):
        """
        Detect console keywords in Vinted title and description (ported from Facebook)
        """
        listing_title_lower = listing_title.lower()
        listing_description_lower = listing_description.lower()
        
        console_keywords = {
            'switch console': 'switch',
            'swith console': 'switch',
            'switc console': 'switch',
            'swich console': 'switch',
            'oled console': 'oled',
            'lite console': 'lite'
        }
        
        # Check if title contains console keywords
        title_contains_console = any(keyword in listing_title_lower for keyword in console_keywords.keys())
        
        # Check if description contains console keywords and title contains relevant terms
        desc_contains_console = any(
            keyword in listing_description_lower and
            any(term in listing_title_lower for term in ['nintendo switch', 'oled', 'lite'])
            for keyword in console_keywords.keys()
        )
        
        detected_console = None
        if title_contains_console or desc_contains_console:
            for keyword, console_type in console_keywords.items():
                if keyword in listing_title_lower or keyword in listing_description_lower:
                    detected_console = console_type
                    break
        
        return detected_console

    def detect_anonymous_games_vinted(self, listing_title, listing_description):
        """
        Detect anonymous games count from title and description (ported from Facebook)
        """
        debug_function_call("detect_anonymous_games_vinted")
        import re  # FIXED: Import re at function level

        def extract_games_number(text):
            # Prioritize specific game type matches first
            matches = (
                re.findall(r'(\d+)\s*(switch|nintendo)\s*games', text.lower()) + # Switch/Nintendo specific
                re.findall(r'(\d+)\s*games', text.lower()) # Generic games
            )
            # Convert matches to integers and find the maximum
            numeric_matches = [int(match[0]) if isinstance(match, tuple) else int(match) for match in matches]
            return max(numeric_matches) if numeric_matches else 0
        
        title_games = extract_games_number(listing_title)
        desc_games = extract_games_number(listing_description)
        return max(title_games, desc_games)

    def detect_sd_card_vinted(self, listing_title, listing_description):
        """
        Detect SD card presence in title or description
        """
        sd_card_keywords = {'sd card', 'sdcard', 'sd', 'card', 'memory card', 'memorycard', 'micro sd', 'microsd',
                        'memory card', 'memorycard', 'sandisk', '128gb', '256gb', 'game'}
        
        title_lower = listing_title.lower()
        desc_lower = listing_description.lower()
        
        return any(keyword in title_lower or keyword in desc_lower for keyword in sd_card_keywords)

    def handle_mutually_exclusive_items_vinted(self, detected_objects, confidences):
        """
        Handle mutually exclusive items for Vinted (ported from Facebook)
        """
        mutually_exclusive_items = ['switch', 'oled', 'lite', 'switch_box', 'oled_box', 'lite_box', 'switch_in_tv', 'oled_in_tv']
        
        # Find the item with highest confidence
        selected_item = max(confidences.items(), key=lambda x: x[1])[0] if any(confidences.values()) else None
        
        if selected_item:
            # Set the selected item to 1 and all others to 0
            for item in mutually_exclusive_items:
                detected_objects[item] = 1 if item == selected_item else 0
                
            # Handle accessory incompatibilities
            if selected_item in ['oled', 'oled_in_tv', 'oled_box']:
                detected_objects['tv_black'] = 0
            elif selected_item in ['switch', 'switch_in_tv', 'switch_box']:
                detected_objects['tv_white'] = 0
                
            if selected_item in ['lite', 'lite_box', 'switch_box', 'oled_box']:
                detected_objects['comfort_h'] = 0
                
            if selected_item in ['switch_in_tv', 'switch_box']:
                detected_objects['tv_black'] = 0
                
            if selected_item in ['oled_in_tv', 'oled_box']:
                detected_objects['tv_white'] = 0
        
        return detected_objects

    def handle_oled_title_conversion_vinted(self, detected_objects, listing_title, listing_description):
        """
        Handle OLED title conversion logic (ported from Facebook)
        """
        listing_title_lower = listing_title.lower()
        listing_description_lower = listing_description.lower()
        
        if (('oled' in listing_title_lower) or ('oled' in listing_description_lower)) and \
        'not oled' not in listing_title_lower and 'not oled' not in listing_description_lower:
            
            for old, new in [('switch', 'oled'), ('switch_in_tv', 'oled_in_tv'), ('switch_box', 'oled_box')]:
                if detected_objects.get(old, 0) > 0:
                    detected_objects[old] = 0
                    detected_objects[new] = 1
        
        return detected_objects
    
    def check_vinted_listing_suitability(self, listing_info):
        """
        Check if a Vinted listing meets all suitability criteria
        FIXED: Properly extract review count from seller_reviews field
        """
        debug_function_call("check_vinted_listing_suitability")
        import re  # FIXED: Import re at function level
        
        title = listing_info.get("title", "").lower()
        description = listing_info.get("description", "").lower()
        price = listing_info.get("price", 0)
        seller_reviews = listing_info.get("seller_reviews", "No reviews yet")
        
        try:
            price_float = float(price)
        except (ValueError, TypeError):
            return "Unsuitable: Unable to parse price"
        
        # FIXED: Extract number of reviews from seller_reviews - this was the bug!
        reviews_count = 0
        if seller_reviews and seller_reviews != "No reviews yet":
            # Handle multiple formats that might come from scrape_item_details
            reviews_text = str(seller_reviews).strip()
            
            # Debug print to see what we're getting
            if print_debug:
                print(f"DEBUG: Raw seller_reviews value: '{reviews_text}'")
            
            # Try multiple extraction methods
            if reviews_text.startswith("Reviews: "):
                # Format: "Reviews: 123"
                try:
                    reviews_count = int(reviews_text.replace("Reviews: ", ""))
                except ValueError:
                    reviews_count = 0
            elif reviews_text.isdigit():
                # Format: "123" (just the number)
                reviews_count = int(reviews_text)
            else:
                # Try to extract any number from the string
                match = re.search(r'\d+', reviews_text)
                if match:
                    reviews_count = int(match.group())
                else:
                    reviews_count = 0
        
        if print_debug:# Debug print to see final extracted count
            print(f"DEBUG: Extracted reviews_count: {reviews_count} (review_min: {review_min})")
        
        checks = [
            (lambda: reviews_count < review_min,
            f"Lack of reviews (has {reviews_count}, needs {review_min}+)"),
            (lambda: any(word in title for word in vinted_title_forbidden_words),
            "Title contains forbidden words"),
            (lambda: not any(word in title for word in vinted_title_must_contain),
            "Title does not contain any required words"),
            (lambda: any(word in description for word in vinted_description_forbidden_words),
            "Description contains forbidden words"),
            (lambda: price_float < vinted_min_price or price_float > vinted_max_price,
            f"Price £{price_float} is outside the range £{vinted_min_price}-£{vinted_max_price}"),
            (lambda: len(re.findall(r'[£$]\s*\d+|\d+\s*[£$]', description)) >= 3,
            "Too many $ symbols in description"),
            (lambda: price_float in vinted_banned_prices,
            "Price in banned prices list")
        ]
        
        for check, message in checks:
            try:
                if check():
                    return f"Unsuitable: {message}"
            except (ValueError, IndexError, AttributeError, TypeError):
                continue
        
        return "Listing is suitable"

    def scrape_item_details(self, driver):
        """
        Enhanced scraper with better price extraction and seller reviews
        UPDATED: Now includes username collection AND stores price for threshold filtering
        """
        debug_function_call("scrape_item_details")
        import re  # FIXED: Import re at function level
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "p.web_ui__Text__subtitle"))
        )

        fields = {
            "title": "h1.web_ui__Text__title",
            "price": "p.web_ui__Text__subtitle",  # Main price field for extraction
            "second_price": "div.web_ui__Text__title.web_ui__Text__clickable.web_ui__Text__underline-none",
            "postage": "h3[data-testid='item-shipping-banner-price']",
            "description": "span.web_ui__Text__text.web_ui__Text__body.web_ui__Text__left.web_ui__Text__format span",
            "uploaded": "span.web_ui__Text__text.web_ui__Text__subtitle.web_ui__Text__left.web_ui__Text__bold",
            "seller_reviews": "span.web_ui__Text__text.web_ui__Text__caption.web_ui__Text__left",  # Main selector for seller reviews
            "username": "span[data-testid='profile-username']",  # NEW: Username field
        }

        data = {}
        for key, sel in fields.items():
            try:
                if key == "seller_reviews":
                    # FIXED: Better handling for seller reviews with multiple selectors
                    review_selectors = [
                        "span.web_ui__Text__text.web_ui__Text__caption.web_ui__Text__left",  # Primary selector
                        "span[class*='caption'][class*='left']",  # Broader selector
                        "div[class*='reviews'] span",  # Alternative selector
                        "*[class*='review']",  # Very broad selector as fallback
                    ]
                    
                    reviews_text = None
                    for review_sel in review_selectors:
                        try:
                            elements = driver.find_elements(By.CSS_SELECTOR, review_sel)
                            for element in elements:
                                text = element.text.strip()
                                # Look for text that contains digits (likely review count)
                                if text and (text.isdigit() or "review" in text.lower() or re.search(r'\d+', text)):
                                    reviews_text = text
                                    if print_debug:
                                        print(f"DEBUG: Found reviews using selector '{review_sel}': '{text}'")
                                    break
                            if reviews_text:
                                break
                        except Exception as e:
                            if print_debug:
                                print(f"DEBUG: Selector '{review_sel}' failed: {e}")
                            continue
                    
                    # Process the found reviews text
                    if reviews_text:
                        if reviews_text == "No reviews yet" or "no review" in reviews_text.lower():
                            data[key] = "No reviews yet"
                        elif reviews_text.isdigit():
                            # Just a number like "123"
                            data[key] = reviews_text  # Keep as string for consistency
                            if print_debug:
                                print(f"DEBUG: Set seller_reviews to: '{reviews_text}'")
                        else:
                            # Try to extract number from text like "123 reviews" or "(123)"
                            match = re.search(r'(\d+)', reviews_text)
                            if match:
                                data[key] = match.group(1)  # Just the number as string
                                if print_debug:
                                    print(f"DEBUG: Extracted number from '{reviews_text}': '{match.group(1)}'")
                            else:
                                data[key] = "No reviews yet"
                    else:
                        data[key] = "No reviews yet"
                        if print_debug:
                            print("DEBUG: No seller reviews found with any selector")
                        
                elif key == "username":
                    # NEW: Handle username extraction with careful error handling
                    try:
                        username_element = driver.find_element(By.CSS_SELECTOR, sel)
                        username_text = username_element.text.strip()
                        if username_text:
                            data[key] = username_text
                            if print_debug:
                                print(f"DEBUG: Found username: '{username_text}'")
                        else:
                            data[key] = "Username not found"
                            if print_debug:
                                print("DEBUG: Username element found but no text")
                    except NoSuchElementException:
                        # Try alternative selectors for username
                        alternative_username_selectors = [
                            "span.web_ui__Text__text.web_ui__Text__body.web_ui__Text__left.web_ui__Text__amplified.web_ui__Text__bold[data-testid='profile-username']",
                            "span[data-testid='profile-username']",
                            "*[data-testid='profile-username']",
                            "span.web_ui__Text__amplified.web_ui__Text__bold",  # Broader fallback
                        ]
                        
                        username_found = False
                        for alt_sel in alternative_username_selectors:
                            try:
                                alt_username_element = driver.find_element(By.CSS_SELECTOR, alt_sel)
                                alt_username_text = alt_username_element.text.strip()
                                if alt_username_text:
                                    data[key] = alt_username_text
                                    print(f"DEBUG: Found username with alternative selector '{alt_sel}': '{alt_username_text}'")
                                    username_found = True
                                    break
                            except NoSuchElementException:
                                continue
                        
                        if not username_found:
                            data[key] = "Username not found"
                            if print_debug:
                                print("DEBUG: Username not found with any selector")
                            
                else:
                    # Handle all other fields normally
                    data[key] = driver.find_element(By.CSS_SELECTOR, sel).text
                    
            except NoSuchElementException:
                if key == "seller_reviews":
                    data[key] = "No reviews yet"
                    if print_debug:
                        print("DEBUG: NoSuchElementException - set seller_reviews to 'No reviews yet'")
                elif key == "username":
                    data[key] = "Username not found"
                    if print_debug:
                        print("DEBUG: NoSuchElementException - set username to 'Username not found'")
                else:
                    data[key] = None

        # Keep title formatting for pygame display
        if data["title"]:
            data["title"] = data["title"][:50] + '...' if len(data["title"]) > 50 else data["title"]

        # NEW: Calculate and store the total price for threshold filtering
        second_price = self.extract_price(data.get("second_price", "0"))
        postage = self.extract_price(data.get("postage", "0"))
        total_price = second_price + postage
        
        # Store the calculated price for use in object detection
        self.current_listing_price_float = total_price
        
        # DEBUG: Print final scraped data for seller_reviews and username
        if print_debug:
            print(f"DEBUG: Final scraped seller_reviews: '{data.get('seller_reviews')}'")
            print(f"DEBUG: Final scraped username: '{data.get('username')}'")
            print(f"DEBUG: Total price calculated: £{total_price:.2f} (stored for threshold filtering)")
            
        return data

    def clear_download_folder(self):
        if os.path.exists(DOWNLOAD_ROOT):
            shutil.rmtree(DOWNLOAD_ROOT)
        os.makedirs(DOWNLOAD_ROOT, exist_ok=True)

    # FIXED: Updated process_vinted_listing function - key section that handles suitability checking

    def process_vinted_listing(self, details, detected_objects, processed_images, listing_counter, url):
        """
        Enhanced processing with comprehensive filtering and analysis - UPDATED with ULTRA-FAST bookmark functionality
        FIXED: Now passes username to bookmark_driver
        MODIFIED: Separate logic for pygame and website display - pygame shows all suitable listings with bookmark failure notices
        UPDATED: Now includes time tracking when items are added to pygame
        """
        global suitable_listings, current_listing_index, recent_listings

        # Extract username from details
        username = details.get("username", None)

        if not username or username == "Username not found":
            username = None
            print("🔖 USERNAME: Not available for this listing")

        # Extract and validate price from the main price field
        price_text = details.get("price", "0")
        listing_price = self.extract_vinted_price(price_text)
        postage = self.extract_price(details.get("postage", "0"))
        total_price = listing_price + postage

        # Get seller reviews
        seller_reviews = details.get("seller_reviews", "No reviews yet")
        if print_debug:    
            print(f"DEBUG: seller_reviews from details: '{seller_reviews}'")

        # Create basic listing info for suitability checking
        listing_info = {
            "title": details.get("title", "").lower(),
            "description": details.get("description", "").lower(),
            "price": total_price,
            "seller_reviews": seller_reviews,
            "url": url
        }

        # Check basic suitability (but don't exit early if VINTED_SHOW_ALL_LISTINGS is True)
        suitability_result = self.check_vinted_listing_suitability(listing_info)
        if print_debug:    
            print(f"DEBUG: Suitability result: '{suitability_result}'")

        # Apply console keyword detection to detected objects
        detected_console = self.detect_console_keywords_vinted(
            details.get("title", ""),
            details.get("description", "")
        )
        if detected_console:
            # Set the detected console to 1 and ensure other mutually exclusive items are 0
            mutually_exclusive_items = ['switch', 'oled', 'lite', 'switch_box', 'oled_box', 'lite_box', 'switch_in_tv', 'oled_in_tv']
            for item in mutually_exclusive_items:
                detected_objects[item] = 1 if item == detected_console else 0

        # Apply OLED title conversion
        detected_objects = self.handle_oled_title_conversion_vinted(
            detected_objects,
            details.get("title", ""),
            details.get("description", "")
        )

        # Calculate revenue with enhanced logic
        total_revenue, expected_profit, profit_percentage, display_objects = self.calculate_vinted_revenue(
            detected_objects, total_price, details.get("title", ""), details.get("description", "")
        )

        # Check profit suitability
        profit_suitability = self.check_vinted_profit_suitability(total_price, profit_percentage)

        # Game count suitability check (same as Facebook) - but don't return early if showing all
        game_classes = [
            '1_2_switch', 'animal_crossing', 'arceus_p', 'bow_z', 'bros_deluxe_m', 'crash_sand',
            'dance', 'diamond_p', 'evee', 'fifa_23', 'fifa_24', 'gta','just_dance', 'kart_m', 'kirby',
            'lets_go_p', 'links_z', 'luigis', 'mario_maker_2', 'mario_sonic', 'mario_tennis', 'minecraft',
            'minecraft_dungeons', 'minecraft_story', 'miscellanious_sonic', 'odyssey_m', 'other_mario',
            'party_m', 'rocket_league', 'scarlet_p', 'shield_p', 'shining_p', 'skywards_z', 'smash_bros',
            'snap_p', 'splatoon_2', 'splatoon_3', 'super_m_party', 'super_mario_3d', 'switch_sports',
            'sword_p', 'tears_z', 'violet_p'
        ]
        game_count = sum(detected_objects.get(game, 0) for game in game_classes)
        non_game_classes = [cls for cls in detected_objects.keys() if cls not in game_classes and detected_objects.get(cls, 0) > 0]

        # Build comprehensive suitability reason
        unsuitability_reasons = []

        # Add basic suitability issues
        if "Unsuitable" in suitability_result:
            unsuitability_reasons.append(suitability_result.replace("Unsuitable: ", ""))

        # Add game count issue
        if 1 <= game_count <= 2 and not non_game_classes:
            unsuitability_reasons.append("1-2 games with no additional non-game items")

        # Add profit suitability issue
        if not profit_suitability:
            unsuitability_reasons.append(f"Profit £{expected_profit:.2f} ({profit_percentage:.2f}%) not suitable for price range")

        # Determine final suitability
        if unsuitability_reasons:
            suitability_reason = "Unsuitable:\n---- " + "\n---- ".join(unsuitability_reasons)
            is_suitable = False
        else:
            suitability_reason = f"Suitable: Profit £{expected_profit:.2f} ({profit_percentage:.2f}%)"
            is_suitable = True

        if print_debug:    
            print(f"DEBUG: Final is_suitable: {is_suitable}, suitability_reason: '{suitability_reason}'")

        # 🔖 MODIFIED BOOKMARK FUNCTIONALITY WITH SUCCESS TRACKING
        bookmark_success = False
        should_bookmark = False
        
        if bookmark_listings and is_suitable:
            should_bookmark = True
        elif bookmark_listings and VINTED_SHOW_ALL_LISTINGS:
            should_bookmark = True
            
            if should_bookmark:
                # CHANGED: Use threaded bookmark execution
                print(f"🔖 THREADED BOOKMARK: {url}")
                
                # Extract username from details
                username = details.get("username", None)
                if not username or username == "Username not found":
                    username = None
                    print("🔖 USERNAME: Not available for this listing")
                
                # Start bookmark in separate thread - no need to wait for completion
                bookmark_success = self.bookmark_driver_threaded(url, username)
                
                # For the rest of the logic, assume bookmark will succeed
                # (the thread will handle the actual success/failure)
                if bookmark_success:
                    print("✅ Bookmark thread started successfully")
                    
                    # Start bookmark stopwatch (existing logic)
                    self.start_bookmark_stopwatch(url)

        # NEW: Generate exact UK time when creating listing info 
        from datetime import datetime
        import pytz
        
        uk_tz = pytz.timezone('Europe/London')
        append_time = datetime.now(uk_tz)
        exact_append_time = append_time.strftime("%H:%M:%S.%f")[:-3]  # Format: HH:MM:SS.mmm
        
        # Create final listing info with exact append time
        final_listing_info = {
            'title': details.get("title", "No title"),
            'description': details.get("description", "No description"),
            'join_date': exact_append_time,  # CHANGED: Use exact UK time instead of upload date
            'price': str(total_price),
            'expected_revenue': total_revenue,
            'profit': expected_profit,
            'detected_items': detected_objects, # Raw detected objects for box 1
            'processed_images': processed_images,
            'bounding_boxes': {'image_paths': [], 'detected_objects': detected_objects},
            'url': url,
            'suitability': suitability_reason,
            'seller_reviews': seller_reviews
        }

        # SEPARATE logic for pygame and website
        should_add_to_website = False
        should_add_to_pygame = False
        should_send_notification = False

        # Website logic (current behavior - only successful bookmarks when bookmark_listings=True and VINTED_SHOW_ALL_LISTINGS=False)
        if bookmark_listings and not VINTED_SHOW_ALL_LISTINGS:
            # When bookmark_listings is ON and VINTED_SHOW_ALL_LISTINGS is OFF:
            # Only add/notify if bookmark was successful
            if bookmark_success:
                should_add_to_website = True
                should_send_notification = True
                print("✅ Adding to website because bookmark was successful")
            else:
                print("❌ Not adding to website because bookmark was not successful")
        else:
            # Original logic for other combinations
            if is_suitable or VINTED_SHOW_ALL_LISTINGS:
                should_add_to_website = True
                should_send_notification = True

        # NEW: Pygame logic (always show suitable listings + bookmark failure info)
        if VINTED_SHOW_ALL_LISTINGS:
            should_add_to_pygame = True
        elif is_suitable:  # Show all suitable listings regardless of bookmark success
            should_add_to_pygame = True

        # Modify suitability_reason for pygame if bookmark failed
        pygame_suitability_reason = suitability_reason
        if should_add_to_pygame and bookmark_listings and is_suitable and not bookmark_success:
            pygame_suitability_reason = suitability_reason + "\n⚠️ BOOKMARK FAILED"
        
        if is_suitable and should_send_fail_bookmark_notification and not should_add_to_website:
            notification_title = f"Listing Failed Bookmark: £{total_price:.2f}"
            notification_message = (
                f"Title: {details.get('title', 'No title')}\n"
                f"Price: £{total_price:.2f}\n"
                f"Expected Profit: £{expected_profit:.2f}\n"
                f"Profit %: {profit_percentage:.2f}%\n"
            )
            
            # Use the Pushover tokens exactly as Facebook does
            if send_notification:
                self.send_pushover_notification(
                    notification_title,
                    notification_message,
                    'aks3to8guqjye193w7ajnydk9jaxh5',
                    'ucwc6fi1mzd3gq2ym7jiwg3ggzv1pc'
                )

        # Add to website (existing logic)
        if should_add_to_website:
            # Send Pushover notification
            if should_send_notification:
                notification_title = f"New Vinted Listing: £{total_price:.2f}"
                notification_message = (
                    f"Title: {details.get('title', 'No title')}\n"
                    f"Price: £{total_price:.2f}\n"
                    f"Expected Profit: £{expected_profit:.2f}\n"
                    f"Profit %: {profit_percentage:.2f}%\n"
                )
                
                # Use the Pushover tokens exactly as Facebook does
                if send_notification:
                    self.send_pushover_notification(
                        notification_title,
                        notification_message,
                        'aks3to8guqjye193w7ajnydk9jaxh5',
                        'ucwc6fi1mzd3gq2ym7jiwg3ggzv1pc'
                    )

            # Add to recent_listings for website navigation
            recent_listings['listings'].append(final_listing_info)
            # Always set to the last (most recent) listing for website display
            recent_listings['current_index'] = len(recent_listings['listings']) - 1

        # Add to pygame (NEW separate logic)
        if should_add_to_pygame:
            # Create pygame-specific listing info with modified suitability
            pygame_listing_info = final_listing_info.copy()
            pygame_listing_info['suitability'] = pygame_suitability_reason
            
            suitable_listings.append(pygame_listing_info)
            current_listing_index = len(suitable_listings) - 1
            
            # UPDATED: Print exact append time when adding to pygame
            print(f"⏰ APPENDED TO PYGAME: {exact_append_time} UK time")
            self.update_listing_details(**pygame_listing_info)

            if is_suitable and not bookmark_success and bookmark_listings:
                print(f"✅ Added suitable listing to pygame with bookmark failure notice: £{total_price:.2f}")
            elif is_suitable:
                print(f"✅ Added suitable listing to pygame: £{total_price:.2f} -> £{expected_profit:.2f} profit ({profit_percentage:.2f}%)")
            else:
                print(f"➕ Added unsuitable listing to pygame (SHOW_ALL mode): £{total_price:.2f}")

        if not should_add_to_pygame:
            print(f"❌ Listing not added to pygame: {suitability_reason}")


    def check_vinted_profit_suitability(self, listing_price, profit_percentage):
        if 10 <= listing_price < 16:
            return 100 <= profit_percentage <= 600 #50
        elif 16 <= listing_price < 25:
            return 65 <= profit_percentage <= 400 #50
        elif 25 <= listing_price < 50:
            return 37.5 <= profit_percentage <= 550 #35
        elif 50 <= listing_price < 100:
            return 35 <= profit_percentage <= 500 #32.5
        elif listing_price >= 100:
            return 30 <= profit_percentage <= 450 # 30
        else:
            return False
            
    def calculate_vinted_revenue(self, detected_objects, listing_price, title, description=""):
        """
        Enhanced revenue calculation with all Facebook logic
        """
        debug_function_call("calculate_vinted_revenue")
        import re  # FIXED: Import re at function level
        
        # List of game-related classes
        game_classes = [
            '1_2_switch', 'animal_crossing', 'arceus_p', 'bow_z', 'bros_deluxe_m', 'crash_sand',
            'dance', 'diamond_p', 'evee', 'fifa_23', 'fifa_24', 'gta','just_dance', 'kart_m', 'kirby',
            'lets_go_p', 'links_z', 'luigis', 'mario_maker_2', 'mario_sonic', 'mario_tennis', 'minecraft',
            'minecraft_dungeons', 'minecraft_story', 'miscellanious_sonic', 'odyssey_m', 'other_mario',
            'party_m', 'rocket_league', 'scarlet_p', 'shield_p', 'shining_p', 'skywards_z', 'smash_bros',
            'snap_p', 'splatoon_2', 'splatoon_3', 'super_m_party', 'super_mario_3d', 'switch_sports',
            'sword_p', 'tears_z', 'violet_p'
        ]

        # Get all prices
        all_prices = self.fetch_all_prices()

        # Count detected games
        detected_games_count = sum(detected_objects.get(game, 0) for game in game_classes)

        # Detect anonymous games from title and description
        text_games_count = self.detect_anonymous_games_vinted(title, description)

        # Calculate miscellaneous games
        misc_games_count = max(0, text_games_count - detected_games_count)
        misc_games_revenue = misc_games_count * 5 # Using same price as Facebook

        # Handle box adjustments (same as Facebook)
        adjustments = {
            'oled_box': ['switch', 'comfort_h', 'tv_white'],
            'switch_box': ['switch', 'comfort_h', 'tv_black'],
            'lite_box': ['lite']
        }

        for box, items in adjustments.items():
            box_count = detected_objects.get(box, 0)
            for item in items:
                detected_objects[item] = max(0, detected_objects.get(item, 0) - box_count)

        # Remove switch_screen if present
        detected_objects.pop('switch_screen', None)

        # Detect SD card and add revenue
        total_revenue = misc_games_revenue

        # Calculate revenue from detected objects
        for item, count in detected_objects.items():
            if isinstance(count, str):
                count_match = re.match(r'(\d+)', count)
                count = int(count_match.group(1)) if count_match else 0

            if count > 0 and item in all_prices:
                item_price = all_prices[item]
                if item == 'controller' and 'pro' in title.lower():
                    item_price += 7.50
                
                item_revenue = item_price * count
                total_revenue += item_revenue

        expected_profit = total_revenue - listing_price
        profit_percentage = (expected_profit / listing_price) * 100 if listing_price > 0 else 0

        print(f"Listing Price: £{listing_price:.2f}")
        print(f"Total Expected Revenue: £{total_revenue:.2f}")
        print(f"Expected Profit/Loss: £{expected_profit:.2f} ({profit_percentage:.2f}%)")

        # CRITICAL FIX: Filter out zero-count items for display (matching Facebook behavior)
        display_objects = {k: v for k, v in detected_objects.items() if v > 0}

        # Add miscellaneous games to display if present
        if misc_games_count > 0:
            display_objects['misc_games'] = misc_games_count

        return total_revenue, expected_profit, profit_percentage, display_objects

    def perform_detection_on_listing_images(self, model, listing_dir):
        """
        Enhanced object detection with all Facebook exceptions and logic
        PLUS Vinted-specific post-scan game deduplication
        NEW: Price threshold filtering for Nintendo Switch related items
        """
        if not os.path.isdir(listing_dir):
            return {}, []

        detected_objects = {class_name: [] for class_name in CLASS_NAMES}
        processed_images = []
        confidences = {item: 0 for item in ['switch', 'oled', 'lite', 'switch_box', 'oled_box', 'lite_box', 'switch_in_tv', 'oled_in_tv']}

        image_files = [f for f in os.listdir(listing_dir) if f.endswith('.png')]
        if not image_files:
            return {class_name: 0 for class_name in CLASS_NAMES}, processed_images

        for image_file in image_files:
            image_path = os.path.join(listing_dir, image_file)
            try:
                img = cv2.imread(image_path)
                if img is None:
                    continue

                # Track detections for this image
                image_detections = {class_name: 0 for class_name in CLASS_NAMES}
                results = model(img, verbose=False)
                
                for result in results:
                    for box in result.boxes.cpu().numpy():
                        class_id = int(box.cls[0])
                        confidence = box.conf[0]
                        
                        if class_id < len(CLASS_NAMES):
                            class_name = CLASS_NAMES[class_id]
                            min_confidence = HIGHER_CONFIDENCE_ITEMS.get(class_name, GENERAL_CONFIDENCE_MIN)
                            
                            if confidence >= min_confidence:
                                if class_name in ['switch', 'oled', 'lite', 'switch_box', 'oled_box', 'lite_box', 'switch_in_tv', 'oled_in_tv']:
                                    confidences[class_name] = max(confidences[class_name], confidence)
                                else:
                                    image_detections[class_name] += 1
                                
                                # Draw bounding box
                                x1, y1, x2, y2 = map(int, box.xyxy[0])
                                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                cv2.putText(img, f"{class_name} ({confidence:.2f})", (x1, y1 - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.625, (0, 255, 0), 2)

                # Update overall detected objects with max from this image
                for class_name, count in image_detections.items():
                    detected_objects[class_name].append(count)

                # Convert to PIL Image for pygame compatibility
                processed_images.append(Image.fromarray(cv2.cvtColor(
                    cv2.copyMakeBorder(img, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=[0, 0, 0]),
                    cv2.COLOR_BGR2RGB)))

            except Exception as e:
                print(f"Error processing image {image_path}: {str(e)}")
                continue

        # Convert lists to max values
        final_detected_objects = {class_name: max(counts) if counts else 0 for class_name, counts in detected_objects.items()}
        
        # Handle mutually exclusive items
        final_detected_objects = self.handle_mutually_exclusive_items_vinted(final_detected_objects, confidences)
        
        # VINTED-SPECIFIC POST-SCAN GAME DEDUPLICATION
        # Define game classes that should be capped at 1 per listing
        vinted_game_classes = [
            '1_2_switch', 'animal_crossing', 'arceus_p', 'bow_z', 'bros_deluxe_m', 'crash_sand',
            'dance', 'diamond_p', 'evee', 'fifa_23', 'fifa_24', 'gta', 'just_dance', 'kart_m', 'kirby',
            'lets_go_p', 'links_z', 'luigis', 'mario_maker_2', 'mario_sonic', 'mario_tennis', 'minecraft',
            'minecraft_dungeons', 'minecraft_story', 'miscellanious_sonic', 'odyssey_m', 'other_mario',
            'party_m', 'rocket_league', 'scarlet_p', 'shield_p', 'shining_p', 'skywards_z', 'smash_bros',
            'snap_p', 'splatoon_2', 'splatoon_3', 'super_m_party', 'super_mario_3d', 'switch_sports',
            'sword_p', 'tears_z', 'violet_p'
        ]
        
        # Cap each game type to maximum 1 per listing for Vinted
        games_before_cap = {}
        for game_class in vinted_game_classes:
            if final_detected_objects.get(game_class, 0) > 1:
                games_before_cap[game_class] = final_detected_objects[game_class]
                final_detected_objects[game_class] = 1
        
        # Log the capping if any games were capped
        if games_before_cap:
            print("🎮 VINTED GAME DEDUPLICATION APPLIED:")
            for game, original_count in games_before_cap.items():
                print(f"  • {game}: {original_count} → 1")
        
        # NEW: PRICE THRESHOLD FILTERING FOR NINTENDO SWITCH ITEMS
        try:
            # Get the current listing price stored during scraping
            listing_price = getattr(self, 'current_listing_price_float', 0.0)
            
            # If the listing price is below the threshold, remove Nintendo Switch detections
            if listing_price > 0 and listing_price < PRICE_THRESHOLD:
                filtered_classes = []
                for switch_class in NINTENDO_SWITCH_CLASSES:
                    if final_detected_objects.get(switch_class, 0) > 0:
                        filtered_classes.append(switch_class)
                        final_detected_objects[switch_class] = 0
                
                if filtered_classes:
                    print(f"🚫 PRICE FILTER: Removed Nintendo Switch detections due to low price (£{listing_price:.2f} < £{PRICE_THRESHOLD:.2f})")
                    print(f"    Filtered classes: {', '.join(filtered_classes)}")
            elif listing_price >= PRICE_THRESHOLD:
                # Optional: Log when price threshold allows detection
                detected_switch_classes = [cls for cls in NINTENDO_SWITCH_CLASSES if final_detected_objects.get(cls, 0) > 0]
                if detected_switch_classes:
                    print(f"✅ PRICE FILTER: Nintendo Switch detections allowed (£{listing_price:.2f} >= £{PRICE_THRESHOLD:.2f})")
        
        except Exception as price_filter_error:
            print(f"⚠️ Warning: Price filtering failed: {price_filter_error}")
            # Continue without price filtering if there's an error
        
        return final_detected_objects, processed_images


    def download_images_for_listing(self, driver, listing_dir):
        """FIXED: Download ALL listing images without limits and prevent duplicates"""
        import concurrent.futures
        import requests
        from PIL import Image
        from io import BytesIO
        import os
        import hashlib
        
        # Wait for the page to fully load
        try:
            WebDriverWait(driver, 10).until(  # Increased timeout for better reliability
                EC.presence_of_element_located((By.TAG_NAME, "img"))
            )
        except TimeoutException:
            print("  ▶ Timeout waiting for images to load")
            return []
        
        # Try multiple selectors in order of preference - focusing on product images only
        img_selectors = [
            # Target product images specifically (avoid profile pictures)
            "img.web_ui__Image__content[data-testid^='item-photo-']",
            "img[data-testid^='item-photo-']",
            # Target images within containers that suggest product photos
            "div.web_ui__Image__cover img.web_ui__Image__content",
            "div.web_ui__Image__scaled img.web_ui__Image__content", 
            "div.web_ui__Image__rounded img.web_ui__Image__content",
            # Broader selectors but still avoiding profile images
            "div.feed-grid img",
            "div[class*='photo'] img",
        ]
        
        imgs = []
        for selector in img_selectors:
            imgs = driver.find_elements(By.CSS_SELECTOR, selector)
            if imgs:
                if print_images_backend_info:
                    print(f"  ▶ Found {len(imgs)} images using selector: {selector}")
                break
        
        if not imgs:
            print("  ▶ No images found with any selector")
            return []
        
        # FIXED: Remove the [:8] limit - process ALL images found
        valid_urls = []
        seen_urls = set()  # Track URLs to prevent duplicates
        
        if print_images_backend_info:
            print(f"  ▶ Processing {len(imgs)} images (NO LIMIT)")
        
        for img in imgs:  # REMOVED [:8] limit here
            src = img.get_attribute("src")
            parent_classes = ""
            
            # Get parent element classes to check for profile picture indicators
            try:
                parent = img.find_element(By.XPATH, "..")
                parent_classes = parent.get_attribute("class") or ""
            except:
                pass
            
            # Check if this is a valid product image
            if src and src.startswith('http'):
                # FIXED: Better duplicate detection using URL normalization
                # Remove query parameters and fragments for duplicate detection
                normalized_url = src.split('?')[0].split('#')[0]
                
                if normalized_url in seen_urls:
                    if print_images_backend_info:
                        print(f"    ⏭️  Skipping duplicate URL: {normalized_url[:50]}...")
                    continue
                
                seen_urls.add(normalized_url)
                
                # Exclude profile pictures and small icons based on URL patterns
                if (
                    # Skip small profile pictures (50x50, 75x75, etc.)
                    '/50x50/' in src or 
                    '/75x75/' in src or 
                    '/100x100/' in src or
                    # Skip if parent has circle class (usually profile pics)
                    'circle' in parent_classes.lower() or
                    # Skip SVG icons
                    src.endswith('.svg') or
                    # Skip very obviously small images by checking dimensions in URL
                    any(size in src for size in ['/32x32/', '/64x64/', '/128x128/'])
                ):
                    print(f"    ⏭️  Skipping filtered image: {src[:50]}...")
                    continue
                
                # Only include images that look like product photos
                if (
                    # Vinted product images typically have f800, f1200, etc.
                    '/f800/' in src or 
                    '/f1200/' in src or 
                    '/f600/' in src or
                    # Or contain vinted/cloudinary and are likely product images
                    (('vinted' in src.lower() or 'cloudinary' in src.lower() or 'amazonaws' in src.lower()) and
                    # And don't have small size indicators
                    not any(small_size in src for small_size in ['/50x', '/75x', '/100x', '/thumb']))
                ):
                    valid_urls.append(src)
                    if print_images_backend_info:
                        print(f"    ✅ Added valid image URL: {src[:50]}...")

        if not valid_urls:
            print(f"  ▶ No valid product images found after filtering from {len(imgs)} total images")
            return []

        if print_images_backend_info:
            print(f"  ▶ Final count: {len(valid_urls)} unique, valid product images")
        
        os.makedirs(listing_dir, exist_ok=True)
        
        # FIXED: Enhanced duplicate detection using content hashes
        def download_single_image(args):
            """Download a single image with enhanced duplicate detection"""
            url, index = args
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Cache-Control': 'no-cache',
                'Referer': driver.current_url
            }
            
            try:
                resp = requests.get(url, timeout=10, headers=headers)
                resp.raise_for_status()
                
                # FIXED: Use content hash to detect identical images with different URLs
                content_hash = hashlib.md5(resp.content).hexdigest()
                
                # Check if we've already downloaded this exact image content
                hash_file = os.path.join(listing_dir, f".hash_{content_hash}")
                if os.path.exists(hash_file):
                    if print_images_backend_info:
                        print(f"    ⏭️  Skipping duplicate content (hash: {content_hash[:8]}...)")
                    return None
                
                img = Image.open(BytesIO(resp.content))
                
                # Skip very small images (likely icons or profile pics that got through)
                if img.width < 200 or img.height < 200:
                    print(f"    ⏭️  Skipping small image: {img.width}x{img.height}")
                    return None
                
                # Resize image for YOLO detection optimization
                MAX_SIZE = (1000, 1000)  # Slightly larger for better detection
                if img.width > MAX_SIZE[0] or img.height > MAX_SIZE[1]:
                    img.thumbnail(MAX_SIZE, Image.LANCZOS)
                    print(f"    📏 Resized image to: {img.width}x{img.height}")
                
                # Convert to RGB if needed
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Save the image
                save_path = os.path.join(listing_dir, f"{index}.png")
                img.save(save_path, format="PNG", optimize=True)
                
                # Create hash marker file to prevent future duplicates
                with open(hash_file, 'w') as f:
                    f.write(f"Downloaded from: {url}")
                if print_images_backend_info:
                    print(f"    ✅ Downloaded unique image {index}: {img.width}x{img.height} (hash: {content_hash[:8]}...)")
                return save_path
                
            except Exception as e:
                print(f"    ❌ Failed to download image from {url[:50]}...: {str(e)}")
                return None
        if print_images_backend_info:
            print(f"  ▶ Downloading {len(valid_urls)} product images concurrently...")
        
        # FIXED: Dynamic batch size based on actual image count
        batch_size = len(valid_urls)  # Each "batch" equals the number of listing images
        max_workers = min(6, batch_size)  # Use appropriate number of workers
        
        if print_images_backend_info:
            print(f"  ▶ Batch size set to: {batch_size} (= number of listing images)")
            print(f"  ▶ Using {max_workers} concurrent workers")
        
        downloaded_paths = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Prepare arguments for concurrent download
            download_args = [(url, i+1) for i, url in enumerate(valid_urls)]
            
            # Submit all download jobs
            future_to_url = {executor.submit(download_single_image, args): args[0] for args in download_args}
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_url):
                result = future.result()
                if result:  # Only add successful downloads
                    downloaded_paths.append(result)

        print(f"  ▶ Successfully downloaded {len(downloaded_paths)} unique images (from {len(valid_urls)} URLs)")
        
        # Clean up hash files (optional - you might want to keep them for faster future runs)
        # Uncomment the next 6 lines if you want to clean up hash files after each listing
        # try:
        #     for file in os.listdir(listing_dir):
        #         if file.startswith('.hash_'):
        #             os.remove(os.path.join(listing_dir, file))
        # except:
        #     pass
        
        return downloaded_paths


    def download_and_process_images_vinted(self, image_urls):
        """FIXED: Process images without arbitrary limits and with better deduplication"""
        processed_images = []
        seen_hashes = set()  # Track content hashes to prevent duplicates
        
        print(f"🖼️  Processing {len(image_urls)} image URLs (NO LIMIT)")
        
        for i, url in enumerate(image_urls):  # REMOVED [:8] limit here
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    # FIXED: Use content hash for duplicate detection
                    content_hash = hashlib.md5(response.content).hexdigest()
                    
                    if content_hash in seen_hashes:
                        if print_images_backend_info:
                            print(f"🖼️  Skipping duplicate image {i+1} (hash: {content_hash[:8]}...)")
                        continue
                    
                    seen_hashes.add(content_hash)
                    
                    img = Image.open(io.BytesIO(response.content))
                    
                    # Skip very small images
                    if img.width < 200 or img.height < 200:
                        print(f"🖼️  Skipping small image {i+1}: {img.width}x{img.height}")
                        continue
                    
                    img = img.convert("RGB")
                    
                    # FIXED: Create proper copy to prevent memory issues
                    img_copy = img.copy()
                    processed_images.append(img_copy)
                    img.close()  # Close original to free memory
                    
                    print(f"🖼️  Processed unique image {i+1}: {img_copy.width}x{img_copy.height}")
                    
                else:
                    print(f"🖼️  Failed to download image {i+1}. Status code: {response.status_code}")
            except Exception as e:
                print(f"🖼️  Error processing image {i+1}: {str(e)}")
        
        print(f"🖼️  Final result: {len(processed_images)} unique processed images")
        return processed_images


    
    def extract_vinted_listing_id(self, url):
        """
        Extract listing ID from Vinted URL
        Example: https://www.vinted.co.uk/items/6862154542-sonic-forces?referrer=catalog
        Returns: "6862154542"
        """
        debug_function_call("extract_vinted_listing_id")
        import re  # FIXED: Import re at function level
        
        if not url:
            return None
        
        # Match pattern: /items/[numbers]-
        match = re.search(r'/items/(\d+)-', url)
        if match:
            return match.group(1)
        
        # Fallback: match any sequence of digits after /items/
        match = re.search(r'/items/(\d+)', url)
        if match:
            return match.group(1)
        
        return None

    def load_scanned_vinted_ids(self):
        """Load previously scanned Vinted listing IDs from file"""
        try:
            if os.path.exists(VINTED_SCANNED_IDS_FILE):
                with open(VINTED_SCANNED_IDS_FILE, 'r') as f:
                    return set(line.strip() for line in f if line.strip())
            return set()
        except Exception as e:
            print(f"Error loading scanned IDs: {e}")
            return set()

    def save_vinted_listing_id(self, listing_id):
        """Save a Vinted listing ID to the scanned file"""
        if not listing_id:
            return
        
        try:
            with open(VINTED_SCANNED_IDS_FILE, 'a') as f:
                f.write(f"{listing_id}\n")
        except Exception as e:
            print(f"Error saving listing ID {listing_id}: {e}")

    def is_vinted_listing_already_scanned(self, url, scanned_ids):
        """Check if a Vinted listing has already been scanned"""
        listing_id = self.extract_vinted_listing_id(url)
        if not listing_id:
            return False
        return listing_id in scanned_ids

    def refresh_vinted_page_and_wait(self, driver, is_first_refresh=True):
        """
        Refresh the Vinted page and wait appropriate time
        """
        print("🔄 Refreshing Vinted page...")
        
        # Navigate back to first page
        params = {
            "search_text": SEARCH_QUERY,
            "price_from": PRICE_FROM,
            "price_to": PRICE_TO,
            "currency": CURRENCY,
            "order": ORDER,
        }
        driver.get(f"{BASE_URL}?{urlencode(params)}")
        
        # Wait for page to load
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.feed-grid"))
            )
            print("✅ Page refreshed and loaded successfully")
        except TimeoutException:
            print("⚠️ Timeout waiting for page to reload")
        
        # Wait for new listings (except first refresh)
        if not is_first_refresh:
            print(f"⏳ Waiting {wait_after_max_reached_vinted} seconds for new listings...")
            time.sleep(wait_after_max_reached_vinted)
        
        return True

    def search_vinted_with_refresh(self, driver, search_query):
        """
        Enhanced search_vinted method with refresh and rescan functionality
        UPDATED: Now restarts the main driver every 250 cycles to prevent freezing
        """
        global suitable_listings, current_listing_index
        
        # CLEAR THE VINTED SCANNED IDS FILE AT THE BEGINNING OF EACH RUN
        try:
            with open(VINTED_SCANNED_IDS_FILE, 'w') as f:
                pass  # This creates an empty file, clearing any existing content
            print(f"✅ Cleared {VINTED_SCANNED_IDS_FILE} at the start of the run")
        except Exception as e:
            print(f"⚠️ Warning: Could not clear {VINTED_SCANNED_IDS_FILE}: {e}")
        
        # Clear previous results
        suitable_listings.clear()
        current_listing_index = 0
        
        # Ensure root download folder exists
        os.makedirs(DOWNLOAD_ROOT, exist_ok=True)

        # Load YOLO Model Once
        print("🧠 Loading object detection model...")
        if not os.path.exists(MODEL_WEIGHTS):
            print(f"❌ Critical Error: Model weights not found at '{MODEL_WEIGHTS}'. Detection will be skipped.")
        else:
            try:
                print("✅ Model loaded successfully.")
            except Exception as e:
                print(f"❌ Critical Error: Could not load YOLO model. Detection will be skipped. Reason: {e}")
        
        print(f"CUDA available: {torch.cuda.is_available()}")
        print(f"GPU name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'No GPU'}")

        # Load model with explicit GPU usage
        if torch.cuda.is_available():
            model = YOLO(MODEL_WEIGHTS).cuda()
            print("✅ YOLO model loaded on GPU")
        else:
            model = YOLO(MODEL_WEIGHTS).cpu()
            print("⚠️ YOLO model loaded on CPU (no CUDA available)")

        # Store original driver reference
        current_driver = driver
        
        # Load previously scanned listing IDs
        scanned_ids = self.load_scanned_vinted_ids()
        print(f"📚 Loaded {len(scanned_ids)} previously scanned listing IDs")

        page = 1
        overall_listing_counter = 0
        refresh_cycle = 1
        is_first_refresh = True
        
        # NEW: Driver restart tracking
        DRIVER_RESTART_INTERVAL = 100
        cycles_since_restart = 0

        # Main scanning loop with refresh functionality AND driver restart
        while True:
            print(f"\n{'='*60}")
            print(f"🔍 STARTING REFRESH CYCLE {refresh_cycle}")
            print(f"🔄 Cycles since last driver restart: {cycles_since_restart}")
            print(f"{'='*60}")
            
            # NEW: Check if we need to restart the driver
            if cycles_since_restart >= DRIVER_RESTART_INTERVAL:
                print(f"\n🔄 DRIVER RESTART: Reached {DRIVER_RESTART_INTERVAL} cycles")
                print("🔄 RESTARTING: Main scraping driver to prevent freezing...")
                
                try:
                    # Close current driver safely
                    print("🔄 CLOSING: Current driver...")
                    current_driver.quit()
                    time.sleep(2)  # Give time for cleanup
                    
                    # Create new driver
                    print("🔄 CREATING: New driver...")
                    current_driver = self.setup_driver()
                    
                    if current_driver is None:
                        print("❌ CRITICAL: Failed to create new driver after restart")
                        break
                    
                    print("✅ DRIVER RESTART: Successfully restarted main driver")
                    cycles_since_restart = 0  # Reset counter
                    
                    # Re-navigate to search page after restart
                    params = {
                        "search_text": search_query,
                        "price_from": PRICE_FROM,
                        "price_to": PRICE_TO,
                        "currency": CURRENCY,
                        "order": ORDER,
                    }
                    current_driver.get(f"{BASE_URL}?{urlencode(params)}")
                    
                    # Wait for page to load after restart
                    try:
                        WebDriverWait(current_driver, 20).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "div.feed-grid"))
                        )
                        print("✅ RESTART: Page loaded successfully after driver restart")
                    except TimeoutException:
                        print("⚠️ RESTART: Timeout waiting for page after driver restart")
                    
                except Exception as restart_error:
                    print(f"❌ RESTART ERROR: Failed to restart driver: {restart_error}")
                    print("💥 CRITICAL: Cannot continue without working driver")
                    break
            
            cycle_listing_counter = 0  # Listings processed in this cycle
            found_already_scanned = False
            
            # Reset to first page for each cycle
            page = 1
            
            while True:  # Page loop
                try:
                    WebDriverWait(current_driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.feed-grid"))
                    )
                except TimeoutException:
                    print("⚠️ Timeout waiting for page to load - moving to next cycle")
                    break

                # Get listing URLs from current page
                els = current_driver.find_elements(By.CSS_SELECTOR, "a.new-item-box__overlay")
                urls = [e.get_attribute("href") for e in els if e.get_attribute("href")]
                
                if not urls:
                    print(f"📄 No listings found on page {page} - moving to next cycle")
                    break

                print(f"📄 Processing page {page} with {len(urls)} listings")

                for idx, url in enumerate(urls, start=1):
                    cycle_listing_counter += 1
                    
                    print(f"[Cycle {refresh_cycle} · Page {page} · Item {idx}/{len(urls)}] #{overall_listing_counter}")
                    
                    # Extract listing ID and check if already scanned
                    listing_id = self.extract_vinted_listing_id(url)
                    
                    if REFRESH_AND_RESCAN and listing_id:
                        if listing_id in scanned_ids:
                            print(f"🔁 DUPLICATE DETECTED: Listing ID {listing_id} already scanned")
                            print(f"🔄 Initiating refresh and rescan process...")
                            found_already_scanned = True
                            break
                    
                    # Check if we've hit the maximum listings for this cycle
                    if REFRESH_AND_RESCAN and cycle_listing_counter > MAX_LISTINGS_VINTED_TO_SCAN:
                        print(f"📊 Reached MAX_LISTINGS_VINTED_TO_SCAN ({MAX_LISTINGS_VINTED_TO_SCAN})")
                        print(f"🔄 Initiating refresh cycle...")
                        break

                    overall_listing_counter += 1


                    # Process the listing (using current_driver instead of driver)
                    current_driver.execute_script("window.open();")
                    current_driver.switch_to.window(current_driver.window_handles[-1])
                    current_driver.get(url)

                    try:
                        listing_start_time = time.time()
                        details = self.scrape_item_details(current_driver)
                        second_price = self.extract_price(details["second_price"])
                        postage = self.extract_price(details["postage"])
                        total_price = second_price + postage

                        print(f"  Link:         {url}")
                        print(f"  Title:        {details['title']}")
                        print(f"  Username:     {details.get('username', 'Username not found')}")
                        print(f"  Price:        {details['price']}")
                        print(f"  Second price: {details['second_price']} ({second_price:.2f})")
                        print(f"  Postage:      {details['postage']} ({postage:.2f})")
                        print(f"  Total price:  £{total_price:.2f}")
                        print(f"  Uploaded:     {details['uploaded']}")

                        # Download images for the current listing
                        listing_dir = os.path.join(DOWNLOAD_ROOT, f"listing {overall_listing_counter}")
                        image_paths = self.download_images_for_listing(current_driver, listing_dir)

                        # Perform object detection and get processed images
                        detected_objects = {}
                        processed_images = []
                        if model and image_paths:
                            detected_objects, processed_images = self.perform_detection_on_listing_images(model, listing_dir)
                            
                            # Print detected objects
                            detected_classes = [cls for cls, count in detected_objects.items() if count > 0]
                            if detected_classes:
                                for cls in sorted(detected_classes):
                                    print(f"  • {cls}: {detected_objects[cls]}")

                        # Process listing for pygame display
                        self.process_vinted_listing(details, detected_objects, processed_images, overall_listing_counter, url)

                        # Mark this listing as scanned
                        if listing_id:
                            scanned_ids.add(listing_id)
                            self.save_vinted_listing_id(listing_id)
                            print(f"✅ Saved listing ID: {listing_id}")

                        print("-" * 40)
                        self.cleanup_processed_images(processed_images)
                        listing_end_time = time.time()
                        elapsed_time = listing_end_time - listing_start_time
                        print(f"⏱️ Listing {overall_listing_counter} processing completed in {elapsed_time:.2f} seconds")

                        
                    except Exception as e:
                        print(f"  ❌ ERROR scraping listing: {e}")
                        # Still mark as scanned even if there was an error
                        if listing_id:
                            scanned_ids.add(listing_id)
                            self.save_vinted_listing_id(listing_id)

                    finally:
                        current_driver.close()
                        current_driver.switch_to.window(current_driver.window_handles[0])  # Use index 0 instead of main

                # Check if we need to break out of page loop
                if found_already_scanned or (REFRESH_AND_RESCAN and cycle_listing_counter > MAX_LISTINGS_VINTED_TO_SCAN):
                    break

                # Try to go to next page
                try:
                    nxt = current_driver.find_element(By.CSS_SELECTOR, "a[data-testid='pagination-arrow-right']")
                    current_driver.execute_script("arguments[0].click();", nxt)
                    page += 1
                    time.sleep(2)
                except NoSuchElementException:
                    print("📄 No more pages available - moving to next cycle")
                    break

            # End of page loop - decide whether to continue or refresh
            if not REFRESH_AND_RESCAN:
                print("🏁 REFRESH_AND_RESCAN disabled - ending scan")
                break
            
            if found_already_scanned:
                print(f"🔁 Found already scanned listing - refreshing immediately")
                self.refresh_vinted_page_and_wait(current_driver, is_first_refresh)
            elif cycle_listing_counter > MAX_LISTINGS_VINTED_TO_SCAN:
                print(f"📊 Reached maximum listings ({MAX_LISTINGS_VINTED_TO_SCAN}) - refreshing")
                self.refresh_vinted_page_and_wait(current_driver, is_first_refresh)
            else:
                print("📄 No more pages and no max reached - refreshing for new listings")
                self.refresh_vinted_page_and_wait(current_driver, is_first_refresh)

            refresh_cycle += 1
            cycles_since_restart += 1  # NEW: Increment counter after each cycle
            is_first_refresh = False

    def start_cloudflare_tunnel(self, port=5000):
        """
        Starts a Cloudflare Tunnel using the cloudflared binary.
        Adjust the cloudflared_path if your executable is in a different location.
        """
        # Path to the cloudflared executable
        #pc
        cloudflared_path = r"C:\Users\ZacKnowsHow\Downloads\cloudflared.exe"
        #laptop
        #cloudflared_path = r"C:\Users\zacha\Downloads\cloudflared.exe"
        
        # Start the tunnel with the desired command-line arguments
        process = subprocess.Popen(
            [cloudflared_path, "tunnel", "--url", f"http://localhost:{port}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Function to read and print cloudflared output asynchronously
        def read_output(proc):
            for line in proc.stdout:
                print("[cloudflared]", line.strip())
        
        # Start a thread to print cloudflared output so you can see the public URL and any errors
        threading.Thread(target=read_output, args=(process,), daemon=True).start()
        
        # Wait a few seconds for the tunnel to establish (adjust if needed).
        time.sleep(5)
        return process

    def run_flask_app(self):
        try:
            print("Starting Flask app for https://fk43b0p45crc03r.xyz/")
            
            # Run Flask locally - your domain should be configured to tunnel to this
            app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
            
        except Exception as e:
            print(f"Error starting Flask app: {e}")
            import traceback
            traceback.print_exc()

    def is_monitoring_active(self):
        """Check if any monitoring threads are still active"""
        # Check if current bookmark driver exists (indicates monitoring might be active)
        if hasattr(self, 'current_bookmark_driver') and self.current_bookmark_driver is not None:
            try:
                # Try to access the driver - if it fails, monitoring is done
                self.current_bookmark_driver.current_url
                return True
            except:
                return False
        return False

    def _execute_bookmark_sequences_with_monitoring(self, current_driver, listing_url, username, step_log):
        """Execute bookmark sequences with Purchase unsuccessful monitoring"""
        actual_url = step_log['actual_url']
        bookmark_start_time = time.time()
        self._log_step(step_log, "function_start", True)
        
        # Create new tab and navigate
        if not self._create_tab_and_navigate(current_driver, actual_url, step_log):
            return False
        
        # Execute first buy sequence (critical sequence)
        first_sequence_success = self._execute_first_buy_sequence(current_driver, step_log)
        
        if not first_sequence_success:
            return False
        
        # Execute second sequence with monitoring (MODIFIED PART)
        return self._execute_second_sequence_with_monitoring(current_driver, actual_url, username, step_log)


    def _initialize_step_logging(self):
        """Initialize the step logging dictionary"""
        return {
            'start_time': time.time(),
            'driver_number': self.current_bookmark_driver_index + 1,
            'steps_completed': [],
            'failures': [],
            'success': False,
            'critical_sequence_completed': False
        }

    def _validate_bookmark_inputs(self, listing_url, username, step_log):
        """Validate inputs for bookmark function"""
        print(f'🔖 CYCLING: Starting bookmark process with driver {step_log["driver_number"]}/5')
        
        # Test mode handling
        if test_bookmark_function:
            actual_url = test_bookmark_link
            self._log_step(step_log, "test_mode_activated", True, f"Using test URL: {actual_url}")
        else:
            actual_url = listing_url
            self._log_step(step_log, "normal_mode_activated", True)
        
        # Username validation
        if not username:
            self._log_step(step_log, "username_validation", False, "No username provided")
            print("⚠️ Could not extract username, possible unable to detect false buy, exiting.")
            sys.exit(0)
        
        self._log_step(step_log, "username_validation", True, f"Username: {username}")
        print(f"🔖 Looking at listing {actual_url} posted by {username}")
        
        # Store the actual URL for later use
        step_log['actual_url'] = actual_url
        return True

    def _create_tab_and_navigate(self, current_driver, actual_url, step_log):
        """Create new tab and navigate to the listing URL"""
        try:
            # ENHANCED TAB MANAGEMENT
            stopwatch_start = time.time()
            print("⏱️ STOPWATCH: Starting timer for new tab and navigation...")
            current_driver.execute_script("window.open('');")
            new_tab = current_driver.window_handles[-1]
            current_driver.switch_to.window(new_tab)
            self._log_step(step_log, "new_tab_created", True, f"Total tabs: {len(current_driver.window_handles)}")
            
            # ROBUST NAVIGATION with retry
            navigation_success = False
            for nav_attempt in range(3):
                try:
                    self._log_step(step_log, f"navigation_attempt_{nav_attempt+1}", True)
                    current_driver.get(actual_url)
                    navigation_success = True
                    self._log_step(step_log, "navigation_complete", True)
                    break
                except Exception as nav_error:
                    self._log_step(step_log, f"navigation_attempt_{nav_attempt+1}", False, str(nav_error))
                    if nav_attempt == 2:
                        self._log_step(step_log, "navigation_final_failure", False, "All navigation attempts failed")
                        break
                    time.sleep(1)
            
            if not navigation_success:
                self._log_step(step_log, "navigation_failed", False, "Could not navigate to listing")
                return False
                
            return True
            
        except Exception as e:
            self._log_step(step_log, "tab_creation_error", False, str(e))
            return False


    def _execute_first_buy_sequence(self, current_driver, step_log):
        """Execute the first buy sequence with NEW pay-button-first logic"""
        self._log_step(step_log, "first_sequence_start", True)
        
        # Find and click first buy button
        first_buy_element, first_buy_selector = self._try_selectors(
            current_driver, 
            'buy_button', 
            operation='click', 
            timeout=5, 
            click_method='all',
            step_log=step_log
        )
        
        if not first_buy_element:
            self._log_step(step_log, "first_buy_button_not_found", False, "Item likely already sold")
            print('🔖 FIRST SEQUENCE: Buy button not found - this means ALREADY SOLD!!!')
            return False
        
        self._log_step(step_log, "first_buy_button_clicked", True, f"Used: {first_buy_selector[:30]}...")
        
        # NEW LOGIC: Wait for pay button to appear (indicates page has loaded)
        print("💳 PAY BUTTON WAIT: Waiting for pay button to determine page has loaded...")
        
        pay_button_found = False
        pay_button = None
        pay_selector = None
        
        # Repeatedly search for pay button until found
        max_pay_wait_attempts = 20  # 20 attempts * 0.5s = 10 seconds max wait
        pay_wait_attempt = 0
        
        while not pay_button_found and pay_wait_attempt < max_pay_wait_attempts:
            pay_wait_attempt += 1
            
            pay_element, pay_sel = self._try_selectors(
                current_driver,
                'pay_button',
                operation='find',
                timeout=0.5,  # Short timeout for each attempt
                step_log=step_log
            )
            
            if pay_element:
                pay_button_found = True
                pay_button = pay_element
                pay_selector = pay_sel
                print(f"✅ PAY BUTTON FOUND: Page loaded (attempt {pay_wait_attempt})")
                self._log_step(step_log, "pay_button_found", True, f"Found after {pay_wait_attempt} attempts")
                break
            
            # Short wait between attempts
            time.sleep(0.5)
        
        if not pay_button_found:
            self._log_step(step_log, "pay_button_not_found", False, "Payment interface never loaded")
            print("❌ PAY BUTTON: Never found - payment interface not available")
            return False
        
        # NOW handle shipping options (page is confirmed loaded)
        print("🚢 SHIPPING CHECK: Starting shipping option validation...")
        
        pay_button_is_valid = True  # Track if our pay button reference is still valid
        
        try:
            # Check if "Ship to pick-up point" is selected (aria-checked="true")
            pickup_selected = False
            try:
                pickup_element = current_driver.find_element(
                    By.XPATH, 
                    '//div[@data-testid="delivery-option-pickup" and @aria-checked="true"]'
                )
                pickup_selected = True
                print("📦 PICKUP SELECTED: Ship to pick-up point is currently selected")
                self._log_step(step_log, "pickup_point_selected", True)
            except NoSuchElementException:
                print("🏠 HOME SELECTED: Ship to home is selected (or pickup not selected)")
                self._log_step(step_log, "ship_home_selected", True)
                pickup_selected = False
            
            # If pickup is selected, check for "Choose a pick-up point" message
            if pickup_selected:
                try:
                    choose_pickup_element = current_driver.find_element(
                        By.XPATH,
                        '//h2[@class="web_ui__Text__text web_ui__Text__title web_ui__Text__left" and text()="Choose a pick-up point"]'
                    )
                    
                    # If we can see "Choose a pick-up point", we need to switch to Ship to home
                    print("⚠️ PICKUP ISSUE: Found 'Choose a pick-up point' - need to switch to Ship to home")
                    self._log_step(step_log, "choose_pickup_point_found", True)
                    
                    # Click "Ship to home"
                    try:
                        ship_home_element = current_driver.find_element(
                            By.XPATH,
                            '//h2[@class="web_ui__Text__text web_ui__Text__title web_ui__Text__left" and text()="Ship to home"]'
                        )
                        ship_home_element.click()
                        print("🏠 SWITCHED: Successfully clicked 'Ship to home'")
                        self._log_step(step_log, "switched_to_ship_home", True)
                        
                        # CRITICAL: The previous pay button reference is now INVALID
                        pay_button_is_valid = False
                        print("⚠️ PAY BUTTON: Previous reference invalidated by shipping change")
                        
                        # Wait 0.3 seconds as specifically requested
                        time.sleep(0.3)
                        print("⏳ WAITED: 0.3 seconds after switching to Ship to home")
                        
                        # NOW search for pay button again
                        print("🔍 PAY BUTTON: Searching again after shipping change...")
                        
                        pay_button_found_again = False
                        max_retry_attempts = 10  # 10 attempts * 0.5s = 5 seconds max
                        retry_attempt = 0
                        
                        while not pay_button_found_again and retry_attempt < max_retry_attempts:
                            retry_attempt += 1
                            
                            pay_element_new, pay_sel_new = self._try_selectors(
                                current_driver,
                                'pay_button',
                                operation='find',
                                timeout=0.5,
                                step_log=step_log
                            )
                            
                            if pay_element_new:
                                pay_button = pay_element_new
                                pay_selector = pay_sel_new
                                pay_button_is_valid = True
                                pay_button_found_again = True
                                print(f"✅ PAY BUTTON: Found again after shipping change (attempt {retry_attempt})")
                                self._log_step(step_log, "pay_button_found_after_shipping_change", True)
                                break
                            
                            time.sleep(0.5)
                        
                        if not pay_button_found_again:
                            print("❌ PAY BUTTON: Could not find pay button after shipping change")
                            self._log_step(step_log, "pay_button_not_found_after_shipping", False)
                            return False
                            
                    except NoSuchElementException:
                        print("❌ SWITCH ERROR: Could not find 'Ship to home' button")
                        self._log_step(step_log, "ship_home_button_not_found", False)
                    except Exception as switch_error:
                        print(f"❌ SWITCH ERROR: Could not click 'Ship to home': {switch_error}")
                        self._log_step(step_log, "switch_to_home_failed", False, str(switch_error))
                        
                except NoSuchElementException:
                    # Pickup is selected but no "Choose a pick-up point" message
                    print("✅ PICKUP OK: Pick-up point selected but no 'Choose a pick-up point' message - continuing normally")
                    self._log_step(step_log, "pickup_point_ready", True)
            
            else:
                # Ship to home is selected - continue normally  
                print("✅ HOME OK: Ship to home is selected - no changes needed")
                self._log_step(step_log, "ship_home_already_selected", True)
            
        except Exception as shipping_error:
            print(f"❌ SHIPPING ERROR: Unexpected error during shipping check: {shipping_error}")
            self._log_step(step_log, "shipping_check_error", False, str(shipping_error))
            # Continue anyway - don't fail the entire process for shipping issues
        
        print("✅ SHIPPING CHECK: Validation completed - proceeding to click pay button")
        
        # Verify we have a valid pay button before clicking
        if not pay_button_is_valid or not pay_button:
            print("❌ PAY BUTTON: No valid pay button reference - cannot proceed")
            self._log_step(step_log, "no_valid_pay_button", False)
            return False
        
        # Execute the critical pay sequence with our confirmed valid pay button
        return self._execute_critical_pay_sequence_with_button(current_driver, pay_button, step_log)

    def _execute_critical_pay_sequence_with_button(self, current_driver, pay_button, step_log):
        """Execute the critical pay sequence using the provided pay button - CANNOT be modified!"""
        try:
            # FORCE-click the pay button using multiple aggressive methods
            pay_clicked = False
            
            # Method 1: Click the pay button directly
            try:
                pay_button.click()
                self._log_step(step_log, "pay_button_click_direct", True, "Clicked pay button directly")
                pay_clicked = True
            except Exception as direct_error:
                self._log_step(step_log, "pay_button_click_direct", False, str(direct_error))
            
            # Method 2: Click the inner span directly
            if not pay_clicked:
                try:
                    pay_span = current_driver.find_element(By.XPATH, "//button[@data-testid='single-checkout-order-summary-purchase-button']//span[text()='Pay']")
                    pay_span.click()
                    self._log_step(step_log, "pay_button_click_span", True, "Clicked Pay span directly")
                    pay_clicked = True
                except Exception as span_error:
                    self._log_step(step_log, "pay_button_click_span", False, str(span_error))
            
            # Method 3: Force enable button and click via JS
            if not pay_clicked:
                try:
                    current_driver.execute_script("""
                        var button = document.querySelector('button[data-testid="single-checkout-order-summary-purchase-button"]');
                        if (button) {
                            button.disabled = false;
                            button.setAttribute('aria-disabled', 'false');
                            button.click();
                        }
                    """)
                    self._log_step(step_log, "pay_button_click_force_js", True, "Force-enabled and clicked via JS")
                    pay_clicked = True
                except Exception as js_error:
                    self._log_step(step_log, "pay_button_click_force_js", False, str(js_error))
            
            # Method 4: Dispatch click event directly
            if not pay_clicked:
                try:
                    current_driver.execute_script("""
                        var button = document.querySelector('button[data-testid="single-checkout-order-summary-purchase-button"]');
                        if (button) {
                            var event = new MouseEvent('click', {
                                view: window,
                                bubbles: true,
                                cancelable: true
                            });
                            button.dispatchEvent(event);
                        }
                    """)
                    self._log_step(step_log, "pay_button_click_dispatch_event", True, "Dispatched click event directly")
                    pay_clicked = True
                except Exception as dispatch_error:
                    self._log_step(step_log, "pay_button_click_dispatch_event", False, str(dispatch_error))
            
            if not pay_clicked:
                self._log_step(step_log, "pay_button_click_all_failed", False, "All 4 aggressive methods failed")
                return False
            
            # ⚠️ CRITICAL: Exact 0.25 second wait - DO NOT MODIFY! ⚠️
            print("🔖 CRITICAL: Waiting exactly 0.25 seconds...")
            time.sleep(0.25)
            
            # ⚠️ CRITICAL: Immediate tab close - DO NOT MODIFY! ⚠️ 
            print("🔖 CRITICAL: Closing tab immediately...")
            current_driver.close()

            stopwatch_end = time.time()
            elapsed = stopwatch_end - step_log['start_time']
            print(f"⏱️ STOPWATCH: First sequence completed in {elapsed:.3f} seconds")
                            
            step_log['critical_sequence_completed'] = True
            self._log_step(step_log, "critical_sequence_completed", True, "0.25s wait + tab close")
            
            # Switch back to main tab
            if len(current_driver.window_handles) > 0:
                current_driver.switch_to.window(current_driver.window_handles[0])
                self._log_step(step_log, "return_to_main_tab", True)
            
            self._log_step(step_log, "first_sequence_complete", True)
            return True
            
        except Exception as critical_error:
            self._log_step(step_log, "critical_sequence_error", False, str(critical_error))
            return False

    def _execute_second_sequence_with_monitoring(self, current_driver, actual_url, username, step_log):
        """Execute second sequence with Purchase unsuccessful monitoring"""
        self._log_step(step_log, "second_sequence_start", True)
        
        try:
            # Open new tab for second sequence
            current_driver.execute_script("window.open('');")
            second_tab = current_driver.window_handles[-1]
            current_driver.switch_to.window(second_tab)
            self._log_step(step_log, "second_tab_created", True)
            
            # Navigate again
            current_driver.get(actual_url)
            self._log_step(step_log, "second_navigation", True)
            
            # Look for buy button again
            second_buy_element, second_buy_selector = self._try_selectors(
                current_driver,
                'buy_button',
                operation='click',
                timeout=15,
                click_method='all',
                step_log=step_log
            )
            
            if second_buy_element:
                self._log_step(step_log, "second_buy_button_clicked", True, f"Used: {second_buy_selector[:30]}...")
                
                # Check for processing payment success
                success = self._check_processing_payment_with_monitoring(current_driver, step_log)
                
                # MODIFIED: Don't close second tab here if monitoring is active
                if not (success and step_log.get('monitoring_active', False)):
                    # Close second tab only if not monitoring
                    current_driver.close()
                    if len(current_driver.window_handles) > 0:
                        current_driver.switch_to.window(current_driver.window_handles[0])
                    self._log_step(step_log, "second_tab_closed", True)
                
                if success:
                    return True
            else:
                self._log_step(step_log, "second_buy_button_not_found", False, "Proceeding with messages")
            
            # Execute messages sequence (only if not monitoring)
            if not step_log.get('monitoring_active', False):
                return self._execute_messages_sequence(current_driver, actual_url, username, step_log)
            else:
                return True  # Return true if monitoring started
                
        except Exception as second_sequence_error:
            self._log_step(step_log, "second_sequence_error", False, str(second_sequence_error))
            return True  # Return True as this isn't a critical failure

    def _check_processing_payment_with_monitoring(self, current_driver, step_log):
        """Check for processing payment message and start monitoring if found"""
        processing_element, processing_selector = self._try_selectors(
            current_driver,
            'processing_payment',
            operation='find',
            timeout=3,
            step_log=step_log
        )
        
        if processing_element:
            element_text = processing_element.text.strip()
            self._log_step(step_log, "processing_payment_found", True, f"Text: {element_text}")
            print('SUCCESSFUL BOOKMARK! CONFIRMED VIA PROCESSING PAYMENT!')
            
            # START MONITORING FOR "Purchase unsuccessful" - NEW FUNCTIONALITY
            print('🔍 MONITORING: Starting "Purchase unsuccessful" detection...')
            step_log['success'] = True
            step_log['monitoring_active'] = True
            
            # Start monitoring in separate thread so other processing can continue
            monitoring_thread = threading.Thread(
                target=self._monitor_purchase_unsuccessful,
                args=(current_driver, step_log)
            )
            monitoring_thread.daemon = True  # Don't block program exit
            monitoring_thread.start()
            
            return True
        else:
            self._log_step(step_log, "processing_payment_not_found", False, "Processing payment message not found")
            print('listing likely bookmarked by another')
            return False


    def bookmark_driver(self, listing_url, username=None):
        """
        MAIN bookmark driver function - FIXED to properly handle monitoring cleanup
        """
        
        # Initialize step logging
        step_log = self._initialize_step_logging()
        
        # Validate inputs and setup
        if not self._validate_bookmark_inputs(listing_url, username, step_log):
            self._log_final_bookmark_result(step_log)
            return False
        
        try:
            # Get the cycling driver
            current_driver = self.get_next_bookmark_driver()
            if current_driver is None:
                self._log_step(step_log, "driver_creation_failed", False, "Could not create cycling driver")
                self._log_final_bookmark_result(step_log)
                return False
            
            self._log_step(step_log, "cycling_driver_created", True, f"Driver {step_log['driver_number']} ready")
            
            try:
                # Execute the main bookmark sequences
                success = self._execute_bookmark_sequences_with_monitoring(current_driver, listing_url, username, step_log)
                
                if success:
                    step_log['success'] = True
                    self._log_step(step_log, "bookmark_function_success", True)
                
                self._log_final_bookmark_result(step_log)
                return success
                
            except Exception as main_error:
                self._log_step(step_log, "main_function_error", False, str(main_error))
                self._log_final_bookmark_result(step_log)
                return False
                
        finally:
            # FIXED: Only close driver if monitoring is NOT active
            if step_log.get('monitoring_active', False):
                print(f"🔍 MONITORING: Active - driver cleanup will be handled by monitoring thread")
                # The monitoring thread will handle driver cleanup when it completes
            else:
                print(f"🗑️ CYCLING: No monitoring active - closing driver normally")
                self.close_current_bookmark_driver()
                print(f"🔄 CYCLING: Driver {step_log['driver_number']} processed, next will be {self.current_bookmark_driver_index + 1}/5")

    def cleanup_purchase_unsuccessful_monitoring(self):
        """
        Clean up any active purchase unsuccessful monitoring when program exits
        """
        global purchase_unsuccessful_detected_urls
        print(f"🧹 CLEANUP: Stopping purchase unsuccessful monitoring for {len(purchase_unsuccessful_detected_urls)} URLs")
        purchase_unsuccessful_detected_urls.clear()

    def _monitor_purchase_unsuccessful(self, current_driver, step_log):
        """
        MODIFIED: Monitor for "Purchase unsuccessful" message and trigger buying drivers
        """
        import time
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        from selenium.common.exceptions import TimeoutException
        
        # Set the monitoring flag
        self.monitoring_threads_active.set()
        
        # Get the current URL being monitored
        current_url = current_driver.current_url
        
        # Start the stopwatch
        monitoring_start_time = time.time()
        print(f"⏱️ STOPWATCH: Started monitoring at {time.strftime('%H:%M:%S')}")
        
        # Maximum wait time: 25 minutes (1500 seconds)
        max_wait_time = 25 * 60  # 1500 seconds
        
        # Define selectors for "Purchase unsuccessful" message
        unsuccessful_selectors = [
            "//div[@class='web_uiCellheading']//div[@class='web_uiCelltitle'][@data-testid='conversation-message--status-message--title']//h2[@class='web_uiTexttext web_uiTexttitle web_uiTextleft web_uiTextwarning' and text()='Purchase unsuccessful']",
            "//h2[@class='web_uiTexttext web_uiTexttitle web_uiTextleft web_uiTextwarning' and text()='Purchase unsuccessful']",
            "//*[contains(@class, 'web_uiTextwarning') and text()='Purchase unsuccessful']",
            "//*[text()='Purchase unsuccessful']"
        ]
        
        print(f"🔍 MONITORING: Watching for 'Purchase unsuccessful' for up to {max_wait_time/60:.0f} minutes...")
        
        global purchase_unsuccessful_detected_urls
        
        try:
            while True:
                elapsed_time = time.time() - monitoring_start_time
                
                # Check if we've exceeded the maximum wait time
                if elapsed_time >= max_wait_time:
                    print(f"⏰ TIMEOUT: Maximum wait time of {max_wait_time/60:.0f} minutes reached")
                    print(f"⏱️ STOPWATCH: Monitoring ended after {elapsed_time/60:.2f} minutes (TIMEOUT)")
                    break
                
                # Check if driver is still alive
                try:
                    current_driver.current_url
                except Exception as driver_dead:
                    print(f"💀 MONITORING: Driver died during monitoring: {driver_dead}")
                    print(f"⏱️ STOPWATCH: Monitoring ended after {elapsed_time/60:.2f} minutes (DRIVER DIED)")
                    break
                
                # Try each selector to find "Purchase unsuccessful"
                found_unsuccessful = False
                for selector in unsuccessful_selectors:
                    try:
                        element = WebDriverWait(current_driver, 1).until(
                            EC.presence_of_element_located((By.XPATH, selector))
                        )
                        
                        # Found it!
                        end_time = time.time()
                        total_elapsed = end_time - monitoring_start_time
                        
                        print(f"🎯 FOUND! 'Purchase unsuccessful' detected!")
                        print(f"📍 ELEMENT: Found using selector: {selector}")
                        print(f"⏱️ STOPWATCH: Monitoring completed in {total_elapsed/60:.2f} minutes ({total_elapsed:.2f} seconds)")
                        print(f"🕒 TIME: Found at {time.strftime('%H:%M:%S')}")
                        
                        # MODIFIED: Signal all waiting buying drivers to click pay NOW
                        print(f"🚀 TRIGGERING: All waiting buying drivers to click pay NOW!")
                        
                        for url, entry in purchase_unsuccessful_detected_urls.items():
                            if entry.get('waiting', True):
                                print(f"🎯 TRIGGERING: Buying driver for {url[:50]}...")
                                entry['waiting'] = False  # Signal the buying driver
                        
                        self._log_step(step_log, "purchase_unsuccessful_found", True, 
                                    f"Found after {total_elapsed:.2f}s using: {selector[:50]}...")
                        
                        found_unsuccessful = True
                        break
                        
                    except TimeoutException:
                        continue
                    except Exception as selector_error:
                        print(f"⚠️ MONITORING: Error with selector {selector}: {selector_error}")
                        continue
                
                if found_unsuccessful:
                    break
                    
                # Wait a bit before checking again
                time.sleep(0.5)  # Check every 500ms for faster response
        
        except Exception as monitoring_error:
            end_time = time.time()
            total_elapsed = end_time - monitoring_start_time
            print(f"❌ MONITORING ERROR: {monitoring_error}")
            print(f"⏱️ STOPWATCH: Monitoring ended after {total_elapsed/60:.2f} minutes (ERROR)")
            self._log_step(step_log, "monitoring_error", False, str(monitoring_error))
        
        finally:
            # Clean up monitoring
            step_log['monitoring_active'] = False
            self.monitoring_threads_active.clear()
            
            print(f"🗑️ MONITORING CLEANUP: Closing monitoring tab and advancing driver...")
            try:
                current_driver.close()
                print(f"✅ MONITORING CLEANUP: Closed monitoring tab")
            except Exception as tab_close_error:
                print(f"⚠️ MONITORING CLEANUP: Error closing tab: {tab_close_error}")
            
            try:
                self.close_current_bookmark_driver()
                print(f"✅ MONITORING CLEANUP: Closed bookmark driver and advanced to next")
            except Exception as driver_close_error:
                print(f"⚠️ MONITORING CLEANUP: Error closing driver: {driver_close_error}")
            
            print(f"🔄 MONITORING COMPLETE: Driver cleanup finished, ready for next bookmark")
            
    def _execute_messages_sequence(self, current_driver, actual_url, username, step_log):
        """Execute the messages sequence for username validation"""
        self._log_step(step_log, "messages_sequence_start", True)
        
        try:
            # Open messages tab
            current_driver.execute_script("window.open('');")
            messages_tab = current_driver.window_handles[-1]
            current_driver.switch_to.window(messages_tab)
            self._log_step(step_log, "messages_tab_created", True)
            
            # Navigate to URL for messages
            current_driver.get(actual_url)
            self._log_step(step_log, "messages_navigation", True)
            
            # Find and click messages button
            messages_element, messages_selector = self._try_selectors(
                current_driver,
                'messages_button',
                operation='click',
                timeout=1,
                click_method='all',
                step_log=step_log
            )
            
            if messages_element:
                self._log_step(step_log, "messages_button_clicked", True, f"Used: {messages_selector[:30]}...")
                
                # Search for username
                self._search_for_username(current_driver, username, actual_url, step_log)
            else:
                self._log_step(step_log, "messages_button_not_found", False, "Messages button not found with any selector")
            
            # Close messages tab
            current_driver.close()
            if len(current_driver.window_handles) > 0:
                current_driver.switch_to.window(current_driver.window_handles[0])
            self._log_step(step_log, "messages_tab_closed", True)
            
            return True
            
        except Exception as messages_error:
            self._log_step(step_log, "messages_sequence_error", False, str(messages_error))
            # Clean up messages tab
            try:
                current_driver.close()
                if len(current_driver.window_handles) > 0:
                    current_driver.switch_to.window(current_driver.window_handles[0])
            except:
                pass
            return True

    def _search_for_username(self, current_driver, username, actual_url, step_log):
        """Search for username in messages to detect accidental purchases"""
        if not username:
            self._log_step(step_log, "no_username_for_search", False, "No username available")
            time.sleep(3)
            return
        
        self._log_step(step_log, "username_search_start", True, f"Searching for: {username}")
        time.sleep(2)  # Wait for messages page to load
        
        try:
            username_element = WebDriverWait(current_driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, f"//h2[contains(@class, 'web_ui') and contains(@class, 'Text') and contains(@class, 'title') and text()='{username}']"))
            )
            
            self._log_step(step_log, "username_found_on_messages", True, f"Found: {username}")
            
            # Try to click username
            username_clicked = self._click_username_element(current_driver, username_element, step_log)
            
            if username_clicked:
                self._log_step(step_log, "accidental_purchase_detected", True, "ABORT - username found in messages")
                print("USERNAME FOUND, POSSIBLE ACCIDENTAL PURCHASE, ABORT")
                time.sleep(3)
                self._log_final_bookmark_result(step_log)
                sys.exit(0)
            else:
                self._log_step(step_log, "username_click_failed", False, "Could not click username")
                
        except TimeoutException:
            self._log_step(step_log, "username_not_found_in_messages", True, f"Username {username} not in messages - likely bookmarked!")
            print(f"📧 NOT FOUND: Username '{username}' not found on messages page")
            print(f"unable to find username {username} for listing {actual_url}, likely bookmarked!")
        except Exception as search_error:
            self._log_step(step_log, "username_search_error", False, str(search_error))
            print(f"unable to find username {username} for listing {actual_url}, likely bookmarked!")

    def _click_username_element(self, current_driver, username_element, step_log):
        """Try to click the username element with multiple methods"""
        username_clicked = False
        for click_method in ['standard', 'javascript', 'actionchains']:
            try:
                if click_method == 'standard':
                    username_element.click()
                elif click_method == 'javascript':
                    current_driver.execute_script("arguments[0].click();", username_element)
                elif click_method == 'actionchains':
                    ActionChains(current_driver).move_to_element(username_element).click().perform()
                
                username_clicked = True
                self._log_step(step_log, f"username_clicked_{click_method}", True)
                break
            except:
                continue
        return username_clicked

    def _try_selectors(self, driver, selector_set_name, operation='find', timeout=5, click_method='standard', step_log=None):
        """Try selectors with quick timeouts and fail fast"""
        SELECTOR_SETS = {

            'purchase_unsuccessful': [
                "//h2[@class='web_uiTexttext web_uiTexttitle web_uiTextleft web_uiTextwarning' and text()='Purchase unsuccessful']",
                "//div[@class='web_uiCelltitle'][@data-testid='conversation-message--status-message--title']//h2[@class='web_uiTexttext web_uiTexttitle web_uiTextleft web_uiTextwarning' and text()='Purchase unsuccessful']",
                "//div[@class='web_uiCellheading']//div[@class='web_uiCelltitle'][@data-testid='conversation-message--status-message--title']//h2[@class='web_uiTexttext web_uiTexttitle web_uiTextleft web_uiTextwarning' and text()='Purchase unsuccessful']",
                "//*[contains(@class, 'web_uiTextwarning') and text()='Purchase unsuccessful']",
                "//*[text()='Purchase unsuccessful']"
            ],

            'buy_button': [
                "button[data-testid='item-buy-button']",
                "button.web_ui__Button__primary[data-testid='item-buy-button']",
                "button.web_ui__Button__button.web_ui__Button__filled.web_ui__Button__default.web_ui__Button__primary.web_ui__Button__truncated",
                "//button[@data-testid='item-buy-button']",
                "//button[contains(@class, 'web_ui__Button__primary')]//span[text()='Buy now']"
            ],
            'pay_button': [
                'button[data-testid="single-checkout-order-summary-purchase-button"]',
                'button[data-testid="single-checkout-order-summary-purchase-button"].web_ui__Button__primary',
                '//button[@data-testid="single-checkout-order-summary-purchase-button"]',
                'button.web_ui__Button__primary[data-testid*="purchase"]',
                '//button[contains(@data-testid, "purchase-button")]'
            ],
            'processing_payment': [
                "//h2[@class='web_ui__Text__text web_ui__Text__title web_ui__Text__left' and text()='Processing payment']",
                "//h2[contains(@class, 'web_ui__Text__title') and text()='Processing payment']",
                "//span[@class='web_ui__Text__text web_ui__Text__body web_ui__Text__left web_ui__Text__format' and contains(text(), \"We've reserved this item for you until your payment finishes processing\")]",
                "//span[contains(text(), \"We've reserved this item for you until your payment finishes processing\")]",
                "//*[contains(text(), 'Processing payment')]"
            ],
            'messages_button': [
                "a[data-testid='header-conversations-button']",
                "a[href='/inbox'][data-testid='header-conversations-button']",
                "a[href='/inbox'].web_ui__Button__button",
                "a[aria-label*='message'][href='/inbox']",
                "a[href='/inbox']"
            ]
        }
        
        selectors = SELECTOR_SETS.get(selector_set_name, [])
        if not selectors:
            if step_log:
                self._log_step(step_log, f"try_selectors_{selector_set_name}", False, "No selectors defined")
            return None, None
        
        for i, selector in enumerate(selectors):
            try:
                if selector.startswith('//'):
                    element = WebDriverWait(driver, timeout).until(
                        EC.element_to_be_clickable((By.XPATH, selector)) if operation == 'click' 
                        else EC.presence_of_element_located((By.XPATH, selector))
                    )
                else:
                    element = WebDriverWait(driver, timeout).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector)) if operation == 'click'
                        else EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                
                if operation == 'click':
                    click_success = self._perform_element_click(driver, element, click_method, step_log, selector_set_name)
                    if not click_success:
                        continue
                
                if step_log:
                    self._log_step(step_log, f"selector_{selector_set_name}_success", True, f"Used selector #{i+1}")
                return element, selector
                
            except TimeoutException:
                if step_log:
                    self._log_step(step_log, f"selector_{selector_set_name}_{i+1}_timeout", False, f"Timeout after {timeout}s")
                continue
            except Exception as e:
                if step_log:
                    self._log_step(step_log, f"selector_{selector_set_name}_{i+1}_error", False, str(e))
                continue
        
        if step_log:
            self._log_step(step_log, f"all_selectors_{selector_set_name}_failed", False, f"All {len(selectors)} selectors failed")
        return None, None

    def _perform_element_click(self, driver, element, click_method, step_log, selector_set_name):
        """Perform element click with specified method(s)"""
        click_success = False
        click_methods = ['standard', 'javascript', 'actionchains'] if click_method == 'all' else [click_method]
        
        for method in click_methods:
            try:
                if method == 'standard':
                    element.click()
                elif method == 'javascript':
                    driver.execute_script("arguments[0].click();", element)
                elif method == 'actionchains':
                    ActionChains(driver).move_to_element(element).click().perform()
                
                click_success = True
                if step_log:
                    self._log_step(step_log, f"click_{selector_set_name}_{method}", True)
                break
            except Exception as click_error:
                if step_log:
                    self._log_step(step_log, f"click_{selector_set_name}_{method}", False, str(click_error))
                continue
        
        return click_success

    def _log_step(self, step_log, step_name, success=True, error_msg=None):
        """Log each step for debugging and success rate analysis"""
        if success:
            step_log['steps_completed'].append(f"{step_name} - {time.time() - step_log['start_time']:.2f}s")
            print(f"✅ DRIVER {step_log['driver_number']}: {step_name}")
        else:
            step_log['failures'].append(f"{step_name}: {error_msg} - {time.time() - step_log['start_time']:.2f}s")
            print(f"❌ DRIVER {step_log['driver_number']}: {step_name} - {error_msg}")

    def _log_final_bookmark_result(self, step_log):
        """Log comprehensive results for success rate analysis"""
        total_time = time.time() - step_log['start_time']
        print(f"\n📊 BOOKMARK ANALYSIS - Driver {step_log['driver_number']}")
        print(f"🔗 URL: {step_log.get('actual_url', 'N/A')[:60]}...")
        print(f"⏱️  Total time: {total_time:.2f}s")
        print(f"✅ Steps completed: {len(step_log['steps_completed'])}")
        print(f"❌ Failures: {len(step_log['failures'])}")
        print(f"🎯 Critical sequence: {'YES' if step_log['critical_sequence_completed'] else 'NO'}")
        print(f"🏆 Overall success: {'YES' if step_log['success'] else 'NO'}")
        
        # Log failures for analysis
        if step_log['failures']:
            print("🔍 FAILURE DETAILS:")
            for failure in step_log['failures'][:3]:  # Show first 3 failures
                print(f"  • {failure}")
    def cleanup_all_cycling_bookmark_drivers(self):
        """
        Clean up any remaining cycling bookmark driver when program exits
        """
        if self.current_bookmark_driver is not None:
            try:
                self.current_bookmark_driver.quit()
                print("🔖 CLEANUP: Cycling bookmark driver closed")
            except:
                pass
            finally:
                self.current_bookmark_driver = None

    def cleanup_persistent_bookmark_driver(self):
        """
        Call this method to clean up the persistent bookmark driver when done
        """
        if hasattr(self, 'persistent_bookmark_driver') and self.persistent_bookmark_driver is not None:
            try:
                self.persistent_bookmark_driver.quit()
                print("🔖 CLEANUP: Persistent bookmark driver closed")
            except:
                pass
            finally:
                self.persistent_bookmark_driver = None

    def check_chrome_processes(self):
        """
        Debug function to check for running Chrome processes
        """
        import psutil
        chrome_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'chrome' in proc.info['name'].lower():
                    chrome_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cmdline': ' '.join(proc.info['cmdline'][:3]) if proc.info['cmdline'] else ''
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        print(f"🔖 CHROME PROCESSES: Found {len(chrome_processes)} running Chrome processes")
        for proc in chrome_processes[:5]:  # Show first 5
            print(f"  • PID: {proc['pid']}, Name: {proc['name']}")
        
        return len(chrome_processes)

    def setup_driver_enhanced_debug(self):
        """
        Enhanced setup_driver with comprehensive debugging
        """
        print("🚀 ENHANCED DRIVER SETUP: Starting...")
        
        # Check for existing Chrome processes
        self.check_chrome_processes()
        
        chrome_opts = Options()
        
        # Basic preferences
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_values.popups": 0,
            "download.prompt_for_download": False,
        }
        chrome_opts.add_experimental_option("prefs", prefs)
        
        # User data directory setup
        print(f"🚀 USER DATA DIR: {PERMANENT_USER_DATA_DIR}")
        chrome_opts.add_argument(f"--user-data-dir={PERMANENT_USER_DATA_DIR}")
        chrome_opts.add_argument(f"--profile-directory=Default")
        
        # Check if user data directory exists and is accessible
        try:
            if not os.path.exists(PERMANENT_USER_DATA_DIR):
                os.makedirs(PERMANENT_USER_DATA_DIR, exist_ok=True)
                print(f"🚀 CREATED: User data directory")
            else:
                print(f"🚀 EXISTS: User data directory found")
        except Exception as dir_error:
            print(f"🚀 DIR ERROR: {dir_error}")
        
        # Core stability arguments (minimal set)
        chrome_opts.add_argument("--no-sandbox")
        chrome_opts.add_argument("--disable-dev-shm-usage")
        chrome_opts.add_argument("--disable-gpu")
        chrome_opts.add_argument("--disable-software-rasterizer")
        
        # Remove potentially problematic arguments
        chrome_opts.add_argument("--headless")  # Try without headless first
        
        # Keep some logging for debugging
        chrome_opts.add_argument("--log-level=3")  # More detailed logging
        chrome_opts.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        
        try:
            service = Service(
                ChromeDriverManager().install()
            )
            
            print("🚀 CREATING: Chrome driver...")
            driver = webdriver.Chrome(service=service, options=chrome_opts)
            
            # Set timeouts
            driver.implicitly_wait(10)
            driver.set_page_load_timeout(30)
            driver.set_script_timeout(30)
            
            print("✅ SUCCESS: Chrome driver initialized successfully")
            return driver
            
        except Exception as e:
            print(f"❌ CRITICAL ERROR: Chrome driver failed: {e}")
            print(f"❌ ERROR TYPE: {type(e).__name__}")
            
            import traceback
            print(f"❌ TRACEBACK:\n{traceback.format_exc()}")
            
            # Show system info for debugging
            print("🔧 SYSTEM INFO:")
            print(f"  • Python: {sys.version}")
            print(f"  • OS: {os.name}")
            print(f"  • Chrome processes: {self.check_chrome_processes()}")
            
            return None

    def setup_persistent_buying_driver(self):
        
        """
        Set up the persistent buying driver that stays open throughout the program
        """
        if self.persistent_buying_driver is not None:
            return True  # Already set up
            
        print("🚀 SETUP: Initializing persistent buying driver...")
        
        try:
            print('USING SETUP_PRSISTENT_BUYING_DRIVER')

            service = Service(
                ChromeDriverManager().install(),
                log_path=os.devnull
            )
            
            chrome_opts = Options()
            #chrome_opts.add_argument("--headless")
            chrome_opts.add_argument("--user-data-dir=C:\VintedBuyer1")
            chrome_opts.add_argument("--profile-directory=Default")
            chrome_opts.add_argument("--no-sandbox")
            chrome_opts.add_argument("--disable-dev-shm-usage")
            chrome_opts.add_argument("--disable-gpu")
            chrome_opts.add_argument("--window-size=800,600")
            chrome_opts.add_argument("--log-level=3")
            chrome_opts.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
                                
            self.persistent_buying_driver = webdriver.Chrome(service=service, options=chrome_opts)
            
            # Set fast timeouts for quick processing
            self.persistent_buying_driver.implicitly_wait(1)
            self.persistent_buying_driver.set_page_load_timeout(8)
            self.persistent_buying_driver.set_script_timeout(3)
            
            # Navigate main tab to vinted.co.uk and keep it as reference
            print("🚀 SETUP: Navigating main tab to vinted.co.uk...")
            self.persistent_buying_driver.get("https://www.vinted.co.uk")
            self.main_tab_handle = self.persistent_buying_driver.current_window_handle
            
            print("✅ SETUP: Persistent buying driver ready!")
            return True
            
        except Exception as e:
            print(f"❌ SETUP: Failed to create persistent buying driver: {e}")
            self.persistent_buying_driver = None
            self.main_tab_handle = None
            return False

    def test_url_collection_mode(self, driver, search_query):
        """
        Simple testing mode that only collects URLs and saves listing IDs
        No bookmarking, no purchasing, no image downloading - just URL collection
        """
        print("🧪 TEST_NUMBER_OF_LISTINGS MODE: Starting URL collection only")
        
        # Setup search URL with parameters
        params = {
            "search_text": search_query,
            "price_from": PRICE_FROM,
            "price_to": PRICE_TO,
            "currency": CURRENCY,
            "order": ORDER,
        }
        driver.get(f"{BASE_URL}?{urlencode(params)}")
        
        refresh_cycle = 1
        
        while True:
            print(end=" ")
            
            try:
                # Wait for page to load
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.feed-grid"))
                )
            except TimeoutException:
                print("0 listings (page load timeout)")
                refresh_cycle += 1
                time.sleep(5)
                continue
            
            # Get listing URLs from current page
            els = driver.find_elements(By.CSS_SELECTOR, "a.new-item-box__overlay")
            urls = [e.get_attribute("href") for e in els if e.get_attribute("href")]
            
            if not urls:
                print("0 listings (no URLs found)")
                refresh_cycle += 1
                time.sleep(5)
                continue
            
            # Count new URLs that haven't been seen before
            new_urls = []
            for url in urls:
                listing_id = self.extract_vinted_listing_id(url)
                if listing_id:
                    # Check if we've already saved this ID
                    try:
                        with open(VINTED_SCANNED_IDS_FILE, 'r') as f:
                            existing_ids = f.read().splitlines()
                        
                        if listing_id not in existing_ids:
                            new_urls.append(url)
                            # Save the listing ID
                            with open(VINTED_SCANNED_IDS_FILE, 'a') as f:
                                f.write(f"{listing_id}\n")
                    except FileNotFoundError:
                        # File doesn't exist yet, all URLs are new
                        new_urls.append(url)
                        with open(VINTED_SCANNED_IDS_FILE, 'a') as f:
                            f.write(f"{listing_id}\n")
            
            # Print the count of new listings found
            print(f"{len(new_urls)} listings")
            
            # Refresh the page and continue
            driver.refresh()
            refresh_cycle += 1
            
            # Small delay to prevent overwhelming the server
            time.sleep(2)


    def test_suitable_urls_mode(self, driver):
        """
        Simple function to cycle through TEST_SUITABLE_URLS and display each on pygame
        Only uses the scraping driver, no buying or bookmarking drivers
        Forces ALL listings to be added to pygame regardless of suitability
        """
        global suitable_listings, current_listing_index, VINTED_SHOW_ALL_LISTINGS, bookmark_listings
        
        print("🧪 TEST_WHETHER_SUITABLE = True - Starting test suitable URLs mode")
        
        # Temporarily override settings to force all listings to show
        original_show_all = VINTED_SHOW_ALL_LISTINGS
        original_bookmark = bookmark_listings
        VINTED_SHOW_ALL_LISTINGS = True  # Force show all listings
        bookmark_listings = False  # Disable bookmarking
        
        # Clear previous results
        suitable_listings.clear()
        current_listing_index = 0
        
        # Load YOLO Model
        print("🧠 Loading object detection model...")
        if torch.cuda.is_available():
            model = YOLO(MODEL_WEIGHTS).cuda()
            print("✅ YOLO model loaded on GPU")
        else:
            model = YOLO(MODEL_WEIGHTS).cpu()
            print("⚠️ YOLO model loaded on CPU (no CUDA available)")
        
        # Process each URL in TEST_SUITABLE_URLS
        for idx, url in enumerate(TEST_SUITABLE_URLS, 1):
            print(f"\n🔍 Processing test URL {idx}/{len(TEST_SUITABLE_URLS)}")
            print(f"🔗 URL: {url}")
            
            try:
                # Open new tab
                driver.execute_script("window.open();")
                driver.switch_to.window(driver.window_handles[-1])
                driver.get(url)
                
                # Scrape details
                details = self.scrape_item_details(driver)
                
                # Download images
                listing_dir = os.path.join(DOWNLOAD_ROOT, f"test_listing_{idx}")
                image_paths = self.download_images_for_listing(driver, listing_dir)
                
                # Perform object detection
                detected_objects = {}
                processed_images = []
                if model and image_paths:
                    detected_objects, processed_images = self.perform_detection_on_listing_images(model, listing_dir)
                
                # Process for pygame display (no booking logic, force show all)
                self.process_vinted_listing(details, detected_objects, processed_images, idx, url)
                
                print(f"✅ Processed test URL {idx} - added to pygame")
                
            except Exception as e:
                print(f"❌ Error processing test URL {idx}: {e}")
            
            finally:
                # Close tab and return to main
                driver.close()
                if len(driver.window_handles) > 0:
                    driver.switch_to.window(driver.window_handles[0])
        
        # Restore original settings
        VINTED_SHOW_ALL_LISTINGS = original_show_all
        bookmark_listings = original_bookmark
        
        print(f"✅ Test mode complete - processed {len(TEST_SUITABLE_URLS)} URLs, all added to pygame")



    # Add this new method to your VintedScraper class:
    def _simulate_buying_process_for_test(self, driver, driver_num, url):
        """
        Simulate the buying process for test mode when no actual listing is available
        This tests the buy button clicking logic without requiring a real purchasable item
        """
        print(f"🧪 SIMULATION: Starting simulated buying process for driver {driver_num}")
        
        try:
            # Open new tab
            driver.execute_script("window.open('');")
            new_tab = driver.window_handles[-1]
            driver.switch_to.window(new_tab)
            print(f"✅ SIMULATION: New tab opened")
            
            # Navigate to URL
            driver.get(url)
            print(f"✅ SIMULATION: Navigated to {url}")
            
            # Wait for page to load
            WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print(f"✅ SIMULATION: Page loaded")
            
            # Look for buy button (even if not clickable)
            buy_selectors = [
                'button[data-testid="item-buy-button"]',
                'button.web_ui__Button__button.web_ui__Button__filled.web_ui__Button__default.web_ui__Button__primary.web_ui__Button__truncated',
                '//button[@data-testid="item-buy-button"]',
                '//button[contains(@class, "web_ui__Button__primary")]//span[text()="Buy now"]'
            ]
            
            buy_button_found = False
            for selector in buy_selectors:
                try:
                    if selector.startswith('//'):
                        buy_button = driver.find_element(By.XPATH, selector)
                    else:
                        buy_button = driver.find_element(By.CSS_SELECTOR, selector)
                    
                    print(f"✅ SIMULATION: Found buy button with selector: {selector}")
                    buy_button_found = True
                    
                    # Try to click it (even if it fails, that's expected)
                    try:
                        buy_button.click()
                        print(f"✅ SIMULATION: Buy button clicked successfully")
                    except Exception as click_error:
                        print(f"⚠️ SIMULATION: Buy button click failed (expected): {click_error}")
                    
                    break
                    
                except NoSuchElementException:
                    continue
            
            if not buy_button_found:
                print(f"⚠️ SIMULATION: No buy button found (item may be sold/removed)")
                print(f"🧪 SIMULATION: Simulating buy button click anyway for test purposes...")
            
            # Simulate waiting for checkout page (even if it doesn't load)
            print(f"🧪 SIMULATION: Waiting for checkout page simulation...")
            time.sleep(2)
            
            # Look for pay button (simulate the buying logic)
            pay_selectors = [
                'button[data-testid="single-checkout-order-summary-purchase-button"]',
                'button[data-testid="single-checkout-order-summary-purchase-button"].web_ui__Button__primary',
            ]
            
            pay_button_found = False
            for selector in pay_selectors:
                try:
                    pay_button = driver.find_element(By.CSS_SELECTOR, selector)
                    print(f"✅ SIMULATION: Found pay button with selector: {selector}")
                    pay_button_found = True
                    
                    # Simulate clicking pay button multiple times (the actual buying logic)
                    for attempt in range(3):
                        print(f"🧪 SIMULATION: Simulated pay button click attempt {attempt + 1}")
                        try:
                            pay_button.click()
                            print(f"✅ SIMULATION: Pay button click attempt {attempt + 1} simulated")
                        except Exception as pay_click_error:
                            print(f"⚠️ SIMULATION: Pay button click {attempt + 1} failed (expected): {pay_click_error}")
                        
                        # Simulate the wait time between clicks
                        time.sleep(buying_driver_click_pay_wait_time)
                        
                    break
                    
                except NoSuchElementException:
                    continue
            
            if not pay_button_found:
                print(f"⚠️ SIMULATION: No pay button found (checkout page didn't load)")
                print(f"🧪 SIMULATION: This is expected behavior for test URLs without actual items")
            
            # Simulate completion
            print(f"✅ SIMULATION: Buying process simulation completed")
            print(f"🧪 SIMULATION: In real scenario, this would continue until purchase success/failure")
            
        except Exception as simulation_error:
            print(f"❌ SIMULATION ERROR: {simulation_error}")
        
        finally:
            # Clean up the tab
            try:
                driver.close()
                if len(driver.window_handles) > 0:
                    driver.switch_to.window(driver.window_handles[0])
                print(f"✅ SIMULATION: Cleanup completed")
            except Exception as cleanup_error:
                print(f"⚠️ SIMULATION CLEANUP: {cleanup_error}")
            
            # Release the driver
            self.release_driver(driver_num)
            print(f"✅ SIMULATION: Driver {driver_num} released")


    def run(self):
        global suitable_listings, current_listing_index, recent_listings, current_listing_title, current_listing_price
        global current_listing_description, current_listing_join_date, current_detected_items, current_profit
        global current_listing_images, current_listing_url, current_suitability, current_expected_revenue
        
        # NEW: Check for TEST_WHETHER_SUITABLE mode
        if TEST_WHETHER_SUITABLE:
            print("🧪 TEST_WHETHER_SUITABLE = True - Starting test suitable URLs mode")
            
            # Initialize ALL global variables including current_seller_reviews
            suitable_listings = []
            current_listing_index = 0
            recent_listings = {'listings': [], 'current_index': 0}
            
            # Initialize all current listing variables INCLUDING current_seller_reviews
            current_listing_title = "No title"
            current_listing_description = "No description" 
            current_listing_join_date = "No join date"
            current_listing_price = "0"
            current_expected_revenue = "0"
            current_profit = "0"
            current_detected_items = "None"
            current_listing_images = []
            current_listing_url = ""
            current_suitability = "Suitability unknown"
            current_seller_reviews = "No reviews yet"  # FIX: Initialize this variable
            
            # Initialize pygame display with default values
            self.update_listing_details("", "", "", "0", 0, 0, {}, [], {})
            
            # Setup driver with headless mode to reduce WebGL errors
            driver = self.setup_driver()
            
            try:
                # Start pygame FIRST so it's ready to display results
                print("🎮 Starting pygame window...")
                pygame_thread = threading.Thread(target=self.run_pygame_window)
                pygame_thread.daemon = True
                pygame_thread.start()
                
                # Give pygame time to initialize
                time.sleep(2)
                
                # Process the test URLs
                self.test_suitable_urls_mode(driver)
                
                # Keep pygame running to display results
                print("🎮 Pygame running - use arrow keys to navigate, ESC to exit")
                pygame_thread.join()  # Wait for pygame to finish
                
            except KeyboardInterrupt:
                print("\n🛑 Test mode stopped by user")
            finally:
                driver.quit()
                pygame.quit()
                print("✅ Driver closed, exiting")
                sys.exit(0)

        # NEW: Check for TEST_NUMBER_OF_LISTINGS mode
        if TEST_NUMBER_OF_LISTINGS:
            print("🧪 TEST_NUMBER_OF_LISTINGS = True - Starting URL collection mode")
            
            # Skip all the complex initialization, just setup basic driver
            driver = self.setup_driver()
            
            try:
                self.test_url_collection_mode(driver, SEARCH_QUERY)
            except KeyboardInterrupt:
                print("\n🛑 URL collection stopped by user")
            finally:
                driver.quit()
                print("✅ Driver closed, exiting")
                sys.exit(0)
        
        # NEW: TEST_BOOKMARK_BUYING_FUNCTIONALITY implementation
        if TEST_BOOKMARK_BUYING_FUNCTIONALITY:
            print("🔖💳 TEST_BOOKMARK_BUYING_FUNCTIONALITY ENABLED")
            print(f"🔗 URL: {TEST_BOOKMARK_BUYING_URL}")
                    
            # Start Flask app in separate thread.
            flask_thread = threading.Thread(target=self.run_flask_app)
            flask_thread.daemon = True
            flask_thread.start()
            
            # Skip all driver initialization, pygame, flask, etc.
            # Only run bookmark + buying process on the test URL
            try:
                print("🔖 STEP 1: Starting bookmark process...")
                
                # First, run the bookmark function
                # Extract username from the URL if possible or use a test username
                test_username = "test_user"  # You might want to make this configurable
                
                bookmark_success = self.bookmark_driver(TEST_BOOKMARK_BUYING_URL, test_username)
                
                if bookmark_success:
                    if wait_for_bookmark_stopwatch_to_buy:
                        print("✅ BOOKMARK: Successfully bookmarked the item")
                        print(f"⏱️ WAITING: Waiting {bookmark_stopwatch_length} seconds for bookmark timer...")
                        
                        # Wait for the full bookmark stopwatch duration
                        time.sleep(bookmark_stopwatch_length)
                        
                        print("✅ WAIT COMPLETE: Bookmark timer finished, starting buying process...")
                        
                    # Now start the buying process using process_single_listing_with_driver
                    driver_num, driver = self.get_available_driver()
                    
                    if driver is not None:
                        print(f"✅ BUYING: Got driver {driver_num}")
                        print("💳 STARTING: Buying process...")
                        
                        # MODIFIED: Use a simulation method when actual buying isn't possible
                        try:
                            self.process_single_listing_with_driver(TEST_BOOKMARK_BUYING_URL, driver_num, driver)
                        except Exception as buying_error:
                            print(f"⚠️ BUYING: Normal buying process failed: {buying_error}")
                            print("🧪 BUYING: Switching to test simulation mode...")
                            
                            # Simulate the buying process steps for testing
                            self._simulate_buying_process_for_test(driver, driver_num, TEST_BOOKMARK_BUYING_URL)
                        
                        print("✅ TEST COMPLETE: Bookmark + Buying process finished")
                    else:
                        print("❌ BUYING ERROR: Could not get available driver")
                        
                else:
                    print("❌ BOOKMARK FAILED: Could not bookmark the item, skipping buying process")
                    
            except Exception as e:
                print(f"❌ TEST ERROR: {e}")
                import traceback
                traceback.print_exc()
            finally:
                # Clean up all drivers
                self.cleanup_all_buying_drivers()
                self.cleanup_persistent_buying_driver()
                self.cleanup_persistent_bookmark_driver()
            
            # Exit immediately after test
            print("🔖💳 TEST_BOOKMARK_BUYING_FUNCTIONALITY COMPLETE - EXITING")
            sys.exit(0)
                
        if BOOKMARK_TEST_MODE:
            print("🧪 BOOKMARK TEST MODE ENABLED")
            print(f"🔗 URL: {BOOKMARK_TEST_URL}")
            print(f"👤 USERNAME: {BOOKMARK_TEST_USERNAME}")
            
            # Initialize all required global variables for proper operation
            suitable_listings = []
            current_listing_index = 0
            recent_listings = {'listings': [], 'current_index': 0}
            
            # Initialize all current listing variables
            current_listing_title = "No title"
            current_listing_description = "No description"
            current_listing_join_date = "No join date"
            current_listing_price = "0"
            current_expected_revenue = "0"
            current_profit = "0"
            current_detected_items = "None"
            current_listing_images = []
            current_listing_url = ""
            current_suitability = "Suitability unknown"
            current_seller_reviews = "No reviews yet"
            
            try:
                # Start the bookmark process
                success = self.bookmark_driver(BOOKMARK_TEST_URL, BOOKMARK_TEST_USERNAME)
                
                if success:
                    print("✅ BOOKMARK TEST SUCCESSFUL")
                    
                    # STAY ALIVE and wait for monitoring to complete
                    print("⏳ STAYING ALIVE: Waiting for monitoring thread to complete...")
                    
                    # Wait for the monitoring thread to finish
                    while self.monitoring_threads_active.is_set():
                        time.sleep(1)
                        print("🔍 MONITORING: Still active, waiting...")
                    
                    print("✅ MONITORING: Complete - all threads finished")
                    
                else:
                    print("❌ BOOKMARK TEST FAILED")
                
            except KeyboardInterrupt:
                print("\n🛑 BOOKMARK TEST: Stopped by user")
                # Force cleanup if user interrupts
                self.cleanup_all_cycling_bookmark_drivers()
            
            except Exception as e:
                print(f"❌ BOOKMARK TEST ERROR: {e}")
                import traceback
                traceback.print_exc()
            
            finally:
                # Final cleanup
                print("🧹 FINAL CLEANUP: Closing any remaining drivers...")
                self.cleanup_all_cycling_bookmark_drivers()
                self.cleanup_all_buying_drivers()
                self.cleanup_persistent_buying_driver()
                self.cleanup_persistent_bookmark_driver()
            
            # Only exit after monitoring is truly complete
            print("🧪 BOOKMARK TEST MODE COMPLETE - EXITING")
            sys.exit(0)

        if BUYING_TEST_MODE:
            print("💳 BUYING TEST MODE ENABLED")
            print(f"🔗 URL: {BUYING_TEST_URL}")
            
            # Skip all driver initialization, pygame, flask, etc.
            # Just run the buying functionality directly
            try:
                # Get an available driver (this will create one if needed)
                driver_num, driver = self.get_available_driver()
                
                if driver is not None:
                    print(f"✅ BUYING TEST: Got driver {driver_num}")
                    # Execute the purchase process using process_single_vinted_listing
                    self.process_single_listing_with_driver(BUYING_TEST_URL, driver_num, driver)
                    print("✅ BUYING TEST PROCESS COMPLETED")
                else:
                    print("❌ BUYING TEST: Could not get available driver")
                    
            except Exception as e:
                print(f"❌ BUYING TEST ERROR: {e}")
                import traceback
                traceback.print_exc()
            finally:
                # Clean up
                self.cleanup_all_buying_drivers()
                self.cleanup_persistent_buying_driver()
            
            # Exit immediately after test
            print("💳 BUYING TEST MODE COMPLETE - EXITING")
            sys.exit(0)
            
        # Initialize ALL global variables properly
        suitable_listings = []
        current_listing_index = 0
        
        # **CRITICAL FIX: Initialize recent_listings for website navigation**
        recent_listings = {
            'listings': [],
            'current_index': 0
        }
        
        # Initialize all current listing variables
        current_listing_title = "No title"
        current_listing_description = "No description"
        current_listing_join_date = "No join date"
        current_listing_price = "0"
        current_expected_revenue = "0"
        current_profit = "0"
        current_detected_items = "None"
        current_listing_images = []
        current_listing_url = ""
        current_suitability = "Suitability unknown"
        
        # Initialize pygame display with default values
        self.update_listing_details("", "", "", "0", 0, 0, {}, [], {})
        
        # Start Flask app in separate thread.
        flask_thread = threading.Thread(target=self.run_flask_app)
        flask_thread.daemon = True
        flask_thread.start()
        
        # Start pygame window in separate thread
        #pygame_thread = threading.Thread(target=self.run_pygame_window)
        #pygame_thread.start()
        
        # NEW: Start thread monitoring system


        
        # NEW: Main scraping driver thread - THIS IS THE KEY CHANGE
        def main_scraping_driver():
            """Main scraping driver function that runs in its own thread"""
            print("🚀 SCRAPING THREAD: Starting main scraping driver thread")
            
            # Clear download folder and start scraping
            self.clear_download_folder()
            driver = self.setup_driver()
            
            if driver is None:
                print("❌ SCRAPING THREAD: Failed to setup main driver")
                return
                
            try:
                print("🔍 SCRAPING THREAD: Setting up persistent buying driver...")
                self.setup_persistent_buying_driver()
                
                print("🚀 SCRAPING THREAD: Starting Vinted search with refresh...")
                self.search_vinted_with_refresh(driver, SEARCH_QUERY)
                
            except Exception as scraping_error:
                print(f"❌ SCRAPING THREAD ERROR: {scraping_error}")
                import traceback
                traceback.print_exc()
                
            finally:
                print("🧹 SCRAPING THREAD: Cleaning up...")
                try:
                    driver.quit()
                    print("✅ SCRAPING THREAD: Main driver closed")
                except:
                    print("⚠️ SCRAPING THREAD: Error closing main driver")
                    
                # Clean up all other drivers and resources
                pygame.quit()
                self.cleanup_persistent_buying_driver()
                self.cleanup_all_buying_drivers()
                self.cleanup_purchase_unsuccessful_monitoring()
                self.cleanup_all_cycling_bookmark_drivers()  # Clean up bookmark drivers too
                
                time.sleep(2)

                print("🏁 SCRAPING THREAD: Main scraping thread completed")
        
        # Create and start the main scraping thread
        print("🧵 MAIN: Creating main scraping driver thread...")
        scraping_thread = Thread(target=main_scraping_driver, name="Main-Scraping-Thread")
        scraping_thread.daemon = False  # Don't make it daemon so program waits for it
        scraping_thread.start()
        
        print("🧵 MAIN: Main scraping driver thread started")
        print("🧵 MAIN: Main thread will now wait for scraping thread to complete...")
        
        try:
            # Wait for the scraping thread to complete
            scraping_thread.join()
            print("✅ MAIN: Scraping thread completed successfully")
            
        except KeyboardInterrupt:
            print("\n🛑 MAIN: Keyboard interrupt received")
            print("🛑 MAIN: Setting shutdown event...")
            self.shutdown_event.set()
            
            print("⏳ MAIN: Waiting for scraping thread to finish...")
            scraping_thread.join(timeout=30)  # Wait up to 30 seconds
            
            if scraping_thread.is_alive():
                print("⚠️ MAIN: Scraping thread still alive after timeout")
            else:
                print("✅ MAIN: Scraping thread finished cleanly")
        
        except Exception as main_error:
            print(f"❌ MAIN THREAD ERROR: {main_error}")
            self.shutdown_event.set()
            
        finally:
            print("🏁 MAIN: Program ending, final cleanup...")
            # Force cleanup if anything is still running
            self.cleanup_all_buying_drivers()
            self.cleanup_persistent_buying_driver()
            self.cleanup_all_cycling_bookmark_drivers()
            self.cleanup_purchase_unsuccessful_monitoring()
            
            print("🏁 MAIN: Program exit")
            sys.exit(0)

if __name__ == "__main__":
    if VM_DRIVER_USE:
        print("VM_DRIVER_USE = True - Running VM driver script instead of main scraper")
        if not HAS_PYAUDIO:
            print("WARNING: pyaudiowpatch not available - audio features may not work")
            print("Install with: pip install PyAudioWPatch")
        main_vm_driver()
    else:
        print("VM_DRIVER_USE = False - Running main Vinted scraper")
        scraper = VintedScraper()
        globals()['vinted_scraper_instance'] = scraper
        scraper.run()