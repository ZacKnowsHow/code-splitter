programme_to_run = 1
#0 = facebook
#1 = vinted

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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
BOOKMARK_TEST_URL = "https://www.vinted.co.uk/items/6990793592-new-look-handbag-black-fake-leather?referrer=catalog"
BOOKMARK_TEST_USERNAME = "leah_lane" 

#tests the buying functionality
BUYING_TEST_MODE = False
BUYING_TEST_URL = "https://www.vinted.co.uk/items/6966124363-mens-t-shirt-bundle-x-3-ml?homepage_session_id=932d30be-02f5-4f54-9616-c412dd6e9da2"

#tests both the bookmark and buying functionality
TEST_BOOKMARK_BUYING_FUNCTIONALITY = False
TEST_BOOKMARK_BUYING_URL = "https://www.vinted.co.uk/items/6989925386-green-and-yellow-chunky-bracelet?referrer=catalog"

PRICE_THRESHOLD = 30.0  # Minimum price threshold - items below this won't detect Nintendo Switch classes
NINTENDO_SWITCH_CLASSES = [
    'controller','tv_black', 
    'tv_white', 'comfort_h',
    'comfort_h_joy', 'switch_box', 'switch', 'switch_in_tv',
]

debug_threads = True
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
        self.driver_lock = threading.Lock()
        
        self.driver_threads = {}  # Store active threads for each driver
        self.thread_lock = Lock()  # Thread safety
        self.shutdown_event = Event()  # Global shutdown signal
        
        # Initialize driver thread tracking
        for i in range(1, 6):
            self.driver_threads[i] = None  # Thread safety for driver management
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
        THREADED: Find and reserve the first available driver with threading support
        Each driver runs in its own dedicated thread
        """
        with self.driver_lock:
            for driver_num in range(1, 6):  # Check drivers 1-5
                # Skip drivers that are currently busy
                if self.driver_status[driver_num] == 'busy':
                    continue
                
                # Check if thread is still active
                if (self.driver_threads[driver_num] and 
                    self.driver_threads[driver_num].is_alive()):
                    continue
                    
                # Reserve this driver slot
                self.driver_status[driver_num] = 'busy'
                
                # SPECIAL HANDLING FOR DRIVER 1 - use persistent_buying_driver
                if driver_num == 1:
                    print(f"🚗 DRIVER 1: Using persistent buying driver in thread")
                    
                    # Check if persistent driver exists and is alive
                    if self.persistent_buying_driver is None or self.is_persistent_driver_dead():
                        print(f"🚗 DRIVER 1: Persistent driver is dead, recreating...")
                        if not self.setup_persistent_buying_driver():
                            print(f"❌ DRIVER 1: Failed to recreate persistent driver")
                            self.driver_status[driver_num] = 'not_created'
                            continue
                    
                    print(f"✅ RESERVED: Persistent buying driver (driver 1) for threading")
                    return driver_num, self.persistent_buying_driver
                    
                # For drivers 2-5, create on demand
                else:
                    if self.buying_drivers[driver_num] is None or self.is_driver_dead(driver_num):
                        print(f"🚗 CREATING: Buying driver {driver_num} for threading")
                        new_driver = self.setup_buying_driver(driver_num)
                        
                        if new_driver is None:
                            print(f"❌ FAILED: Could not create buying driver {driver_num}")
                            self.driver_status[driver_num] = 'not_created'
                            continue
                            
                        self.buying_drivers[driver_num] = new_driver
                        print(f"✅ CREATED: Buying driver {driver_num} successfully for threading")
                    
                    print(f"✅ RESERVED: Buying driver {driver_num} for threading")
                    return driver_num, self.buying_drivers[driver_num]
            
            print("❌ ERROR: All 5 buying drivers are currently busy")
            return None, None
   
    def process_listing_in_thread(self, url, driver_num, driver):
        """
        NEW: Process a single listing in a dedicated thread
        This ensures each driver runs independently without blocking others
        """
        thread_id = threading.current_thread().ident
        print(f"🧵 THREAD {thread_id}: Starting processing on driver {driver_num}")
        
        try:
            # Set thread-local data
            threading.current_thread().driver_num = driver_num
            threading.current_thread().processing_url = url
            
            # Call the existing processing method
            if wait_for_bookmark_stopwatch_to_buy:
                self.process_single_listing_with_driver_modified(url, driver_num, driver)
            else:
                self.process_single_listing_with_driver(url, driver_num, driver)
                
            print(f"🧵 THREAD {thread_id}: Completed processing on driver {driver_num}")
            
        except Exception as thread_error:
            print(f"🧵 THREAD {thread_id}: Error on driver {driver_num}: {thread_error}")
            
        finally:
            # Clean up thread reference
            with self.thread_lock:
                if driver_num in self.driver_threads:
                    self.driver_threads[driver_num] = None
            
            print(f"🧵 THREAD {thread_id}: Thread cleanup completed for driver {driver_num}")

    
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
        THREADED: Release a driver back to the free pool with thread safety
        """
        with self.driver_lock:
            print(f"🔓 RELEASING: Buying driver {driver_num}")
            
            # Mark thread as completed (it will be cleaned up by monitor)
            if driver_num in self.driver_threads and self.driver_threads[driver_num]:
                print(f"🧵 MARKING: Thread for driver {driver_num} as completed")
            
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
