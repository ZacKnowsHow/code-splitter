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
BOOKMARK_TEST_URL = "https://www.vinted.co.uk/items/4402812396-paper-back-book?referrer=catalog"
BOOKMARK_TEST_USERNAME = "leah_lane" 

#tests the buying functionality
BUYING_TEST_MODE = False
BUYING_TEST_URL = "https://www.vinted.co.uk/items/6966124363-mens-t-shirt-bundle-x-3-ml?homepage_session_id=932d30be-02f5-4f54-9616-c412dd6e9da2"

#tests both the bookmark and buying functionality
TEST_BOOKMARK_BUYING_FUNCTIONALITY = True
TEST_BOOKMARK_BUYING_URL = "https://www.vinted.co.uk/items/6979387938-montblanc-explorer-extreme-parfum?referrer=catalog"

PRICE_THRESHOLD = 30.0  # Minimum price threshold - items below this won't detect Nintendo Switch classes
NINTENDO_SWITCH_CLASSES = [
    'controller','tv_black', 
    'tv_white', 'comfort_h',
    'comfort_h_joy', 'switch_box', 'switch', 'switch_in_tv',
]

VINTED_SHOW_ALL_LISTINGS = False
print_debug = False
print_images_backend_info = False
test_bookmark_function = False
bookmark_listings = True
click_pay_button_final_check = True
test_bookmark_link = "https://www.vinted.co.uk/items/4402812396-paper-back-book?referrer=catalog"
bookmark_stopwatch_length = 540
buying_driver_click_pay_wait_time = 7.5
actually_purchase_listing = True
wait_for_bookmark_stopwatch_to_buy = True
test_purchase_not_true = False #uses the url below rather than the one from the web page
test_purchase_url = "https://www.vinted.co.uk/items/6963326227-nintendo-switch-1?referrer=catalog"
#sold listing: https://www.vinted.co.uk/items/6900159208-laptop-case
should_send_fail_bookmark_notification = True

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
MAX_LISTINGS_TO_SCAN = 50
REFRESH_AND_RESCAN = True  # Set to False to disable refresh functionality
MAX_LISTINGS_VINTED_TO_SCAN = 5  # Maximum listings to scan before refresh
wait_after_max_reached_vinted = 0  # Seconds to wait between refresh cycles (5 minutes)
VINTED_SCANNED_IDS_FILE = "vinted_scanned_ids.txt"
FAILURE_REASON_LISTED = True
REPEAT_LISTINGS = True
WAIT_TIME_AFTER_REFRESH = 125
LOCK_POSITION = True
SHOW_ALL_LISTINGS = False
SHOW_PARTIALLY_SUITABLE = False
setup_website = False
send_message = True
current_listing_url = ""
send_notification = True
WAIT_TIME_FOR_WEBSITE_MESSAGE = 25
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

ngrok_auth_code = "ngrok config add-authtoken 2roTu5SuJVRTFYSd2d1JBTyhjXA_5qNzmjZBn5EHVA2dwMfrZ"
ngrok_static_website_command = "ngrok http --url=equal-ape-sincerely.ngrok-free.app 5000 --region=eu"

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
   'controller': 15, 'crash_sand': 11, 'diamond_p': 26, 'evee': 25, 'fifa_23': 7.5, 'fifa_24': 14,
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

@app.route('/button-clicked', methods=['POST'])
def button_clicked():
    if print_debug:
        print("DEBUG: Received a button-click POST request")
    global messaging_driver, website_static_price
    url = request.form.get('url')
    website_static_price_str = request.form.get('website_price')
    price_increment = int(request.form.get('price_increment', 5))
    
    if not url:
        return 'NO URL PROVIDED', 400
    
    # Put the request in the queue
    request_queue.put((url, website_static_price_str, price_increment))
    
    # Start processing the queue if not already processing
    if not hasattr(button_clicked, 'is_processing') or not button_clicked.is_processing:
        button_clicked.is_processing = True
        # Access the scraper instance through a global variable
        if 'scraper_instance' in globals():
            threading.Thread(target=scraper_instance.process_request_queue).start()
    
    return 'REQUEST ADDED TO QUEUE', 200

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


class FacebookScraper:
    
    def __init__(self):
        pass

    def start_cloudflare_tunnel(self, port=5000):
        """
        Starts your existing Cloudflare Tunnel for fk43b0p45crc03r.xyz
        """
        #pc
        cloudflared_path = r"C:\Users\ZacKnowsHow\Downloads\cloudflared.exe"
        #laptop
        #cloudflared_path = r"C:\Users\zacha\Downloads\cloudflared.exe"
        
        # Use your existing tunnel with explicit config file path
        process = subprocess.Popen(
            [cloudflared_path, "tunnel", "--config", r"C:\Users\zacha\.cloudflared\config.yml", "run"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW  # Run in background without window
        )
        
        def read_output(proc):
            for line in proc.stdout:
                print("[cloudflared]", line.strip())
                if "Registered tunnel connection" in line:
                    print(f"✅ Tunnel connection established")
                    print(f"🌐 Your scraper is accessible at: https://fk43b0p45crc03r.xyz")
                elif "Starting tunnel" in line:
                    print("🚇 Starting Cloudflare tunnel...")
        
        def read_errors(proc):
            for line in proc.stderr:
                error_line = line.strip()
                if error_line and "WRN" not in error_line:  # Skip warnings
                    print("[cloudflared ERROR]", error_line)
        
        # Start threads to read both stdout and stderr
        threading.Thread(target=read_output, args=(process,), daemon=True).start()
        threading.Thread(target=read_errors, args=(process,), daemon=True).start()
        
        print("⏳ Waiting for tunnel to establish...")
        time.sleep(10)  # Give more time for tunnel to establish connections
        return process

    def periodically_restart_messaging_driver(self):
        global messaging_driver
        while True:
            try:
                # Sleep for 1 hour
                time.sleep(3600)  # 3600 seconds = 1 hour
                
                print("🔄 Initiating periodic messaging driver restart...")
                
                # Safely close the existing driver if it exists
                if messaging_driver:
                    try:
                        messaging_driver.quit()
                        print("✅ Previous messaging driver closed successfully")
                    except Exception as close_error:
                        print(f"❌ Error closing previous driver: {close_error}")
                
                # Reinitialize the driver
                messaging_driver = self.setup_chrome_messaging_driver()
                
                if messaging_driver is None:
                    print("❌ Failed to reinitialize messaging driver")
                else:
                    print("✅ Messaging driver reinitialized successfully")
            
            except Exception as e:
                print(f"❌ Error in driver restart thread: {e}")

    def setup_ngrok_tunnel(self):
        try:
            # Open a new command prompt
            subprocess.Popen('start cmd', shell=True)
            time.sleep(1)  # Give the command prompt a moment to open

            # Simulate keystrokes to set up ngrok
            pyautogui.typewrite(ngrok_auth_code)
            pyautogui.press('enter')
            time.sleep(2)  # Wait for authentication

            # Type and execute the static website command
            pyautogui.typewrite(ngrok_static_website_command)
            pyautogui.press('enter')
            
            print("✅ Ngrok tunnel setup complete")
            return True
        except Exception as e:
            print(f"❌ Error setting up ngrok tunnel: {e}")
            return False

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

    def check_driver_health(self, driver):
        try:
            # Multiple health check strategies
            strategies = [
                # Check if we can execute a simple JavaScript
                lambda: driver.execute_script("return document.readyState") == "complete",
                
                # Check if we can navigate to a simple page
                lambda: driver.get("https://www.microsoft.com") is not None,
                
                # Check if we can find an element
                lambda: driver.find_element(By.TAG_NAME, 'body') is not None
            ]
            
            # If any strategy fails, consider driver unhealthy
            for strategy in strategies:
                try:
                    if not strategy():
                        print(f"❌ Driver health check failed: {strategy.__name__}")
                        return False
                except Exception as e:
                    print(f"❌ Driver health check error: {e}")
                    return False
            
            print("✅ Driver is healthy")
            return True
        
        except Exception as e:
            print(f"❌ Comprehensive driver health check failed: {e}")
            return False

    def login_to_facebook(self, driver):
        """
        Navigate directly to Facebook Marketplace instead of logging in.
        Assumes the browser is already logged in.
        """ 
        print("Navigating directly to Facebook Marketplace...")
        
        try:
            # Clear the listing_ids.txt file when starting
            with open('listing_ids.txt', 'w') as f:
                pass
            print("Cleared listing_ids.txt")

            # Navigate directly to Marketplace
            driver.get("https://www.facebook.com/marketplace/liverpool")
            
            # Wait for the Marketplace page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[role='main']"))
            )
            print("Successfully navigated to Facebook Marketplace.")
        
        except Exception as e:
            print(f"Error navigating to Marketplace: {str(e)}")


    def render_main_page(self):
        try:
            # Ensure default values if variables are None or empty 
            title = str(current_listing_title or 'No Title Available') 
            price = str(current_listing_price or 'No Price Available') 
            description = str(current_listing_description or 'No Description Available') 
            website_price = str(current_listing_price or 'No Price Available')
            
            detected_items = str(current_detected_items or 'No items')        
            # Filter out items with zero count from the string 

            profit = str(current_profit or 'No Profit Available') 
            join_date = str(current_listing_join_date or 'No Join Date Available') 
            listing_url = str(current_listing_url or 'No URL Available')

            all_listings_json = json.dumps([
                {
                    'title': listing['title'],
                    'description': listing['description'],
                    'join_date': listing['join_date'],
                    'price': listing['price'],
                    'profit': listing['profit'],
                    'detected_items': str(listing.get('detected_items') or 'No Items'),
                    'processed_images': [self.base64_encode_image(img) for img in listing['processed_images']],
                    'url': listing['url'],
                    'suitability': listing['suitability']
                } 
                for listing in recent_listings['listings']
            ])

            # Convert images to base64 for web display 
            image_html = "" 
            if current_listing_images: 
                image_html = "<div class='image-container'>" 
                for img in current_listing_images: 
                    # Convert PIL Image to base64 
                    buffered = io.BytesIO() 
                    img.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()

                    image_html += f''' 
                    <div class="image-wrapper"> 
                        <img src="data:image/png;base64,{img_str}" alt="Listing Image"> 
                    </div> 
                    ''' 
                image_html += "</div>" 
            else: 
                image_html = "<p>No images available</p>" 

            return f''' 
        <html> 
        <head> 
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
            <link rel="apple-touch-icon" href="/static/icon.png">
            <link rel="icon" type="image/png" href="/static/icon.png">
            <meta name="apple-mobile-web-app-capable" content="yes">
            <meta name="apple-mobile-web-app-status-bar-style" content="black">
            <meta name="apple-mobile-web-app-title" content="Marketplace Scanner">
            
            <style> 
                * {{ 
                    box-sizing: border-box; 
                    margin: 0; 
                    padding: 0; 
                }} 
                .price-button-container {{
                    display: flex;
                    flex-direction: column;
                    gap: 5px;
                    margin-top: 10px;
                }}

                .button-row {{
                    display: flex;
                    justify-content: space-between;
                    gap: 10px;
                }}

                .button-row .custom-button {{
                    flex: 1;  /* This ensures both buttons in a row are equal width */
                }}

                .custom-button:nth-child(1) {{ background-color: #4CAF50; }}  /* Green */
                .custom-button:nth-child(2) {{ background-color: #2196F3; }}  /* Blue */
                .custom-button:nth-child(3) {{ background-color: #FF9800; }}  /* Orange */
                .custom-button:nth-child(4) {{ background-color: #9C27B0; }}
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
                p {{ 
                    word-wrap: break-word; 
                    margin-bottom: 0; 
                    padding: 0 10px; 
                }} 
                .header {{ 
                    color: black; 
                    font-size: 18px; 
                    font-style: italic; 
                    font-weight: bold; 
                }} 
                .image-wrapper {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    max-width: 100%;  /* Ensures images don't exceed container width */
                    max-height: 200px;  /* Limit individual image height */
                    overflow: hidden;
                }}

                .image-wrapper img {{
                    max-width: 100%;    /* Fit horizontally */
                    max-height: 100%;   /* Fit vertically */
                    object-fit: contain; /* Maintain aspect ratio */
                }}
                .content-title {{ 
                    color:rgb(173, 13, 144);  /* Dark Purple */ 
                    font-weight: bold; 
                    font-size: 1.6em;
                }} 
                .content-price {{ 
                    color:rgb(19, 133, 194);  /* Saddle Brown (dark brown) */ 
                    font-weight: bold; 
                }} 
                .content-description {{ 
                    color: #006400;  /* Dark Green */ 
                    font-weight: bold; 
                }} 
                .content-revenue {{ 
                    color:rgb(124, 14, 203);  /* Indigo */ 
                    font-weight: bold; 
                }} 
                .content-profit {{ 
                    color:rgb(186, 14, 14);  /* Dark Red */ 
                    font-weight: bold; 
                }} 
                .content-join-date {{ 
                    color: #4169E1;  /* Royal Blue */ 
                    font-weight: bold; 
                }} 
                .content-detected-items {{ 
                    color: #8B008B;  /* Dark Magenta */ 
                    font-weight: bold; 
                }} 
                .image-container {{
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: center;
                    align-items: center;
                    gap: 10px;
                    max-height: 335px;  /* Increased from 300px by ~25-50% */
                    overflow-y: auto;
                    padding: 10px;
                    background-color: #f9f9f9;
                    border: 1px solid black;
                    border-radius: 10px;
                    margin-bottom: 10px;
                }}
                .listing-container {{
                    width: 100%;
                    height: 100%;
                    margin: 0;
                    padding: 0;
                    overflow: hidden;
                }}

                .listing-container.slide-out {{
                    transition: transform 0.3s ease;
                    transform: translateX(100%);
                }}

                /* Prevent text selection and improve touch interaction */
                body {{
                    user-select: none;
                    -webkit-user-select: none;
                    touch-action: manipulation;
                }}

                /* Improve button and interactive element touch response */
                .custom-button, button {{
                    touch-action: manipulation;
                    -webkit-tap-highlight-color: transparent;
                }}
                .custom-button:active, .button-clicked {{
                    background-color: rgba(0, 0, 0, 0.2) !important;  /* Darkens the button when clicked */
                    transform: scale(0.95);  /* Slightly shrinks the button */
                    transition: background-color 0.3s, transform 0.3s;
                }}
                .custom-button {{
                    width: 100%;
                    padding: 10px;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    font-size: 15px;
                    touch-action: manipulation;
                    -webkit-tap-highlight-color: transparent;
                }}
                body {{ 
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif; 
                    background-color: #f0f0f0; 
                    display: flex; 
                    justify-content: center; 
                    align-items: center; 
                    min-height: 100vh;  f
                    margin: 0; 
                    padding: 0;
                    line-height: 1.6; 
                    touch-action: manipulation;
                    overscroll-behavior-y: none;
                }} 
                .listing-url {{ 
                    font-size: 10px;  /* Reduced by about 75% */ 
                    word-break: break-all; 
                    border: 1px solid black; 
                    border-radius: 5px; 
                    padding: 5px; 
                    margin-top: 10px; 
                    font-weight: bold; 
                }} 
            </style> 
            <script>
                const allListings = {all_listings_json};
                let currentListingIndex = 0;
                let touchStartX = 0;
                let touchEndX = 0;
                const minSwipeDistance = 50; // Minimum distance to trigger swipe
                function refreshPage() {{
                    // Simple page reload
                    location.reload();
                }}
                function handleTouchStart(event) {{
                    touchStartX = event.touches[0].clientX;
                    touchStartY = event.touches[0].clientY;  // Added Y coordinate tracking
                }}

                function handleTouchMove(event) {{
                    touchEndX = event.touches[0].clientX;
                    touchEndY = event.touches[0].clientY;
                    
                    // Calculate distances
                    const verticalDistance = Math.abs(touchStartY - touchEndY);
                    const horizontalDistance = Math.abs(touchStartX - touchEndX);
                    
                    // Much more permissive vertical scrolling
                    // Allow scrolling if vertical movement is significantly more than horizontal
                    if (horizontalDistance <= verticalDistance * 0.75) {{
                        // Normal vertical scrolling behavior
                        return;
                    }} else {{
                        // Prevent horizontal dragging if horizontal movement is too significant
                        event.preventDefault();
                    }}
                }}

                function handleTouchEnd(event) {{
                    const swipeDistance = touchStartX - touchEndX;
                    const verticalDistance = Math.abs(touchStartY - event.changedTouches[0].clientY);
                    const horizontalDistance = Math.abs(swipeDistance);

                    // Reset the listing container's transform
                    const listingContainer = document.querySelector('.listing-container');
                    listingContainer.style.transform = 'translateX(0)';
                    listingContainer.style.transition = 'transform 0.3s ease';

                    // Only change listing if it was a clear horizontal swipe and not a vertical scroll
                    if (horizontalDistance > minSwipeDistance && verticalDistance < minSwipeDistance) {{
                        if (swipeDistance > 0) {{
                            // Swiped left (next listing)
                            updateListingDisplay(currentListingIndex + 1);
                        }} else {{
                            // Swiped right (previous listing)
                            updateListingDisplay(currentListingIndex - 1);
                        }}
                    }}
                }}

                function updateListingDisplay(index) {{
                    if (index < 0) index = allListings.length - 1;
                    if (index >= allListings.length) index = 0;
                    
                    currentListingIndex = index;
                    const listing = allListings[index];

                    // Update all elements with a smooth transition
                    const listingContainer = document.querySelector('.listing-container');
                    listingContainer.classList.add('slide-out');
                    
                    setTimeout(() => {{
                        // Update content
                        document.querySelector('.content-title').textContent = listing.title;
                        document.querySelector('.content-price').textContent = 'Price: £' + listing.price;
                        document.querySelector('.content-profit').textContent = `Profit:\n£${{listing.profit.toFixed(2)}}`;
                        document.querySelector('.content-join-date').textContent = listing.join_date;
                        document.querySelector('.content-detected-items').textContent = listing.detected_items;
                        document.querySelector('.content-description').textContent = listing.description;
                        document.querySelector('.content-url').textContent = listing.url;
                        document.getElementById('listing-counter').textContent = `Listing ${{currentListingIndex + 1}} of ${{allListings.length}}`;

                        // Update images
                        const imageContainer = document.querySelector('.image-container');
                        imageContainer.innerHTML = ''; // Clear existing images
                        listing.processed_images.forEach(imgBase64 => {{
                            const imageWrapper = document.createElement('div');
                            imageWrapper.className = 'image-wrapper';
                            const img = document.createElement('img');
                            img.src = `data:image/png;base64,${{imgBase64}}`;
                            img.alt = 'Listing Image';
                            imageWrapper.appendChild(img);
                            imageContainer.appendChild(imageWrapper);
                        }});

                        // Reset slide animation
                        listingContainer.classList.remove('slide-out');
                    }}, 300); // Match this with CSS transition time
                }}

                // Add touch event listeners
                document.addEventListener('DOMContentLoaded', () => {{
                    const listingContainer = document.querySelector('.listing-container');
                    listingContainer.addEventListener('touchstart', handleTouchStart, false);
                    listingContainer.addEventListener('touchmove', handleTouchMove, false);
                    listingContainer.addEventListener('touchend', handleTouchEnd, false);
                }});

                // Initialize display on page load
                window.onload = () => updateListingDisplay(0);
                    function changeListingIndex(direction) {{
                        if (direction === 'next') {{
                            updateListingDisplay(currentListingIndex + 1);
                        }} else if (direction === 'previous') {{
                            updateListingDisplay(currentListingIndex - 1);
                        }}
                    }}

                    // Initialize display on page load
                function handleButtonClick(priceIncrement) {{
                    var urlElement = document.querySelector('.content-url'); 
                    var url = urlElement ? urlElement.textContent.trim() : ''; 

                    var priceElement = document.querySelector('.content-price');
                    var websitePrice = priceElement ? priceElement.textContent.trim() : '';

                    // Get title and description
                    var titleElement = document.querySelector('.content-title');
                    var descriptionElement = document.querySelector('.content-description');
                    
                    var websiteTitle = titleElement ? titleElement.textContent.trim() : 'No Title';
                    var websiteDescription = descriptionElement ? descriptionElement.textContent.trim() : 'No Description';

                    // Get the clicked button
                    var clickedButton = event.target;

                    // Add a class for the click animation
                    clickedButton.classList.add('button-clicked');

                    // Remove the class after the animation
                    setTimeout(() => {{
                        clickedButton.classList.remove('button-clicked');
                    }}, 300);  // Same duration as the CSS transition

                    fetch('/button-clicked', {{
                        method: 'POST', 
                        headers: {{
                            'Content-Type': 'application/x-www-form-urlencoded', 
                        }}, 
                        body: `url=${{encodeURIComponent(url)}}&website_price=${{encodeURIComponent(websitePrice)}}&website_title=${{encodeURIComponent(websiteTitle)}}&website_description=${{encodeURIComponent(websiteDescription)}}&price_increment=${{priceIncrement}}` 
                    }}) 
                    .then(response => {{
                        if (response.ok) {{
                            console.log('Button clicked successfully'); 
                        }} else {{
                            console.error('Failed to click button'); 
                        }}
                    }})
                    .catch(error => {{
                        console.error('Error:', error); 
                    }});
                }}

                function handleCustomPriceClick() {{
                    // Prompt user for custom price increment
                    var customIncrement = prompt("Enter custom price increment (in £):", "15");
                    
                    // Validate input
                if (customIncrement === null) {{
                        return; // User cancelled
                    }}
                    
                    // Convert to number and handle invalid input
                    customIncrement = parseFloat(customIncrement);
                    
                    if (isNaN(customIncrement) || customIncrement <= 0) {{
                        alert("Please enter a valid positive number.");
                        return;
                    }}

                    var urlElement = document.querySelector('.content-url'); 
                    var url = urlElement ? urlElement.textContent.trim() : ''; 

                    var priceElement = document.querySelector('.content-price');
                    var websitePrice = priceElement ? priceElement.textContent.trim() : '';

                    // Get title and description
                    var titleElement = document.querySelector('.content-title');
                    var descriptionElement = document.querySelector('.content-description');
                    
                    var websiteTitle = titleElement ? titleElement.textContent.trim() : 'No Title';
                    var websiteDescription = descriptionElement ? descriptionElement.textContent.trim() : 'No Description';

                    fetch('/button-clicked', {{
                        method: 'POST', 
                        headers: {{
                            'Content-Type': 'application/x-www-form-urlencoded', 
                        }}, 
                        body: `url=${{encodeURIComponent(url)}}&website_price=${{encodeURIComponent(websitePrice)}}&website_title=${{encodeURIComponent(websiteTitle)}}&website_description=${{encodeURIComponent(websiteDescription)}}&price_increment=${{customIncrement}}` 
                    }}) 
                    .then(response => {{
                        if (response.ok) {{
                            console.log('Button clicked successfully'); 
                        }} else {{
                            console.error('Failed to click button'); 
                        }}
                    }})
                    .catch(error => {{
                        console.error('Error:', error); 
                    }});
                }}
            </script> 

        </head> 
        <body> 
            <div class="container listing-container">
                <div class="container">
                    <div class="button-row">
                        <button class="custom-button" onclick="refreshPage()" style="background-color:rgb(108,178,209);">Refresh Page</button>
                    </div>
                    <div class="listing-counter" id="listing-counter">
                        Listing 1 of 1
                    </div>
                    <div class="section-box"> 
                        <p><span class="header"></span><span class="content-title">{title}</span></p> 
                    </div>
                    <div class="financial-row"> 
                        <div class="financial-item"> 
                            <p><span class="header"></span><span class="content-price">{price}</span></p> 
                        </div> 
                        <div class="financial-item"> 
                            <p><span class="header"></span><span class="content-profit">{profit}</span></p> 
                        </div> 
                    </div> 

                    <div class="section-box"> 
                        <p><span class="header"></span><span class="content-description">{description}</span></p> 
                    </div>

                    <div class="price-button-container">
                        <div class="button-row">
                            <button class="custom-button" onclick="handleButtonClick(5)"" style="background-color:rgb(109,171,96);">Message price + £5</button>
                            <button class="custom-button" onclick="handleButtonClick(10)"" style="background-color:rgb(79,158,196);">Message price + £10</button>
                        </div>
                        <div class="button-row">
                            <button class="custom-button" onclick="handleButtonClick(15)"" style="background-color:rgb(151,84,80);">Message price + £15</button>
                            <button class="custom-button" onclick="handleButtonClick(20)"" style="background-color: rgb(192,132,17);">Message price + £20</button>
                            <button class="custom-button" onclick="handleCustomPriceClick()" style="background-color: rgb(76,175,80);">Custom Price +</button>
                        </div>
                    </div>
                    <div class="details-row">
                        <div class="details-item"> 
                            <p><span class="header"></span><span class="content-detected-items">{detected_items}</span></p> 
                        </div> 
                        <div class="image-container"> 
                            {image_html} 
                        </div> 
                    </div>

                    <div class="details-item"> 
                            <p><span class="header"></span><span class="content-join-date">{join_date}</span></p> 
                        </div> 
                    <div class="navigation-buttons">
                        <button onclick="changeListingIndex('previous')">Previous</button>
                        <button onclick="changeListingIndex('next')">Next</button>
                    </div>
                    <div class="listing-url" id="listing-url"> 
                        <p><span class="header">Listing URL: </span><span class="content-url">{listing_url}</span></p>
                    </div>
                </div> 
            </div>
        </body> 
        </html> 
        ''' 

        except Exception as e: 
            return f"<html><body><h1>Error</h1><p>{str(e)}</p></body></html>" 


    

    def process_request_queue(self):
        global messaging_driver
        while not request_queue.empty():
            url, website_static_price_str, price_increment = request_queue.get()
            start_time = time.time()
            message_sent = False
            try:
                # Parse the price from the string
                try:
                    cleaned_price_str = (
                        website_static_price_str
                        .replace('Price:', '')
                        .replace('\n', '')
                        .replace('£', '')
                        .replace(' ', '')
                        .strip()
                    )
                    website_static_price = float(cleaned_price_str)
                    print(f"🏷️ Website Static Price: £{website_static_price:.2f}")
                except (ValueError, AttributeError) as e:
                    print(f"Error parsing price: {e}")
                    print(f"Problematic price string: {website_static_price_str}")
                    website_static_price = 0.00
                    continue

                # Validate the URL format
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url

                # Reinitialize the driver if needed
                if not messaging_driver:
                    messaging_driver = self.setup_chrome_messaging_driver()
                    if not messaging_driver:
                        print("❌ No driver available.")
                        continue

                # Navigate to the target URL
                messaging_driver.get(url)
                WebDriverWait(messaging_driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'body'))
                )

                # Create the messaging string using the adjusted website price
                website_price_adjusted = int(round(website_static_price)) + price_increment
                message_1 = f"hi, is this still available? happy to pay £{website_price_adjusted} + shipping, if that works for you? I'm Richmond based so collection is a bit far! (id pay first obviously)"

                # NEW: Search for an element containing the text "Message seller" (case-insensitive)
                print("[Progress] Searching for 'Message seller' element on the page...")
                elements = messaging_driver.find_elements(
                    By.XPATH,
                    "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'message seller')]"
                )
                found_button = None
                for elem in elements:
                    if elem.is_displayed():
                        found_button = elem
                        break

                if found_button:
                    print("[Success] Found the 'Message seller' element. Attempting click...")
                    try:
                        messaging_driver.execute_script("arguments[0].click();", found_button)
                        print("✅ 'Message seller' button clicked successfully.")
                        message_sent = True
                    except Exception as js_click_err:
                        print(f"❌ JavaScript click failed: {js_click_err}")
                else:
                    print("❌ Failed to locate the 'Message seller' element.")

                # Allow time for the message window to load
                time.sleep(2)

                if not message_sent:
                    print("❌ Message seller button was not clicked, skipping further processing.")
                    continue

                # Use ActionChains to clear and then type the message
                actions = ActionChains(messaging_driver)
                for _ in range(6):
                    actions.send_keys(Keys.TAB)
                actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL)
                actions.send_keys(message_1)
                actions.perform()

                # If sending is enabled, try to click the send button
                if send_message:
                    try:
                        send_button = WebDriverWait(messaging_driver, 10).until(
                            EC.element_to_be_clickable(( 
                                By.XPATH, 
                                "//span[contains(@class, 'x1lliihq') and contains(@class, 'x6ikm8r') "
                                "and contains(@class, 'x10wlt62') and contains(@class, 'x1n2onr6') "
                                "and contains(@class, 'xlyipyv') and contains(@class, 'xuxw1ft') and text()='Send Message']"
                            ))
                        )
                        try:
                            send_button.click()
                        except Exception as e:
                            try:
                                messaging_driver.execute_script("arguments[0].click();", send_button)
                            except Exception as e2:
                                ActionChains(messaging_driver).move_to_element(send_button).click().perform()
                        print("🚀 Message sent successfully! 🚀")
                        message_sent = True
                    except Exception as send_error:
                        print(f"🚨 Failed to send message: {send_error}")
                        if time.time() - start_time > WAIT_TIME_FOR_WEBSITE_MESSAGE:
                            print(f"⏰ Messaging process timed out after {WAIT_TIME_FOR_WEBSITE_MESSAGE} seconds")
                        continue

                print(f"Successfully processed request for {url}")

            except Exception as e:
                print(f"Error processing request for {url}: {e}")
            finally:
                request_queue.task_done()  # This is called exactly once per item
                if request_queue.empty():
                    self.button_clicked.is_processing = False


    def base64_encode_image(self, img):
        """Convert PIL Image to base64 string, resizing if necessary"""
        # Resize image while maintaining aspect ratio
        max_size = (200, 200)
        img.thumbnail(max_size, Image.LANCZOS)
        
        # Convert to base64
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    
    def run_flask_app(self):
        try:
            print("Starting Flask app with existing Cloudflare Tunnel...")
            print("Your website will be available at: https://fk43b0p45crc03r.xyz")
            
            # Start your existing tunnel
            tunnel_process = self.start_cloudflare_tunnel(port=5000)
            
            # Run Flask on localhost - the tunnel will route external traffic to this
            app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
            
        except Exception as e:
            print(f"Error starting Flask app: {e}")
            import traceback
            traceback.print_exc()
        finally:
            try:
                if tunnel_process:
                    tunnel_process.terminate()
                    print("Tunnel terminated.")
            except Exception as term_err:
                print(f"Error terminating tunnel: {term_err}")


    def get_ngrok_url(self):
        return "equal-ape-sincerely.ngrok-free.app"

    def start_ngrok_and_get_url(self):
        return "equal-ape-sincerely.ngrok-free.app"

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
            'click': pygame.font.Font(None, 28),  # New font for click text
            'suitability': pygame.font.Font(None, 28)  # New font for suitability reason

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
                elif i == 8:  # Rectangle 9 (index 8) - Join Date
                    self.render_text_in_rect(screen, fonts['join_date'], current_listing_join_date, rect, (0, 0, 0))
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


            screen.blit(fonts['title'].render("LOCKED" if LOCK_POSITION else "UNLOCKED", True, (255, 0, 0) if LOCK_POSITION else (0, 255, 0)), (10, 10))

            if suitable_listings:
                listing_counter = fonts['number'].render(f"Listing {current_listing_index + 1}/{len(suitable_listings)}", True, (0, 0, 0))
                screen.blit(listing_counter, (10, 40))

            pygame.display.flip()
            clock.tick(30)

        self.save_rectangle_config(rectangles)
        pygame.quit()

    def setup_chrome_profile_driver(self):
        # CRITICAL: Ensure NO Chrome instances are open before running
        
        # Comprehensive Chrome options
        chrome_options = webdriver.ChromeOptions()
        prefs = {
            "profile.default_content_setting_values.notifications": 2,  # Disable notifications
            "profile.default_content_setting_values.popups": 0,         # Block popups (default = 0)
            "download.prompt_for_download": False,                      # Disable download prompt
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        # Use a dedicated, isolated user data directory to prevent conflicts.
        chrome_options.add_argument(f"user-data-dir={SCRAPER_USER_DATA_DIR}")
        chrome_options.add_argument("profile-directory=Default")
        #profile 10 is blue orchid
        #default = laptop
        #profile 2 = pc
        
        # Additional safety options
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        try:
            # Use specific Chrome driver path
            service = Service(ChromeDriverManager().install(), log_path=os.devnull)
            
            # Create driver with robust error handling
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Verify driver is functional
            print("Scraper Chrome driver successfully initialized!")
            
            return driver
        
        except Exception as e:
            print(f"CRITICAL CHROME DRIVER ERROR: {e}")
            print("Possible solutions:")
            print("1. Close all Chrome instances")
            print("2. Verify Chrome profile exists")
            print("3. Check Chrome and WebDriver versions")
            sys.exit(1)


    def setup_chrome_messaging_driver(self):
        chrome_options = webdriver.ChromeOptions()
        prefs = {
            "profile.default_content_setting_values.notifications": 2,  # Disable notifications
            "profile.default_content_setting_values.popups": 0,         # Block popups (default = 0)
            "download.prompt_for_download": False,                      # Disable download prompt
        }
        chrome_options.add_experimental_option("prefs", prefs)
        # Use a separate, dedicated user data directory for the second driver.
        chrome_options.add_argument(f"user-data-dir={MESSAGING_USER_DATA_DIR}")
        chrome_options.add_argument("profile-directory=Profile 11")
        #profile 11 = pc
        #profile 1 = laptop


        # Additional options to improve stability
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        try:
            # Use specific Chrome driver path
            service = Service(ChromeDriverManager().install(), log_path=os.devnull)
            
            # Create driver with robust error handling
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Verify driver is functional
            print("Messaging Chrome driver successfully initialized!")
            
            return driver

        except Exception as e:
            print(f"CRITICAL CHROME DRIVER ERROR: {e}")
            print("Possible solutions:")
            print("1. Ensure Google Chrome is closed")
            print("2. Verify Chrome profile path is correct")
            print("3. Check Chrome and WebDriver versions")
            return None  # Return None instead of sys.exit(1)
            
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
                return  # Skip rendering if font creation fails

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

    def render_multiline_text(self, screen, font, text, rect, color):
        # Convert dictionary to formatted string if needed
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
        
    def update_listing_details(self, title, description, join_date, price, expected_revenue, profit, detected_items, processed_images, bounding_boxes, url=None, suitability=None):
        global current_listing_title, current_listing_description, current_listing_join_date, current_listing_price
        global current_expected_revenue, current_profit, current_detected_items, current_listing_images 
        global current_bounding_boxes, current_listing_url, current_suitability 

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

        # Handle price formatting
        if isinstance(price, str) and price.startswith("Price:\n£"):
            formatted_price = price
        else:
            try:
                float_price = float(price) if price is not None else 0.00
                formatted_price = f"Price:\n£{float_price:.2f}"
            except ValueError:
                formatted_price = "Price:\n£0.00"

        # Handle expected_revenue formatting
        if isinstance(expected_revenue, float):
            formatted_expected_revenue = f"Rev:\n£{expected_revenue:.2f}"
        elif isinstance(expected_revenue, str) and expected_revenue.startswith("Rev:\n£"):
            formatted_expected_revenue = expected_revenue
        else:
            formatted_expected_revenue = "Rev:\n£0.00"

        # Handle profit formatting
        if isinstance(profit, float):
            formatted_profit = f"Profit:\n£{profit:.2f}"
        elif isinstance(profit, str) and profit.startswith("Profit:\n£"):
            formatted_profit = profit
        else:
            formatted_profit = "Profit:\n£0.00"

        # Handle detected_items with individual revenues
            # Handle detected_items with individual revenues
        if isinstance(detected_items, dict):
            all_prices = self.fetch_all_prices()
            formatted_detected_items = {}
            for item, count in detected_items.items():
                if count > 0:
                    item_price = all_prices.get(item, 0) * float(count)
                    formatted_detected_items[item] = f"{count} (£{item_price:.2f})"
        else:
            formatted_detected_items = {"no_items": "No items detected"}

        # Explicitly set the global variable
        current_detected_items = formatted_detected_items
        current_listing_title = title[:50] + '...' if len(title) > 50 else title
        current_listing_description = description[:200] + '...' if len(description) > 200 else description
        current_listing_join_date = join_date
        current_listing_price = f"Price:\n£{float(price):.2f}" if price else "Price:\n£0.00"
        current_expected_revenue = f"Rev:\n£{expected_revenue:.2f}" if expected_revenue else "Rev:\n£0.00"
        current_profit = f"Profit:\n£{profit:.2f}" if profit else "Profit:\n£0.00"
        current_listing_url = url
        current_suitability = suitability if suitability else "Suitability unknown"

    def update_pygame_window(self, title, description, join_date, price):
        self.update_listing_details(title, description, join_date, price)
        # No need to do anything else here, as the Pygame loop will use the updated global variables

    def clear_output_file(self):
        with open(OUTPUT_FILE_PATH, 'w') as f:
            f.write('')  # This will clear the file
        print(f"Cleared the content of {OUTPUT_FILE_PATH}")

    def write_to_file(self, message, summary=False):
        with open(OUTPUT_FILE_PATH, 'a') as f:
            f.write(message + '\n')
        if summary:
            print(message)

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

    def process_suitable_listing(self, listing_info, all_prices, listing_index):
        # Default values to ensure the variable always exists
        processed_images = []
        image_paths = []
        suitability_reason = "Not processed"
        profit_suitability = False
        display_objects = {}  # Initialize as empty dictionary

        if listing_info["image_urls"]:
            for j, image_url in enumerate(listing_info["image_urls"]):
                save_path = os.path.join(r"C:\Users\ZacKnowsHow\Downloads", f"listing_{listing_index+1}_photo_{j+1}.jpg")
                if self.save_image(image_url, save_path):
                    image_paths.append(save_path)
        else:
            print("No product images found to save.")

        detected_objects = {}
        processed_images = []
        total_revenue = 0
        expected_profit = 0
        profit_percentage = 0
        
        if image_paths:
            print("Performing object detection...")
            detected_objects, processed_images = self.perform_object_detection(image_paths, listing_info["title"], listing_info["description"])
            listing_price = float(listing_info["price"])
            total_revenue, expected_profit, profit_percentage, display_objects = self.calculate_revenue(
                detected_objects, all_prices, listing_price, listing_info["title"], listing_info["description"])
            listing_info['processed_images'] = processed_images.copy()

        # Remove 'controller' from display_objects to prevent comparison issues    
        # Store the processed images in listing_info, instead of creating copies
        listing_info['processed_images'] = processed_images
        
        # Game classes for detection
        game_classes = [
    '1_2_switch', 'animal_crossing', 'arceus_p', 'bow_z', 'bros_deluxe_m', 'crash_sand',
    'dance', 'diamond_p', 'evee', 'fifa_23', 'fifa_24', 'gta','just_dance', 'kart_m', 'kirby',
    'lets_go_p', 'links_z', 'luigis', 'mario_maker_2', 'mario_sonic', 'mario_tennis', 'minecraft',
    'minecraft_dungeons', 'minecraft_story', 'miscellanious_sonic', 'odyssey_m', 'other_mario',
    'party_m', 'rocket_league', 'scarlet_p', 'shield_p', 'shining_p', 'skywards_z', 'smash_bros',
    'snap_p', 'splatoon_2', 'splatoon_3', 'super_m_party', 'super_mario_3d', 'switch_sports',
    'sword_p', 'tears_z', 'violet_p'
    ]
        
        # Count detected games
        game_count = sum(detected_objects.get(game, 0) for game in game_classes)
        
        # Identify non-game classes
        non_game_classes = [cls for cls in detected_objects.keys() if cls not in game_classes and detected_objects.get(cls, 0) > 0]
        
        # Add a new suitability check for game count that actually prevents listing from being added
        if 1 <= game_count <= 2 and not non_game_classes:
            suitability_reason = "Unsuitable: 1-2 games with no additional non-game items"
            return False, suitability_reason

        # Existing profit suitability check
        profit_suitability = self.check_profit_suitability(float(listing_info["price"]), profit_percentage)
        
        # Remove 'controller' from display_objects to prevent comparison issues
        
        # Existing suitability checks
        suitability_checks = [
            (lambda: any(word in listing_info["title"].lower() for word in title_forbidden_words),
            "Title forbidden words"),
            (lambda: not any(word in listing_info["title"].lower() for word in title_must_contain),
            "Title doesn't contain required words"),
            (lambda: any(word in listing_info["description"].lower() for word in description_forbidden_words),
            "Description forbidden words"),
            (lambda: "join_date not found" not in listing_info["join_date"].lower() and 
                    int(listing_info["join_date"].split()[-1]) == 2025,
            "Joined 2025"),
            (lambda: listing_info["price"] != "Price not found" and 
                    (float(listing_info["price"]) < min_price or float(listing_info["price"]) > max_price),
            f"Price £{listing_info['price']} isnt in range £{min_price}-£{max_price}"),
            (lambda: len(re.findall(r'[£$]\s*\d+|\d+\s*[£$]', listing_info["description"])) >= 3,
            "Too many $ symbols"),
            (lambda: not profit_suitability,
            "Profit unsuitable"),
            (lambda: float(listing_info["price"]) in BANNED_PRICES,
            "Price in banned prices")
        ]
        
        unsuitability_reasons = [message for check, message in suitability_checks if check()]
        
        if unsuitability_reasons:
            suitability_reason = "Unsuitable:\n---- " + "\n---- ".join(unsuitability_reasons)
        else:
            suitability_reason = "Listing is suitable"
        
        # Add to suitable_listings with proper image handling
        if SHOW_ALL_LISTINGS or SHOW_PARTIALLY_SUITABLE or profit_suitability:

            notification_title = f"New Suitable Listing: £{listing_info['price']}"
            notification_message = (
                f"Title: {listing_info['title']}\n"
                f"Price: £{listing_info['price']}\n"
                f"Expected Profit: £{expected_profit:.2f}\n"
                f"Profit %: {profit_percentage:.2f}%\n"
            )
            
            # Use the Pushover tokens you provided
            if send_notification:
                self.send_pushover_notification(
                    notification_title, 
                    notification_message, 
                    'aks3to8guqjye193w7ajnydk9jaxh5', 
                    'ucwc6fi1mzd3gq2ym7jiwg3ggzv1pc'
                )

            display_objects = {k: v for k, v in display_objects.items() if 
                (isinstance(v, int) and v > 0) or 
                (isinstance(v, str) and v != '0' and v != '')}
                
            print(f'Detected Objects: {display_objects}')
            # display_object = dictionary
            new_listing = {
                'title': listing_info["title"],
                'description': listing_info["description"],
                'join_date': listing_info["join_date"],
                'price': listing_info["price"],
                'expected_revenue': total_revenue,
                'profit': expected_profit,
                'processed_images': listing_info['processed_images'],
                'detected_items': display_objects,
                'bounding_boxes': {
                    'image_paths': image_paths,
                    'detected_objects': detected_objects
                },
                'url': listing_info["url"],
                'suitability': suitability_reason
            }
            
            recent_listings['listings'].append(new_listing)
            
            # Always set to the last (most recent) listing
            recent_listings['current_index'] = len(recent_listings['listings']) - 1
            
            # Update current listing details
            self.update_listing_details(**recent_listings['listings'][recent_listings['current_index']])
            
            suitable_listings.append(new_listing)
            
            global current_listing_index
            current_listing_index = len(suitable_listings) - 1 
            self.update_listing_details(**suitable_listings[current_listing_index])

        return profit_suitability, suitability_reason

    def download_and_process_images(self, image_urls):
        processed_images = []
        for url in image_urls[:8]:  # Limit to 8 images
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    img = Image.open(io.BytesIO(response.content))
                    img = img.convert("RGB")
                    img_copy = img.copy()  # Create a copy
                    processed_images.append(img_copy)
                    img.close()  # Close the original image
                    del img  # Explicitly delete the original
                else:
                    print(f"Failed to download image. Status code: {response.status_code}")
            except Exception as e:
                print(f"Error processing image: {str(e)}")
        return processed_images

    def scroll_page(self, driver, scroll_times=1):
        """
        Scroll down the page using ActionChains and Page Down key
        
        :param driver: Selenium WebDriver instance
        :param scroll_times: Number of times to press Page Down
        """
        try:
            # Create ActionChains object
            actions = ActionChains(driver)
            
            # Scroll down specified number of times
            for _ in range(scroll_times):
                actions.send_keys(Keys.PAGE_DOWN).perform()
                
                # Optional: Add a small pause between scrolls to simulate natural scrolling
                time.sleep(0.5)
            
            print(f"Scrolled down {scroll_times} time(s)")
        
        except Exception as e:
            print(f"Error during scrolling: {e}")

    def scroll_and_load_listings(self, driver, scanned_urls):
        """Scroll to the bottom of the page and load listings chronologically."""
        print("Scrolling to the bottom of the page...")
        
        # Set an initial height for the page
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            # Scroll down to the bottom of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for new listings to load

            # Get the new height after scrolling
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            # Check for new listings
            listing_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'x78zum5 xdt5ytf x1n2onr6')]//a[contains(@href, '/marketplace/item/')]")
            for element in listing_elements:
                url = element.get_attribute('href')
                if url and url not in scanned_urls:
                    scanned_urls.add(url)
                    yield url  # Yield the new listing URL

            # If we have scrolled to the bottom and the height hasn't changed, break the loop
            if new_height == last_height:
                print("Reached the bottom of the page. Stopping scroll.")
                break
            
            last_height = new_height  # Update the last height for the next scroll

    def extract_item_id(self, url):
        # Use a regular expression to find the item ID
        match = re.search(r'/item/(\d+)/', url)
        if match:
            listing_id_url = match.group(1)  # Save the extracted item ID
            return listing_id_url  # Return the extracted item ID
        else:
            print("Item ID not found in the URL.")
            return None  # Return None if no item ID is found

    def search_and_select_listings(self, driver, search_query, output_file_path):
        import gc
        visible_listings_scanned = 0
        global suitable_listings, current_listing_index, duplicate_counter, scanned_urls 
        marketplace_url = f"https://www.facebook.com/marketplace/search?query={search_query}" 

        listing_queue = []  # Maintain as list for ordered processing
        no_new_listings_count = 0 
        suitability_reason = "Not processed"
        profit_suitability = False
        first_scan = True 
        scanned_urls = []  # Maintain as list for ordered processing
        consecutive_duplicate_count = 0 

        scanned_urls_file = "scanned_urls.txt" 
        try: 
            with open(scanned_urls_file, 'r') as f: 
                scanned_urls = [line.strip() for line in f if line.strip()]  # Read non-empty lines
        except FileNotFoundError: 
            print("No previous scanned URLs file found. Starting fresh.") 

        # Clear the file at start
        with open(scanned_urls_file, 'w') as f: 
            pass 

        suitable_listings.clear() 
        current_listing_index = 0 

        while True:
            # Clear temporary variables at start of each loop.
            if 'current_listing_images' in globals():
                for img in current_listing_images:
                    try:
                        img.close()  # Close all images
                    except Exception as e:
                        print(f"Error closing image: {str(e)}")
                current_listing_images.clear()  # Clear the list
            listings_scanned = 0
            scanned_urls = []
            scanned_urls.clear()
            current_listing_index = 0
            listing_queue.clear()
            listing_queue = []
            
            # Get fresh marketplace page
            driver.get(marketplace_url) 
            print(f"Searching for: {search_query}") 
            main_window = driver.current_window_handle 

            try:
                # Wait for marketplace to load
                WebDriverWait(driver, 30).until( 
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='main']")) 
                ) 
                print("Marketplace feed loaded.") 

                # Apply sorting and filtering
                self.apply_sorting_and_filtering(driver) 

                # Initialize prices
                all_prices = self.initialize_prices() 

                # Scroll to top and wait
                driver.execute_script("window.scrollTo(0, 0);") 
                time.sleep(2) 

                # Find all listing elements
                listing_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'x78zum5 xdt5ytf x1n2onr6')]//a[contains(@href, '/marketplace/item/')]")

                # NEW Collection Logic with duplicate prevention
                new_urls_added = 0
                for element in listing_elements:
                    try:
                        url = element.get_attribute('href')
                        if url and url not in scanned_urls and url not in listing_queue:
                            listing_queue.append(url)
                            new_urls_added += 1
                    except Exception as e:
                        print(f"Error processing listing element: {str(e)}")
                        continue

                print(f"Added {new_urls_added} new URLs to queue. Total queue size: {len(listing_queue)}")

                if not listing_elements: 
                    print("🚨 No listings found. Waiting for new listings to load...") 
                    time.sleep(5)  
                    continue

                # Process listings from queue
                while listing_queue:
                    if listings_scanned >= MAX_LISTINGS_TO_SCAN:
                        break
                    try:
                        # Get next URL from queue
                        listing_url = listing_queue.pop(0)
                        print(f"Processing listing {visible_listings_scanned + 1}: {listing_url}")
                        print(f"Remaining listings in queue: {len(listing_queue)}")
                        
                        # Skip if already scanned (double-check)
                        if listing_url in scanned_urls:
                            print(f"Skipping already scanned URL: {listing_url}")
                            continue
                        listing_id_url = self.extract_item_id(listing_url)
                    
                        try:
                            with open('listing_ids.txt', 'r') as f:
                                existing_ids = f.read().splitlines()
                            
                            if listing_id_url in existing_ids:
                                print('DUPLICATE FOUND')
                                consecutive_duplicate_count += 1
                        except Exception as e:
                            print(f"Error in determing if duplicate listing ID: {str(e)}")
                        try:
                            with open('listing_ids.txt', 'a') as f:
                                f.write(f"{listing_id_url}\n")
                            print(f"Saved listing ID: {listing_id_url}")
                        except Exception as e:
                            print(f"Error saving listing ID: {str(e)}")

                        if consecutive_duplicate_count >= 1:  
                            print(f"Consecutive duplicate count: {consecutive_duplicate_count}") 

                            if consecutive_duplicate_count >= 2: 
                                print(f"Detected 2 consecutive duplicates. Waiting for {WAIT_TIME_AFTER_REFRESH} seconds before refreshing.") 
                                time.sleep(WAIT_TIME_AFTER_REFRESH) 
                                consecutive_duplicate_count = 0 
                                break

                            continue
                        else:
                            
                            consecutive_duplicate_count = 0 

                        # Open new window and process listing
                        driver.execute_script("window.open('');") 
                        driver.switch_to.window(driver.window_handles[-1]) 

                        try: 
                            driver.get(listing_url) 
                            listing_info = self.extract_listing_info(driver, listing_url) 

                            
                            listing_info["url"] = listing_url

                            # Unified processing logic
                            if SHOW_ALL_LISTINGS or (not SHOW_ALL_LISTINGS and "Listing is suitable" in self.check_listing_suitability(listing_info)):
                                suitability_result = self.check_listing_suitability(listing_info)
                                profit_suitability, suitability_reason = self.process_suitable_listing(listing_info, all_prices, listings_scanned)
                                suitability_reason = suitability_result if not SHOW_ALL_LISTINGS else "Processed (SHOW_ALL_LISTINGS is True)"

                            if FAILURE_REASON_LISTED: 
                                self.write_to_file(f"\nListing {visible_listings_scanned + 1}: {listing_url}") 
                                self.write_to_file(f"Suitability: {suitability_reason}") 

                            # Mark URL as scanned
                            scanned_urls.append(listing_url)
                            
                            # Write scanned URL to file
                            with open(scanned_urls_file, 'a') as f: 
                                f.write(f"{listing_url}\n") 

                            listings_scanned += 1  
                            visible_listings_scanned += 1

                        except Exception as e:
                            print(f"An unexpected error occurred {str(e)}")
                            continue
                        finally: 
                            driver.close() 
                            driver.switch_to.window(main_window) 
                            
                            # Find new listing elements AFTER processing current listing
                            try:
                                new_listing_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'x78zum5 xdt5ytf x1n2onr6')]//a[contains(@href, '/marketplace/item/')]")
                                
                                # Counter to track new unique URLs
                                new_unique_urls_added = 0
                                
                                # Add only truly new URLs
                                for element in new_listing_elements:
                                    try:
                                        url = element.get_attribute('href')
                                        if url and url not in scanned_urls and url not in listing_queue:
                                            listing_queue.append(url)
                                            new_unique_urls_added += 1
                                    except Exception as e:
                                        print(f"Error processing new listing element: {str(e)}")
                                
                                print(f"Added {new_unique_urls_added} new unique URLs to queue. Total queue: {len(listing_queue)}")
                            
                            except Exception as e:
                                print(f"Error finding new listings: {e}")
                            
                            # Scroll periodically to load more listings
                            if listings_scanned % 10 == 0:  # Every 6 listings
                                self.scroll_page(driver, scroll_times=1)  # Scroll once
                    except Exception as e:
                        print(f"Error processing listing: {str(e)}")
                    # Break out if no more listings in queue
                    if not listing_queue:
                        print("Listing queue is empty. Breaking search loop.")
                        break

            except Exception as e:
                print(f"Error during searching: {str(e)}") 
                time.sleep(5)

    def apply_sorting_and_filtering(self, driver):
        """Apply sorting and filtering options on the marketplace."""
        try:
            # Sort by newest
            sort_by_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Sort by']"))
            )
            driver.execute_script("arguments[0].click();", sort_by_button)
            newest_first_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Date listed: Newest first']"))
            )
            driver.execute_script("arguments[0].click();", newest_first_option)
            time.sleep(2)

            # Filter by last 24 hours
            date_listed_dropdown = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'x1lliihq') and text()='Date listed']"))
            )
            driver.execute_script("arguments[0].click();", date_listed_dropdown)
            last_24_hours_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'x1lliihq') and text()='Last 24 hours']"))
            )
            driver.execute_script("arguments[0].click();", last_24_hours_option)
            time.sleep(2)
        except Exception as e:
            print(f"Error applying filters: {str(e)}")


    def extract_element_text_with_timeout(self, driver, selectors, element_name, timeout=element_exractor_timeout):
        print(f"Attempting to extract {element_name} with {timeout}s timeout...")
        for selector in selectors:
            try:
                element = WebDriverWait(driver, element_exractor_timeout).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                text = element.text.strip()
                if text:
                    print(f"Successfully extracted {element_name}: {text}")
                    return text
            except (TimeoutException, Exception) as e:
                print(f"Error with {element_name}")
        print(f"{element_name} not found within {element_exractor_timeout}s")
        return f"{element_name} not found"

    def extract_listing_info(self, driver, url):
        # Extract the listing ID from the URL

        driver.get(url)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        driver.get(url)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        raw_title = self.extract_element_text_with_timeout(driver, [
            "//h1[@aria-hidden='false']//span[contains(@class, 'x193iq5w') and contains(@class, 'xeuugli') and contains(@class, 'x13faqbe')]",
            "//h1[@aria-hidden='false']//span[contains(@class, 'x193iq5w') and contains(@class, 'xeuugli')]",
            "//h1[@aria-hidden='false']//span"
        ], "title")
        raw_description = self.extract_element_text_with_timeout(driver, ["//div[contains(@class, 'xz9dl7a x4uap5 xsag5q8')]//span[contains(@class, 'x193iq5w')]"], "description")

        listing_info = {
            "image_urls": self.extract_listing_images(driver),
            "title": raw_title.lower(),
            "description": raw_description.lower(),
            "join_date": self.extract_element_text_with_timeout(driver, ["//span[contains(@class, 'x193iq5w') and contains(@class, 'x1yc453h') and contains(text(), 'Joined Facebook')]", "//span[contains(text(), 'Joined Facebook')]"], "join_date"),
            "posting_date": self.extract_element_text_with_timeout(driver, ["//span[contains(@class, 'x193iq5w') and contains(@class, 'xeuugli') and contains(text(), 'Listed')]//span[@aria-hidden='true']", "//span[contains(text(), 'Listed')]//span[@aria-hidden='true']", "//span[contains(@class, 'x193iq5w') and contains(@class, 'xeuugli') and contains(text(), 'Listed')]"], "posting_date"),
        }
        
        if "see more" in listing_info["title"]:
            listing_info["title"] = listing_info["title"][:listing_info["title"].find("see more")]
        if len(listing_info["title"]) > 100:
            listing_info["title"] = listing_info["title"][:97] + "..."

        listing_info["posting_date"] = self.convert_to_minutes(listing_info["posting_date"]) if listing_info["posting_date"] != "posting_date not found" else max_posting_age_minutes + 1

        try:
            price_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x676frb.x1lkfr7t.x1lbecb7.xk50ysn.xzsf02u")))
            raw_price = re.sub(r'[^\d.]', '', price_element.text.split('Â·')[0].strip())
            
            if raw_price and raw_price != "0":
                # New price truncation logic
                if len(raw_price) > 3:
                    raw_price = raw_price[:3]  # Take the first 3 digits
                
                multiplied_price = float(raw_price) * price_mulitplier
                listing_info["price"] = str(multiplied_price)
            else:
                listing_info["price"] = "0"
        except:
            listing_info["price"] = "0"

        listing_info["expected_revenue"] = None
        listing_info["profit"] = None
        listing_info["detected_items"] = {}
        listing_info["processed_images"] = self.download_and_process_images(listing_info["image_urls"])

        return listing_info

    def extract_element_text(self, driver, selectors, element_name):
        print(f"Attempting to extract {element_name}...")
        for selector in selectors:
            try:
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, selector)))
                text = element.text.strip()
                if text:
                    print(f"Successfully extracted {element_name}: {text}")
                    return text
            except Exception as e:
                print(f"Error extracting {element_name} with selector {selector}: {str(e)}")
        
        print(f"{element_name} not found")
        return f"{element_name} not found"

    def extract_listing_images(self, driver):
        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img.x5yr21d.xl1xv1r.xh8yej3")))
            return list(set(img.get_attribute("src") for img in driver.find_elements(By.CSS_SELECTOR, "img.x5yr21d.xl1xv1r.xh8yej3")))
        except Exception as e:
            print(f"Error in image extraction: {str(e)}")
            return []

    def convert_to_minutes(self, time_str):
        time_units = {
            'minute': 1, 'hour': 60, 'day': 1440,
            'week': 10080, 'month': 43200, 'year': 525600
        }
        for unit, multiplier in time_units.items():
            if unit in time_str:
                match = re.search(r'\d+', time_str)
                if match:
                    count = int(match.group())
                else:
                    count = 1 if f'a {unit}' in time_str else 0
                return count * multiplier
        return 0

    def check_listing_suitability(self, listing_info):
        checks = [
            
            (lambda: any(word in listing_info["title"].lower() for word in title_forbidden_words),
            "Title contains forbidden words"),
            (lambda: not any(word in listing_info["title"].lower() for word in title_must_contain),
            "Title does not contain any required words"),
            (lambda: any(word in listing_info["description"].lower() for word in description_forbidden_words),
            "Description contains forbidden words"),
            (lambda: "join_date not found" not in listing_info["join_date"].lower() and 
                    int(listing_info["join_date"].split()[-1]) == 2025,
            "Seller joined Facebook in 2025"),
            (lambda: listing_info["price"] != "Price not found" and 
                    (float(listing_info["price"]) < min_price or float(listing_info["price"]) > max_price),
            f"Price £{listing_info['price']} is outside the range £{min_price}-£{max_price}"),
            (lambda: len(re.findall(r'[£$]\s*\d+|\d+\s*[£$]', listing_info["description"])) >= 3,
            "Too many $ symbols"),
            (lambda: float(listing_info["price"]) in BANNED_PRICES,
            "Price in banned prices"),
        ]
        for check, message in checks:
            try:
                if check():
                    return f"Unsuitable: {message}"
            except (ValueError, IndexError, AttributeError, TypeError):
                if "price" in message:
                    return "Unsuitable: Unable to parse price"
                if "posting_date" in message:
                    return "Unsuitable: Unable to parse posting date"
                continue

        return "Listing is suitable"

    def save_image(self, image_url, save_path):
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                with open(save_path, 'wb') as file:
                    file.write(response.content)
                saved_images = 0
                saved_images + 1
                return True
            else:
                print(f"Failed to download image. Status code: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error saving image: {str(e)}")
            return False

    def perform_detection_on_listing_images(self, model, listing_dir):
        """
        Enhanced object detection with all Facebook exceptions and logic
        MODIFIED: All game classes are now capped at 1 per listing
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
        
        # NEW CODE: Cap all game classes at 1 per listing
        # Define the game classes that need to be capped
        game_classes_to_cap = [
            '1_2_switch', 'animal_crossing', 'arceus_p', 'bow_z', 'bros_deluxe_m', 'crash_sand',
            'dance', 'diamond_p', 'evee', 'fifa_23', 'fifa_24', 'gta', 'just_dance', 'kart_m', 'kirby',
            'lets_go_p', 'links_z', 'luigis', 'mario_maker_2', 'mario_sonic', 'mario_tennis', 'minecraft',
            'minecraft_dungeons', 'minecraft_story', 'miscellanious_sonic', 'odyssey_m', 'other_mario',
            'party_m', 'rocket_league', 'scarlet_p', 'shield_p', 'shining_p', 'skywards_z', 'smash_bros',
            'snap_p', 'splatoon_2', 'splatoon_3', 'super_m_party', 'super_mario_3d', 'switch_sports',
            'sword_p', 'tears_z', 'violet_p'
        ]
        
        # Cap each game class at maximum 1
        games_capped = []
        for game_class in game_classes_to_cap:
            if final_detected_objects.get(game_class, 0) > 1:
                original_count = final_detected_objects[game_class]
                final_detected_objects[game_class] = 1
                games_capped.append(f"{game_class}: {original_count} -> 1")
        
        # Print capping information if any games were capped
        if games_capped:
            print(f"🎮 GAMES CAPPED: {', '.join(games_capped)}")
        
        return final_detected_objects, processed_images

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

    def check_profit_suitability(self, listing_price, profit_percentage):
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

    def calculate_revenue(self, detected_objects, all_prices, listing_price, listing_title, listing_description):
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
        
        # Count detected games
        detected_games_count = sum(detected_objects.get(game, 0) for game in game_classes)
        
        # Find highest number before "games" in title and description
        def extract_games_number(text):
        # Prioritize specific game type matches first
            matches = (
                re.findall(r'(\d+)\s*(switch|nintendo)\s*games', text.lower()) +  # Switch/Nintendo specific
                re.findall(r'(\d+)\s*games', text.lower())  # Generic games
            )
            
            # Convert matches to integers and find the maximum
            numeric_matches = [int(match[0]) if isinstance(match, tuple) else int(match) for match in matches]
            
            return max(numeric_matches) if numeric_matches else 0
        
        title_games = extract_games_number(listing_title)
        desc_games = extract_games_number(listing_description)
        text_games_count = max(title_games, desc_games)
        
        # Calculate miscellaneous games
        misc_games_count = max(0, text_games_count - detected_games_count)
        misc_games_revenue = misc_games_count * miscellaneous_games_price
        
        adjustments = {
            'oled_box': ['switch', 'comfort_h', 'tv_white'],
            'switch_box': ['switch', 'comfort_h', 'tv_black'],
            'lite_box': ['lite']
        }

        for box, items in adjustments.items():
            box_count = detected_objects.get(box, 0)
            for item in items:
                detected_objects[item] = max(0, detected_objects.get(item, 0) - box_count)
        detected_objects.pop('switch_screen', None)

        display_objects = detected_objects.copy()

        sd_card_keywords = SD_CARD_WORD
        title_lower = listing_title.lower()
        desc_lower = listing_description.lower()

        sd_card_present = any(keyword in title_lower or keyword in desc_lower for keyword in sd_card_keywords)

        total_revenue = misc_games_revenue

        if sd_card_present:
            total_revenue += sd_card_revenue
            print(f"SD Card detected: Added £{sd_card_revenue} to revenue")

        for item, count in detected_objects.items():
            # Safely handle both string and integer counts
            if isinstance(count, str):
                count_match = re.match(r'(\d+)', count)
                count = int(count_match.group(1)) if count_match else 0
            
            item_price = all_prices.get(item, 0)
            if item == 'controller' and 'pro' in listing_title.lower() and count > 0:
                pro_price = item_price + 7.50
                total_revenue += pro_price * count
            else:
                total_revenue += item_price * count
        
        print("\nRevenue Breakdown:")
        for item, count in detected_objects.items():
            # Safely handle both string and integer counts
            if isinstance(count, str):
                count_match = re.match(r'(\d+)', count)
                count = int(count_match.group(1)) if count_match else 0
            
            if item in all_prices:
                base_price = all_prices[item]
                if item == 'controller' and 'pro' in listing_title.lower() and count > 0:
                    item_revenue = (base_price + 7.50) * count
                else:
                    item_revenue = base_price * count
            else:
                print(f"Cannot calculate price for {item}. Price not found.")
        
        if misc_games_count > 0:
            print(f"Miscellaneous games: {misc_games_count} x £{miscellaneous_games_price:.2f} = £{misc_games_revenue:.2f}")

        expected_profit = total_revenue - listing_price
        profit_percentage = (expected_profit / listing_price) * 100 if listing_price > 0 else 0

        print(f"Listing Price: £{listing_price:.2f}")
        print(f"Total Expected Revenue: £{total_revenue:.2f}")
        print(f"Expected Profit/Loss: £{expected_profit:.2f} ({profit_percentage:.2f}%)")

        controller_count = detected_objects.get('controller', 0)
        if controller_count > 0:
            item_price = all_prices.get('controller', 0)
            if 'pro' in listing_title.lower():
                pro_price = item_price + 7.50
                total_revenue += pro_price * controller_count
        
        # Remove controller from detected_objects before returning

        return total_revenue, expected_profit, profit_percentage, display_objects

    def write_listing_to_file(self, output_file_path, listing_info, suitability_result):
        with open(output_file_path, 'a') as f:
            if SHOW_ALL_LISTINGS or "Listing is suitable" in suitability_result:
                f.write(f"Listing {listing_info['unique_id']}: {listing_info['url']} Price: £{listing_info['price']}, Expected revenue: £{listing_info.get('expected_revenue', 0):.2f} ")
                if listing_info.get('detected_items'):
                    f.write("Detected items: ")
                    for item, count in listing_info['detected_items'].items():
                        f.write(f"{item}={count} ")
                f.write(f"Suitability: {suitability_result}\n")
            else:
                f.write(f"Listing {listing_info['unique_id']} was unsuitable: {suitability_result} {listing_info['url']}\n")

    def initialize_prices(self):
        return self.fetch_all_prices()

    def run(self):
        global scraper_instance
        scraper_instance = self
        global driver, messaging_driver, current_listing_url  # Add current_listing_url to globals

        if setup_website:
            print("Setting up Cloudflare Tunnel website tunnel...")
            # Since run_flask_app() now integrates Cloudflare Tunnel (via cloudflared),
            # you don't need to call a separate tunnel setup function here.
            # (Any additional Cloudflare initialization code could go here if needed.)

        self.clear_output_file()

        # Start the Flask app in a separate thread
        flask_thread = threading.Thread(target=self.run_flask_app)
        flask_thread.daemon = True
        flask_thread.start()

        pygame_thread = threading.Thread(target=self.run_pygame_window)
        pygame_thread.start()

        # Set up two separate drivers
        driver = None
        messaging_driver = None

        try:
            # Setup Chrome Profile Driver for scraping
            driver = self.setup_chrome_profile_driver()

            # Setup a second, separate Chrome Driver for messaging
            messaging_driver = self.setup_chrome_messaging_driver()

            if messaging_driver is None:
                print("Failed to initialize messaging driver. Exiting.")
                return
            
            driver_restart_thread = threading.Thread(target=self.periodically_restart_messaging_driver, daemon=True)
            driver_restart_thread.start()

            print("Logging in to Facebook on second driver...")
            self.login_to_facebook(driver)

            all_prices = self.initialize_prices()

            # Initialize current_listing_url
            current_listing_url = ""

            self.update_listing_details("", "", "", "0", None, None, {}, [], None)

            print(f"Searching for listings with query: {search_query}")
            self.search_and_select_listings(driver, search_query, OUTPUT_FILE_PATH)

        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            import traceback
            traceback.print_exc()

        finally:
            if driver:
                driver.quit()
            if messaging_driver:
                messaging_driver.quit()

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
        FIXED: Enhanced button click handler with better error handling and driver management
        MODIFIED: Now checks wait_for_bookmark_stopwatch_to_buy variable and waits for bookmark timer
        """
        print(f"🔘 VINTED BUTTON: Processing {url}")
        
        # Check if already clicked to prevent duplicates
        if url in self.clicked_yes_listings:
            print(f"🔄 VINTED BUTTON: Listing {url} already processed, ignoring")
            return
        
        # Mark as clicked immediately to prevent race conditions
        self.clicked_yes_listings.add(url)
        
        # NEW: Check wait_for_bookmark_stopwatch_to_buy variable
        if wait_for_bookmark_stopwatch_to_buy:
            print(f"⏰ WAITING: wait_for_bookmark_stopwatch_to_buy is TRUE")
            
            # Check if this listing has a bookmark timer
            if url in self.bookmark_timers:
                print(f"⏰ TIMER: Found active bookmark timer for {url}")
                
                # Calculate how long the listing has been bookmarked
                # We need to track when bookmarking started for each listing
                if not hasattr(self, 'bookmark_start_times'):
                    self.bookmark_start_times = {}
                
                if url in self.bookmark_start_times:
                    elapsed_time = time.time() - self.bookmark_start_times[url]
                    remaining_time = bookmark_stopwatch_length - elapsed_time
                    
                    if remaining_time > 0:
                        print(f"⏰ WAITING: Need to wait {remaining_time:.1f} more seconds for bookmark timer")
                        print(f"⏰ STATUS: Listing has been bookmarked for {elapsed_time:.1f} seconds")
                        
                        # Wait for the remaining time
                        time.sleep(remaining_time)
                        print(f"⏰ COMPLETE: Bookmark timer reached {bookmark_stopwatch_length} seconds")
                    else:
                        print(f"⏰ READY: Bookmark timer already exceeded {bookmark_stopwatch_length} seconds")
                else:
                    print(f"⚠️ WARNING: No bookmark start time found for {url}, proceeding immediately")
            else:
                print(f"⚠️ WARNING: No bookmark timer found for {url}, proceeding immediately")
        else:
            print(f"🚀 IMMEDIATE: wait_for_bookmark_stopwatch_to_buy is FALSE, proceeding immediately")
        
        # FIXED: Better driver acquisition with retry logic
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            driver_num, driver = self.get_available_driver()
            
            if driver is not None:
                # Successfully got a driver, process in separate thread
                processing_thread = threading.Thread(
                    target=self.process_single_listing_with_driver,
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
        # Remove from clicked list so they can try again later
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
            # INSTANT bookmark execution - now with username parameter
            print(f"🔖 INSTANT BOOKMARK: {url}")
            
            # Capture stdout to detect the success message
            from io import StringIO
            import contextlib
            
            # Create a string buffer to capture print output
            captured_output = StringIO()
            
            # Temporarily redirect stdout to capture the bookmark_driver output
            with contextlib.redirect_stdout(captured_output):
                self.bookmark_driver(url, username)
            
            # Get the captured output and restore normal stdout
            bookmark_output = captured_output.getvalue()
            
            # Print the captured output normally so you can still see it
            print(bookmark_output, end='')
            
            # Check if the success message was printed
            if 'SUCCESSFUL BOOKMARK! CONFIRMED VIA PROCESSING PAYMENT!' in bookmark_output:
                bookmark_success = True
                print("🎉 BOOKMARK SUCCESS DETECTED!")
                self.start_bookmark_stopwatch(url)
            else:
                print("❌ Bookmark did not succeed")

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
        DRIVER_RESTART_INTERVAL = 250
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

    def bookmark_driver(self, listing_url, username=None):
        """
        ENHANCED ROBUST bookmark driver with success rate logging, selector alternatives, and failure fast-path
        CRITICAL: Preserves the exact 0.25 second wait and tab closing sequence after pay button click
        """
        
        # SUCCESS RATE LOGGING - Track exactly where and when things break
        step_log = {
            'start_time': time.time(),
            'steps_completed': [],
            'failures': [],
            'success': False,
            'critical_sequence_completed': False
        }
        
        def log_step(step_name, success=True, error_msg=None):
            """Log each step for debugging and success rate analysis"""
            if success:
                step_log['steps_completed'].append(f"{step_name} - {time.time() - step_log['start_time']:.2f}s")
                print(f"✅ STEP: {step_name}")
            else:
                step_log['failures'].append(f"{step_name}: {error_msg} - {time.time() - step_log['start_time']:.2f}s")
                print(f"❌ STEP: {step_name} - {error_msg}")
        
        def log_final_result():
            """Log final results for success rate analysis"""
            total_time = time.time() - step_log['start_time']
            print(f"\n📊 BOOKMARK ANALYSIS for {listing_url[:50]}...")
            print(f"⏱️  Total time: {total_time:.2f}s")
            print(f"✅ Steps completed: {len(step_log['steps_completed'])}")
            print(f"❌ Failures: {len(step_log['failures'])}")
            print(f"🎯 Critical sequence: {'YES' if step_log['critical_sequence_completed'] else 'NO'}")
            print(f"🏆 Overall success: {'YES' if step_log['success'] else 'NO'}")
            
            # Log failures for analysis
            if step_log['failures']:
                print("🔍 FAILURE DETAILS:")
                for failure in step_log['failures']:
                    print(f"  • {failure}")
        
        # SELECTOR ALTERNATIVES - For each critical element, have 3-4 backup selectors ready
        SELECTOR_SETS = {
            'buy_button': [
                "button[data-testid='item-buy-button']",  # Primary
                "button.web_ui__Button__primary[data-testid='item-buy-button']",  # With class
                "button.web_ui__Button__button.web_ui__Button__filled.web_ui__Button__default.web_ui__Button__primary.web_ui__Button__truncated",  # Full class chain
                "//button[@data-testid='item-buy-button']",  # XPath fallback
                "//button[contains(@class, 'web_ui__Button__primary')]//span[text()='Buy now']"  # Text-based XPath
            ],
            
            'pay_button': [
                'button[data-testid="single-checkout-order-summary-purchase-button"]',  # Primary
                'button[data-testid="single-checkout-order-summary-purchase-button"].web_ui__Button__primary',  # With class
                '//button[@data-testid="single-checkout-order-summary-purchase-button"]',  # XPath
                'button.web_ui__Button__primary[data-testid*="purchase"]',  # Partial match
                '//button[contains(@data-testid, "purchase-button")]'  # Broader XPath
            ],
            
            'processing_payment': [
                "//h2[@class='web_ui__Text__text web_ui__Text__title web_ui__Text__left' and text()='Processing payment']",  # Exact
                "//h2[contains(@class, 'web_ui__Text__title') and text()='Processing payment']",  # Broader class match
                "//span[@class='web_ui__Text__text web_ui__Text__body web_ui__Text__left web_ui__Text__format' and contains(text(), \"We've reserved this item for you until your payment finishes processing\")]",  # Alternative message
                "//span[contains(text(), \"We've reserved this item for you until your payment finishes processing\")]",  # Broader span match
                "//*[contains(text(), 'Processing payment')]"  # Very broad fallback
            ],
            
            'messages_button': [
                "a[data-testid='header-conversations-button']",  # Primary
                "a[href='/inbox'][data-testid='header-conversations-button']",  # With href
                "a[href='/inbox'].web_ui__Button__button",  # Class-based
                "a[aria-label*='message'][href='/inbox']",  # Aria-label based
                "a[href='/inbox']"  # Broad fallback
            ]
        }
        
        def try_selectors(driver, selector_set_name, operation='find', timeout=5, click_method='standard'):
            """
            FAILURE FAST-PATH - Try selectors with quick timeouts and fail fast
            Returns (element, selector_used) or (None, None) if all fail
            """
            selectors = SELECTOR_SETS.get(selector_set_name, [])
            if not selectors:
                log_step(f"try_selectors_{selector_set_name}", False, "No selectors defined")
                return None, None
            
            for i, selector in enumerate(selectors):
                try:
                    log_step(f"trying_selector_{selector_set_name}_{i+1}", True, f"Selector: {selector[:30]}...")
                    
                    # Quick timeout per selector - fail fast approach
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
                    
                    # If we need to click, try different click methods
                    if operation == 'click':
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
                                log_step(f"click_{selector_set_name}_{method}", True)
                                break
                            except Exception as click_error:
                                log_step(f"click_{selector_set_name}_{method}", False, str(click_error))
                                continue
                        
                        if not click_success:
                            continue  # Try next selector if all click methods fail
                    
                    log_step(f"selector_{selector_set_name}_success", True, f"Used selector #{i+1}")
                    return element, selector
                    
                except TimeoutException:
                    log_step(f"selector_{selector_set_name}_{i+1}_timeout", False, f"Timeout after {timeout}s")
                    continue
                except Exception as e:
                    log_step(f"selector_{selector_set_name}_{i+1}_error", False, str(e))
                    continue
            
            log_step(f"all_selectors_{selector_set_name}_failed", False, f"All {len(selectors)} selectors failed")
            return None, None
        
        # START OF MAIN FUNCTION LOGIC
        print('🔖 ENHANCED: Entering enhanced bookmark_driver with robust error handling')
        
        # Test mode handling
        if test_bookmark_function:
            actual_url = test_bookmark_link
            log_step("test_mode_activated", True, f"Using test URL: {actual_url}")
        else:
            actual_url = listing_url
            log_step("normal_mode_activated", True)
        
        # Username validation
        if not username:
            log_step("username_validation", False, "No username provided")
            log_final_result()
            print("⚠️ Could not extract username, possible unable to detect false buy, exiting.")
            sys.exit(0)
        
        log_step("username_validation", True, f"Username: {username}")
        print(f"🔖 Looking at listing {actual_url} posted by {username}")
        
        try:
            bookmark_start_time = time.time()
            log_step("function_start", True)
            
            # ENHANCED DRIVER INITIALIZATION with better error handling
            if not hasattr(self, 'persistent_bookmark_driver') or self.persistent_bookmark_driver is None:
                log_step("driver_initialization_start", True)
                
                # SPEED OPTIMIZATION: Pre-cached service
                if not hasattr(self, '_cached_chromedriver_path'):
                    try:
                        self._cached_chromedriver_path = ChromeDriverManager().install()
                        log_step("chromedriver_cache", True)
                    except Exception as e:
                        log_step("chromedriver_cache", False, str(e))
                        log_final_result()
                        return False
                
                # ROBUST CHROME OPTIONS
                try:
                    chrome_opts = Options()
                    bookmark_user_data_dir = "C:\VintedScraper_Default_Bookmark"
                    chrome_opts.add_argument(f"--user-data-dir={bookmark_user_data_dir}")
                    chrome_opts.add_argument("--profile-directory=Profile 4")
                    #chrome_opts.add_argument("--headless")
                    chrome_opts.add_argument("--no-sandbox")
                    chrome_opts.add_argument("--disable-dev-shm-usage")
                    chrome_opts.add_argument("--disable-gpu")
                    chrome_opts.add_argument("--window-size=800,600")
                    chrome_opts.add_argument("--log-level=3")
                    chrome_opts.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
                    
                    service = Service(self._cached_chromedriver_path, log_path=os.devnull)
                    log_step("chrome_options_configured", True)
                    
                    self.persistent_bookmark_driver = webdriver.Chrome(service=service, options=chrome_opts)
                    log_step("driver_created", True)
                    
                    # BALANCED timeouts - fail fast but not too aggressive
                    self.persistent_bookmark_driver.implicitly_wait(1)
                    self.persistent_bookmark_driver.set_page_load_timeout(8)
                    self.persistent_bookmark_driver.set_script_timeout(3)
                    log_step("timeouts_configured", True)
                    
                    # Navigate to Vinted homepage
                    try:
                        self.persistent_bookmark_driver.get("https://www.vinted.co.uk")
                        log_step("homepage_navigation", True)
                    except Exception as homepage_error:
                        log_step("homepage_navigation", False, str(homepage_error))
                        # Don't fail completely if homepage fails
                        
                except Exception as driver_setup_error:
                    log_step("driver_initialization", False, str(driver_setup_error))
                    log_final_result()
                    return False
            else:
                # Test existing driver
                try:
                    self.persistent_bookmark_driver.current_url
                    log_step("existing_driver_health_check", True)
                except Exception as health_error:
                    log_step("existing_driver_health_check", False, str(health_error))
                    self.persistent_bookmark_driver = None
                    return self.bookmark_driver(listing_url, username)  # Recursive retry
            
            # ENHANCED TAB MANAGEMENT
            try:
                stopwatch_start = time.time()
                print("⏱️ STOPWATCH: Starting timer for new tab and navigation...")
                self.persistent_bookmark_driver.execute_script("window.open('');")
                new_tab = self.persistent_bookmark_driver.window_handles[-1]
                self.persistent_bookmark_driver.switch_to.window(new_tab)
                log_step("new_tab_created", True, f"Total tabs: {len(self.persistent_bookmark_driver.window_handles)}")
            except Exception as tab_error:
                log_step("new_tab_created", False, str(tab_error))
                log_final_result()
                return False
            
            # ROBUST NAVIGATION with retry
            navigation_success = False
            for nav_attempt in range(3):  # Try navigation up to 3 times
                try:
                    log_step(f"navigation_attempt_{nav_attempt+1}", True)
                    self.persistent_bookmark_driver.get(actual_url)
                    navigation_success = True
                    log_step("navigation_complete", True)
                    break
                except Exception as nav_error:
                    log_step(f"navigation_attempt_{nav_attempt+1}", False, str(nav_error))
                    if nav_attempt == 2:  # Last attempt
                        log_step("navigation_final_failure", False, "All navigation attempts failed")
                        self.persistent_bookmark_driver.close()
                        if len(self.persistent_bookmark_driver.window_handles) > 0:
                            self.persistent_bookmark_driver.switch_to.window(self.persistent_bookmark_driver.window_handles[0])
                        log_final_result()
                        return False
                    time.sleep(1)  # Brief pause between retries
            
            # FIRST BUY NOW SEQUENCE with enhanced error handling
            log_step("first_sequence_start", True)
            
            first_buy_element, first_buy_selector = try_selectors(
                self.persistent_bookmark_driver, 
                'buy_button', 
                operation='click', 
                timeout=5, 
                click_method='all'
            )
            
            if first_buy_element:
                log_step("first_buy_button_clicked", True, f"Used: {first_buy_selector[:30]}...")
                
     
                pay_element, pay_selector = try_selectors(
                    self.persistent_bookmark_driver,
                    'pay_button',
                    operation='find',
                    timeout=10
                )
                
                if pay_element:
                    log_step("pay_button_found", True, f"Used: {pay_selector[:30]}...")
                    # CRITICAL SEQUENCE - This is the part that CANNOT be touched!
                    try:
                        # FIXED: Force-click the pay button using multiple aggressive methods
                        pay_clicked = False
                        
                        # Method 1: Click the inner span (Pay text) directly - this bypasses disabled button issues
                        try:
                            pay_span = self.persistent_bookmark_driver.find_element(By.XPATH, "//button[@data-testid='single-checkout-order-summary-purchase-button']//span[text()='Pay']")
                            pay_span.click()
                            log_step("pay_button_click_span", True, "Clicked Pay span directly")
                            pay_clicked = True
                        except Exception as span_error:
                            log_step("pay_button_click_span", False, str(span_error))
                        
                        # Method 2: If span click failed, try aggressive JavaScript on button
                        if not pay_clicked:
                            try:
                                # Force enable button and click it
                                self.persistent_bookmark_driver.execute_script("""
                                    var button = document.querySelector('button[data-testid="single-checkout-order-summary-purchase-button"]');
                                    if (button) {
                                        button.disabled = false;
                                        button.setAttribute('aria-disabled', 'false');
                                        button.click();
                                    }
                                """)
                                log_step("pay_button_click_force_js", True, "Force-enabled and clicked via JS")
                                pay_clicked = True
                            except Exception as js_error:
                                log_step("pay_button_click_force_js", False, str(js_error))
                        
                        # Method 3: If still failed, try dispatching click event directly
                        if not pay_clicked:
                            try:
                                self.persistent_bookmark_driver.execute_script("""
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
                                log_step("pay_button_click_dispatch_event", True, "Dispatched click event directly")
                                pay_clicked = True
                            except Exception as dispatch_error:
                                log_step("pay_button_click_dispatch_event", False, str(dispatch_error))
                        
                        # Method 4: Last resort - try form submission
                        if not pay_clicked:
                            try:
                                self.persistent_bookmark_driver.execute_script("""
                                    var button = document.querySelector('button[data-testid="single-checkout-order-summary-purchase-button"]');
                                    var form = button ? button.closest('form') : null;
                                    if (form) {
                                        form.submit();
                                    }
                                """)
                                log_step("pay_button_form_submit", True, "Submitted form directly")
                                pay_clicked = True
                            except Exception as form_error:
                                log_step("pay_button_form_submit", False, str(form_error))
                        
                        if pay_clicked:
                            # ⚠️ CRITICAL: Exact 0.25 second wait - DO NOT MODIFY! ⚠️
                            print("🔖 CRITICAL: Waiting exactly 0.25 seconds...")
                            time.sleep(0.25)
                            
                            # ⚠️ CRITICAL: Immediate tab close - DO NOT MODIFY! ⚠️
                            print("🔖 CRITICAL: Closing tab immediately...")
                            self.persistent_bookmark_driver.close()

                            stopwatch_end = time.time()
                            elapsed = stopwatch_end - stopwatch_start
                            print(f"⏱️ STOPWATCH: First sequence completed in {elapsed:.3f} seconds")
                                            
                            step_log['critical_sequence_completed'] = True
                            log_step("critical_sequence_completed", True, "0.25s wait + tab close")
                            
                            # Continue with timing and tab management...
                            bookmark_end_time = time.time()
                            total_elapsed_time = bookmark_end_time - bookmark_start_time
                            log_step("first_sequence_timing", True, f"Completed in {total_elapsed_time:.2f}s")
                            
                            # Switch back to main tab
                            if len(self.persistent_bookmark_driver.window_handles) > 0:
                                self.persistent_bookmark_driver.switch_to.window(self.persistent_bookmark_driver.window_handles[0])
                                log_step("return_to_main_tab", True)
                            
                            log_step("first_sequence_complete", True)
                        else:
                            log_step("pay_button_click_all_failed", False, "All 4 aggressive methods failed")
                            self.persistent_bookmark_driver.close()
                            if len(self.persistent_bookmark_driver.window_handles) > 0:
                                self.persistent_bookmark_driver.switch_to.window(self.persistent_bookmark_driver.window_handles[0])
                            log_final_result()
                            return False
                            
                    except Exception as critical_error:
                        log_step("critical_sequence_error", False, str(critical_error))
                        self.persistent_bookmark_driver.close()
                        if len(self.persistent_bookmark_driver.window_handles) > 0:
                            self.persistent_bookmark_driver.switch_to.window(self.persistent_bookmark_driver.window_handles[0])
                        log_final_result()
                        return False
                else:
                    log_step("pay_button_not_found", False, "No pay button found with any selector")
                    self.persistent_bookmark_driver.close()
                    if len(self.persistent_bookmark_driver.window_handles) > 0:
                        self.persistent_bookmark_driver.switch_to.window(self.persistent_bookmark_driver.window_handles[0])
            else:
                log_step("first_buy_button_not_found", False, "Item likely already sold")
                print('🔖 FIRST SEQUENCE: Buy button not found - this means ALREADY SOLD!!!')
                self.persistent_bookmark_driver.close()
                if len(self.persistent_bookmark_driver.window_handles) > 0:
                    self.persistent_bookmark_driver.switch_to.window(self.persistent_bookmark_driver.window_handles[0])
                log_final_result()
                return False
            
            # SECOND SEQUENCE - Enhanced with better error handling
            log_step("second_sequence_start", True)
            
            try:
                # Open new tab for second sequence
                self.persistent_bookmark_driver.execute_script("window.open('');")
                second_tab = self.persistent_bookmark_driver.window_handles[-1]
                self.persistent_bookmark_driver.switch_to.window(second_tab)
                log_step("second_tab_created", True)
                
                # Navigate again with retry logic
                second_nav_success = False
                for nav_attempt in range(2):
                    try:
                        self.persistent_bookmark_driver.get(actual_url)
                        second_nav_success = True
                        log_step("second_navigation", True)
                        break
                    except Exception as second_nav_error:
                        log_step(f"second_navigation_attempt_{nav_attempt+1}", False, str(second_nav_error))
                        if nav_attempt == 1:  # Last attempt
                            break
                        time.sleep(0.5)
                
                if not second_nav_success:
                    log_step("second_navigation_failed", False, "Could not navigate for second sequence")
                    self.persistent_bookmark_driver.close()
                    if len(self.persistent_bookmark_driver.window_handles) > 0:
                        self.persistent_bookmark_driver.switch_to.window(self.persistent_bookmark_driver.window_handles[0])
                    log_final_result()
                    return False
                
                # Look for buy button again with enhanced selectors
                second_buy_element, second_buy_selector = try_selectors(
                    self.persistent_bookmark_driver,
                    'buy_button',
                    operation='click',
                    timeout=15,
                    click_method='all'
                )
                
                if second_buy_element:
                    log_step("second_buy_button_clicked", True, f"Used: {second_buy_selector[:30]}...")
                    
                    # Look for processing payment message with enhanced selectors
                    processing_element, processing_selector = try_selectors(
                        self.persistent_bookmark_driver,
                        'processing_payment',
                        operation='find',
                        timeout=3
                    )
                    
                    if processing_element:
                        element_text = processing_element.text.strip()
                        log_step("processing_payment_found", True, f"Text: {element_text}")
                        print('SUCCESSFUL BOOKMARK! CONFIRMED VIA PROCESSING PAYMENT!')
                        step_log['success'] = True
                    else:
                        log_step("processing_payment_not_found", False, "Processing payment message not found")
                        print('listing likely bookmarked by another')
                    
                    # Close second tab
                    self.persistent_bookmark_driver.close()
                    if len(self.persistent_bookmark_driver.window_handles) > 0:
                        self.persistent_bookmark_driver.switch_to.window(self.persistent_bookmark_driver.window_handles[0])
                    log_step("second_tab_closed", True)
                    
                    log_final_result()
                    return True
                    
                else:
                    log_step("second_buy_button_not_found", False, "Proceeding with messages")
                    # Continue with messages functionality...
                    
                    # ENHANCED MESSAGES FUNCTIONALITY
                    log_step("messages_sequence_start", True)
                    
                    try:
                        # Open messages tab
                        self.persistent_bookmark_driver.execute_script("window.open('');")
                        messages_tab = self.persistent_bookmark_driver.window_handles[-1]
                        self.persistent_bookmark_driver.switch_to.window(messages_tab)
                        log_step("messages_tab_created", True)
                        
                        # Navigate to URL for messages
                        self.persistent_bookmark_driver.get(actual_url)
                        log_step("messages_navigation", True)
                        
                        # Find messages button with enhanced selectors
                        messages_element, messages_selector = try_selectors(
                            self.persistent_bookmark_driver,
                            'messages_button',
                            operation='click',
                            timeout=1,
                            click_method='all'
                        )
                        
                        if messages_element:
                            log_step("messages_button_clicked", True, f"Used: {messages_selector[:30]}...")
                            
                            # Search for username if available
                            if username:
                                log_step("username_search_start", True, f"Searching for: {username}")
                                
                                time.sleep(2)  # Wait for messages page to load
                                
                                try:
                                    username_element = WebDriverWait(self.persistent_bookmark_driver, 3).until(
                                        EC.element_to_be_clickable((By.XPATH, f"//h2[contains(@class, 'web_ui') and contains(@class, 'Text') and contains(@class, 'title') and text()='{username}']"))
                                    )
                                    
                                    log_step("username_found_on_messages", True, f"Found: {username}")
                                    
                                    # Try to click username
                                    username_clicked = False
                                    for click_method in ['standard', 'javascript', 'actionchains']:
                                        try:
                                            if click_method == 'standard':
                                                username_element.click()
                                            elif click_method == 'javascript':
                                                self.persistent_bookmark_driver.execute_script("arguments[0].click();", username_element)
                                            elif click_method == 'actionchains':
                                                ActionChains(self.persistent_bookmark_driver).move_to_element(username_element).click().perform()
                                            
                                            username_clicked = True
                                            log_step(f"username_clicked_{click_method}", True)
                                            break
                                        except:
                                            continue
                                    
                                    if username_clicked:
                                        log_step("accidental_purchase_detected", True, "ABORT - username found in messages")
                                        print("USERNAME FOUND, POSSIBLE ACCIDENTAL PURCHASE, ABORT")
                                        time.sleep(3)
                                        log_final_result()
                                        sys.exit(0)
                                    else:
                                        log_step("username_click_failed", False, "Could not click username")
                                        
                                except TimeoutException:
                                    log_step("username_not_found_in_messages", True, f"Username {username} not in messages - likely bookmarked!")
                                    print(f"📧 NOT FOUND: Username '{username}' not found on messages page")
                                    print(f"unable to find username {username} for listing {actual_url}, likely bookmarked!")
                                except Exception as search_error:
                                    log_step("username_search_error", False, str(search_error))
                                    print(f"unable to find username {username} for listing {actual_url}, likely bookmarked!")
                            else:
                                log_step("no_username_for_search", False, "No username available")
                                time.sleep(3)
                        else:
                            log_step("messages_button_not_found", False, "Messages button not found with any selector")
                        
                        # Close messages tab
                        self.persistent_bookmark_driver.close()
                        if len(self.persistent_bookmark_driver.window_handles) > 0:
                            self.persistent_bookmark_driver.switch_to.window(self.persistent_bookmark_driver.window_handles[0])
                        log_step("messages_tab_closed", True)
                        
                    except Exception as messages_error:
                        log_step("messages_sequence_error", False, str(messages_error))
                        # Clean up messages tab
                        try:
                            self.persistent_bookmark_driver.close()
                            if len(self.persistent_bookmark_driver.window_handles) > 0:
                                self.persistent_bookmark_driver.switch_to.window(self.persistent_bookmark_driver.window_handles[0])
                        except:
                            pass
            
            except Exception as second_sequence_error:
                log_step("second_sequence_error", False, str(second_sequence_error))
                # Clean up any open tabs
                try:
                    self.persistent_bookmark_driver.close()
                    if len(self.persistent_bookmark_driver.window_handles) > 0:
                        self.persistent_bookmark_driver.switch_to.window(self.persistent_bookmark_driver.window_handles[0])
                except:
                    pass
            
            # Mark overall success
            step_log['success'] = True
            log_step("bookmark_function_success", True)
            log_final_result()
            return True
            
        except Exception as main_error:
            log_step("main_function_error", False, str(main_error))
            log_final_result()
            return False

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
        chrome_opts.add_argument("--log-level=1")  # More detailed logging
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
                        
                        # Execute the purchase process
                        self.process_single_listing_with_driver(TEST_BOOKMARK_BUYING_URL, driver_num, driver)
                        
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
            
            # Skip all driver initialization, pygame, flask, etc.
            # Just run the bookmark function directly
            success = self.bookmark_driver(BOOKMARK_TEST_URL, BOOKMARK_TEST_USERNAME)
            
            if success:
                print("✅ BOOKMARK TEST SUCCESSFUL")
            else:
                print("❌ BOOKMARK TEST FAILED")
            
            # Exit immediately after test
            print("🧪 BOOKMARK TEST MODE COMPLETE - EXITING")
            sys.exit(0)
        
        # NEW: BUYING_TEST_MODE implementation
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
        pygame_thread = threading.Thread(target=self.run_pygame_window)
        pygame_thread.start()
        
        # Clear download folder and start scraping
        self.clear_download_folder()
        driver = self.setup_driver()
        self.setup_persistent_buying_driver()
        try:
            self.search_vinted_with_refresh(driver, SEARCH_QUERY)
        finally:
            driver.quit()
            pygame.quit()
            self.cleanup_persistent_buying_driver()
            self.cleanup_all_buying_drivers()  # NEW: Clean up buying drivers
            sys.exit(0)

if __name__ == "__main__":
    if programme_to_run == 0:
        scraper = FacebookScraper()
        # Store globally for Flask route access
        globals()['scraper_instance'] = scraper
    else:
        scraper = VintedScraper()
        # Store globally for Flask route access - CRITICAL for button functionality
        globals()['vinted_scraper_instance'] = scraper
        
        # Replace the normal search with enhanced version in the run method
        # Modify the run() method to use search_vinted_enhanced instead of search_vinted
    
    scraper.run()