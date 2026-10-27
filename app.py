import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- Your existing logic ---
def check_brackets(text: str):
    pairs = {')': '(', ']': '[', '}': '{'}
    opening = set(pairs.values())
    stack = [] 
    for i, ch in enumerate(text):
        if ch in opening:
            stack.append((ch, i))
        elif ch in pairs:
            if not stack:
                return f"Error: unmatched '{ch}' at index {i}"
            top_char, top_idx = stack.pop()
            if top_char != pairs[ch]:
                return f"Error: '{ch}' at index {i} does not match '{top_char}' at index {top_idx}"
    if stack:
        ch, idx = stack[-1]
        return f"Error: unclosed '{ch}' at index {idx}"
    return "OK: all brackets balanced"

# --- Simple Web Interface ---
HTML_PAGE = """
<!doctype html>
<title>Bracket Checker</title>
<h2>Stack Bracket Checker</h2>
<form method="POST">
  <input type="text" name="text" placeholder="e.g. {[()()]}" style="width:300px; padding:5px;">
  <button type="submit">Check</button>
</form>
{% if result %}
  <h3>Result:</h3>
  <p style="background:#eee; padding:10px; font-family:monospace;">{{ result }}</p>
{% endif %}
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        user_input = request.form.get('text', '')
        result = check_brackets(user_input)
    return render_template_string(HTML_PAGE, result=result)

if __name__ == '__main__':
    # Render provides a PORT env variable; default to 5000 locally
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
