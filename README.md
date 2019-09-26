# Goal:
Train a ML model to recognize my spouse and I when we get home, and then have it greet us with a fun fact. This involved writing a function to query the wikipedia API, and then sending the results to AWS polly to synthesize the text. 

### Setup

In the images folder create a directory with the name of the person you want the model to recognize. Start by adding one cropped photo of their face to this newly created directory. In polly.py change your profile to match the one you have configured in ~/.aws/credentials if on mac/linux.
