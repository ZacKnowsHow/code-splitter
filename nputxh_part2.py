# Continuation from line 2201
        time.sleep(0.5)  # Brief pause before continuing

def setup_driver_universal(vm_ip_address, config):
    """Universal setup function for any driver configuration - DON'T KILL ACTIVE MONITORING SESSIONS"""
    
    # Session cleanup - ONLY clean up sessions that aren't being monitored
    try:
        import requests
        status_response = requests.get(f"http://{vm_ip_address}:4444/status", timeout=5)
        status_data = status_response.json()
        
        if 'value' in status_data and 'nodes' in status_data['value']:
            for node in status_data['value']['nodes']:
                if 'slots' in node:
                    for slot in node['slots']:
                        if slot.get('session'):
                            session_id = slot['session']['sessionId']
                            
                            # CHECK IF THIS SESSION IS BEING MONITORED - DON'T KILL IT
                            session_is_monitored = False
                            for driver_id, monitor_info in background_monitors.items():
                                if monitor_info.get('driver_session') == session_id:
                                    session_is_monitored = True
                                    print(f"Keeping active monitoring session: {session_id} (Driver {driver_id})")
                                    break
                            
                            if not session_is_monitored:
                                print(f"Cleaning up inactive session: {session_id}")
                                delete_response = requests.delete(
                                    f"http://{vm_ip_address}:4444/session/{session_id}",
                                    timeout=10
                                )
                                print(f"Cleaned up session: {session_id}")
                            else:
                                print(f"Skipping active monitoring session: {session_id}")
    
    except Exception as e:
        print(f"Session cleanup failed: {e}")
    
    # Chrome options for the VM instance
    chrome_options = ChromeOptions()
    chrome_options.add_argument(f"--user-data-dir={config['user_data_dir']}")
    chrome_options.add_argument(f"--profile-directory={config['profile']}")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # VM-specific optimizations
    chrome_options.add_argument('--force-device-scale-factor=1')
    chrome_options.add_argument('--high-dpi-support=1')
    chrome_options.add_argument(f"--remote-debugging-port={config['port']}")
    chrome_options.add_argument('--remote-allow-origins=*')
    chrome_options.add_argument('--disable-features=VizDisplayCompositor')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--allow-running-insecure-content')

    
    print(f"Chrome options configured: {len(chrome_options.arguments)} arguments")
    
    driver = None
    
    try:
        print("Attempting to connect to remote WebDriver...")
        
        driver = webdriver.Remote(
            command_executor=f'http://{vm_ip_address}:4444',
            options=chrome_options
        )
        
        print(f"✓ Successfully created remote WebDriver connection")
        print(f"Session ID: {driver.session_id}")
        
        print("Applying stealth modifications...")
        stealth_script = """
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
        Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
        window.chrome = {runtime: {}};
        Object.defineProperty(navigator, 'permissions', {get: () => ({query: () => Promise.resolve({state: 'granted'})})});
        
        Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 4});
        Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});
        Object.defineProperty(screen, 'colorDepth', {get: () => 24});
        """
        driver.execute_script(stealth_script)
        print("✓ Stealth script applied successfully")
        
        print(f"✓ Successfully connected to VM Chrome with clean profile")
        return driver
        
    except Exception as e:
        print(f"✗ Failed to connect to VM WebDriver")
        print(f"Error: {str(e)}")
        
        if driver:
            try:
                driver.quit()
            except:
                pass
        
        return None

def find_buy_button_with_shadow_dom(driver):
    """
    Enhanced buy now button finder - JavaScript click first approach
    Finds button and immediately clicks with JavaScript for reliability
    """
    print("🔍 SHADOW DOM: Starting buy button search with JavaScript-first approach...")
    
    # Method 1: Find button and immediately click with JavaScript
    print("⚡ JAVASCRIPT-FIRST: Finding and clicking buy button with JavaScript...")
    buy_selectors = [
        'button[data-testid="item-buy-button"]',
        'button.web_ui__Button__button.web_ui__Button__filled.web_ui__Button__default.web_ui__Button__primary.web_ui__Button__truncated',
        '//button[@data-testid="item-buy-button"]',
        '//button[contains(@class, "web_ui__Button__primary")]//span[text()="Buy now"]',
        '//span[text()="Buy now"]/parent::button'
    ]
    
    for selector in buy_selectors:
        try:
            if selector.startswith('//'):
                buy_button = driver.find_element(By.XPATH, selector)
            else:
                buy_button = driver.find_element(By.CSS_SELECTOR, selector)
            
            print(f"✅ FOUND: Buy button with: {selector}")
            
            # IMMEDIATELY click with JavaScript - no other methods tried
            try:
                driver.execute_script("arguments[0].click();", buy_button)
                print(f"✅ JAVASCRIPT-FIRST: Buy button clicked immediately with JavaScript")
                return buy_button, selector
            except Exception as js_error:
                print(f"❌ JAVASCRIPT-FIRST: JavaScript click failed: {js_error}")
                continue
                
        except:
            continue
    
    # Method 2: Shadow DOM traversal using JavaScript
    print("🌊 SHADOW DOM: Standard selectors failed, trying Shadow DOM traversal...")
    
    shadow_dom_script = """
    function findBuyButtonInShadowDOM() {
        // Function to recursively search through shadow roots
        function searchInShadowRoot(element) {
            if (!element) return null;
            
            // Check if this element has a shadow root
            if (element.shadowRoot) {
                // Search within the shadow root
                let shadowButton = element.shadowRoot.querySelector('button[data-testid="item-buy-button"]');
                if (shadowButton) {
                    console.log('Found buy button in shadow root of:', element.tagName);
                    return shadowButton;
                }
                
                // Try other selectors in shadow root
                let shadowButtonAlt = element.shadowRoot.querySelector('button.web_ui__Button__primary');
                if (shadowButtonAlt) {
                    let span = shadowButtonAlt.querySelector('span');
                    if (span && span.textContent.includes('Buy now')) {
                        console.log('Found buy button (alternative) in shadow root of:', element.tagName);
                        return shadowButtonAlt;
                    }
                }
                
                // Recursively search child elements in shadow root
                let shadowChildren = element.shadowRoot.querySelectorAll('*');
                for (let child of shadowChildren) {
                    let result = searchInShadowRoot(child);
                    if (result) return result;
                }
            }
            
            return null;
        }
        
        // Search all elements in the main document
        let allElements = document.querySelectorAll('*');
        for (let element of allElements) {
            let result = searchInShadowRoot(element);
            if (result) {
                return result;
            }
        }
        
        return null;
    }
    
    return findBuyButtonInShadowDOM();
    """
    
    try:
        shadow_button = driver.execute_script(shadow_dom_script)
        if shadow_button:
            print("✅ SHADOW DOM: Found buy button via Shadow DOM traversal!")
            return shadow_button, "shadow_dom_traversal"
    except Exception as e:
        print(f"❌ SHADOW DOM: Shadow DOM search failed: {e}")
    
    # Method 3: Alternative Shadow DOM approach - search by text content
    print("🔍 SHADOW DOM: Trying text-based Shadow DOM search...")
    
    text_based_script = """
    function findBuyButtonByText() {
        function searchForBuyNowText(element) {
            if (!element) return null;
            
            // Check shadow root
            if (element.shadowRoot) {
                // Look for any button with "Buy now" text in shadow root
                let buttons = element.shadowRoot.querySelectorAll('button');
                for (let button of buttons) {
                    if (button.textContent && button.textContent.includes('Buy now')) {
                        console.log('Found "Buy now" button in shadow root via text search');
                        return button;
                    }
                }
                
                // Recursively search in shadow root
                let shadowChildren = element.shadowRoot.querySelectorAll('*');
                for (let child of shadowChildren) {
                    let result = searchForBuyNowText(child);
                    if (result) return result;
                }
            }
            
            return null;
        }
        
        let allElements = document.querySelectorAll('*');
        for (let element of allElements) {
            let result = searchForBuyNowText(element);
            if (result) return result;
        }
        
        return null;
    }
    
    return findBuyButtonByText();
    """
    
    try:
        text_button = driver.execute_script(text_based_script)
        if text_button:
            print("✅ SHADOW DOM: Found buy button via text-based Shadow DOM search!")
            return text_button, "shadow_dom_text_search"
    except Exception as e:
        print(f"❌ SHADOW DOM: Text-based Shadow DOM search failed: {e}")
    
    # Method 4: Deep Shadow DOM inspection - log what's actually in shadow roots
    print("🔍 SHADOW DOM: Performing deep inspection to debug...")
    
    inspection_script = """
    function inspectShadowRoots() {
        let findings = [];
        
        function inspectElement(element, path = '') {
            if (!element) return;
            
            if (element.shadowRoot) {
                let shadowButtons = element.shadowRoot.querySelectorAll('button');
                if (shadowButtons.length > 0) {
                    findings.push({
                        path: path + ' > ' + element.tagName + '[shadow]',
                        buttonCount: shadowButtons.length,
                        buttons: Array.from(shadowButtons).map(btn => ({
                            tagName: btn.tagName,
                            className: btn.className,
                            textContent: btn.textContent?.substring(0, 50),
                            testId: btn.getAttribute('data-testid'),
                            id: btn.id
                        }))
                    });
                }
                
                // Inspect children in shadow root
                let shadowChildren = element.shadowRoot.querySelectorAll('*');
                for (let i = 0; i < Math.min(shadowChildren.length, 10); i++) {
                    inspectElement(shadowChildren[i], path + ' > ' + element.tagName + '[shadow]');
                }
            }
        }
        
        let allElements = document.querySelectorAll('*');
        for (let i = 0; i < Math.min(allElements.length, 20); i++) {
            inspectElement(allElements[i], 'root');
        }
        
        return findings;
    }
    
    return inspectShadowRoots();
    """
    
    try:
        inspection_results = driver.execute_script(inspection_script)
        if inspection_results:
            print("🔍 SHADOW DOM INSPECTION RESULTS:")
            for result in inspection_results[:3]:  # Show first 3 results
                print(f"  📍 Path: {result['path']}")
                print(f"  🔘 Button count: {result['buttonCount']}")
                for btn in result['buttons'][:2]:  # Show first 2 buttons
                    print(f"    - {btn['tagName']}: '{btn['textContent']}' (testId: {btn['testId']})")
    except Exception as e:
        print(f"❌ SHADOW DOM: Inspection failed: {e}")
    
    print("❌ SHADOW DOM: All Shadow DOM methods failed to find buy button")
    return None, None



class HIDKeyboard:
    """
    True OS-level keyboard input using Windows SendInput API
    Generates hardware-level events indistinguishable from real keyboard
    """
    
    # Windows API constants
    INPUT_KEYBOARD = 1
    KEYEVENTF_KEYUP = 0x0002
    KEYEVENTF_UNICODE = 0x0004
    
    # Virtual Key Codes for common keys
    VK_CODES = {
        '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34,
        '5': 0x35, '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39,
        'right': 0x27,  # Right arrow key
        'left': 0x25,   # Left arrow key
        'tab': 0x09,    # Tab key
        'enter': 0x0D,  # Enter key
        'space': 0x20,  # Space key
        'backspace': 0x08  # Backspace key
    }
    
    def __init__(self):
        """Initialize the HID keyboard with Windows API structures"""
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32
        
        # Define Windows structures
        class KEYBDINPUT(ctypes.Structure):
            _fields_ = [
                ("wVk", ctypes.wintypes.WORD),
                ("wScan", ctypes.wintypes.WORD),
                ("dwFlags", ctypes.wintypes.DWORD),
                ("time", ctypes.wintypes.DWORD),
                ("dwExtraInfo", ctypes.POINTER(ctypes.wintypes.ULONG))
            ]
        
        class HARDWAREINPUT(ctypes.Structure):
            _fields_ = [
                ("uMsg", ctypes.wintypes.DWORD),
                ("wParamL", ctypes.wintypes.WORD),
                ("wParamH", ctypes.wintypes.WORD)
            ]
        
        class MOUSEINPUT(ctypes.Structure):
            _fields_ = [
                ("dx", ctypes.wintypes.LONG),
                ("dy", ctypes.wintypes.LONG),
                ("mouseData", ctypes.wintypes.DWORD),
                ("dwFlags", ctypes.wintypes.DWORD),
                ("time", ctypes.wintypes.DWORD),
                ("dwExtraInfo", ctypes.POINTER(ctypes.wintypes.ULONG))
            ]
        
        class INPUT_UNION(ctypes.Union):
            _fields_ = [
                ("ki", KEYBDINPUT),
                ("mi", MOUSEINPUT),
                ("hi", HARDWAREINPUT)
            ]
        
        class INPUT(ctypes.Structure):
            _fields_ = [
                ("type", ctypes.wintypes.DWORD),
                ("ii", INPUT_UNION)
            ]
        
        # Store structure classes for use
        self.KEYBDINPUT = KEYBDINPUT
        self.INPUT = INPUT
        self.INPUT_UNION = INPUT_UNION
        
        print("✅ HID Keyboard initialized with Windows SendInput API")
    
    def send_key_press(self, key, hold_time=None):
        """
        Send a single key press event (key down + key up)
        
        Args:
            key (str): The key to press ('0'-'9', 'right', 'left', etc.)
            hold_time (float): Time to hold key down in seconds (optional)
        
        Returns:
            bool: True if successful, False if failed
        """
        if key not in self.VK_CODES:
            print(f"❌ HID: Unknown key '{key}'")
            return False
        
        vk_code = self.VK_CODES[key]
        
        try:
            # Create key down event
            key_input_down = self.INPUT()
            key_input_down.type = self.INPUT_KEYBOARD
            key_input_down.ii.ki = self.KEYBDINPUT()
            key_input_down.ii.ki.wVk = vk_code
            key_input_down.ii.ki.wScan = 0
            key_input_down.ii.ki.dwFlags = 0  # Key down
            key_input_down.ii.ki.time = 0
            key_input_down.ii.ki.dwExtraInfo = None
            
            # Create key up event
            key_input_up = self.INPUT()
            key_input_up.type = self.INPUT_KEYBOARD
            key_input_up.ii.ki = self.KEYBDINPUT()
            key_input_up.ii.ki.wVk = vk_code
            key_input_up.ii.ki.wScan = 0
            key_input_up.ii.ki.dwFlags = self.KEYEVENTF_KEYUP  # Key up
            key_input_up.ii.ki.time = 0
            key_input_up.ii.ki.dwExtraInfo = None
            
            # Send key down event
            result_down = self.user32.SendInput(
                1,  # Number of inputs
                ctypes.pointer(key_input_down),
                ctypes.sizeof(self.INPUT)
            )
            
            if result_down == 0:
                error_code = self.kernel32.GetLastError()
                print(f"❌ HID: SendInput key down failed, error code: {error_code}")
                return False
            
            # Hold the key if specified
            if hold_time:
                time.sleep(hold_time)
            else:
                # Default brief hold time for realistic key press
                time.sleep(random.uniform(0.02, 0.08))
            
            # Send key up event
            result_up = self.user32.SendInput(
                1,  # Number of inputs
                ctypes.pointer(key_input_up),
                ctypes.sizeof(self.INPUT)
            )
            
            if result_up == 0:
                error_code = self.kernel32.GetLastError()
                print(f"❌ HID: SendInput key up failed, error code: {error_code}")
                return False
            
            print(f"✅ HID: Successfully sent key '{key}' (VK: {vk_code:02X})")
            return True
            
        except Exception as e:
            print(f"❌ HID: Exception sending key '{key}': {e}")
            return False
    
    def send_unicode_char(self, char):
        """
        Send a Unicode character directly (alternative method)
        
        Args:
            char (str): Single Unicode character to send
        
        Returns:
            bool: True if successful, False if failed
        """
        try:
            unicode_value = ord(char)
            
            # Create Unicode input event
            unicode_input = self.INPUT()
            unicode_input.type = self.INPUT_KEYBOARD
            unicode_input.ii.ki = self.KEYBDINPUT()
            unicode_input.ii.ki.wVk = 0  # Must be 0 for Unicode
            unicode_input.ii.ki.wScan = unicode_value
            unicode_input.ii.ki.dwFlags = self.KEYEVENTF_UNICODE
            unicode_input.ii.ki.time = 0
            unicode_input.ii.ki.dwExtraInfo = None
            
            result = self.user32.SendInput(
                1,
                ctypes.pointer(unicode_input),
                ctypes.sizeof(self.INPUT)
            )
            
            if result == 0:
                error_code = self.kernel32.GetLastError()
                print(f"❌ HID: Unicode input failed for '{char}', error code: {error_code}")
                return False
            
            print(f"✅ HID: Successfully sent Unicode char '{char}' (U+{unicode_value:04X})")
            return True
            
        except Exception as e:
            print(f"❌ HID: Exception sending Unicode '{char}': {e}")
            return False
    
    def type_sequence(self, sequence, delay_between_keys=None):
        """
        Type a sequence of characters with realistic timing
        
        Args:
            sequence (str): String of characters to type
            delay_between_keys (float): Delay between keystrokes (optional)
        
        Returns:
            bool: True if all keys sent successfully
        """
        success_count = 0
        
        for i, char in enumerate(sequence):
            print(f"🔤 HID: Typing character {i+1}/{len(sequence)}: '{char}'")
            
            # Add realistic pre-keystroke delay
            if i > 0:  # No delay before first character
                delay = delay_between_keys if delay_between_keys else random.uniform(0.1, 0.3)
                time.sleep(delay)
            
            # Try virtual key code method first (more reliable)
            if char in self.VK_CODES:
                success = self.send_key_press(char)
            else:
                # Fallback to Unicode method
                success = self.send_unicode_char(char)
            
            if success:
                success_count += 1
            else:
                print(f"❌ HID: Failed to send character '{char}' at position {i}")
        
        success_rate = (success_count / len(sequence)) * 100
        print(f"📊 HID: Typing complete - {success_count}/{len(sequence)} characters sent ({success_rate:.1f}% success)")
        
        return success_count == len(sequence)
    
    def send_navigation_key(self, direction):
        """
        Send navigation keys (arrow keys, tab, enter, etc.)
        
        Args:
            direction (str): 'right', 'left', 'tab', 'enter', 'space', 'backspace'
        
        Returns:
            bool: True if successful
        """
        if direction not in self.VK_CODES:
            print(f"❌ HID: Unknown navigation key '{direction}'")
            return False
        
        return self.send_key_press(direction)


class AudioNumberDetector:
    def __init__(self, driver=None):
        self.driver = driver
        if not HAS_PYAUDIO:
            print("ERROR: pyaudiowpatch not available - audio detection will not work")
            return
            
        self.recognizer = sr.Recognizer()
        
        # Enhanced recognizer settings
        self.recognizer.energy_threshold = 200
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.5
        self.recognizer.phrase_threshold = 0.2
        self.recognizer.non_speaking_duration = 0.3
        
        self.is_running = False
        
        # Enhanced audio settings for better quality
        self.CHUNK = 2048
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        
        self.p = pyaudio.PyAudio()
        self.audio_queue = queue.Queue()
        
        # Audio processing parameters
        self.buffer_duration = 40
        self.overlap_duration = 2
        
        # Number collection
        self.collected_numbers = []
        self.target_count = 6
        self.numbers_lock = threading.Lock()
        self.complete_sequence = ""
        
        print(f"Buffer duration: {self.buffer_duration}s, Overlap: {self.overlap_duration}s")
        print(f"Will stop after collecting {self.target_count} numbers in sequence")

    def get_default_speakers(self):
        """Get the default speakers/output device for loopback capture"""
        try:
            wasapi_info = self.p.get_host_api_info_by_type(pyaudio.paWASAPI)
            default_speakers = self.p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
            
            if not default_speakers["isLoopbackDevice"]:
                for loopback in self.p.get_loopback_device_info_generator():
                    if default_speakers["name"] in loopback["name"]:
                        default_speakers = loopback
                        break
            
            print(f"Found system audio device: {default_speakers['name']}")
            return default_speakers
            
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

def base64_encode_image(img):
    """Convert PIL Image to base64 string, resizing if necessary"""
    max_size = (200, 200)
    img.thumbnail(max_size, Image.LANCZOS)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


if __name__ == "__main__":
    if VM_DRIVER_USE:
        print("VM_DRIVER_USE = True - Running VM driver script instead of main scraper")
        if not HAS_PYAUDIO:
            print("WARNING: pyaudiowpatch not available - audio features may not work")
            print("Install with: pip install PyAudioWPatch")
        main_vm_driver()