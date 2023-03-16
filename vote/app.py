from flask import Flask, render_template, request, redirect, url_for, session
import redis

app = Flask(__name__)
app.secret_key = 'my_secret_key'  # Change this to a random string

# Redis connection settings
redis_host = '172.30.180.232'  # Replace with your Redis hostname or IP address
redis_port = 6379
redis_password = 'Dev0ops@123'  # Replace with your Redis password

# Connect to Redis
r = redis.Redis(host=redis_host, port=redis_port, password=redis_password, db=0)


@app.route('/')
def index():
    # Check if the user is logged in
    if 'username' in session:
        # Get the current vote counts
        yes_count = r.get('yes') or 0
        no_count = r.get('no') or 0
        return render_template('index.html', username=session['username'], yes_count=yes_count, no_count=no_count)
    else:
        return redirect(url_for('login'))


@app.route('/vote', methods=['POST'])
def vote():
    # Check if the user is logged in
    if 'username' in session:
        # Get the user's vote
        vote = request.form.get('vote')

        # Increment the vote count in Redis
        if vote == 'yes':
            r.incr('yes')
        elif vote == 'no':
            r.incr('no')

        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the username and password are correct
        if username == 'my_username' and password == 'my_password':
            # Store the username in the session
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    # Remove the username from the session
    session.pop('username', None)
    return redirect(url_for('login'))
