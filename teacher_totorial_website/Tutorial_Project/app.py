from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'segun_secret_key'

# --- FAKE DATABASE ---
USERS = {
    "student@futa.edu.ng": {"password": "password123", "role": "student"},
    "tutor@futa.edu.ng": {"password": "tutor123", "role": "tutor"}
}

# New storage for our features
ANNOUNCEMENTS = ["Welcome to the new portal! Check your schedule for Monday."]
SCHEDULE = [
    {"day": "Monday", "time": "10:00 AM", "subject": "Mathematics"},
    {"day": "Wednesday", "time": "2:00 PM", "subject": "Physics"},
]
VIDEO_LESSONS = [
    {"title": "Introduction to Algebra", "subject": "Mathematics", "url": "https://www.youtube.com/embed/dQw4w9WgXcQ"},
    {"title": "Laws of Motion", "subject": "Physics", "url": "https://www.youtube.com/embed/dQw4w9WgXcQ"},
]
LIVE_CLASS_LINK = "https://zoom.us/j/123456789"

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    email = request.form.get('email')
    password = request.form.get('password')
    if email in USERS and USERS[email]['password'] == password:
        session['user'] = email
        session['role'] = USERS[email]['role']
        return redirect(url_for('tutor_dashboard' if session['role'] == 'tutor' else 'student_dashboard'))
    return "Invalid credentials! <a href='/'>Try again</a>"

@app.route('/student_dashboard')
def student_dashboard():
    if session.get('role') == 'student':
        # We pass all the data to the HTML template
        return render_template('student_dash.html', 
                               announcements=ANNOUNCEMENTS, 
                               schedule=SCHEDULE, 
                               videos=VIDEO_LESSONS, 
                               live_link=LIVE_CLASS_LINK)
    return redirect(url_for('login'))

@app.route('/tutor_dashboard')
def tutor_dashboard():
    if session.get('role') == 'tutor':
        return render_template('tutor_dash.html', 
                               announcements=ANNOUNCEMENTS, 
                               schedule=SCHEDULE)
    return redirect(url_for('login'))

# --- NEW ROUTES FOR TUTOR ACTIONS ---

@app.route('/post_announcement', methods=['POST'])
def post_announcement():
    text = request.form.get('announcement')
    if text:
        ANNOUNCEMENTS.insert(0, text) # Add to top of list
    return redirect(url_for('tutor_dashboard'))

@app.route('/add_schedule', methods=['POST'])
def add_schedule():
    day = request.form.get('day')
    time = request.form.get('time')
    subject = request.form.get('subject')
    SCHEDULE.append({"day": day, "time": time, "subject": subject})
    return redirect(url_for('tutor_dashboard'))

@app.route('/update_link', methods=['POST'])
def update_link():
    global LIVE_CLASS_LINK
    LIVE_CLASS_LINK = request.form.get('link')
    return redirect(url_for('tutor_dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)