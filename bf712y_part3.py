# Continuation from line 4401
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
        UPDATED: Now includes username collection AND stores price for threshold filtering
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

        # NEW: Calculate and store the total price for threshold filtering
        second_price = self.extract_price(data.get("second_price", "0"))
        postage = self.extract_price(data.get("postage", "0"))
        total_price = second_price + postage
        
        # Store the calculated price for use in object detection
        self.current_listing_price_float = total_price
        
        # DEBUG: Print final scraped data for seller_reviews and username
        if print_debug:
            print(f"DEBUG: Final scraped seller_reviews: '{data.get('seller_reviews')}'")
            print(f"DEBUG: Final scraped username: '{data.get('username')}'")
            print(f"DEBUG: Total price calculated: £{total_price:.2f} (stored for threshold filtering)")
            
        return data

    def clear_download_folder(self):
        if os.path.exists(DOWNLOAD_ROOT):
            shutil.rmtree(DOWNLOAD_ROOT)
        os.makedirs(DOWNLOAD_ROOT, exist_ok=True)

    # FIXED: Updated process_vinted_listing function - key section that handles suitability checking

    def process_vinted_listing_with_vm_bookmarks(self, details, detected_objects, processed_images, listing_counter, url):
        """
        Enhanced processing with comprehensive filtering and analysis - UPDATED with ULTRA-FAST bookmark functionality
        FIXED: Now passes username to bookmark_driver
        MODIFIED: Separate logic for pygame and website display - pygame shows all suitable listings with bookmark failure notices
        UPDATED: Now includes time tracking when items are added to pygame
        """
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
            # CHANGED: Use VM-based bookmark execution
            print(f"🔖 VM-THREADED BOOKMARK: {url}")
            
            # Extract username from details
            username = details.get("username", None)
            if not username or username == "Username not found":
                username = None
                print("🔖 VM-USERNAME: Not available for this listing")
            
            # Start VM bookmark in separate thread
            bookmark_success = self.vm_bookmark_driver_threaded(url, username)
            
            if bookmark_success:
                print("✅ VM bookmark thread started successfully")
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
