import tweepy

    # print(type(stopwords))
    # print(custom_mask[0])

 # register_matplotlib_converters()
    # sns.set(style='whitegrid', palette='muted', font_scale=1.2)
    # HAPPY_COLORS_PALETTE = ["#01BEFE", "#FFDD00", "#FF7D00", "#FF006D", "#ADFF02", "#8F00FF"]
    # sns.set_palette(sns.color_palette(HAPPY_COLORS_PALETTE))
    # rcParams['figure.figsize'] = 8, 8  
    # show_word_cloud(wordcloud,title)
    # print("wordcloud generated")
# exampletext ='The robot clicked disapprovingly, gurgled briefly inside its cubical interior and extruded a pony glass of brownish liquid. "Sir, you will undoubtedly end up in a drunkards grave, dead of hepatic cirrhosis, it informed me virtuously as it returned my ID card. I glared as I pushed the glass across the table.The wave crashed and hit the sandcastle head-on. The sandcastle began to melt under the waves force and as the wave receded, half the sandcastle was gone. The next wave hit, not quite as strong, but still managed to cover the remains of the sandcastle and take more of it away. The third wave, a big one, crashed over the sandcastle completely covering and engulfing it. When it receded, there was no trace the sandcastle ever existed and hours of hard work disappeared forever.He had done everything right. There had been no mistakes throughout the entire process. It had been perfection and he knew it without a doubt, but the results still stared back at him with the fact that he had lost.Where do they get a random paragraph? he wondered as he clicked the generate button. Do they just write a random paragraph or do they get it somewhere? At that moment he read the random paragraph and realized it was about random paragraphs and his world would never be the same.There was something beautiful in his hate. It wasnt the hate itself as it was a disgusting display of racism and intolerance. It was what propelled the hate and the fact that although he had this hate, he didnt understand where it came from. It was at that moment that she realized that there was hope in changing him.'
# wordcloudgenerate(exampletext,'xyz','sample',1)

def twitterdata(hotelname):
    consumerkey = "253pprPRXjYdqWHPLsVOrR3gx"
    consumersecret = "Hl9b7xRziXSYm87kmlVenEKAwCQMiN99Ig3h7ZGjhe28fG3Art"
    accesstoken = "1195350987109617664-bmmGfhp0Da3yhtJWYHFeeaBf0kRP62"
    accesstokensecret = "DyVPmrrlQw6VICBCCG6NH8t4270E3Uzd22IubvWbIKgBx"
    
    auth = tweepy.OAuthHandler(consumer_key=consumerkey,consumer_secret = consumersecret)
    auth.set_access_token(accesstoken,accesstokensecret)
    auth.secure = True
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    keyword_old = hotelname
    vacation_keywords =['vacation','holidays']

    # keyword_old = keyword_old +' '+convert_list_to_string(vacation_keywords, ' ')
    # print(keyword_old)

    retweet_filter = '-filter:retweets'
    keywords = keyword_old+retweet_filter
    no_of_tweets = 100
    filename = 'tweets.txt'
    sinceId = None
    
    max_id = -1
    maxTweets = 1000

    tweetCount = 0
    print("Downloading max {0} tweets".format(maxTweets))
    with open(filename, 'w') as f:
        while tweetCount < maxTweets:
            tweets = []
            try:
                if (max_id <= 0):
                    if (not sinceId):
                        new_tweets = api.search(q=keywords, lang ="en", count=no_of_tweets, tweet_mode='extended')

                    else:
                        new_tweets = api.search(q=keywords, lang ="en", count=no_of_tweets,
                                            since_id=sinceId, tweet_mode='extended')
                else:
                    if (not sinceId):
                        new_tweets = api.search(q=keywords, lang ="en", count=no_of_tweets,
                                            max_id=str(max_id - 1), tweet_mode='extended')
                    else:
                        new_tweets = api.search(q=keywords, lang ="en", count=no_of_tweets,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId, tweet_mode='extended')

                if not new_tweets:
                    print("No more tweets found")
                    break
                for tweet in new_tweets:
                    tweet_verified = tweet.user.verified
                    if(tweet_verified == False and (hotelname not in tweet.user.name) ):
                        f.write(str(tweet.full_text.replace('\n','').encode("utf-8"))+"\n")


                tweetCount += len(new_tweets)
                print("Downloaded {0} tweets".format(tweetCount))
                max_id = new_tweets[-1].id
                    
            except tweepy.TweepError as e:
                # Just exit if any error
                print("some error : " + str(e))
                break
                    
    print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, filename))
    return (filename, tweetCount)

# data =twitterdata('MGM Grand')