import random

QUOTES = ["You're almost there!", "All done!", "Only a little more data.", "Keep it up!", "You're the best!", "Thankfully, persistence is a great substitute for talent.",
"Everything will be okay in the end. If it's not okay, then it's not the end.", "There, there, I know it's rough.", "Whew!", "You're the best!",
"Remember, man does not live on bread alone: sometimes he needs a little buttering up.", "Truth is, we are all tragedies waiting to happen.", "A M00se once bit my sister... " ]


def get_encouragement():
	return QUOTES[random.randint(0,len(QUOTES)-1)]

