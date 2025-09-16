# Continuation from line 8801
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