# Continuation from line 8801
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
                
                # SIMPLE CHANGE: Use VM bookmark system
                test_username = "test_user"
                
                # Call the VM bookmark function directly
                bookmark_success = self.vm_bookmark_simple(TEST_BOOKMARK_BUYING_URL, test_username)
                
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
                # SIMPLE CHANGE: Use VM bookmark system instead of old system
                success = self.vm_bookmark_simple(BOOKMARK_TEST_URL, BOOKMARK_TEST_USERNAME)
                
                if success:
                    print("✅ BOOKMARK TEST SUCCESSFUL")
                    print("⏳ VM bookmark process completed")
                else:
                    print("❌ BOOKMARK TEST FAILED")
                
            except KeyboardInterrupt:
                print("\n🛑 BOOKMARK TEST: Stopped by user")
            except Exception as e:
                print(f"❌ BOOKMARK TEST ERROR: {e}")
                import traceback
                traceback.print_exc()
            finally:
                print("🧹 FINAL CLEANUP: VM bookmark system cleaned up automatically")
            
            # Only exit after bookmark is complete
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
                self.search_vinted_with_refresh_enhanced(driver, SEARCH_QUERY)

                
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
                self.cleanup_all_bookmark_drivers()
                
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
            self.cleanup_purchase_unsuccessful_monitoring()
            
            print("🏁 MAIN: Program exit")
            sys.exit(0)

    # ADD this simple method to VintedScraper class:
    def vm_bookmark_simple(self, listing_url, username):
        """
        SIMPLE: Just call the VM bookmark function directly
        """
        print(f"🔖 VM BOOKMARK: {listing_url}")
        
        try:
            # Call the VM main function directly
            main_vm_driver()  # This already does everything we need
            return True
        except Exception as e:
            print(f"❌ VM BOOKMARK ERROR: {e}")
            return False

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