# Continuation from line 4401
            if captcha_result == "no_captcha":
                print(f"✅ PREPARE: {driver_name} ready - no captcha needed")
            elif captcha_result == True:
                print(f"🎧 PREPARE: {driver_name} captcha solved")
            else:
                print(f"⚠️ PREPARE: {driver_name} captcha handling failed, continuing anyway")
            
            # STEP 8: Store the driver and mark as ready
            with self.bookmark_system_lock:
                self.bookmark_drivers[driver_index] = fresh_driver
                self.bookmark_driver_status[driver_index] = 'ready'
                ready_count = self._get_ready_driver_count()  # ADD THIS LINE
                print(f"📊 DRIVER COUNT: Now have {ready_count}/5 ready drivers")  # ADD THIS LINE
                
            print(f"✅ PREPARE: {driver_name} is now ready for bookmarking")
            
        except Exception as prepare_error:
            print(f"❌ PREPARE ERROR: {driver_name} preparation failed: {prepare_error}")
            self.bookmark_driver_status[driver_index] = 'error'

    def cleanup_all_session_monitoring(self):
        """
        Clean up all session monitoring threads when program exits
        """
        print("🧹 SESSION CLEANUP: Stopping all session monitoring threads...")
        
        # Stop all active monitoring
        for driver_index in list(self.session_monitoring_active.keys()):
            self.session_monitoring_active[driver_index] = False
        
        # Wait for threads to finish (with timeout)
        active_threads = []
        for driver_index, thread in self.session_monitoring_threads.items():
            if thread and thread.is_alive():
                active_threads.append((driver_index + 1, thread))
        
        if active_threads:
            print(f"🧹 SESSION CLEANUP: Waiting for {len(active_threads)} monitoring threads...")
            
            for driver_num, thread in active_threads:
                thread.join(timeout=5)  # 5 second timeout per thread
                if thread.is_alive():
                    print(f"⚠️ SESSION CLEANUP: Monitor-{driver_num} still running after timeout")
                else:
                    print(f"✅ SESSION CLEANUP: Monitor-{driver_num} stopped cleanly")
        
        # Clear all references
        self.session_monitoring_threads.clear()
        self.session_monitoring_active.clear()
        
        print("✅ SESSION CLEANUP: All session monitoring cleaned up")

    def _create_vm_bookmark_driver(self, config, driver_index):
        """
        MODIFIED: Create a bookmark driver and start session monitoring
        """
        vm_ip_address = "192.168.56.101"  # Your VM IP
        
        try:
            chrome_options = ChromeOptions()
            chrome_options.add_argument(f"--user-data-dir={config['user_data_dir']}")
            chrome_options.add_argument(f"--profile-directory={config['profile_directory']}")
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument('--force-device-scale-factor=1')
            chrome_options.add_argument('--high-dpi-support=1')
            chrome_options.add_argument(f'--remote-debugging-port={9230 + driver_index}')
            chrome_options.add_argument('--remote-allow-origins=*')
            chrome_options.add_argument('--disable-features=VizDisplayCompositor')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--allow-running-insecure-content')
            
            # Create driver connection to VM
            driver = webdriver.Remote(
                command_executor=f'http://{vm_ip_address}:4444',
                options=chrome_options
            )
            
            # Apply stealth modifications
            stealth_script = """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
            window.chrome = {runtime: {}};
            Object.defineProperty(navigator, 'permissions', {get: () => ({query: () => Promise.resolve({state: 'granted'})})});
            """
            driver.execute_script(stealth_script)
            
            print(f"✅ CREATE: Driver {driver_index + 1} connected to VM successfully")
            
            # NEW: Start session monitoring for this driver
            driver_name = config['driver_name']
            self._start_session_monitoring(driver, driver_index, driver_name)
            
            return driver
            
        except Exception as e:
            print(f"❌ CREATE: Failed to create VM driver {driver_index + 1}: {e}")
            return None


    def _handle_cookie_consent(self, driver, driver_name):
        """Handle cookie consent for the driver"""
        try:
            cookie_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            cookie_button.click()
            print(f"🍪 COOKIES: Accepted for {driver_name}")
            time.sleep(random.uniform(1, 2))
        except TimeoutException:
            print(f"🍪 COOKIES: No consent dialog for {driver_name}")

    def cleanup_all_bookmark_threads(self):
        """
        Clean up all bookmark driver threads when program exits
        """
        print("🧹 CLEANUP: Stopping all bookmark driver threads...")
        
        active_threads = []
        for driver_index, thread in self.bookmark_driver_threads.items():
            if thread and thread.is_alive():
                active_threads.append((driver_index + 1, thread))
        
        if active_threads:
            print(f"🧹 CLEANUP: Found {len(active_threads)} active bookmark threads")
            
            # Give threads 10 seconds to finish naturally
            print("⏳ CLEANUP: Waiting 10 seconds for threads to complete...")
            for driver_num, thread in active_threads:
                thread.join(timeout=10)
                if thread.is_alive():
                    print(f"⚠️ CLEANUP: BookmarkDriver-{driver_num} still running after timeout")
                else:
                    print(f"✅ CLEANUP: BookmarkDriver-{driver_num} completed")
        
        print("✅ CLEANUP: Bookmark thread cleanup completed")
    

    def cleanup_all_bookmark_drivers(self):
        """
        MODIFIED: Clean up all bookmark drivers and session monitoring when program exits
        """
        print("🧹 CLEANUP: Stopping all bookmark drivers and session monitoring...")
        
        # First stop all session monitoring
        self.cleanup_all_session_monitoring()
        
        # Then clean up drivers as before
        with self.bookmark_system_lock:
            for driver_index in range(5):
                if driver_index in self.bookmark_drivers:
                    try:
                        driver_name = self.bookmark_driver_configs[driver_index]['driver_name']
                        print(f"🗑️ CLEANUP: Closing {driver_name}")
                        
                        self.bookmark_drivers[driver_index].quit()
                        del self.bookmark_drivers[driver_index]
                        
                        print(f"✅ CLEANUP: {driver_name} closed")
                    except Exception as e:
                        print(f"⚠️ CLEANUP: Error closing driver {driver_index + 1}: {e}")
            
            # Clear statuses
            for i in range(5):
                self.bookmark_driver_status[i] = 'not_created'
        
        print("✅ CLEANUP: All bookmark drivers and session monitoring cleaned up")


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
                                        pay_clicked = True
                                        print(f"✅ DRIVER {driver_num}: Pay clicked using force method")
                                    except Exception as final_error:
                                        print(f"❌ DRIVER {driver_num}: All pay click methods failed: {final_error}")
                            
                            if pay_clicked:
                                print(f"💳 DRIVER {driver_num}: Payment initiated successfully!")
                                
                                # Continue with existing purchase logic
                                self.handle_post_payment_logic(driver, driver_num, url)
                            
                            break  # Exit monitoring loop
                            
                        except Exception as click_error:
                            print(f"❌ DRIVER {driver_num}: Error clicking pay button: {click_error}")
                            break
                
                # Sleep briefly before next check
                time.sleep(check_interval)
        
        except Exception as monitoring_error:
            print(f"❌ DRIVER {driver_num}: Monitoring error: {monitoring_error}")
        
        finally:
            # Clean up monitoring entry
            if url in purchase_unsuccessful_detected_urls:
                del purchase_unsuccessful_detected_urls[url]
            
            print(f"🧹 DRIVER {driver_num}: Monitoring cleanup completed")


    def process_single_listing_with_driver_modified(self, url, driver_num, driver):
        """
        MODIFIED: Process listing that immediately navigates to buy page and waits for "Purchase unsuccessful"
        """
        print(f"🔥 DRIVER {driver_num}: Starting MODIFIED processing of {url[:50]}...")
        
        try:
            # Driver health check
            try:
                current_url = driver.current_url
                print(f"✅ DRIVER {driver_num}: Driver alive")
            except Exception as e:
                print(f"❌ DRIVER {driver_num}: Driver is dead: {str(e)}")
                return
            
            # Open new tab
            try:
                driver.execute_script("window.open('');")
                new_tab = driver.window_handles[-1]
                driver.switch_to.window(new_tab)
                print(f"✅ DRIVER {driver_num}: New tab opened")
            except Exception as e:
                print(f"❌ DRIVER {driver_num}: Failed to open new tab: {str(e)}")
                return
            
            # Navigate to URL
            actual_url = test_purchase_url if test_purchase_not_true else url
            
            navigation_success = False
            for nav_attempt in range(3):
                try:
                    driver.get(actual_url)
                    WebDriverWait(driver, 8).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                    navigation_success = True
                    print(f"✅ DRIVER {driver_num}: Navigation successful")
                    break
                except Exception as nav_error:
                    print(f"❌ DRIVER {driver_num}: Navigation attempt {nav_attempt+1} failed: {str(nav_error)}")
                    if nav_attempt < 2:
                        time.sleep(1)
            
            if not navigation_success:
                print(f"❌ DRIVER {driver_num}: All navigation attempts failed")
                try:
                    driver.close()
                    if len(driver.window_handles) > 0:
                        driver.switch_to.window(driver.window_handles[0])
                except:
                    pass
                return
            
            # Click Buy now button
            buy_button_clicked = False
            buy_selectors = [
                'button[data-testid="item-buy-button"]',
                'button.web_ui__Button__button.web_ui__Button__filled.web_ui__Button__default.web_ui__Button__primary.web_ui__Button__truncated',
                '//button[@data-testid="item-buy-button"]',
                '//button[contains(@class, "web_ui__Button__primary")]//span[text()="Buy now"]'
            ]
            
            for selector in buy_selectors:
                try:
                    if selector.startswith('//'):
                        buy_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        buy_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    
                    # Try multiple click methods
                    for click_method in ['standard', 'javascript']:
                        try:
                            if click_method == 'standard':
                                buy_button.click()
                            else:
                                driver.execute_script("arguments[0].click();", buy_button)
                            
                            buy_button_clicked = True
                            print(f"✅ DRIVER {driver_num}: Buy button clicked using {click_method}")
                            break
                        except Exception as click_error:
                            continue
                    
                    if buy_button_clicked:
                        break
                        
                except Exception as selector_error:
                    continue
            
            if not buy_button_clicked:
                print(f"❌ DRIVER {driver_num}: Could not click buy button - item likely sold")
                try:
                    driver.close()
                    if len(driver.window_handles) > 0:
                        driver.switch_to.window(driver.window_handles[0])
                except:
                    pass
                return
            
            # MODIFIED: Find and store pay button location BUT DON'T CLICK YET
            print(f"🔍 DRIVER {driver_num}: Finding pay button (but not clicking yet)...")
            
            pay_button = None
            pay_selectors = [
                'button[data-testid="single-checkout-order-summary-purchase-button"]',
                '//button[@data-testid="single-checkout-order-summary-purchase-button"]'
            ]
            
            for selector in pay_selectors:
                try:
                    if selector.startswith('//'):
                        pay_button = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, selector))
                        )
                    else:
                        pay_button = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                    
                    print(f"✅ DRIVER {driver_num}: Pay button found and stored")
                    break
                    
                except Exception as selector_error:
                    continue
            
            if not pay_button:
                print(f"❌ DRIVER {driver_num}: Could not find pay button")
                try:
                    driver.close()
                    if len(driver.window_handles) > 0:
                        driver.switch_to.window(driver.window_handles[0])
                except:
                    pass
                return
            
            # MODIFIED: Register this URL for "Purchase unsuccessful" monitoring
            global purchase_unsuccessful_detected_urls
            purchase_unsuccessful_detected_urls[url] = {
                'driver': driver,
                'driver_num': driver_num,
                'pay_button': pay_button,
                'waiting': True,
                'start_time': time.time()
            }
            
            print(f"🔍 DRIVER {driver_num}: Registered for 'Purchase unsuccessful' monitoring")
            print(f"⏱️ DRIVER {driver_num}: Will wait for bookmark driver to detect 'Purchase unsuccessful'")
            
            # Start monitoring thread for this specific URL
            monitoring_thread = threading.Thread(
                target=self.monitor_for_purchase_unsuccessful,
                args=(url, driver, driver_num, pay_button)
            )
            monitoring_thread.daemon = True
            monitoring_thread.start()
            
        except Exception as critical_error:
            print(f"❌ DRIVER {driver_num}: Critical error: {str(critical_error)}")
            # Clean up
            try:
                driver.close()
                if len(driver.window_handles) > 0:
                    driver.switch_to.window(driver.window_handles[0])
            except:
                pass
            self.release_driver(driver_num)

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

            'purchase_unsuccessful': [
                 "//h2[@class='web_uiTexttext web_uiTexttitle web_uiTextleft web_uiTextwarning' and text()='Purchase unsuccessful']",
                "//div[@class='web_uiCelltitle'][@data-testid='conversation-message--status-message--title']//h2[@class='web_uiTexttext web_uiTexttitle web_uiTextleft web_uiTextwarning' and text()='Purchase unsuccessful']",
                "//div[@class='web_uiCellheading']//div[@class='web_uiCelltitle'][@data-testid='conversation-message--status-message--title']//h2[@class='web_uiTexttext web_uiTexttitle web_uiTextleft web_uiTextwarning' and text()='Purchase unsuccessful']",
                "//*[contains(@class, 'web_uiTextwarning') and text()='Purchase unsuccessful']",
                "//*[text()='Purchase unsuccessful']"
            ],
            
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
        MODIFIED: Enhanced button click handler that immediately opens buying driver on "yes"
        """
        print(f"🔘 VINTED BUTTON: Processing {url}")
        
        # Check if already clicked to prevent duplicates
        if url in self.clicked_yes_listings:
            print(f"🔄 VINTED BUTTON: Listing {url} already processed, ignoring")
            return
        
        # Mark as clicked immediately to prevent race conditions
        self.clicked_yes_listings.add(url)
        
        # MODIFIED: Immediately start buying process when user clicks yes
        print(f"🚀 IMMEDIATE: Starting buying process for {url}")
        
        # Get available driver
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            driver_num, driver = self.get_available_driver()
            
            if driver is not None:
                # Successfully got a driver, process in separate thread
                processing_thread = threading.Thread(
                    target=self.process_single_listing_with_driver_modified,
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
