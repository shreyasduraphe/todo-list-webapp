import os
from flask import Flask, render_template, request, redirect, url_for
import redis

# Initialize Flask app
app = Flask(__name__)

# Connect to Redis.
# The REDIS_HOST environment variable will be used by Docker Compose.
# It defaults to 'localhost' for easy local testing without containers.
redis_host = os.environ.get('REDIS_HOST', 'localhost')
db = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handles both displaying the to-do list and adding new items.
    """
    if request.method == 'POST':
        # Get the new item from the form and add it to the list in Redis
        item = request.form.get('todo_item')
        if item:
            # lpush adds the new item to the beginning of the list
            db.lpush('todolist', item)
        return redirect(url_for('index'))

    # For a GET request, fetch all items from the list
    todo_list = db.lrange('todolist', 0, -1)
    return render_template('index.html', todo_list=todo_list)

@app.route('/delete/<item>')
def delete(item):
    """
    Deletes a specific item from the list.
    """
    # lrem removes the first occurrence of 'item' from the list
    db.lrem('todolist', 1, item)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Run the app on all available network interfaces
    app.run(host='0.0.0.0', port=5000, debug=True)