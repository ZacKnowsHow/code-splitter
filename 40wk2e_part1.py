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
from scipy import signal
import wave
import ctypes

#uses custom url for buying in vm, for testing. works same as normal, just with custom url instead.

CLICK_PAY_BUTTON = False

VM_DRIVER_USE = False
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

VINTED_SHOW_ALL_LISTINGS = True
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
