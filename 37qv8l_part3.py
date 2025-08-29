# Continuation from line 4401
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

        # DEBUG: Print final scraped data for seller_reviews and username
        if print_debug:
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
        MODIFIED: Separate logic for pygame and website display - pygame shows all suitable listings with bookmark failure notices
        """
        global suitable_listings, current_listing_index, recent_listings

        # Extract username from details - THIS WAS MISSING!
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

        # SEPARATE logic for pygame and website
        should_add_to_website = False
        should_add_to_pygame = False  # Always true for pygame to show suitable listings
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
            model = YOLO(MODEL_WEIGHTS).cuda()  # Force GPU
            print("✅ YOLO model loaded on GPU")
        else:
            model = YOLO(MODEL_WEIGHTS).cpu()   # Fallback to CPU
            print("⚠️ YOLO model loaded on CPU (no CUDA available)")

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

                    # Process the listing (same as original logic)
                    driver.execute_script("window.open();")
                    driver.switch_to.window(driver.window_handles[-1])
                    driver.get(url)

                    try:
                        listing_start_time = time.time()
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
                
                # Look for Pay button with enhanced selectors
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
                        # Try multiple click methods for pay button
                        pay_clicked = False
                        for click_method in ['standard', 'javascript']:
                            try:
                                if click_method == 'standard':
                                    pay_element.click()
                                else:
                                    self.persistent_bookmark_driver.execute_script("arguments[0].click();", pay_element)
                                
                                log_step(f"pay_button_click_{click_method}", True)
                                pay_clicked = True
                                break
                            except Exception as click_error:
                                log_step(f"pay_button_click_{click_method}", False, str(click_error))
                                continue
                        
                        if pay_clicked:
                            # ⚠️ CRITICAL: Exact 0.25 second wait - DO NOT MODIFY! ⚠️
                            print("🔖 CRITICAL: Waiting exactly 0.25 seconds...")
                            time.sleep(0.25)
                            
                            # ⚠️ CRITICAL: Immediate tab close - DO NOT MODIFY! ⚠️
                            print("🔖 CRITICAL: Closing tab immediately...")
                            self.persistent_bookmark_driver.close()
                            
                            step_log['critical_sequence_completed'] = True
                            log_step("critical_sequence_completed", True, "0.25s wait + tab close")
                            
                            # Calculate timing for the critical sequence
                            bookmark_end_time = time.time()
                            total_elapsed_time = bookmark_end_time - bookmark_start_time
                            log_step("first_sequence_timing", True, f"Completed in {total_elapsed_time:.2f}s")
                            
                            # Switch back to main tab
                            if len(self.persistent_bookmark_driver.window_handles) > 0:
                                self.persistent_bookmark_driver.switch_to.window(self.persistent_bookmark_driver.window_handles[0])
                                log_step("return_to_main_tab", True)
                            
                            log_step("first_sequence_complete", True)
                        else:
                            log_step("pay_button_click_all_failed", False, "All click methods failed")
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