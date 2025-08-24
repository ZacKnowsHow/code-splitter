# Continuation from line 4401
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
            actual_url = listing_url
            print(f"🔖 NORMAL MODE: Using actual listing URL")
        
        # USERNAME IS NOW PASSED AS PARAMETER - NO NEED TO EXTRACT FROM DRIVER
        if not username:
            print("⚠️ Could not extract username, proceeding without username lookup")
        
        print(f"🔖 Looking at listing {actual_url} posted by {username if username else 'unknown user'}")
        
        try:
            print(f"🔖 STARTING BOOKMARK: {actual_url}")
            
            # Initialize persistent driver if it doesn't exist
            if not hasattr(self, 'persistent_bookmark_driver') or self.persistent_bookmark_driver is None:
                print("🔖 INITIALIZING: Creating persistent bookmark driver...")
                
                # SPEED OPTIMIZATION 1: Pre-cached service
                if not hasattr(self, '_cached_chromedriver_path'):
                    self._cached_chromedriver_path = ChromeDriverManager().install()
                
                # SPEED OPTIMIZATION 2: Minimal Chrome options
                chrome_opts = Options()
                bookmark_user_data_dir = f"{PERMANENT_USER_DATA_DIR}_Bookmark"
                chrome_opts.add_argument(f"--user-data-dir={bookmark_user_data_dir}")
                chrome_opts.add_argument("--profile-directory=Profile 4")
                chrome_opts.add_argument("--no-sandbox")
                chrome_opts.add_argument("--disable-dev-shm-usage")
                chrome_opts.add_argument("--disable-gpu")
                chrome_opts.add_argument("--disable-extensions")
                chrome_opts.add_argument("--disable-plugins")
                chrome_opts.add_argument("--disable-web-security")
                chrome_opts.add_argument("--disable-features=TranslateUI")
                chrome_opts.add_argument("--disable-background-networking")
                chrome_opts.add_argument("--no-first-run")
                chrome_opts.add_argument("--window-size=1920,1080")
                chrome_opts.add_argument("--log-level=3")
                chrome_opts.add_argument("--silent")
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
            
            # Check if driver is still alive
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
                
                # ULTRA-FAST BUY BUTTON CLICKING
                print("🔖 SEARCHING: Looking for Buy now button...")
                
                # Multiple selectors for maximum speed and reliability
                buy_selectors = [
                    "button[data-testid='item-buy-button']",  # Most specific
                    "button.web_ui__Button__primary[data-testid='item-buy-button']",  # Backup
                    "button:contains('Buy now')",  # Text-based fallback
                    ".web_ui__Button__primary .web_ui__Button__label:contains('Buy now')",  # Label-based
                ]
                
                buy_button_found = False
                for selector in buy_selectors:
                    try:
                        # Very short wait - just 0.5 seconds per selector
                        buy_button = WebDriverWait(self.persistent_bookmark_driver, 0.5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                        
                        print(f"🔖 FOUND: Buy button with selector: {selector}")
                        
                        # INSTANT CLICK - try multiple click methods for speed
                        click_successful = False
                        try:
                            buy_button.click()
                            print("🔖 CLICKED: Standard click successful")
                            click_successful = True
                        except:
                            try:
                                self.persistent_bookmark_driver.execute_script("arguments[0].click();", buy_button)
                                print("🔖 CLICKED: JavaScript click successful")
                                click_successful = True
                            except:
                                try:
                                    ActionChains(self.persistent_bookmark_driver).move_to_element(buy_button).click().perform()
                                    print("🔖 CLICKED: ActionChains click successful")
                                    click_successful = True
                                except:
                                    print("🔖 CLICK: All click methods failed")
                        
                        # If click was successful, wait for payment page to load - ULTRA FAST
                        if click_successful:
                            print("🔖 WAITING: For payment page to load...")
                            
                            try:
                                # SINGLE FAST CHECK - only look for the specific Pay button
                                pay_button = WebDriverWait(self.persistent_bookmark_driver, 8).until(
                                    EC.element_to_be_clickable((By.CSS_SELECTOR, 
                                        'button[data-testid="single-checkout-order-summary-purchase-button"]'
                                    ))
                                )
                                print("🔖 PAYMENT PAGE LOADED!")
                                
                                # CHECK IF WE SHOULD CLICK THE PAY BUTTON
                                if click_pay_button_final_check:
                                    print("🔖 FINAL CHECK MODE: Clicking Pay button...")
                                    
                                    try:
                                        # SINGLE CLICK ATTEMPT - no retries, no fallbacks
                                        pay_button.click()
                                        
                                        # PRECISELY 0.25 seconds after the click - NO MATTER WHAT
                                        time.sleep(0.25)
                                        
                                        # CTRL+W to close tab instantly
                                        self.persistent_bookmark_driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 'w')
                                        
                                        print("🔖 FINAL CHECK SUCCESS: Pay button clicked and tab closed after 0.25s")
                                        
                                    except Exception as final_error:
                                        print(f"🔖 FINAL CHECK FAILURE: Error during pay button click or tab close - {final_error}")
                                
                            except TimeoutException:
                                print("🔖 PAYMENT PAGE: Timeout - Pay button not found")
                            except Exception as e:
                                print(f"🔖 PAYMENT PAGE ERROR: {e}")
                        
                        buy_button_found = True
                        break
                        
                    except TimeoutException:
                        continue  # Try next selector
                    except Exception as e:
                        print(f"🔖 SELECTOR ERROR: {selector} - {e}")
                        continue
                
                # MODIFIED: Print 'already sold' when buy button not found
                if not buy_button_found:
                    print("already sold")
                
            except Exception as nav_error:
                # Timeout is fine - we just want to trigger the visit
                print(f"🔖 NAVIGATION: Timeout (acceptable)")
            
            # Close the current tab (but keep the driver alive)
            print("🔖 TAB: Closing current tab...")
            self.persistent_bookmark_driver.close()
            
            # Switch back to the first tab to keep the driver ready
            if len(self.persistent_bookmark_driver.window_handles) > 0:
                self.persistent_bookmark_driver.switch_to.window(self.persistent_bookmark_driver.window_handles[0])
                print(f"🔖 TAB: Switched back to main tab (remaining tabs: {len(self.persistent_bookmark_driver.window_handles)})")
            
            # NEW: MODIFIED MESSAGE CHECKING FUNCTIONALITY
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
                    "a[data-testid='header-conversations-button']",  # Most specific
                    "a[href='/inbox'][data-testid='header-conversations-button']",  # More specific with href
                    "a[href='/inbox'].web_ui__Button__button",  # Alternative with class
                    "a[aria-label*='message'][href='/inbox']",  # Aria-label contains 'message'
                    "a[href='/inbox']",  # Broad fallback
                ]
                
                messages_button_found = False
                for selector in messages_selectors:
                    try:
                        # Short wait for each selector - 1 second
                        messages_button = WebDriverWait(self.persistent_bookmark_driver, 1).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                        
                        # Get the aria-label to see how many messages
                        aria_label = messages_button.get_attribute("aria-label") or "messages"
                        print(f"📧 MESSAGES: Found messages button with selector: {selector}")
                        print(f"📧 MESSAGES: Button label: {aria_label}")
                        
                        # Click the messages button
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
                        
                    except TimeoutException:
                        continue  # Try next selector
                    except Exception as e:
                        print(f"📧 MESSAGES: Selector error {selector} - {e}")
                        continue
                
                if messages_button_found:
                    print("📧 MESSAGES: Button clicked successfully")
                    
                    # NEW: SEARCH FOR THE USERNAME ON THE MESSAGES PAGE
                    if username:
                        print(f"📧 SEARCHING: Looking for username '{username}' on messages page...")
                        
                        # Wait for messages page to load
                        time.sleep(2)
                        
                        # Look for the username using the specific pattern provided
                        username_selector = f'h2.web_uiTexttext.web_uiTexttitle.web_uiTextleft:contains("{username}")'
                        
                        try:
                            #REMOVE THIS LATER!!!
                            username = 'yvonnematthew'
                            # Wait for the username element to appear
                            username_element = WebDriverWait(self.persistent_bookmark_driver, 3).until(
                                EC.element_to_be_clickable((By.XPATH, f"//h2[contains(@class, 'web_ui') and contains(@class, 'Text') and contains(@class, 'title') and text()='{username}']"))
                            )
                            
                            print(f"📧 FOUND: Username '{username}' on messages page!")
                            
                            # Click on the username
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
                            
                            # Wait 3 seconds after clicking

                            try:
                                print('wating 5s for shit to load')
                                purchase_element = self.persistent_bookmark_driver.find_element(By.CSS_SELECTOR, 'h2.web_ui__Text__text.web_ui__Text__title.web_ui__Text__left.web_ui__Text__muted')
                                if purchase_element.text.strip() == "Purchase successful":
                                    print("Purchase successful found - stopping scraper")
                                    import sys
                                    sys.exit(0)
                            except:
                                print('passing')
                                pass
                            
                        except TimeoutException:
                            print(f"📧 NOT FOUND: Username '{username}' not found on messages page")
                            print(f"unable to find username {username} for listing {actual_url}, likely failed to bookmark or buy.")
                        except Exception as search_error:
                            print(f"📧 SEARCH ERROR: Error searching for username '{username}': {search_error}")
                            print(f"unable to find username {username} for listing {actual_url}, likely failed to bookmark or buy.")
                            
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
        # chrome_opts.add_argument("--headless")  # Try without headless first
        
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
        try:
            self.search_vinted_with_refresh(driver, SEARCH_QUERY)
        finally:
            driver.quit()

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