#!/usr/bin/env python3
#
# This is a script written in response to the following tweet:
#   https://twitter.com/standupmaths/status/1007615177842360320
#
# The script will scan through the responses to both the tweet above and the
# original tweet (https://twitter.com/standupmaths/status/1007579550505734144)
# since several people have made guesses on the second tweet.
#
# For each response, the script will try to pull out the numerical guess.
# If it fails to pull out the guess automatically, it will ask for user input
# in order to confirm either:
#  - there was no guess in the tweet, it can be ignored
#  - there was a guess, and the user can manually enter it
#
# Once all of the guesses have been collated, they will be sorted numerically
# and printed out into a space seperated text file of the following format:
#   # Script run at: <time>
#   <twitter username> <guess>
#   <twitter username> <guess>
#   ...
#
# Written by github user pmacg. MIT license.
import tweepy
import os
from datetime import datetime
import operator

# IDs of Matt's tweets
MATTS_TWEETS_IDS = [1007579550505734144, 1007615177842360320]

# Return True if a word looks like it might be a number
# That is, it contains only digits, commas and periods
def is_numbery(word):
  found_digit = False
  for c in word:
    if c not in '0123456789.,':
      return False
    if c in '0123456789':
      found_digit = True
  return found_digit

# Try to extract a numerical answer from the given tweet.
# Return None if no answer could be automatically parsed.
def parse_tweet_for_answer(tweet):
  # Split the tweet into 'words'
  tweet_text_tokens = tweet.text.replace('!','').replace('?','').split()

  # Look for words with only digits, commas and periods
  numbery_words = [word for word in tweet_text_tokens if is_numbery(word)]

  if len(numbery_words) == 1:
    number = numbery_words[0]
    
    # If the number contains both a comma and a period, assume the second one
    # represents a decimal point, and strip it and any following characters off.
    if ',' in number and '.' in number:
      comma_index = number.find(',')
      period_index = number.find('.')
      if period_index > comma_index:
        number = number[:period_index].replace(',', '')
      else:
        number = number[:comma_index].replace('.', '')

    # If the number contains only a period, assume it is a decimal point and
    # strip any following characters off
    elif '.' in number:
      i = number.find('.')
      number = number[:i]

    # If the number contains only digits and commas, assume it is a thousands
    # seperator and remove it
    elif ',' in number:
      number = number.replace(',', '')

    # Try to parse the number
    try:
      int_guess = int(number)
      print("Successfully parsed guess.")
      return int_guess
    except:
      # Couldn't parse the resulting number, return None
      return None

  else:
    # If there are 0 or multiple numbery words, we can't parse this tweet.
    return None

# Interact with the use to get an answer for this tweet
# Or return None if there is no answer in the tweet
def manual_intervention(tweet):
  print("\n\nTweet\n-----\n%s\n" % (tweet.text))
  answer = None
  while answer is None:
    response = input("If the above tweet contains a guess, enter it here (otherwise just hit enter): ")
    
    if not response:
      # The input was left blank, and so the tweet doesn't contain a guess
      print("No answer in tweet. Skipping.")
      return None
    
    # Convert the answer to an integer
    try:
      answer = int(response)
    except:
      print("Input not parseable as an integer!")
  return answer

# Write the collated guesses out into a file
def write_output_file(guesses):
  print("Writing results to output.txt...")
  current_time = str(datetime.now())
  with open("output.txt", 'w') as fout:
    fout.write("# Script run at: %s\n" % (current_time))
    for user, guess in sorted(guesses.items(), key=operator.itemgetter(1)):
      fout.write("%s %s\n" % (user, guess))

if __name__ == "__main__":
  # Load in the twitter API credentials from the environment
  try:
    consumer_key = os.environ['TWITTER_CONSUMER_KEY']
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
  except KeyError:
    print("Please make sure you have the following environment variables set:\n"
          " - TWITTER_CONSUMER_KEY\n"
          " - TWITTER_CONSUMER_SECRET\n"
          " - TWITTER_ACCESS_TOKEN\n"
          " - TWITTER_ACCESS_TOKEN_SECRET\n")
    exit()

  # Authenticate with Twitter
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  api = tweepy.API(auth)

  # This dictionary will hold all of the guesses. Keys are strings (usernames),
  # values are integers
  guesses = {}

  # Find all replies to the two tweets. This is surprisingly difficult to do since
  # Twitter doesn't provide an API request to get replies to a given tweet.
  #
  # First, find the last 10000 tweets @standupmaths. I'm assuming this will cover
  # all tweets as part of this competition.
  all_tweets_at_standupmaths = tweepy.Cursor(api.search, q="to:@standupmaths").items(10000)

  # Then, find only tweets which are in reply to the competition tweets 
  for tweet in all_tweets_at_standupmaths:
    if tweet.in_reply_to_status_id in MATTS_TWEETS_IDS:
      # Found a reply!
      # Try to extract an answer from the tweet automatically
      possible_answer = parse_tweet_for_answer(tweet)
      
      if possible_answer is None:
        # We didnt manage to extract an answer automatically, engage with the user
        # of the script to manually get the answer
        possible_answer = manual_intervention(tweet)

      if possible_answer is not None:
        # We have an answer from this tweet. Add id to the dictionary
        guesses['@' + tweet.author.screen_name] = possible_answer

  # We've been through all of the tweets, time to write out the summary file
  write_output_file(guesses)
