# Continuation from line 6601
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
                    chrome_opts.add_argument("--profile-directory=Profile 17")
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
                        # FIXED: Force-click the pay button using multiple aggressive methods
                        pay_clicked = False
                        
                        # Method 1: Click the inner span (Pay text) directly - this bypasses disabled button issues
                        try:
                            pay_span = self.persistent_bookmark_driver.find_element(By.XPATH, "//button[@data-testid='single-checkout-order-summary-purchase-button']//span[text()='Pay']")
                            pay_span.click()
                            log_step("pay_button_click_span", True, "Clicked Pay span directly")
                            pay_clicked = True
                        except Exception as span_error:
                            log_step("pay_button_click_span", False, str(span_error))
                        
                        # Method 2: If span click failed, try aggressive JavaScript on button
                        if not pay_clicked:
                            try:
                                # Force enable button and click it
                                self.persistent_bookmark_driver.execute_script("""
                                    var button = document.querySelector('button[data-testid="single-checkout-order-summary-purchase-button"]');
                                    if (button) {
                                        button.disabled = false;
                                        button.setAttribute('aria-disabled', 'false');
                                        button.click();
                                    }
                                """)
                                log_step("pay_button_click_force_js", True, "Force-enabled and clicked via JS")
                                pay_clicked = True
                            except Exception as js_error:
                                log_step("pay_button_click_force_js", False, str(js_error))
                        
                        # Method 3: If still failed, try dispatching click event directly
                        if not pay_clicked:
                            try:
                                self.persistent_bookmark_driver.execute_script("""
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
                                log_step("pay_button_click_dispatch_event", True, "Dispatched click event directly")
                                pay_clicked = True
                            except Exception as dispatch_error:
                                log_step("pay_button_click_dispatch_event", False, str(dispatch_error))
                        
                        # Method 4: Last resort - try form submission
                        if not pay_clicked:
                            try:
                                self.persistent_bookmark_driver.execute_script("""
                                    var button = document.querySelector('button[data-testid="single-checkout-order-summary-purchase-button"]');
                                    var form = button ? button.closest('form') : null;
                                    if (form) {
                                        form.submit();
                                    }
                                """)
                                log_step("pay_button_form_submit", True, "Submitted form directly")
                                pay_clicked = True
                            except Exception as form_error:
                                log_step("pay_button_form_submit", False, str(form_error))
                        
                        if pay_clicked:
                            # ⚠️ CRITICAL: Exact 0.25 second wait - DO NOT MODIFY! ⚠️
                            print("🔖 CRITICAL: Waiting exactly 0.25 seconds...")
                            time.sleep(1.25)
                            
                            # ⚠️ CRITICAL: Immediate tab close - DO NOT MODIFY! ⚠️
                            print("🔖 CRITICAL: Closing tab immediately...")
                            self.persistent_bookmark_driver.close()
                            
                            step_log['critical_sequence_completed'] = True
                            log_step("critical_sequence_completed", True, "0.25s wait + tab close")
                            
                            # Continue with timing and tab management...
                            bookmark_end_time = time.time()
                            total_elapsed_time = bookmark_end_time - bookmark_start_time
                            log_step("first_sequence_timing", True, f"Completed in {total_elapsed_time:.2f}s")
                            
                            # Switch back to main tab
                            if len(self.persistent_bookmark_driver.window_handles) > 0:
                                self.persistent_bookmark_driver.switch_to.window(self.persistent_bookmark_driver.window_handles[0])
                                log_step("return_to_main_tab", True)
                            
                            log_step("first_sequence_complete", True)
                        else:
                            log_step("pay_button_click_all_failed", False, "All 4 aggressive methods failed")
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
        
        # NEW: TEST_BOOKMARK_BUYING_FUNCTIONALITY implementation
        if TEST_BOOKMARK_BUYING_FUNCTIONALITY:
            print("🔖💳 TEST_BOOKMARK_BUYING_FUNCTIONALITY ENABLED")
            print(f"🔗 URL: {TEST_BOOKMARK_BUYING_URL}")
            
            # Skip all driver initialization, pygame, flask, etc.
            # Only run bookmark + buying process on the test URL
            try:
                print("🔖 STEP 1: Starting bookmark process...")
                
                # First, run the bookmark function
                # Extract username from the URL if possible or use a test username
                test_username = "test_user"  # You might want to make this configurable
                
                bookmark_success = self.bookmark_driver(TEST_BOOKMARK_BUYING_URL, test_username)
                
                if bookmark_success:
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
                        
                        # Execute the purchase process
                        self.process_single_listing_with_driver(TEST_BOOKMARK_BUYING_URL, driver_num, driver)
                        
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
            
            # Skip all driver initialization, pygame, flask, etc.
            # Just run the bookmark function directly
            success = self.bookmark_driver(BOOKMARK_TEST_URL, BOOKMARK_TEST_USERNAME)
            
            if success:
                print("✅ BOOKMARK TEST SUCCESSFUL")
            else:
                print("❌ BOOKMARK TEST FAILED")
            
            # Exit immediately after test
            print("🧪 BOOKMARK TEST MODE COMPLETE - EXITING")
            sys.exit(0)
        
        # NEW: BUYING_TEST_MODE implementation
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
        pygame_thread = threading.Thread(target=self.run_pygame_window)
        pygame_thread.start()
        
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