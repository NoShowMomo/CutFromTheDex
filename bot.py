# Copyright (c) 2015–2016 Molly White
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import requests
import os
import tweepy
from secrets import *
import pokemonList
from time import gmtime, strftime
from pathlib import Path


# ====== Individual bot configuration ==========================
bot_username = 'CutFromTheDex'
logfile_name = bot_username + ".log"

auth = tweepy.OAuthHandler(C_KEY, C_SECRET)  
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)  
api = tweepy.API(auth)
# ==============================================================


def create_tweet(pokemon):
    """Create the text of the tweet you want to send."""
    # Replace this with your code!
    Prefix = "RIP "
    Suffix = ", Gone But Not Forgotten. Like and RT To Pay Your Respects #RipNationaIDex #BringBackNationaIDex"
    tweet = Prefix + pokemon + Suffix
    return tweet


def tweet(text):
    """Send out the text as a tweet."""
    # Twitter authentication
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)

    # Send the tweet and log success or failure
    try:
        api.update_status(text)
    except tweepy.error.TweepError as e:
        log(e)
    else:
        log("Tweeted: " + text)

def tweet_image(url, message):
    filename = 'temp.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

        api.update_with_media(filename, status=message)
        os.remove(filename)
    else:
        print("Unable to download image")


def log(message):
    """Log message to logfile."""
    path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(path, logfile_name), 'a+') as f:
        t = strftime("%d %b %Y %H:%M:%S", gmtime())
        f.write("\n" + t + " " + message)

def getPokemonNumber():
    number = 0
    newNumber = 0
    pokePath = Path("pokemonNumber.txt")
    with open(pokePath, "r") as pokefile:
        x = pokefile.readline()
        number = int(x)
    with open(pokePath, "w+") as pokefile:
        newNumber = number + 1
        pokefile.write(str(newNumber))
    return newNumber

def lambda_handler(event, context):
    #index = getPokemonNumber()
    pokemonName = pokemonList.DexNames.del(0)
    pokemonNumber = pokemonList.DexNumbers.del(0)
    pokemonImage = "https://www.serebii.net/pokemon/art/" + pokemonNumber + ".png"
    tweet_text = create_tweet(pokemonName)
    print(tweet_text)
    print(pokemonName)
    print(pokemonImage)
    #tweet_image(pokemonImage, tweet_text)