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

BOOKMARK_TEST_MODE = False
BOOKMARK_TEST_URL = "https://www.vinted.co.uk/items/6966914082-scarf?referrer=catalog"
BOOKMARK_TEST_USERNAME = "leah_lane" 

BUYING_TEST_MODE = False
BUYING_TEST_URL = "https://www.vinted.co.uk/items/6966124363-mens-t-shirt-bundle-x-3-ml?homepage_session_id=932d30be-02f5-4f54-9616-c412dd6e9da2"

TEST_BOOKMARK_BUYING_FUNCTIONALITY = True
TEST_BOOKMARK_BUYING_URL = "https://www.vinted.co.uk/items/6961760221-joy-con-controllers-for-nintendo-switch-brand-new?referrer=catalog"

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
                               'read description', 'joy pads', 'spares and repairs', 'neon', 'spares or repairs', 'dock cover', '3d print']

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
        return 65 <= profit_percentage <= 400
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
