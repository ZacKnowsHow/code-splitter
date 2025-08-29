# Continuation from line 2201
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

# Enhanced process_single_listing_with_driver function with robustness improvements

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
