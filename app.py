from flask import Flask, render_template_string, request, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'super_secret_library_key' # For simple session management

def get_db_connection():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    return conn

# Simple Home / Login Page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM patrons WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('profile', patron_id=user['id']))
        else:
            return "Invalid username! Try 'alice123', 'bob_reader', etc.", 401

    return '''
        <h2>Library Patron Login</h2>
        <form method="post">
            Username: <input type="text" name="username" placeholder="e.g. alice123"><br><br>
            <input type="submit" value="Login">
        </form>
    '''

# VULNERABLE PROFILE ENDPOINT (IDOR)
@app.route('/patron/profile/<int:patron_id>')
def profile(patron_id):
    # 1. Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # 2. THE FIX: Enforce object-level authorization
    if session['user_id'] != patron_id:
        return "Access Denied: You are not authorized to view this profile.", 403
    
    # 3. Fetch and display data if authorized
    conn = get_db_connection()
    patron = conn.execute('SELECT * FROM patrons WHERE id = ?', (patron_id,)).fetchone()
    conn.close()
    
    if not patron:
        return "Patron not found", 404
    
    # Render profile including sensitive private notes
    template = '''
        <h2>Library Patron Portal</h2>
        <p><b>Logged in as user ID:</b> {{ session['user_id'] }}</p>
        <hr>
        <h3>Profile Details for ID: {{ patron['id'] }}</h3>
        <p><b>Username:</b> {{ patron['username'] }}</p>
        <p><b>Full Name:</b> {{ patron['full_name'] }}</p>
        <p><b>Email:</b> {{ patron['email'] }}</p>
        <p><b>Current Book:</b> {{ patron['borrowed_book'] }}</p>
        <p style="color: red;"><b>Private Notes (Sensitive):</b> {{ patron['private_notes'] }}</p>
        <br>
        <a href="/">Logout</a> | <a href="/patron/profile/{{ patron['id'] + 1 }}">Next ID &gt;&gt;</a>
    '''
    return render_template_string(template, patron=patron)

if __name__ == '__main__':
    app.run(debug=True, port=5000) 