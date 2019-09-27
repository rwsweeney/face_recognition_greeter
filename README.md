# Goal:
Train a ML model to recognize my spouse and I when we get home, and then have it greet us with a fun fact. This involved writing a function to query the wikipedia API, and then sending the results to AWS polly to synthesize the text. 

### Setup

**Images:**
Add a directory in the images folder with the name of each person you want the model to recognize. Crop a photo of the face of the person, and place one single photo in the directory as a .jpg.

**AWS Polly:**
In polly.py replace profile_name="personal-aws" with the name of your AWS access keys. On linux and mac these can be found in ~/.aws/credentials

**Configure a video stream**
I've used the free android app, IP Webcam, and in main.py you can set the rtsp end point for streaming video to the greeter.
