from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir

session = Session(profile_name="personal-aws")
polly = session.client("polly")


def synthesize_input(text_input):
    try:
        response = polly.synthesize_speech(
            Text=text_input, OutputFormat="mp3", VoiceId="Amy"
        )
    except (BotoCoreError, ClientError) as error:
        print(error)
        sys.exit(-1)

    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            output = os.path.join(gettempdir(), "speech.mp3")

            try:
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                print(error)
                sys.exit(-1)

    else:
        print("Could not stream audio")
        sys.exit(-1)

    return output
