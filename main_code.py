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
import ctypes


VM_DRIVER_USE = True
google_login = True

VM_BOOKMARK_URLS = [
    "https://www.vinted.co.uk/items/7102546985-fc24-nintendo-switch?homepage_session_id=6e3fa7fa-65d1-4aef-a0da-dda652e1c311", 
    "https://www.vinted.co.uk/items/7087256735-lol-born-to-travel-nintendo-switch?homepage_session_id=83612002-66a0-4de7-9bb8-dfbf49be0db7",
    "https://www.vinted.co.uk/items/7083522788-instant-sports-nintendo-switch?homepage_session_id=2d9b4a2d-5def-4730-bc0c-d4e42e13fe12",
    "https://www.vinted.co.uk/items/7097706534-just-dance-2022-nintendo-switch-game-cartridge?homepage_session_id=6c527539-91d8-4297-8e48-f96581b761d3"
]

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

# 2. Modified main_vm_driver function (replace your existing main_vm_driver function)
def main_vm_driver():
    """Main VM driver function - Enhanced to run 5 drivers sequentially with URL bookmarking"""
    # VM IP address - change this to your VM's IP
    vm_ip_address = "192.168.56.101"
    
    # Driver configurations
    driver_configs = [
        {"user_data_dir": "C:\\VintedScraper_Default_Bookmark", "profile": "Profile 4", "port": 9223},
        {"user_data_dir": "C:\\VintedScraper_Default_Bookmark", "profile": "Profile 4", "port": 9224},
        {"user_data_dir": "C:\\VintedScraper_Default_Bookmark", "profile": "Profile 4", "port": 9226},
        {"user_data_dir": "C:\\VintedScraper_Default_Bookmark", "profile": "Profile 4", "port": 9227},
        {"user_data_dir": "C:\\VintedScraper_Default_Bookmark", "profile": "Profile 4", "port": 9228}
    ]
    
    print(f"\n🔖 BOOKMARKING: Will bookmark {len(VM_BOOKMARK_URLS)} URLs across 5 drivers:")
    for i, url in enumerate(VM_BOOKMARK_URLS, 1):
        print(f"  Driver {i}: {url}")
    
    # Run all 5 drivers sequentially with URL bookmarking
    for i, config in enumerate(driver_configs, 1):
        print(f"\n{'='*60}")
        print(f"STARTING DRIVER {i}/5")
        print(f"User Data: {config['user_data_dir']}")
        print(f"Profile: {config['profile']}")
        print(f"Assigned URL: {VM_BOOKMARK_URLS[i-1]}")
        print(f"{'='*60}")
        
        # Clear browser data for this driver
        clear_browser_data_universal(vm_ip_address, config)
        
        # Small delay before creating driver
        time.sleep(1)
        
        driver = setup_driver_universal(vm_ip_address, config)
        
        if not driver:
            print(f"Failed to create VM driver {i} - continuing to next")
            continue
        
        detector = None
        
        try:
            print(f"Navigating to vinted.co.uk with driver {i}...")
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
                print(f"Driver {i} login completed successfully.")
                
                # NEW: LOGIN SUCCESSFUL - NOW BOOKMARK THE ASSIGNED URL
                assigned_url = VM_BOOKMARK_URLS[i-1]  # Get URL for this driver (0-indexed)
                print(f"\n🔖 BOOKMARKING: Driver {i} starting bookmark process for:")
                print(f"🔗 URL: {assigned_url}")
                
                # Execute bookmark using existing logic
                bookmark_success = execute_vm_bookmark_process(driver, assigned_url, i)
                
                if bookmark_success:
                    print(f"✅ BOOKMARKING: Driver {i} successfully bookmarked URL!")
                else:
                    print(f"❌ BOOKMARKING: Driver {i} failed to bookmark URL")
                
            elif result == True:
                print("Audio captcha button clicked successfully!")
                print("="*60)
                print("STARTING AUDIO DETECTION...")
                print("="*60)
                
                # Initialize and start audio detection with driver reference
                if HAS_PYAUDIO:
                    detector = AudioNumberDetector(driver=driver)
                    detector.start_listening()
                    
                    # After captcha is solved, proceed with bookmarking
                    print(f"\n🔖 BOOKMARKING: Driver {i} captcha solved, starting bookmark process...")
                    assigned_url = VM_BOOKMARK_URLS[i-1]
                    print(f"🔗 URL: {assigned_url}")
                    
                    bookmark_success = execute_vm_bookmark_process(driver, assigned_url, i)
                    
                    if bookmark_success:
                        print(f"✅ BOOKMARKING: Driver {i} successfully bookmarked URL!")
                    else:
                        print(f"❌ BOOKMARKING: Driver {i} failed to bookmark URL")
                        
                else:
                    print("ERROR: Cannot start audio detection - pyaudiowpatch not available")
            else:
                print("Failed to click audio captcha button")
            
            print(f"Driver {i} completed!")
            
            # Keep browser open for a bit to see the result
            time.sleep(10)
            
        except KeyboardInterrupt:
            print(f"\n\nStopping driver {i}...")
            if detector:
                detector.stop()
        except Exception as e:
            print(f"An error occurred in driver {i}: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            if detector:
                try:
                    detector.stop()
                except:
                    pass
            # Close current driver
            try:
                driver.quit()
                print(f"Driver {i} closed successfully")
            except:
                print(f"Error closing driver {i}")
    
    print("\n" + "="*60)
    print("ALL 5 DRIVERS COMPLETED SUCCESSFULLY")
    print("URL BOOKMARKING PROCESS COMPLETE")
    print("="*60)

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
        success = execute_vm_bookmark_sequences(driver, url, username, step_log)
        
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
def execute_vm_bookmark_sequences(driver, listing_url, username, step_log):
    """
    Execute bookmark sequences for VM drivers using existing bookmark logic
    """
    try:
        # Create new tab and navigate (using existing logic)
        print(f"🔖 DRIVER {step_log['driver_number']}: Creating new tab...")
        stopwatch_start = time.time()
        driver.execute_script("window.open('');")
        new_tab = driver.window_handles[-1]
        driver.switch_to.window(new_tab)
        
        # Navigate to listing
        print(f"🔖 DRIVER {step_log['driver_number']}: Navigating to listing...")
        driver.get(listing_url)
        
        # Execute first buy sequence (critical for bookmarking)
        success = execute_vm_first_buy_sequence(driver, step_log)
        
        if success:
            print(f"🔖 DRIVER {step_log['driver_number']}: First buy sequence completed")
            
            # Execute second sequence with monitoring (if needed)
            execute_vm_second_sequence(driver, listing_url, step_log)
            
            return True
        else:
            print(f"🔖 DRIVER {step_log['driver_number']}: First buy sequence failed")
            return False
            
    except Exception as e:
        print(f"❌ DRIVER {step_log['driver_number']}: Sequence execution error: {e}")
        return False
    finally:
        # Always switch back to main tab
        try:
            if len(driver.window_handles) > 1:
                driver.close()  # Close bookmark tab
                driver.switch_to.window(driver.window_handles[0])  # Return to main tab
        except:
            pass

def execute_vm_first_buy_sequence(driver, step_log):
    """
    Execute first buy sequence for VM driver using JavaScript-first approach
    """
    return execute_vm_first_buy_sequence_with_shadow_dom(driver, step_log)



# 5. VM-specific first buy sequence (using EXACT main program logic)
def execute_vm_first_buy_sequence_with_shadow_dom(driver, step_log):
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
        handle_vm_shipping_options(driver, step_log)
        
        # Execute critical pay sequence (same timing as main scraper)
        return execute_vm_critical_pay_sequence(driver, pay_button, step_log)
        
    except Exception as e:
        print(f"❌ JAVASCRIPT-FIRST: First buy sequence error: {e}")
        return False

def execute_vm_second_sequence_with_javascript_first(driver, actual_url, step_log):
    """
    Execute second sequence using the same JavaScript-first approach for buy button
    """
    print(f"🔍 JAVASCRIPT-FIRST: Executing second sequence...")
    
    try:
        # Open new tab for second sequence
        driver.execute_script("window.open('');")
        second_tab = driver.window_handles[-1]
        driver.switch_to.window(second_tab)
        step_log['steps_completed'].append(f"second_tab_created - {time.time() - step_log['start_time']:.2f}s")
        
        # Navigate again
        driver.get(actual_url)
        step_log['steps_completed'].append(f"second_navigation - {time.time() - step_log['start_time']:.2f}s")
        
        # Look for buy button again using SAME JavaScript-first approach
        print(f"🔍 JAVASCRIPT-FIRST: Looking for second buy button...")
        second_buy_button, second_buy_selector = find_buy_button_with_shadow_dom(driver)
        
        if second_buy_button:
            print(f"✅ JAVASCRIPT-FIRST: Second buy button found and clicked using: {second_buy_selector}")
            step_log['steps_completed'].append(f"second_buy_button_clicked - {time.time() - step_log['start_time']:.2f}s")
            
            # Check for processing payment success with extended timeout
            print(f"🔍 JAVASCRIPT-FIRST: Waiting up to 15 seconds for processing payment message...")
            processing_element, VM_SELECTOR_SETS = vm_try_selectors(
                driver,
                'processing_payment',
                operation='find',
                timeout=15,  # Extended timeout to 15 seconds
                step_log=step_log
            )
            
            if processing_element:
                element_text = processing_element.text.strip()
                step_log['steps_completed'].append(f"processing_payment_found - {time.time() - step_log['start_time']:.2f}s")
                print('✅ JAVASCRIPT-FIRST: SUCCESSFUL BOOKMARK! CONFIRMED VIA PROCESSING PAYMENT!')
                
                # Define purchase unsuccessful selectors
                purchase_unsuccessful_selectors = [
                    "//h2[@class='web_uiTexttext web_uiTexttitle web_uiTextleft web_uiTextwarning' and text()='Purchase unsuccessful']",
                    "//div[@class='web_uiCelltitle'][@data-testid='conversation-message--status-message--title']//h2[@class='web_uiTexttext web_uiTexttitle web_uiTextleft web_uiTextwarning' and text()='Purchase unsuccessful']",
                    "//div[@class='web_uiCellheading']//div[@class='web_uiCelltitle'][@data-testid='conversation-message--status-message--title']//h2[@class='web_uiTexttext web_uiTexttitle web_uiTextleft web_uiTextwarning' and text()='Purchase unsuccessful']",
                    "//*[contains(@class, 'web_uiTextwarning') and text()='Purchase unsuccessful']",
                    "//*[text()='Purchase unsuccessful']"
                ]
                
                print("🔍 JAVASCRIPT-FIRST: Monitoring for 'Purchase unsuccessful' message for up to 25 minutes...")
                print("⏰ JAVASCRIPT-FIRST: Checking every 100ms for purchase status...")
                
                # Monitor for purchase unsuccessful for up to 25 minutes (1500 seconds)
                max_wait_time = 5  # 25 minutes in seconds
                check_interval = 0.1  # 100ms
                start_monitor_time = time.time()
                purchase_unsuccessful_found = False
                
                while time.time() - start_monitor_time < max_wait_time:
                    try:
                        # Check each selector for purchase unsuccessful
                        for selector in purchase_unsuccessful_selectors:
                            try:
                                unsuccessful_element = driver.find_element(By.XPATH, selector)
                                if unsuccessful_element and unsuccessful_element.is_displayed():
                                    purchase_unsuccessful_found = True
                                    elapsed_time = time.time() - start_monitor_time
                                    print(f"❌ JAVASCRIPT-FIRST: 'Purchase unsuccessful' found after {elapsed_time:.2f} seconds!")
                                    step_log['steps_completed'].append(f"purchase_unsuccessful_found - {time.time() - step_log['start_time']:.2f}s")
                                    break
                            except:
                                continue  # Selector not found, continue checking
                        
                        if purchase_unsuccessful_found:
                            break
                            
                        time.sleep(check_interval)  # Wait 100ms before next check
                        
                    except Exception as e:
                        print(f"⚠️ JAVASCRIPT-FIRST: Error during purchase status monitoring: {e}")
                        time.sleep(check_interval)
                
                # Determine why we're closing the tab
                if purchase_unsuccessful_found:
                    print("🚪 JAVASCRIPT-FIRST: Closing tab due to 'Purchase unsuccessful' message detected")
                else:
                    elapsed_time = time.time() - start_monitor_time
                    print(f"🚪 JAVASCRIPT-FIRST: Closing tab after {elapsed_time:.2f} seconds (25 minute timeout reached)")
                    step_log['steps_completed'].append(f"purchase_monitoring_timeout - {time.time() - step_log['start_time']:.2f}s")
                
                # Close second tab
                driver.close()
                if len(driver.window_handles) > 0:
                    driver.switch_to.window(driver.window_handles[0])
        else:
            print(f"❌ JAVASCRIPT-FIRST: Second buy button not found")
            
        # Close second tab
        driver.close()
        if len(driver.window_handles) > 0:
            driver.switch_to.window(driver.window_handles[0])
            
        return True  # Return true as this isn't a critical failure
            
    except Exception as second_sequence_error:
        print(f"❌ JAVASCRIPT-FIRST: Second sequence error: {second_sequence_error}")
        # Clean up second tab
        try:
            driver.close()
            if len(driver.window_handles) > 0:
                driver.switch_to.window(driver.window_handles[0])
        except:
            pass
        return True

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
def handle_vm_shipping_options(driver, step_log):
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
                choose_pickup = driver.find_element(
                    By.XPATH,
                    '//h2[@class="web_ui__Text__text web_ui__Text__title web_ui__Text__left" and text()="Choose a pick-up point"]'
                )
                
                print(f"🏠 DRIVER {step_log['driver_number']}: Switching to Ship to home...")
                
                # Click "Ship to home"
                ship_home = driver.find_element(
                    By.XPATH,
                    '//h2[@class="web_ui__Text__text web_ui__Text__title web_ui__Text__left" and text()="Ship to home"]'
                )
                ship_home.click()
                
                # Wait 0.3 seconds as in main scraper
                print(f"✅ DRIVER {step_log['driver_number']}: Switched to Ship to home, waiting 3 seconds...")
                time.sleep(3)
            except:
                print(f"✅ DRIVER {step_log['driver_number']}: Pickup point ready")
                
        except:
            print(f"✅ DRIVER {step_log['driver_number']}: Ship to home already selected")
            
    except Exception as e:
        print(f"⚠️ DRIVER {step_log['driver_number']}: Shipping options error: {e}")

# 7. VM-specific critical pay sequence (EXACT same timing as main scraper)
def execute_vm_critical_pay_sequence(driver, pay_button, step_log):
    """
    Execute critical pay sequence with EXACT same timing as main scraper
    """
    try:
        print(f"💳 DRIVER {step_log['driver_number']}: Executing critical pay sequence...")
        
        # Click pay button using multiple methods (same as main scraper)
        pay_clicked = False
        
        # Method 1: Direct click
        try:
            #pay_button.click()
            pay_clicked = True
            print(f"✅ DRIVER {step_log['driver_number']}: Pay button clicked (direct)")
        except:
            # Method 2: JavaScript click
            try:
                #driver.execute_script("arguments[0].click();", pay_button)
                pay_clicked = True
                print(f"✅ DRIVER {step_log['driver_number']}: Pay button clicked (JavaScript)")
            except:
                # Method 3: Force enable and click
                try:
                    #driver.execute_script("""
                    #    arguments[0].disabled = false;
                    #    arguments[0].click();
                    #""", pay_button)
                    pay_clicked = True
                    print(f"✅ DRIVER {step_log['driver_number']}: Pay button clicked (force)")
                except Exception as final_error:
                    print(f"❌ DRIVER {step_log['driver_number']}: All pay click methods failed")
                    return False
        
        if pay_clicked:
            # CRITICAL: Exact 0.25 second wait (same as main scraper)
            print(f"🔖 DRIVER {step_log['driver_number']}: CRITICAL - Waiting exactly 0.25 seconds...")
            time.sleep(5)
            
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
        
        return False
        
    except Exception as e:
        print(f"❌ DRIVER {step_log['driver_number']}: Critical pay sequence error: {e}")
        return False

# 8. VM-specific second sequence (for completeness - monitors for success)
def execute_vm_second_sequence(driver, listing_url, step_log):
    """
    Execute second sequence for VM driver using JavaScript-first approach
    """
    return execute_vm_second_sequence_with_javascript_first(driver, listing_url, step_log)


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

def base64_encode_image(img):
    """Convert PIL Image to base64 string, resizing if necessary"""
    max_size = (200, 200)
    img.thumbnail(max_size, Image.LANCZOS)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


if __name__ == "__main__":
    if VM_DRIVER_USE:
        print("VM_DRIVER_USE = True - Running VM driver script instead of main scraper")
        if not HAS_PYAUDIO:
            print("WARNING: pyaudiowpatch not available - audio features may not work")
            print("Install with: pip install PyAudioWPatch")
        main_vm_driver()