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
import threading
from threading import Lock
import time
from collections import defaultdict
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
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, WebDriverException
from scipy import signal
import wave
import ctypes

#uses custom url for buying in vm, for testing. works same as normal, just with custom url instead.

CLICK_PAY_BUTTON = False

VM_DRIVER_USE = True
google_login = True

VM_BOOKMARK_URLS = [
]

# tests whether the listing is suitable for buying based on URL rather than scanning
TEST_WHETHER_SUITABLE = False
TEST_SUITABLE_URLS = [
    'https://www.vinted.co.uk/items/7279764017-nintendo-switch-bundle?homepage_session_id=b016ee1d-ee4d-4e6e-b8f3-28476113364e',
    'https://www.vinted.co.uk/items/6963025596-nintendo-switch-oled-model-the-legend-of-zelda-tears-of-the-kingdom-edition?referrer=catalog',
    'https://www.vinted.co.uk/items/6970192196-nintendo-switch-lite-in-grey?referrer=catalog'
]

# tests the number of listings found by the search
TEST_NUMBER_OF_LISTINGS = False

PRICE_THRESHOLD = 30.0
OLED_PRICE_THRESHOLD = 50.0  # Higher threshold for OLED models  # Minimum price threshold - items below this won't detect Nintendo Switch classes
NINTENDO_SWITCH_CLASSES = [
    'controller','tv_black', 'switch_screen'
    'tv_white', 'comfort_h', 'lite', 'lite_box', 'lite_in_tv', 'oled', 'oled_box', 'oled_in_tv',
    'comfort_h_joy', 'switch_box', 'switch', 'switch_in_tv',
]


OLED_CLASSES = [
    'oled', 'oled_box', 'oled_in_tv'
]

VINTED_SHOW_ALL_LISTINGS = False
MIN_PRICE_FOR_CONSOLE_KEYWORD_DETECTION = 40.0  # Set to your desired minimum price
misc_games_cap = 5
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
listing_timers = {}
listing_timers_lock = Lock()
current_bookmark_status = "No bookmark attempted"
bookmark_stopwatch_start = None
test_purchase_not_true = False #uses the url below rather than the one from the web page
test_purchase_url = "https://www.vinted.co.uk/items/6963326227-nintendo-switch-1?referrer=catalog"
#sold listing: https://www.vinted.co.uk/items/6900159208-laptop-case
should_send_fail_bookmark_notification = True


current_item_confidences = {}  # NEW: Track confidence for each detected item
current_item_revenues = {}     # NEW: Track revenue for each detected item
current_listing_timestamps = {}  # NEW: Track timestamps for listing events

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

import pyaudiowpatch as pyaudio
HAS_PYAUDIO = True

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

GENERAL_CONFIDENCE_MIN = 0.6
HIGHER_CONFIDENCE_MIN = 0.65
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
MAX_LISTINGS_VINTED_TO_SCAN = 15  # Maximum listings to scan before refresh
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
   '1_2_switch': 10, 'animal_crossing': 24, 'arceus_p': 27.5, 'bow_z': 27, 'bros_deluxe_m': 24,
   'comfort_h': 5,
   'controller': 12, 'crash_sand': 9.5, 'diamond_p': 24, 'evee': 27.5, 'fifa_23': 7.5, 'fifa_24': 10,
   'gta': 22, 'just_dance': 6, 'kart_m': 22, 'kirby': 29, 'lets_go_p': 22, 'links_z': 25,
   'lite': 65, 'luigis': 18, 'mario_maker_2': 14.5, 'mario_sonic': 14.5, 'mario_tennis': 16.5,
   'minecraft': 13.5,
   'minecraft_dungeons': 11.5, 'minecraft_story': 48.5, 'miscellanious_sonic': 14, 'odyssey_m': 23.5,
   'oled': 120, 'other_mario': 20,
   'party_m': 24, 'rocket_league': 14.5, 'scarlet_p': 25.5, 'shield_p': 23, 'shining_p': 24.5,
   'skywards_z': 25,
   'smash_bros': 23.5, 'snap_p': 19, 'splatoon_2': 7.5, 'splatoon_3': 22, 'super_m_party': 20,
   'super_mario_3d': 42,
   'switch': 73.5, 'switch_sports': 19, 'sword_p': 21, 'tears_z': 28, 'tv_black': 17, 'tv_white': 23,
   'violet_p': 23.5
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

if VM_DRIVER_USE:
    
    # Try to import noisereduce for advanced noise reduction
    try:
        import noisereduce as nr
        HAS_NOISEREDUCE = True
        print("noisereduce available - enhanced noise reduction enabled")
    except ImportError:
        HAS_NOISEREDUCE = False
        print("noisereduce not available - install with: pip install noisereduce")
    

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

def send_keypress_with_hid_keyboard(key, hold_time=None):
    """
    Send keypress using HID Keyboard (replacement for PyAutoGUI)
    
    Args:
        key (str): Key to send ('0'-'9', 'right', 'left', etc.)
        hold_time (float): How long to hold the key
    
    Returns:
        bool: True if successful
    """
    try:
        # Initialize HID keyboard if not already done
        if not hasattr(send_keypress_with_hid_keyboard, 'hid_keyboard'):
            send_keypress_with_hid_keyboard.hid_keyboard = HIDKeyboard()
        
        # Add human-like delay before keystroke
        time.sleep(random.uniform(0.05, 0.15))
        
        # Send the key using HID keyboard
        success = send_keypress_with_hid_keyboard.hid_keyboard.send_key_press(key, hold_time)
        
        if success:
            # Optional additional delay after keystroke
            if not hold_time:
                time.sleep(random.uniform(0.05, 0.12))
            
            print(f"🎹 HID: Successfully pressed key '{key}'")
            return True
        else:
            print(f"❌ HID: Failed to press key '{key}'")
            return False
        
    except Exception as e:
        print(f"❌ HID: Keystroke failed for '{key}': {e}")
        return False

def input_captcha_solution_hid(self, sequence):
    """
    Input the 6-digit sequence into the captcha form using HID keyboard
    This generates true OS-level keystrokes indistinguishable from real keyboard input
    """
    if not self.driver or not sequence or len(sequence) != 6:
        print("Cannot input solution: missing driver or invalid sequence")
        return False
    
    print(f"🎹 HID: Starting to input captcha solution: {sequence}")
    
    try:
        # Initialize HID keyboard
        hid_keyboard = HIDKeyboard()
        
        # Navigate to the correct iframe (same iframe logic as before)
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
        
        print("🎹 HID: Starting to input digits using OS-level keyboard events...")
        
        # Click on the first input field to focus it (using Selenium for positioning)
        time.sleep(random.uniform(0.5, 1.0))
        
        # Scroll into view
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", first_input)
        time.sleep(random.uniform(0.3, 0.6))

        # Click with ActionChains to focus the field
        from selenium.webdriver.common.action_chains import ActionChains
        action = ActionChains(self.driver)

        offset_x = random.randint(-2, 2)
        offset_y = random.randint(-2, 2)

        action.move_to_element_with_offset(first_input, offset_x, offset_y)
        time.sleep(random.uniform(0.2, 0.4))
        action.move_to_element(first_input)
        time.sleep(random.uniform(0.1, 0.3))
        action.click().perform()
        
        print("🎹 HID: Clicked on first input field, now sending HID keystrokes...")

        # Input each digit using HID keyboard (TRUE OS-LEVEL KEYSTROKES)
        for i, digit in enumerate(sequence):
            print(f"🎹 HID: Inputting digit {i+1}: {digit}")
            
            # Special handling for '1' digit as in original code
            if digit == '1':
                time.sleep(2.3)
            
            # Random delay before typing (human-like)
            time.sleep(random.uniform(0.2, 0.6))
            
            # Send the digit using HID keyboard (OS-LEVEL)
            success = hid_keyboard.send_key_press(digit)
            
            if success:
                print(f"✅ HID: Successfully sent OS-level keystroke for digit: {digit}")
            else:
                print(f"❌ HID: Failed to send OS-level keystroke for digit: {digit}")
                # Continue anyway - partial input might still work
            
            time.sleep(random.uniform(0.3, 0.4))
            
            # If not the last digit, move to next field with HID arrow key
            if i < len(sequence) - 1:
                time.sleep(random.uniform(0.2, 0.6))
                
                # Use HID keyboard for RIGHT arrow key (OS-LEVEL)
                arrow_success = hid_keyboard.send_navigation_key('right')
                
                if arrow_success:
                    print(f"✅ HID: Successfully sent OS-level RIGHT arrow key")
                else:
                    print(f"❌ HID: Failed to send OS-level RIGHT arrow key")
                    # Try TAB as backup
                    tab_success = hid_keyboard.send_navigation_key('tab')
                    if tab_success:
                        print(f"✅ HID: Successfully sent OS-level TAB key as backup")
                    else:
                        print(f"❌ HID: Both RIGHT and TAB keys failed")
                
                time.sleep(random.uniform(0.05, 0.25))

        print("🎹 HID: All digits entered using OS-level keystrokes!")
            
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
            
            print("✅ HID: Successfully clicked Verify button!")
            
            # Wait to see the result
            time.sleep(random.uniform(2.0, 4.0))
            
            self.driver.switch_to.default_content()
            return True
            
        else:
            print("Could not find Verify button")
            self.driver.switch_to.default_content()
            return False
            
    except Exception as e:
        print(f"❌ HID: Error inputting captcha solution: {e}")
        import traceback
        traceback.print_exc()
        try:
            self.driver.switch_to.default_content()
        except:
            pass
        return False


# Integration helper function for your existing code
def replace_pyautogui_with_hid():
    """
    Helper function to replace PyAutoGUI calls with HID keyboard
    Call this to patch your existing send_keypress_with_pyautogui function
    """
    global send_keypress_with_pyautogui
    send_keypress_with_pyautogui = send_keypress_with_hid_keyboard
    print("✅ Replaced PyAutoGUI with HID Keyboard implementation")


def start_listing_timer(url):
    """
    Thread-safe function to start timing a listing
    Args:
        url (str): The listing URL to track
    Returns:
        float: The start timestamp
    """
    with listing_timers_lock:
        start_time = time.time()
        listing_timers[url] = {
            'start_time': start_time,
            'end_time': None,
            'duration': None,
            'stage': 'started'
        }
        print(f"⏱️ TIMER START: {url[:50]}... at {time.strftime('%H:%M:%S', time.localtime(start_time))}")
        return start_time

def stop_listing_timer(url, stage='completed'):
    """
    Thread-safe function to stop timing a listing
    Args:
        url (str): The listing URL to track
        stage (str): The stage at which timing stopped (e.g., 'pay_clicked', 'failed')
    Returns:
        float: The duration in seconds, or None if timer wasn't started
    """
    with listing_timers_lock:
        if url not in listing_timers:
            print(f"⚠️ TIMER WARNING: No timer found for {url[:50]}...")
            return None
        
        end_time = time.time()
        start_time = listing_timers[url]['start_time']
        duration = end_time - start_time
        
        listing_timers[url]['end_time'] = end_time
        listing_timers[url]['duration'] = duration
        listing_timers[url]['stage'] = stage
        
        print(f"⏱️ TIMER STOP: {url[:50]}...")
        print(f"⏱️ TIMER DURATION: {duration:.3f} seconds ({duration:.2f}s)")
        print(f"⏱️ TIMER STAGE: {stage}")
        
        return duration

def get_listing_timer(url):
    """
    Thread-safe function to get timer info for a listing
    Args:
        url (str): The listing URL
    Returns:
        dict: Timer information or None if not found
    """
    with listing_timers_lock:
        return listing_timers.get(url, None)

def get_elapsed_time(url):
    """
    Thread-safe function to get elapsed time for a listing (even if not stopped)
    Args:
        url (str): The listing URL
    Returns:
        float: Elapsed time in seconds, or None if timer not started
    """
    with listing_timers_lock:
        if url not in listing_timers:
            return None
        
        start_time = listing_timers[url]['start_time']
        
        if listing_timers[url]['end_time']:
            # Timer already stopped
            return listing_timers[url]['duration']
        else:
            # Timer still running
            return time.time() - start_time

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
        
        # CRITICAL FIX: Prevent session timeout
        chrome_options.add_argument('--disable-background-timer-throttling')
        chrome_options.add_argument('--disable-renderer-backgrounding')
        chrome_options.add_argument('--disable-backgrounding-occluded-windows')
        chrome_options.add_argument('--disable-ipc-flooding-protection')
        chrome_options.add_argument('--memory-pressure-off')
        
        # Modern Selenium 4+ approach - set capabilities directly on ChromeOptions
        # Set only valid Selenium Grid timeout capabilities
        chrome_options.set_capability('se:idleTimeout', 0)        # No idle timeout (infinite)
        chrome_options.set_capability('se:sessionTimeout', 0)     # No session timeout (infinite)
        
        print(f"Chrome options configured: {len(chrome_options.arguments)} arguments")
        print(f"INFINITE SESSION: Grid timeouts set to 0 (never expires)")
        
        driver = None
        
        try:
            print("Attempting to connect to remote WebDriver...")
            
            driver = webdriver.Remote(
                command_executor=f'http://{vm_ip_address}:4444',
                options=chrome_options
            )
            
            print(f"✓ Successfully created remote WebDriver connection")
            print(f"Session ID: {driver.session_id}")
            
            # Set client-side timeouts after session creation
            try:
                driver.implicitly_wait(0)  # No implicit wait
                driver.set_page_load_timeout(300)  # 5 minutes page load timeout
                driver.set_script_timeout(30)  # 30 seconds script timeout
                print("✓ Client-side timeouts configured")
            except Exception as timeout_error:
                print(f"Warning: Could not set client timeouts: {timeout_error}")
            
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
        
        # Chrome options for the VM instance
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
        
        # CRITICAL FIX: Prevent session timeout
        chrome_options.add_argument('--disable-background-timer-throttling')
        chrome_options.add_argument('--disable-renderer-backgrounding')
        chrome_options.add_argument('--disable-backgrounding-occluded-windows')
        chrome_options.add_argument('--disable-ipc-flooding-protection')
        chrome_options.add_argument('--memory-pressure-off')
        
        # Modern Selenium 4+ approach - set capabilities directly on ChromeOptions
        # Set only valid Selenium Grid timeout capabilities
        chrome_options.set_capability('se:idleTimeout', 0)        # No idle timeout (infinite)
        chrome_options.set_capability('se:sessionTimeout', 0)     # No session timeout (infinite)
        
        print(f"Chrome options configured: {len(chrome_options.arguments)} arguments")
        print(f"INFINITE SESSION: Grid timeouts set to 0 (never expires)")
        
        driver = None
        
        try:
            print("Attempting to connect to remote WebDriver...")
            
            # Modern Selenium 4+ approach - use options only
            driver = webdriver.Remote(
                command_executor=f'http://{vm_ip_address}:4444',
                options=chrome_options
            )
            
            print(f"✓ Successfully created remote WebDriver connection")
            print(f"Session ID: {driver.session_id}")
            
            # Set client-side timeouts after session creation
            try:
                driver.implicitly_wait(0)  # No implicit wait
                driver.set_page_load_timeout(300)  # 5 minutes page load timeout
                driver.set_script_timeout(30)  # 30 seconds script timeout
                print("✓ Client-side timeouts configured")
            except Exception as timeout_error:
                print(f"Warning: Could not set client timeouts: {timeout_error}")
            
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

# 3. New function to execute bookmark process for VM drivers
def execute_vm_bookmark_process(driver, url, driver_number):
    """
    Execute the bookmark process for a VM driver using existing bookmark logic
    """
    try:
        print(f"🔖 DRIVER {driver_number}: Starting bookmark execution...")
        
        # Extract username from the URL if possible (simplified for VM use)
        # You might want to enhance this to actually scrape the username
        username = f"vm_user_{driver_number}"  # Placeholder - could be enhanced
        
        # Use the existing bookmark logic structure
        step_log = {
            'start_time': time.time(),
            'driver_number': driver_number,
            'steps_completed': [],
            'failures': [],
            'success': False,
            'critical_sequence_completed': False,
            'actual_url': url
        }
        
        # Execute the main bookmark sequences using existing logic
        # Pass vinted_scraper_instance for timestamp tracking
        scraper_instance = globals().get('vinted_scraper_instance', None)
        success = execute_vm_bookmark_sequences(driver, url, username, step_log, scraper_instance)        
        if success:
            step_log['success'] = True
            print(f"✅ DRIVER {driver_number}: Bookmark process completed successfully")
        else:
            print(f"❌ DRIVER {driver_number}: Bookmark process failed")
        
        # Log final results
        total_time = time.time() - step_log['start_time']
        print(f"📊 DRIVER {driver_number} BOOKMARK ANALYSIS:")
        print(f"⏱️  Total time: {total_time:.2f}s")
        print(f"✅ Steps completed: {len(step_log['steps_completed'])}")
        print(f"❌ Failures: {len(step_log['failures'])}")
        print(f"🎯 Critical sequence: {'YES' if step_log['critical_sequence_completed'] else 'NO'}")
        print(f"🏆 Overall success: {'YES' if step_log['success'] else 'NO'}")
        
        return success
        
    except Exception as e:
        print(f"❌ DRIVER {driver_number}: Bookmark execution error: {e}")
        return False

# 4. VM-specific bookmark sequences (adapted from existing VintedScraper methods)
def execute_vm_bookmark_sequences(driver, listing_url, username, step_log, scraper_instance=None):
    """
    Execute bookmark sequences - FIXED argument count
    """
    try:
        print(f"🔖 DRIVER {step_log['driver_number']}: Creating new tab...")
        driver.execute_script("window.open('');")
        new_tab = driver.window_handles[-1]
        driver.switch_to.window(new_tab)
        
        print(f"🔖 DRIVER {step_log['driver_number']}: Navigating to listing...")
        driver.get(listing_url)
        
        # FIXED: Only pass 2 arguments (driver, step_log)
        success = execute_vm_first_buy_sequence(driver, step_log)
        
        if success:
            print(f"🔖 DRIVER {step_log['driver_number']}: Sequence completed")
            return True
        else:
            print(f"🔖 DRIVER {step_log['driver_number']}: Sequence failed")
            return False
            
    except Exception as e:
        print(f"❌ DRIVER {step_log['driver_number']}: Error: {e}")
        return False
    finally:
        try:
            if len(driver.window_handles) > 1:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
        except:
            pass

def execute_vm_first_buy_sequence(driver, step_log):
    """
    Execute first buy sequence for VM driver using JavaScript-first approach
    """
    return execute_vm_first_buy_sequence_with_shadow_dom(driver, step_log)



# 5. VM-specific first buy sequence (using EXACT main program logic)
def execute_vm_first_buy_sequence_with_shadow_dom(driver, step_log, scraper_instance=None):    
    """
    Modified first buy sequence - JavaScript-first clicking
    """
    try:
        print(f"🔖 JAVASCRIPT-FIRST: Looking for Buy now button...")
        
        # Use the new JavaScript-first buy button finder (already clicks the button)
        buy_button, buy_selector = find_buy_button_with_shadow_dom(driver)
        
        if not buy_button:
            print(f"❌ JAVASCRIPT-FIRST: Buy button not found - item likely sold")
            return False
        
        print(f"✅ JAVASCRIPT-FIRST: Buy button found and clicked using: {buy_selector}")
        step_log['steps_completed'].append(f"javascript_first_buy_button_clicked - {time.time() - step_log['start_time']:.2f}s")
        # TIMESTAMP: Record when buy button was clicked
        if scraper_instance and 'actual_url' in step_log:
            scraper_instance.record_listing_timestamp(step_log['actual_url'], 'buy_clicked')
        
        # Wait for pay button to appear using existing logic
        print(f"💳 JAVASCRIPT-FIRST: Waiting for pay button...")
        
        pay_button, pay_selector = vm_try_selectors(
            driver,
            'pay_button',
            operation='find',
            timeout=15,
            step_log=step_log
        )
        
        if not pay_button:
            print(f"❌ JAVASCRIPT-FIRST: Pay button not found")
            return False
        
        print(f"✅ JAVASCRIPT-FIRST: Pay button found using: {pay_selector[:30]}...")
        step_log['steps_completed'].append(f"javascript_first_pay_button_found - {time.time() - step_log['start_time']:.2f}s")
        
        # Handle shipping options (same as main scraper)
        handle_vm_shipping_options(driver, step_log, scraper_instance)    
        # Execute critical pay sequence (same timing as main scraper)
        return execute_vm_critical_pay_sequence(driver, pay_button, step_log, scraper_instance)        
    except Exception as e:
        print(f"❌ JAVASCRIPT-FIRST: First buy sequence error: {e}")
        return False



# NEW: Add the EXACT selector system from main program
def vm_try_selectors(driver, selector_set_name, operation='find', timeout=5, click_method='standard', step_log=None):
    """
    EXACT same selector logic as main program's _try_selectors method
    """
    # EXACT same selector sets as main program
    SELECTOR_SETS = {
        'buy_button': [
            'button[data-testid="item-buy-button"]',
            'button[data-testid="item-buy-button"].web_ui__Button__primary',
            'button.web_ui__Button__button.web_ui__Button__filled.web_ui__Button__default.web_ui__Button__primary.web_ui__Button__truncated',
            'button.web_ui__Button__button[data-testid="item-buy-button"]',
            '//button[@data-testid="item-buy-button"]',
            '//button[contains(@class, "web_ui__Button__primary")]//span[text()="Buy now"]',
            '//span[text()="Buy now"]/parent::button',
            'button[class*="web_ui__Button"][class*="primary"]',
            '//button[contains(@class, "web_ui__Button")]//span[contains(text(), "Buy")]'
        ],
        'pay_button': [
            'button[data-testid="single-checkout-order-summary-purchase-button"]',
            'button[data-testid="single-checkout-order-summary-purchase-button"].web_ui__Button__primary',
            '//button[@data-testid="single-checkout-order-summary-purchase-button"]',
            'button.web_ui__Button__primary[data-testid*="purchase"]',
            '//button[contains(@data-testid, "purchase-button")]',
            '//button[contains(@class, "web_ui__Button__primary")]',
            'button[class*="web_ui__Button"][class*="primary"][data-testid*="purchase"]'
        ],
        'processing_payment': [
            "//h2[@class='web_ui__Text__text web_ui__Text__title web_ui__Text__left' and text()='Processing payment']",
            "//h2[contains(@class, 'web_ui__Text__title') and text()='Processing payment']",
            "//span[@class='web_ui__Text__text web_ui__Text__body web_ui__Text__left web_ui__Text__format' and contains(text(), \"We've reserved this item for you until your payment finishes processing\")]",
            "//span[contains(text(), \"We've reserved this item for you until your payment finishes processing\")]",
            "//*[contains(text(), 'Processing payment')]"
        ]
    }
    
    selectors = SELECTOR_SETS.get(selector_set_name, [])
    if not selectors:
        if step_log:
            vm_log_step(step_log, f"no_selectors_{selector_set_name}", False, "No selectors defined")
        return None, None
    
    for i, selector in enumerate(selectors):
        try:
            if step_log and print_debug:
                print(f"🔍 DRIVER {step_log['driver_number']}: Trying selector {i+1}/{len(selectors)} for {selector_set_name}")
            
            # Use appropriate locator strategy (EXACT same as main program)
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
            
            # If we need to click, use EXACT same click methods as main program
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
                        
                        if step_log:
                            vm_log_step(step_log, f"click_{selector_set_name}_{method}", True)
                        break
                    except Exception as click_error:
                        if step_log:
                            vm_log_step(step_log, f"click_{selector_set_name}_{method}_attempt", False, str(click_error))
                        continue
                else:
                    continue  # All click methods failed, try next selector
            
            if step_log:
                vm_log_step(step_log, f"selector_{selector_set_name}_success", True, f"Used #{i+1}: {selector[:30]}...")
            return element, selector
            
        except TimeoutException:
            if step_log:
                vm_log_step(step_log, f"selector_{selector_set_name}_{i+1}_timeout", False, f"Timeout after {timeout}s")
            continue
        except Exception as e:
            if step_log:
                vm_log_step(step_log, f"selector_{selector_set_name}_{i+1}_error", False, str(e)[:100])
            continue
    
    if step_log:
        vm_log_step(step_log, f"all_selectors_{selector_set_name}_failed", False, f"All {len(selectors)} selectors failed")
    return None, None

# NEW: Add the EXACT logging function from main program
def vm_log_step(step_log, step_name, success=True, error_msg=None):
    """EXACT same logging logic as main program's _log_step method"""
    if success:
        step_log['steps_completed'].append(f"{step_name} - {time.time() - step_log['start_time']:.2f}s")
        print(f"✅ DRIVER {step_log['driver_number']}: {step_name}")
    else:
        step_log['failures'].append(f"{step_name}: {error_msg} - {time.time() - step_log['start_time']:.2f}s")
        print(f"❌ DRIVER {step_log['driver_number']}: {step_name} - {error_msg}")

# 6. VM-specific shipping options handler
def handle_vm_shipping_options(driver, step_log, scraper_instance=None):
    """
    Handle shipping options for VM driver (adapted from main scraper)
    """
    try:
        print(f"🚢 DRIVER {step_log['driver_number']}: Checking shipping options...")
        
        # Check if "Ship to pick-up point" is selected
        try:
            pickup_element = driver.find_element(
                By.XPATH, 
                '//div[@data-testid="delivery-option-pickup" and @aria-checked="true"]'
            )
            print(f"📦 DRIVER {step_log['driver_number']}: Pickup point selected")
            
            # Check for "Choose a pick-up point" message
            try:
                
                print(f"🏠 DRIVER {step_log['driver_number']}: Switching to Ship to home...")
                
                # Click "Ship to home"
                # Click "Ship to home"
                ship_home = driver.find_element(
                    By.XPATH,
                    '//h2[@class="web_ui__Text__text web_ui__Text__title web_ui__Text__left" and text()="Ship to home"]'
                )
                ship_home.click()

                print(f"✅ DRIVER {step_log['driver_number']}: Switched to Ship to home, waiting 3 seconds...")
                # TIMESTAMP: Record when ship to home was clicked
                if scraper_instance and 'actual_url' in step_log:
                    scraper_instance.record_listing_timestamp(step_log['actual_url'], 'ship_to_home_clicked')

                # TIMESTAMP: Record ship to home click (need scraper instance passed through)
                # This will be handled in Step 7B

                time.sleep(3)
            except:
                print(f"✅ DRIVER {step_log['driver_number']}: Pickup point ready")
                
        except:
            print(f"✅ DRIVER {step_log['driver_number']}: Ship to home already selected")
            
    except Exception as e:
        print(f"⚠️ DRIVER {step_log['driver_number']}: Shipping options error: {e}")

# 7. VM-specific critical pay sequence (EXACT same timing as main scraper)
def execute_vm_critical_pay_sequence(driver, pay_button, step_log, scraper_instance=None):
    """
    MODIFIED: Now stops the timer when pay button is clicked
    Execute critical pay sequence with EXACT same timing as main scraper
    """
    try:
        print(f"💳 DRIVER {step_log['driver_number']}: Executing critical pay sequence...")
        
        # Get the URL from step_log to track timer
        listing_url = step_log.get('actual_url', None)
        # Get URL from step_log for timestamp tracking
        listing_url = step_log.get('actual_url', None)
        
        # Click pay button using multiple methods (same as main scraper)
        pay_clicked = False
        
        # Method 1: Direct click
        try:
            if not VINTED_SHOW_ALL_LISTINGS:
                if CLICK_PAY_BUTTON:
                    print('1')
                    pay_button.click()
            pay_clicked = True
            # TIMESTAMP: Record when pay button was clicked (direct method)
            if scraper_instance and 'actual_url' in step_log:
                scraper_instance.record_listing_timestamp(step_log['actual_url'], 'pay_clicked')

            print(f"✅ DRIVER {step_log['driver_number']}: Pay button clicked (direct)")
        except:
            # Method 2: JavaScript click
            try:
                if not VINTED_SHOW_ALL_LISTINGS:
                    if CLICK_PAY_BUTTON:
                        print('1')
                        driver.execute_script("arguments[0].click();", pay_button)
                pay_clicked = True
                # TIMESTAMP: Record when pay button was clicked (JavaScript method)
                if scraper_instance and 'actual_url' in step_log:
                    scraper_instance.record_listing_timestamp(step_log['actual_url'], 'pay_clicked')
                print(f"✅ DRIVER {step_log['driver_number']}: Pay button clicked (JavaScript)")
            except:
                # Method 3: Force enable and click
                try:
                    if not VINTED_SHOW_ALL_LISTINGS:
                        if CLICK_PAY_BUTTON:
                            print('1')
                            driver.execute_script("""
                                arguments[0].disabled = false;
                                arguments[0].click();
                            """, pay_button)
                    pay_clicked = True
                    # TIMESTAMP: Record when pay button was clicked (force method)
                    if scraper_instance and 'actual_url' in step_log:
                        scraper_instance.record_listing_timestamp(step_log['actual_url'], 'pay_clicked')
                    print(f"✅ DRIVER {step_log['driver_number']}: Pay button clicked (force)")
                except Exception as final_error:
                    print(f"❌ DRIVER {step_log['driver_number']}: All pay click methods failed")
                    # Stop timer on failure
                    if listing_url:
                        stop_listing_timer(listing_url, stage='pay_click_failed')
                    return False
        
        # ============================================================================
        # NEW: STOP TIMER IMMEDIATELY AFTER PAY BUTTON IS CLICKED
        # ============================================================================
        if pay_clicked and listing_url:
            duration = stop_listing_timer(listing_url, stage='pay_button_clicked')
            if duration:
                print(f"🎯 TIMER RESULT: Total time from suitable detection to pay click: {duration:.3f} seconds")
                print(f"🎯 TIMER BREAKDOWN:")
                print(f"   • Listing marked suitable → Pay button clicked")
                print(f"   • Duration: {duration:.2f}s")
        
        # CRITICAL: Exact 0.25 second wait (same as main scraper)
        print(f"🔖 DRIVER {step_log['driver_number']}: CRITICAL - Waiting exactly seconds...")
        time.sleep(2.5)
        
        # [Rest of existing code continues unchanged...]
        
        # NEW: Wait for "Purchase successful" detection before closing tab
        print(f"🔍 DRIVER {step_log['driver_number']}: Searching for 'Purchase successful' message...")
        
        purchase_successful = False
        start_time = time.time()
        timeout = 15
        
        while (time.time() - start_time) < timeout:
            try:
                # Method 1: Use the data-testid selector (most reliable)
                success_element = driver.find_element(
                    By.CSS_SELECTOR, 
                    'div[data-testid="conversation-message--status-message--title"] h2'
                )
                
                if success_element and success_element.text == "Purchase successful":
                    purchase_successful = True
                    print(f"✅ DRIVER {step_log['driver_number']}: Purchase successful message found!")
                    break
                    
            except:
                try:
                    # Method 2: Use the corrected h2 selector (without the muted class)
                    success_element = driver.find_element(
                        By.CSS_SELECTOR, 
                        'h2.web_ui__Text__text.web_ui__Text__title.web_ui__Text__left'
                    )
                    
                    if success_element and success_element.text == "Purchase successful":
                        purchase_successful = True
                        print(f"✅ DRIVER {step_log['driver_number']}: Purchase successful message found!")
                        break
                        
                except:
                    try:
                        # Method 3: Use XPath for more flexibility
                        success_element = driver.find_element(
                            By.XPATH, 
                            "//h2[text()='Purchase successful']"
                        )
                        
                        if success_element:
                            purchase_successful = True
                            print(f"✅ DRIVER {step_log['driver_number']}: Purchase successful message found!")
                            break
                            
                    except:
                        # No element found yet, continue waiting
                        pass
            
            # Wait 0.1 seconds before checking again
            time.sleep(0.1)
        
        # Print result based on what was found
        if purchase_successful:
            print(f"🎉 DRIVER {step_log['driver_number']}: SUCCESSFUL - Purchase successful message detected!")
        else:
            print(f"⚠️ DRIVER {step_log['driver_number']}: UNSUCCESSFUL - Purchase successful message not found within 15 seconds")
        
        # CRITICAL: Immediate tab close (same as main scraper)
        print(f"🔖 DRIVER {step_log['driver_number']}: CRITICAL - Closing tab immediately...")
        driver.close()
        
        step_log['critical_sequence_completed'] = True
        
        # Switch back to main tab
        if len(driver.window_handles) > 0:
            driver.switch_to.window(driver.window_handles[0])
        
        elapsed = time.time() - step_log['start_time']
        print(f"⏱️ DRIVER {step_log['driver_number']}: Critical sequence completed in {elapsed:.3f} seconds")
        
        return True
        
    except Exception as e:
        print(f"❌ DRIVER {step_log['driver_number']}: Critical pay sequence error: {e}")
        # Stop timer on exception
        if listing_url:
            stop_listing_timer(listing_url, stage='exception')
        return False


# Additional selector sets needed for the vm_try_selectors function
VM_SELECTOR_SETS = {
    'processing_payment': [
        "//h2[@class='web_ui__Text__text web_ui__Text__title web_ui__Text__left' and text()='Processing payment']",
        "//h2[contains(@class, 'web_ui__Text__title') and text()='Processing payment']",
        "//span[@class='web_ui__Text__text web_ui__Text__body web_ui__Text__left web_ui__Text__format' and contains(text(), \"We've reserved this item for you until your payment finishes processing\")]",
        "//span[contains(text(), \"We've reserved this item for you until your payment finishes processing\")]",
        "//*[contains(text(), 'Processing payment')]"
    ]
}

def clear_browser_data_universal(vm_ip_address, config):
    """
    Universal function to clear browser data for any driver configuration
    """
    print("=" * 50)
    print(f"CLEARING BROWSER DATA FOR {config['user_data_dir']}...")
    print("=" * 50)
    
    clear_driver = None
    
    try:
        print("Step 1: Setting up temporary driver for data clearing...")
        
        # Use universal Chrome options
        chrome_options = ChromeOptions()
        chrome_options.add_argument(f"--user-data-dir={config['user_data_dir']}")
        chrome_options.add_argument(f"--profile-directory={config['profile']}")
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--force-device-scale-factor=1')
        chrome_options.add_argument('--high-dpi-support=1')
        chrome_options.add_argument(f"--remote-debugging-port={config['port']}")
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

def setup_driver_universal(vm_ip_address, config):
    """Universal setup function for any driver configuration"""
    
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
    
    # Chrome options for the VM instance
    chrome_options = ChromeOptions()
    chrome_options.add_argument(f"--user-data-dir={config['user_data_dir']}")
    chrome_options.add_argument(f"--profile-directory={config['profile']}")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # VM-specific optimizations
    chrome_options.add_argument('--force-device-scale-factor=1')
    chrome_options.add_argument('--high-dpi-support=1')
    chrome_options.add_argument(f"--remote-debugging-port={config['port']}")
    chrome_options.add_argument('--remote-allow-origins=*')
    chrome_options.add_argument('--disable-features=VizDisplayCompositor')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--start-maximized")
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

def find_buy_button_with_shadow_dom(driver):
    """
    Enhanced buy now button finder - JavaScript click first approach
    Finds button and immediately clicks with JavaScript for reliability
    """
    print("🔍 SHADOW DOM: Starting buy button search with JavaScript-first approach...")
    
    # Method 1: Find button and immediately click with JavaScript
    print("⚡ JAVASCRIPT-FIRST: Finding and clicking buy button with JavaScript...")
    buy_selectors = [
        'button[data-testid="item-buy-button"]',
        'button.web_ui__Button__button.web_ui__Button__filled.web_ui__Button__default.web_ui__Button__primary.web_ui__Button__truncated',
        '//button[@data-testid="item-buy-button"]',
        '//button[contains(@class, "web_ui__Button__primary")]//span[text()="Buy now"]',
        '//span[text()="Buy now"]/parent::button'
    ]
    
    for selector in buy_selectors:
        try:
            if selector.startswith('//'):
                buy_button = driver.find_element(By.XPATH, selector)
            else:
                buy_button = driver.find_element(By.CSS_SELECTOR, selector)
            
            print(f"✅ FOUND: Buy button with: {selector}")
            
            # IMMEDIATELY click with JavaScript - no other methods tried
            try:
                driver.execute_script("arguments[0].click();", buy_button)
                print(f"✅ JAVASCRIPT-FIRST: Buy button clicked immediately with JavaScript")
                return buy_button, selector
            except Exception as js_error:
                print(f"❌ JAVASCRIPT-FIRST: JavaScript click failed: {js_error}")
                continue
                
        except:
            continue
    
    # Method 2: Shadow DOM traversal using JavaScript
    print("🌊 SHADOW DOM: Standard selectors failed, trying Shadow DOM traversal...")
    
    shadow_dom_script = """
    function findBuyButtonInShadowDOM() {
        // Function to recursively search through shadow roots
        function searchInShadowRoot(element) {
            if (!element) return null;
            
            // Check if this element has a shadow root
            if (element.shadowRoot) {
                // Search within the shadow root
                let shadowButton = element.shadowRoot.querySelector('button[data-testid="item-buy-button"]');
                if (shadowButton) {
                    console.log('Found buy button in shadow root of:', element.tagName);
                    return shadowButton;
                }
                
                // Try other selectors in shadow root
                let shadowButtonAlt = element.shadowRoot.querySelector('button.web_ui__Button__primary');
                if (shadowButtonAlt) {
                    let span = shadowButtonAlt.querySelector('span');
                    if (span && span.textContent.includes('Buy now')) {
                        console.log('Found buy button (alternative) in shadow root of:', element.tagName);
                        return shadowButtonAlt;
                    }
                }
                
                // Recursively search child elements in shadow root
                let shadowChildren = element.shadowRoot.querySelectorAll('*');
                for (let child of shadowChildren) {
                    let result = searchInShadowRoot(child);
                    if (result) return result;
                }
            }
            
            return null;
        }
        
        // Search all elements in the main document
        let allElements = document.querySelectorAll('*');
        for (let element of allElements) {
            let result = searchInShadowRoot(element);
            if (result) {
                return result;
            }
        }
        
        return null;
    }
    
    return findBuyButtonInShadowDOM();
    """
    
    try:
        shadow_button = driver.execute_script(shadow_dom_script)
        if shadow_button:
            print("✅ SHADOW DOM: Found buy button via Shadow DOM traversal!")
            return shadow_button, "shadow_dom_traversal"
    except Exception as e:
        print(f"❌ SHADOW DOM: Shadow DOM search failed: {e}")
    
    # Method 3: Alternative Shadow DOM approach - search by text content
    print("🔍 SHADOW DOM: Trying text-based Shadow DOM search...")
    
    text_based_script = """
    function findBuyButtonByText() {
        function searchForBuyNowText(element) {
            if (!element) return null;
            
            // Check shadow root
            if (element.shadowRoot) {
                // Look for any button with "Buy now" text in shadow root
                let buttons = element.shadowRoot.querySelectorAll('button');
                for (let button of buttons) {
                    if (button.textContent && button.textContent.includes('Buy now')) {
                        console.log('Found "Buy now" button in shadow root via text search');
                        return button;
                    }
                }
                
                // Recursively search in shadow root
                let shadowChildren = element.shadowRoot.querySelectorAll('*');
                for (let child of shadowChildren) {
                    let result = searchForBuyNowText(child);
                    if (result) return result;
                }
            }
            
            return null;
        }
        
        let allElements = document.querySelectorAll('*');
        for (let element of allElements) {
            let result = searchForBuyNowText(element);
            if (result) return result;
        }
        
        return null;
    }
    
    return findBuyButtonByText();
    """
    
    try:
        text_button = driver.execute_script(text_based_script)
        if text_button:
            print("✅ SHADOW DOM: Found buy button via text-based Shadow DOM search!")
            return text_button, "shadow_dom_text_search"
    except Exception as e:
        print(f"❌ SHADOW DOM: Text-based Shadow DOM search failed: {e}")
    
    # Method 4: Deep Shadow DOM inspection - log what's actually in shadow roots
    print("🔍 SHADOW DOM: Performing deep inspection to debug...")
    
    inspection_script = """
    function inspectShadowRoots() {
        let findings = [];
        
        function inspectElement(element, path = '') {
            if (!element) return;
            
            if (element.shadowRoot) {
                let shadowButtons = element.shadowRoot.querySelectorAll('button');
                if (shadowButtons.length > 0) {
                    findings.push({
                        path: path + ' > ' + element.tagName + '[shadow]',
                        buttonCount: shadowButtons.length,
                        buttons: Array.from(shadowButtons).map(btn => ({
                            tagName: btn.tagName,
                            className: btn.className,
                            textContent: btn.textContent?.substring(0, 50),
                            testId: btn.getAttribute('data-testid'),
                            id: btn.id
                        }))
                    });
                }
                
                // Inspect children in shadow root
                let shadowChildren = element.shadowRoot.querySelectorAll('*');
                for (let i = 0; i < Math.min(shadowChildren.length, 10); i++) {
                    inspectElement(shadowChildren[i], path + ' > ' + element.tagName + '[shadow]');
                }
            }
        }
        
        let allElements = document.querySelectorAll('*');
        for (let i = 0; i < Math.min(allElements.length, 20); i++) {
            inspectElement(allElements[i], 'root');
        }
        
        return findings;
    }
    
    return inspectShadowRoots();
    """
    
    try:
        inspection_results = driver.execute_script(inspection_script)
        if inspection_results:
            print("🔍 SHADOW DOM INSPECTION RESULTS:")
            for result in inspection_results[:3]:  # Show first 3 results
                print(f"  📍 Path: {result['path']}")
                print(f"  🔘 Button count: {result['buttonCount']}")
                for btn in result['buttons'][:2]:  # Show first 2 buttons
                    print(f"    - {btn['tagName']}: '{btn['textContent']}' (testId: {btn['testId']})")
    except Exception as e:
        print(f"❌ SHADOW DOM: Inspection failed: {e}")
    
    print("❌ SHADOW DOM: All Shadow DOM methods failed to find buy button")
    return None, None



class HIDKeyboard:
    """
    True OS-level keyboard input using Windows SendInput API
    Generates hardware-level events indistinguishable from real keyboard
    """
    
    # Windows API constants
    INPUT_KEYBOARD = 1
    KEYEVENTF_KEYUP = 0x0002
    KEYEVENTF_UNICODE = 0x0004
    
    # Virtual Key Codes for common keys
    VK_CODES = {
        '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34,
        '5': 0x35, '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39,
        'right': 0x27,  # Right arrow key
        'left': 0x25,   # Left arrow key
        'tab': 0x09,    # Tab key
        'enter': 0x0D,  # Enter key
        'space': 0x20,  # Space key
        'backspace': 0x08  # Backspace key
    }
    
    def __init__(self):
        """Initialize the HID keyboard with Windows API structures"""
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32
        
        # Define Windows structures
        class KEYBDINPUT(ctypes.Structure):
            _fields_ = [
                ("wVk", ctypes.wintypes.WORD),
                ("wScan", ctypes.wintypes.WORD),
                ("dwFlags", ctypes.wintypes.DWORD),
                ("time", ctypes.wintypes.DWORD),
                ("dwExtraInfo", ctypes.POINTER(ctypes.wintypes.ULONG))
            ]
        
        class HARDWAREINPUT(ctypes.Structure):
            _fields_ = [
                ("uMsg", ctypes.wintypes.DWORD),
                ("wParamL", ctypes.wintypes.WORD),
                ("wParamH", ctypes.wintypes.WORD)
            ]
        
        class MOUSEINPUT(ctypes.Structure):
            _fields_ = [
                ("dx", ctypes.wintypes.LONG),
                ("dy", ctypes.wintypes.LONG),
                ("mouseData", ctypes.wintypes.DWORD),
                ("dwFlags", ctypes.wintypes.DWORD),
                ("time", ctypes.wintypes.DWORD),
                ("dwExtraInfo", ctypes.POINTER(ctypes.wintypes.ULONG))
            ]
        
        class INPUT_UNION(ctypes.Union):
            _fields_ = [
                ("ki", KEYBDINPUT),
                ("mi", MOUSEINPUT),
                ("hi", HARDWAREINPUT)
            ]
        
        class INPUT(ctypes.Structure):
            _fields_ = [
                ("type", ctypes.wintypes.DWORD),
                ("ii", INPUT_UNION)
            ]
        
        # Store structure classes for use
        self.KEYBDINPUT = KEYBDINPUT
        self.INPUT = INPUT
        self.INPUT_UNION = INPUT_UNION
        
        print("✅ HID Keyboard initialized with Windows SendInput API")
    
    def send_key_press(self, key, hold_time=None):
        """
        Send a single key press event (key down + key up)
        
        Args:
            key (str): The key to press ('0'-'9', 'right', 'left', etc.)
            hold_time (float): Time to hold key down in seconds (optional)
        
        Returns:
            bool: True if successful, False if failed
        """
        if key not in self.VK_CODES:
            print(f"❌ HID: Unknown key '{key}'")
            return False
        
        vk_code = self.VK_CODES[key]
        
        try:
            # Create key down event
            key_input_down = self.INPUT()
            key_input_down.type = self.INPUT_KEYBOARD
            key_input_down.ii.ki = self.KEYBDINPUT()
            key_input_down.ii.ki.wVk = vk_code
            key_input_down.ii.ki.wScan = 0
            key_input_down.ii.ki.dwFlags = 0  # Key down
            key_input_down.ii.ki.time = 0
            key_input_down.ii.ki.dwExtraInfo = None
            
            # Create key up event
            key_input_up = self.INPUT()
            key_input_up.type = self.INPUT_KEYBOARD
            key_input_up.ii.ki = self.KEYBDINPUT()
            key_input_up.ii.ki.wVk = vk_code
            key_input_up.ii.ki.wScan = 0
            key_input_up.ii.ki.dwFlags = self.KEYEVENTF_KEYUP  # Key up
            key_input_up.ii.ki.time = 0
            key_input_up.ii.ki.dwExtraInfo = None
            
            # Send key down event
            result_down = self.user32.SendInput(
                1,  # Number of inputs
                ctypes.pointer(key_input_down),
                ctypes.sizeof(self.INPUT)
            )
            
            if result_down == 0:
                error_code = self.kernel32.GetLastError()
                print(f"❌ HID: SendInput key down failed, error code: {error_code}")
                return False
            
            # Hold the key if specified
            if hold_time:
                time.sleep(hold_time)
            else:
                # Default brief hold time for realistic key press
                time.sleep(random.uniform(0.02, 0.08))
            
            # Send key up event
            result_up = self.user32.SendInput(
                1,  # Number of inputs
                ctypes.pointer(key_input_up),
                ctypes.sizeof(self.INPUT)
            )
            
            if result_up == 0:
                error_code = self.kernel32.GetLastError()
                print(f"❌ HID: SendInput key up failed, error code: {error_code}")
                return False
            
            print(f"✅ HID: Successfully sent key '{key}' (VK: {vk_code:02X})")
            return True
            
        except Exception as e:
            print(f"❌ HID: Exception sending key '{key}': {e}")
            return False
    
    def send_unicode_char(self, char):
        """
        Send a Unicode character directly (alternative method)
        
        Args:
            char (str): Single Unicode character to send
        
        Returns:
            bool: True if successful, False if failed
        """
        try:
            unicode_value = ord(char)
            
            # Create Unicode input event
            unicode_input = self.INPUT()
            unicode_input.type = self.INPUT_KEYBOARD
            unicode_input.ii.ki = self.KEYBDINPUT()
            unicode_input.ii.ki.wVk = 0  # Must be 0 for Unicode
            unicode_input.ii.ki.wScan = unicode_value
            unicode_input.ii.ki.dwFlags = self.KEYEVENTF_UNICODE
            unicode_input.ii.ki.time = 0
            unicode_input.ii.ki.dwExtraInfo = None
            
            result = self.user32.SendInput(
                1,
                ctypes.pointer(unicode_input),
                ctypes.sizeof(self.INPUT)
            )
            
            if result == 0:
                error_code = self.kernel32.GetLastError()
                print(f"❌ HID: Unicode input failed for '{char}', error code: {error_code}")
                return False
            
            print(f"✅ HID: Successfully sent Unicode char '{char}' (U+{unicode_value:04X})")
            return True
            
        except Exception as e:
            print(f"❌ HID: Exception sending Unicode '{char}': {e}")
            return False
    
    def type_sequence(self, sequence, delay_between_keys=None):
        """
        Type a sequence of characters with realistic timing
        
        Args:
            sequence (str): String of characters to type
            delay_between_keys (float): Delay between keystrokes (optional)
        
        Returns:
            bool: True if all keys sent successfully
        """
        success_count = 0
        
        for i, char in enumerate(sequence):
            print(f"🔤 HID: Typing character {i+1}/{len(sequence)}: '{char}'")
            
            # Add realistic pre-keystroke delay
            if i > 0:  # No delay before first character
                delay = delay_between_keys if delay_between_keys else random.uniform(0.1, 0.3)
                time.sleep(delay)
            
            # Try virtual key code method first (more reliable)
            if char in self.VK_CODES:
                success = self.send_key_press(char)
            else:
                # Fallback to Unicode method
                success = self.send_unicode_char(char)
            
            if success:
                success_count += 1
            else:
                print(f"❌ HID: Failed to send character '{char}' at position {i}")
        
        success_rate = (success_count / len(sequence)) * 100
        print(f"📊 HID: Typing complete - {success_count}/{len(sequence)} characters sent ({success_rate:.1f}% success)")
        
        return success_count == len(sequence)
    
    def send_navigation_key(self, direction):
        """
        Send navigation keys (arrow keys, tab, enter, etc.)
        
        Args:
            direction (str): 'right', 'left', 'tab', 'enter', 'space', 'backspace'
        
        Returns:
            bool: True if successful
        """
        if direction not in self.VK_CODES:
            print(f"❌ HID: Unknown navigation key '{direction}'")
            return False
        
        return self.send_key_press(direction)


class AudioNumberDetector:
    def __init__(self, driver=None):
        self.driver = driver
            
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

def base64_encode_image(img):
    """Convert PIL Image to base64 string, resizing if necessary"""
    max_size = (200, 200)
    img.thumbnail(max_size, Image.LANCZOS)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Vinted profit suitability ranges (same structure as Facebook but independent variables)
def check_vinted_profit_suitability(listing_price, profit_percentage):
    if 10 <= listing_price < 16:
        return 150 <= profit_percentage <= 600
    elif 16 <= listing_price < 25:
        return 80 <= profit_percentage <= 500
    elif 25 <= listing_price < 50:
        return 50 <= profit_percentage <= 550
    elif 50 <= listing_price < 100:
        return 40 <= profit_percentage <= 500
    elif listing_price >= 100:
        return 32.5 <= profit_percentage <= 450
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
    """Handle Vinted scraper button clicks - send to VM system"""
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
            
            # Send URL to VM bookmark system
            if 'vinted_scraper_instance' in globals():
                vinted_scraper_instance.send_to_vm_bookmark_system(url)
                print(f'🚀 Sent to VM bookmark system: {url}')
            else:
                print("WARNING: No Vinted scraper instance found")
                # Fallback: just add to VM_BOOKMARK_URLS directly
                if url not in VM_BOOKMARK_URLS:
                    VM_BOOKMARK_URLS.append(url)
                    print(f'📋 Added to VM_BOOKMARK_URLS: {url}')
                    
        elif action == 'buy_no':
            print(f'❌ VINTED NO BUTTON: User does not wish to buy listing: {url}')
            # No action needed for "No" button
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
        
    def login_vm_driver(self, driver):
        """Login the VM driver and wait on homepage - extracted from main_vm_driver logic"""
        try:
            print("🔄 VM LOGIN: Starting login process...")
            
            # Clear browser data first
            print("🔄 VM LOGIN: Clearing cookies...")
            driver.delete_all_cookies()
            
            # Navigate to Vinted
            print("🔄 VM LOGIN: Navigating to vinted.co.uk...")
            driver.get("https://vinted.co.uk")
            
            # Random delay after page load
            time.sleep(random.uniform(2, 4))
            
            # Wait for and accept cookies
            print("🔄 VM LOGIN: Accepting cookies...")
            if wait_and_click(driver, By.ID, "onetrust-accept-btn-handler", 15):
                print("✅ VM LOGIN: Cookie consent accepted")
            else:
                print("⚠️ VM LOGIN: Cookie consent button not found")
            
            time.sleep(random.uniform(1, 2))
            
            # Click Sign up | Log in button
            print("🔄 VM LOGIN: Looking for login button...")
            signup_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="header--login-button"]'))
            )
            
            human_like_delay()
            action = move_to_element_naturally(driver, signup_button)
            time.sleep(random.uniform(0.1, 0.3))
            action.click().perform()
            print("✅ VM LOGIN: Clicked Sign up | Log in button")
            
            time.sleep(random.uniform(1, 2))
            
            if google_login:
                print("🔄 VM LOGIN: Using Google login...")
                google_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="google-oauth-button"]'))
                )
                
                human_like_delay()
                action = move_to_element_naturally(driver, google_button)
                time.sleep(random.uniform(0.1, 0.3))
                action.click().perform()
                print("✅ VM LOGIN: Clicked Continue with Google")
                
            else:
                print("🔄 VM LOGIN: Using email login...")
                # ... email login logic stays the same ...
            
            # Wait a bit for login process
            time.sleep(random.uniform(3, 5))
            
            # Handle captcha if present
            result = handle_datadome_audio_captcha(driver)

            if result == "no_captcha":
                print("✅ VM LOGIN: No captcha present - login successful!")
                return True
            elif result == True:
                print("🔄 VM LOGIN: Captcha detected - handling...")
                if HAS_PYAUDIO:
                    detector = AudioNumberDetector(driver=driver)
                    detector.start_listening()
                    # Wait for captcha completion
                    print("⏳ VM LOGIN: Waiting for captcha completion...")
                    return True
                else:
                    print("❌ VM LOGIN: Cannot handle captcha - no audio support")
                    return False
            else:
                print("❌ VM LOGIN: Captcha handling failed")
                return False
                
        except Exception as e:
            print(f"❌ VM LOGIN: Error during login: {e}")
            return False

    def execute_bookmark_with_preloaded_driver(self, url):
        """Execute bookmark using the already logged-in VM driver"""
        global current_bookmark_status
        
        if not self.vm_driver_ready or not self.current_vm_driver:
            print("❌ BOOKMARK: No VM driver ready - cannot bookmark")
            current_bookmark_status = "BOOKMARK FAILED: No driver"
            return False
        
        with self.vm_driver_lock:
            print(f"🔖 BOOKMARK: Using pre-loaded driver for: {url}")
            
            try:
                # Create step log for tracking
                step_log = {
                    'start_time': time.time(),
                    'driver_number': 1,
                    'steps_completed': [],
                    'failures': [],
                    'success': False,
                    'critical_sequence_completed': False,
                    'actual_url': url
                }
                
                # Execute the bookmark sequence
                success = execute_vm_bookmark_sequences(self.current_vm_driver, url, "preloaded_user", step_log)
                
                self.vm_driver_ready = False  # Mark as used
                
                total_time = time.time() - step_log['start_time']
                print(f"📊 BOOKMARK ANALYSIS:")
                print(f"⏱️  Total time: {total_time:.2f}s")
                print(f"✅ Steps completed: {len(step_log['steps_completed'])}")
                print(f"❌ Failures: {len(step_log['failures'])}")
                print(f"🏆 Overall success: {'YES' if success else 'NO'}")
                
                # Set bookmark status based on success
                if success:
                    current_bookmark_status = "✅ BOOKMARK SUCCEEDED"
                    print(f"✅ BOOKMARK STATUS: Success")
                else:
                    current_bookmark_status = "❌ BOOKMARK FAILED"
                    print(f"❌ BOOKMARK STATUS: Failed")
                
                return success
                
            except Exception as e:
                print(f"❌ BOOKMARK: Error using pre-loaded driver: {e}")
                current_bookmark_status = f"❌ BOOKMARK FAILED: {str(e)[:30]}"
                self.vm_driver_ready = False
                return False

    def prepare_next_vm_driver(self):
        """Prepare the NEXT VM driver after current one is used"""
        print("🔄 NEXT DRIVER: Preparing next VM driver...")
        
        try:
            # Close current driver if it exists
            if self.current_vm_driver:
                try:
                    self.current_vm_driver.quit()
                    print("✅ NEXT DRIVER: Closed previous driver")
                except:
                    print("⚠️ NEXT DRIVER: Error closing previous driver")
            
            # Clear browser data for new session
            clear_browser_data_universal("192.168.56.101", {
                "user_data_dir": "C:\\VintedScraper_Default_Bookmark", 
                "profile": "Profile 4", 
                "port": 9224
            })
            
            time.sleep(1)  # Brief delay
            
            # Create new VM driver
            self.current_vm_driver = setup_driver_universal("192.168.56.101", {
                "user_data_dir": "C:\\VintedScraper_Default_Bookmark", 
                "profile": "Profile 4", 
                "port": 9224
            })
            
            if not self.current_vm_driver:
                print("❌ NEXT DRIVER: Failed to create new VM driver")
                self.vm_driver_ready = False
                return
            
            # Login the new driver
            success = self.login_vm_driver(self.current_vm_driver)
            
            if success:
                self.vm_driver_ready = True
                print("✅ NEXT DRIVER: New VM driver ready and logged in")
            else:
                print("❌ NEXT DRIVER: Failed to login new VM driver")
                self.vm_driver_ready = False
                
        except Exception as e:
            print(f"❌ NEXT DRIVER: Error preparing next driver: {e}")
            self.vm_driver_ready = False


    def prepare_initial_vm_driver(self):
        """Prepare the initial VM driver during startup - called ONCE at the beginning"""
        print("🚀 STARTUP: Preparing initial VM driver for immediate use")
        
        try:
            # Create and setup the first VM driver
            self.current_vm_driver = setup_driver_universal("192.168.56.101", {
                "user_data_dir": "C:\\VintedScraper_Default_Bookmark", 
                "profile": "Profile 4", 
                "port": 9224
            })
            
            if not self.current_vm_driver:
                print("❌ STARTUP: Failed to create initial VM driver")
                return False
            
            # Clear cookies and login
            success = self.login_vm_driver(self.current_vm_driver)
            
            if success:
                self.vm_driver_ready = True
                print("✅ STARTUP: Initial VM driver ready and logged in - waiting for first listing")
                return True
            else:
                print("❌ STARTUP: Failed to login initial VM driver")
                return False
                
        except Exception as e:
            print(f"❌ STARTUP: Error preparing initial VM driver: {e}")
            return False

    def __init__(self):
        """
        Modified init - FIXED to properly initialize all confidence/revenue tracking
        """
        global current_listing_title, current_listing_description, current_listing_join_date, current_listing_price
        global current_expected_revenue, current_profit, current_detected_items, current_listing_images
        global current_bounding_boxes, current_listing_url, current_suitability, suitable_listings
        global current_listing_index, recent_listings
        global current_item_confidences, current_item_revenues
        
        # **CRITICAL FIX: Initialize recent_listings for website navigation**
        recent_listings = {
            'listings': [],
            'current_index': 0
        }
        
        # FIXED: Initialize confidence and revenue tracking dictionaries
        current_item_confidences = {}
        current_item_revenues = {}
        
        # Initialize all current listing variables
        if VM_DRIVER_USE:
            self.current_vm_driver = None
            self.vm_driver_ready = False
            self.vm_driver_lock = threading.Lock()
            
            print("🔄 STARTUP: Preparing initial VM driver...")
            self.prepare_next_vm_driver()
        else:
            self.current_vm_driver = None
            self.vm_driver_ready = False
            self.vm_driver_lock = None
        
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

        # Initialize VM connection flag
        self.vm_bookmark_queue = []

        self.listing_timestamps = {}  # Format: {url: {'navigated': timestamp, 'marked_suitable': timestamp, etc.}}
        self.listing_timestamps_lock = threading.Lock()
        
        # Check if CUDA is available
        print(f"CUDA available: {torch.cuda.is_available()}")
        print(f"GPU name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'No GPU'}")

        # Load model with explicit GPU usage
        if torch.cuda.is_available():
            model = YOLO(MODEL_WEIGHTS).cuda()
            print("✅ YOLO model loaded on GPU")
        else:
            model = YOLO(MODEL_WEIGHTS).cpu()
            print("⚠️ YOLO model loaded on CPU (no CUDA available)")

    def record_listing_timestamp(self, url, event_name):
        """
        Thread-safe function to record a timestamp for a listing event
        Args:
            url (str): The listing URL
            event_name (str): Name of the event (e.g., 'navigated', 'marked_suitable', 'buy_clicked', etc.)
        """
        from datetime import datetime
        import pytz
        
        with self.listing_timestamps_lock:
            # Initialize dict for this URL if it doesn't exist
            if url not in self.listing_timestamps:
                self.listing_timestamps[url] = {}
            
            # Record timestamp in UK timezone with milliseconds
            uk_tz = pytz.timezone('Europe/London')
            timestamp = datetime.now(uk_tz)
            formatted_timestamp = timestamp.strftime("%H:%M:%S.%f")[:-3]  # Format: HH:MM:SS.mmm
            
            self.listing_timestamps[url][event_name] = formatted_timestamp
            print(f"⏱️ TIMESTAMP RECORDED: {event_name} at {formatted_timestamp} for {url[:50]}...")


    def run_pygame_window(self):
        global LOCK_POSITION, current_listing_index, suitable_listings, current_bookmark_status
        
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
            'items': pygame.font.Font(None, 24),
            'click': pygame.font.Font(None, 28),
            'suitability': pygame.font.Font(None, 28),
            'reviews': pygame.font.Font(None, 28),
            'exact_time': pygame.font.Font(None, 22),
            'bookmark_status': pygame.font.Font(None, 24)
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
                            current_listing = suitable_listings[current_listing_index]
                            stored_images = current_listing.get('processed_images', [])
                            
                            # CRITICAL FIX: Pass ALL parameters including confidence and revenue
                            self.update_listing_details(
                                title=current_listing['title'],
                                description=current_listing['description'],
                                join_date=current_listing['join_date'],
                                price=current_listing['price'],
                                expected_revenue=current_listing['expected_revenue'],
                                profit=current_listing['profit'],
                                detected_items=current_listing['detected_items'],
                                processed_images=stored_images,
                                bounding_boxes=current_listing['bounding_boxes'],
                                url=current_listing.get('url'),
                                suitability=current_listing.get('suitability'),
                                seller_reviews=current_listing.get('seller_reviews'),
                                bookmark_status=current_listing.get('bookmark_status'),
                                item_confidences=current_listing.get('item_confidences', {}),  # ADDED
                                item_revenues=current_listing.get('item_revenues', {}),        # ADDED
                                listing_timestamps=current_listing.get('listing_timestamps', {})
                            )
                    elif event.key == pygame.K_LEFT:
                        if suitable_listings:
                            current_listing_index = (current_listing_index - 1) % len(suitable_listings)
                            current_listing = suitable_listings[current_listing_index]
                            stored_images = current_listing.get('processed_images', [])
                            
                            # CRITICAL FIX: Pass ALL parameters including confidence and revenue
                            self.update_listing_details(
                                title=current_listing['title'],
                                description=current_listing['description'],
                                join_date=current_listing['join_date'],
                                price=current_listing['price'],
                                expected_revenue=current_listing['expected_revenue'],
                                profit=current_listing['profit'],
                                detected_items=current_listing['detected_items'],
                                processed_images=stored_images,
                                bounding_boxes=current_listing['bounding_boxes'],
                                url=current_listing.get('url'),
                                suitability=current_listing.get('suitability'),
                                seller_reviews=current_listing.get('seller_reviews'),
                                bookmark_status=current_listing.get('bookmark_status'),
                                item_confidences=current_listing.get('item_confidences', {}),  # ADDED
                                item_revenues=current_listing.get('item_revenues', {}),        # ADDED
                                listing_timestamps=current_listing.get('listing_timestamps', {})
                            )
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
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

                if i == 2:  # Rectangle 3 - Title
                    self.render_text_in_rect(screen, fonts['title'], current_listing_title, rect, (0, 0, 0))
                elif i == 1:  # Rectangle 2 - Price
                    self.render_text_in_rect(screen, fonts['price'], current_listing_price, rect, (0, 0, 255))
                elif i == 7:  # Rectangle 8 - Description
                    self.render_multiline_text(screen, fonts['description'], current_listing_description, rect, (0, 0, 0))
                elif i == 8:  # Rectangle 9 - Join Date + Bookmark Status
                    time_label = "Appended:"
                    combined_text = f"{time_label}\n{current_listing_join_date}\n\n{current_bookmark_status}"
                    
                    if "SUCCEEDED" in current_bookmark_status:
                        status_color = (0, 200, 0)
                    elif "FAILED" in current_bookmark_status:
                        status_color = (255, 0, 0)
                    else:
                        status_color = (100, 100, 100)
                    
                    self.render_text_in_rect(screen, fonts['bookmark_status'], combined_text, rect, status_color)
                elif i == 4:  # Rectangle 5 - Expected Revenue
                    self.render_text_in_rect(screen, fonts['revenue'], current_expected_revenue, rect, (0, 128, 0))
                elif i == 9:  # Rectangle 10 - Profit
                    self.render_text_in_rect(screen, fonts['profit'], current_profit, rect, (128, 0, 128))
                elif i == 0:  # Rectangle 1 - Detected Items WITH confidence, count, and revenue
                    # CRITICAL: Access global current_item_confidences and current_item_revenues
                    if isinstance(current_detected_items, dict):
                        formatted_lines = []
                        for item_name, count in current_detected_items.items():
                            if count > 0:
                                # Get confidence and revenue from GLOBAL variables
                                confidence_val = current_item_confidences.get(item_name, 0.0)
                                confidence_pct = confidence_val * 100
                                
                                revenue_val = current_item_revenues.get(item_name, 0.0)
                                
                                # Format: "item_name: conf=85.2% cnt=2 rev=£45.50"
                                formatted_lines.append(
                                    f"{item_name}: conf={confidence_pct:.1f}% cnt={count} rev=£{revenue_val:.2f}"
                                )
                        
                        display_text = "\n".join(formatted_lines) if formatted_lines else "No items detected"
                    else:
                        display_text = "No items detected"
                    
                    self.render_multiline_text(screen, fonts['items'], display_text, rect, (0, 0, 0))
                elif i == 10:  # Rectangle 11 - Images
                    self.render_images(screen, current_listing_images, rect, current_bounding_boxes)
                elif i == 3:  # Rectangle 4 - Click to open
                    click_text = "CLICK TO OPEN LISTING IN CHROME"
                    self.render_text_in_rect(screen, fonts['click'], click_text, rect, (255, 0, 0))
                elif i == 5:  # Rectangle 6 - Suitability Reason + Timestamps
                    timestamp_lines = []
                    
                    if current_listing_timestamps:
                        timestamp_lines.append("\n--- TIMINGS ---")
                        
                        if 'navigated' in current_listing_timestamps:
                            timestamp_lines.append(f"Navigated: {current_listing_timestamps['navigated']}")
                        
                        if 'marked_suitable' in current_listing_timestamps:
                            timestamp_lines.append(f"Marked suitable: {current_listing_timestamps['marked_suitable']}")
                        else:
                            timestamp_lines.append("Marked suitable: N/A (unsuitable)")
                        
                        if 'buy_clicked' in current_listing_timestamps:
                            timestamp_lines.append(f"Buy clicked: {current_listing_timestamps['buy_clicked']}")
                        else:
                            timestamp_lines.append("Buy clicked: Never clicked")
                        
                        if 'ship_to_home_clicked' in current_listing_timestamps:
                            timestamp_lines.append(f"Ship to home: {current_listing_timestamps['ship_to_home_clicked']}")
                        else:
                            timestamp_lines.append("Ship to home: Not clicked")
                        
                        if 'pay_clicked' in current_listing_timestamps:
                            timestamp_lines.append(f"Pay clicked: {current_listing_timestamps['pay_clicked']}")
                        else:
                            timestamp_lines.append("Pay clicked: Not clicked")
                    else:
                        timestamp_lines.append("\n--- TIMINGS ---")
                        timestamp_lines.append("No timing data available")
                    
                    combined_text = current_suitability + "\n" + "\n".join(timestamp_lines)
                    
                    self.render_text_in_rect(screen, fonts['suitability'], combined_text, rect, (255, 0, 0) if "Unsuitable" in current_suitability else (0, 255, 0))
                elif i == 6:  # Rectangle 7 - Seller Reviews
                    self.render_text_in_rect(screen, fonts['reviews'], current_seller_reviews, rect, (0, 0, 128))

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
        """
        Enhanced render_images that supports up to 25 images with dynamic grid sizing:
        - 1 image: 1x1 grid (full rectangle)
        - 2-4 images: 2x2 grid
        - 5-9 images: 3x3 grid
        - 10-16 images: 4x4 grid
        - 17-25 images: 5x5 grid
        """
        if not images:
            return

        num_images = len(images)
        
        # Determine grid size based on number of images
        if num_images == 1:
            grid_size = 1
        elif 2 <= num_images <= 4:
            grid_size = 2
        elif 5 <= num_images <= 9:
            grid_size = 3
        elif 10 <= num_images <= 16:
            grid_size = 4
        elif 17 <= num_images <= 25:
            grid_size = 5
        else:
            # Cap at 25 images maximum
            grid_size = 5
            num_images = min(num_images, 25)

        # Calculate cell dimensions
        cell_width = rect.width // grid_size
        cell_height = rect.height // grid_size

        # Render each image in the grid
        for i, img in enumerate(images):
            if i >= grid_size * grid_size:
                # Maximum capacity reached for current grid size
                break
            
            # Calculate row and column position
            row = i // grid_size
            col = i % grid_size
            
            # Resize image to fit cell
            img = img.resize((cell_width, cell_height))
            
            # Convert PIL image to pygame surface
            img_surface = pygame.image.fromstring(img.tobytes(), img.size, img.mode)
            
            # Calculate position on screen
            x_pos = rect.left + col * cell_width
            y_pos = rect.top + row * cell_height
            
            # Blit (draw) the image on screen
            screen.blit(img_surface, (x_pos, y_pos))

        # Display suitability reason (existing code preserved)
        if FAILURE_REASON_LISTED:
            font = pygame.font.Font(None, 24)
            suitability_text = font.render(
                current_suitability, 
                True, 
                (255, 0, 0) if "Unsuitable" in current_suitability else (0, 255, 0)
            )
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

    def update_listing_details(self, title, description, join_date, price, expected_revenue, 
                            profit, detected_items, processed_images, bounding_boxes, 
                            url=None, suitability=None, seller_reviews=None, 
                            bookmark_status=None, item_confidences=None, item_revenues=None, 
                            listing_timestamps=None):
        """
        FIXED: Properly updates global variables including confidence and revenue
        """
        global current_listing_title, current_listing_description, current_listing_join_date, current_listing_price
        global current_expected_revenue, current_profit, current_detected_items, current_listing_images 
        global current_bounding_boxes, current_listing_url, current_suitability, current_seller_reviews
        global current_bookmark_status, current_item_confidences, current_item_revenues
        global current_listing_timestamps

        # Initialize if None
        if item_confidences is None:
            item_confidences = {}
        if item_revenues is None:
            item_revenues = {}

        # Handle bookmark status
        if bookmark_status:
            current_bookmark_status = bookmark_status

        # CRITICAL: Initialize confidence/revenue for all detected items
        if detected_items and isinstance(detected_items, dict):
            for item_name, count in detected_items.items():
                if count > 0:
                    if item_name not in item_confidences:
                        item_confidences[item_name] = 0.0
                    if item_name not in item_revenues:
                        item_revenues[item_name] = 0.0

        # CRITICAL: Update GLOBAL dicts with deep copies
        current_item_confidences = {}
        current_item_revenues = {}
        
        for item, conf in item_confidences.items():
            current_item_confidences[item] = float(conf)
        
        for item, rev in item_revenues.items():
            current_item_revenues[item] = float(rev)

        # Handle images
        if processed_images:
            if 'current_listing_images' in globals() and current_listing_images:
                for img in current_listing_images:
                    try:
                        img.close()
                    except:
                        pass
                current_listing_images.clear()

            for img in processed_images:
                try:
                    img_copy = img.copy()
                    current_listing_images.append(img_copy)
                except Exception as e:
                    print(f"Error copying image: {str(e)}")

        # Store bounding boxes
        current_bounding_boxes = {
            'image_paths': bounding_boxes.get('image_paths', []) if bounding_boxes else [],
            'detected_objects': bounding_boxes.get('detected_objects', {}) if bounding_boxes else {}
        }

        # Handle detected_items formatting
        if isinstance(detected_items, dict):
            formatted_detected_items = {}
            for item, count in detected_items.items():
                try:
                    count_int = int(count) if isinstance(count, str) else count
                    if count_int > 0:
                        formatted_detected_items[item] = count_int
                except (ValueError, TypeError):
                    continue
            
            if not formatted_detected_items:
                formatted_detected_items = {"no_items": 0}
        else:
            formatted_detected_items = {"no_items": 0}

        stored_append_time = join_date if join_date else "No timestamp"

        # Update ALL global variables
        current_detected_items = formatted_detected_items
        current_listing_title = title[:50] + '...' if len(title) > 50 else title
        current_listing_description = description[:200] + '...' if len(description) > 200 else description if description else "No description"
        current_listing_join_date = stored_append_time
        current_listing_price = f"Price:\n£{float(price):.2f}" if price else "Price:\n£0.00"
        current_expected_revenue = f"Rev:\n£{expected_revenue:.2f}" if expected_revenue else "Rev:\n£0.00"
        current_profit = f"Profit:\n£{profit:.2f}" if profit else "Profit:\n£0.00"
        current_listing_url = url
        current_suitability = suitability if suitability else "Suitability unknown"
        current_seller_reviews = seller_reviews if seller_reviews else "No reviews yet"
        current_listing_timestamps = listing_timestamps if listing_timestamps else {}
        
        # DEBUG: Verify data was stored
        if print_debug:
            print(f"🐛 STORED {len(current_item_confidences)} confidences:")
            for item, conf in current_item_confidences.items():
                rev = current_item_revenues.get(item, 0.0)
                print(f"  {item}: conf={conf:.2%}, rev=£{rev:.2f}")



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

        options.add_argument("--disable-browser-side-navigation")
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
        import re
        
        title = listing_info.get("title", "").lower()
        description = listing_info.get("description", "").lower()
        price = listing_info.get("price", 0)
        seller_reviews = listing_info.get("seller_reviews", "No reviews yet")
        
        try:
            price_float = float(price)
        except (ValueError, TypeError):
            return "Unsuitable: Unable to parse price"
        
        # Extract number of reviews from seller_reviews
        reviews_count = 0
        if seller_reviews and seller_reviews != "No reviews yet":
            reviews_text = str(seller_reviews).strip()
            
            if print_debug:
                print(f"DEBUG: Raw seller_reviews value: '{reviews_text}'")
            
            if reviews_text.startswith("Reviews: "):
                try:
                    reviews_count = int(reviews_text.replace("Reviews: ", ""))
                except ValueError:
                    reviews_count = 0
            elif reviews_text.isdigit():
                reviews_count = int(reviews_text)
            else:
                match = re.search(r'\d+', reviews_text)
                if match:
                    reviews_count = int(match.group())
                else:
                    reviews_count = 0
        
        if print_debug:
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
            "Too many $ symbols in description")
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
        OPTIMIZED: Enhanced scraper that collects ALL elements in a SINGLE operation
        Uses JavaScript to gather all data at once for maximum speed
        UPDATED: Now includes username collection AND stores price for threshold filtering
        ** MODIFIED: Now amends postage price if below £2.99 **
        """
        debug_function_call("scrape_item_details")
        import re
        
        # Wait for page to be ready
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "p.web_ui__Text__subtitle"))
        )

        # OPTIMIZATION: Single JavaScript command to collect ALL elements at once
        scraping_script = """
        function scrapeAllElements() {
            const data = {
                title: null,
                price: null,
                second_price: null,
                postage: null,
                description: null,
                uploaded: null,
                seller_reviews: null,
                username: null
            };
            
            // Helper function to get text from element
            function getElementText(selector) {
                try {
                    const element = document.querySelector(selector);
                    return element ? element.textContent.trim() : null;
                } catch (e) {
                    return null;
                }
            }
            
            // Helper function to get text from multiple selectors (returns first match)
            function getElementTextMultiSelector(selectors) {
                for (let selector of selectors) {
                    try {
                        const element = document.querySelector(selector);
                        if (element && element.textContent.trim()) {
                            return element.textContent.trim();
                        }
                    } catch (e) {
                        continue;
                    }
                }
                return null;
            }
            
            // Title
            data.title = getElementText("h1.web_ui__Text__title");
            
            // Price (main price field)
            data.price = getElementText("p.web_ui__Text__subtitle");
            
            // Second price
            data.second_price = getElementText("div.web_ui__Text__title.web_ui__Text__clickable.web_ui__Text__underline-none");
            
            // Postage
            data.postage = getElementText("h3[data-testid='item-shipping-banner-price']");
            
            // Description - collect all spans within the description container
            try {
                const descSpans = document.querySelectorAll("span.web_ui__Text__text.web_ui__Text__body.web_ui__Text__left.web_ui__Text__format span");
                if (descSpans.length > 0) {
                    data.description = Array.from(descSpans).map(span => span.textContent.trim()).join(' ');
                }
            } catch (e) {
                data.description = null;
            }
            
            // Uploaded
            data.uploaded = getElementText("span.web_ui__Text__text.web_ui__Text__subtitle.web_ui__Text__left.web_ui__Text__bold");
            
            // Seller reviews - try multiple selectors and find one with digits
            const reviewSelectors = [
                "span.web_ui__Text__text.web_ui__Text__caption.web_ui__Text__left",
                "span[class*='caption'][class*='left']",
                "div[class*='reviews'] span",
                "*[class*='review']"
            ];
            
            for (let selector of reviewSelectors) {
                try {
                    const elements = document.querySelectorAll(selector);
                    for (let element of elements) {
                        const text = element.textContent.trim();
                        // Look for text that contains digits (likely review count)
                        if (text && (text.match(/\\d+/) || text.toLowerCase().includes('review'))) {
                            data.seller_reviews = text;
                            break;
                        }
                    }
                    if (data.seller_reviews) break;
                } catch (e) {
                    continue;
                }
            }
            
            // Username - try multiple selectors
            const usernameSelectors = [
                "span[data-testid='profile-username']",
                "span.web_ui__Text__text.web_ui__Text__body.web_ui__Text__left.web_ui__Text__amplified.web_ui__Text__bold[data-testid='profile-username']",
                "*[data-testid='profile-username']",
                "span.web_ui__Text__amplified.web_ui__Text__bold"
            ];
            
            data.username = getElementTextMultiSelector(usernameSelectors);
            
            return data;
        }
        
        return scrapeAllElements();
        """
        
        try:
            # Execute the JavaScript to collect all data in ONE operation
            data_raw = driver.execute_script(scraping_script)
            
            # Convert the raw data to the expected format
            data = {
                "title": data_raw.get("title"),
                "price": data_raw.get("price"),
                "second_price": data_raw.get("second_price"),
                "postage": data_raw.get("postage"),
                "description": data_raw.get("description"),
                "uploaded": data_raw.get("uploaded"),
                "seller_reviews": data_raw.get("seller_reviews") if data_raw.get("seller_reviews") else "No reviews yet",
                "username": data_raw.get("username") if data_raw.get("username") else "Username not found"
            }
            
        except Exception as js_error:
            print(f"JavaScript scraping failed: {js_error}")
            print("Falling back to traditional Selenium scraping...")
            
            # FALLBACK: Traditional Selenium scraping (original method)
            fields = {
                "title": "h1.web_ui__Text__title",
                "price": "p.web_ui__Text__subtitle",
                "second_price": "div.web_ui__Text__title.web_ui__Text__clickable.web_ui__Text__underline-none",
                "postage": "h3[data-testid='item-shipping-banner-price']",
                "description": "span.web_ui__Text__text.web_ui__Text__body.web_ui__Text__left.web_ui__Text__format span",
                "uploaded": "span.web_ui__Text__text.web_ui__Text__subtitle.web_ui__Text__left.web_ui__Text__bold",
                "seller_reviews": "span.web_ui__Text__text.web_ui__Text__caption.web_ui__Text__left",
                "username": "span[data-testid='profile-username']",
            }

            data = {}
            for key, sel in fields.items():
                try:
                    if key == "seller_reviews":
                        # [Existing seller reviews logic - kept unchanged]
                        review_selectors = [
                            "span.web_ui__Text__text.web_ui__Text__caption.web_ui__Text__left",
                            "span[class*='caption'][class*='left']",
                            "div[class*='reviews'] span",
                            "*[class*='review']",
                        ]
                        
                        reviews_text = None
                        for review_sel in review_selectors:
                            try:
                                elements = driver.find_elements(By.CSS_SELECTOR, review_sel)
                                for element in elements:
                                    text = element.text.strip()
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
                        
                        if reviews_text:
                            if reviews_text == "No reviews yet" or "no review" in reviews_text.lower():
                                data[key] = "No reviews yet"
                            elif reviews_text.isdigit():
                                data[key] = reviews_text
                                if print_debug:
                                    print(f"DEBUG: Set seller_reviews to: '{reviews_text}'")
                            else:
                                match = re.search(r'(\d+)', reviews_text)
                                if match:
                                    data[key] = match.group(1)
                                    if print_debug:
                                        print(f"DEBUG: Extracted number from '{reviews_text}': '{match.group(1)}'")
                                else:
                                    data[key] = "No reviews yet"
                        else:
                            data[key] = "No reviews yet"
                            if print_debug:
                                print("DEBUG: No seller reviews found with any selector")
                            
                    elif key == "username":
                        # [Existing username logic - kept unchanged]
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
                            alternative_username_selectors = [
                                "span.web_ui__Text__text.web_ui__Text__body.web_ui__Text__left.web_ui__Text__amplified.web_ui__Text__bold[data-testid='profile-username']",
                                "span[data-testid='profile-username']",
                                "*[data-testid='profile-username']",
                                "span.web_ui__Text__amplified.web_ui__Text__bold",
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

        # ========================================================================
        # CRITICAL NEW CODE: POSTAGE PRICE AMENDMENT
        # ========================================================================
        # Extract the postage price as a float
        postage_text = data.get("postage", "£0")
        postage_value = self.extract_price(postage_text)
        
        # CRITICAL: Apply the £2.99 minimum postage rule
        MIN_POSTAGE = 2.99
        original_postage = postage_value
        
        if postage_value < MIN_POSTAGE:
            postage_value = MIN_POSTAGE
            print(f"🔧 POSTAGE AMENDED: £{original_postage:.2f} → £{MIN_POSTAGE:.2f}")
            
            # Update the data dict with the amended postage (formatted as text)
            data["postage"] = f"£{MIN_POSTAGE:.2f}"
        else:
            print(f"✅ POSTAGE OK: £{postage_value:.2f} (no amendment needed)")
        
        # ========================================================================
        # END OF POSTAGE AMENDMENT CODE
        # ========================================================================

        # Process seller_reviews value (same logic for both JS and fallback methods)
        if data.get("seller_reviews") and data["seller_reviews"] != "No reviews yet":
            reviews_text = str(data["seller_reviews"]).strip()
            
            if print_debug:
                print(f"DEBUG: Raw seller_reviews value: '{reviews_text}'")
            
            if reviews_text.startswith("Reviews: "):
                try:
                    data["seller_reviews"] = reviews_text.replace("Reviews: ", "")
                except ValueError:
                    data["seller_reviews"] = "No reviews yet"
            elif reviews_text.isdigit():
                data["seller_reviews"] = reviews_text
            else:
                match = re.search(r'\d+', reviews_text)
                if match:
                    data["seller_reviews"] = match.group()
                else:
                    data["seller_reviews"] = "No reviews yet"

        # Keep title formatting for pygame display
        if data["title"]:
            data["title"] = data["title"][:50] + '...' if len(data["title"]) > 50 else data["title"]

        # Calculate and store the total price for threshold filtering
        second_price = self.extract_price(data.get("second_price", "0"))
        postage = self.extract_price(data.get("postage", "0"))  # This now uses the AMENDED postage
        total_price = second_price + postage
        
        # Store the calculated price for use in object detection
        self.current_listing_price_float = total_price
        
        # DEBUG: Print final scraped data
        if print_debug:
            print(f"DEBUG: Final scraped seller_reviews: '{data.get('seller_reviews')}'")
            print(f"DEBUG: Final scraped username: '{data.get('username')}'")
            print(f"DEBUG: Total price calculated: £{total_price:.2f} (stored for threshold filtering)")
            print(f"DEBUG: Postage used in calculation: £{postage:.2f}")
            
        return data

    def clear_download_folder(self):
        if os.path.exists(DOWNLOAD_ROOT):
            shutil.rmtree(DOWNLOAD_ROOT)
        os.makedirs(DOWNLOAD_ROOT, exist_ok=True)

                
    def process_listing_immediately_with_vm(self, url, details, detected_objects, processed_images, listing_counter, all_confidences=None, item_revenues_from_detection=None):
        """
        FIXED: Now properly checks for misc_games when evaluating game-only listings
        EXCEPTION: If listing has 3 actual detected games AND misc_games, it should NOT be marked unsuitable
        """
        global suitable_listings, current_listing_index, recent_listings, current_bookmark_status

        print(f"🚀 REAL-TIME: Processing listing #{listing_counter}")
        
        # Initialize if None
        if all_confidences is None:
            all_confidences = {}
        if item_revenues_from_detection is None:
            item_revenues_from_detection = {}

        username = details.get("username", None)
        if not username or username == "Username not found":
            username = None

        second_price = self.extract_price(details.get("second_price", "0"))
        postage = self.extract_price(details.get("postage", "0"))
        total_price = second_price + postage
        
        print(f"💰 PRICE: £{total_price:.2f}")

        seller_reviews = details.get("seller_reviews", "No reviews yet")

        listing_info = {
            "title": details.get("title", "").lower(),
            "description": details.get("description", "").lower(),
            "price": total_price,
            "seller_reviews": seller_reviews,
            "url": url
        }

        suitability_result = self.check_vinted_listing_suitability(listing_info)

        # ========================================================================
        # CRITICAL FIX: Only apply console keyword detection if price is high enough
        # This prevents false positives from text mentions on low-priced game-only listings
        # ========================================================================
        detected_console = None
        
        # Only run keyword detection if price meets threshold
        if total_price >= MIN_PRICE_FOR_CONSOLE_KEYWORD_DETECTION:
            detected_console = self.detect_console_keywords_vinted(
                details.get("title", ""),
                details.get("description", "")
            )
            
            if detected_console:
                print(f"💰 CONSOLE KEYWORD: Found '{detected_console}' in text (price £{total_price:.2f} >= £{MIN_PRICE_FOR_CONSOLE_KEYWORD_DETECTION})")
                mutually_exclusive_items = ['switch', 'oled', 'lite', 'switch_box', 'oled_box', 
                                            'lite_box', 'switch_in_tv', 'oled_in_tv']
                for item in mutually_exclusive_items:
                    detected_objects[item] = 1 if item == detected_console else 0
            else:
                print(f"💰 CONSOLE KEYWORD: No keywords found (price £{total_price:.2f} >= threshold)")
        else:
            print(f"⏭️ CONSOLE KEYWORD: Skipped (price £{total_price:.2f} < £{MIN_PRICE_FOR_CONSOLE_KEYWORD_DETECTION})")
            # Don't run keyword detection at all for low-priced listings

        detected_objects = self.handle_oled_title_conversion_vinted(
            detected_objects,
            details.get("title", ""),
            details.get("description", "")
        )

        # Calculate revenue (this creates a NEW item_revenues dict)
        total_revenue, expected_profit, profit_percentage, display_objects, item_revenues_from_calc = \
            self.calculate_vinted_revenue(
                detected_objects,
                total_price, 
                details.get("title", ""), 
                details.get("description", "")
            )

        final_item_revenues = {}
        final_item_revenues.update(item_revenues_from_calc)
        final_item_revenues.update(item_revenues_from_detection)

        if print_debug:
            print(f"🐛 DEBUG: detected_objects after revenue calc has {len(detected_objects)} items")
            if 'misc_games' in detected_objects:
                print(f"🐛 DEBUG: misc_games = {detected_objects['misc_games']}")

        profit_suitability = self.check_vinted_profit_suitability(total_price, profit_percentage)

        # ========================================================================
        # CRITICAL SECTION - GAME FILTER LOGIC WITH EXCEPTION FOR MISC_GAMES
        # ========================================================================
        game_classes = [
            '1_2_switch', 'animal_crossing', 'arceus_p', 'bow_z', 'bros_deluxe_m', 'crash_sand',
            'dance', 'diamond_p', 'evee', 'fifa_23', 'fifa_24', 'gta', 'just_dance', 'kart_m', 'kirby',
            'lets_go_p', 'links_z', 'luigis', 'mario_maker_2', 'mario_sonic', 'mario_tennis', 'minecraft',
            'minecraft_dungeons', 'minecraft_story', 'miscellanious_sonic', 'odyssey_m', 'other_mario',
            'party_m', 'rocket_league', 'scarlet_p', 'shield_p', 'shining_p', 'skywards_z', 'smash_bros',
            'snap_p', 'splatoon_2', 'splatoon_3', 'super_m_party', 'super_mario_3d', 'switch_sports',
            'sword_p', 'tears_z', 'violet_p'
        ]
        
        # Count actual detected games (not including misc_games)
        game_count = sum(detected_objects.get(game, 0) for game in game_classes)
        
        # Count misc_games separately
        misc_games_count = detected_objects.get('misc_games', 0)
        
        # Get non-game classes (excluding misc_games)
        non_game_classes = [
            cls for cls in detected_objects.keys() 
            if cls not in game_classes 
            and cls != 'misc_games'
            and detected_objects.get(cls, 0) > 0
        ]

        unsuitability_reasons = []

        if "Unsuitable" in suitability_result:
            unsuitability_reasons.append(suitability_result.replace("Unsuitable: ", ""))

        # ========================================================================
        # CRITICAL FIX: Exception for listings with exactly 3 games + misc_games
        # ========================================================================
        # Original rule: 1-3 games with no additional non-game items = unsuitable
        # Exception: If game_count == 3 AND misc_games > 0, then it IS suitable
        
        if 1 <= game_count <= 3 and not non_game_classes:
            # Check for the exception: exactly 3 detected games WITH misc_games
            if game_count == 3 and misc_games_count > 0:
                # EXCEPTION APPLIES - this listing is suitable
                print(f"✅ EXCEPTION: 3 detected games + {misc_games_count} misc_games = SUITABLE")
            else:
                # No exception - apply original unsuitable rule
                unsuitability_reasons.append(
                    f"{game_count} game(s) with no additional non-game items"
                )
                print(f"❌ UNSUITABLE: {game_count} game(s), no misc_games or < 3 detected games")

        if not profit_suitability:
            unsuitability_reasons.append(
                f"Profit £{expected_profit:.2f} ({profit_percentage:.2f}%) not suitable"
            )

        if unsuitability_reasons:
            suitability_reason = "Unsuitable:\n---- " + "\n---- ".join(unsuitability_reasons)
            is_suitable = False
        else:
            suitability_reason = f"Suitable: Profit £{expected_profit:.2f} ({profit_percentage:.2f}%)"
            is_suitable = True
            
            # TIMESTAMP: Record when listing was marked as suitable
            self.record_listing_timestamp(url, 'marked_suitable')

        bookmark_status = "No bookmark attempted"
        
        if is_suitable or VINTED_SHOW_ALL_LISTINGS:
            if VM_DRIVER_USE:
                start_listing_timer(url)
                
                try:
                    success = self.execute_bookmark_with_preloaded_driver(url)
                    bookmark_status = current_bookmark_status
                    if not success:
                        stop_listing_timer(url, stage='failed')
                except Exception as vm_error:
                    bookmark_status = f"❌ BOOKMARK FAILED: {str(vm_error)[:30]}"
                    stop_listing_timer(url, stage='error')
            
                if VM_DRIVER_USE:
                    try:
                        self.prepare_next_vm_driver()
                    except Exception as prep_error:
                        print(f"❌ NEXT DRIVER ERROR: {prep_error}")
        else:
            bookmark_status = "Unsuitable - no bookmark"

        from datetime import datetime
        import pytz
        uk_tz = pytz.timezone('Europe/London')
        append_time = datetime.now(uk_tz)
        exact_append_time = append_time.strftime("%H:%M:%S.%f")[:-3]

        preserved_images = []
        for img in processed_images:
            try:
                img_copy = img.copy()
                preserved_images.append(img_copy)
            except Exception as e:
                print(f"Error copying image: {e}")

        if print_debug:
            print(f"🐛 DEBUG: Confidences dict has {len(all_confidences)} items")
            print(f"🐛 DEBUG: Revenues dict has {len(final_item_revenues)} items")
            for item in detected_objects:
                if detected_objects[item] > 0:
                    conf = all_confidences.get(item, 0.0)
                    rev = final_item_revenues.get(item, 0.0)
                    print(f"🐛 DEBUG: {item} -> conf={conf:.2%}, rev=£{rev:.2f}")

        listing_timestamps_data = {}
        with self.listing_timestamps_lock:
            if url in self.listing_timestamps:
                listing_timestamps_data = self.listing_timestamps[url].copy()

        final_listing_info = {
            'title': details.get("title", "No title"),
            'description': details.get("description", "No description"),
            'join_date': exact_append_time,
            'price': str(total_price),
            'expected_revenue': total_revenue,
            'profit': expected_profit,
            'detected_items': detected_objects,
            'processed_images': preserved_images,
            'bounding_boxes': {'image_paths': [], 'detected_objects': detected_objects},
            'url': url,
            'suitability': suitability_reason,
            'seller_reviews': seller_reviews,
            'bookmark_status': bookmark_status,
            'item_confidences': all_confidences,
            'item_revenues': final_item_revenues,
            'listing_timestamps': listing_timestamps_data
        }

        should_add_to_display = is_suitable or VINTED_SHOW_ALL_LISTINGS

        if should_add_to_display:
            recent_listings['listings'].append(final_listing_info)
            recent_listings['current_index'] = len(recent_listings['listings']) - 1

            suitable_listings.append(final_listing_info)
            current_listing_index = len(suitable_listings) - 1
            
            self.update_listing_details(**final_listing_info)

            print(f"✅ Added to display")

        self.cleanup_processed_images(processed_images)

        
    # FIXED: Updated process_vinted_listing function - key section that handles suitability checking
    def send_to_vm_bookmark_system(self, url):
        """
        DEPRECATED: This method is now replaced by immediate processing
        Real-time processing happens in process_listing_immediately_with_vm
        """
        print(f"⚠️  DEPRECATED: send_to_vm_bookmark_system called")
        print(f"🔄 REAL-TIME: Processing should happen immediately, not queued")
        pass  # Do nothing - real-time processing handles this

    def process_vinted_listing(self, details, detected_objects, processed_images, listing_counter, url, all_confidences=None, item_revenues=None):
        """
        FIXED: Actually uses the confidences and revenues passed in
        """
        print(f"📋 PROCESSING: Listing #{listing_counter}")
        
        # CRITICAL: Pass through the confidences and revenues
        self.process_listing_immediately_with_vm(
            url, 
            details, 
            detected_objects, 
            processed_images, 
            listing_counter,
            all_confidences,  # ADD THIS PARAMETER
            item_revenues     # ADD THIS PARAMETER
        )
        
        print(f"✅ PROCESSING COMPLETE: Listing #{listing_counter} finished")


    def should_process_listing_immediately(self, is_suitable, detected_objects, total_price):
        """
        Determine if a listing should trigger immediate VM processing
        You can customize this logic based on your specific criteria
        """
        # Only process if listing is suitable
        if not is_suitable:
            return False
        
        # Additional filters can be added here
        # For example: minimum price threshold
        if total_price < 15.0:
            print(f"⏭️  SKIP VM: Price £{total_price:.2f} below minimum threshold")
            return False
        
        # Check for specific high-value items
        high_value_items = ['switch', 'oled', 'lite', 'switch_box', 'oled_box', 'lite_box']
        has_high_value_item = any(detected_objects.get(item, 0) > 0 for item in high_value_items)
        
        if not has_high_value_item:
            print(f"⏭️  SKIP VM: No high-value items detected")
            return False
        
        print(f"🎯 TRIGGER VM: Listing meets criteria for immediate processing")
        return True

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
        FIXED: Now checks if detected_objects has ANY items before adding misc_games
        Returns: (total_revenue, expected_profit, profit_percentage, display_objects, item_revenues)
        """
        debug_function_call("calculate_vinted_revenue")
        import re
        
        game_classes = [
            '1_2_switch', 'animal_crossing', 'arceus_p', 'bow_z', 'bros_deluxe_m', 'crash_sand',
            'dance', 'diamond_p', 'evee', 'fifa_23', 'fifa_24', 'gta','just_dance', 'kart_m', 'kirby',
            'lets_go_p', 'links_z', 'luigis', 'mario_maker_2', 'mario_sonic', 'mario_tennis', 'minecraft',
            'minecraft_dungeons', 'minecraft_story', 'miscellanious_sonic', 'odyssey_m', 'other_mario',
            'party_m', 'rocket_league', 'scarlet_p', 'shield_p', 'shining_p', 'skywards_z', 'smash_bros',
            'snap_p', 'splatoon_2', 'splatoon_3', 'super_m_party', 'super_mario_3d', 'switch_sports',
            'sword_p', 'tears_z', 'violet_p'
        ]

        all_prices = self.fetch_all_prices()

        # CRITICAL FIX: Check if detected_objects has ANY non-zero items
        has_any_detections = any(
            detected_objects.get(item, 0) > 0 
            for item in detected_objects.keys()
        )
        
        # Count detected games from YOLO
        detected_games_count = sum(detected_objects.get(game, 0) for game in game_classes)
        
        # Extract games mentioned in text
        text_games_count = self.detect_anonymous_games_vinted(title, description)

        # CRITICAL FIX: Only calculate misc games if we have ANY detections
        # This prevents misc_games from being added to completely empty listings
        if has_any_detections:
            # Calculate misc games (text mentions minus detected, capped at misc_games_cap)
            misc_games_count_uncapped = max(0, text_games_count - detected_games_count)
            misc_games_count = min(misc_games_count_uncapped, misc_games_cap)
            
            if misc_games_count_uncapped > misc_games_cap:
                print(f"🎮 MISC GAMES CAP APPLIED: {misc_games_count_uncapped} → {misc_games_count} (cap: {misc_games_cap})")
            
            # Calculate misc games revenue
            misc_games_revenue = misc_games_count * miscellaneous_games_price
            
            # Add misc_games to detected_objects for display
            if misc_games_count > 0:
                detected_objects['misc_games'] = misc_games_count
                print(f"🎮 MISC GAMES ADDED TO DETECTED_OBJECTS: {misc_games_count} games = £{misc_games_revenue:.2f}")
        else:
            # FIX: No detections at all - don't add any misc games
            misc_games_count = 0
            misc_games_revenue = 0.0
            print(f"🎮 MISC GAMES SKIPPED: No detections in listing (detected_objects empty)")
        
        # Track per-item revenue
        item_revenues = {}

        # Add misc games revenue to tracking (only if > 0)
        if misc_games_count > 0:
            item_revenues['misc_games'] = misc_games_revenue

        # Handle box adjustments (remove items that are part of boxes)
        adjustments = {
            'oled_box': ['switch', 'comfort_h', 'tv_white'],
            'switch_box': ['switch', 'comfort_h', 'tv_black'],
            'lite_box': ['lite']
        }

        for box, items in adjustments.items():
            box_count = detected_objects.get(box, 0)
            for item in items:
                detected_objects[item] = max(0, detected_objects.get(item, 0) - box_count)

        # Remove switch_screen (not a revenue item)
        detected_objects.pop('switch_screen', None)

        # Start with misc games revenue
        total_revenue = misc_games_revenue

        # Calculate revenue from detected objects
        for item, count in detected_objects.items():
            # Skip misc_games since we already added it
            if item == 'misc_games':
                continue
                
            if isinstance(count, str):
                count_match = re.match(r'(\d+)', count)
                count = int(count_match.group(1)) if count_match else 0

            if count > 0 and item in all_prices:
                item_price = all_prices[item]
                
                # Special handling for pro controllers
                if item == 'controller' and 'pro' in title.lower():
                    item_price += 7.50
                
                item_revenue = item_price * count
                total_revenue += item_revenue
                
                # Store per-item revenue
                item_revenues[item] = item_revenue
        
        # Debug output (now only shows items that exist)
        for item, count in detected_objects.items():
            if count > 0:
                price_info = all_prices.get(item, 'NOT IN PRICES')
                if item == 'misc_games':
                    price_info = f"£{miscellaneous_games_price:.2f} each"
                print(f"DEBUG ITEM: {item} = {count}, price = {price_info}")

        # Calculate profit
        expected_profit = total_revenue - listing_price
        profit_percentage = (expected_profit / listing_price) * 100 if listing_price > 0 else 0

        print(f"Listing Price: £{listing_price:.2f}")
        print(f"Total Expected Revenue: £{total_revenue:.2f}")
        print(f"Expected Profit/Loss: £{expected_profit:.2f} ({profit_percentage:.2f}%)")

        # Create display_objects (items with count > 0)
        display_objects = {k: v for k, v in detected_objects.items() if v > 0}

        # Return all values including the MODIFIED detected_objects
        return total_revenue, expected_profit, profit_percentage, display_objects, item_revenues



    def perform_detection_on_listing_images(self, model, listing_dir):
        """
        COMPLETELY FIXED: Now properly tracks confidence AND calculates revenue for EVERY detected item
        """
        if not os.path.isdir(listing_dir):
            return {}, [], {}, {}

        detected_objects = {class_name: [] for class_name in CLASS_NAMES}
        processed_images = []
        
        # FIXED: Track confidence for ALL classes, not just mutually exclusive ones
        max_confidence_per_class = {class_name: 0.0 for class_name in CLASS_NAMES}

        image_files = [f for f in os.listdir(listing_dir) if f.endswith('.png')]
        if not image_files:
            return {class_name: 0 for class_name in CLASS_NAMES}, processed_images, max_confidence_per_class, {}

        for image_file in image_files:
            image_path = os.path.join(listing_dir, image_file)
            try:
                img = cv2.imread(image_path)
                if img is None:
                    continue

                image_detections = {class_name: 0 for class_name in CLASS_NAMES}
                results = model(img, verbose=False)
                
                # Process each detection
                for result in results:
                    for box in result.boxes.cpu().numpy():
                        class_id = int(box.cls[0])
                        confidence = float(box.conf[0])
                        
                        if class_id < len(CLASS_NAMES):
                            class_name = CLASS_NAMES[class_id]
                            min_confidence = HIGHER_CONFIDENCE_ITEMS.get(class_name, GENERAL_CONFIDENCE_MIN)
                            
                            if confidence >= min_confidence:
                                # CRITICAL FIX: Update max confidence for ALL classes
                                max_confidence_per_class[class_name] = max(
                                    max_confidence_per_class[class_name], 
                                    confidence
                                )
                                
                                # Count detections (except mutually exclusive items)
                                if class_name not in ['switch', 'oled', 'lite', 'switch_box', 
                                                    'oled_box', 'lite_box', 'switch_in_tv', 'oled_in_tv']:
                                    image_detections[class_name] += 1
                                
                                # Draw bounding boxes
                                x1, y1, x2, y2 = map(int, box.xyxy[0])
                                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                cv2.putText(img, f"{class_name} ({confidence:.2f})", (x1, y1 - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.625, (0, 255, 0), 2)

                # Accumulate counts per class
                for class_name, count in image_detections.items():
                    detected_objects[class_name].append(count)

                # Store processed image
                processed_images.append(Image.fromarray(cv2.cvtColor(
                    cv2.copyMakeBorder(img, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=[0, 0, 0]),
                    cv2.COLOR_BGR2RGB)))

            except Exception as e:
                print(f"Error processing image {image_path}: {str(e)}")
                continue

        # Finalize counts (max across images)
        final_detected_objects = {
            class_name: max(counts) if counts else 0 
            for class_name, counts in detected_objects.items()
        }
        
        # Handle mutually exclusive items
        confidences_for_exclusive = {
            item: max_confidence_per_class[item] 
            for item in ['switch', 'oled', 'lite', 'switch_box', 'oled_box', 
                        'lite_box', 'switch_in_tv', 'oled_in_tv']
        }
        final_detected_objects = self.handle_mutually_exclusive_items_vinted(
            final_detected_objects, 
            confidences_for_exclusive
        )
        
        # Apply game deduplication
        vinted_game_classes = [
            '1_2_switch', 'animal_crossing', 'arceus_p', 'bow_z', 'bros_deluxe_m', 'crash_sand',
            'dance', 'diamond_p', 'evee', 'fifa_23', 'fifa_24', 'gta', 'just_dance', 'kart_m', 'kirby',
            'lets_go_p', 'links_z', 'luigis', 'mario_maker_2', 'mario_sonic', 'mario_tennis', 'minecraft',
            'minecraft_dungeons', 'minecraft_story', 'miscellanious_sonic', 'odyssey_m', 'other_mario',
            'party_m', 'rocket_league', 'scarlet_p', 'shield_p', 'shining_p', 'skywards_z', 'smash_bros',
            'snap_p', 'splatoon_2', 'splatoon_3', 'super_m_party', 'super_mario_3d', 'switch_sports',
            'sword_p', 'tears_z', 'violet_p'
        ]
        
        games_before_cap = {}
        for game_class in vinted_game_classes:
            if final_detected_objects.get(game_class, 0) > 1:
                games_before_cap[game_class] = final_detected_objects[game_class]
                final_detected_objects[game_class] = 1
        
        if games_before_cap:
            print("🎮 VINTED GAME DEDUPLICATION APPLIED:")
            for game, original_count in games_before_cap.items():
                print(f"  • {game}: {original_count} → 1")
        
        # Apply price threshold filtering
        try:
            listing_price = getattr(self, 'current_listing_price_float', 0.0)
            
            if listing_price > 0 and listing_price < PRICE_THRESHOLD:
                filtered_classes = []
                for switch_class in NINTENDO_SWITCH_CLASSES:
                    if final_detected_objects.get(switch_class, 0) > 0:
                        filtered_classes.append(switch_class)
                        final_detected_objects[switch_class] = 0
                        max_confidence_per_class[switch_class] = 0.0
                
                if filtered_classes:
                    print(f"🚫 PRICE FILTER: Removed Nintendo Switch detections (£{listing_price:.2f} < £{PRICE_THRESHOLD:.2f})")
        except Exception as price_filter_error:
            print(f"⚠️ Warning: Price filtering failed: {price_filter_error}")
        
        # CRITICAL FIX: Calculate per-item revenue HERE using detected counts
        all_prices = self.fetch_all_prices()
        item_revenues = {}
        
        for item, count in final_detected_objects.items():
            if count > 0 and item in all_prices:
                item_price = all_prices[item]
                item_revenue = item_price * count
                item_revenues[item] = item_revenue
                
                # DEBUG OUTPUT
                if print_debug:
                    print(f"💰 REVENUE: {item} × {count} = £{item_revenue:.2f} (confidence: {max_confidence_per_class[item]:.2%})")
        
        # Return: detected_objects, processed_images, confidences, revenues
        return final_detected_objects, processed_images, max_confidence_per_class, item_revenues

    def download_images_for_listing(self, driver, listing_dir):
        """
        ENHANCED: Download listing images with carousel detection for 5+ images
        - If 4 or fewer listing images: Use normal scraping (current behavior)
        - If 5+ listing images: Click an image to open carousel, then scrape from carousel
        """
        import concurrent.futures
        import requests
        from PIL import Image
        from io import BytesIO
        import os
        import hashlib
        
        # Wait for the page to fully load
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "img"))
            )
        except TimeoutException:
            print("  ▶ Timeout waiting for images to load")
            return []
        
        # STEP 1: Count listing images to determine which mode to use
        print("  ▶ STEP 1: Detecting listing image count...")
        
        listing_img_selectors = [
            "img.web_ui__Image__content[data-testid^='item-photo-']",
            "img[data-testid^='item-photo-']",
        ]
        
        listing_images = []
        for selector in listing_img_selectors:
            listing_images = driver.find_elements(By.CSS_SELECTOR, selector)
            if listing_images:
                print(f"  ▶ Found {len(listing_images)} listing images using selector: {selector}")
                break
        
        if not listing_images:
            print("  ▶ No listing images found")
            return []
        
        listing_image_count = len(listing_images)
        print(f"  ▶ Listing image count: {listing_image_count}")
        
        # STEP 2: Decide which mode to use based on count
        if listing_image_count <= 4:
            # NORMAL MODE: 4 or fewer images - use existing logic
            print(f"  ▶ MODE: NORMAL (≤4 images) - Using standard scraping")
            
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
            
            valid_urls = []
            seen_urls = set()
            
            if print_images_backend_info:
                print(f"  ▶ Processing {len(imgs)} images")
            
            for img in imgs:
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
                    # Remove query parameters and fragments for duplicate detection
                    normalized_url = src.split('?')[0].split('#')[0]
                    
                    if normalized_url in seen_urls:
                        if print_images_backend_info:
                            print(f"    ⏭️  Skipping duplicate URL: {normalized_url[:50]}...")
                        continue
                    
                    seen_urls.add(normalized_url)
                    
                    # Exclude profile pictures and small icons based on URL patterns
                    if (
                        '/50x50/' in src or 
                        '/75x75/' in src or 
                        '/100x100/' in src or
                        'circle' in parent_classes.lower() or
                        src.endswith('.svg') or
                        any(size in src for size in ['/32x32/', '/64x64/', '/128x128/'])
                    ):
                        if print_images_backend_info:
                            print(f"    ⏭️  Skipping filtered image: {src[:50]}...")
                        continue
                    
                    # Only include images that look like product photos
                    if (
                        '/f800/' in src or 
                        '/f1200/' in src or 
                        '/f600/' in src or
                        (('vinted' in src.lower() or 'cloudinary' in src.lower() or 'amazonaws' in src.lower()) and
                        not any(small_size in src for small_size in ['/50x', '/75x', '/100x', '/thumb']))
                    ):
                        valid_urls.append(src)
                        if print_images_backend_info:
                            print(f"    ✅ Added valid image URL: {src[:50]}...")
        
        else:
            # CAROUSEL MODE: 5+ images - click image to open carousel
            print(f"  ▶ MODE: CAROUSEL (>4 images) - Clicking image to open carousel")
            
            try:
                # STEP 3: Click on the first listing image to open carousel
                first_listing_image = listing_images[0]
                print(f"  ▶ STEP 2: Clicking first listing image to open carousel...")
                
                # Scroll into view
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", first_listing_image)
                time.sleep(0.5)
                
                # Try multiple click methods
                clicked = False
                
                # Method 1: Direct click
                try:
                    first_listing_image.click()
                    clicked = True
                    print(f"  ▶ ✅ Clicked image (direct click)")
                except Exception as e1:
                    print(f"  ▶ ⚠️ Direct click failed: {e1}")
                    
                    # Method 2: JavaScript click
                    try:
                        driver.execute_script("arguments[0].click();", first_listing_image)
                        clicked = True
                        print(f"  ▶ ✅ Clicked image (JavaScript click)")
                    except Exception as e2:
                        print(f"  ▶ ⚠️ JavaScript click failed: {e2}")
                        
                        # Method 3: ActionChains click
                        try:
                            from selenium.webdriver.common.action_chains import ActionChains
                            ActionChains(driver).move_to_element(first_listing_image).click().perform()
                            clicked = True
                            print(f"  ▶ ✅ Clicked image (ActionChains click)")
                        except Exception as e3:
                            print(f"  ▶ ❌ All click methods failed: {e3}")
                
                if not clicked:
                    print(f"  ▶ ❌ Failed to click image - falling back to normal mode")
                    # Fallback to normal mode logic - but avoid infinite recursion
                    # Just use the listing images we already found
                    valid_urls = []
                    seen_urls = set()
                    
                    for img in listing_images:
                        src = img.get_attribute("src")
                        if src and src.startswith('http'):
                            normalized_url = src.split('?')[0].split('#')[0]
                            if normalized_url not in seen_urls:
                                seen_urls.add(normalized_url)
                                valid_urls.append(src)
                else:
                    # STEP 4: Wait for carousel to appear
                    print(f"  ▶ STEP 3: Waiting for carousel to appear...")
                    time.sleep(1.5)  # Give carousel time to animate
                    
                    # STEP 5: Find all carousel images
                    print(f"  ▶ STEP 4: Scanning for carousel images...")
                    
                    carousel_selectors = [
                        'img[data-testid="image-carousel-image"]',
                        'img.image-carousel__image',
                        'img[alt="post"]',
                    ]
                    
                    carousel_images = []
                    for selector in carousel_selectors:
                        carousel_images = driver.find_elements(By.CSS_SELECTOR, selector)
                        if carousel_images:
                            print(f"  ▶ Found {len(carousel_images)} carousel images using selector: {selector}")
                            break
                    
                    if not carousel_images:
                        print(f"  ▶ ⚠️ No carousel images found - using listing images as fallback")
                        # Use the listing images we already found
                        valid_urls = []
                        seen_urls = set()
                        
                        for img in listing_images:
                            src = img.get_attribute("src")
                            if src and src.startswith('http'):
                                normalized_url = src.split('?')[0].split('#')[0]
                                if normalized_url not in seen_urls:
                                    seen_urls.add(normalized_url)
                                    valid_urls.append(src)
                    else:
                        # STEP 6: Extract URLs from carousel images
                        valid_urls = []
                        seen_urls = set()
                        
                        print(f"  ▶ STEP 5: Extracting URLs from {len(carousel_images)} carousel images...")
                        
                        for idx, img in enumerate(carousel_images):
                            src = img.get_attribute("src")
                            
                            if src and src.startswith('http'):
                                # Remove query parameters and fragments for duplicate detection
                                normalized_url = src.split('?')[0].split('#')[0]
                                
                                if normalized_url in seen_urls:
                                    if print_images_backend_info:
                                        print(f"    ⏭️  Skipping duplicate carousel URL: {normalized_url[:50]}...")
                                    continue
                                
                                seen_urls.add(normalized_url)
                                
                                # Carousel images are always valid listing images, no filtering needed
                                valid_urls.append(src)
                                if print_images_backend_info:
                                    print(f"    ✅ Added carousel image URL {idx+1}: {src[:50]}...")
                        
                        # OPTIMIZATION: No need to close carousel - tab will be closed immediately after this
                        print(f"  ▶ STEP 6: Carousel will be closed when tab closes (optimization)")
            
            except Exception as carousel_error:
                print(f"  ▶ ❌ Carousel mode error: {carousel_error}")
                print(f"  ▶ Falling back to listing images...")
                import traceback
                traceback.print_exc()
                # Fallback: use the listing images we already found
                valid_urls = []
                seen_urls = set()
                
                for img in listing_images:
                    src = img.get_attribute("src")
                    if src and src.startswith('http'):
                        normalized_url = src.split('?')[0].split('#')[0]
                        if normalized_url not in seen_urls:
                            seen_urls.add(normalized_url)
                            valid_urls.append(src)
        
        # STEP 7/8: Download images (same for both modes)
        if not valid_urls:
            print(f"  ▶ No valid product images found after filtering")
            return []

        if print_images_backend_info:
            print(f"  ▶ Final count: {len(valid_urls)} unique, valid product images")
        
        os.makedirs(listing_dir, exist_ok=True)
        
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
                
                # Use content hash to detect identical images with different URLs
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
                    if print_images_backend_info:
                        print(f"    ⏭️  Skipping small image: {img.width}x{img.height}")
                    return None
                
                # Resize image for YOLO detection optimization
                MAX_SIZE = (1000, 1000)
                if img.width > MAX_SIZE[0] or img.height > MAX_SIZE[1]:
                    img.thumbnail(MAX_SIZE, Image.LANCZOS)
                    if print_images_backend_info:
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
        
        # Dynamic batch size based on actual image count
        batch_size = len(valid_urls)
        max_workers = min(6, batch_size)
        
        if print_images_backend_info:
            print(f"  ▶ Batch size set to: {batch_size}")
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
                if result:
                    downloaded_paths.append(result)

        print(f"  ▶ Successfully downloaded {len(downloaded_paths)} unique images (from {len(valid_urls)} URLs)")
        
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
        
        try:
            driver.get(f"{BASE_URL}?{urlencode(params)}")
        except (TimeoutException, WebDriverException) as e:
            print(f"❌ Page load failed: {e}")
            print("🔄 Restarting driver...")
            try:
                driver.quit()
            except:
                pass
            driver = self.setup_driver()
            driver.get(f"{BASE_URL}?{urlencode(params)}")
            return driver
        
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
        
        return driver

    def search_vinted_with_refresh(self, driver, search_query):
        """
        Enhanced search_vinted method with refresh and rescan functionality
        UPDATED: Now restarts the main driver every 250 cycles to prevent freezing
        """
        global suitable_listings, current_listing_index
        
        # CLEAR THE VINTED SCANNED IDS FILE AT THE BEGINNING OF EACH RUN
        try:
            with open(VINTED_SCANNED_IDS_FILE, 'w') as f:
                pass
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
        DRIVER_RESTART_INTERVAL = 100000
        cycles_since_restart = 0

        # INITIAL NAVIGATION: Navigate to Vinted search on first startup
        params = {
            "search_text": search_query,
            "price_from": PRICE_FROM,
            "price_to": PRICE_TO,
            "currency": CURRENCY,
            "order": ORDER,
        }
        print("🔄 Initial navigation to Vinted catalog...")
        current_driver.get(f"{BASE_URL}?{urlencode(params)}")
        print("✅ Navigated to Vinted catalog successfully")
        time.sleep(2)

        # Main scanning loop with refresh functionality AND driver restart
        while True:
            print(f"\n{'='*60}")
            print(f"🔍 STARTING REFRESH CYCLE {refresh_cycle}")
            print(f"🔄 Cycles since last driver restart: {cycles_since_restart}")
            print(f"{'='*60}")
            
            try:
                # NEW: Check if we need to restart the driver
                if cycles_since_restart >= DRIVER_RESTART_INTERVAL:
                    print(f"\n🔄 DRIVER RESTART: Reached {DRIVER_RESTART_INTERVAL} cycles")
                    print("🔄 RESTARTING: Main scraping driver to prevent freezing...")
                    
                    try:
                        print("🔄 CLOSING: Current driver...")
                        current_driver.quit()
                        time.sleep(2)
                        
                        print("🔄 CREATING: New driver...")
                        current_driver = self.setup_driver()
                        
                        if current_driver is None:
                            print("❌ CRITICAL: Failed to create new driver after restart")
                            break
                        
                        print("✅ DRIVER RESTART: Successfully restarted main driver")
                        cycles_since_restart = 0
                        
                        params = {
                            "search_text": search_query,
                            "price_from": PRICE_FROM,
                            "price_to": PRICE_TO,
                            "currency": CURRENCY,
                            "order": ORDER,
                        }
                        current_driver.get(f"{BASE_URL}?{urlencode(params)}")
                        
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
                
                cycle_listing_counter = 0
                found_already_scanned = False
                
                page = 1
                
                while True:
                    try:
                        WebDriverWait(current_driver, 20).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "div.feed-grid"))
                        )
                    except TimeoutException:
                        print("⚠️ Timeout waiting for page to load - moving to next cycle")
                        break

                    els = current_driver.find_elements(By.CSS_SELECTOR, "a.new-item-box__overlay")
                    urls = [e.get_attribute("href") for e in els if e.get_attribute("href")]
                    
                    if not urls:
                        print(f"📄 No listings found on page {page} - moving to next cycle")
                        break

                    print(f"📄 Processing page {page} with {len(urls)} listings")

                    for idx, url in enumerate(urls, start=1):
                        cycle_listing_counter += 1
                        
                        print(f"[Cycle {refresh_cycle} · Page {page} · Item {idx}/{len(urls)}] #{overall_listing_counter}")
                        
                        listing_id = self.extract_vinted_listing_id(url)
                        
                        if REFRESH_AND_RESCAN and listing_id:
                            if listing_id in scanned_ids:
                                print(f"🔁 DUPLICATE DETECTED: Listing ID {listing_id} already scanned")
                                print(f"🔄 Initiating refresh and rescan process...")
                                found_already_scanned = True
                                break
                        
                        if REFRESH_AND_RESCAN and cycle_listing_counter > MAX_LISTINGS_VINTED_TO_SCAN:
                            print(f"📊 Reached MAX_LISTINGS_VINTED_TO_SCAN ({MAX_LISTINGS_VINTED_TO_SCAN})")
                            print(f"🔄 Initiating refresh cycle...")
                            break

                        overall_listing_counter += 1

                        current_driver.execute_script("window.open();")
                        current_driver.switch_to.window(current_driver.window_handles[-1])
                        current_driver.get(url)

                        self.record_listing_timestamp(url, 'navigated')

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

                            listing_dir = os.path.join(DOWNLOAD_ROOT, f"listing {overall_listing_counter}")
                            image_paths = self.download_images_for_listing(current_driver, listing_dir)

                            detected_objects = {}
                            processed_images = []
                            all_confidences = {}
                            item_revenues = {}

                            if model and image_paths:
                                detected_objects, processed_images, all_confidences, item_revenues = \
                                    self.perform_detection_on_listing_images(model, listing_dir)
                                
                                detected_classes = [cls for cls, count in detected_objects.items() if count > 0]
                                if detected_classes:
                                    print("📊 DETECTED ITEMS:")
                                    for cls in sorted(detected_classes):
                                        confidence = all_confidences.get(cls, 0.0)
                                        revenue = item_revenues.get(cls, 0.0)
                                        print(f"  • {cls}: count={detected_objects[cls]} conf={confidence:.1%} rev=£{revenue:.2f}")

                            self.process_vinted_listing(
                                details, 
                                detected_objects, 
                                processed_images, 
                                overall_listing_counter, 
                                url, 
                                all_confidences,
                                item_revenues
                            )
                            
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
                            if listing_id:
                                scanned_ids.add(listing_id)
                                self.save_vinted_listing_id(listing_id)

                        finally:
                            current_driver.close()
                            current_driver.switch_to.window(current_driver.window_handles[0])

                    if found_already_scanned or (REFRESH_AND_RESCAN and cycle_listing_counter > MAX_LISTINGS_VINTED_TO_SCAN):
                        break

                    try:
                        nxt = current_driver.find_element(By.CSS_SELECTOR, "a[data-testid='pagination-arrow-right']")
                        current_driver.execute_script("arguments[0].click();", nxt)
                        page += 1
                        time.sleep(2)
                    except NoSuchElementException:
                        print("📄 No more pages available - moving to next cycle")
                        break

                if not REFRESH_AND_RESCAN:
                    print("🏁 REFRESH_AND_RESCAN disabled - ending scan")
                    break
                
                if found_already_scanned:
                    print(f"🔁 Found already scanned listing - refreshing immediately")
                    current_driver = self.refresh_vinted_page_and_wait(current_driver, is_first_refresh)
                elif cycle_listing_counter > MAX_LISTINGS_VINTED_TO_SCAN:
                    print(f"📊 Reached maximum listings ({MAX_LISTINGS_VINTED_TO_SCAN}) - refreshing")
                    current_driver = self.refresh_vinted_page_and_wait(current_driver, is_first_refresh)
                else:
                    print("📄 No more pages and no max reached - refreshing for new listings")
                    current_driver = self.refresh_vinted_page_and_wait(current_driver, is_first_refresh)

                refresh_cycle += 1
                cycles_since_restart += 1
                is_first_refresh = False
                
            except (TimeoutException, WebDriverException) as e:
                print(f"❌ Error in main loop: {e}")
                print("🔄 Restarting driver and continuing...")
                try:
                    current_driver.quit()
                except:
                    pass
                current_driver = self.setup_driver()
                cycles_since_restart = 0
                continue

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
        """Simplified run method without internal booking/buying functionality"""
        global suitable_listings, current_listing_index, recent_listings, current_listing_title, current_listing_price
        global current_listing_description, current_listing_join_date, current_detected_items, current_profit
        global current_listing_images, current_listing_url, current_suitability, current_expected_revenue
        
        # Check for test modes (keep existing test mode logic)
        if TEST_WHETHER_SUITABLE:
            # [Keep existing TEST_WHETHER_SUITABLE code unchanged]
            pass
            
        if TEST_NUMBER_OF_LISTINGS:
            # [Keep existing TEST_NUMBER_OF_LISTINGS code unchanged]
            pass
        
        # Remove TEST_BOOKMARK_BUYING_FUNCTIONALITY, BOOKMARK_TEST_MODE, BUYING_TEST_MODE blocks
        
        # Initialize ALL global variables properly
        suitable_listings = []
        current_listing_index = 0
        
        # Initialize recent_listings for website navigation
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
        current_seller_reviews = "No reviews yet"
        
        # Initialize pygame display with default values
        self.update_listing_details("", "", "", "0", 0, 0, {}, [], {})
        
        # Start Flask app in separate thread
        flask_thread = threading.Thread(target=self.run_flask_app)
        flask_thread.daemon = True
        flask_thread.start()
        
        # Main scraping driver thread
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
                
                # Clean up VM driver too
                try:
                    if self.current_vm_driver:
                        self.current_vm_driver.quit()
                        print("✅ SCRAPING THREAD: VM driver closed")
                except:
                    print("⚠️ SCRAPING THREAD: Error closing VM driver")
                    
                pygame.quit()
                time.sleep(2)
                print("🏁 SCRAPING THREAD: Main scraping thread completed")
        
        # Create and start the main scraping thread
        print("🧵 MAIN: Creating main scraping driver thread...")
        scraping_thread = Thread(target=main_scraping_driver, name="Main-Scraping-Thread")
        scraping_thread.daemon = False
        scraping_thread.start()

        # Start pygame window in separate thread
        pygame_thread = threading.Thread(target=self.run_pygame_window)
        pygame_thread.start()
        
        print("🧵 MAIN: Main scraping driver thread started")
        print("🧵 MAIN: Main thread will now wait for scraping thread to complete...")
        
        try:
            # Wait for the scraping thread to complete
            scraping_thread.join()
            print("✅ MAIN: Scraping thread completed successfully")
            
        except KeyboardInterrupt:
            print("\n🛑 MAIN: Keyboard interrupt received")
            print("⏳ MAIN: Waiting for scraping thread to finish...")
            scraping_thread.join(timeout=30)
            
            if scraping_thread.is_alive():
                print("⚠️ MAIN: Scraping thread still alive after timeout")
            else:
                print("✅ MAIN: Scraping thread finished cleanly")
        
        except Exception as main_error:
            print(f"❌ MAIN THREAD ERROR: {main_error}")
            
        finally:
            print("🏁 MAIN: Program ending, final cleanup...")
            print("🏁 MAIN: Program exit")
            sys.exit(0)

if __name__ == "__main__":

    scraper = VintedScraper()
    globals()['vinted_scraper_instance'] = scraper
    scraper.run()