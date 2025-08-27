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

test_bookmark_function = False
bookmark_listings = False
click_pay_button_final_check = False
test_bookmark_link = "https://www.vinted.co.uk/items/6900159208-laptop-case"
bookmark_stopwatch_length = 500
buying_driver_click_pay_wait_time = 5
#sold listing: https://www.vinted.co.uk/items/6900159208-laptop-case

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
SD_card_price = 5

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
REFRESH_AND_RESCAN = False  # Set to False to disable refresh functionality
MAX_LISTINGS_VINTED_TO_SCAN = 6  # Maximum listings to scan before refresh
wait_after_max_reached_vinted = 10  # Seconds to wait between refresh cycles (5 minutes)
VINTED_SCANNED_IDS_FILE = "vinted_scanned_ids.txt"
FAILURE_REASON_LISTED = True
REPEAT_LISTINGS = True
WAIT_TIME_AFTER_REFRESH = 125
LOCK_POSITION = True
SHOW_ALL_LISTINGS = True
VINTED_SHOW_ALL_LISTINGS = True
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

vinted_title_forbidden_words = ['unofficial', 'keyboard', 'mouse', 'ps4', 'ps5', 'sold', 'organizer', 'holder', 'joy con', 'gift', 'read des'
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

        # Return the complete HTML with modified JavaScript for Vinted
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
                
                /* NEW: Buy decision buttons */
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
            </style>
            <script>
                const allListings = {all_listings_json};
                let currentListingIndex = 0;
                console.log('All listings loaded:', allListings);
                console.log('Number of listings:', allListings.length);

                function refreshPage() {{
                    location.reload();
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
                    const counterEl = document.getElementById('listing-counter');

                    if (titleEl) titleEl.textContent = listing.title;
                    if (priceEl) priceEl.textContent = 'Price: £' + listing.price;
                    if (profitEl) profitEl.textContent = `Profit: £${{listing.profit.toFixed(2)}}`;
                    if (joinDateEl) joinDateEl.textContent = listing.join_date;
                    if (detectedItemsEl) detectedItemsEl.textContent = listing.detected_items;
                    if (descriptionEl) descriptionEl.textContent = listing.description;
                    if (urlEl) urlEl.textContent = listing.url;
                    if (counterEl) counterEl.textContent = `Listing ${{currentListingIndex + 1}} of ${{allListings.length}}`;

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

                // NEW: Buy decision functions
                function buyYes() {{
                    var urlElement = document.querySelector('.content-url');
                    var url = urlElement ? urlElement.textContent.trim() : '';
                    
                    if (url && url !== 'No URL Available') {{
                        console.log('User wishes to buy listing: ' + url);
                        
                        // Send POST request to Flask backend (similar to Facebook buttons)
                        fetch('/vinted-button-clicked', {{
                            method: 'POST',
                            headers: {{
                                'Content-Type': 'application/x-www-form-urlencoded',
                            }},
                            body: `url=${{encodeURIComponent(url)}}&action=buy_yes`
                        }})
                        .then(response => {{
                            if (response.ok) {{
                                console.log('Vinted YES button clicked successfully');
                            }} else {{
                                console.error('Failed to process Vinted YES button');
                            }}
                        }})
                        .catch(error => {{
                            console.error('Error with Vinted YES button:', error);
                        }});
                    }}else {{
                        console.log('User wishes to buy listing but no URL available');
                    }}
                }}

                function buyNo() {{
                    var urlElement = document.querySelector('.content-url');
                    var url = urlElement ? urlElement.textContent.trim() : '';
                    
                    if (url && url !== 'No URL Available') {{
                        console.log('User does not wish to buy listing: ' + url);
                        
                        // Send POST request to Flask backend (similar to Facebook buttons)
                        fetch('/vinted-button-clicked', {{
                            method: 'POST',
                            headers: {{
                                'Content-Type': 'application/x-www-form-urlencoded',
                            }},
                            body: `url=${{encodeURIComponent(url)}}&action=buy_no`
                        }})
                        .then(response => {{
                            if (response.ok) {{
                                console.log('Vinted NO button clicked successfully');
                            }} else {{
                                console.error('Failed to process Vinted NO button');
                            }}
                        }})
                        .catch(error => {{
                            console.error('Error with Vinted NO button:', error);
                        }});
                    }} else {{
                        console.log('User does not wish to buy listing but no URL available');
                    }}
                }}

                // Initialize display on page load
                window.onload = () => {{
                    console.log('Page loaded, initializing display');
                    if (allListings.length > 0) {{
                        updateListingDisplay(0);
                    }} else {{
                        console.log('No listings to display');
                    }}
                }};
            </script>
        </head>
        <body>
            <div class="container listing-container">
                <div class="button-row">
                    <button class="custom-button" onclick="refreshPage()" style="background-color:rgb(108,178,209);">Refresh Page</button>
                </div>
                <div class="listing-counter" id="listing-counter">
                    Listing 1 of 1
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
                
                <!-- NEW: Buy decision buttons -->
                <div class="buy-decision-container">
                    <button class="buy-yes-button" onclick="buyYes()">
                        Yes - Buy now
                    </button>
                    <button class="buy-no-button" onclick="buyNo()">
                        No - Do not purchase
                    </button>
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
        self.clicked_yes_listings = set()  # Track listings that have been clicked "yes"
        self.bookmark_timers = {}
        self.buying_drivers = {}  # Dictionary to store drivers {1: driver_object, 2: driver_object, etc.}
        self.driver_status = {}   # Track driver status {1: 'free'/'busy', 2: 'free'/'busy', etc.}
        self.driver_lock = threading.Lock()  # Thread safety for driver management
        
        # Initialize all driver slots as not created
        for i in range(1, 6):  # Drivers 1-5
            self.buying_drivers[i] = None
            self.driver_status[i] = 'free'
    def get_available_driver(self):
        """
        Find and reserve the first available driver.
        Returns: (driver_number, driver_instance) or (None, None) if all busy
        """
        with self.driver_lock:
            for driver_num in range(1, 6):  # Check drivers 1-5
                if self.driver_status[driver_num] == 'free':
                    # Reserve this driver
                    self.driver_status[driver_num] = 'busy'
                    
                    # Create driver if it doesn't exist
                    if self.buying_drivers[driver_num] is None:
                        print(f"🚗 CREATING: Buying driver {driver_num}")
                        self.buying_drivers[driver_num] = self.setup_buying_driver(driver_num)
                        if self.buying_drivers[driver_num] is None:
                            print(f"❌ FAILED: Could not create buying driver {driver_num}")
                            self.driver_status[driver_num] = 'free'  # Free it back up
                            continue
                    
                    print(f"✅ RESERVED: Buying driver {driver_num}")
                    return driver_num, self.buying_drivers[driver_num]
            
            print("❌ ERROR: All 5 buying drivers are currently busy")
            return None, None

    def release_driver(self, driver_num):
        """
        Release a driver back to the free pool and handle cleanup
        """
        with self.driver_lock:
            print(f"🔓 RELEASING: Buying driver {driver_num}")
            
            # Close driver if it's not driver 1 (driver 1 stays open permanently)
            if driver_num != 1 and self.buying_drivers[driver_num] is not None:
                try:
                    print(f"🗑️ CLOSING: Buying driver {driver_num}")
                    self.buying_drivers[driver_num].quit()
                    self.buying_drivers[driver_num] = None
                except Exception as e:
                    print(f"⚠️ WARNING: Error closing driver {driver_num}: {e}")
                    self.buying_drivers[driver_num] = None
            
            # Mark as free
            self.driver_status[driver_num] = 'free'
            print(f"✅ FREED: Buying driver {driver_num}")
    def start_bookmark_stopwatch(self, listing_url):
        """
        Start a stopwatch for a successfully bookmarked listing
        """
        print(f"⏱️ STOPWATCH: Starting timer for {listing_url}")
        
        def stopwatch_timer():
            time.sleep(bookmark_stopwatch_length)
            print(f'LISTING {listing_url} HAS BEEN BOOKMARKED FOR {bookmark_stopwatch_length} SECONDS!')
            
            # Clean up the timer reference
            if listing_url in self.bookmark_timers:
                del self.bookmark_timers[listing_url]
        
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
            'reviews': pygame.font.Font(None, 28)  # New font for seller reviews
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
                elif i == 8:  # Rectangle 9 (index 8) - Upload Date
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
                elif i == 6:  # Rectangle 7 (index 6) - NEW: Seller Reviews
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

        # Explicitly set the global variables
        current_detected_items = formatted_detected_items
        current_listing_title = title[:50] + '...' if len(title) > 50 else title
        current_listing_description = description[:200] + '...' if len(description) > 200 else description if description else "No description"
        current_listing_join_date = join_date if join_date else "Unknown upload date"
        current_listing_price = f"Price:\n£{float(price):.2f}" if price else "Price:\n£0.00"
        current_expected_revenue = f"Rev:\n£{expected_revenue:.2f}" if expected_revenue else "Rev:\n£0.00"
        current_profit = f"Profit:\n£{profit:.2f}" if profit else "Profit:\n£0.00"
        current_listing_url = url
        current_suitability = suitability if suitability else "Suitability unknown"
        current_seller_reviews = seller_reviews if seller_reviews else "No reviews yet"

    def process_single_listing_with_driver(self, url, driver_num, driver):
        """
        Process a single listing using the specified driver
        """
        start_time = time.time()
        
        try:
            print(f"🔥 DRIVER {driver_num}: Processing {url}")
            
            # Verify driver is still alive
            driver.current_url
            
            # Open new tab for processing
            print(f"📑 DRIVER {driver_num}: Opening new tab")
            driver.execute_script("window.open('');")
            new_tab = driver.window_handles[-1]
            driver.switch_to.window(new_tab)
            
            # Navigate to listing URL
            print(f"🔗 DRIVER {driver_num}: Navigating to listing")
            driver.get(url)
            
            # Wait for page to load
            time.sleep(2)
            
            # Look for Buy now button
            print(f"🔘 DRIVER {driver_num}: Looking for Buy now button")
            
            buy_selectors = [
                'button[data-testid="item-buy-button"]',
                'button.web_ui__Button__button.web_ui__Button__filled.web_ui__Button__default.web_ui__Button__primary.web_ui__Button__truncated',
                'button.web_ui__Button__button[data-testid="item-buy-button"]',
                '//button[@data-testid="item-buy-button"]',
                '//button[contains(@class, "web_ui__Button__primary")]//span[text()="Buy now"]',
            ]
            
            buy_button = None
            for selector in buy_selectors:
                try:
                    if selector.startswith('//'):
                        buy_button = WebDriverWait(driver, 2).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        buy_button = WebDriverWait(driver, 2).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    print(f"✅ DRIVER {driver_num}: Found Buy now button")
                    break
                except TimeoutException:
                    continue
            
            if buy_button:
                # Click the Buy now button
                try:
                    buy_button.click()
                    print(f"✅ DRIVER {driver_num}: Clicked Buy now button")
                except Exception as e:
                    try:
                        driver.execute_script("arguments[0].click();", buy_button)
                        print(f"✅ DRIVER {driver_num}: Clicked Buy now button (JS)")
                    except Exception as e2:
                        print(f"❌ DRIVER {driver_num}: Failed to click Buy now button")
                        raise e2
                
                # Wait for shipping page and start alternating clicks
                print(f"🚚 DRIVER {driver_num}: Waiting for shipping page")
                try:
                    pickup_point_header = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//h2[@class="web_ui__Text__text web_ui__Text__title web_ui__Text__left" and text()="Ship to pick-up point"]'))
                    )
                    print(f"✅ DRIVER {driver_num}: Shipping page loaded")
                    
                    # Record start time for alternating clicks
                    first_click_time = time.time()
                    
                    print(f"🔄 DRIVER {driver_num}: Starting {bookmark_stopwatch_length}s alternating click sequence")
                    
                    while True:
                        # Check if time elapsed
                        if time.time() - first_click_time >= bookmark_stopwatch_length:
                            print(f"⏰ DRIVER {driver_num}: {bookmark_stopwatch_length} seconds elapsed, stopping")
                            break
                        
                        # Click "Ship to pick-up point"
                        try:
                            pickup_point = driver.find_element(
                                By.XPATH, 
                                '//h2[@class="web_ui__Text__text web_ui__Text__title web_ui__Text__left" and text()="Ship to pick-up point"]'
                            )
                            pickup_point.click()
                            print(f"📦 DRIVER {driver_num}: Clicked 'Ship to pick-up point'")
                        except Exception as e:
                            print(f"⚠️ DRIVER {driver_num}: Could not click 'Ship to pick-up point': {e}")
                        
                        # Wait
                        time.sleep(buying_driver_click_pay_wait_time)
                        
                        # Check time again
                        if time.time() - first_click_time >= bookmark_stopwatch_length:
                            print(f"⏰ DRIVER {driver_num}: Time elapsed during wait, stopping")
                            break
                        
                        # Click "Ship to home"
                        try:
                            ship_to_home = driver.find_element(
                                By.XPATH, 
                                '//h2[@class="web_ui__Text__text web_ui__Text__title web_ui__Text__left" and text()="Ship to home"]'
                            )
                            ship_to_home.click()
                            print(f"🏠 DRIVER {driver_num}: Clicked 'Ship to home'")
                        except Exception as e:
                            print(f"⚠️ DRIVER {driver_num}: Could not click 'Ship to home': {e}")
                        
                        # Wait
                        time.sleep(buying_driver_click_pay_wait_time)
                
                except TimeoutException:
                    print(f"⚠️ DRIVER {driver_num}: Timeout waiting for shipping page")
                
            else:
                print(f"❌ DRIVER {driver_num}: Buy now button not found")
            
            # Close the processing tab (keep main tab open)
            print(f"🗑️ DRIVER {driver_num}: Closing processing tab")
            driver.close()
            
            # Switch back to main tab (vinted.co.uk)
            if len(driver.window_handles) > 0:
                driver.switch_to.window(driver.window_handles[0])
                print(f"🏠 DRIVER {driver_num}: Back to main tab")
            
            elapsed = time.time() - start_time
            print(f"✅ DRIVER {driver_num}: Completed processing in {elapsed:.2f} seconds")
            
        except Exception as e:
            print(f"❌ DRIVER {driver_num}: Error processing {url}: {e}")
            
            # Try to recover by switching back to main tab
            try:
                if len(driver.window_handles) > 0:
                    driver.switch_to.window(driver.window_handles[0])
            except:
                print(f"⚠️ DRIVER {driver_num}: Could not recover to main tab")
        
        finally:
            # Always release the driver when done
            self.release_driver(driver_num)

    def cleanup_all_buying_drivers(self):
        """
        Clean up all buying drivers when program exits
        """
        print("🧹 CLEANUP: Closing all buying drivers")
        
        with self.driver_lock:
            for driver_num in range(1, 6):
                if self.buying_drivers[driver_num] is not None:
                    try:
                        self.buying_drivers[driver_num].quit()
                        print(f"🗑️ CLEANUP: Closed buying driver {driver_num}")
                    except:
                        pass
                    finally:
                        self.buying_drivers[driver_num] = None
                        self.driver_status[driver_num] = 'free'
        
        print("✅ CLEANUP: All buying drivers closed")

    def vinted_button_clicked_enhanced(self, url):
        """
        UPDATED: Enhanced button click handler using multiple drivers
        """
        print(f"🔘 VINTED BUTTON: Processing {url}")
        
        # Check if already clicked to prevent duplicates
        if url in self.clicked_yes_listings:
            print(f"🔄 VINTED BUTTON: Listing {url} already processed, ignoring")
            return
        
        # Mark as clicked
        self.clicked_yes_listings.add(url)
        
        # Get an available driver
        driver_num, driver = self.get_available_driver()
        
        if driver is None:
            print("❌ ERROR: All 5 buying drivers are currently busy. Please wait and try again.")
            # Remove from clicked list so they can try again later
            self.clicked_yes_listings.discard(url)
            return
        
        # Process the listing in a separate thread so it doesn't block
        processing_thread = threading.Thread(
            target=self.process_single_listing_with_driver,
            args=(url, driver_num, driver)
        )
        processing_thread.daemon = True
        processing_thread.start()

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
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
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
            fallback_opts.add_argument("--headless")
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
        Setup a specific buying driver with its own user data directory
        """
        try:
            print(f"🚗 SETUP: Creating buying driver {driver_num}")
            
            service = Service(
                ChromeDriverManager().install(),
                log_path=os.devnull
            )
            
            chrome_opts = Options()
            # Each driver gets its own directory
            user_data_dir = f"C:\\VintedBuyer{driver_num}"
            chrome_opts.add_argument(f"--user-data-dir={user_data_dir}")
            chrome_opts.add_argument("--profile-directory=Default")
            
            # Standard options
            chrome_opts.add_argument("--no-sandbox")
            chrome_opts.add_argument("--disable-dev-shm-usage")
            chrome_opts.add_argument("--disable-gpu")
            chrome_opts.add_argument("--window-size=800,600")
            chrome_opts.add_argument("--log-level=3")
            chrome_opts.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
            
            # Create the driver
            driver = webdriver.Chrome(service=service, options=chrome_opts)
            
            # Set timeouts for quick processing
            driver.implicitly_wait(1)
            driver.set_page_load_timeout(10)
            driver.set_script_timeout(5)
            
            # Navigate to vinted.co.uk instead of blank page
            print(f"🏠 NAVIGATE: Driver {driver_num} going to vinted.co.uk")
            driver.get("https://www.vinted.co.uk")
            
            print(f"✅ SUCCESS: Buying driver {driver_num} created and ready")
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
        
        # Debug print to see final extracted count
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
        UPDATED: Now includes username collection
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
                                    print(f"DEBUG: Found reviews using selector '{review_sel}': '{text}'")
                                    break
                            if reviews_text:
                                break
                        except Exception as e:
                            print(f"DEBUG: Selector '{review_sel}' failed: {e}")
                            continue
                    
                    # Process the found reviews text
                    if reviews_text:
                        if reviews_text == "No reviews yet" or "no review" in reviews_text.lower():
                            data[key] = "No reviews yet"
                        elif reviews_text.isdigit():
                            # Just a number like "123"
                            data[key] = reviews_text  # Keep as string for consistency
                            print(f"DEBUG: Set seller_reviews to: '{reviews_text}'")
                        else:
                            # Try to extract number from text like "123 reviews" or "(123)"
                            match = re.search(r'(\d+)', reviews_text)
                            if match:
                                data[key] = match.group(1)  # Just the number as string
                                print(f"DEBUG: Extracted number from '{reviews_text}': '{match.group(1)}'")
                            else:
                                data[key] = "No reviews yet"
                    else:
                        data[key] = "No reviews yet"
                        print("DEBUG: No seller reviews found with any selector")
                        
                elif key == "username":
                    # NEW: Handle username extraction with careful error handling
                    try:
                        username_element = driver.find_element(By.CSS_SELECTOR, sel)
                        username_text = username_element.text.strip()
                        if username_text:
                            data[key] = username_text
                            print(f"DEBUG: Found username: '{username_text}'")
                        else:
                            data[key] = "Username not found"
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
                            print("DEBUG: Username not found with any selector")
                            
                else:
                    # Handle all other fields normally
                    data[key] = driver.find_element(By.CSS_SELECTOR, sel).text
                    
            except NoSuchElementException:
                if key == "seller_reviews":
                    data[key] = "No reviews yet"
                    print("DEBUG: NoSuchElementException - set seller_reviews to 'No reviews yet'")
                elif key == "username":
                    data[key] = "Username not found"
                    print("DEBUG: NoSuchElementException - set username to 'Username not found'")
                else:
                    data[key] = None

        # Keep title formatting for pygame display
        if data["title"]:
            data["title"] = data["title"][:50] + '...' if len(data["title"]) > 50 else data["title"]

        # DEBUG: Print final scraped data for seller_reviews and username
        print(f"DEBUG: Final scraped seller_reviews: '{data.get('seller_reviews')}'")
        print(f"DEBUG: Final scraped username: '{data.get('username')}'")
        
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
        MODIFIED: Only adds to pygame/website and sends notifications on successful bookmark when bookmark_listings=True and VINTED_SHOW_ALL_LISTINGS=False
        """
        global suitable_listings, current_listing_index, recent_listings

        # Extract username from details - THIS WAS MISSING!
        username = details.get("username", None)
        if username and username != "Username not found":
            print(f"🔖 USERNAME EXTRACTED: {username}")
        else:
            username = None
            print("🔖 USERNAME: Not available for this listing")

        # Extract and validate price from the main price field
        price_text = details.get("price", "0")
        listing_price = self.extract_vinted_price(price_text)
        postage = self.extract_price(details.get("postage", "0"))
        total_price = listing_price + postage

        # Get seller reviews
        seller_reviews = details.get("seller_reviews", "No reviews yet")
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

        # Create final listing info
        final_listing_info = {
            'title': details.get("title", "No title"),
            'description': details.get("description", "No description"),
            'join_date': details.get("uploaded", "Unknown upload date"),
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

        # MODIFIED: Add to suitable listings based on new logic
        should_add_listing = False
        should_send_notification = False
        # this here stops all of the non bookmarked listings from being added
        if bookmark_listings and not VINTED_SHOW_ALL_LISTINGS:
            # When bookmark_listings is ON and VINTED_SHOW_ALL_LISTINGS is OFF:
            # Only add/notify if bookmark was successful
            if bookmark_success:
                should_add_listing = True
                should_send_notification = True
                print("✅ Adding listing because bookmark was successful")
            else:
                print("❌ Not adding listing because bookmark was not successful")
        else:
            # Original logic for other combinations
            if is_suitable or VINTED_SHOW_ALL_LISTINGS:
                should_add_listing = True
                should_send_notification = True
        
        if should_add_listing:
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

            suitable_listings.append(final_listing_info)

            # Add to recent_listings for website navigation
            recent_listings['listings'].append(final_listing_info)
            # Always set to the last (most recent) listing for website display
            recent_listings['current_index'] = len(recent_listings['listings']) - 1

            current_listing_index = len(suitable_listings) - 1
            self.update_listing_details(**final_listing_info)

            if is_suitable:
                print(f"✅ Added suitable listing: £{total_price:.2f} -> £{expected_profit:.2f} profit ({profit_percentage:.2f}%)")
            else:
                print(f"➕ Added unsuitable listing (SHOW_ALL mode or successful bookmark): £{total_price:.2f}")
        else:
            print(f"❌ Listing not added: {suitability_reason}")


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
        if self.detect_sd_card_vinted(title, description):
            total_revenue += 5 # Same SD card revenue as Facebook
            print(f"SD Card detected: Added £5 to revenue")

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

        print(f"\nVinted Revenue Breakdown:")
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
        
        return final_detected_objects, processed_images


    def download_images_for_listing(self, driver, listing_dir):
        # Wait for the page to fully load
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "img"))
            )
            # Additional wait for dynamic content
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
                print(f"  ▶ Found {len(imgs)} images using selector: {selector}")
                break
        
        if not imgs:
            print("  ▶ No images found with any selector")
            return []
        
        # Filter images more strictly to avoid profile pictures and small icons
        valid_imgs = []
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
                    valid_imgs.append(img)
        
        if not valid_imgs:
            print(f"  ▶ No valid product images found after filtering from {len(imgs)} total images")
            # Debug: print what we found for troubleshooting
            for i, img in enumerate(imgs[:5]):  # Show first 5 for debugging
                src = img.get_attribute("src")
                alt = img.get_attribute("alt")
                try:
                    parent = img.find_element(By.XPATH, "..")
                    parent_classes = parent.get_attribute("class") or ""
                except:
                    parent_classes = "unknown"
                print(f"    Image {i+1}: src='{src[:80]}...', alt='{alt}', parent_classes='{parent_classes}'")
            return []

        os.makedirs(listing_dir, exist_ok=True)
        downloaded_paths = []
        seen_urls = set()
        image_index = 1

        print(f"  ▶ Attempting to download {len(valid_imgs)} product images")
        
        for img_el in valid_imgs[:10]:  # Limit to first 10 images
            src = img_el.get_attribute("src")
            if not src or src in seen_urls:
                continue

            seen_urls.add(src)

            try:
                # Add headers to mimic browser request
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Referer': driver.current_url
                }
                
                resp = requests.get(src, timeout=15, headers=headers)
                resp.raise_for_status()
                
                # Verify it's actually an image
                img = Image.open(BytesIO(resp.content))
                
                # Skip very small images (likely icons or profile pics that got through)
                if img.width < 200 or img.height < 200:
                    print(f"    ⏭️  Skipping small image: {img.width}x{img.height}")
                    continue
                
                save_path = os.path.join(listing_dir, f"{image_index}.png")
                img.save(save_path, format="PNG")
                downloaded_paths.append(save_path)
                image_index += 1
                print(f"    ✅ Downloaded product image {image_index-1}: {img.width}x{img.height}")

            except Exception as e:
                print(f"    ❌ Failed to download image from {src[:50]}...: {str(e)}")
                continue

        print(f"  ▶ Successfully downloaded {len(downloaded_paths)} product images")
        return downloaded_paths

    
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
        UPDATED: Now prints username alongside other listing details
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
        model = None
        if not os.path.exists(MODEL_WEIGHTS):
            print(f"❌ Critical Error: Model weights not found at '{MODEL_WEIGHTS}'. Detection will be skipped.")
        else:
            try:
                model = YOLO(MODEL_WEIGHTS)
                print("✅ Model loaded successfully.")
            except Exception as e:
                print(f"❌ Critical Error: Could not load YOLO model. Detection will be skipped. Reason: {e}")

        # Initial page setup
        params = {
            "search_text": search_query,
            "price_from": PRICE_FROM,
            "price_to": PRICE_TO,
            "currency": CURRENCY,
            "order": ORDER,
        }
        driver.get(f"{BASE_URL}?{urlencode(params)}")
        main = driver.current_window_handle

        # Load previously scanned listing IDs (this will now be empty since we cleared the file)
        scanned_ids = self.load_scanned_vinted_ids()
        print(f"📚 Loaded {len(scanned_ids)} previously scanned listing IDs")

        page = 1
        overall_listing_counter = 0  # Total listings processed across all cycles
        refresh_cycle = 1
        is_first_refresh = True

        # Main scanning loop with refresh functionality
        while True:
            print(f"\n{'='*60}")
            print(f"🔍 STARTING REFRESH CYCLE {refresh_cycle}")
            print(f"{'='*60}")
            
            cycle_listing_counter = 0  # Listings processed in this cycle
            found_already_scanned = False
            
            # Reset to first page for each cycle
            page = 1
            
            while True:  # Page loop
                try:
                    WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.feed-grid"))
                    )
                except TimeoutException:
                    print("⚠️ Timeout waiting for page to load - moving to next cycle")
                    break

                # Get listing URLs from current page
                els = driver.find_elements(By.CSS_SELECTOR, "a.new-item-box__overlay")
                urls = [e.get_attribute("href") for e in els if e.get_attribute("href")]
                
                if not urls:
                    print(f"📄 No listings found on page {page} - moving to next cycle")
                    break

                print(f"📄 Processing page {page} with {len(urls)} listings")

                for idx, url in enumerate(urls, start=1):
                    overall_listing_counter += 1
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

                    # Process the listing (same as original logic)
                    driver.execute_script("window.open();")
                    driver.switch_to.window(driver.window_handles[-1])
                    driver.get(url)

                    try:
                        details = self.scrape_item_details(driver)
                        second_price = self.extract_price(details["second_price"])
                        postage = self.extract_price(details["postage"])
                        total_price = second_price + postage

                        print(f"  Link:         {url}")
                        print(f"  Title:        {details['title']}")
                        print(f"  Username:     {details.get('username', 'Username not found')}")  # NEW: Print username
                        print(f"  Price:        {details['price']}")
                        print(f"  Second price: {details['second_price']} ({second_price:.2f})")
                        print(f"  Postage:      {details['postage']} ({postage:.2f})")
                        print(f"  Total price:  £{total_price:.2f}")
                        print(f"  Uploaded:     {details['uploaded']}")

                        # Download images for the current listing
                        listing_dir = os.path.join(DOWNLOAD_ROOT, f"listing {overall_listing_counter}")
                        image_paths = self.download_images_for_listing(driver, listing_dir)

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
                        
                    except Exception as e:
                        print(f"  ❌ ERROR scraping listing: {e}")
                        # Still mark as scanned even if there was an error
                        if listing_id:
                            scanned_ids.add(listing_id)
                            self.save_vinted_listing_id(listing_id)

                    finally:
                        driver.close()
                        driver.switch_to.window(main)

                # Check if we need to break out of page loop
                if found_already_scanned or (REFRESH_AND_RESCAN and cycle_listing_counter > MAX_LISTINGS_VINTED_TO_SCAN):
                    break

                # Try to go to next page
                try:
                    nxt = driver.find_element(By.CSS_SELECTOR, "a[data-testid='pagination-arrow-right']")
                    driver.execute_script("arguments[0].click();", nxt)
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
                self.refresh_vinted_page_and_wait(driver, is_first_refresh)
            elif cycle_listing_counter > MAX_LISTINGS_VINTED_TO_SCAN:
                print(f"📊 Reached maximum listings ({MAX_LISTINGS_VINTED_TO_SCAN}) - refreshing")
                self.refresh_vinted_page_and_wait(driver, is_first_refresh)
            else:
                print("📄 No more pages and no max reached - refreshing for new listings")
                self.refresh_vinted_page_and_wait(driver, is_first_refresh)

            refresh_cycle += 1
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

    def bookmark_driver(self, listing_url, username=None):  # ADD username parameter
            print('entering bookmark_driver')
            """
            ULTRA-FAST bookmark driver - uses single persistent driver with tabs
            MODIFIED: Now looks for username and bookmarks/buys accordingly
            FIXED: Now accepts username as parameter from process_vinted_listing
            """
            # TEST MODE: If test_bookmark_function is True, use test_bookmark_link instead
            if test_bookmark_function:
                actual_url = test_bookmark_link
                print(f"🔖 TEST MODE: Using test URL instead of actual listing URL")
                print(f"🔖 TEST URL: {actual_url}")
            else:
                print('else')
                actual_url = listing_url
                print(f"🔖 NORMAL MODE: Using actual listing URL")
            
            # USERNAME IS NOW PASSED AS PARAMETER - NO NEED TO EXTRACT FROM DRIVER
            if not username:
                print("⚠️ Could not extract username, possible unable to detect false buy, exiting.")
                sys.exit(0)
            
            print(f"🔖 Looking at listing {actual_url} posted by {username if username else 'unknown user'}")
            
            try:
                print(f"🔖 STARTING BOOKMARK: {actual_url}")
                
                # Initialize persistent driver if it doesn't exist
                # In your bookmark_driver function, replace the driver initialization section with this:

                # Initialize persistent driver if it doesn't exist
                if not hasattr(self, 'persistent_bookmark_driver') or self.persistent_bookmark_driver is None:
                    print("🔖 INITIALIZING: Creating persistent bookmark driver...")
                    
                    # SPEED OPTIMIZATION 1: Pre-cached service
                    if not hasattr(self, '_cached_chromedriver_path'):
                        self._cached_chromedriver_path = ChromeDriverManager().install()
                    
                    # SPEED OPTIMIZATION 2: Minimal Chrome options
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
                    print("🔖 SERVICE: Using cached ChromeDriver")
                    
                    print("🔖 DRIVER: Creating persistent driver...")
                    self.persistent_bookmark_driver = webdriver.Chrome(service=service, options=chrome_opts)
                    print("🔖 DRIVER: Persistent driver created!")
                    
                    # BALANCED timeouts - fast but not too aggressive
                    self.persistent_bookmark_driver.implicitly_wait(1)
                    self.persistent_bookmark_driver.set_page_load_timeout(8)
                    self.persistent_bookmark_driver.set_script_timeout(3)
                    
                    # NEW: Navigate to Vinted homepage on the main tab
                    try:
                        print("🔖 HOMEPAGE: Navigating to vinted.co.uk...")
                        self.persistent_bookmark_driver.get("https://www.vinted.co.uk")
                        print("🔖 HOMEPAGE: Successfully loaded vinted.co.uk")
                    except Exception as homepage_error:
                        print(f"🔖 HOMEPAGE: Failed to load vinted.co.uk - {homepage_error}")
                        # Don't fail the whole process if homepage load fails
                        pass
                try:
                    self.persistent_bookmark_driver.current_url  # Test if driver is alive
                    print("🔖 DRIVER: Using existing persistent driver")
                except:
                    print("🔖 DRIVER: Existing driver is dead, creating new one...")
                    # Driver is dead, create a new one
                    self.persistent_bookmark_driver = None
                    return self.bookmark_driver(listing_url, username)  # Recursive call to recreate with username
                
                # Open new tab for this listing
                print("🔖 TAB: Opening new tab...")
                self.persistent_bookmark_driver.execute_script("window.open('');")
                
                # Switch to the new tab
                new_tab = self.persistent_bookmark_driver.window_handles[-1]
                self.persistent_bookmark_driver.switch_to.window(new_tab)
                print(f"🔖 TAB: Switched to new tab (total tabs: {len(self.persistent_bookmark_driver.window_handles)})")
                
                # Navigate to the listing URL
                print(f"🔖 NAVIGATING...")
                try:
                    self.persistent_bookmark_driver.get(actual_url)
                    print("🔖 NAVIGATION: Complete")
                    
                    # NEW: FIRST BUY NOW + PAY SEQUENCE (before messages)
                    print("🔖 FIRST SEQUENCE: Looking for Buy now button...")
                    
                    buy_selectors = [
                        "button[data-testid='item-buy-button']",
                        "button.web_ui__Button__primary[data-testid='item-buy-button']",
                        "button:contains('Buy now')",
                        ".web_ui__Button__primary .web_ui__Button__label:contains('Buy now')",
                    ]
                    
                    first_buy_clicked = False
                    for selector in buy_selectors:
                        try:
                            buy_button = WebDriverWait(self.persistent_bookmark_driver, 0.5).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                            )
                            
                            print(f"🔖 FIRST SEQUENCE: Buy button found, clicking...")
                            buy_button.click()
                            first_buy_clicked = True
                            break
                            
                        except:
                            continue
                    
                    if first_buy_clicked:
                        print("🔖 FIRST SEQUENCE: Buy button clicked, looking for Pay button...")
                        
                        try:
                            # Look for pay button
                            pay_button = WebDriverWait(self.persistent_bookmark_driver, 10).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, 
                                    'button[data-testid="single-checkout-order-summary-purchase-button"]'
                                ))
                            )
                            
                            print("🔖 FIRST SEQUENCE: Pay button found, clicking...")
                            pay_button.click()
                            
                            print("🔖 FIRST SEQUENCE: Waiting 0.25 seconds...")
                            time.sleep(0.25)
                            
                            print("🔖 FIRST SEQUENCE: Closing tab...")
                            self.persistent_bookmark_driver.close()
                            
                            # Switch back to main tab
                            if len(self.persistent_bookmark_driver.window_handles) > 0:
                                self.persistent_bookmark_driver.switch_to.window(self.persistent_bookmark_driver.window_handles[0])
                            
                            print("🔖 FIRST SEQUENCE: Complete. Opening new tab for second sequence...")
                            
                        except:
                            print("🔖 FIRST SEQUENCE: Pay button not found, closing tab...")
                            self.persistent_bookmark_driver.close()
                            if len(self.persistent_bookmark_driver.window_handles) > 0:
                                self.persistent_bookmark_driver.switch_to.window(self.persistent_bookmark_driver.window_handles[0])
                        # Navigate to listing URL again (second time)
                        print("🔖 SECOND SEQUENCE: Opening new tab and navigating to listing...")
                        self.persistent_bookmark_driver.execute_script("window.open('');")
                        second_tab = self.persistent_bookmark_driver.window_handles[-1]
                        self.persistent_bookmark_driver.switch_to.window(second_tab)
                        
                        self.persistent_bookmark_driver.get(actual_url)
                        print("🔖 SECOND SEQUENCE: Navigation complete")
                        
                        # Look for buy button AGAIN
                        print("🔖 SECOND SEQUENCE: Looking for Buy now button...")
                        
                        second_buy_button_found = False
                        for selector in buy_selectors:
                            try:
                                buy_button = WebDriverWait(self.persistent_bookmark_driver, 0.5).until(
                                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                                )
                                
                                print(f"🔖 SECOND SEQUENCE: Buy button found with selector: {selector}")
                                buy_button.click()
                                second_buy_button_found = True
                                break
                                
                            except:
                                continue
                        
                        if second_buy_button_found:
                            print("🔖 SECOND SEQUENCE: Buy button clicked, waiting for loading...")
                            
                            # Wait for loading and look for processing payment message
                            try:
                                # Use the exact HTML structure you provided
                                processing_selectors = [
                                    # Exact selector for the h2 "Processing payment" element
                                    "//h2[@class='web_ui__Text__text web_ui__Text__title web_ui__Text__left' and text()='Processing payment']",
                                    
                                    # Alternative: look for the reservation message span
                                    "//span[@class='web_ui__Text__text web_ui__Text__body web_ui__Text__left web_ui__Text__format' and contains(text(), \"We've reserved this item for you until your payment finishes processing\")]",
                                    
                                    # Fallback: broader selectors
                                    "//h2[contains(@class, 'web_ui__Text__title') and text()='Processing payment']",
                                    "//span[contains(text(), \"We've reserved this item for you until your payment finishes processing\")]"
                                ]
                                
                                processing_found = False
                                
                                for i, selector in enumerate(processing_selectors, 1):
                                    try:
                                        print(f"🔖 SECOND SEQUENCE: Trying selector {i}...")
                                        
                                        processing_element = WebDriverWait(self.persistent_bookmark_driver, 3).until(
                                            EC.presence_of_element_located((By.XPATH, selector))
                                        )
                                        
                                        element_text = processing_element.text.strip()
                                        print(f"🔖 SECOND SEQUENCE: Found element with text: '{element_text}'")
                                        print('SUCCESSFUL BOOKMARK! CONFIRMED VIA PROCESSING PAYMENT!')
                                        processing_found = True
                                        break
                                        
                                    except TimeoutException:
                                        continue
                                    except Exception as e:
                                        print(f"🔖 SECOND SEQUENCE: Selector {i} error: {e}")
                                        continue
                                
                                if not processing_found:
                                    print('listing likely bookmarked by another')
                                    
                            except Exception as detection_error:
                                print(f'🔖 SECOND SEQUENCE: Error during processing payment detection: {detection_error}')
                                print('listing likely bookmarked by another')
                            
                            # Close tab and return (do NOT continue with messages)
                            print("🔖 SECOND SEQUENCE: Closing tab...")
                            self.persistent_bookmark_driver.close()
                            if len(self.persistent_bookmark_driver.window_handles) > 0:
                                self.persistent_bookmark_driver.switch_to.window(self.persistent_bookmark_driver.window_handles[0])
                            
                            return True
                        
                        else:
                            print("🔖 SECOND SEQUENCE: Buy button not found, proceeding with messages...")
                            
                            # Continue with existing messages functionality
                            print("📧 MESSAGES: Opening new tab to check messages...")
                            self.persistent_bookmark_driver.execute_script("window.open('');")
                            
                            # Switch to the new messages tab
                            messages_tab = self.persistent_bookmark_driver.window_handles[-1]
                            self.persistent_bookmark_driver.switch_to.window(messages_tab)
                            print(f"📧 MESSAGES: Switched to messages tab (total tabs: {len(self.persistent_bookmark_driver.window_handles)})")
                            
                            try:
                                # Navigate to the same URL first
                                print(f"📧 MESSAGES: Navigating to {actual_url}...")
                                self.persistent_bookmark_driver.get(actual_url)
                                print("📧 MESSAGES: Navigation complete")
                                
                                # Look for the messages button with multiple selectors
                                print("📧 MESSAGES: Looking for messages button...")
                                
                                messages_selectors = [
                                    "a[data-testid='header-conversations-button']",
                                    "a[href='/inbox'][data-testid='header-conversations-button']",
                                    "a[href='/inbox'].web_ui__Button__button",
                                    "a[aria-label*='message'][href='/inbox']",
                                    "a[href='/inbox']",
                                ]
                                
                                messages_button_found = False
                                for selector in messages_selectors:
                                    try:
                                        messages_button = WebDriverWait(self.persistent_bookmark_driver, 1).until(
                                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                                        )
                                        
                                        aria_label = messages_button.get_attribute("aria-label") or "messages"
                                        print(f"📧 MESSAGES: Found messages button with selector: {selector}")
                                        print(f"📧 MESSAGES: Button label: {aria_label}")
                                        
                                        try:
                                            messages_button.click()
                                            print("📧 MESSAGES: Standard click successful")
                                        except:
                                            try:
                                                self.persistent_bookmark_driver.execute_script("arguments[0].click();", messages_button)
                                                print("📧 MESSAGES: JavaScript click successful")
                                            except:
                                                try:
                                                    ActionChains(self.persistent_bookmark_driver).move_to_element(messages_button).click().perform()
                                                    print("📧 MESSAGES: ActionChains click successful")
                                                except:
                                                    print("📧 MESSAGES: All click methods failed")
                                                    continue
                                        
                                        messages_button_found = True
                                        break
                                        
                                    except:
                                        continue
                                
                                if messages_button_found:
                                    print("📧 MESSAGES: Button clicked successfully")
                                    
                                    # Search for username functionality
                                    if username:
                                        print(f"📧 SEARCHING: Looking for username '{username}' on messages page...")
                                        
                                        time.sleep(2)
                                        
                                        try:
                                            
                                            username_element = WebDriverWait(self.persistent_bookmark_driver, 3).until(
                                                EC.element_to_be_clickable((By.XPATH, f"//h2[contains(@class, 'web_ui') and contains(@class, 'Text') and contains(@class, 'title') and text()='{username}']"))
                                            )
                                            
                                            print(f"📧 FOUND: Username '{username}' on messages page!")
                                            
                                            try:
                                                username_element.click()
                                                print(f"📧 CLICKED: Username '{username}' clicked successfully")
                                            except:
                                                try:
                                                    self.persistent_bookmark_driver.execute_script("arguments[0].click();", username_element)
                                                    print(f"📧 CLICKED: Username '{username}' clicked with JavaScript")
                                                except:
                                                    try:
                                                        ActionChains(self.persistent_bookmark_driver).move_to_element(username_element).click().perform()
                                                        print(f"📧 CLICKED: Username '{username}' clicked with ActionChains")
                                                    except:
                                                        print(f"📧 CLICK FAILED: Could not click username '{username}'")
                                            
                                            print("USERNAME FOUND, POSSIBLE ACCIDENTAL PURCHASE, ABORT")
                                            time.sleep(3)
                                            sys.exit(0)
                                            
                                        except TimeoutException:
                                            print(f"📧 NOT FOUND: Username '{username}' not found on messages page")
                                            print(f"unable to find username {username} for listing {actual_url}, likely bookmarked!")
                                        except Exception as search_error:                        
                                            print(f"📧 SEARCH ERROR: Error searching for username '{username}': {search_error}")
                                            print(f"unable to find username {username} for listing {actual_url}, likely bookmarked!")
                                            
                                    else:
                                        print("📧 NO USERNAME: No username available for search, waiting 3 seconds...")
                                        time.sleep(3)
                                        
                                else:
                                    print("📧 MESSAGES: Messages button not found")
                                    
                            except Exception as messages_error:
                                print(f"📧 MESSAGES: Error during messages check - {messages_error}")
                            
                            # Close the messages tab
                            print("📧 MESSAGES: Closing messages tab...")
                            self.persistent_bookmark_driver.close()
                            
                            # Switch back to the main tab
                            if len(self.persistent_bookmark_driver.window_handles) > 0:
                                self.persistent_bookmark_driver.switch_to.window(self.persistent_bookmark_driver.window_handles[0])
                                print(f"📧 MESSAGES: Back to main tab (remaining tabs: {len(self.persistent_bookmark_driver.window_handles)})")
                            
                            print("🔖 SUCCESS: Bookmark and messages check completed!")
                            return True
                    else:
                        print("🔖 FIRST SEQUENCE: Buy button not found, closing tab...")
                        print('this means ALREADY SOLD!!!')
                        self.persistent_bookmark_driver.close()
                        if len(self.persistent_bookmark_driver.window_handles) > 0:
                            self.persistent_bookmark_driver.switch_to.window(self.persistent_bookmark_driver.window_handles[0])
                            
                except Exception as nav_error:
                    print(f"🔖 NAVIGATION: Error - {nav_error}")
                
            except Exception as e:
                print(f"🔖 FAST ERROR: {e}")
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

    def run(self):
        global suitable_listings, current_listing_index, recent_listings, current_listing_title, current_listing_price
        global current_listing_description, current_listing_join_date, current_detected_items, current_profit
        global current_listing_images, current_listing_url, current_suitability, current_expected_revenue
        
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
        
        # Initialize pygame display with default valuess
        self.update_listing_details("", "", "", "0", 0, 0, {}, [], {})
        
        # Start Flask app in separate thread.
        flask_thread = threading.Thread(target=self.run_flask_app)
        flask_thread.daemon = True
        flask_thread.start()
        
        # Start pygame window in separate threadu
        pygame_thread = threading.Thread(target=self.run_pygame_window)
        pygame_thread.start()
        
        # Clear download folder and start scrapingu
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