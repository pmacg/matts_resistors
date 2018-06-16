# Matt's Resistors
Matt asked people to guess how many resistors: https://twitter.com/standupmaths/status/1007579550505734144

Then he asked for someone to collate the submissions: https://twitter.com/standupmaths/status/1007615177842360320

I'd like to play with the Twitter API, so why not over-engineer a solution?

# Running the code
I've only tested on Linux, but I'm not aware of any reason why these instructions shouldn't work on Windows.

## Python 3
- pip install -r requirements.txt
- Set the following environment variables with your twitter API credentials. (See [the Twitter docs](https://developer.twitter.com/en/docs/basics/getting-started))
  - TWITTER_CONSUMER_KEY
  - TWITTER_CONSUMER_SECRET
  - TWITTER_ACCESS_TOKEN
  - TWITTER_ACCESS_TOKEN_SECRET
- python resistors.py
- The script is interactive and will ask for user input on tweets it cannot parse automatically. Simply follow the on-screen instructions.

## Python 2
- Install Python 3 https://www.python.org/downloads/
- Follow the instructions in the 'Python 3' section

# Output
The script will generate a file (output.txt) with a sorted list of gueses.
