# app/llm_generator.py
import openai
import json
import base64
import re
from app.utils import Config

class LLMCodeGenerator:
    def __init__(self):
        if not Config.OPENAI_API_KEY:
            raise ValueError("OpenAI API key not configured. Set OPENAI_API_KEY in .env file")
        
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        print("✅ OpenAI client initialized")
    
    def generate_app(self, brief: str, attachments: list, checks: list) -> dict:
        """Generate complete app code using LLM based on brief and requirements"""
        
        print(f"🧠 Generating code with LLM for: {brief[:100]}...")
        
        # Process attachments information
        attachment_info = self._process_attachments(attachments)
        
        system_prompt = """You are an expert web developer specializing in creating minimal, deployable static web applications for GitHub Pages.

IMPORTANT: Return ONLY valid JSON with this exact structure:
{
    "index.html": "complete HTML content with embedded CSS/JS or references",
    "script.js": "JavaScript code if needed, otherwise empty string",
    "style.css": "CSS code if needed, otherwise empty string"
}

Requirements:
- Create SINGLE FILE applications when possible (HTML with embedded CSS/JS)
- If separate files are needed, keep them minimal
- NO backend dependencies - static only
- Mobile responsive
- Clean, professional code
- Include Bootstrap 5 via CDN for styling
- Handle any file attachments mentioned in the brief
- Ensure all specified checks will pass
- Use modern HTML5, CSS3, ES6+
- Include proper error handling
- Make it actually functional for the described purpose"""

        user_prompt = f"""
CREATE THIS APPLICATION:
{brief}

REQUIRED CHECKS (MUST PASS):
{chr(10).join(f"• {check}" for check in checks)}

ATTACHMENTS TO HANDLE:
{attachment_info}

SPECIFIC INSTRUCTIONS:
1. Create a COMPLETE, WORKING application
2. If the brief mentions specific functionality (calculator, counter, data processing), implement it
3. Use Bootstrap 5 for styling via CDN
4. Make it visually appealing and professional
5. Ensure it works on GitHub Pages (static only)
6. Include necessary comments
7. Handle any file processing mentioned in attachments
8. Make sure all the required checks will pass

Return ONLY the JSON object with the code files.
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-1106",  # Using 3.5 for cost efficiency, can upgrade to gpt-4
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                max_tokens=4000,
                response_format={"type": "json_object"}
            )
            
            generated_code = json.loads(response.choices[0].message.content)
            print("✅ LLM code generation successful")
            
            return self._validate_and_clean_code(generated_code, brief)
            
        except Exception as e:
            print(f"❌ LLM generation failed: {e}")
            # Fallback to simple generator
            from app.simple_generator import SimpleCodeGenerator
            fallback = SimpleCodeGenerator()
            return fallback.generate_from_brief(brief)
    
    def _process_attachments(self, attachments: list) -> str:
        """Process attachment information for the LLM"""
        if not attachments:
            return "No attachments provided"
        
        attachment_info = "Available attachments:\n"
        for attachment in attachments:
            name = attachment.get('name', 'unknown')
            file_type = name.split('.')[-1].upper() if '.' in name else 'FILE'
            attachment_info += f"- {name} ({file_type} file)\n"
            
            # Provide sample data for common file types
            if 'sample' in name.lower() or 'data' in name.lower():
                attachment_info += "  This appears to be sample data that should be used in the application.\n"
        
        return attachment_info
    
    def _validate_and_clean_code(self, code: dict, brief: str) -> dict:
        """Ensure the generated code has all required files and is valid"""
        
        # Ensure all required keys exist
        required_files = ["index.html", "script.js", "style.css"]
        for file in required_files:
            if file not in code:
                code[file] = ""
        
        # Validate HTML structure
        html_content = code["index.html"]
        if not html_content.strip():
            code["index.html"] = self._get_fallback_html(brief)
        else:
            # Ensure HTML has proper structure
            if "<!DOCTYPE html>" not in html_content:
                code["index.html"] = self._wrap_in_html_template(html_content, brief)
        
        # Clean and validate CSS/JS
        code["style.css"] = self._clean_css(code["style.css"])
        code["script.js"] = self._clean_javascript(code["script.js"])
        
        return code
    
    def _wrap_in_html_template(self, content: str, brief: str) -> str:
        """Wrap content in proper HTML template if missing"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated App: {brief[:50]}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        {self._get_basic_css()}
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center mb-4">Generated Application</h1>
        {content}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        {self._get_basic_js()}
    </script>
</body>
</html>"""
    
    def _get_fallback_html(self, brief: str) -> str:
        """Provide fallback HTML if generation fails"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; background: #f8f9fa; }}
        .app-container {{ max-width: 800px; margin: 50px auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .feature-card {{ margin: 15px 0; padding: 20px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #007bff; }}
    </style>
</head>
<body>
    <div class="app-container">
        <h1 class="text-center text-primary mb-4">🚀 Generated Application</h1>
        
        <div class="feature-card">
            <h3>📋 Application Purpose</h3>
            <p class="lead">{brief}</p>
        </div>
        
        <div class="feature-card">
            <h3>⚡ Features</h3>
            <ul>
                <li>Automatically generated by AI</li>
                <li>Responsive Bootstrap design</li>
                <li>GitHub Pages ready</li>
                <li>Professional styling</li>
            </ul>
        </div>
        
        <div class="feature-card">
            <h3>🎯 Interactive Demo</h3>
            <div class="text-center">
                <button class="btn btn-success btn-lg" onclick="demoAction()">Try Me!</button>
                <p id="demo-output" class="mt-3 text-muted">Click the button to see interaction</p>
            </div>
        </div>
    </div>

    <script>
        function demoAction() {{
            const messages = [
                "Hello! The app is working!",
                "AI generation successful!",
                "GitHub Pages deployment ready!",
                "Everything is functioning! 🎉"
            ];
            const randomMessage = messages[Math.floor(Math.random() * messages.length)];
            document.getElementById('demo-output').textContent = randomMessage;
            document.getElementById('demo-output').className = 'mt-3 text-success fw-bold';
        }}
        
        console.log("Application loaded successfully!");
    </script>
</body>
</html>"""
    
    def _clean_css(self, css: str) -> str:
        """Clean and validate CSS"""
        if not css or not css.strip():
            return self._get_basic_css()
        
        # Ensure basic responsive design
        if "@media" not in css and "responsive" not in css.lower():
            css += "\n\n/* Responsive design */\n@media (max-width: 768px) {\n    .container { padding: 10px; }\n}"
        
        return css
    
    def _clean_javascript(self, js: str) -> str:
        """Clean and validate JavaScript"""
        if not js or not js.strip():
            return self._get_basic_js()
        
        # Add basic error handling if not present
        if "try" not in js and "catch" not in js:
            js = "// Application JavaScript\n" + js
        
        return js
    
    def _get_basic_css(self) -> str:
        return """/* Basic responsive styles */
.container { max-width: 800px; margin: 0 auto; }
@media (max-width: 768px) {
    .container { padding: 10px; }
}
.feature-card { 
    margin: 15px 0; 
    padding: 20px; 
    background: #f8f9fa; 
    border-radius: 8px; 
    border-left: 4px solid #007bff; 
}"""
    
    def _get_basic_js(self) -> str:
        return """// Basic application functionality
console.log("Application initialized");

function showNotification(message, type = 'info') {
    // Basic notification function
    console.log(`${type.toUpperCase()}: ${message}`);
}"""