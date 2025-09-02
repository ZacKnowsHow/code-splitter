# Continuation from line 6601
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
        
        def thread_monitor():
            while not self.shutdown_event.is_set():
                self.monitor_driver_threads()
                time.sleep(5)

        monitor_thread = Thread(target=thread_monitor, name="Thread-Monitor")
        monitor_thread.daemon = True
        monitor_thread.start()

        print("🧵 MONITOR: Thread monitoring started")
        # Clear download folder and start scraping
        self.clear_download_folder()
        driver = self.setup_driver()
        self.setup_persistent_buying_driver()
        try:
            self.search_vinted_with_refresh(driver, SEARCH_QUERY)
        finally:
            driver.quit()
            pygame.quit()
            self.cleanup_persistent_buying_driver()
            self.cleanup_all_buying_drivers()
            self.cleanup_purchase_unsuccessful_monitoring()  # NEW: Clean up buying drivers
            time.sleep(2)
        
            active_count = self.get_active_thread_count()
            if active_count > 0:
                print(f"⚠️ WARNING: {active_count} threads still active after cleanup")
            else:
                print("✅ SUCCESS: All threads cleaned up successfully")
            
            sys.exit(0)

if __name__ == "__main__":

    scraper = VintedScraper()

    globals()['vinted_scraper_instance'] = scraper
        
    scraper.run()