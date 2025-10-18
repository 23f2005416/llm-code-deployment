import openai
import json
import base64
import re
from app.utils import Config

class LLMCodeGenerator:
    def __init__(self):
        if not Config.OPENAI_API_KEY:
            raise ValueError("OpenAI API key not configured. Set OPENAI_API_KEY in .env file")

        # For openai>=1.0.0 - new client syntax
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        print("✅ OpenAI client initialized (v1.0+)")

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
            # For openai>=1.0.0 - new API syntax
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                max_tokens=4000
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
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated App: {brief[:50]}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center mb-4">Generated Application</h1>
        {content}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>'''
    
    def _get_fallback_html(self, brief: str) -> str:
        """Provide fallback HTML if generation fails"""
        from app.simple_generator import SimpleCodeGenerator
        fallback = SimpleCodeGenerator()
        basic_app = fallback._generate_basic_app(brief)
        return basic_app["index.html"]
    
    def _clean_css(self, css: str) -> str:
        """Clean and validate CSS"""
        if not css or not css.strip():
            return "/* Basic styles */\n.container { max-width: 800px; margin: 0 auto; }"
        return css
    
    def _clean_javascript(self, js: str) -> str:
        """Clean and validate JavaScript"""
        if not js or not js.strip():
            return "// Application JavaScript\nconsole.log('App loaded');"
        return js
