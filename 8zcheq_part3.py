# Continuation from line 4401
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
            'miscellaneous_games': 5  # ADDED: Price for miscellaneous games (£5 each)
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
            
            # Wait a bit for login process
            time.sleep(random.uniform(3, 5))
            
            driver.set_window_size(900, 600)
            
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
        """Execute bookmark using driver from manager"""
        
        # Get current driver from manager
        bookmark_driver = self.driver_manager.get_driver()
        
        if not bookmark_driver or not self.driver_manager.is_ready():
            print("❌ BOOKMARK: No valid driver available in manager")
            return False
        
        driver_session = self.driver_manager.get_session_id()
        print(f"🔖 BOOKMARK: Using driver from manager (Session: {driver_session})")
        print(f"🔖 BOOKMARK: Driver ALREADY on listing page: {url}")
        
        try:
            # Verify driver is still valid
            try:
                _ = bookmark_driver.current_url
            except Exception as driver_check_error:
                print(f"❌ BOOKMARK: Driver is no longer valid: {driver_check_error}")
                self.driver_manager.invalidate_driver()
                return False
            
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
            
            # Execute first buy sequence
            success = execute_vm_first_buy_sequence(bookmark_driver, step_log)
            
            # Driver is now used - invalidate in manager
            self.driver_manager.invalidate_driver()
            print(f"⚠️ BOOKMARK: Driver marked as used in manager")
            
            total_time = time.time() - step_log['start_time']
            print(f"📊 BOOKMARK ANALYSIS:")
            print(f"⏱️  Total time: {total_time:.2f}s")
            print(f"✅ Steps completed: {len(step_log['steps_completed'])}")
            print(f"❌ Failures: {len(step_log['failures'])}")
            print(f"🏆 Overall success: {'YES' if success else 'NO'}")
            
            # Store bookmark result
            self.last_bookmark_result = {
                'url': url,
                'success': success,
                'timestamp': time.time()
            }
            
            return success
            
        except Exception as e:
            print(f"❌ BOOKMARK: Error using driver: {e}")
            self.driver_manager.invalidate_driver()
            self.last_bookmark_result = {
                'url': url,
                'success': False,
                'timestamp': time.time()
            }
            return False

    def prepare_next_vm_driver(self):
        """Prepare the NEXT VM driver after current one is used"""
        print("🔄 NEXT DRIVER: Preparing next VM driver...")
        
        try:
            # Get old driver from manager
            old_driver = self.driver_manager.get_driver()
            old_session = self.driver_manager.get_session_id()
            
            # Invalidate old driver in manager FIRST
            self.driver_manager.invalidate_driver()
            print(f"⚠️ NEXT DRIVER: Old driver invalidated in manager (Session: {old_session})")
            
            # CRITICAL FIX: Close the old driver IMMEDIATELY before any other operations
            if old_driver:
                try:
                    print(f"🔄 NEXT DRIVER: Closing old driver IMMEDIATELY (Session: {old_session})")
                    old_driver.quit()
                    print(f"✅ NEXT DRIVER: Old driver closed successfully (Session: {old_session})")
                except Exception as close_error:
                    print(f"⚠️ NEXT DRIVER: Error closing old driver: {close_error}")
            
            # CRITICAL: Wait for old driver to fully close before proceeding
            print("⏳ NEXT DRIVER: Waiting 2 seconds for old driver to fully terminate...")
            time.sleep(2)
            
            # Now clear browser data for NEW session (no old driver interfering)
            print("🔄 NEXT DRIVER: Old driver confirmed closed, now clearing browser data for NEW session...")
            clear_browser_data_universal("192.168.56.101", {
                "user_data_dir": "C:\\VintedScraper_Default_Bookmark", 
                "profile": "Profile 4", 
                "port": 9224
            })
            
            # Small delay after clearing
            time.sleep(1)
            
            # Create new VM driver
            print("🔄 NEXT DRIVER: Creating new VM driver...")
            new_driver = setup_driver_universal("192.168.56.101", {
                "user_data_dir": "C:\\VintedScraper_Default_Bookmark", 
                "profile": "Profile 4", 
                "port": 9224
            })
            
            if not new_driver:
                print("❌ NEXT DRIVER: Failed to create new VM driver")
                # ADDED: Ensure manager knows there's no driver
                self.driver_manager.set_driver(None)
                return
            
            # Verify new driver is functional
            try:
                _ = new_driver.current_url
                new_session = new_driver.session_id
                print(f"✅ NEXT DRIVER: New driver verified (Session: {new_session})")
            except Exception as verify_error:
                print(f"❌ NEXT DRIVER: New driver verification failed: {verify_error}")
                try:
                    new_driver.quit()
                except:
                    pass
                # ADDED: Ensure manager knows there's no driver
                self.driver_manager.set_driver(None)
                return
            
            # Login the new driver
            print("🔄 NEXT DRIVER: Logging in new driver...")
            success = self.login_vm_driver(new_driver)
            
            if success:
                # Register new driver with manager
                self.driver_manager.set_driver(new_driver)
                print("✅ NEXT DRIVER: New VM driver registered with manager and ready")
            else:
                print("❌ NEXT DRIVER: Failed to login new VM driver")
                try:
                    new_driver.quit()
                except:
                    pass
                # ADDED: Ensure manager knows there's no driver
                self.driver_manager.set_driver(None)
                
        except Exception as e:
            print(f"❌ NEXT DRIVER: Error preparing next driver: {e}")
            import traceback
            traceback.print_exc()
            # ADDED: Ensure manager knows there's no driver on exception
            self.driver_manager.set_driver(None)

    def __init__(self):
        """Modified init - Initialize for VM-based scraping with driver manager"""
        global current_listing_title, current_listing_description, current_listing_join_date, current_listing_price
        global current_expected_revenue, current_profit, current_detected_items, current_listing_images
        global current_bounding_boxes, current_listing_url, current_suitability, suitable_listings
        global current_listing_index, recent_listings, current_seller_reviews, current_bookmark_status
        
        print("🔧 INIT: Starting VintedScraper initialization...")
        
        recent_listings = {
            'listings': [],
            'current_index': 0
        }

        self.program_start_time = time.time()
        
        # NEW: Initialize centralized driver manager FIRST
        self.driver_manager = DriverManager()
        print("🔧 INIT: Driver manager created")
        
        # Track bookmark results
        self.last_bookmark_result = None
        self.bookmark_results_by_url = {}
        
        # Initialize VM bookmark queue
        self.vm_bookmark_queue = []
        
        # Load YOLO model
        print(f"🧠 CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"🎮 GPU name: {torch.cuda.get_device_name(0)}")
        
        print("🧠 Loading YOLO model ONCE at startup...")
        if not os.path.exists(MODEL_WEIGHTS):
            print(f"❌ Model weights not found at '{MODEL_WEIGHTS}'")
            self.model = None
        else:
            try:
                if torch.cuda.is_available():
                    self.model = YOLO(MODEL_WEIGHTS)
                    self.model.to('cuda')
                    print("✅ YOLO model loaded on GPU (CUDA)")
                else:
                    self.model = YOLO(MODEL_WEIGHTS)
                    print("⚠️ YOLO model loaded on CPU")
                
                print("🔥 Warming up model...")
                import numpy as np
                dummy_img = np.zeros((640, 640, 3), dtype=np.uint8)
                _ = self.model(dummy_img, verbose=False)
                print("✅ Model warmed up and ready")
                print(f"✅ Model device: {next(self.model.model.parameters()).device}")
                
            except Exception as e:
                print(f"❌ Could not load YOLO model: {e}")
                import traceback
                traceback.print_exc()
                self.model = None
        
        # Prepare initial VM driver AFTER driver manager is created
        print("🔄 INIT: Preparing initial VM driver...")
        try:
            # Clear browser data first
            clear_browser_data_universal("192.168.56.101", {
                "user_data_dir": "C:\\VintedScraper_Default_Bookmark", 
                "profile": "Profile 4", 
                "port": 9224
            })
            
            time.sleep(1)
            
            # Create initial driver
            initial_driver = setup_driver_universal("192.168.56.101", {
                "user_data_dir": "C:\\VintedScraper_Default_Bookmark", 
                "profile": "Profile 4", 
                "port": 9224
            })
            
            if not initial_driver:
                print("❌ INIT: Failed to create initial VM driver")
            else:
                # Login the initial driver
                success = self.login_vm_driver(initial_driver)
                
                if success:
                    # Register with driver manager
                    self.driver_manager.set_driver(initial_driver)
                    print("✅ INIT: Initial VM driver ready and registered with manager")
                else:
                    print("❌ INIT: Failed to login initial VM driver")
                    try:
                        initial_driver.quit()
                    except:
                        pass
        except Exception as init_driver_error:
            print(f"❌ INIT: Error preparing initial driver: {init_driver_error}")
            import traceback
            traceback.print_exc()
        
        # Initialize listing variables
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
        current_seller_reviews = "No reviews yet"  # FIXED: Added this line
        current_bookmark_status = "Not attempted"  # FIXED: Added this line
        suitable_listings = []
        current_listing_index = 0
        
        print("✅ INIT: VintedScraper initialization complete")

    def format_runtime(self, elapsed_seconds):
        """
        Format elapsed time into HH:MM:SS format
        """
        hours = int(elapsed_seconds // 3600)
        minutes = int((elapsed_seconds % 3600) // 60)
        seconds = int(elapsed_seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def render_suitability_with_bookmark(self, screen, font, text, rect, suitability_color, bookmark_color):
        """
        Render suitability text with bookmark status in different color
        Splits text at double newline to separate suitability from bookmark status
        """
        try:
            # Split text into suitability and bookmark parts
            parts = text.split('\n\n')
            
            if len(parts) == 1:
                # No bookmark status, just render suitability
                self.render_text_in_rect(screen, font, text, rect, suitability_color)
                return
            
            suitability_text = parts[0]
            bookmark_text = parts[1] if len(parts) > 1 else ""
            
            # Calculate space for each part
            # Wrap suitability text
            suitability_lines = []
            words = suitability_text.split()
            current_line = []
            for word in words:
                test_line = ' '.join(current_line + [word])
                test_width, _ = font.size(test_line)
                if test_width <= rect.width - 10:
                    current_line.append(word)
                else:
                    if current_line:
                        suitability_lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        suitability_lines.append(word)
            if current_line:
                suitability_lines.append(' '.join(current_line))
            
            # Wrap bookmark text
            bookmark_lines = []
            words = bookmark_text.split()
            current_line = []
            for word in words:
                test_line = ' '.join(current_line + [word])
                test_width, _ = font.size(test_line)
                if test_width <= rect.width - 10:
                    current_line.append(word)
                else:
                    if current_line:
                        bookmark_lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        bookmark_lines.append(word)
            if current_line:
                bookmark_lines.append(' '.join(current_line))
            
            # Calculate total height needed
            total_lines = len(suitability_lines) + len(bookmark_lines)
            line_height = font.get_linesize()
            total_height = total_lines * line_height + 10  # 10px gap between sections
            
            # Scale font if needed
            if total_height > rect.height:
                scale_factor = rect.height / total_height
                new_font_size = max(1, int(font.get_height() * scale_factor))
                try:
                    font = pygame.font.Font(None, new_font_size)
                    line_height = font.get_linesize()
                except pygame.error:
                    pass  # Keep original font if scaling fails
            
            # Render suitability lines
            y = rect.top + 5
            for line in suitability_lines:
                try:
                    text_surface = font.render(line, True, suitability_color)
                    text_rect = text_surface.get_rect(centerx=rect.centerx, top=y)
                    screen.blit(text_surface, text_rect)
                    y += line_height
                except pygame.error as e:
                    print(f"Error rendering suitability line: {e}")
                    continue
            
            # Add gap
            y += 5
            
            # Render bookmark lines
            for line in bookmark_lines:
                try:
                    text_surface = font.render(line, True, bookmark_color)
                    text_rect = text_surface.get_rect(centerx=rect.centerx, top=y)
                    screen.blit(text_surface, text_rect)
                    y += line_height
                except pygame.error as e:
                    print(f"Error rendering bookmark line: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error in render_suitability_with_bookmark: {e}")
            # Fallback to simple rendering
            self.render_text_in_rect(screen, font, text, rect, suitability_color)


    def run_pygame_window(self):
        global LOCK_POSITION, current_listing_index, suitable_listings
        global current_seller_reviews, current_bookmark_status  # FIXED: Added this line
        
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
                            # CRITICAL FIX: Properly switch to stored listing data including images
                            current_listing = suitable_listings[current_listing_index]
                            
                            # FIXED: Pass the stored images from the listing, not empty list
                            stored_images = current_listing.get('processed_images', [])
                            
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
                                bookmark_status=current_listing.get('bookmark_status', 'Not attempted')
                            )
                    elif event.key == pygame.K_LEFT:
                        if suitable_listings:
                            current_listing_index = (current_listing_index - 1) % len(suitable_listings)
                            # CRITICAL FIX: Properly switch to stored listing data including images
                            current_listing = suitable_listings[current_listing_index]
                            
                            # FIXED: Pass the stored images from the listing, not empty list
                            stored_images = current_listing.get('processed_images', [])
                            
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
                                bookmark_status=current_listing.get('bookmark_status', 'Not attempted')
                            )
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
                elif i == 8:  # Rectangle 9 (index 8) - FIXED: Shows exact stored timestamp
                    time_label = "Appended:"
                    self.render_text_in_rect(screen, fonts['exact_time'], f"{time_label}\n{current_listing_join_date}", rect, (0, 128, 0))
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
                elif i == 5:  # Rectangle 6 (index 5) - Suitability Reason AND Bookmark Status
                    # NEW: Combine suitability and bookmark status
                    combined_text = current_suitability
                    if 'current_bookmark_status' in globals() and current_bookmark_status:
                        combined_text = f"{current_suitability}\n\n{current_bookmark_status}"
                    
                    # Determine color based on bookmark status
                    if 'current_bookmark_status' in globals() and current_bookmark_status:
                        if "successful" in current_bookmark_status.lower():
                            bookmark_color = (0, 255, 0)  # Green for success
                        elif "failed" in current_bookmark_status.lower():
                            bookmark_color = (255, 0, 0)  # Red for failure
                        else:
                            bookmark_color = (128, 128, 128)  # Gray for not attempted
                    else:
                        bookmark_color = (128, 128, 128)  # Gray default
                    
                    # Use red for unsuitable, green for suitable, but show bookmark status in appropriate color
                    base_color = (255, 0, 0) if "Unsuitable" in current_suitability else (0, 255, 0)
                    
                    # Render with multi-color support
                    self.render_suitability_with_bookmark(screen, fonts['suitability'], combined_text, rect, base_color, bookmark_color)
                elif i == 6:  # Rectangle 7 (index 6) - Seller Reviews
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

    def update_listing_details(self, title, description, join_date, price, expected_revenue, profit, detected_items, processed_images, bounding_boxes, url=None, suitability=None, seller_reviews=None, bookmark_status=None):
        global current_listing_title, current_listing_description, current_listing_join_date, current_listing_price
        global current_expected_revenue, current_profit, current_detected_items, current_listing_images 
        global current_bounding_boxes, current_listing_url, current_suitability, current_seller_reviews
        global current_bookmark_status

        # CRITICAL FIX 1: Don't clear existing images when switching between listings
        # Only clear if we're setting NEW images (not switching to existing listing)
        if processed_images:  # Only clear and replace if new images are provided
            # Close and clear existing images
            if 'current_listing_images' in globals():
                for img in current_listing_images:
                    try:
                        img.close()  # Explicitly close the image
                    except Exception as e:
                        print(f"Error closing image: {str(e)}")
                current_listing_images.clear()

            # Add new images
            for img in processed_images:
                try:
                    img_copy = img.copy()  # Create a fresh copy
                    current_listing_images.append(img_copy)
                except Exception as e:
                    print(f"Error copying image: {str(e)}")
        # If no processed_images provided, keep existing current_listing_images intact

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

        # CRITICAL FIX 2: Use the exact join_date parameter that was stored, never generate new timestamp
        stored_append_time = join_date if join_date else "No timestamp"

        # Explicitly set the global variables
        current_detected_items = formatted_detected_items
        current_listing_title = title[:50] + '...' if len(title) > 50 else title
        current_listing_description = description[:200] + '...' if len(description) > 200 else description if description else "No description"
        current_listing_join_date = stored_append_time  # FIXED: Use stored timestamp, never current time
        current_listing_price = f"Price:\n£{float(price):.2f}" if price else "Price:\n£0.00"
        current_expected_revenue = f"Rev:\n£{expected_revenue:.2f}" if expected_revenue else "Rev:\n£0.00"
        current_profit = f"Profit:\n£{profit:.2f}" if profit else "Profit:\n£0.00"
        current_listing_url = url
        current_suitability = suitability if suitability else "Suitability unknown"
        current_seller_reviews = seller_reviews if seller_reviews else "No reviews yet"
        current_bookmark_status = bookmark_status if bookmark_status else "Not attempted"  # NEW: Set bookmark status
        
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
        OPTIMIZED: Single-pass element extraction using JavaScript
        Waits for page load, then extracts ALL fields in one round-trip
        """
        # Wait for page to be ready (same as original implicit behavior)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.web_ui__Text__title"))
            )
        except TimeoutException:
            print("Warning: Page load timeout in scrape_item_details")
        
        # Single JavaScript execution that extracts ALL fields at once
        extract_script = """
        return {
            title: document.querySelector('h1.web_ui__Text__title')?.textContent || null,
            price: document.querySelector('p.web_ui__Text__subtitle')?.textContent || null,
            second_price: document.querySelector('div.web_ui__Text__title.web_ui__Text__clickable.web_ui__Text__underline-none')?.textContent || null,
            postage: document.querySelector('h3[data-testid="item-shipping-banner-price"]')?.textContent || null,
            description: Array.from(document.querySelectorAll('span.web_ui__Text__text.web_ui__Text__body.web_ui__Text__left.web_ui__Text__format span')).map(el => el.textContent).join(' ') || null,
            uploaded: document.querySelector('span.web_ui__Text__text.web_ui__Text__subtitle.web_ui__Text__left.web_ui__Text__bold')?.textContent || null,
            username: document.querySelector('span[data-testid="profile-username"]')?.textContent || null,
            seller_reviews: (() => {
                const selectors = [
                    'span.web_ui__Text__text.web_ui__Text__caption.web_ui__Text__left',
                    'span[class*="caption"][class*="left"]'
                ];
                for (let sel of selectors) {
                    const elements = document.querySelectorAll(sel);
                    for (let el of elements) {
                        const text = el.textContent.trim();
                        if (text && (text.match(/\\d+/) || text.toLowerCase().includes('review') || text.toLowerCase().includes('no review'))) {
                            return text;
                        }
                    }
                }
                return "No reviews yet";
            })()
        };
        """
        
        try:
            # SINGLE round-trip to VM driver - extracts all data at once
            data = driver.execute_script(extract_script)
            
            # Process seller reviews (exact same logic as original)
            reviews_text = data.get("seller_reviews", "No reviews yet")
            if reviews_text == "No reviews yet" or "no review" in reviews_text.lower():
                data["seller_reviews"] = "No reviews yet"
            elif reviews_text.isdigit():
                data["seller_reviews"] = reviews_text
            else:
                import re
                match = re.search(r'(\d+)', reviews_text)
                data["seller_reviews"] = match.group(1) if match else "No reviews yet"
            
            # Process title (exact same logic as original)
            if data["title"]:
                data["title"] = data["title"][:50] + '...' if len(data["title"]) > 50 else data["title"]
            
            # Calculate and store total price (exact same logic as original)
            second_price = self.extract_price(data.get("second_price", "0"))
            postage = self.extract_price(data.get("postage", "0"))
            total_price = second_price + postage
            self.current_listing_price_float = total_price
            
            return data
            
        except Exception as e:
            print(f"Error in optimized scrape_item_details: {e}")
            # Return same structure as original with None values
            return {
                "title": "Error extracting title",
                "price": None,
                "second_price": None,
                "postage": None,
                "description": None,
                "uploaded": None,
                "seller_reviews": "No reviews yet",
                "username": "Username not found"
            }

    def clear_download_folder(self):
        if os.path.exists(DOWNLOAD_ROOT):
            shutil.rmtree(DOWNLOAD_ROOT)
        os.makedirs(DOWNLOAD_ROOT, exist_ok=True)

        
    def process_listing_immediately_with_vm(self, url, details, detected_objects, processed_images, listing_counter):
        """
        IMMEDIATELY process a suitable listing with pre-loaded VM driver
        FIXED: Uses driver manager instead of instance attributes
        """
        global suitable_listings, current_listing_index, recent_listings

        print(f"🚀 REAL-TIME: Immediately processing listing with PRE-LOADED VM driver")
        print(f"🔗 URL: {url}")
        print(f"⏸️  SCRAPING PAUSED: Processing will begin now...")

        # Extract username from details
        username = details.get("username", None)
        if not username or username == "Username not found":
            username = None
            print("🔖 USERNAME: Not available for this listing")

        # Extract and validate price
        price_text = details.get("price", "0")
        listing_price = self.extract_vinted_price(price_text)
        postage = self.extract_price(details.get("postage", "0"))
        total_price = listing_price + postage

        # Get seller reviews
        seller_reviews = details.get("seller_reviews", "No reviews yet")

        # Create listing info for suitability checking
        listing_info = {
            "title": details.get("title", "").lower(),
            "description": details.get("description", "").lower(),
            "price": total_price,
            "seller_reviews": seller_reviews,
            "url": url
        }

        # Check basic suitability 
        suitability_result = self.check_vinted_listing_suitability(listing_info)
        print(f"📋 SUITABILITY: {suitability_result}")

        # Apply console keyword detection to detected objects
        detected_console = self.detect_console_keywords_vinted(
            details.get("title", ""),
            details.get("description", "")
        )
        if detected_console:
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

        # Game count suitability check
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
            print(f"❌ UNSUITABLE: {suitability_reason}")
        else:
            suitability_reason = f"Suitable: Profit £{expected_profit:.2f} ({profit_percentage:.2f}%)"
            is_suitable = True
            print(f"✅ SUITABLE: {suitability_reason}")

        # Initialize bookmark status
        bookmark_status = "Not attempted"
        
        # ============= VM PROCESSING =============
        if is_suitable or VINTED_SHOW_ALL_LISTINGS:
            print(f"🚀 REAL-TIME PROCESSING: Using PRE-LOADED VM driver from manager")
            print(f"⏸️  SCRAPING IS PAUSED UNTIL VM PROCESS COMPLETES")
            
            # Call the bookmark function that uses driver manager
            try:
                success = self.execute_bookmark_with_preloaded_driver(url)
                if success:
                    print(f"✅ VM PROCESS COMPLETED: Listing has been bookmarked successfully")
                    bookmark_status = "Bookmark successful"
                else:
                    print(f"❌ VM PROCESS FAILED: Bookmark attempt was unsuccessful")
                    bookmark_status = "Bookmark failed"
                
                # Store bookmark result for this URL
                self.bookmark_results_by_url[url] = {
                    'success': success,
                    'status': bookmark_status,
                    'timestamp': time.time()
                }
                
            except Exception as vm_error:
                print(f"❌ VM PROCESS ERROR: {vm_error}")
                print(f"⚠️  Continuing with scraping despite VM error...")
                bookmark_status = "Bookmark failed"
                self.bookmark_results_by_url[url] = {
                    'success': False,
                    'status': bookmark_status,
                    'timestamp': time.time()
                }
            
            # CRITICAL: After processing, prepare the NEXT driver
            try:
                print(f"🔄 PREPARING NEXT DRIVER: Setting up new VM driver for next listing...")
                self.prepare_next_vm_driver()
                print(f"✅ NEXT DRIVER READY: VM driver prepared and logged in")
            except Exception as prep_error:
                print(f"❌ NEXT DRIVER ERROR: {prep_error}")
            
            print(f"▶️  SCRAPING RESUMED: VM process complete, continuing with search...")
        else:
            print(f"❌ UNSUITABLE LISTING: Skipping VM process, continuing with scraping")
            bookmark_status = "Not suitable - not attempted"
            self.bookmark_results_by_url[url] = {
                'success': False,
                'status': bookmark_status,
                'timestamp': time.time()
            }

        # CRITICAL FIX: Generate exact UK time when creating listing info and store it permanently
        from datetime import datetime
        import pytz
        
        uk_tz = pytz.timezone('Europe/London')
        append_time = datetime.now(uk_tz)
        exact_append_time = append_time.strftime("%H:%M:%S.%f")[:-3]

        # CRITICAL FIX: Create deep copies of images to prevent memory issues
        preserved_images = []
        for img in processed_images:
            try:
                img_copy = img.copy()
                preserved_images.append(img_copy)
            except Exception as e:
                print(f"Error copying image for storage: {e}")

        # Create final listing info with exact append time, preserved images, AND bookmark status
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
            'bookmark_status': bookmark_status
        }

        # Determine whether to display on website/pygame
        should_add_to_display = is_suitable or VINTED_SHOW_ALL_LISTINGS

        if should_add_to_display:
            # Send notification if suitable
            if is_suitable and send_notification:
                notification_title = f"New Vinted Listing: £{total_price:.2f}"
                notification_message = (
                    f"Title: {details.get('title', 'No title')}\n"
                    f"Price: £{total_price:.2f}\n"
                    f"Expected Profit: £{expected_profit:.2f}\n"
                    f"Profit %: {profit_percentage:.2f}%\n"
                    f"Bookmark: {bookmark_status}\n"
                )
                
                self.send_pushover_notification(
                    notification_title,
                    notification_message,
                    'aks3to8guqjye193w7ajnydk9jaxh5',
                    'ucwc6fi1mzd3gq2ym7jiwg3ggzv1pc'
                )

            # Add to recent_listings for website navigation
            recent_listings['listings'].append(final_listing_info)
            recent_listings['current_index'] = len(recent_listings['listings']) - 1

            # Add to pygame display
            suitable_listings.append(final_listing_info)
            current_listing_index = len(suitable_listings) - 1
            
            print(f"⏰ APPENDED TO DISPLAY: {exact_append_time} UK time (PRESERVED FOR PYGAME)")
            self.update_listing_details(**final_listing_info)

            if is_suitable:
                print(f"✅ Added suitable listing: £{total_price:.2f} -> £{expected_profit:.2f} profit ({profit_percentage:.2f}%) - {bookmark_status}")
            else:
                print(f"➕ Added unsuitable listing (SHOW_ALL mode): £{total_price:.2f} - {bookmark_status}")

        if not should_add_to_display:
            print(f"❌ Listing not added to display: {suitability_reason}")

        print(f"🔄 REAL-TIME PROCESSING COMPLETE: Ready to resume scraping")

    # FIXED: Updated process_vinted_listing function - key section that handles suitability checking
    def send_to_vm_bookmark_system(self, url):
        """
        DEPRECATED: This method is now replaced by immediate processing
        Real-time processing happens in process_listing_immediately_with_vm
        """
        print(f"⚠️  DEPRECATED: send_to_vm_bookmark_system called")
        print(f"🔄 REAL-TIME: Processing should happen immediately, not queued")
        pass  # Do nothing - real-time processing handles this

    def process_vinted_listing(self, details, detected_objects, processed_images, listing_counter, url):
        """
        MODIFIED: Now calls immediate processing instead of queueing
        """
        print(f"📋 PROCESSING: Listing #{listing_counter}")
        
        # Call the new real-time processing method
        self.process_listing_immediately_with_vm(url, details, detected_objects, processed_images, listing_counter)
        
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
        MODIFIED: Now adds miscellaneous games to detected_objects for visibility
        """
        debug_function_call("calculate_vinted_revenue")
        import re
        
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

        # Count detected games from YOLO detection
        detected_games_count = sum(detected_objects.get(game, 0) for game in game_classes)

        # Detect anonymous games from title and description
        text_games_count = self.detect_anonymous_games_vinted(title, description)

        # Calculate miscellaneous games (games mentioned in text but not detected by YOLO)
        misc_games_count = max(0, text_games_count - detected_games_count)
        misc_games_revenue = misc_games_count * 5  # Using £5 per miscellaneous game

        # CRITICAL NEW CODE: Add miscellaneous games to detected_objects for visibility
        if misc_games_count > 0:
            detected_objects['miscellaneous_games'] = misc_games_count
            print(f"💰 REVENUE: Added {misc_games_count} miscellaneous games (£{misc_games_revenue:.2f}) to detected objects")
        else:
            # Ensure key doesn't exist if count is 0
            detected_objects.pop('miscellaneous_games', None)

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

        # Calculate revenue from detected objects
        total_revenue = misc_games_revenue  # Start with miscellaneous games revenue

        for item, count in detected_objects.items():
            # Skip miscellaneous_games since we already counted it
            if item == 'miscellaneous_games':
                continue
                
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
        if misc_games_count > 0:
            print(f"Miscellaneous Games: {misc_games_count} games @ £5 = £{misc_games_revenue:.2f}")
        print(f"Total Expected Revenue: £{total_revenue:.2f}")
        print(f"Expected Profit/Loss: £{expected_profit:.2f} ({profit_percentage:.2f}%)")

        # CRITICAL: Filter out zero-count items for display (matching Facebook behavior)
        display_objects = {k: v for k, v in detected_objects.items() if v > 0}

        # Note: miscellaneous_games is already in detected_objects if count > 0, so it will appear in display_objects

        return total_revenue, expected_profit, profit_percentage, display_objects

    def download_and_detect_images_in_memory(self, driver, model):
        """
        SINGLE FUNCTION: Download images directly into memory and run YOLO detection
        WITHOUT writing to disk. This eliminates the entire disk I/O bottleneck.
        """
        import requests
        from PIL import Image
        from io import BytesIO
        import hashlib
        import cv2
        import numpy as np
        
        # Quick image element find
        try:
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.TAG_NAME, "img"))
            )
        except TimeoutException:
            return {class_name: 0 for class_name in CLASS_NAMES}, []
        
        # Get image URLs (your existing logic)
        img_selectors = [
            "img[data-testid^='item-photo-']",
            "div.web_ui__Image__cover img.web_ui__Image__content",
        ]
        
        imgs = []
        for selector in img_selectors:
            imgs = driver.find_elements(By.CSS_SELECTOR, selector)
            if imgs:
                break
        
        if not imgs:
            return {class_name: 0 for class_name in CLASS_NAMES}, []
        
        # Collect valid URLs
        valid_urls = []
        seen_urls = set()
        
        for img in imgs:
            src = img.get_attribute("src")
            if src and src.startswith('http'):
                normalized_url = src.split('?')[0].split('#')[0]
                if normalized_url in seen_urls:
                    continue
                seen_urls.add(normalized_url)
                if ('/50x50/' in src or '/75x75/' in src or src.endswith('.svg')):
                    continue
                if ('/f800/' in src or '/f1200/' in src or '/f600/' in src):
                    valid_urls.append(src)
        
        if not valid_urls:
            return {class_name: 0 for class_name in CLASS_NAMES}, []
        
        # Initialize detection results
        detected_objects = {class_name: [] for class_name in CLASS_NAMES}
        processed_images = []
        confidences = {item: 0 for item in ['switch', 'oled', 'lite', 'switch_box', 'oled_box', 'lite_box', 'switch_in_tv', 'oled_in_tv']}
        
        # Process each image IN MEMORY
        for url in valid_urls:
            try:
                # Download directly to memory
                resp = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
                resp.raise_for_status()
                
                # Open as PIL Image (in memory)
                pil_img = Image.open(BytesIO(resp.content))
                
                # Skip tiny images
                if pil_img.width < 200 or pil_img.height < 200:
                    continue
                
                # Convert to RGB if needed
                if pil_img.mode != 'RGB':
                    pil_img = pil_img.convert('RGB')
                
                # Resize for YOLO (in memory)
                MAX_SIZE = (1000, 1000)
                if pil_img.width > MAX_SIZE[0] or pil_img.height > MAX_SIZE[1]:
                    pil_img.thumbnail(MAX_SIZE, Image.LANCZOS)
                
                # Convert PIL to OpenCV format (in memory)
                cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
                
                # Run YOLO detection directly on memory image
                image_detections = {class_name: 0 for class_name in CLASS_NAMES}
                results = model(cv_img, verbose=False)
                
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
                                
                                # Draw bounding box on the image
                                x1, y1, x2, y2 = map(int, box.xyxy[0])
                                cv2.rectangle(cv_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                cv2.putText(cv_img, f"{class_name} ({confidence:.2f})", (x1, y1 - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.625, (0, 255, 0), 2)
                
                # Update overall detected objects
                for class_name, count in image_detections.items():
                    detected_objects[class_name].append(count)
                
                # Convert back to PIL for pygame (in memory, with border)
                bordered_cv = cv2.copyMakeBorder(cv_img, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=[0, 0, 0])
                final_pil = Image.fromarray(cv2.cvtColor(bordered_cv, cv2.COLOR_BGR2RGB))
                processed_images.append(final_pil)
                
            except Exception as e:
                print(f"    ❌ Image processing error: {str(e)}")
                continue
        
        # Finalize detection counts
        final_detected_objects = {class_name: max(counts) if counts else 0 for class_name, counts in detected_objects.items()}
        
        # Handle mutually exclusive items
        final_detected_objects = self.handle_mutually_exclusive_items_vinted(final_detected_objects, confidences)
        
        # Game deduplication (Vinted specific)
        vinted_game_classes = [
            '1_2_switch', 'animal_crossing', 'arceus_p', 'bow_z', 'bros_deluxe_m', 'crash_sand',
            'dance', 'diamond_p', 'evee', 'fifa_23', 'fifa_24', 'gta', 'just_dance', 'kart_m', 'kirby',
            'lets_go_p', 'links_z', 'luigis', 'mario_maker_2', 'mario_sonic', 'mario_tennis', 'minecraft',
            'minecraft_dungeons', 'minecraft_story', 'miscellanious_sonic', 'odyssey_m', 'other_mario',
            'party_m', 'rocket_league', 'scarlet_p', 'shield_p', 'shining_p', 'skywards_z', 'smash_bros',
            'snap_p', 'splatoon_2', 'splatoon_3', 'super_m_party', 'super_mario_3d', 'switch_sports',
            'sword_p', 'tears_z', 'violet_p'
        ]
        
        for game_class in vinted_game_classes:
            if final_detected_objects.get(game_class, 0) > 1:
                final_detected_objects[game_class] = 1
        
        # Price threshold filtering
        try:
            listing_price = getattr(self, 'current_listing_price_float', 0.0)
            if listing_price > 0 and listing_price < PRICE_THRESHOLD:
                for switch_class in NINTENDO_SWITCH_CLASSES:
                    if final_detected_objects.get(switch_class, 0) > 0:
                        final_detected_objects[switch_class] = 0
        except:
            pass
        
        return final_detected_objects, processed_images


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
        MODIFIED: Always get current driver from manager
        driver parameter is IGNORED - we use manager
        """
        print(f"🔄 SCRAPING: Using driver manager for all scraping operations")
        global suitable_listings, current_listing_index
        
        # CRITICAL: Ignore passed driver parameter - always use manager
        print(f"⚠️ SCRAPING: Ignoring passed driver parameter - using driver manager")
        
        # Clear scanned IDs file
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

        # Load YOLO Model
        print("🧠 Model already loaded in __init__")
        model = self.model
        
        if not model:
            print("❌ No model available for detection")
            return

        # Load previously scanned listing IDs
        scanned_ids = self.load_scanned_vinted_ids()
        print(f"📚 Loaded {len(scanned_ids)} previously scanned listing IDs")

        page = 1
        overall_listing_counter = 0
        refresh_cycle = 1
        is_first_refresh = True
        cycles_since_restart = 0

        # Main scanning loop
        while True:
            # CRITICAL: Get current driver from manager at start of each cycle
            current_driver = self.driver_manager.get_driver()
            
            if not current_driver or not self.driver_manager.is_ready():
                print("❌ SCRAPING: No valid driver in manager, attempting to prepare new driver...")
                self.prepare_next_vm_driver()
                current_driver = self.driver_manager.get_driver()
                
                if not current_driver:
                    print("❌ SCRAPING: Failed to get valid driver from manager, exiting...")
                    break
            
            driver_session = self.driver_manager.get_session_id()
            current_time = time.time()
            runtime_seconds = current_time - self.program_start_time
            runtime_formatted = self.format_runtime(runtime_seconds)
            
            print(f"\n{'='*60}")
            print(f"🔍 STARTING REFRESH CYCLE {refresh_cycle}")
            print(f"🔄 Cycles since last driver restart: {cycles_since_restart}")
            print(f"⏰ Time since start: {runtime_formatted}")
            print(f"🚗 Current driver session: {driver_session}")
            print(f"{'='*60}")
            
            cycle_listing_counter = 0
            found_already_scanned = False
            page = 1
            
            while True:  # Page loop
                # CRITICAL: Refresh driver reference from manager for each page
                current_driver = self.driver_manager.get_driver()
                
                if not current_driver or not self.driver_manager.is_ready():
                    print("⚠️ SCRAPING: Driver became invalid during page processing")
                    print("🔄 SCRAPING: Attempting to get fresh driver from manager...")
                    self.prepare_next_vm_driver()
                    current_driver = self.driver_manager.get_driver()
                    
                    if not current_driver:
                        print("❌ SCRAPING: Cannot get valid driver, breaking page loop")
                        break
                    else:
                        print(f"✅ SCRAPING: Got fresh driver (Session: {self.driver_manager.get_session_id()})")
                
                current_driver.set_window_size(800, 600)
                
                try:
                    WebDriverWait(current_driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.feed-grid"))
                    )
                except TimeoutException:
                    print("⚠️ Timeout waiting for page to load - moving to next cycle")
                    break

                # Get listing URLs
                try:
                    els = current_driver.find_elements(By.CSS_SELECTOR, "a.new-item-box__overlay")
                    urls = [e.get_attribute("href") for e in els if e.get_attribute("href")]
                except Exception as url_error:
                    print(f"❌ Error getting listing URLs: {url_error}")
                    break
                
                if not urls:
                    print(f"📄 No listings found on page {page} - moving to next cycle")
                    break

                print(f"📄 Processing page {page} with {len(urls)} listings")

                for idx, url in enumerate(urls, start=1):
                    cycle_listing_counter += 1
                    
                    print(f"[Cycle {refresh_cycle} · Page {page} · Item {idx}/{len(urls)}] #{overall_listing_counter}")
                    
                    # Check for duplicate
                    listing_id = self.extract_vinted_listing_id(url)
                    
                    if REFRESH_AND_RESCAN and listing_id:
                        if listing_id in scanned_ids:
                            print(f"🔁 DUPLICATE DETECTED: Listing ID {listing_id} already scanned")
                            print(f"🔄 Initiating refresh and rescan process...")
                            found_already_scanned = True
                            break
                    
                    # Check max listings per cycle
                    if REFRESH_AND_RESCAN and cycle_listing_counter > MAX_LISTINGS_VINTED_TO_SCAN:
                        print(f"📊 Reached MAX_LISTINGS_VINTED_TO_SCAN ({MAX_LISTINGS_VINTED_TO_SCAN})")
                        print(f"🔄 Initiating refresh cycle...")
                        break

                    overall_listing_counter += 1

                    # CRITICAL: Get fresh driver from manager before opening tab
                    current_driver = self.driver_manager.get_driver()
                    
                    if not current_driver or not self.driver_manager.is_ready():
                        print("⚠️ SCRAPING: Driver invalid before opening tab, getting fresh driver...")
                        self.prepare_next_vm_driver()
                        current_driver = self.driver_manager.get_driver()
                        
                        if not current_driver:
                            print("❌ SCRAPING: Cannot get valid driver, skipping listing")
                            continue
                        else:
                            print(f"✅ SCRAPING: Got fresh driver (Session: {self.driver_manager.get_session_id()})")

                    # Process the listing
                    try:
                        current_driver.execute_script("window.open();")
                        current_driver.switch_to.window(current_driver.window_handles[-1])
                        current_driver.get(url)
                    except Exception as tab_error:
                        print(f"❌ Error opening listing tab: {tab_error}")
                        continue

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
