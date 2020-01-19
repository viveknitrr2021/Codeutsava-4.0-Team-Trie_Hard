from TwitterFollowBot import TwitterBot

def retweet():
	my_bot = TwitterBot()
	my_bot.auto_rt("caa",count=10)

if __name__ == '__main__':
	retweet()