# Continuation from line 8801
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
                    
            # Start Flask app in separate thread.
            flask_thread = threading.Thread(target=self.run_flask_app)
            flask_thread.daemon = True
            flask_thread.start()
            
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
                        
                        # MODIFIED: Use a simulation method when actual buying isn't possible
                        try:
                            self.process_single_listing_with_driver(TEST_BOOKMARK_BUYING_URL, driver_num, driver)
                        except Exception as buying_error:
                            print(f"⚠️ BUYING: Normal buying process failed: {buying_error}")
                            print("🧪 BUYING: Switching to test simulation mode...")
                            
                            # Simulate the buying process steps for testing
                            self._simulate_buying_process_for_test(driver, driver_num, TEST_BOOKMARK_BUYING_URL)
                        
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
            
            # Initialize all required global variables for proper operation
            suitable_listings = []
            current_listing_index = 0
            recent_listings = {'listings': [], 'current_index': 0}
            
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
            
            try:
                # Start the bookmark process
                success = self.bookmark_driver(BOOKMARK_TEST_URL, BOOKMARK_TEST_USERNAME)
                
                if success:
                    print("✅ BOOKMARK TEST SUCCESSFUL")
                    
                    # STAY ALIVE and wait for monitoring to complete
                    print("⏳ STAYING ALIVE: Waiting for monitoring thread to complete...")
                    
                    # Wait for the monitoring thread to finish
                    while self.monitoring_threads_active.is_set():
                        time.sleep(1)
                        print("🔍 MONITORING: Still active, waiting...")
                    
                    print("✅ MONITORING: Complete - all threads finished")
                    
                else:
                    print("❌ BOOKMARK TEST FAILED")
                
            except KeyboardInterrupt:
                print("\n🛑 BOOKMARK TEST: Stopped by user")
                # Force cleanup if user interrupts
                self.cleanup_all_cycling_bookmark_drivers()
            
            except Exception as e:
                print(f"❌ BOOKMARK TEST ERROR: {e}")
                import traceback
                traceback.print_exc()
            
            finally:
                # Final cleanup
                print("🧹 FINAL CLEANUP: Closing any remaining drivers...")
                self.cleanup_all_cycling_bookmark_drivers()
                self.cleanup_all_buying_drivers()
                self.cleanup_persistent_buying_driver()
                self.cleanup_persistent_bookmark_driver()
            
            # Only exit after monitoring is truly complete
            print("🧪 BOOKMARK TEST MODE COMPLETE - EXITING")
            sys.exit(0)

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
        #pygame_thread = threading.Thread(target=self.run_pygame_window)
        #pygame_thread.start()
        
        # NEW: Start thread monitoring system


        
        # NEW: Main scraping driver thread - THIS IS THE KEY CHANGE
        def main_scraping_driver():
            """Main scraping driver function that runs in its own thread"""
            print("🚀 SCRAPING THREAD: Starting main scraping driver thread")
            
            # Clear download folder and start scraping
            self.clear_download_folder()
            driver = self.setup_driver()
            
            if driver is None:
                print("❌ SCRAPING THREAD: Failed to setup main driver")
                return
                
            try:
                print("🔍 SCRAPING THREAD: Setting up persistent buying driver...")
                self.setup_persistent_buying_driver()
                
                print("🚀 SCRAPING THREAD: Starting Vinted search with refresh...")
                self.search_vinted_with_refresh(driver, SEARCH_QUERY)
                
            except Exception as scraping_error:
                print(f"❌ SCRAPING THREAD ERROR: {scraping_error}")
                import traceback
                traceback.print_exc()
                
            finally:
                print("🧹 SCRAPING THREAD: Cleaning up...")
                try:
                    driver.quit()
                    print("✅ SCRAPING THREAD: Main driver closed")
                except:
                    print("⚠️ SCRAPING THREAD: Error closing main driver")
                    
                # Clean up all other drivers and resources
                pygame.quit()
                self.cleanup_persistent_buying_driver()
                self.cleanup_all_buying_drivers()
                self.cleanup_purchase_unsuccessful_monitoring()
                self.cleanup_all_cycling_bookmark_drivers()  # Clean up bookmark drivers too
                
                time.sleep(2)

                print("🏁 SCRAPING THREAD: Main scraping thread completed")
        
        # Create and start the main scraping thread
        print("🧵 MAIN: Creating main scraping driver thread...")
        scraping_thread = Thread(target=main_scraping_driver, name="Main-Scraping-Thread")
        scraping_thread.daemon = False  # Don't make it daemon so program waits for it
        scraping_thread.start()
        
        print("🧵 MAIN: Main scraping driver thread started")
        print("🧵 MAIN: Main thread will now wait for scraping thread to complete...")
        
        try:
            # Wait for the scraping thread to complete
            scraping_thread.join()
            print("✅ MAIN: Scraping thread completed successfully")
            
        except KeyboardInterrupt:
            print("\n🛑 MAIN: Keyboard interrupt received")
            print("🛑 MAIN: Setting shutdown event...")
            self.shutdown_event.set()
            
            print("⏳ MAIN: Waiting for scraping thread to finish...")
            scraping_thread.join(timeout=30)  # Wait up to 30 seconds
            
            if scraping_thread.is_alive():
                print("⚠️ MAIN: Scraping thread still alive after timeout")
            else:
                print("✅ MAIN: Scraping thread finished cleanly")
        
        except Exception as main_error:
            print(f"❌ MAIN THREAD ERROR: {main_error}")
            self.shutdown_event.set()
            
        finally:
            print("🏁 MAIN: Program ending, final cleanup...")
            # Force cleanup if anything is still running
            self.cleanup_all_buying_drivers()
            self.cleanup_persistent_buying_driver()
            self.cleanup_all_cycling_bookmark_drivers()
            self.cleanup_purchase_unsuccessful_monitoring()
            
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