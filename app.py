from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, send_from_directory
import os
from xml.etree import ElementTree
import sig_tools




# function to run every 10 minutes
def sensor():

    # character id, account id, guild id, guild name
    ids = ['521159', '291978', '2366', 'Solo Player']

    sig_tools.jonwon(ids)

    

# Initialize background scheduler
sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor,'interval',minutes=10)
sched.start()



app = Flask(__name__)



@app.route('/')
def show_index():

    sensor()
    return send_from_directory('static/images', 'jonwon.jpeg')



if __name__ == "__main__":
    app.run(debug=False)
