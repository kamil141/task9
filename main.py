#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import libraries
import redis
import os
from flask import Flask, redirect, url_for, render_template
from datetime import datetime

# Create and initialize connection to Redis
app = Flask(__name__)
redis = redis.Redis(host=os.environ.get('REDIS_HOST'),
                    password=os.environ.get('REDIS_PASS'),
                    port=os.environ.get('REDIS_PORT'),
                    db=0)

# Get the current date and time
now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

# Set a new server start date and time, reset sessionvisitors counter
redis.set('sessionvisitors', 0)
redis.set('startdate', now)

# Redirect all requests from / to /visitor
@app.route('/')
def hello_world():
    return redirect(url_for('visitor'))

@app.route('/visitor')
def visitor():
    # Increase both counters (all sessions and sessions from the server start)
    redis.incr('sessionvisitors')
    redis.incr('allvisitors')

    # Get data from Redis
    all_visitors = redis.get('allvisitors').decode("utf-8")
    session_visitors = redis.get('sessionvisitors').decode("utf-8")
    start_date = redis.get('startdate').decode("utf-8")

    # Render HTML page and return it to the client
    return render_template('visitor.html', all_visitors=all_visitors, session_visitors=session_visitors, start_date=start_date)


@app.route('/visitor/reset')
def reset_visitor():
    # Reset both counters to 0
    redis.set('sessionvisitors', 0)
    redis.set('allvisitors', 0)

    # Get data from Redis
    all_visitors = redis.get('allvisitors').decode("utf-8")
    session_visitors = redis.get('sessionvisitors').decode("utf-8")
    start_date = redis.get('startdate').decode("utf-8")

    # Render HTML page and return it to the client
    return render_template('reset.html', all_visitors=all_visitors, session_visitors=session_visitors, start_date=start_date)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
