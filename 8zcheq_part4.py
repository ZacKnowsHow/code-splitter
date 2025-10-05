# Continuation from line 6601

                        # Download and detect images
                        detected_objects, processed_images = self.download_and_detect_images_in_memory(current_driver, model)
                        
                        # Print detected objects
                        detected_classes = [cls for cls, count in detected_objects.items() if count > 0]
                        if detected_classes:
                            for cls in sorted(detected_classes):
                                print(f"  • {cls}: {detected_objects[cls]}")

                        # Process listing
                        self.process_vinted_listing(details, detected_objects, processed_images, overall_listing_counter, url)

                        # Mark as scanned
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
                        if listing_id:
                            scanned_ids.add(listing_id)
                            self.save_vinted_listing_id(listing_id)

                    finally:
                        # Close tab safely
                        try:
                            # Get fresh driver reference
                            current_driver = self.driver_manager.get_driver()
                            
                            if current_driver and self.driver_manager.is_ready():
                                if len(current_driver.window_handles) > 1:
                                    current_driver.close()
                                    current_driver.switch_to.window(current_driver.window_handles[0])
                                else:
                                    print("⚠️ Only one window open, not closing")
                            else:
                                print("⚠️ Driver no longer valid, skipping tab close")
                        except Exception as close_error:
                            print(f"⚠️ Error closing tab: {close_error}")
                            try:
                                if current_driver and len(current_driver.window_handles) > 0:
                                    current_driver.switch_to.window(current_driver.window_handles[0])
                            except:
                                print("⚠️ Could not recover window state")

                # Check if we need to break out of page loop
                if found_already_scanned or (REFRESH_AND_RESCAN and cycle_listing_counter > MAX_LISTINGS_VINTED_TO_SCAN):
                    break

                # Pagination
                try:
                    current_driver = self.driver_manager.get_driver()
                    
                    if not current_driver or not self.driver_manager.is_ready():
                        print("⚠️ Driver invalid, cannot paginate")
                        break
                    
                    nxt = current_driver.find_element(By.CSS_SELECTOR, "a[data-testid='pagination-arrow-right']")
                    current_driver.execute_script("arguments[0].click();", nxt)
                    page += 1
                    time.sleep(2)
                except NoSuchElementException:
                    print("📄 No more pages available - moving to next cycle")
                    break
                except Exception as pagination_error:
                    print(f"❌ Pagination error: {pagination_error}")
                    break

            # End of page loop - refresh
            if not REFRESH_AND_RESCAN:
                print("🏁 REFRESH_AND_RESCAN disabled - ending scan")
                break
            
            # Get fresh driver for refresh
            current_driver = self.driver_manager.get_driver()
            
            if not current_driver or not self.driver_manager.is_ready():
                print("❌ No valid driver for refresh, exiting...")
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
            cycles_since_restart += 1
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
        Test function to cycle through TEST_SUITABLE_URLS and display each on pygame
        FIXED: Uses driver manager and updated workflow
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
        
        # Use the model that was already loaded in __init__
        model = self.model
        
        if not model:
            print("❌ TEST: No YOLO model available")
            return
        
        print("✅ TEST: Using pre-loaded YOLO model")
        
        # Process each URL in TEST_SUITABLE_URLS
        for idx, url in enumerate(TEST_SUITABLE_URLS, 1):
            print(f"\n{'='*60}")
            print(f"🔍 TEST: Processing URL {idx}/{len(TEST_SUITABLE_URLS)}")
            print(f"🔗 URL: {url}")
            print(f"{'='*60}")
            
            try:
                # Get current driver from manager
                current_driver = self.driver_manager.get_driver()
                
                if not current_driver or not self.driver_manager.is_ready():
                    print("❌ TEST: No driver available from manager")
                    print("🔄 TEST: Attempting to prepare driver...")
                    self.prepare_next_vm_driver()
                    current_driver = self.driver_manager.get_driver()
                    
                    if not current_driver:
                        print("❌ TEST: Failed to get driver, skipping this URL")
                        continue
                
                # Open new tab
                print("📑 TEST: Opening new tab...")
                current_driver.execute_script("window.open();")
                current_driver.switch_to.window(current_driver.window_handles[-1])
                current_driver.get(url)
                print("✅ TEST: Navigated to URL")
                
                # Wait for page to load
                try:
                    WebDriverWait(current_driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "h1.web_ui__Text__title"))
                    )
                    print("✅ TEST: Page loaded")
                except TimeoutException:
                    print("⚠️ TEST: Page load timeout, continuing anyway...")
                
                # Scrape details
                print("📋 TEST: Scraping listing details...")
                details = self.scrape_item_details(current_driver)
                print(f"✅ TEST: Details scraped - Title: {details.get('title', 'N/A')[:50]}")
                
                # Download and detect images IN MEMORY (using optimized method)
                print("🖼️ TEST: Detecting objects in images...")
                detected_objects, processed_images = self.download_and_detect_images_in_memory(current_driver, model)
                
                # Print detected objects
                detected_classes = [cls for cls, count in detected_objects.items() if count > 0]
                if detected_classes:
                    print(f"✅ TEST: Detected {len(detected_classes)} object types:")
                    for cls in sorted(detected_classes):
                        print(f"  • {cls}: {detected_objects[cls]}")
                else:
                    print("⚠️ TEST: No objects detected")
                
                # Process for pygame display (no booking logic, force show all)
                print("📊 TEST: Processing listing for display...")
                self.process_vinted_listing(details, detected_objects, processed_images, idx, url)
                
                print(f"✅ TEST: Listing {idx} processed and added to pygame")
                
                # Clean up processed images
                self.cleanup_processed_images(processed_images)
                
            except Exception as e:
                print(f"❌ TEST: Error processing URL {idx}: {e}")
                import traceback
                traceback.print_exc()
            
            finally:
                # Close tab and return to main
                try:
                    current_driver = self.driver_manager.get_driver()
                    if current_driver and len(current_driver.window_handles) > 1:
                        current_driver.close()
                    if current_driver and len(current_driver.window_handles) > 0:
                        current_driver.switch_to.window(current_driver.window_handles[0])
                    print(f"✅ TEST: Tab closed, returned to main window")
                except Exception as cleanup_error:
                    print(f"⚠️ TEST: Cleanup error: {cleanup_error}")
        
        # Restore original settings
        VINTED_SHOW_ALL_LISTINGS = original_show_all
        bookmark_listings = original_bookmark
        
        print(f"\n{'='*60}")
        print(f"✅ TEST MODE COMPLETE")
        print(f"📊 Processed {len(TEST_SUITABLE_URLS)} URLs")
        print(f"📊 Total listings in pygame: {len(suitable_listings)}")
        print(f"{'='*60}")


    # Add this new method to your VintedScraper class:
    def _simulate_buying_process_for_test(self, driver, driver_num, url):
        """
        Simulate the buying process for test mode when no actual listing is available
        This tests the buy button clicking logic without requiring a real purchasable item
        """
        print(f"🧪 SIMULATION: Starting simulated buying process for driver {driver_num}")
        
        try:
            # Open new tab
            driver.execute_script("window.open('');")
            new_tab = driver.window_handles[-1]
            driver.switch_to.window(new_tab)
            print(f"✅ SIMULATION: New tab opened")
            
            # Navigate to URL
            driver.get(url)
            print(f"✅ SIMULATION: Navigated to {url}")
            
            # Wait for page to load
            WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print(f"✅ SIMULATION: Page loaded")
            
            # Look for buy button (even if not clickable)
            buy_selectors = [
                'button[data-testid="item-buy-button"]',
                'button.web_ui__Button__button.web_ui__Button__filled.web_ui__Button__default.web_ui__Button__primary.web_ui__Button__truncated',
                '//button[@data-testid="item-buy-button"]',
                '//button[contains(@class, "web_ui__Button__primary")]//span[text()="Buy now"]'
            ]
            
            buy_button_found = False
            for selector in buy_selectors:
                try:
                    if selector.startswith('//'):
                        buy_button = driver.find_element(By.XPATH, selector)
                    else:
                        buy_button = driver.find_element(By.CSS_SELECTOR, selector)
                    
                    print(f"✅ SIMULATION: Found buy button with selector: {selector}")
                    buy_button_found = True
                    
                    # Try to click it (even if it fails, that's expected)
                    try:
                        buy_button.click()
                        print(f"✅ SIMULATION: Buy button clicked successfully")
                    except Exception as click_error:
                        print(f"⚠️ SIMULATION: Buy button click failed (expected): {click_error}")
                    
                    break
                    
                except NoSuchElementException:
                    continue
            
            if not buy_button_found:
                print(f"⚠️ SIMULATION: No buy button found (item may be sold/removed)")
                print(f"🧪 SIMULATION: Simulating buy button click anyway for test purposes...")
            
            # Simulate waiting for checkout page (even if it doesn't load)
            print(f"🧪 SIMULATION: Waiting for checkout page simulation...")
            time.sleep(2)
            
            # Look for pay button (simulate the buying logic)
            pay_selectors = [
                'button[data-testid="single-checkout-order-summary-purchase-button"]',
                'button[data-testid="single-checkout-order-summary-purchase-button"].web_ui__Button__primary',
            ]
            
            pay_button_found = False
            for selector in pay_selectors:
                try:
                    pay_button = driver.find_element(By.CSS_SELECTOR, selector)
                    print(f"✅ SIMULATION: Found pay button with selector: {selector}")
                    pay_button_found = True
                    
                    # Simulate clicking pay button multiple times (the actual buying logic)
                    for attempt in range(3):
                        print(f"🧪 SIMULATION: Simulated pay button click attempt {attempt + 1}")
                        try:
                            pay_button.click()
                            print(f"✅ SIMULATION: Pay button click attempt {attempt + 1} simulated")
                        except Exception as pay_click_error:
                            print(f"⚠️ SIMULATION: Pay button click {attempt + 1} failed (expected): {pay_click_error}")
                        
                        # Simulate the wait time between clicks
                        time.sleep(buying_driver_click_pay_wait_time)
                        
                    break
                    
                except NoSuchElementException:
                    continue
            
            if not pay_button_found:
                print(f"⚠️ SIMULATION: No pay button found (checkout page didn't load)")
                print(f"🧪 SIMULATION: This is expected behavior for test URLs without actual items")
            
            # Simulate completion
            print(f"✅ SIMULATION: Buying process simulation completed")
            print(f"🧪 SIMULATION: In real scenario, this would continue until purchase success/failure")
            
        except Exception as simulation_error:
            print(f"❌ SIMULATION ERROR: {simulation_error}")
        
        finally:
            # Clean up the tab
            try:
                driver.close()
                if len(driver.window_handles) > 0:
                    driver.switch_to.window(driver.window_handles[0])
                print(f"✅ SIMULATION: Cleanup completed")
            except Exception as cleanup_error:
                print(f"⚠️ SIMULATION CLEANUP: {cleanup_error}")
            
            # Release the driver
            self.release_driver(driver_num)
            print(f"✅ SIMULATION: Driver {driver_num} released")

    def run(self):
        """Modified run method to use driver manager"""
        global suitable_listings, current_listing_index, recent_listings, current_listing_title, current_listing_price
        global current_listing_description, current_listing_join_date, current_detected_items, current_profit
        global current_listing_images, current_listing_url, current_suitability, current_expected_revenue
        global current_bookmark_status
        
        # Check for test modes
        if TEST_WHETHER_SUITABLE:
            print("🧪 TEST_WHETHER_SUITABLE = True - Starting test mode")
            
            # Initialize globals for test mode
            suitable_listings = []
            current_listing_index = 0
            recent_listings = {'listings': [], 'current_index': 0}
            
            # Get driver from manager (should be already initialized in __init__)
            driver = self.driver_manager.get_driver()
            
            if not driver or not self.driver_manager.is_ready():
                print("❌ TEST: No driver available, attempting to prepare one...")
                self.prepare_next_vm_driver()
                driver = self.driver_manager.get_driver()
            
            if driver:
                print("✅ TEST: Driver ready, starting test...")
                
                # Start pygame in background thread for test mode
                pygame_thread = threading.Thread(target=self.run_pygame_window)
                pygame_thread.start()
                
                # Give pygame time to initialize
                time.sleep(2)
                
                # Run test mode
                self.test_suitable_urls_mode(driver)
                
                # Keep pygame window open
                print("✅ TEST: Test complete, pygame window will remain open")
                print("Press ESC in pygame window to exit")
                
                # Wait for pygame thread
                try:
                    pygame_thread.join()
                except KeyboardInterrupt:
                    print("\n🛑 TEST: Keyboard interrupt received")
            else:
                print("❌ TEST: Could not get driver, exiting test mode")
            
            return
            
        if TEST_NUMBER_OF_LISTINGS:
            print("🧪 TEST_NUMBER_OF_LISTINGS = True - Starting URL collection test")
            
            # For this test mode, we need a simple driver (not from manager)
            driver = self.setup_driver()  # Local driver for this specific test
            if driver:
                self.test_url_collection_mode(driver, SEARCH_QUERY)
                driver.quit()
            return
        
        # Rest of normal run() method continues...
        # Initialize ALL global variables properly
        suitable_listings = []
        current_listing_index = 0
        
        # Initialize recent_listings for website navigation
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
        current_seller_reviews = "No reviews yet"
        current_bookmark_status = "Not attempted"
        
        # Initialize pygame display with default values
        self.update_listing_details("", "", "", "0", 0, 0, {}, [], {}, bookmark_status="Not attempted")
        
        # Start Flask app in separate thread
        flask_thread = threading.Thread(target=self.run_flask_app)
        flask_thread.daemon = True
        flask_thread.start()
        
        # Main scraping driver thread
        def main_scraping_driver():
            """Main scraping driver function using driver manager"""
            print("🚀 SCRAPING: Starting scraping using driver manager")
            
            self.clear_download_folder()
            
            # Get initial driver from manager
            driver = self.driver_manager.get_driver()
            
            if driver is None:
                print("❌ SCRAPING: No driver available in manager")
                return
            
            driver_session = self.driver_manager.get_session_id()
            print(f"🚀 SCRAPING: Starting with driver (Session: {driver_session})")
            
            try:
                print("🚀 SCRAPING THREAD: Starting Vinted search with refresh...")
                # Pass driver but it will be ignored - manager is used
                self.search_vinted_with_refresh(driver, SEARCH_QUERY)
                
            except Exception as scraping_error:
                print(f"❌ SCRAPING THREAD ERROR: {scraping_error}")
                import traceback
                traceback.print_exc()
                
            finally:
                print("🧹 SCRAPING THREAD: Cleaning up...")
                # Close driver through manager
                self.driver_manager.close_driver()
                print("✅ SCRAPING THREAD: Driver closed via manager")
                pygame.quit()
                time.sleep(2)
                print("🏁 SCRAPING THREAD: Main scraping thread completed")
        
        # Create and start the main scraping thread
        print("🧵 MAIN: Creating main scraping driver thread...")
        scraping_thread = Thread(target=main_scraping_driver, name="Scraping-Thread")
        scraping_thread.daemon = False
        scraping_thread.start()

        # Start pygame window
        pygame_thread = threading.Thread(target=self.run_pygame_window)
        pygame_thread.start()
        
        print("🧵 MAIN: Scraping driver thread started")
        print("🧵 MAIN: Main thread will now wait for scraping thread to complete...")
        
        try:
            scraping_thread.join()
            print("✅ MAIN: Scraping thread completed successfully")
            
        except KeyboardInterrupt:
            print("\n🛑 MAIN: Keyboard interrupt received")
            scraping_thread.join(timeout=30)
            
        except Exception as main_error:
            print(f"❌ MAIN THREAD ERROR: {main_error}")
            
        finally:
            print("🏁 MAIN: Program ending, final cleanup...")
            self.driver_manager.close_driver()
            print("🏁 MAIN: Program exit")
            sys.exit(0)

if __name__ == "__main__":
    if VM_DRIVER_USE:
        print("VM_DRIVER_USE = True - Running VM driver script instead of main scraper")
        if not HAS_PYAUDIO:
            print("WARNING: pyaudiowpatch not available - audio features may not work")
            print("Install with: pip install PyAudioWPatch")
        main_vm_driver()
    else:
        print("VM_DRIVER_USE = False - Running main Vinted scraper")
        scraper = VintedScraper()
        globals()['vinted_scraper_instance'] = scraper
        scraper.run()