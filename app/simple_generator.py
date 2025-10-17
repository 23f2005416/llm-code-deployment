# app/simple_generator.py
class SimpleCodeGenerator:
    """Simple code generator for testing GitHub integration"""
    
    def generate_from_brief(self, brief: str) -> dict:
        """Generate basic code files from brief"""
        
        # Simple template based on brief content
        if "calculator" in brief.lower():
            return self._generate_calculator()
        elif "counter" in brief.lower():
            return self._generate_counter()
        else:
            return self._generate_basic_app(brief)
    
    def _generate_basic_app(self, brief: str) -> dict:
        return {
            "index.html": f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .feature {{ margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center mb-4">🚀 Generated Application</h1>
        <div class="feature">
            <h3>About This App</h3>
            <p>{brief}</p>
        </div>
        <div class="feature">
            <h3>Features</h3>
            <ul>
                <li>Automatically generated</li>
                <li>Responsive design</li>
                <li>Bootstrap 5 styling</li>
                <li>GitHub Pages ready</li>
            </ul>
        </div>
        <div class="text-center mt-4">
            <button class="btn btn-primary" onclick="showMessage()">Click Me!</button>
            <p id="message" class="mt-3 text-success"></p>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>""",
            "script.js": """function showMessage() {
    const messages = [
        "Hello! This app is working!",
        "GitHub integration successful!",
        "Auto-deployment is awesome!",
        "You clicked the button! 🎉"
    ];
    const randomMessage = messages[Math.floor(Math.random() * messages.length)];
    document.getElementById('message').textContent = randomMessage;
}

console.log("Application loaded successfully!");""",
            "style.css": """.feature {
    border-left: 4px solid #007bff;
}

.btn-primary {
    background: linear-gradient(45deg, #007bff, #0056b3);
    border: none;
    padding: 10px 20px;
    border-radius: 25px;
}

.container {
    margin-top: 20px;
}"""
        }
    
    def _generate_calculator(self) -> dict:
        return {
            "index.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculator App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .calculator { max-width: 300px; margin: 50px auto; padding: 20px; background: #333; border-radius: 10px; }
        .display { background: #000; color: white; text-align: right; padding: 10px; font-size: 24px; margin-bottom: 10px; border-radius: 5px; }
        .btn { margin: 2px; }
    </style>
</head>
<body>
    <div class="calculator">
        <div class="display" id="display">0</div>
        <div class="row">
            <button class="btn btn-light col-3" onclick="clearDisplay()">C</button>
            <button class="btn btn-light col-3" onclick="appendToDisplay('/')">/</button>
            <button class="btn btn-light col-3" onclick="appendToDisplay('*')">×</button>
            <button class="btn btn-light col-3" onclick="appendToDisplay('-')">-</button>
        </div>
        <div class="row">
            <button class="btn btn-secondary col-3" onclick="appendToDisplay('7')">7</button>
            <button class="btn btn-secondary col-3" onclick="appendToDisplay('8')">8</button>
            <button class="btn btn-secondary col-3" onclick="appendToDisplay('9')">9</button>
            <button class="btn btn-light col-3" onclick="appendToDisplay('+')">+</button>
        </div>
        <div class="row">
            <button class="btn btn-secondary col-3" onclick="appendToDisplay('4')">4</button>
            <button class="btn btn-secondary col-3" onclick="appendToDisplay('5')">5</button>
            <button class="btn btn-secondary col-3" onclick="appendToDisplay('6')">6</button>
            <button class="btn btn-success col-3" onclick="calculate()">=</button>
        </div>
        <div class="row">
            <button class="btn btn-secondary col-9" onclick="appendToDisplay('0')">0</button>
            <button class="btn btn-secondary col-3" onclick="appendToDisplay('.')">.</button>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>""",
            "script.js": """let currentDisplay = '0';
let shouldResetDisplay = false;

function updateDisplay() {
    document.getElementById('display').textContent = currentDisplay;
}

function appendToDisplay(value) {
    if (currentDisplay === '0' || shouldResetDisplay) {
        currentDisplay = value;
        shouldResetDisplay = false;
    } else {
        currentDisplay += value;
    }
    updateDisplay();
}

function clearDisplay() {
    currentDisplay = '0';
    updateDisplay();
}

function calculate() {
    try {
        currentDisplay = eval(currentDisplay.replace('×', '*')).toString();
    } catch (error) {
        currentDisplay = 'Error';
    }
    shouldResetDisplay = true;
    updateDisplay();
}

updateDisplay();"""
        }
    
    def _generate_counter(self) -> dict:
        return {
            "index.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Counter App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .counter-container { text-align: center; margin-top: 100px; }
        .count-display { font-size: 4rem; font-weight: bold; margin: 20px 0; }
        .btn { margin: 5px; font-size: 1.2rem; }
    </style>
</head>
<body>
    <div class="counter-container">
        <h1>Counter Application</h1>
        <div class="count-display" id="count">0</div>
        <div>
            <button class="btn btn-danger btn-lg" onclick="decrement()">-1</button>
            <button class="btn btn-warning btn-lg" onclick="resetCounter()">Reset</button>
            <button class="btn btn-success btn-lg" onclick="increment()">+1</button>
        </div>
        <div class="mt-4">
            <button class="btn btn-info" onclick="incrementBy(5)">+5</button>
            <button class="btn btn-info" onclick="incrementBy(10)">+10</button>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>""",
            "script.js": """let count = 0;

function updateDisplay() {
    document.getElementById('count').textContent = count;
    document.body.style.backgroundColor = count < 0 ? '#ffebee' : count > 0 ? '#e8f5e8' : '#f5f5f5';
}

function increment() {
    count++;
    updateDisplay();
}

function decrement() {
    count--;
    updateDisplay();
}

function resetCounter() {
    count = 0;
    updateDisplay();
}

function incrementBy(value) {
    count += value;
    updateDisplay();
}

updateDisplay();"""
        }
    
    def update_existing_app(self, existing_code: dict, update_brief: str) -> dict:
        """Update existing app code based on round 2 brief"""
        
        # Detect what kind of update is requested
        brief_lower = update_brief.lower()
        
        # Check for common update patterns
        if any(keyword in brief_lower for keyword in ['dark mode', 'dark', 'theme']):
            return self._add_dark_mode(existing_code)
        elif any(keyword in brief_lower for keyword in ['search', 'filter']):
            return self._add_search_functionality(existing_code)
        elif any(keyword in brief_lower for keyword in ['favorite', 'bookmark', 'save']):
            return self._add_favorites(existing_code)
        elif any(keyword in brief_lower for keyword in ['chart', 'graph', 'visualization']):
            return self._add_charts(existing_code)
        else:
            # Generic update - enhance existing features
            return self._enhance_existing(existing_code, update_brief)

    def _add_dark_mode(self, existing_code: dict) -> dict:
        """Add dark mode toggle to existing app"""
        html = existing_code.get("index.html", "")
        css = existing_code.get("style.css", "")
        js = existing_code.get("script.js", "")
        
        # Add dark mode toggle button to HTML
        if '<body>' in html:
            dark_toggle = '''
    <!-- Dark Mode Toggle -->
    <div class="dark-mode-toggle">
        <button id="darkModeToggle" class="btn btn-outline-secondary">🌙 Dark Mode</button>
    </div>
    '''
            html = html.replace('<body>', '<body>\n' + dark_toggle)
        
        # Add dark mode CSS
        dark_css = '''
    /* Dark Mode Styles */
    body.dark-mode {
        background-color: #1a1a1a;
        color: #ffffff;
    }

    body.dark-mode .container,
    body.dark-mode .card,
    body.dark-mode .feature-card {
        background-color: #2d2d2d;
        color: #ffffff;
    }

    body.dark-mode .btn {
        border-color: #555;
    }

    .dark-mode-toggle {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
    }
    '''
        css += dark_css
        
        # Add dark mode JavaScript
        dark_js = '''
    // Dark Mode Functionality
    function toggleDarkMode() {
        document.body.classList.toggle('dark-mode');
        const toggleBtn = document.getElementById('darkModeToggle');
        if (document.body.classList.contains('dark-mode')) {
            toggleBtn.textContent = '☀️ Light Mode';
            localStorage.setItem('darkMode', 'enabled');
        } else {
            toggleBtn.textContent = '🌙 Dark Mode';
            localStorage.setItem('darkMode', 'disabled');
        }
    }

    // Initialize dark mode
    document.addEventListener('DOMContentLoaded', function() {
        const darkModeToggle = document.getElementById('darkModeToggle');
        if (darkModeToggle) {
            darkModeToggle.addEventListener('click', toggleDarkMode);
        }
        
        // Check saved preference
        if (localStorage.getItem('darkMode') === 'enabled') {
            document.body.classList.add('dark-mode');
            if (darkModeToggle) darkModeToggle.textContent = '☀️ Light Mode';
        }
    });
    '''
        js += dark_js
        
        return {
            "index.html": html,
            "style.css": css,
            "script.js": js
        }

    def _add_search_functionality(self, existing_code: dict) -> dict:
        """Add search functionality to existing app"""
        html = existing_code.get("index.html", "")
        css = existing_code.get("style.css", "")
        js = existing_code.get("script.js", "")
        
        # Add search bar to HTML
        if '<body>' in html:
            search_bar = '''
    <!-- Search Functionality -->
    <div class="search-container mb-4">
        <div class="input-group">
            <input type="text" id="searchInput" class="form-control" placeholder="Search...">
            <button id="searchButton" class="btn btn-primary">Search</button>
        </div>
        <div id="searchResults" class="mt-3"></div>
    </div>
    '''
            html = html.replace('<body>', '<body>\n' + search_bar)
        
        # Add search CSS
        search_css = '''
    /* Search Styles */
    .search-container {
        max-width: 600px;
        margin: 0 auto 20px auto;
    }

    .search-result-item {
        padding: 10px;
        margin: 5px 0;
        background: #f8f9fa;
        border-radius: 5px;
        border-left: 3px solid #007bff;
    }

    .search-highlight {
        background-color: yellow;
        font-weight: bold;
    }
    '''
        css += search_css
        
        # Add search JavaScript
        search_js = '''
    // Search Functionality
    function performSearch() {
        const searchTerm = document.getElementById('searchInput').value.toLowerCase();
        const resultsContainer = document.getElementById('searchResults');
        
        if (!searchTerm) {
            resultsContainer.innerHTML = '<p class="text-muted">Enter a search term</p>';
            return;
        }
        
        // Simple content search (can be enhanced based on app content)
        const pageContent = document.body.textContent.toLowerCase();
        const matches = pageContent.includes(searchTerm);
        
        if (matches) {
            resultsContainer.innerHTML = `
                <div class="search-result-item">
                    <strong>Found matches for:</strong> "${searchTerm}"
                    <br><small>Content contains your search term</small>
                </div>
            `;
            
            // Highlight text (simple implementation)
            highlightText(searchTerm);
        } else {
            resultsContainer.innerHTML = '<p class="text-muted">No results found</p>';
        }
    }

    function highlightText(searchTerm) {
        // Simple text highlighting
        const bodyText = document.body.innerHTML;
        const highlighted = bodyText.replace(
            new RegExp(searchTerm, 'gi'),
            match => `<span class="search-highlight">${match}</span>`
        );
        document.body.innerHTML = highlighted;
    }

    // Event listeners
    document.addEventListener('DOMContentLoaded', function() {
        const searchButton = document.getElementById('searchButton');
        const searchInput = document.getElementById('searchInput');
        
        if (searchButton) {
            searchButton.addEventListener('click', performSearch);
        }
        
        if (searchInput) {
            searchInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    performSearch();
                }
            });
        }
    });
    '''
        js += search_js
        
        return {
            "index.html": html,
            "style.css": css,
            "script.js": js
        }

    def _add_favorites(self, existing_code: dict) -> dict:
        """Add favorites functionality to existing app"""
        html = existing_code.get("index.html", "")
        css = existing_code.get("style.css", "")
        js = existing_code.get("script.js", "")
        
        # Add favorites section to HTML
        if '<body>' in html:
            favorites_section = '''
    <!-- Favorites Section -->
    <div class="favorites-section mt-4">
        <h3>⭐ Favorites</h3>
        <div id="favoritesList" class="favorites-list"></div>
    </div>
    '''
            html = html.replace('</body>', favorites_section + '\n</body>')
        
        # Add favorites CSS
        favorites_css = '''
    /* Favorites Styles */
    .favorites-section {
        background: #fff3cd;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
    }

    .favorite-item {
        background: white;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .favorite-item button {
        background: none;
        border: none;
        color: #dc3545;
        cursor: pointer;
    }

    .add-to-favorites {
        background: #ffc107;
        border: none;
        padding: 5px 10px;
        border-radius: 3px;
        cursor: pointer;
    }
    '''
        css += favorites_css
        
        # Add favorites JavaScript
        favorites_js = '''
    // Favorites Functionality
    class FavoritesManager {
        constructor() {
            this.favorites = JSON.parse(localStorage.getItem('favorites')) || [];
            this.renderFavorites();
        }
        
        addFavorite(item) {
            if (!this.favorites.includes(item)) {
                this.favorites.push(item);
                this.saveFavorites();
                this.renderFavorites();
            }
        }
        
        removeFavorite(item) {
            this.favorites = this.favorites.filter(fav => fav !== item);
            this.saveFavorites();
            this.renderFavorites();
        }
        
        saveFavorites() {
            localStorage.setItem('favorites', JSON.stringify(this.favorites));
        }
        
        renderFavorites() {
            const favoritesList = document.getElementById('favoritesList');
            if (favoritesList) {
                if (this.favorites.length === 0) {
                    favoritesList.innerHTML = '<p class="text-muted">No favorites yet. Add some items to your favorites!</p>';
                } else {
                    favoritesList.innerHTML = this.favorites.map(item => `
                        <div class="favorite-item">
                            <span>${item}</span>
                            <button onclick="favoritesManager.removeFavorite('${item}')">❌</button>
                        </div>
                    `).join('');
                }
            }
        }
    }

    // Initialize favorites manager
    const favoritesManager = new FavoritesManager();

    // Function to add current item to favorites (example)
    function addCurrentToFavorites() {
        const itemName = document.title || 'Current Item';
        favoritesManager.addFavorite(itemName);
        alert(`Added "${itemName}" to favorites!`);
    }

    // Add favorite buttons to relevant elements
    document.addEventListener('DOMContentLoaded', function() {
        // Example: Add favorite button to main content
        const mainContent = document.querySelector('.container, .app-container');
        if (mainContent) {
            const favoriteBtn = document.createElement('button');
            favoriteBtn.className = 'add-to-favorites mb-3';
            favoriteBtn.innerHTML = '⭐ Add to Favorites';
            favoriteBtn.onclick = addCurrentToFavorites;
            mainContent.insertBefore(favoriteBtn, mainContent.firstChild);
        }
    });
    '''
        js += favorites_js
        
        return {
            "index.html": html,
            "style.css": css,
            "script.js": js
        }

    def _enhance_existing(self, existing_code: dict, update_brief: str) -> dict:
        """Generic enhancement of existing app"""
        html = existing_code.get("index.html", "")
        css = existing_code.get("style.css", "")
        js = existing_code.get("script.js", "")
        
        # Add enhancement notice
        enhancement_html = f'''
    <!-- Enhancement Update -->
    <div class="enhancement-notice alert alert-info">
        <h4>🚀 App Enhanced!</h4>
        <p><strong>Update:</strong> {update_brief}</p>
    </div>
    '''
        if '<body>' in html:
            html = html.replace('<body>', '<body>\n' + enhancement_html)
        
        # Enhanced CSS
        enhanced_css = '''
    /* Enhanced Styles */
    .enhancement-notice {
        border-left: 4px solid #17a2b8;
    }

    .feature-enhanced {
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    '''
        css += enhanced_css
        
        return {
            "index.html": html,
            "style.css": css,
            "script.js": js
        }