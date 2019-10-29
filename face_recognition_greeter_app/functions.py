import datetime
from wikipedia import random_fact
from polly import synthesize_input
import subprocess

# Add a 6 hour counter for seen_rachel, seen_sarah, etc. Once the 6 hour timer goes down to 0 set seen_rachel to false.

def timed_greeting(name):
    ctime = datetime.datetime.now()
    ctime = ctime.hour

    if ctime >= 0 and ctime < 6:
        return f"Welcome home, {name}. Long night? You probably don't want to hear this, but "
    elif ctime >= 6 and ctime < 12:
        return f"Good morning, {name}. Did you know, "
    elif ctime >= 12 and ctime < 17:
        return f"Good afternoon, {name}. Did you know, "
    elif ctime >= 17 and ctime < 24:
        return f"Good evening, {name}. Did you know, "

    return "Something went wrong. Your code sucks"


# This function prepares text to greet the person with a random fact from wikipedia, and then sends it off to AWS polly to be synthesized. Opener works on mac, but hasn't been tested elsewhere.
def play_and_reco(name):
    text = timed_greeting(name) + random_fact()
    sample_audio = synthesize_input(text)
    opener = "open"
    subprocess.call([opener, sample_audio])

# Create a class for the alarm with needed functions
class Alarm:

    def alarm_mode():
        # if name = unknown:
        #    unknown_count = unknown_count + 1
        # if unknown_count > 30 & rachel/sarah counter != 1:
        #    Start the alarm beeping process
        # In main function it could say 
        # if unknown_count > 30 & not rachel_seen or sarah_seen:
        #     start_alarm():
        # 

        pass

    def deactivate():
        pass

    def active():
        # Connect this to an alexa skill with a... flask listener?
        pass


    def email_owner():
        pass
