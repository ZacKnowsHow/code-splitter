# Continuation from line 6601
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
