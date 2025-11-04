# Continuation from line 4401
                "user_data_dir": "C:\\VintedScraper_Default_Bookmark", 
                "profile": "Profile 4", 
                "port": 9224
            })
            
            time.sleep(1)  # Brief delay
            
            # Create new VM driver
            self.current_vm_driver = setup_driver_universal("192.168.56.101", {
                "user_data_dir": "C:\\VintedScraper_Default_Bookmark", 
                "profile": "Profile 4", 
                "port": 9224
            })
            
            if not self.current_vm_driver:
                print("❌ NEXT DRIVER: Failed to create new VM driver")
                self.vm_driver_ready = False
                return
            
            # Login the new driver
            success = self.login_vm_driver(self.current_vm_driver)
            
            if success:
                self.vm_driver_ready = True
                print("✅ NEXT DRIVER: New VM driver ready and logged in")
            else:
                print("❌ NEXT DRIVER: Failed to login new VM driver")
                self.vm_driver_ready = False
                
        except Exception as e:
            print(f"❌ NEXT DRIVER: Error preparing next driver: {e}")
            self.vm_driver_ready = False


    def prepare_initial_vm_driver(self):
        """Prepare the initial VM driver during startup - called ONCE at the beginning"""
        print("🚀 STARTUP: Preparing initial VM driver for immediate use")
        
        try:
            # Create and setup the first VM driver
            self.current_vm_driver = setup_driver_universal("192.168.56.101", {
                "user_data_dir": "C:\\VintedScraper_Default_Bookmark", 
                "profile": "Profile 4", 
                "port": 9224
            })
            
            if not self.current_vm_driver:
                print("❌ STARTUP: Failed to create initial VM driver")
                return False
            
            # Clear cookies and login
            success = self.login_vm_driver(self.current_vm_driver)
            
            if success:
                self.vm_driver_ready = True
                print("✅ STARTUP: Initial VM driver ready and logged in - waiting for first listing")
                return True
            else:
                print("❌ STARTUP: Failed to login initial VM driver")
                return False
                
        except Exception as e:
            print(f"❌ STARTUP: Error preparing initial VM driver: {e}")
            return False

    def __init__(self):
        """
        Modified init - FIXED to properly initialize all confidence/revenue tracking
        """
        global current_listing_title, current_listing_description, current_listing_join_date, current_listing_price
        global current_expected_revenue, current_profit, current_detected_items, current_listing_images
        global current_bounding_boxes, current_listing_url, current_suitability, suitable_listings
        global current_listing_index, recent_listings
        global current_item_confidences, current_item_revenues
        
        # **CRITICAL FIX: Initialize recent_listings for website navigation**
        recent_listings = {
            'listings': [],
            'current_index': 0
        }
        
        # FIXED: Initialize confidence and revenue tracking dictionaries
        current_item_confidences = {}
        current_item_revenues = {}
        
        # Initialize all current listing variables
        if VM_DRIVER_USE:
            self.current_vm_driver = None
            self.vm_driver_ready = False
            self.vm_driver_lock = threading.Lock()
            
            print("🔄 STARTUP: Preparing initial VM driver...")
            self.prepare_next_vm_driver()
        else:
            self.current_vm_driver = None
            self.vm_driver_ready = False
            self.vm_driver_lock = None
        
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

        # Initialize VM connection flag
        self.vm_bookmark_queue = []

        self.listing_timestamps = {}  # Format: {url: {'navigated': timestamp, 'marked_suitable': timestamp, etc.}}
        self.listing_timestamps_lock = threading.Lock()
        
        # Check if CUDA is available
        print(f"CUDA available: {torch.cuda.is_available()}")
        print(f"GPU name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'No GPU'}")

        # Load model with explicit GPU usage
        if torch.cuda.is_available():
            model = YOLO(MODEL_WEIGHTS).cuda()
            print("✅ YOLO model loaded on GPU")
        else:
            model = YOLO(MODEL_WEIGHTS).cpu()
            print("⚠️ YOLO model loaded on CPU (no CUDA available)")

    def record_listing_timestamp(self, url, event_name):
        """
        Thread-safe function to record a timestamp for a listing event
        Args:
            url (str): The listing URL
            event_name (str): Name of the event (e.g., 'navigated', 'marked_suitable', 'buy_clicked', etc.)
        """
        from datetime import datetime
        import pytz
        
        with self.listing_timestamps_lock:
            # Initialize dict for this URL if it doesn't exist
            if url not in self.listing_timestamps:
                self.listing_timestamps[url] = {}
            
            # Record timestamp in UK timezone with milliseconds
            uk_tz = pytz.timezone('Europe/London')
            timestamp = datetime.now(uk_tz)
            formatted_timestamp = timestamp.strftime("%H:%M:%S.%f")[:-3]  # Format: HH:MM:SS.mmm
            
            self.listing_timestamps[url][event_name] = formatted_timestamp
            print(f"⏱️ TIMESTAMP RECORDED: {event_name} at {formatted_timestamp} for {url[:50]}...")


    def run_pygame_window(self):
        global LOCK_POSITION, current_listing_index, suitable_listings, current_bookmark_status
        
        screen, clock = self.initialize_pygame_window()
        rectangles = [pygame.Rect(*rect) for rect in self.load_rectangle_config()] if self.load_rectangle_config() else [
            pygame.Rect(0, 0, 240, 180), pygame.Rect(240, 0, 240, 180), pygame.Rect(480, 0, 320, 180),
            pygame.Rect(0, 180, 240, 180), pygame.Rect(240, 180, 240, 180), pygame.Rect(480, 180, 320, 180),
            pygame.Rect(0, 360, 240, 240), pygame.Rect(240, 360, 240, 120), pygame.Rect(240, 480, 240, 120),
            pygame.Rect(480, 360, 160, 240), pygame.Rect(640, 360, 160, 240)
        ]
        
        fonts = {
            'number': pygame.font.Font(None, 24),
            'price': pygame.font.Font(None, 36),
            'title': pygame.font.Font(None, 40),
            'description': pygame.font.Font(None, 28),
            'join_date': pygame.font.Font(None, 28),
            'revenue': pygame.font.Font(None, 36),
            'profit': pygame.font.Font(None, 36),
            'items': pygame.font.Font(None, 24),
            'click': pygame.font.Font(None, 28),
            'suitability': pygame.font.Font(None, 28),
            'reviews': pygame.font.Font(None, 28),
            'exact_time': pygame.font.Font(None, 22),
            'bookmark_status': pygame.font.Font(None, 24)
        }
        
        dragging = False
        resizing = False
        drag_rect = None
        drag_offset = (0, 0)
        resize_edge = None

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:
                        LOCK_POSITION = not LOCK_POSITION
                    elif event.key == pygame.K_RIGHT:
                        if suitable_listings:
                            current_listing_index = (current_listing_index + 1) % len(suitable_listings)
                            current_listing = suitable_listings[current_listing_index]
                            stored_images = current_listing.get('processed_images', [])
                            
                            # CRITICAL FIX: Pass ALL parameters including confidence and revenue
                            self.update_listing_details(
                                title=current_listing['title'],
                                description=current_listing['description'],
                                join_date=current_listing['join_date'],
                                price=current_listing['price'],
                                expected_revenue=current_listing['expected_revenue'],
                                profit=current_listing['profit'],
                                detected_items=current_listing['detected_items'],
                                processed_images=stored_images,
                                bounding_boxes=current_listing['bounding_boxes'],
                                url=current_listing.get('url'),
                                suitability=current_listing.get('suitability'),
                                seller_reviews=current_listing.get('seller_reviews'),
                                bookmark_status=current_listing.get('bookmark_status'),
                                item_confidences=current_listing.get('item_confidences', {}),  # ADDED
                                item_revenues=current_listing.get('item_revenues', {}),        # ADDED
                                listing_timestamps=current_listing.get('listing_timestamps', {})
                            )
                    elif event.key == pygame.K_LEFT:
                        if suitable_listings:
                            current_listing_index = (current_listing_index - 1) % len(suitable_listings)
                            current_listing = suitable_listings[current_listing_index]
                            stored_images = current_listing.get('processed_images', [])
                            
                            # CRITICAL FIX: Pass ALL parameters including confidence and revenue
                            self.update_listing_details(
                                title=current_listing['title'],
                                description=current_listing['description'],
                                join_date=current_listing['join_date'],
                                price=current_listing['price'],
                                expected_revenue=current_listing['expected_revenue'],
                                profit=current_listing['profit'],
                                detected_items=current_listing['detected_items'],
                                processed_images=stored_images,
                                bounding_boxes=current_listing['bounding_boxes'],
                                url=current_listing.get('url'),
                                suitability=current_listing.get('suitability'),
                                seller_reviews=current_listing.get('seller_reviews'),
                                bookmark_status=current_listing.get('bookmark_status'),
                                item_confidences=current_listing.get('item_confidences', {}),  # ADDED
                                item_revenues=current_listing.get('item_revenues', {}),        # ADDED
                                listing_timestamps=current_listing.get('listing_timestamps', {})
                            )
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if rectangles[3].collidepoint(event.pos):
                            if suitable_listings and 0 <= current_listing_index < len(suitable_listings):
                                current_url = suitable_listings[current_listing_index].get('url')
                                if current_url:
                                    try:
                                        import webbrowser
                                        webbrowser.open(current_url)
                                    except Exception as e:
                                        print(f"Failed to open URL: {e}")
                        elif not LOCK_POSITION:
                            for i, rect in enumerate(rectangles):
                                if rect.collidepoint(event.pos):
                                    if event.pos[0] > rect.right - 10 and event.pos[1] > rect.bottom - 10:
                                        resizing = True
                                        drag_rect = i
                                        resize_edge = 'bottom-right'
                                    else:
                                        dragging = True
                                        drag_rect = i
                                        drag_offset = (rect.x - event.pos[0], rect.y - event.pos[1])
                                    break
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        dragging = False
                        resizing = False
                        drag_rect = None
            
            # Handle dragging and resizing
            if dragging and drag_rect is not None:
                rectangles[drag_rect].x = pygame.mouse.get_pos()[0] + drag_offset[0]
                rectangles[drag_rect].y = pygame.mouse.get_pos()[1] + drag_offset[1]
            elif resizing and drag_rect is not None:
                if resize_edge == 'bottom-right':
                    width = max(pygame.mouse.get_pos()[0] - rectangles[drag_rect].left, 20)
                    height = max(pygame.mouse.get_pos()[1] - rectangles[drag_rect].top, 20)
                    rectangles[drag_rect].size = (width, height)
            
            screen.fill((204, 210, 255))
            for i, rect in enumerate(rectangles):
                pygame.draw.rect(screen, (0, 0, 0), rect, 2)
                number_text = fonts['number'].render(str(i + 1), True, (255, 0, 0))
                number_rect = number_text.get_rect(topright=(rect.right - 5, rect.top + 5))
                screen.blit(number_text, number_rect)

                if i == 2:  # Rectangle 3 - Title
                    self.render_text_in_rect(screen, fonts['title'], current_listing_title, rect, (0, 0, 0))
                elif i == 1:  # Rectangle 2 - Price
                    self.render_text_in_rect(screen, fonts['price'], current_listing_price, rect, (0, 0, 255))
                elif i == 7:  # Rectangle 8 - Description
                    self.render_multiline_text(screen, fonts['description'], current_listing_description, rect, (0, 0, 0))
                elif i == 8:  # Rectangle 9 - Join Date + Bookmark Status
                    time_label = "Appended:"
                    combined_text = f"{time_label}\n{current_listing_join_date}\n\n{current_bookmark_status}"
                    
                    if "SUCCEEDED" in current_bookmark_status:
                        status_color = (0, 200, 0)
                    elif "FAILED" in current_bookmark_status:
                        status_color = (255, 0, 0)
                    else:
                        status_color = (100, 100, 100)
                    
                    self.render_text_in_rect(screen, fonts['bookmark_status'], combined_text, rect, status_color)
                elif i == 4:  # Rectangle 5 - Expected Revenue
                    self.render_text_in_rect(screen, fonts['revenue'], current_expected_revenue, rect, (0, 128, 0))
                elif i == 9:  # Rectangle 10 - Profit
                    self.render_text_in_rect(screen, fonts['profit'], current_profit, rect, (128, 0, 128))
                elif i == 0:  # Rectangle 1 - Detected Items WITH confidence, count, and revenue
                    # CRITICAL: Access global current_item_confidences and current_item_revenues
                    if isinstance(current_detected_items, dict):
                        formatted_lines = []
                        for item_name, count in current_detected_items.items():
                            if count > 0:
                                # Get confidence and revenue from GLOBAL variables
                                confidence_val = current_item_confidences.get(item_name, 0.0)
                                confidence_pct = confidence_val * 100
                                
                                revenue_val = current_item_revenues.get(item_name, 0.0)
                                
                                # Format: "item_name: conf=85.2% cnt=2 rev=£45.50"
                                formatted_lines.append(
                                    f"{item_name}: conf={confidence_pct:.1f}% cnt={count} rev=£{revenue_val:.2f}"
                                )
                        
                        display_text = "\n".join(formatted_lines) if formatted_lines else "No items detected"
                    else:
                        display_text = "No items detected"
                    
                    self.render_multiline_text(screen, fonts['items'], display_text, rect, (0, 0, 0))
                elif i == 10:  # Rectangle 11 - Images
                    self.render_images(screen, current_listing_images, rect, current_bounding_boxes)
                elif i == 3:  # Rectangle 4 - Click to open
                    click_text = "CLICK TO OPEN LISTING IN CHROME"
                    self.render_text_in_rect(screen, fonts['click'], click_text, rect, (255, 0, 0))
                elif i == 5:  # Rectangle 6 - Suitability Reason + Timestamps
                    timestamp_lines = []
                    
                    if current_listing_timestamps:
                        timestamp_lines.append("\n--- TIMINGS ---")
                        
                        if 'navigated' in current_listing_timestamps:
                            timestamp_lines.append(f"Navigated: {current_listing_timestamps['navigated']}")
                        
                        if 'marked_suitable' in current_listing_timestamps:
                            timestamp_lines.append(f"Marked suitable: {current_listing_timestamps['marked_suitable']}")
                        else:
                            timestamp_lines.append("Marked suitable: N/A (unsuitable)")
                        
                        if 'buy_clicked' in current_listing_timestamps:
                            timestamp_lines.append(f"Buy clicked: {current_listing_timestamps['buy_clicked']}")
                        else:
                            timestamp_lines.append("Buy clicked: Never clicked")
                        
                        if 'ship_to_home_clicked' in current_listing_timestamps:
                            timestamp_lines.append(f"Ship to home: {current_listing_timestamps['ship_to_home_clicked']}")
                        else:
                            timestamp_lines.append("Ship to home: Not clicked")
                        
                        if 'pay_clicked' in current_listing_timestamps:
                            timestamp_lines.append(f"Pay clicked: {current_listing_timestamps['pay_clicked']}")
                        else:
                            timestamp_lines.append("Pay clicked: Not clicked")
                    else:
                        timestamp_lines.append("\n--- TIMINGS ---")
                        timestamp_lines.append("No timing data available")
                    
                    combined_text = current_suitability + "\n" + "\n".join(timestamp_lines)
                    
                    self.render_text_in_rect(screen, fonts['suitability'], combined_text, rect, (255, 0, 0) if "Unsuitable" in current_suitability else (0, 255, 0))
                elif i == 6:  # Rectangle 7 - Seller Reviews
                    self.render_text_in_rect(screen, fonts['reviews'], current_seller_reviews, rect, (0, 0, 128))

            screen.blit(fonts['title'].render("LOCKED" if LOCK_POSITION else "UNLOCKED", True, (255, 0, 0) if LOCK_POSITION else (0, 255, 0)), (10, 10))

            if suitable_listings:
                listing_counter = fonts['number'].render(f"Listing {current_listing_index + 1}/{len(suitable_listings)}", True, (0, 0, 0))
                screen.blit(listing_counter, (10, 40))

            pygame.display.flip()
            clock.tick(30)

        self.save_rectangle_config(rectangles)
        pygame.quit()
        
    def base64_encode_image(self, img):
        """Convert PIL Image to base64 string, resizing if necessary"""
        # Resize image while maintaining aspect ratio
        max_size = (200, 200)
        img.thumbnail(max_size, Image.LANCZOS)
        
        # Convert to base64
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()

    def render_images(self, screen, images, rect, bounding_boxes):
        """
        Enhanced render_images that supports up to 25 images with dynamic grid sizing:
        - 1 image: 1x1 grid (full rectangle)
        - 2-4 images: 2x2 grid
        - 5-9 images: 3x3 grid
        - 10-16 images: 4x4 grid
        - 17-25 images: 5x5 grid
        """
        if not images:
            return

        num_images = len(images)
        
        # Determine grid size based on number of images
        if num_images == 1:
            grid_size = 1
        elif 2 <= num_images <= 4:
            grid_size = 2
        elif 5 <= num_images <= 9:
            grid_size = 3
        elif 10 <= num_images <= 16:
            grid_size = 4
        elif 17 <= num_images <= 25:
            grid_size = 5
        else:
            # Cap at 25 images maximum
            grid_size = 5
            num_images = min(num_images, 25)

        # Calculate cell dimensions
        cell_width = rect.width // grid_size
        cell_height = rect.height // grid_size

        # Render each image in the grid
        for i, img in enumerate(images):
            if i >= grid_size * grid_size:
                # Maximum capacity reached for current grid size
                break
            
            # Calculate row and column position
            row = i // grid_size
            col = i % grid_size
            
            # Resize image to fit cell
            img = img.resize((cell_width, cell_height))
            
            # Convert PIL image to pygame surface
            img_surface = pygame.image.fromstring(img.tobytes(), img.size, img.mode)
            
            # Calculate position on screen
            x_pos = rect.left + col * cell_width
            y_pos = rect.top + row * cell_height
            
            # Blit (draw) the image on screen
            screen.blit(img_surface, (x_pos, y_pos))

        # Display suitability reason (existing code preserved)
        if FAILURE_REASON_LISTED:
            font = pygame.font.Font(None, 24)
            suitability_text = font.render(
                current_suitability, 
                True, 
                (255, 0, 0) if "Unsuitable" in current_suitability else (0, 255, 0)
            )
            screen.blit(suitability_text, (rect.left + 10, rect.bottom - 30))

    def initialize_pygame_window(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption("Facebook Marketplace Scanner")
        return screen, pygame.time.Clock()

    def load_rectangle_config(self):
        return json.load(open(CONFIG_FILE, 'r')) if os.path.exists(CONFIG_FILE) else None

    def save_rectangle_config(self, rectangles):
        json.dump([(rect.x, rect.y, rect.width, rect.height) for rect in rectangles], open(CONFIG_FILE, 'w'))
        
    def render_text_in_rect(self, screen, font, text, rect, color):
        words = text.split()
        lines = []
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_width, _ = font.size(test_line)
            if test_width <= rect.width - 10:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        if current_line:
            lines.append(' '.join(current_line))

        total_height = sum(font.size(line)[1] for line in lines)
        if total_height > rect.height:
            scale_factor = rect.height / total_height
            new_font_size = max(1, int(font.get_height() * scale_factor))
            try:
                font = pygame.font.Font(None, new_font_size)  # Use default font
            except pygame.error:
                print(f"Error creating font with size {new_font_size}")
                return  # Skip rendering if font creation fail

        y = rect.top + 5
        for line in lines:
            try:
                text_surface = font.render(line, True, color)
                text_rect = text_surface.get_rect(centerx=rect.centerx, top=y)
                screen.blit(text_surface, text_rect)
                y += font.get_linesize()
            except pygame.error as e:
                print(f"Error rendering text: {e}")
                continue  # Skip this line if rendering fails

    def extract_price(self, text):
        import re
        """
        Extracts a float from a string like '£4.50' or '4.50 GBP'
        Returns 0.0 if nothing is found or text is None
        """
        if not text:
            return 0.0
        match = re.search(r"[\d,.]+", text)
        if match:
            return float(match.group(0).replace(",", ""))
        return 0.0
    
    def render_multiline_text(self, screen, font, text, rect, color):
        # Convert dictionary to formatted string if need
        if isinstance(text, dict):
            text_lines = []
            for key, value in text.items():
                text_lines.append(f"{key}: {value}")
            text = '\n'.join(text_lines)
        
        # Rest of the existing function remains the same
        words = text.split()
        lines = []
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_width, _ = font.size(test_line)
            if test_width <= rect.width - 20:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        if current_line:
            lines.append(' '.join(current_line))

        total_height = sum(font.size(line)[1] for line in lines)
        if total_height > rect.height:
            scale_factor = rect.height / total_height
            new_font_size = max(1, int(font.get_height() * scale_factor))
            try:
                font = pygame.font.Font(None, new_font_size)  # Use default font
            except pygame.error:
                print(f"Error creating font with size {new_font_size}")
                return  # Skip rendering if font creation fails

        y_offset = rect.top + 10
        for line in lines:
            try:
                text_surface = font.render(line, True, color)
                text_rect = text_surface.get_rect(centerx=rect.centerx, top=y_offset)
                screen.blit(text_surface, text_rect)
                y_offset += font.get_linesize()
                if y_offset + font.get_linesize() > rect.bottom - 10:
                    break
            except pygame.error as e:
                print(f"Error rendering text: {e}")
                continue  # Skip this line if rendering fails
        


    def bookmark_stopwatch_wrapper(self, func_name, tab_open_func, *args, **kwargs):
        """
        Wrapper function that times bookmark operations from tab open to ctrl+w
        """
        import time
        
        # Start timing when tab is opened
        start_time = time.time()
        print(f"⏱️ STOPWATCH START: {func_name} - Tab opening...")
        
        try:
            # Execute the tab opening and bookmark operation
            result = tab_open_func(*args, **kwargs)
            
            # Stop timing immediately after the 0.25s wait and ctrl+w
            end_time = time.time()
            elapsed = end_time - start_time
            
            print(f"⏱️ STOPWATCH END: {func_name} completed in {elapsed:.3f} seconds")
            return result
            
        except Exception as e:
            end_time = time.time()
            elapsed = end_time - start_time
            print(f"⏱️ STOPWATCH END: {func_name} failed after {elapsed:.3f} seconds - {e}")
   
            raise

    def update_listing_details(self, title, description, join_date, price, expected_revenue, 
                            profit, detected_items, processed_images, bounding_boxes, 
                            url=None, suitability=None, seller_reviews=None, 
                            bookmark_status=None, item_confidences=None, item_revenues=None, 
                            listing_timestamps=None):
        """
        FIXED: Properly updates global variables including confidence and revenue
        """
        global current_listing_title, current_listing_description, current_listing_join_date, current_listing_price
        global current_expected_revenue, current_profit, current_detected_items, current_listing_images 
        global current_bounding_boxes, current_listing_url, current_suitability, current_seller_reviews
        global current_bookmark_status, current_item_confidences, current_item_revenues
        global current_listing_timestamps

        # Initialize if None
        if item_confidences is None:
            item_confidences = {}
        if item_revenues is None:
            item_revenues = {}

        # Handle bookmark status
        if bookmark_status:
            current_bookmark_status = bookmark_status

        # CRITICAL: Initialize confidence/revenue for all detected items
        if detected_items and isinstance(detected_items, dict):
            for item_name, count in detected_items.items():
                if count > 0:
                    if item_name not in item_confidences:
                        item_confidences[item_name] = 0.0
                    if item_name not in item_revenues:
                        item_revenues[item_name] = 0.0

        # CRITICAL: Update GLOBAL dicts with deep copies
        current_item_confidences = {}
        current_item_revenues = {}
        
        for item, conf in item_confidences.items():
            current_item_confidences[item] = float(conf)
        
        for item, rev in item_revenues.items():
            current_item_revenues[item] = float(rev)

        # Handle images
        if processed_images:
            if 'current_listing_images' in globals() and current_listing_images:
                for img in current_listing_images:
                    try:
                        img.close()
                    except:
                        pass
                current_listing_images.clear()

            for img in processed_images:
                try:
                    img_copy = img.copy()
                    current_listing_images.append(img_copy)
                except Exception as e:
                    print(f"Error copying image: {str(e)}")

        # Store bounding boxes
        current_bounding_boxes = {
            'image_paths': bounding_boxes.get('image_paths', []) if bounding_boxes else [],
            'detected_objects': bounding_boxes.get('detected_objects', {}) if bounding_boxes else {}
        }

        # Handle detected_items formatting
        if isinstance(detected_items, dict):
            formatted_detected_items = {}
            for item, count in detected_items.items():
                try:
                    count_int = int(count) if isinstance(count, str) else count
                    if count_int > 0:
                        formatted_detected_items[item] = count_int
                except (ValueError, TypeError):
                    continue
            
            if not formatted_detected_items:
                formatted_detected_items = {"no_items": 0}
        else:
            formatted_detected_items = {"no_items": 0}

        stored_append_time = join_date if join_date else "No timestamp"

        # Update ALL global variables
        current_detected_items = formatted_detected_items
        current_listing_title = title[:50] + '...' if len(title) > 50 else title
        current_listing_description = description[:200] + '...' if len(description) > 200 else description if description else "No description"
        current_listing_join_date = stored_append_time
        current_listing_price = f"Price:\n£{float(price):.2f}" if price else "Price:\n£0.00"
        current_expected_revenue = f"Rev:\n£{expected_revenue:.2f}" if expected_revenue else "Rev:\n£0.00"
        current_profit = f"Profit:\n£{profit:.2f}" if profit else "Profit:\n£0.00"
        current_listing_url = url
        current_suitability = suitability if suitability else "Suitability unknown"
        current_seller_reviews = seller_reviews if seller_reviews else "No reviews yet"
        current_listing_timestamps = listing_timestamps if listing_timestamps else {}
        
        # DEBUG: Verify data was stored
        if print_debug:
            print(f"🐛 STORED {len(current_item_confidences)} confidences:")
            for item, conf in current_item_confidences.items():
                rev = current_item_revenues.get(item, 0.0)
                print(f"  {item}: conf={conf:.2%}, rev=£{rev:.2f}")



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

        options.add_argument("--disable-browser-side-navigation")
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
        import re
        
        title = listing_info.get("title", "").lower()
        description = listing_info.get("description", "").lower()
        price = listing_info.get("price", 0)
        seller_reviews = listing_info.get("seller_reviews", "No reviews yet")
        
        try:
            price_float = float(price)
        except (ValueError, TypeError):
            return "Unsuitable: Unable to parse price"
        
        # Extract number of reviews from seller_reviews
        reviews_count = 0
        if seller_reviews and seller_reviews != "No reviews yet":
            reviews_text = str(seller_reviews).strip()
            
            if print_debug:
                print(f"DEBUG: Raw seller_reviews value: '{reviews_text}'")
            
            if reviews_text.startswith("Reviews: "):
                try:
                    reviews_count = int(reviews_text.replace("Reviews: ", ""))
                except ValueError:
                    reviews_count = 0
            elif reviews_text.isdigit():
                reviews_count = int(reviews_text)
            else:
                match = re.search(r'\d+', reviews_text)
                if match:
                    reviews_count = int(match.group())
                else:
                    reviews_count = 0
        
        if print_debug:
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
            "Too many $ symbols in description")
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
        OPTIMIZED: Enhanced scraper that collects ALL elements in a SINGLE operation
        Uses JavaScript to gather all data at once for maximum speed
        UPDATED: Now includes username collection AND stores price for threshold filtering
        ** MODIFIED: Now amends postage price if below £2.99 **
        """
        debug_function_call("scrape_item_details")
        import re
        
        # Wait for page to be ready
        WebDriverWait(driver, 10, poll_frequency=0.05).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "p.web_ui__Text__subtitle"))
        )

        # OPTIMIZATION: Single JavaScript command to collect ALL elements at once
        scraping_script = """
        function scrapeAllElements() {
            const data = {
                title: null,
                price: null,
                second_price: null,
                postage: null,
                description: null,
                uploaded: null,
                seller_reviews: null,
                username: null
            };
            
            // Helper function to get text from element
            function getElementText(selector) {
                try {
                    const element = document.querySelector(selector);
                    return element ? element.textContent.trim() : null;
                } catch (e) {
                    return null;
                }
            }
            
            // Helper function to get text from multiple selectors (returns first match)
            function getElementTextMultiSelector(selectors) {
                for (let selector of selectors) {
                    try {
                        const element = document.querySelector(selector);
                        if (element && element.textContent.trim()) {
                            return element.textContent.trim();
                        }
                    } catch (e) {
                        continue;
                    }
                }
                return null;
            }
            
            // Title
            data.title = getElementText("h1.web_ui__Text__title");
            
            // Price (main price field)
            data.price = getElementText("p.web_ui__Text__subtitle");
            
            // Second price
            data.second_price = getElementText("div.web_ui__Text__title.web_ui__Text__clickable.web_ui__Text__underline-none");
            
            // Postage
            data.postage = getElementText("h3[data-testid='item-shipping-banner-price']");
            
            // Description - collect all spans within the description container
            try {
                const descSpans = document.querySelectorAll("span.web_ui__Text__text.web_ui__Text__body.web_ui__Text__left.web_ui__Text__format span");
                if (descSpans.length > 0) {
                    data.description = Array.from(descSpans).map(span => span.textContent.trim()).join(' ');
                }
            } catch (e) {
                data.description = null;
            }
            
            // Uploaded
            data.uploaded = getElementText("span.web_ui__Text__text.web_ui__Text__subtitle.web_ui__Text__left.web_ui__Text__bold");
            
            // Seller reviews - try multiple selectors and find one with digits
            const reviewSelectors = [
                "span.web_ui__Text__text.web_ui__Text__caption.web_ui__Text__left",
                "span[class*='caption'][class*='left']",
                "div[class*='reviews'] span",
                "*[class*='review']"
            ];
            
            for (let selector of reviewSelectors) {
                try {
                    const elements = document.querySelectorAll(selector);
                    for (let element of elements) {
                        const text = element.textContent.trim();
                        // Look for text that contains digits (likely review count)
                        if (text && (text.match(/\\d+/) || text.toLowerCase().includes('review'))) {
                            data.seller_reviews = text;
                            break;
                        }
                    }
                    if (data.seller_reviews) break;
                } catch (e) {
                    continue;
                }
            }
            
            // Username - try multiple selectors
            const usernameSelectors = [
                "span[data-testid='profile-username']",
                "span.web_ui__Text__text.web_ui__Text__body.web_ui__Text__left.web_ui__Text__amplified.web_ui__Text__bold[data-testid='profile-username']",
                "*[data-testid='profile-username']",
                "span.web_ui__Text__amplified.web_ui__Text__bold"
            ];
            
            data.username = getElementTextMultiSelector(usernameSelectors);
            
            return data;
        }
        
        return scrapeAllElements();
        """
        
        try:
            # Execute the JavaScript to collect all data in ONE operation
            data_raw = driver.execute_script(scraping_script)
            
            # Convert the raw data to the expected format
            data = {
                "title": data_raw.get("title"),
                "price": data_raw.get("price"),
                "second_price": data_raw.get("second_price"),
                "postage": data_raw.get("postage"),
                "description": data_raw.get("description"),
                "uploaded": data_raw.get("uploaded"),
                "seller_reviews": data_raw.get("seller_reviews") if data_raw.get("seller_reviews") else "No reviews yet",
                "username": data_raw.get("username") if data_raw.get("username") else "Username not found"
            }
            
        except Exception as js_error:
            print(f"JavaScript scraping failed: {js_error}")
            print("Falling back to traditional Selenium scraping...")
            
            # FALLBACK: Traditional Selenium scraping (original method)
            fields = {
                "title": "h1.web_ui__Text__title",
                "price": "p.web_ui__Text__subtitle",
                "second_price": "div.web_ui__Text__title.web_ui__Text__clickable.web_ui__Text__underline-none",
                "postage": "h3[data-testid='item-shipping-banner-price']",
                "description": "span.web_ui__Text__text.web_ui__Text__body.web_ui__Text__left.web_ui__Text__format span",
                "uploaded": "span.web_ui__Text__text.web_ui__Text__subtitle.web_ui__Text__left.web_ui__Text__bold",
                "seller_reviews": "span.web_ui__Text__text.web_ui__Text__caption.web_ui__Text__left",
                "username": "span[data-testid='profile-username']",
            }

            data = {}
            for key, sel in fields.items():
                try:
                    if key == "seller_reviews":
                        # [Existing seller reviews logic - kept unchanged]
                        review_selectors = [
                            "span.web_ui__Text__text.web_ui__Text__caption.web_ui__Text__left",
                            "span[class*='caption'][class*='left']",
                            "div[class*='reviews'] span",
                            "*[class*='review']",
                        ]
                        
                        reviews_text = None
                        for review_sel in review_selectors:
                            try:
                                elements = driver.find_elements(By.CSS_SELECTOR, review_sel)
                                for element in elements:
                                    text = element.text.strip()
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
                        
                        if reviews_text:
                            if reviews_text == "No reviews yet" or "no review" in reviews_text.lower():
                                data[key] = "No reviews yet"
                            elif reviews_text.isdigit():
                                data[key] = reviews_text
                                if print_debug:
                                    print(f"DEBUG: Set seller_reviews to: '{reviews_text}'")
                            else:
                                match = re.search(r'(\d+)', reviews_text)
                                if match:
                                    data[key] = match.group(1)
                                    if print_debug:
                                        print(f"DEBUG: Extracted number from '{reviews_text}': '{match.group(1)}'")
                                else:
                                    data[key] = "No reviews yet"
                        else:
                            data[key] = "No reviews yet"
                            if print_debug:
                                print("DEBUG: No seller reviews found with any selector")
                            
                    elif key == "username":
                        # [Existing username logic - kept unchanged]
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
                            alternative_username_selectors = [
                                "span.web_ui__Text__text.web_ui__Text__body.web_ui__Text__left.web_ui__Text__amplified.web_ui__Text__bold[data-testid='profile-username']",
                                "span[data-testid='profile-username']",
                                "*[data-testid='profile-username']",
                                "span.web_ui__Text__amplified.web_ui__Text__bold",
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

        # ========================================================================
        # CRITICAL NEW CODE: POSTAGE PRICE AMENDMENT
        # ========================================================================
        # Extract the postage price as a float
        postage_text = data.get("postage", "£0")
        postage_value = self.extract_price(postage_text)
        
        # CRITICAL: Apply the £2.99 minimum postage rule
        MIN_POSTAGE = 2.99
        original_postage = postage_value
        
        if postage_value < MIN_POSTAGE:
            postage_value = MIN_POSTAGE
            print(f"🔧 POSTAGE AMENDED: £{original_postage:.2f} → £{MIN_POSTAGE:.2f}")
            
            # Update the data dict with the amended postage (formatted as text)
            data["postage"] = f"£{MIN_POSTAGE:.2f}"
        else:
            print(f"✅ POSTAGE OK: £{postage_value:.2f} (no amendment needed)")
        
        # ========================================================================
        # END OF POSTAGE AMENDMENT CODE
        # ========================================================================

        # Process seller_reviews value (same logic for both JS and fallback methods)
        if data.get("seller_reviews") and data["seller_reviews"] != "No reviews yet":
            reviews_text = str(data["seller_reviews"]).strip()
            
            if print_debug:
                print(f"DEBUG: Raw seller_reviews value: '{reviews_text}'")
            
            if reviews_text.startswith("Reviews: "):
                try:
                    data["seller_reviews"] = reviews_text.replace("Reviews: ", "")
                except ValueError:
                    data["seller_reviews"] = "No reviews yet"
            elif reviews_text.isdigit():
                data["seller_reviews"] = reviews_text
            else:
                match = re.search(r'\d+', reviews_text)
                if match:
                    data["seller_reviews"] = match.group()
                else:
                    data["seller_reviews"] = "No reviews yet"

        # Keep title formatting for pygame display
        if data["title"]:
            data["title"] = data["title"][:50] + '...' if len(data["title"]) > 50 else data["title"]

        # Calculate and store the total price for threshold filtering
        second_price = self.extract_price(data.get("second_price", "0"))
        postage = self.extract_price(data.get("postage", "0"))  # This now uses the AMENDED postage
        total_price = second_price + postage
        
        # Store the calculated price for use in object detection
        self.current_listing_price_float = total_price
        
        # DEBUG: Print final scraped data
        if print_debug:
            print(f"DEBUG: Final scraped seller_reviews: '{data.get('seller_reviews')}'")
            print(f"DEBUG: Final scraped username: '{data.get('username')}'")
            print(f"DEBUG: Total price calculated: £{total_price:.2f} (stored for threshold filtering)")
            print(f"DEBUG: Postage used in calculation: £{postage:.2f}")
            
        return data

    def clear_download_folder(self):
        if os.path.exists(DOWNLOAD_ROOT):
            shutil.rmtree(DOWNLOAD_ROOT)
        os.makedirs(DOWNLOAD_ROOT, exist_ok=True)

                
    def process_listing_immediately_with_vm(self, url, details, detected_objects, processed_images, listing_counter, all_confidences=None, item_revenues_from_detection=None):
        """
        FIXED: Now properly checks for misc_games when evaluating game-only listings
        EXCEPTION: If listing has 3 actual detected games AND misc_games, it should NOT be marked unsuitable
        """
        global suitable_listings, current_listing_index, recent_listings, current_bookmark_status

        print(f"🚀 REAL-TIME: Processing listing #{listing_counter}")
        
        # Initialize if None
        if all_confidences is None:
            all_confidences = {}
        if item_revenues_from_detection is None:
            item_revenues_from_detection = {}

        username = details.get("username", None)
        if not username or username == "Username not found":
            username = None

        second_price = self.extract_price(details.get("second_price", "0"))
        postage = self.extract_price(details.get("postage", "0"))
        total_price = second_price + postage
        
        print(f"💰 PRICE: £{total_price:.2f}")

        seller_reviews = details.get("seller_reviews", "No reviews yet")

        listing_info = {
            "title": details.get("title", "").lower(),
            "description": details.get("description", "").lower(),
            "price": total_price,
            "seller_reviews": seller_reviews,
            "url": url
        }

        suitability_result = self.check_vinted_listing_suitability(listing_info)

        # ========================================================================
        # CRITICAL FIX: Only apply console keyword detection if price is high enough
        # This prevents false positives from text mentions on low-priced game-only listings
        # ========================================================================
        detected_console = None
        
        # Only run keyword detection if price meets threshold
        if total_price >= MIN_PRICE_FOR_CONSOLE_KEYWORD_DETECTION:
            detected_console = self.detect_console_keywords_vinted(
                details.get("title", ""),
                details.get("description", "")
            )
            
            if detected_console:
                print(f"💰 CONSOLE KEYWORD: Found '{detected_console}' in text (price £{total_price:.2f} >= £{MIN_PRICE_FOR_CONSOLE_KEYWORD_DETECTION})")
                mutually_exclusive_items = ['switch', 'oled', 'lite', 'switch_box', 'oled_box', 
                                            'lite_box', 'switch_in_tv', 'oled_in_tv']
                for item in mutually_exclusive_items:
                    detected_objects[item] = 1 if item == detected_console else 0
            else:
                print(f"💰 CONSOLE KEYWORD: No keywords found (price £{total_price:.2f} >= threshold)")
        else:
            print(f"⏭️ CONSOLE KEYWORD: Skipped (price £{total_price:.2f} < £{MIN_PRICE_FOR_CONSOLE_KEYWORD_DETECTION})")
            # Don't run keyword detection at all for low-priced listings

        detected_objects = self.handle_oled_title_conversion_vinted(
            detected_objects,
            details.get("title", ""),
            details.get("description", "")
        )

        # Calculate revenue (this creates a NEW item_revenues dict)
        total_revenue, expected_profit, profit_percentage, display_objects, item_revenues_from_calc = \
            self.calculate_vinted_revenue(
                detected_objects,
                total_price, 
                details.get("title", ""), 
                details.get("description", "")
            )

        final_item_revenues = {}
        final_item_revenues.update(item_revenues_from_calc)
        final_item_revenues.update(item_revenues_from_detection)

        if print_debug:
            print(f"🐛 DEBUG: detected_objects after revenue calc has {len(detected_objects)} items")
            if 'misc_games' in detected_objects:
                print(f"🐛 DEBUG: misc_games = {detected_objects['misc_games']}")

        profit_suitability = self.check_vinted_profit_suitability(total_price, profit_percentage)

        # ========================================================================
        # CRITICAL SECTION - GAME FILTER LOGIC WITH EXCEPTION FOR MISC_GAMES
        # ========================================================================
        game_classes = [
            '1_2_switch', 'animal_crossing', 'arceus_p', 'bow_z', 'bros_deluxe_m', 'crash_sand',
            'dance', 'diamond_p', 'evee', 'fifa_23', 'fifa_24', 'gta', 'just_dance', 'kart_m', 'kirby',
            'lets_go_p', 'links_z', 'luigis', 'mario_maker_2', 'mario_sonic', 'mario_tennis', 'minecraft',
            'minecraft_dungeons', 'minecraft_story', 'miscellanious_sonic', 'odyssey_m', 'other_mario',
            'party_m', 'rocket_league', 'scarlet_p', 'shield_p', 'shining_p', 'skywards_z', 'smash_bros',
            'snap_p', 'splatoon_2', 'splatoon_3', 'super_m_party', 'super_mario_3d', 'switch_sports',
            'sword_p', 'tears_z', 'violet_p'
        ]
        
        # Count actual detected games (not including misc_games)
        game_count = sum(detected_objects.get(game, 0) for game in game_classes)
        
        # Count misc_games separately
        misc_games_count = detected_objects.get('misc_games', 0)
        
        # Get non-game classes (excluding misc_games)
        non_game_classes = [
            cls for cls in detected_objects.keys() 
            if cls not in game_classes 
            and cls != 'misc_games'
            and detected_objects.get(cls, 0) > 0
        ]

        unsuitability_reasons = []

        if "Unsuitable" in suitability_result:
            unsuitability_reasons.append(suitability_result.replace("Unsuitable: ", ""))

        # ========================================================================
        # CRITICAL FIX: Exception for listings with exactly 3 games + misc_games
        # ========================================================================
        # Original rule: 1-3 games with no additional non-game items = unsuitable
        # Exception: If game_count == 3 AND misc_games > 0, then it IS suitable
        
        if 1 <= game_count <= 3 and not non_game_classes:
            # Check for the exception: exactly 3 detected games WITH misc_games
            if game_count == 3 and misc_games_count > 0:
                # EXCEPTION APPLIES - this listing is suitable
                print(f"✅ EXCEPTION: 3 detected games + {misc_games_count} misc_games = SUITABLE")
            else:
                # No exception - apply original unsuitable rule
                unsuitability_reasons.append(
                    f"{game_count} game(s) with no additional non-game items"
                )
                print(f"❌ UNSUITABLE: {game_count} game(s), no misc_games or < 3 detected games")

        if not profit_suitability:
            unsuitability_reasons.append(
                f"Profit £{expected_profit:.2f} ({profit_percentage:.2f}%) not suitable"
            )

        if unsuitability_reasons:
            suitability_reason = "Unsuitable:\n---- " + "\n---- ".join(unsuitability_reasons)
            is_suitable = False
        else:
            suitability_reason = f"Suitable: Profit £{expected_profit:.2f} ({profit_percentage:.2f}%)"
            is_suitable = True
            
            # TIMESTAMP: Record when listing was marked as suitable
            self.record_listing_timestamp(url, 'marked_suitable')

        bookmark_status = "No bookmark attempted"
        
        if is_suitable or VINTED_SHOW_ALL_LISTINGS:
            if VM_DRIVER_USE:
                start_listing_timer(url)
                
                try:
                    success = self.execute_bookmark_with_preloaded_driver(url)
                    bookmark_status = current_bookmark_status
                    if not success:
                        stop_listing_timer(url, stage='failed')
                except Exception as vm_error:
                    bookmark_status = f"❌ BOOKMARK FAILED: {str(vm_error)[:30]}"
                    stop_listing_timer(url, stage='error')
            
                if VM_DRIVER_USE:
                    try:
                        self.prepare_next_vm_driver()
                    except Exception as prep_error:
                        print(f"❌ NEXT DRIVER ERROR: {prep_error}")
        else:
            bookmark_status = "Unsuitable - no bookmark"

        from datetime import datetime
        import pytz
        uk_tz = pytz.timezone('Europe/London')
        append_time = datetime.now(uk_tz)
        exact_append_time = append_time.strftime("%H:%M:%S.%f")[:-3]

        preserved_images = []
        for img in processed_images:
            try:
                img_copy = img.copy()
                preserved_images.append(img_copy)
            except Exception as e:
                print(f"Error copying image: {e}")

        if print_debug:
            print(f"🐛 DEBUG: Confidences dict has {len(all_confidences)} items")
            print(f"🐛 DEBUG: Revenues dict has {len(final_item_revenues)} items")
            for item in detected_objects:
                if detected_objects[item] > 0:
                    conf = all_confidences.get(item, 0.0)
                    rev = final_item_revenues.get(item, 0.0)
                    print(f"🐛 DEBUG: {item} -> conf={conf:.2%}, rev=£{rev:.2f}")

        listing_timestamps_data = {}
        with self.listing_timestamps_lock:
            if url in self.listing_timestamps:
                listing_timestamps_data = self.listing_timestamps[url].copy()

        final_listing_info = {
            'title': details.get("title", "No title"),
            'description': details.get("description", "No description"),
            'join_date': exact_append_time,
            'price': str(total_price),
            'expected_revenue': total_revenue,
            'profit': expected_profit,
            'detected_items': detected_objects,
            'processed_images': preserved_images,
            'bounding_boxes': {'image_paths': [], 'detected_objects': detected_objects},
            'url': url,
            'suitability': suitability_reason,
            'seller_reviews': seller_reviews,
            'bookmark_status': bookmark_status,
            'item_confidences': all_confidences,
            'item_revenues': final_item_revenues,
            'listing_timestamps': listing_timestamps_data
        }

        should_add_to_display = is_suitable or VINTED_SHOW_ALL_LISTINGS

        if should_add_to_display:
            recent_listings['listings'].append(final_listing_info)
            recent_listings['current_index'] = len(recent_listings['listings']) - 1

            suitable_listings.append(final_listing_info)
            current_listing_index = len(suitable_listings) - 1
            
            self.update_listing_details(**final_listing_info)

            print(f"✅ Added to display")

        self.cleanup_processed_images(processed_images)

        
    # FIXED: Updated process_vinted_listing function - key section that handles suitability checking
    def send_to_vm_bookmark_system(self, url):
        """
        DEPRECATED: This method is now replaced by immediate processing
        Real-time processing happens in process_listing_immediately_with_vm
        """
        print(f"⚠️  DEPRECATED: send_to_vm_bookmark_system called")
        print(f"🔄 REAL-TIME: Processing should happen immediately, not queued")
        pass  # Do nothing - real-time processing handles this

    def process_vinted_listing(self, details, detected_objects, processed_images, listing_counter, url, all_confidences=None, item_revenues=None):
        """
        FIXED: Actually uses the confidences and revenues passed in
        """
        print(f"📋 PROCESSING: Listing #{listing_counter}")
        
        # CRITICAL: Pass through the confidences and revenues
        self.process_listing_immediately_with_vm(
            url, 
            details, 
            detected_objects, 
            processed_images, 
            listing_counter,
            all_confidences,  # ADD THIS PARAMETER
            item_revenues     # ADD THIS PARAMETER
        )
        
        print(f"✅ PROCESSING COMPLETE: Listing #{listing_counter} finished")


    def should_process_listing_immediately(self, is_suitable, detected_objects, total_price):
        """
        Determine if a listing should trigger immediate VM processing
        You can customize this logic based on your specific criteria
        """
        # Only process if listing is suitable
        if not is_suitable:
            return False
        
        # Additional filters can be added here
        # For example: minimum price threshold
        if total_price < 15.0:
            print(f"⏭️  SKIP VM: Price £{total_price:.2f} below minimum threshold")
            return False
        
        # Check for specific high-value items
        high_value_items = ['switch', 'oled', 'lite', 'switch_box', 'oled_box', 'lite_box']
        has_high_value_item = any(detected_objects.get(item, 0) > 0 for item in high_value_items)
        
        if not has_high_value_item:
            print(f"⏭️  SKIP VM: No high-value items detected")
            return False
        
        print(f"🎯 TRIGGER VM: Listing meets criteria for immediate processing")
        return True

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
        FIXED: Now checks if detected_objects has ANY items before adding misc_games
        Returns: (total_revenue, expected_profit, profit_percentage, display_objects, item_revenues)
        """
        debug_function_call("calculate_vinted_revenue")
        import re
        
        game_classes = [
            '1_2_switch', 'animal_crossing', 'arceus_p', 'bow_z', 'bros_deluxe_m', 'crash_sand',
            'dance', 'diamond_p', 'evee', 'fifa_23', 'fifa_24', 'gta','just_dance', 'kart_m', 'kirby',
            'lets_go_p', 'links_z', 'luigis', 'mario_maker_2', 'mario_sonic', 'mario_tennis', 'minecraft',
            'minecraft_dungeons', 'minecraft_story', 'miscellanious_sonic', 'odyssey_m', 'other_mario',
            'party_m', 'rocket_league', 'scarlet_p', 'shield_p', 'shining_p', 'skywards_z', 'smash_bros',
            'snap_p', 'splatoon_2', 'splatoon_3', 'super_m_party', 'super_mario_3d', 'switch_sports',
            'sword_p', 'tears_z', 'violet_p'
        ]

        all_prices = self.fetch_all_prices()

        # CRITICAL FIX: Check if detected_objects has ANY non-zero items
        has_any_detections = any(
            detected_objects.get(item, 0) > 0 
            for item in detected_objects.keys()
        )
        
        # Count detected games from YOLO
        detected_games_count = sum(detected_objects.get(game, 0) for game in game_classes)
        
        # Extract games mentioned in text
        text_games_count = self.detect_anonymous_games_vinted(title, description)

        # CRITICAL FIX: Only calculate misc games if we have ANY detections
        # This prevents misc_games from being added to completely empty listings
        if has_any_detections:
            # Calculate misc games (text mentions minus detected, capped at misc_games_cap)
            misc_games_count_uncapped = max(0, text_games_count - detected_games_count)
            misc_games_count = min(misc_games_count_uncapped, misc_games_cap)
            
            if misc_games_count_uncapped > misc_games_cap:
                print(f"🎮 MISC GAMES CAP APPLIED: {misc_games_count_uncapped} → {misc_games_count} (cap: {misc_games_cap})")
            
            # Calculate misc games revenue
            misc_games_revenue = misc_games_count * miscellaneous_games_price
            
            # Add misc_games to detected_objects for display
            if misc_games_count > 0:
                detected_objects['misc_games'] = misc_games_count
                print(f"🎮 MISC GAMES ADDED TO DETECTED_OBJECTS: {misc_games_count} games = £{misc_games_revenue:.2f}")
        else:
            # FIX: No detections at all - don't add any misc games
            misc_games_count = 0
            misc_games_revenue = 0.0
            print(f"🎮 MISC GAMES SKIPPED: No detections in listing (detected_objects empty)")
        
        # Track per-item revenue
        item_revenues = {}

        # Add misc games revenue to tracking (only if > 0)
        if misc_games_count > 0:
            item_revenues['misc_games'] = misc_games_revenue

        # Handle box adjustments (remove items that are part of boxes)
        adjustments = {
            'oled_box': ['switch', 'comfort_h', 'tv_white'],
            'switch_box': ['switch', 'comfort_h', 'tv_black'],
            'lite_box': ['lite']
        }

        for box, items in adjustments.items():
            box_count = detected_objects.get(box, 0)
            for item in items:
                detected_objects[item] = max(0, detected_objects.get(item, 0) - box_count)

        # Remove switch_screen (not a revenue item)
        detected_objects.pop('switch_screen', None)

        # Start with misc games revenue
        total_revenue = misc_games_revenue

        # Calculate revenue from detected objects
        for item, count in detected_objects.items():
            # Skip misc_games since we already added it
            if item == 'misc_games':
                continue
                
            if isinstance(count, str):
                count_match = re.match(r'(\d+)', count)
                count = int(count_match.group(1)) if count_match else 0

            if count > 0 and item in all_prices:
                item_price = all_prices[item]
                
                # Special handling for pro controllers
                if item == 'controller' and 'pro' in title.lower():
                    item_price += 7.50
                
                item_revenue = item_price * count
                total_revenue += item_revenue
                
                # Store per-item revenue
                item_revenues[item] = item_revenue
        
        # Debug output (now only shows items that exist)
        for item, count in detected_objects.items():
            if count > 0:
                price_info = all_prices.get(item, 'NOT IN PRICES')
                if item == 'misc_games':
                    price_info = f"£{miscellaneous_games_price:.2f} each"
                print(f"DEBUG ITEM: {item} = {count}, price = {price_info}")

        # Calculate profit
        expected_profit = total_revenue - listing_price
        profit_percentage = (expected_profit / listing_price) * 100 if listing_price > 0 else 0

        print(f"Listing Price: £{listing_price:.2f}")
        print(f"Total Expected Revenue: £{total_revenue:.2f}")
        print(f"Expected Profit/Loss: £{expected_profit:.2f} ({profit_percentage:.2f}%)")

        # Create display_objects (items with count > 0)
        display_objects = {k: v for k, v in detected_objects.items() if v > 0}

        # Return all values including the MODIFIED detected_objects
        return total_revenue, expected_profit, profit_percentage, display_objects, item_revenues



    def perform_detection_on_listing_images(self, model, listing_dir):
        """
        COMPLETELY FIXED: Now properly tracks confidence AND calculates revenue for EVERY detected item
        """
        if not os.path.isdir(listing_dir):
            return {}, [], {}, {}

        detected_objects = {class_name: [] for class_name in CLASS_NAMES}
        processed_images = []
        
        # FIXED: Track confidence for ALL classes, not just mutually exclusive ones
        max_confidence_per_class = {class_name: 0.0 for class_name in CLASS_NAMES}

        image_files = [f for f in os.listdir(listing_dir) if f.endswith('.png')]
        if not image_files:
            return {class_name: 0 for class_name in CLASS_NAMES}, processed_images, max_confidence_per_class, {}

        for image_file in image_files:
            image_path = os.path.join(listing_dir, image_file)
            try:
                img = cv2.imread(image_path)
                if img is None:
                    continue

                image_detections = {class_name: 0 for class_name in CLASS_NAMES}
                results = model(img, verbose=False)
                
                # Process each detection
                for result in results:
                    for box in result.boxes.cpu().numpy():
                        class_id = int(box.cls[0])
                        confidence = float(box.conf[0])
                        
                        if class_id < len(CLASS_NAMES):
                            class_name = CLASS_NAMES[class_id]
                            min_confidence = HIGHER_CONFIDENCE_ITEMS.get(class_name, GENERAL_CONFIDENCE_MIN)
                            
                            if confidence >= min_confidence:
                                # CRITICAL FIX: Update max confidence for ALL classes
                                max_confidence_per_class[class_name] = max(
                                    max_confidence_per_class[class_name], 
                                    confidence
                                )
                                
                                # Count detections (except mutually exclusive items)
                                if class_name not in ['switch', 'oled', 'lite', 'switch_box', 
                                                    'oled_box', 'lite_box', 'switch_in_tv', 'oled_in_tv']:
                                    image_detections[class_name] += 1
                                
                                # Draw bounding boxes
                                x1, y1, x2, y2 = map(int, box.xyxy[0])
                                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                cv2.putText(img, f"{class_name} ({confidence:.2f})", (x1, y1 - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.625, (0, 255, 0), 2)

                # Accumulate counts per class
                for class_name, count in image_detections.items():
                    detected_objects[class_name].append(count)

                # Store processed image
                processed_images.append(Image.fromarray(cv2.cvtColor(
                    cv2.copyMakeBorder(img, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=[0, 0, 0]),
                    cv2.COLOR_BGR2RGB)))

            except Exception as e:
                print(f"Error processing image {image_path}: {str(e)}")
                continue

        # Finalize counts (max across images)
        final_detected_objects = {
            class_name: max(counts) if counts else 0 
            for class_name, counts in detected_objects.items()
        }
        
        # Handle mutually exclusive items
        confidences_for_exclusive = {
            item: max_confidence_per_class[item] 
            for item in ['switch', 'oled', 'lite', 'switch_box', 'oled_box', 
                        'lite_box', 'switch_in_tv', 'oled_in_tv']
        }
        final_detected_objects = self.handle_mutually_exclusive_items_vinted(
            final_detected_objects, 
            confidences_for_exclusive
        )
        
        # Apply game deduplication
        vinted_game_classes = [
            '1_2_switch', 'animal_crossing', 'arceus_p', 'bow_z', 'bros_deluxe_m', 'crash_sand',
            'dance', 'diamond_p', 'evee', 'fifa_23', 'fifa_24', 'gta', 'just_dance', 'kart_m', 'kirby',
            'lets_go_p', 'links_z', 'luigis', 'mario_maker_2', 'mario_sonic', 'mario_tennis', 'minecraft',
            'minecraft_dungeons', 'minecraft_story', 'miscellanious_sonic', 'odyssey_m', 'other_mario',
            'party_m', 'rocket_league', 'scarlet_p', 'shield_p', 'shining_p', 'skywards_z', 'smash_bros',
            'snap_p', 'splatoon_2', 'splatoon_3', 'super_m_party', 'super_mario_3d', 'switch_sports',
            'sword_p', 'tears_z', 'violet_p'
        ]
        
        games_before_cap = {}
        for game_class in vinted_game_classes:
            if final_detected_objects.get(game_class, 0) > 1:
                games_before_cap[game_class] = final_detected_objects[game_class]
                final_detected_objects[game_class] = 1
        
        if games_before_cap:
            print("🎮 VINTED GAME DEDUPLICATION APPLIED:")
            for game, original_count in games_before_cap.items():
                print(f"  • {game}: {original_count} → 1")
        
        # Apply price threshold filtering
        try:
            listing_price = getattr(self, 'current_listing_price_float', 0.0)
            
            if listing_price > 0 and listing_price < PRICE_THRESHOLD:
                filtered_classes = []
                for switch_class in NINTENDO_SWITCH_CLASSES:
                    if final_detected_objects.get(switch_class, 0) > 0:
                        filtered_classes.append(switch_class)
                        final_detected_objects[switch_class] = 0
                        max_confidence_per_class[switch_class] = 0.0
                
                if filtered_classes:
                    print(f"🚫 PRICE FILTER: Removed Nintendo Switch detections (£{listing_price:.2f} < £{PRICE_THRESHOLD:.2f})")
        except Exception as price_filter_error:
            print(f"⚠️ Warning: Price filtering failed: {price_filter_error}")
        
        # CRITICAL FIX: Calculate per-item revenue HERE using detected counts
        all_prices = self.fetch_all_prices()
        item_revenues = {}
        
        for item, count in final_detected_objects.items():
            if count > 0 and item in all_prices:
                item_price = all_prices[item]
                item_revenue = item_price * count
                item_revenues[item] = item_revenue
                
                # DEBUG OUTPUT
                if print_debug:
                    print(f"💰 REVENUE: {item} × {count} = £{item_revenue:.2f} (confidence: {max_confidence_per_class[item]:.2%})")
        
        # Return: detected_objects, processed_images, confidences, revenues
        return final_detected_objects, processed_images, max_confidence_per_class, item_revenues

    def download_images_for_listing(self, driver, listing_dir):
        """
        ENHANCED: Download listing images with carousel detection for 5+ images
        - If 4 or fewer listing images: Use normal scraping (current behavior)
        - If 5+ listing images: Click an image to open carousel, then scrape from carousel
        """
        import concurrent.futures
        import requests
        from PIL import Image
        from io import BytesIO
        import os
        import hashlib
        
        # Wait for the page to fully load
        try:
            WebDriverWait(driver, 10, poll_frequency=0.05).until(
                EC.presence_of_element_located((By.TAG_NAME, "img"))
            )
        except TimeoutException:
            print("  ▶ Timeout waiting for images to load")
            return []
        
        # STEP 1: Count listing images to determine which mode to use
        print("  ▶ STEP 1: Detecting listing image count...")
        
        listing_img_selectors = [
            "img.web_ui__Image__content[data-testid^='item-photo-']",
            "img[data-testid^='item-photo-']",
        ]
        
        listing_images = []
        for selector in listing_img_selectors:
            listing_images = driver.find_elements(By.CSS_SELECTOR, selector)
            if listing_images:
                print(f"  ▶ Found {len(listing_images)} listing images using selector: {selector}")
                break
        
        if not listing_images:
            print("  ▶ No listing images found")
            return []
        
        listing_image_count = len(listing_images)
        print(f"  ▶ Listing image count: {listing_image_count}")
        
        # STEP 2: Decide which mode to use based on count
        if listing_image_count <= 4:
            # NORMAL MODE: 4 or fewer images - use existing logic
            print(f"  ▶ MODE: NORMAL (≤4 images) - Using standard scraping")
            
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
            
            valid_urls = []
            seen_urls = set()
            
            if print_images_backend_info:
                print(f"  ▶ Processing {len(imgs)} images")
            
            for img in imgs:
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
                    # Remove query parameters and fragments for duplicate detection
                    normalized_url = src.split('?')[0].split('#')[0]
                    
                    if normalized_url in seen_urls:
                        if print_images_backend_info:
                            print(f"    ⏭️  Skipping duplicate URL: {normalized_url[:50]}...")
                        continue
                    
                    seen_urls.add(normalized_url)
                    
                    # Exclude profile pictures and small icons based on URL patterns
                    if (
                        '/50x50/' in src or 
                        '/75x75/' in src or 
                        '/100x100/' in src or
                        'circle' in parent_classes.lower() or
                        src.endswith('.svg') or
                        any(size in src for size in ['/32x32/', '/64x64/', '/128x128/'])
                    ):
                        if print_images_backend_info:
                            print(f"    ⏭️  Skipping filtered image: {src[:50]}...")
                        continue
                    
                    # Only include images that look like product photos
                    if (
                        '/f800/' in src or 
                        '/f1200/' in src or 
                        '/f600/' in src or
                        (('vinted' in src.lower() or 'cloudinary' in src.lower() or 'amazonaws' in src.lower()) and
                        not any(small_size in src for small_size in ['/50x', '/75x', '/100x', '/thumb']))
                    ):
                        valid_urls.append(src)
                        if print_images_backend_info:
                            print(f"    ✅ Added valid image URL: {src[:50]}...")
        
        else:
            # CAROUSEL MODE: 5+ images - click image to open carousel
            print(f"  ▶ MODE: CAROUSEL (>4 images) - Clicking image to open carousel")
            
            try:
                # STEP 3: Click on the first listing image to open carousel
                first_listing_image = listing_images[0]
                print(f"  ▶ STEP 2: Clicking first listing image to open carousel...")
                
                # Scroll into view
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", first_listing_image)
                time.sleep(0.5)
                
                # Try multiple click methods
                clicked = False
                
                # Method 1: Direct click
                try:
                    first_listing_image.click()
                    clicked = True
                    print(f"  ▶ ✅ Clicked image (direct click)")
                except Exception as e1:
                    print(f"  ▶ ⚠️ Direct click failed: {e1}")
                    
                    # Method 2: JavaScript click
                    try:
                        driver.execute_script("arguments[0].click();", first_listing_image)
                        clicked = True
                        print(f"  ▶ ✅ Clicked image (JavaScript click)")
                    except Exception as e2:
                        print(f"  ▶ ⚠️ JavaScript click failed: {e2}")
                        
                        # Method 3: ActionChains click
                        try:
                            from selenium.webdriver.common.action_chains import ActionChains
                            ActionChains(driver).move_to_element(first_listing_image).click().perform()
                            clicked = True
                            print(f"  ▶ ✅ Clicked image (ActionChains click)")
                        except Exception as e3:
                            print(f"  ▶ ❌ All click methods failed: {e3}")
                
                if not clicked:
                    print(f"  ▶ ❌ Failed to click image - falling back to normal mode")
                    # Fallback to normal mode logic - but avoid infinite recursion
                    # Just use the listing images we already found
                    valid_urls = []
                    seen_urls = set()
                    
                    for img in listing_images:
                        src = img.get_attribute("src")
                        if src and src.startswith('http'):
                            normalized_url = src.split('?')[0].split('#')[0]
                            if normalized_url not in seen_urls:
                                seen_urls.add(normalized_url)
                                valid_urls.append(src)
                else:
                    # STEP 4: Wait for carousel to appear
                    print(f"  ▶ STEP 3: Waiting for carousel to appear...")
                    time.sleep(1.5)  # Give carousel time to animate
                    
                    # STEP 5: Find all carousel images
                    print(f"  ▶ STEP 4: Scanning for carousel images...")
                    
                    carousel_selectors = [
                        'img[data-testid="image-carousel-image"]',
                        'img.image-carousel__image',
                        'img[alt="post"]',
                    ]
                    
                    carousel_images = []
                    for selector in carousel_selectors:
                        carousel_images = driver.find_elements(By.CSS_SELECTOR, selector)
                        if carousel_images:
                            print(f"  ▶ Found {len(carousel_images)} carousel images using selector: {selector}")
                            break
                    
                    if not carousel_images:
                        print(f"  ▶ ⚠️ No carousel images found - using listing images as fallback")
                        # Use the listing images we already found
                        valid_urls = []
                        seen_urls = set()
                        
                        for img in listing_images:
                            src = img.get_attribute("src")
                            if src and src.startswith('http'):
                                normalized_url = src.split('?')[0].split('#')[0]
                                if normalized_url not in seen_urls:
                                    seen_urls.add(normalized_url)
                                    valid_urls.append(src)
                    else:
                        # STEP 6: Extract URLs from carousel images
                        valid_urls = []
                        seen_urls = set()
                        
                        print(f"  ▶ STEP 5: Extracting URLs from {len(carousel_images)} carousel images...")
                        
                        for idx, img in enumerate(carousel_images):
                            src = img.get_attribute("src")
                            
                            if src and src.startswith('http'):
                                # Remove query parameters and fragments for duplicate detection
                                normalized_url = src.split('?')[0].split('#')[0]
                                
                                if normalized_url in seen_urls:
                                    if print_images_backend_info:
                                        print(f"    ⏭️  Skipping duplicate carousel URL: {normalized_url[:50]}...")
                                    continue
                                
                                seen_urls.add(normalized_url)
                                
                                # Carousel images are always valid listing images, no filtering needed
                                valid_urls.append(src)
                                if print_images_backend_info:
                                    print(f"    ✅ Added carousel image URL {idx+1}: {src[:50]}...")
                        
                        # OPTIMIZATION: No need to close carousel - tab will be closed immediately after this
                        print(f"  ▶ STEP 6: Carousel will be closed when tab closes (optimization)")
            
            except Exception as carousel_error:
                print(f"  ▶ ❌ Carousel mode error: {carousel_error}")
                print(f"  ▶ Falling back to listing images...")
                import traceback
                traceback.print_exc()
                # Fallback: use the listing images we already found
                valid_urls = []
                seen_urls = set()
                
