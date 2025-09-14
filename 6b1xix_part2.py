# Continuation from line 2201
            
        except Exception as e:
            print(f"Error finding speakers: {e}")
            return None
    
    def extract_numbers_sequence(self, text):
        """Extract numbers from text in the correct sequence"""
        word_to_num = {
            'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
            'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
            'ten': '10', 'eleven': '11', 'twelve': '12', 'thirteen': '13',
            'fourteen': '14', 'fifteen': '15', 'sixteen': '16', 'seventeen': '17',
            'eighteen': '18', 'nineteen': '19', 'twenty': '20', 'thirty': '30',
            'forty': '40', 'fifty': '50', 'sixty': '60', 'seventy': '70',
            'eighty': '80', 'ninety': '90', 'hundred': '100'
        }
        
        words = text.lower().replace(',', '').replace('.', '').split()
        numbers = []
        
        for word in words:
            if word in word_to_num:
                numbers.append(word_to_num[word])
            elif word.isdigit():
                numbers.append(word)
            elif re.match(r'^\d+$', word):
                for digit in word:
                    numbers.append(digit)
        
        digit_matches = re.findall(r'\b\d\b', text)
        all_numbers = numbers + digit_matches
        
        # Remove the duplicate filtering - keep all numbers in sequence
        valid_numbers = []
        for num in all_numbers:
            if num.isdigit() and len(num) == 1:
                valid_numbers.append(num)
        
        return valid_numbers
    
    def find_complete_sequence(self, text):
        """Try to find a complete 6-digit sequence"""
        text_clean = re.sub(r'[^\w\s]', ' ', text.lower())
        numbers = self.extract_numbers_sequence(text)
        
        if len(numbers) == 6:
            return ''.join(numbers)
        
        sequence_patterns = [r'(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)']
        
        word_to_num = {
            'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
            'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'
        }
        
        for pattern in sequence_patterns:
            matches = re.findall(pattern, text_clean)
            for match in matches:
                sequence = []
                for word in match:
                    if word in word_to_num:
                        sequence.append(word_to_num[word])
                    elif word.isdigit() and len(word) == 1:
                        sequence.append(word)
                
                if len(sequence) == 6:
                    return ''.join(sequence)
        
        return None

    def input_captcha_solution(self, sequence):
        """Input the 6-digit sequence into the captcha form using trusted events"""
        if not self.driver or not sequence or len(sequence) != 6:
            print("Cannot input solution: missing driver or invalid sequence")
            return False
        
        print(f"Starting to input captcha solution: {sequence}")
        
        try:
            # Navigate to the correct iframe (same as before)
            self.driver.switch_to.default_content()
            
            iframe_selectors = [
                "iframe[src*='captcha']",
                "iframe[src*='datadome']",
                "iframe[id*='datadome']",
                "iframe[class*='datadome']",
                "iframe[title*='captcha']",
                "iframe[title*='DataDome']"
            ]
            
            iframe_found = False
            for selector in iframe_selectors:
                try:
                    iframe = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    print(f"Found main iframe with selector: {selector}")
                    self.driver.switch_to.frame(iframe)
                    iframe_found = True
                    break
                except TimeoutException:
                    continue
            
            if not iframe_found:
                print("Could not find captcha iframe for input")
                return False
            
            # Find input fields
            input_selectors = [
                "input.audio-captcha-inputs",
                "input[class*='audio-captcha-inputs']",
                "input[data-index='1']",
                "input[maxlength='1'][inputmode='numeric']",
                "input[data-form-type='other'][maxlength='1']"
            ]
            
            input_found = False
            first_input = None
            
            for selector in input_selectors:
                try:
                    first_input = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    print(f"Found first input field with selector: {selector}")
                    input_found = True
                    break
                except TimeoutException:
                    continue
            
            # Check nested iframes if not found
            if not input_found:
                print("Input fields not found in current iframe, checking nested iframes...")
                
                try:
                    nested_iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
                    print(f"Found {len(nested_iframes)} nested iframes")
                    
                    for i, nested_iframe in enumerate(nested_iframes):
                        try:
                            print(f"Trying nested iframe {i}...")
                            self.driver.switch_to.frame(nested_iframe)
                            
                            for selector in input_selectors:
                                try:
                                    first_input = WebDriverWait(self.driver, 3).until(
                                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                                    )
                                    print(f"Found first input field in nested iframe {i} with selector: {selector}")
                                    input_found = True
                                    break
                                except:
                                    continue
                            
                            if input_found:
                                break
                            
                            self.driver.switch_to.parent_frame()
                            
                        except Exception as e:
                            print(f"Error with nested iframe {i}: {e}")
                            try:
                                self.driver.switch_to.parent_frame()
                            except:
                                self.driver.switch_to.default_content()
                                for sel in iframe_selectors:
                                    try:
                                        iframe = self.driver.find_element(By.CSS_SELECTOR, sel)
                                        self.driver.switch_to.frame(iframe)
                                        break
                                    except:
                                        continue
                            continue
                
                except Exception as e:
                    print(f"Error searching nested iframes for inputs: {e}")
            
            if not input_found or not first_input:
                print("Could not find input fields")
                self.driver.switch_to.default_content()
                return False
            
            print("Starting to input digits using native Selenium methods...")
            
            # Click on the first input field
            time.sleep(random.uniform(0.5, 1.0))
            
            # Scroll into view
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", first_input)
            time.sleep(random.uniform(0.3, 0.6))

            action = ActionChains(self.driver)


            # Click with ActionChains (this generates trusted events)


            offset_x = random.randint(-2, 2)
            offset_y = random.randint(-2, 2)

            action.move_to_element_with_offset(first_input, offset_x, offset_y)
            time.sleep(random.uniform(0.2, 0.4))
            action.move_to_element(first_input)
            time.sleep(random.uniform(0.1, 0.3))
            action.click().perform()
            
            print("Clicked on first input field")


            # Input each digit using send_keys (generates TRUSTED events)
            # Input each digit using PyAutoGUI
            for i, digit in enumerate(sequence):
                print(f"Inputting digit {i+1}: {digit}")
                
                if digit == '1':
                    time.sleep(2.3)
                
                # Random delay before typing
                time.sleep(random.uniform(0.2, 0.6))
                
                # Use PyAutoGUI instead of Windows API
                if not send_keypress_with_pyautogui(digit):
                    print(f"Failed to send PyAutoGUI keystroke for digit: {digit}")
                
                time.sleep(random.uniform(0.3, 0.4))
                
                print(f"Typed digit: {digit}")
                
                # If not the last digit, move to next field with arrow key
                if i < len(sequence) - 1:
                    time.sleep(random.uniform(0.2, 0.6))
                    
                    # Use PyAutoGUI for arrow key
                    if not send_keypress_with_pyautogui('right'):
                        print(f"Failed to send PyAutoGUI RIGHT key")
                    
                    print(f"Moved to next input field")
                    time.sleep(random.uniform(0.05, 0.25))

            print("All digits entered successfully!")
                
                # Wait a moment for any validation
            time.sleep(random.uniform(1.0, 2.0))
                
                # Find and click the Verify button (same as before)
            print("Looking for Verify button...")
            
            verify_button_selectors = [
                "button.audio-captcha-submit-button",
                "button[class*='audio-captcha-submit-button']",
                "button.push-button.no-margin",
                "button[role='button'][class*='submit']",
                "button:contains('Verify')",
                "//button[contains(@class, 'audio-captcha-submit-button')]",
                "//button[text()='Verify']",
                "//button[contains(text(), 'Verify')]"
            ]
            
            verify_button = None
            for selector in verify_button_selectors:
                try:
                    if selector.startswith("//"):
                        verify_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        verify_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    print(f"Found Verify button with selector: {selector}")
                    break
                except TimeoutException:
                    continue
            
            if not verify_button:
                print("Verify button not found, trying to find any submit-like button...")
                try:
                    all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
                    for button in all_buttons:
                        button_text = button.text.lower().strip()
                        button_class = button.get_attribute("class") or ""
                        
                        if ("verify" in button_text or 
                            "submit" in button_text or 
                            "confirm" in button_text or
                            "submit" in button_class.lower() or
                            "verify" in button_class.lower()):
                            verify_button = button
                            print(f"Found potential verify button: text='{button_text}', class='{button_class}'")
                            break
                except Exception as e:
                    print(f"Error searching for buttons: {e}")
            
            if verify_button:
                # Wait a moment before clicking verify
                time.sleep(random.uniform(0.5, 1.0))
                
                # Scroll into view
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", verify_button)
                time.sleep(random.uniform(0.3, 0.6))
                
                # Human-like click with ActionChains (generates trusted events)
                action = ActionChains(self.driver)
                offset_x = random.randint(-3, 3)
                offset_y = random.randint(-3, 3)
                action.move_to_element_with_offset(verify_button, offset_x, offset_y)
                time.sleep(random.uniform(0.2, 0.4))
                action.move_to_element(verify_button)
                time.sleep(random.uniform(0.2, 0.5))
                action.click().perform()
                
                print("Successfully clicked Verify button!")
                
                # Wait to see the result
                time.sleep(random.uniform(2.0, 4.0))
                
                self.driver.switch_to.default_content()
                return True
                
            else:
                print("Could not find Verify button")
                self.driver.switch_to.default_content()
                return False
                
        except Exception as e:
            print(f"Error inputting captcha solution: {e}")
            import traceback
            traceback.print_exc()
            try:
                self.driver.switch_to.default_content()
            except:
                pass
            return False

    def preprocess_audio(self, audio_data, sample_rate):
        """Enhanced audio preprocessing for better recognition"""
        audio_np = np.frombuffer(audio_data, dtype=np.int16)
        
        if self.CHANNELS == 2:
            audio_np = audio_np.reshape(-1, 2).mean(axis=1).astype(np.int16)
        
        if np.max(np.abs(audio_np)) > 0:
            audio_np = audio_np.astype(np.float32)
            audio_np = audio_np / np.max(np.abs(audio_np)) * 0.8
        
        nyquist = sample_rate / 2
        high_cutoff = 100
        high = high_cutoff / nyquist
        b, a = signal.butter(2, high, btype='high')
        audio_np = signal.filtfilt(b, a, audio_np)
        
        low_cutoff = 8000
        low = low_cutoff / nyquist
        b, a = signal.butter(2, low, btype='low')
        audio_np = signal.filtfilt(b, a, audio_np)
        
        if HAS_NOISEREDUCE:
            try:
                noise_sample_length = min(sample_rate, len(audio_np) // 4)
                if len(audio_np) > noise_sample_length * 2:
                    audio_np = nr.reduce_noise(
                        y=audio_np, 
                        sr=sample_rate,
                        stationary=False,
                        prop_decrease=0.8
                    )
            except Exception as e:
                print(f"Noise reduction failed: {e}")
        
        pre_emphasis = 0.97
        audio_np = np.append(audio_np[0], audio_np[1:] - pre_emphasis * audio_np[:-1])
        
        if np.max(np.abs(audio_np)) > 0:
            audio_np = audio_np / np.max(np.abs(audio_np)) * 0.9
        
        audio_np = (audio_np * 32767).astype(np.int16)
        return audio_np.tobytes()
    
    def process_audio_data(self, audio_data):
        """Process audio data and extract numbers"""
        try:
            audio_np = np.frombuffer(audio_data, dtype=np.int16)
            volume = np.sqrt(np.mean(audio_np**2))
            max_volume = np.max(np.abs(audio_np))
            
            print(f"Audio volume: {volume:.1f}, max: {max_volume}")
            
            if volume < 8:
                print("Audio too quiet, skipping...")
                return
            
            processed_audio = self.preprocess_audio(audio_data, self.RATE)
            
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                wf = wave.open(tmp_file.name, 'wb')
                wf.setnchannels(1)
                wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(processed_audio)
                wf.close()
                
                try:
                    with sr.AudioFile(tmp_file.name) as source:
                        self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                        audio = self.recognizer.record(source)
                        
                        print("Attempting speech recognition...")
                        
                        text = None
                        try:
                            # Try with show_all=True to get confidence scores and alternatives
                            result = self.recognizer.recognize_google(audio, language='en-US', show_all=True)
                            if isinstance(result, dict) and 'alternative' in result:
                                # Get the most confident result
                                text = result['alternative'][0]['transcript']
                                print(f"Google Recognition (detailed): '{text}'")
                                
                                # Also check other alternatives for better matches
                                for alt in result['alternative'][:3]:  # Check top 3 alternatives
                                    alt_text = alt['transcript']
                                    alt_numbers = self.extract_numbers_sequence(alt_text)
                                    if len(alt_numbers) >= 6:
                                        text = alt_text
                                        print(f"Using alternative with more numbers: '{text}'")
                                        break
                            else:
                                text = self.recognizer.recognize_google(audio, language='en-US', show_all=False)
                                print(f"Google Recognition: '{text}'")
                                
                        except (sr.UnknownValueError, sr.RequestError):
                            print("Google recognition failed, trying Sphinx...")
                            try:
                                text = self.recognizer.recognize_sphinx(audio)
                                print(f"Sphinx Recognition: '{text}'")
                            except:
                                print("Sphinx recognition also failed")
                        
                        if text:
                            timestamp = time.strftime("%H:%M:%S")
                            
                            # Try to find complete sequence
                            complete_seq = self.find_complete_sequence(text)
                            if complete_seq and len(complete_seq) == 6:
                                with self.numbers_lock:
                                    self.complete_sequence = complete_seq
                                    print(f"\n[{timestamp}] *** COMPLETE SEQUENCE FOUND: {complete_seq} ***")
                                    print(f"[{timestamp}] From text: '{text}'")
                                    print("="*60)
                                    print(f"SUCCESS! Complete 6-digit sequence: {complete_seq}")
                                    print("="*60)
                                    
                                    # Input the sequence into the captcha form
                                    if self.input_captcha_solution(complete_seq):
                                        print("Successfully inputted captcha solution!")
                                    else:
                                        print("Failed to input captcha solution")
                                    
                                    self.stop()
                                    return
                            
                            # Otherwise collect individual numbers
                            numbers = self.extract_numbers_sequence(text)
                            if numbers:
                                with self.numbers_lock:
                                    new_numbers = []
                                    for num in numbers:
                                        if len(self.collected_numbers) < self.target_count:
                                            self.collected_numbers.append(num)
                                            new_numbers.append(num)
                                    
                                    if new_numbers:
                                        print(f"[{timestamp}] NEW NUMBERS: {' '.join(new_numbers)}")
                                        print(f"[{timestamp}] Full text: '{text}'")
                                        print(f"[{timestamp}] Sequence so far ({len(self.collected_numbers)}/{self.target_count}): {' '.join(self.collected_numbers)}")
                                    
                                    if len(self.collected_numbers) >= self.target_count:
                                        final_sequence = ''.join(self.collected_numbers[:self.target_count])
                                        print("\n" + "="*60)
                                        print(f"SUCCESS! Collected {self.target_count} numbers:")
                                        print(f"FINAL SEQUENCE: {final_sequence}")
                                        print("="*60)
                                        
                                        # Input the sequence into the captcha form
                                        if self.input_captcha_solution(final_sequence):
                                            print("Successfully inputted captcha solution!")
                                        else:
                                            print("Failed to input captcha solution")
                                        
                                        self.stop()
                                        return
                            else:
                                print(f"[{timestamp}] No numbers found in: '{text}'")
                        
                finally:
                    try:
                        os.unlink(tmp_file.name)
                    except:
                        pass
                        
        except Exception as e:
            print(f"Audio processing error: {e}")
    
    def audio_processor_thread(self):
        """Background thread to process audio chunks"""
        while self.is_running:
            try:
                if not self.audio_queue.empty():
                    audio_data = self.audio_queue.get(timeout=1)
                    processor = threading.Thread(target=self.process_audio_data, args=(audio_data,), daemon=True)
                    processor.start()
                else:
                    time.sleep(0.1)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Processor thread error: {e}")
    
    def start_listening(self):
        """Start capturing system audio output"""
        default_speakers = self.get_default_speakers()
        
        if not default_speakers:
            print("Could not find system speakers!")
            return
        
        try:
            stream = self.p.open(
                format=self.FORMAT,
                channels=int(default_speakers["maxInputChannels"]),
                rate=int(default_speakers["defaultSampleRate"]),
                input=True,
                input_device_index=default_speakers["index"],
                frames_per_buffer=self.CHUNK
            )
            
            print(f"Listening to PC system audio... Press Ctrl+C to stop.")
            print("Looking for 6-digit number sequence...")
            print("-" * 60)
            
            self.is_running = True
            
            # Start processor threads
            for i in range(2):
                processor = threading.Thread(target=self.audio_processor_thread, daemon=True)
                processor.start()
                print(f"Started audio processor thread {i+1}")
            
            audio_buffer = b""
            buffer_size = self.RATE * self.buffer_duration * 2
            overlap_size = self.RATE * self.overlap_duration * 2
            
            while self.is_running:
                try:
                    data = stream.read(self.CHUNK, exception_on_overflow=False)
                    audio_buffer += data
                    
                    with self.numbers_lock:
                        if len(self.collected_numbers) >= self.target_count or self.complete_sequence:
                            break
                    
                    if len(audio_buffer) >= buffer_size:
                        print(f"Processing {self.buffer_duration}s audio chunk...")
                        
                        if self.audio_queue.qsize() < 3:
                            self.audio_queue.put(audio_buffer[:buffer_size])
                        else:
                            print("Audio queue full, skipping chunk...")
                            
                        audio_buffer = audio_buffer[-overlap_size:]
                        
                except Exception as e:
                    print(f"Stream error: {e}")
                    break
            
            stream.stop_stream()
            stream.close()
            
        except Exception as e:
            print(f"Error starting capture: {e}")

    def stop(self):
        """Stop the transcriber"""
        self.is_running = False
        self.p.terminate()

def debug_function_call(func_name, line_number=None):
    """Debug function to track where errors occur"""
    if print_debug:
        print(f"DEBUG: Entering function {func_name}" + (f" at line {line_number}" if line_number else ""))

# Vinted profit suitability ranges (same structure as Facebook but independent variables)
def check_vinted_profit_suitability(listing_price, profit_percentage):
    if 10 <= listing_price < 16:
        return 100 <= profit_percentage <= 600
    elif 16 <= listing_price < 25:
        return 50 <= profit_percentage <= 400
    elif 25 <= listing_price < 50:
        return 37.5 <= profit_percentage <= 550
    elif 50 <= listing_price < 100:
        return 35 <= profit_percentage <= 500
    elif listing_price >= 100:
        return 30 <= profit_percentage <= 450
    else:
        return False

@app.route("/", methods=["GET", "POST"])
def index():
    # Remove the 'self' parameter and access global variables instead
    global recent_listings, current_listing_title, current_listing_price, current_listing_description
    global current_listing_join_date, current_detected_items, current_profit, current_listing_images
    global current_listing_url
    
    if "authenticated" in session:
        return render_main_page()  # Call the standalone function
    
    if request.method == "POST":
        entered_pin = request.form.get("pin")
        if int(entered_pin) == PIN_CODE:
            session["authenticated"] = True
            return redirect(url_for("index"))
        else:
            return '''
            <html>
            <head>
                <title>Enter PIN</title>
            </head>
            <body>
                <h2>Enter 5-digit PIN to access</h2>
                <p style="color: red;">Incorrect PIN</p>
                <form method="POST">
                    <input type="password" name="pin" maxlength="5" required>
                    <button type="submit">Submit</button>
                </form>
            </body>
            </html>
            '''
    
    return '''
    <html>
    <head>
        <title>Enter PIN</title>
    </head>
    <body>
        <h2>Enter 5-digit PIN to access</h2>
        <form method="POST">
            <input type="password" name="pin" maxlength="5" required>
            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    '''

@app.route("/logout")
def logout():
    session.pop("authenticated", None)
    return redirect(url_for("index"))

@app.route('/static/icon.png')
def serve_icon():
    #pc
    #return send_file(r"C:\Users\ZacKnowsHow\Downloads\icon_2 (1).png", mimetype='image/png')
    #laptop
    return send_file(r"C:\Users\ZacKnowsHow\Downloads\icon_2.png", mimetype='image/png')

@app.route('/change_listing', methods=['POST'])
def change_listing():
    direction = request.form.get('direction')
    total_listings = len(recent_listings['listings'])
    
    if direction == 'next':
        recent_listings['current_index'] = (recent_listings['current_index'] + 1) % total_listings
    elif direction == 'previous':
        recent_listings['current_index'] = (recent_listings['current_index'] - 1) % total_listings
    
    current_listing = recent_listings['listings'][recent_listings['current_index']]
    
    # Convert images to base64
    processed_images_base64 = []
    for img in current_listing['processed_images']:
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        processed_images_base64.append(img_str)
    
    return jsonify({
        'title': current_listing['title'],
        'description': current_listing['description'],
        'join_date': current_listing['join_date'],
        'price': current_listing['price'],
        'expected_revenue': current_listing['expected_revenue'],
        'profit': current_listing['profit'],
        'detected_items': current_listing['detected_items'],
        'processed_images': processed_images_base64,
        'bounding_boxes': current_listing['bounding_boxes'],
        'url': current_listing['url'],
        'suitability': current_listing['suitability'],
        'current_index': recent_listings['current_index'] + 1,
        'total_listings': total_listings
    })

@app.route('/vinted-button-clicked', methods=['POST'])
def vinted_button_clicked():
    """Handle Vinted scraper button clicks with enhanced functionality"""
    if print_debug:
        print("DEBUG: Received a Vinted button-click POST request")
    
    # Get the listing URL and action from the form data
    url = request.form.get('url')
    action = request.form.get('action')
    
    if not url:
        print("ERROR: No URL provided in Vinted button click")
        return 'NO URL PROVIDED', 400
    
    try:
        # Print the appropriate message based on the action
        if action == 'buy_yes':
            print(f'✅ VINTED YES BUTTON: User wishes to buy listing: {url}')
            
            # Access the Vinted scraper instance and trigger enhanced button functionality
            if 'vinted_scraper_instance' in globals():
                vinted_scraper_instance.vinted_button_clicked_enhanced(url)
            else:
                print("WARNING: No Vinted scraper instance found")
                print(f'Vinted button clicked on listing: {url}')
                with open('vinted_clicked_listings.txt', 'a') as f:
                    f.write(f"{action}: {url}\n")
                    
        elif action == 'buy_no':
            print(f'❌ VINTED NO BUTTON: User does not wish to buy listing: {url}')
            # DO NOT CALL vinted_button_clicked_enhanced - just print message
            # No navigation should happen for "No" button
        else:
            print(f'🔘 VINTED BUTTON: Unknown action "{action}" for listing: {url}')
        
        return 'VINTED BUTTON CLICK PROCESSED', 200
        
    except Exception as e:
        print(f"ERROR processing Vinted button click: {e}")
        return 'ERROR PROCESSING REQUEST', 500


# Replace the render_main_page function starting at line ~465 with this modified version

def render_main_page():
    try:
        # Access global variables
        global current_listing_title, current_listing_price, current_listing_description
        global current_listing_join_date, current_detected_items, current_profit
        global current_listing_images, current_listing_url, recent_listings
        if print_debug:
            print("DEBUG: render_main_page called")
            print(f"DEBUG: recent_listings has {len(recent_listings.get('listings', []))} listings")
            print(f"DEBUG: current_listing_title = {current_listing_title}")
            print(f"DEBUG: current_listing_price = {current_listing_price}")

        # Ensure default values if variables are None or empty
        title = str(current_listing_title or 'No Title Available')
        price = str(current_listing_price or 'Price: £0.00')
        description = str(current_listing_description or 'No Description Available')
        detected_items = str(current_detected_items or 'No items detected')
        profit = str(current_profit or 'Profit: £0.00')
        join_date = str(current_listing_join_date or 'No Join Date Available')
        listing_url = str(current_listing_url or 'No URL Available')

        # Create all_listings_json - this is crucial for the JavaScript
        all_listings_json = "[]" # Default empty array
        if recent_listings and 'listings' in recent_listings and recent_listings['listings']:
            try:
                listings_data = []
                for listing in recent_listings['listings']:
                    # Convert images to base64
                    processed_images_base64 = []
                    if 'processed_images' in listing and listing['processed_images']:
                        for img in listing['processed_images']:
                            try:
                                processed_images_base64.append(base64_encode_image(img))
                            except Exception as img_error:
                                print(f"Error encoding image: {img_error}")

                    listings_data.append({
                        'title': str(listing.get('title', 'No Title')),
                        'description': str(listing.get('description', 'No Description')),
                        'join_date': str(listing.get('join_date', 'No Date')),
                        'price': str(listing.get('price', '0')),
                        'profit': float(listing.get('profit', 0)),
                        'detected_items': str(listing.get('detected_items', 'No Items')),
                        'processed_images': processed_images_base64,
                        'url': str(listing.get('url', 'No URL')),
                        'suitability': str(listing.get('suitability', 'Unknown'))
                    })
                all_listings_json = json.dumps(listings_data)
                if print_debug:
                    print(f"DEBUG: Created JSON for {len(listings_data)} listings")
            except Exception as json_error:
                print(f"ERROR creating listings JSON: {json_error}")
                all_listings_json = "[]"

        # Convert current images to base64 for web display
        image_html = ""
        if current_listing_images:
            image_html = "<div class='image-container'>"
            try:
                for img in current_listing_images:
                    buffered = io.BytesIO()
                    img.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    image_html += f'''
                    <div class="image-wrapper">
                        <img src="data:image/png;base64,{img_str}" alt="Listing Image">
                    </div>
                    '''
                image_html += "</div>"
            except Exception as img_error:
                print(f"Error processing current images: {img_error}")
                image_html = "<p>Error loading images</p>"
        else:
            image_html = "<p>No images available</p>"

        # Return the complete HTML with NEW top bar layout and stopwatch functionality
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
            <link rel="apple-touch-icon" href="/static/icon.png">
            <link rel="icon" type="image/png" href="/static/icon.png">
            <meta name="apple-mobile-web-app-capable" content="yes">
            <meta name="apple-mobile-web-app-status-bar-style" content="black">
            <meta name="apple-mobile-web-app-title" content="Marketplace Scanner">
            <title>Marketplace Scanner</title>
            <style>
                * {{
                    box-sizing: border-box;
                    margin: 0;
                    padding: 0;
                }}
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
                    background-color: #f0f0f0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    margin: 0;
                    padding: 0;
                    line-height: 1.6;
                    touch-action: manipulation;
                    overscroll-behavior-y: none;
                }}
                .container {{
                    background-color: white;
                    padding: 25px;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    text-align: center;
                    width: 100%;
                    max-width: 375px;
                    margin: 0 auto;
                    position: relative;
                    height: calc(100vh - 10px);
                    overflow-y: auto;
                }}
                
                /* NEW: Top bar styles */
                .top-bar {{
                    display: flex;
                    gap: 5px;
                    margin-bottom: 15px;
                    justify-content: space-between;
                }}
                
                .top-bar-item {{
                    flex: 1;
                    padding: 8px 4px;
                    border-radius: 8px;
                    font-size: 12px;
                    font-weight: bold;
                    color: white;
                    text-align: center;
                    min-height: 40px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }}
                
                .refresh-button {{
                    background-color: #4CAF50;
                    cursor: pointer;
                    transition: all 0.2s ease;
                    border: none;
                    touch-action: manipulation;
                    -webkit-tap-highlight-color: transparent;
                }}
                
                .refresh-button:hover {{
                    background-color: #45a049;
                    transform: translateY(-1px);
                }}
                
                .refresh-button:active {{
                    transform: translateY(0);
                }}
                
                .listing-counter {{
                    background-color: #2196F3;
                }}
                
                .stopwatch-display {{
                    background-color: #FF9800;
                    font-family: monospace;
                }}
                
                .custom-button {{
                    width: 100%;
                    padding: 12px;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    font-size: 16px;
                    font-weight: bold;
                    touch-action: manipulation;
                    -webkit-tap-highlight-color: transparent;
                    cursor: pointer;
                    transition: all 0.2s ease;
                }}
                .custom-button:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                }}
                .custom-button:active {{
                    transform: translateY(0);
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .section-box, .financial-row, .details-row {{
                    border: 1px solid black;
                    border-radius: 5px;
                    margin-bottom: -1px;
                }}
                .section-box {{
                    padding: 10px;
                }}
                .financial-row, .details-row {{
                    display: flex;
                    justify-content: space-between;
                }}
                .financial-item, .details-item {{
                    flex: 1;
                    padding: 10px;
                    border-right: 1px solid black;
                    font-weight: bold;
                    font-size: 19px;
                }}
                .financial-item:last-child, .details-item:last-child {{
                    border-right: none;
                }}
                .content-title {{
                    color: rgb(173, 13, 144);
                    font-weight: bold;
                    font-size: 1.6em;
                }}
                .content-price {{
                    color: rgb(19, 133, 194);
                    font-weight: bold;
                }}
                .content-description {{
                    color: #006400;
                    font-weight: bold;
                }}
                .content-profit {{
                    color: rgb(186, 14, 14);
                    font-weight: bold;
                }}
                .content-join-date {{
                    color: #4169E1;
                    font-weight: bold;
                }}
                .content-detected-items {{
                    color: #8B008B;
                    font-weight: bold;
                }}
                .image-container {{
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: center;
                    align-items: center;
                    gap: 10px;
                    max-height: 335px;
                    overflow-y: auto;
                    padding: 10px;
                    background-color: #f9f9f9;
                    border: 1px solid black;
                    border-radius: 10px;
                    margin-bottom: 10px;
                }}
                .image-wrapper {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    max-width: 100%;
                    max-height: 200px;
                    overflow: hidden;
                }}
                .image-wrapper img {{
                    max-width: 100%;
                    max-height: 100%;
                    object-fit: contain;
                }}
                .listing-url {{
                    font-size: 10px;
                    word-break: break-all;
                    border: 1px solid black;
                    border-radius: 5px;
                    padding: 5px;
                    margin-top: 10px;
                    font-weight: bold;
                }}
                .single-button-container {{
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                    margin: 15px 0;
                }}
                .open-listing-button {{
                    background-color: #28a745;
                    font-size: 18px;
                    padding: 15px;
                }}
                
                /* Buy decision buttons */
                .buy-decision-container {{
                    display: flex;
                    gap: 10px;
                    margin: 15px 0;
                }}
                .buy-yes-button {{
                    background-color: #28a745;
                    flex: 1;
                    padding: 15px;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 8px;
                    color: white;
                    border: none;
                    cursor: pointer;
                    transition: all 0.2s ease;
                    touch-action: manipulation;
                    -webkit-tap-highlight-color: transparent;
                }}
                .buy-yes-button:hover {{
                    background-color: #218838;
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                }}
                .buy-yes-button:active {{
                    transform: translateY(0);
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .buy-no-button {{
                    background-color: #dc3545;
                    flex: 1;
                    padding: 15px;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 8px;
                    color: white;
                    border: none;
                    cursor: pointer;
                    transition: all 0.2s ease;
                    touch-action: manipulation;
                    -webkit-tap-highlight-color: transparent;
                }}
                .buy-no-button:hover {{
                    background-color: #c82333;
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                }}
                .buy-no-button:active {{
                    transform: translateY(0);
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                
                /* Confirmation button styles */
                .confirmation-container {{
                    display: none;
                    flex-direction: column;
                    gap: 10px;
                    margin: 15px 0;
                }}
                
                .confirmation-text {{
                    color: #333;
                    font-weight: bold;
                    font-size: 14px;
                    margin-bottom: 10px;
                    text-align: center;
                }}
                
                .confirmation-buttons {{
                    display: flex;
                    gap: 10px;
                }}
                
                .confirm-yes-button {{
                    background-color: #28a745;
                    flex: 1;
                    padding: 15px;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 8px;
                    color: white;
                    border: none;
                    cursor: pointer;
                    transition: all 0.2s ease;
                    touch-action: manipulation;
                    -webkit-tap-highlight-color: transparent;
                }}
                
                .confirm-no-button {{
                    background-color: #6c757d;
                    flex: 1;
                    padding: 15px;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 8px;
                    color: white;
                    border: none;
                    cursor: pointer;
                    transition: all 0.2s ease;
                    touch-action: manipulation;
                    -webkit-tap-highlight-color: transparent;
                }}
                
                .confirm-yes-button:hover {{
                    background-color: #218838;
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                }}
                
                .confirm-no-button:hover {{
                    background-color: #5a6268;
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                }}
                
                .confirm-yes-button:active, .confirm-no-button:active {{
                    transform: translateY(0);
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
            </style>
            <script>
                const allListings = {all_listings_json};
                let currentListingIndex = 0;
                let stopwatchIntervals = {{}};
                console.log('All listings loaded:', allListings);
                console.log('Number of listings:', allListings.length);

                function refreshPage() {{
                    location.reload();
                }}

                function updateStopwatch() {{
                    if (allListings.length === 0) return;
                    
                    const currentListing = allListings[currentListingIndex];
                    const currentUrl = currentListing.url;
                    const stopwatchElement = document.querySelector('.stopwatch-display');
                    
                    if (stopwatchElement) {{
                        // Check if this URL has an active stopwatch
                        // This would need to be populated from the Python backend
                        // For now, show placeholder text
                        stopwatchElement.textContent = 'No stopwatch - listing unbookmarked';
                    }}
                }}

                function updateListingDisplay(index) {{
                    if (allListings.length === 0) {{
                        console.log('No listings available');
                        return;
                    }}
                    if (index < 0) index = allListings.length - 1;
                    if (index >= allListings.length) index = 0;
                    currentListingIndex = index;
                    const listing = allListings[index];
                    console.log('Updating to listing:', listing);

                    // Update content
                    const titleEl = document.querySelector('.content-title');
                    const priceEl = document.querySelector('.content-price');
                    const profitEl = document.querySelector('.content-profit');
                    const joinDateEl = document.querySelector('.content-join-date');
                    const detectedItemsEl = document.querySelector('.content-detected-items');
                    const descriptionEl = document.querySelector('.content-description');
                    const urlEl = document.querySelector('.content-url');
                    const counterEl = document.querySelector('.listing-counter');

                    if (titleEl) titleEl.textContent = listing.title;
                    if (priceEl) priceEl.textContent = 'Price: £' + listing.price;
                    if (profitEl) profitEl.textContent = `Profit: £${{listing.profit.toFixed(2)}}`;
                    if (joinDateEl) joinDateEl.textContent = listing.join_date;
                    if (detectedItemsEl) detectedItemsEl.textContent = listing.detected_items;
                    if (descriptionEl) descriptionEl.textContent = listing.description;
                    if (urlEl) urlEl.textContent = listing.url;
                    if (counterEl) counterEl.textContent = `${{currentListingIndex + 1}} of ${{allListings.length}}`;

                    // Update images
                    const imageContainer = document.querySelector('.image-container');
                    if (imageContainer) {{
                        imageContainer.innerHTML = '';
                        listing.processed_images.forEach(imgBase64 => {{
                            const imageWrapper = document.createElement('div');
                            imageWrapper.className = 'image-wrapper';
                            const img = document.createElement('img');
                            img.src = `data:image/png;base64=${{imgBase64}}`;
                            img.alt = 'Listing Image';
                            imageWrapper.appendChild(img);
                            imageContainer.appendChild(imageWrapper);
                        }});
                    }}
                    
                    // Update stopwatch
                    updateStopwatch();
                    
                    // Reset confirmation dialog state
                    hideConfirmation();
                }}

                function changeListingIndex(direction) {{
                    if (direction === 'next') {{
                        updateListingDisplay(currentListingIndex + 1);
                    }} else if (direction === 'previous') {{
                        updateListingDisplay(currentListingIndex - 1);
                    }}
                }}

                // Single button function to open listing directly
                function openListing() {{
                    var urlElement = document.querySelector('.content-url');
                    var url = urlElement ? urlElement.textContent.trim() : '';
                    
                    if (url && url !== 'No URL Available') {{
                        console.log('Opening listing:', url);
                        window.open(url, '_blank');
                    }} else {{
                        alert('No valid URL available for this listing');
                    }}
                }}
                
                // Confirmation dialog functions
                function showConfirmation(message, confirmCallback, cancelCallback) {{
                    const buyDecisionContainer = document.querySelector('.buy-decision-container');
                    const confirmationContainer = document.querySelector('.confirmation-container');
                    
                    if (buyDecisionContainer) buyDecisionContainer.style.display = 'none';
                    if (confirmationContainer) {{
                        confirmationContainer.style.display = 'flex';
                        
                        const confirmationText = confirmationContainer.querySelector('.confirmation-text');
                        if (confirmationText) confirmationText.textContent = message;
                        
                        const confirmYesBtn = confirmationContainer.querySelector('.confirm-yes-button');
                        const confirmNoBtn = confirmationContainer.querySelector('.confirm-no-button');
                        
                        if (confirmYesBtn) {{
                            confirmYesBtn.onclick = function() {{
                                confirmCallback();
                                hideConfirmation();
                            }};
                        }}
                        
                        if (confirmNoBtn) {{
                            confirmNoBtn.onclick = function() {{
                                cancelCallback();
                                hideConfirmation();
                            }};
                        }}
                    }}
                }}
                
                function hideConfirmation() {{
                    const buyDecisionContainer = document.querySelector('.buy-decision-container');
                    const confirmationContainer = document.querySelector('.confirmation-container');
                    
                    if (buyDecisionContainer) buyDecisionContainer.style.display = 'flex';
                    if (confirmationContainer) confirmationContainer.style.display = 'none';
                }}

                // Buy decision functions with confirmation
                function buyYes() {{
                    showConfirmation(
                        'Are you sure you want to buy this listing?',
                        function() {{
                            var urlElement = document.querySelector('.content-url');
                            var url = urlElement ? urlElement.textContent.trim() : '';
                            
                            if (url && url !== 'No URL Available') {{
                                console.log('User confirmed: wants to buy listing: ' + url);
                                
                                fetch('/vinted-button-clicked', {{
                                    method: 'POST',
                                    headers: {{
                                        'Content-Type': 'application/x-www-form-urlencoded',
                                    }},
                                    body: `url=${{encodeURIComponent(url)}}&action=buy_yes`
                                }})
                                .then(response => {{
                                    if (response.ok) {{
                                        console.log('Vinted YES button confirmed and sent successfully');
                                    }} else {{
                                        console.error('Failed to process Vinted YES button');
                                    }}
                                }})
                                .catch(error => {{
                                    console.error('Error with Vinted YES button:', error);
                                }});
                            }} else {{
                                console.log('User confirmed: wants to buy listing but no URL available');
                            }}
                        }},
                        function() {{
                            console.log('User cancelled buying decision');
                        }}
                    );
                }}

                function buyNo() {{
                    showConfirmation(
                        'Are you sure you don\\'t want to buy this listing?',
                        function() {{
                            var urlElement = document.querySelector('.content-url');
                            var url = urlElement ? urlElement.textContent.trim() : '';
                            
                            if (url && url !== 'No URL Available') {{
                                console.log('User confirmed: does not want to buy listing: ' + url);
                                
                                fetch('/vinted-button-clicked', {{
                                    method: 'POST',
                                    headers: {{
                                        'Content-Type': 'application/x-www-form-urlencoded',
                                    }},
                                    body: `url=${{encodeURIComponent(url)}}&action=buy_no`
                                }})
                                .then(response => {{
                                    if (response.ok) {{
                                        console.log('Vinted NO button confirmed and sent successfully');
                                    }} else {{
                                        console.error('Failed to process Vinted NO button');
                                    }}
                                }})
                                .catch(error => {{
                                    console.error('Error with Vinted NO button:', error);
                                }});
                            }} else {{
                                console.log('User confirmed: does not want to buy listing but no URL available');
                            }}
                        }},
                        function() {{
                            console.log('User cancelled buying decision');
                        }}
                    );
                }}

                // Initialize display on page load
                window.onload = () => {{
                    console.log('Page loaded, initializing display');
                    if (allListings.length > 0) {{
                        updateListingDisplay(0);
                    }} else {{
                        console.log('No listings to display');
                    }}
                    
                    // Start stopwatch update interval
                    setInterval(updateStopwatch, 1000);
                }};
            </script>
        </head>
        <body>
            <div class="container listing-container">
                <!-- NEW: Top bar with three colored rectangles -->
                <div class="top-bar">
                    <button class="top-bar-item refresh-button" onclick="refreshPage()">
                        Refresh Page
                    </button>
                    <div class="top-bar-item listing-counter" id="listing-counter">
                        1 of 1
                    </div>
                    <div class="top-bar-item stopwatch-display" id="stopwatch-display">
                        No stopwatch - listing unbookmarked
                    </div>
                </div>
                
                <div class="section-box">
                    <p><span class="content-title">{title}</span></p>
                </div>
                <div class="financial-row">
                    <div class="financial-item">
                        <p><span class="content-price">{price}</span></p>
                    </div>
                    <div class="financial-item">
                        <p><span class="content-profit">{profit}</span></p>
                    </div>
                </div>
                <div class="section-box">
                    <p><span class="content-description">{description}</span></p>
                </div>
                
                <!-- Single button for opening listing -->
                <div class="single-button-container">
                    <button class="custom-button open-listing-button" onclick="openListing()">
                        Open Listing in New Tab
                    </button>
                </div>
                
                <!-- Buy decision buttons -->
                <div class="buy-decision-container">
                    <button class="buy-yes-button" onclick="buyYes()">
                        Yes - Buy now
                    </button>
                    <button class="buy-no-button" onclick="buyNo()">
                        No - Do not purchase
                    </button>
                </div>
                
                <!-- Confirmation dialog (initially hidden) -->
                <div class="confirmation-container">
                    <div class="confirmation-text">
                        Are you sure?
                    </div>
                    <div class="confirmation-buttons">
                        <button class="confirm-yes-button">
                            Yes
                        </button>
                        <button class="confirm-no-button">
                            No
                        </button>
                    </div>
                </div>
                
                <div class="details-row">
                    <div class="details-item">
                        <p><span class="content-detected-items">{detected_items}</span></p>
                    </div>
                </div>
                <div class="image-container">
                    {image_html}
                </div>
                <div class="details-item">
                    <p><span class="content-join-date">{join_date}</span></p>
                </div>
                <div class="navigation-buttons">
                    <button onclick="changeListingIndex('previous')" class="custom-button" style="background-color: #666;">Previous</button>
                    <button onclick="changeListingIndex('next')" class="custom-button" style="background-color: #666;">Next</button>
                </div>
                <div class="listing-url" id="listing-url">
                    <p><span class="header">Listing URL: </span><span class="content-url">{listing_url}</span></p>
                </div>
            </div>
        </body>
        </html>
        '''
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR in render_main_page: {e}")
        print(f"Traceback: {error_details}")
        return f"<html><body><h1>Error in render_main_page</h1><pre>{error_details}</pre></body></html>"

def base64_encode_image(img):
    """Convert PIL Image to base64 string, resizing if necessary"""
    max_size = (200, 200)
    img.thumbnail(max_size, Image.LANCZOS)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


class VintedScraper:

    def restart_driver_if_dead(self, driver):
        """If driver is dead, create a new one. That's it."""
        try:
            driver.current_url  # Simple test
            return driver  # Driver is fine
        except:
            print("🔄 Driver crashed, restarting...")
            try:
                driver.quit()
            except:
                pass
            return self.setup_driver()
    # Add this method to the VintedScraper class
    def send_pushover_notification(self, title, message, api_token, user_key):
        """
        Send a notification via Pushover
        :param title: Notification title
        :param message: Notification message
        :param api_token: Pushover API token
        :param user_key: Pushover user key
        """
        try:
            url = "https://api.pushover.net/1/messages.json"
            payload = {
                "token": api_token,
                "user": user_key,
                "title": title,
                "message": message
            }
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                print(f"Notification sent successfully: {title}")
            else:
                print(f"Failed to send notification. Status code: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error sending Pushover notification: {str(e)}")

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
            'anonymous_games': 5  # Add price for anonymous games
        })
        return all_prices
    def __init__(self):

        # Initialize pygame-related variables similar to FacebookScraper
        global current_listing_title, current_listing_description, current_listing_join_date, current_listing_price
        global current_expected_revenue, current_profit, current_detected_items, current_listing_images
        global current_bounding_boxes, current_listing_url, current_suitability, suitable_listings
        global current_listing_index, recent_listings
        
        # **CRITICAL FIX: Initialize recent_listings for website navigation**
        recent_listings = {
            'listings': [],
            'current_index': 0
        }
        
        self.session_monitoring_threads = {}  # Track monitoring threads for each driver
        self.session_monitoring_active = {}   # Track if monitoring is active for each driver
    
        # Initialize all current listing variables
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
        suitable_listings = []
        current_listing_index = 0
        self.monitoring_threads_active = threading.Event()

        self.vinted_button_queue = queue.Queue()
        self.vinted_processing_active = threading.Event()  # To track if we're currently processing
        self.main_driver = None
        self.persistent_buying_driver = None
        self.main_tab_handle = None
        self.clicked_yes_listings = set()
        self.bookmark_timers = {}
        self.buying_drivers = {}  # Dictionary to store drivers {1: driver_object, 2: driver_object, etc.}
        self.driver_status = {}   # Track driver status {1: 'free'/'busy', 2: 'free'/'busy', etc.}
        self.driver_lock = threading.Lock()  # Thread safety for driver management
        # Check if CUDA is available
        
        print(f"CUDA available: {torch.cuda.is_available()}")
        print(f"GPU name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'No GPU'}")

        # Load model with explicit GPU usage
        if torch.cuda.is_available():
            model = YOLO(MODEL_WEIGHTS).cuda()  # Force GPU
            print("✅ YOLO model loaded on GPU")
        else:
            model = YOLO(MODEL_WEIGHTS).cpu()   # Fallback to CPU
            print("⚠️ YOLO model loaded on CPU (no CUDA available)")

        # Initialize all driver slots as not created
        for i in range(1, 6):  # Drivers 1-5
            self.buying_drivers[i] = None
            self.driver_status[i] = 'not_created'

        self.bookmark_driver_threads = {}  # Track threads for each driver
        self.bookmark_driver_locks = {}    # Lock for each driver
        
        # Initialize locks for each bookmark driver
        for i in range(5):
            self.bookmark_driver_locks[i] = threading.Lock()


        self.bookmark_drivers = {}  # {0: driver, 1: driver, 2: driver, 3: driver, 4: driver}
        self.bookmark_driver_status = {}  # {0: 'preparing', 1: 'ready', 2: 'busy', 3: 'not_created', 4: 'not_created'}
        self.current_bookmark_driver_index = 0
        self.bookmark_queue = Queue()  # Queue of listings waiting to be bookmarked
        self.scraping_paused = threading.Event()  # Event to pause/resume scraping
        self.scraping_paused.set()  # Initially allow scraping
        
        # Lock for thread safety
        self.bookmark_system_lock = threading.Lock()
        
        # Configuration for each of the 5 drivers
        self.bookmark_driver_configs = [
            {
                'user_data_dir': 'C:\\VintedScraper_Default_Bookmark',
                'profile_directory': 'Profile 4',
                'google_login': True,  # Original driver uses Google login
                'driver_name': 'BookmarkDriver-1'
            },
            {
                'user_data_dir': 'C:\\VintedScraper_Default2_Bookmark', 
                'profile_directory': 'Profile 17',
                'google_login': False,  # This one uses email login
                'driver_name': 'BookmarkDriver-2'
            },
            {
                'user_data_dir': 'C:\\VintedScraper_Default3_Bookmark',
                'profile_directory': 'Profile 6',
                'google_login': True,  # Uses Google login
                'driver_name': 'BookmarkDriver-3'
            },
            {
                'user_data_dir': 'C:\\VintedScraper_Default4_Bookmark',
                'profile_directory': 'Profile 12',
                'google_login': False,  # Uses email login
                'driver_name': 'BookmarkDriver-4'
            },
            {
                'user_data_dir': 'C:\\VintedScraper_Default5_Bookmark',
                'profile_directory': 'Profile 18',
                'google_login': True,  # Uses Google login
                'driver_name': 'BookmarkDriver-5'
            }
        ]
        
        # Initialize all driver statuses
        for i in range(5):
            self.bookmark_driver_status[i] = 'not_created'
        
        # Start the bookmark system
        self._initialize_bookmark_system()
        self.current_bookmark_driver = None
        self.available_ready_drivers = 0  # Track count of ready drivers
        self.shutdown_event = threading.Event()


    def _initialize_bookmark_system(self):
        """Initialize the 5-driver cycling bookmark system"""
        print("🔖 INIT: Starting 5-driver cycling bookmark system")
        
        # Start the bookmark queue processor in a separate thread
        bookmark_processor_thread = threading.Thread(
            target=self._bookmark_queue_processor,
            name="Bookmark-Queue-Processor",
            daemon=True
        )
        bookmark_processor_thread.start()
        
        # Prepare the first driver immediately
        self._prepare_next_driver_async(0)
        
        print("✅ INIT: 5-driver bookmark system initialized")

    def _start_session_monitoring(self, driver, driver_index, driver_name):
        """
        Start session blocking monitoring for a specific bookmark driver
        """
        print(f"🛡️ SESSION MONITOR: Starting monitoring for {driver_name}")
        
        # Mark monitoring as active
        self.session_monitoring_active[driver_index] = True
        
        # Create and start monitoring thread
        monitor_thread = threading.Thread(
            target=self._session_blocking_monitor_thread,
            args=(driver, driver_index, driver_name),
            name=f"SessionMonitor-{driver_name}",
            daemon=True
        )
        
        # Store thread reference
        self.session_monitoring_threads[driver_index] = monitor_thread
        
        # Start the monitoring
        monitor_thread.start()
        
        print(f"✅ SESSION MONITOR: {driver_name} monitoring thread started")

    def _find_next_available_driver_slot(self):
        """
        Find the next available driver slot for replacement
        """
        for i in range(5):
            status = self.bookmark_driver_status.get(i, 'not_created')
            if status in ['not_created', 'error', 'session_blocked']:
                return i
        return None
    
    def _session_blocking_monitor_thread(self, driver, driver_index, driver_name):
        """
        Main monitoring thread that checks for session blocking
        Runs continuously while the driver is active
        """
        print(f"🛡️ {driver_name}: Session monitoring thread started")
        
        # Session blocking detection selectors based on your document
        blocking_selectors = [
            # Main blocking message
            "p.captcha__human__title",
            
            # Specific text indicators
            "//p[contains(text(), 'Your session has been blocked')]",
            "//p[contains(text(), 'unusual activity with your session')]",
            "//p[contains(text(), 'temporarily blocked your access')]",
            
            # DataDome captcha indicators
            "iframe[src*='captcha']",
            "iframe[src*='datadome']",
            "iframe[id*='captcha']",
            
            # Button elements that indicate blocking
            "button[id='show-human-auth']",
            "#show-human-requestId",
            
            # Form elements specific to the blocking page
            "form[id='human-contact-form']",
            "textarea[id='human-comment']",
            
            # Warning/error class indicators
            ".captcha__robot__warning",
            ".captcha__human__title"
        ]
        
        try:
            while self.session_monitoring_active.get(driver_index, False):
                try:
                    # Quick check if driver is still alive
                    current_url = driver.current_url
                    
                    # Check each selector for blocking indicators
                    session_blocked = False
                    
                    for selector in blocking_selectors:
                        try:
                            if selector.startswith('//'):
                                # XPath selector
                                element = driver.find_element(By.XPATH, selector)
                            else:
                                # CSS selector
                                element = driver.find_element(By.CSS_SELECTOR, selector)
                            
                            if element:
                                # Found a blocking indicator
                                print(f"🚨 SESSION BLOCKED")
                                print(f"🛡️ {driver_name}: Detected blocking element: {selector}")
                                session_blocked = True
                                break
                                
                        except NoSuchElementException:
                            # Element not found - continue checking
                            continue
                        except Exception as selector_error:
                            # Selector failed - continue with next one
                            continue
                    
                    if session_blocked:
                        # Session is blocked - trigger cleanup and driver cycling
                        print(f"🛡️ {driver_name}: SESSION BLOCKED - Initiating driver cleanup")
                        self._handle_session_blocking(driver, driver_index, driver_name)
                        break
                    
                    # Wait before next check (check every 2 seconds)
                    time.sleep(2)
                    
                except Exception as driver_error:
                    # Driver is dead or unresponsive
                    print(f"💀 {driver_name}: Driver died during session monitoring: {driver_error}")
                    break
            
            print(f"🛡️ {driver_name}: Session monitoring stopped")
            
        except Exception as monitor_error:
            print(f"❌ {driver_name}: Session monitoring error: {monitor_error}")
            
        finally:
            # Clean up monitoring references
            self.session_monitoring_active[driver_index] = False
            if driver_index in self.session_monitoring_threads:
                del self.session_monitoring_threads[driver_index]

    def _handle_session_blocking(self, driver, driver_index, driver_name):
        """
        Handle when session blocking is detected
        Close the driver and advance to the next one
        """
        print(f"🚨 BLOCKING HANDLER: {driver_name} session blocked - starting cleanup")
        
        try:
            # Stop monitoring for this driver
            self.session_monitoring_active[driver_index] = False
            
            # Close the blocked driver
            print(f"🗑️ BLOCKING HANDLER: Closing blocked {driver_name}")
            driver.quit()
            
            # Remove from active drivers
            if driver_index in self.bookmark_drivers:
                del self.bookmark_drivers[driver_index]
            
            # Mark as blocked/error state
            self.bookmark_driver_status[driver_index] = 'session_blocked'
            
            print(f"✅ BLOCKING HANDLER: {driver_name} cleaned up due to session blocking")
            
            # If this was the current driver, advance to next
            if driver_index == self.current_bookmark_driver_index:
                print(f"🔄 BLOCKING HANDLER: Advancing from blocked current driver")
                
                with self.bookmark_system_lock:
                    self._advance_to_next_driver()
                    
                    # Start preparing a replacement driver
                    replacement_index = self._find_next_available_driver_slot()
                    if replacement_index is not None:
                        self._prepare_next_driver_async(replacement_index)
                        print(f"🔧 BLOCKING HANDLER: Started preparing replacement driver {replacement_index + 1}")
            
            print(f"🔄 BLOCKING HANDLER: Session blocking handled for {driver_name}")
            
        except Exception as cleanup_error:
            print(f"❌ BLOCKING HANDLER: Error during cleanup: {cleanup_error}")
            
    def _bookmark_queue_processor(self):
        """Main queue processor that handles bookmark requests"""
        print("🔖 PROCESSOR: Bookmark queue processor started")
        
        while True:
            try:
                # Wait for a bookmark request
                try:
                    listing_url, username = self.bookmark_queue.get(timeout=1)
                    print(f"🔖 PROCESSOR: Got bookmark request for {listing_url[:50]}...")
                except Empty:
                    continue
                
                # FIXED: Check if we have any ready drivers BEFORE pausing scraping
                ready_driver_count = sum(1 for status in self.bookmark_driver_status.values() if status == 'ready')
                
                if ready_driver_count == 0:
                    print("⏸️ NO DRIVERS: No ready bookmark drivers available - PAUSING SCRAPING")
                    self.scraping_paused.clear()  # Pause scraping
                    
                    # Wait until we have at least 1 ready driver
                    while True:
                        time.sleep(1)
                        ready_count = sum(1 for status in self.bookmark_driver_status.values() if status == 'ready')
                        if ready_count > 0:
                            print(f"✅ DRIVER READY: {ready_count} drivers ready - RESUMING SCRAPING")
                            self.scraping_paused.set()  # Resume scraping
                            break
                        print(f"⏳ WAITING: Still no ready drivers ({ready_count}/5 ready)")
                else:
                    print(f"✅ DRIVERS AVAILABLE: {ready_driver_count} ready drivers - no need to pause")
                    # STILL pause briefly to prevent overwhelming
                    print("⏸️ PAUSE: Brief pause for bookmark processing")
                    self.scraping_paused.clear()
                
                try:
                    # Process the bookmark request
                    success = self._process_bookmark_with_cycling(listing_url, username)
                    if success:
                        print(f"✅ PROCESSOR: Bookmark successful for {listing_url[:50]}...")
                    else:
                        print(f"❌ PROCESSOR: Bookmark failed for {listing_url[:50]}...")
                
                finally:
                    # RESUME SCRAPING after bookmark processing
                    print("▶️ RESUME: Resuming main scraping after bookmark")
                    self.scraping_paused.set()
                    self.bookmark_queue.task_done()
                    
            except Exception as processor_error:
                print(f"❌ PROCESSOR ERROR: {processor_error}")
                # Make sure to resume scraping even if there's an error
                self.scraping_paused.set()
                continue

    def _process_bookmark_with_cycling(self, listing_url, username):
        """Process bookmark using the cycling driver system with proper timing"""
        with self.bookmark_system_lock:
            print(f"🔖 CYCLE: Processing bookmark with driver {self.current_bookmark_driver_index + 1}/5")
            
            # FIXED: Wait for a ready driver instead of just checking once
            max_wait_attempts = 30  # 30 seconds max wait
            wait_attempt = 0
            current_driver = None
            
            while current_driver is None and wait_attempt < max_wait_attempts:
                current_driver = self._get_ready_bookmark_driver()
                
                if current_driver is None:
                    print(f"⏳ CYCLE: No ready driver, waiting... (attempt {wait_attempt + 1})")
                    time.sleep(1)
                    wait_attempt += 1
                    continue
            
            if current_driver is None:
                print(f"❌ CYCLE: No ready driver available after {max_wait_attempts} seconds")
                return False
            
            # Mark current driver as busy
            self.bookmark_driver_status[self.current_bookmark_driver_index] = 'busy'
            print(f"🔖 EXEC: Executing bookmark with driver {self.current_bookmark_driver_index + 1}")
        
        # Execute bookmark outside the lock to prevent blocking
        success = self._execute_enhanced_bookmark(current_driver, listing_url, username, self.current_bookmark_driver_index)
        
        with self.bookmark_system_lock:
            if success:
                print(f"✅ CYCLE: Driver {self.current_bookmark_driver_index + 1} completed successfully")
            else:
                print(f"❌ CYCLE: Driver {self.current_bookmark_driver_index + 1} failed")
            
            # Check if monitoring is active for this driver before cleanup
            if not self._is_monitoring_active_for_current_driver():
                # No monitoring active - safe to clean up and advance
                self._cleanup_current_driver()
                self._advance_to_next_driver()
                # Start preparing the next driver now
                next_driver_index = (self.current_bookmark_driver_index + 1) % 5
                self._prepare_next_driver_async(next_driver_index)
            else:
                print(f"🔍 CYCLE: Monitoring active - cleanup will be handled by monitoring thread")
                
        return success

    def _get_ready_driver_count(self):
        """Get count of ready drivers"""
        return sum(1 for status in self.bookmark_driver_status.values() if status == 'ready')


    def _is_monitoring_active_for_current_driver(self):
        """Check if monitoring is currently active for the current driver"""
        # This can be implemented by checking a flag set when monitoring starts
        return hasattr(self, 'current_driver_monitoring_active') and self.current_driver_monitoring_active


    def _get_ready_bookmark_driver(self):
        """Get the current ready bookmark driver"""
        current_index = self.current_bookmark_driver_index
        
        if (current_index in self.bookmark_drivers and 
            self.bookmark_driver_status[current_index] == 'ready'):
            return self.bookmark_drivers[current_index]
        
        print(f"⚠️ CYCLE: Driver {current_index + 1} not ready (status: {self.bookmark_driver_status.get(current_index, 'unknown')})")
        return None

    def _prepare_next_driver_async(self, driver_index):
        """Prepare the next driver asynchronously"""
        prepare_thread = threading.Thread(
            target=self._prepare_driver,
            args=(driver_index,),
            name=f"Prepare-Driver-{driver_index + 1}",
            daemon=True
        )
        prepare_thread.start()
        print(f"🔧 ASYNC: Started preparing driver {driver_index + 1} in background")

    def _prepare_driver(self, driver_index):
        """
        FIXED: Prepare a specific bookmark driver - CLEAR COOKIES FIRST, THEN navigate to Vinted
        """
        config = self.bookmark_driver_configs[driver_index]
        driver_name = config['driver_name']
        
        print(f"🔧 PREPARE: Starting preparation of {driver_name}")
        
        try:
            # Mark as preparing
            self.bookmark_driver_status[driver_index] = 'preparing'
            
            # STEP 1: Create the driver
            driver = self._create_vm_bookmark_driver(config, driver_index)
            
            if driver is None:
                print(f"❌ PREPARE: Failed to create {driver_name}")
                self.bookmark_driver_status[driver_index] = 'error'
                return
            
            print(f"✅ CREATE: {driver_name} created successfully")
            
            # STEP 2: CLEAR COOKIES FIRST - Navigate to a basic page to clear cookies
            print(f"🧹 PREPARE: Opening chrome://settings/clearBrowserData for {driver_name}")
            driver.get("chrome://settings/clearBrowserData")
            
            # Wait for the settings page to load
            time.sleep(3)
            
            print(f"🔍 PREPARE: Looking for clear data button in Shadow DOM for {driver_name}")
            
            # Enhanced Shadow DOM script for clearing data
            shadow_dom_clear_script = """
            function findAndClickClearButton() {
                console.log('Starting shadow DOM search for clear button...');
                
                // Strategy 1: Direct path to clear button
                try {
                    let settingsUi = document.querySelector('settings-ui');
                    if (settingsUi && settingsUi.shadowRoot) {
                        console.log('Found settings-ui with shadowRoot');
                        
                        let settingsMain = settingsUi.shadowRoot.querySelector('settings-main');
                        if (settingsMain && settingsMain.shadowRoot) {
                            console.log('Found settings-main with shadowRoot');
                            
                            let clearBrowserData = settingsMain.shadowRoot.querySelector('settings-clear-browsing-data-dialog');
                            if (clearBrowserData && clearBrowserData.shadowRoot) {
                                console.log('Found clear-browsing-data-dialog with shadowRoot');
                                
                                let clearButton = clearBrowserData.shadowRoot.querySelector('#clearButton');
                                if (clearButton && !clearButton.disabled) {
                                    console.log('Found and clicking clear button!');
                                    clearButton.click();
                                    return true;
                                } else {
                                    console.log('Clear button found but disabled or null');
                                }
                            }
                        }
                    }
                } catch (e) {
                    console.log('Strategy 1 failed:', e);
                }
                
                // Strategy 2: Search all elements recursively
                try {
                    console.log('Trying recursive shadow DOM search...');
                    function searchRecursively(element, depth = 0) {
                        if (depth > 10) return false; // Prevent infinite recursion
                        
                        if (element.shadowRoot) {
                            // Look for clear button
                            let clearButton = element.shadowRoot.querySelector('#clearButton, button[id*="clear"], cr-button[id*="clear"]');
                            if (clearButton && !clearButton.disabled) {
                                console.log('Found clear button via recursive search at depth', depth);
                                clearButton.click();
                                return true;
                            }
                            
                            // Search children
                            let children = element.shadowRoot.querySelectorAll('*');
                            for (let child of children) {
                                if (searchRecursively(child, depth + 1)) {
                                    return true;
                                }
                            }
                        }
                        return false;
                    }
                    
                    let allElements = document.querySelectorAll('*');
                    for (let el of allElements) {
                        if (searchRecursively(el)) {
                            return true;
                        }
                    }
                } catch (e) {
                    console.log('Strategy 2 failed:', e);
                }
                
                // Strategy 3: Look for any button with "clear" or "delete" text
                try {
                    console.log('Trying text-based button search...');
                    function findButtonByText(element) {
                        if (element.shadowRoot) {
                            let buttons = element.shadowRoot.querySelectorAll('button, cr-button, paper-button');
                            for (let btn of buttons) {
                                let text = (btn.textContent || '').toLowerCase();
                                if ((text.includes('delete') || text.includes('clear')) && !btn.disabled) {
                                    console.log('Found button with text:', btn.textContent);
                                    btn.click();
                                    return true;
                                }
                            }
                            
                            let children = element.shadowRoot.querySelectorAll('*');
                            for (let child of children) {
                                if (findButtonByText(child)) {
                                    return true;
                                }
                            }
                        }
                        return false;
                    }
                    
                    let allElements = document.querySelectorAll('*');
                    for (let el of allElements) {
                        if (findButtonByText(el)) {
                            return true;
                        }
                    }
                } catch (e) {
                    console.log('Strategy 3 failed:', e);
                }
                
                console.log('All strategies failed - clear button not found');
                return false;
            }
            
            return findAndClickClearButton();
            """
            
            # Execute the shadow DOM script
            clear_result = driver.execute_script(shadow_dom_clear_script)
            
            if clear_result:
                print(f"✅ PREPARE: Successfully clicked clear data button for {driver_name}")
                print(f"⏳ PREPARE: Waiting for data clearing to complete for {driver_name}")
                time.sleep(4)  # Wait for clearing to complete
            else:
                print(f"⚠️ PREPARE: Could not find clear button, using fallback method for {driver_name}")
                # Fallback: use delete_all_cookies
                driver.delete_all_cookies()
                print(f"✅ PREPARE: Used delete_all_cookies() as fallback for {driver_name}")
            
            # STEP 3: Close the driver after clearing cookies
            print(f"🔒 PREPARE: Closing {driver_name} after cookie clearing")
            driver.quit()
            time.sleep(1)  # Brief pause after closing
            
            # STEP 4: Create a NEW driver for actual use
            print(f"🔄 PREPARE: Creating fresh {driver_name} after cookie clearing")
            fresh_driver = self._create_vm_bookmark_driver(config, driver_index)
            
            if fresh_driver is None:
                print(f"❌ PREPARE: Failed to recreate fresh {driver_name}")
                self.bookmark_driver_status[driver_index] = 'error'
                return
            
            # STEP 5: NOW navigate to Vinted with the fresh driver
            print(f"🌐 PREPARE: Navigating fresh {driver_name} to Vinted")
            fresh_driver.get("https://vinted.co.uk")
            
            # Handle cookie consent
            self._handle_cookie_consent(fresh_driver, driver_name)
            
            # STEP 6: Perform login based on configuration
            login_success = self._perform_vinted_login_simple(fresh_driver, config, driver_name)
            
            if not login_success:
                print(f"❌ PREPARE: Login failed for {driver_name}")
                fresh_driver.quit()
                self.bookmark_driver_status[driver_index] = 'error'
                return
            
            # STEP 7: Handle any captcha that appears
            captcha_result = handle_datadome_audio_captcha(fresh_driver)
            
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
        
