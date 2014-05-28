This project is currently under development, feel free to poke around and use what there is though.

The indeed.py program provides a class for extracting all job postings for a search term in a particular location and giving a basic summary of the results. It'll give the word:wordCount, with options to: make the words into bigrams, add the part of speech per word, find the local frequencies of the words and adjust the data according to a few filters. There is a suggested database architecture in the indeed_project directory along with a little helper robot to extract and store all the data. 

Specifics on the indeed.py program:


Make sure nltk is installed and the stopwords & wordnet corpus are downloaded, if you don't have nltk:

	$ pip install nltk
	$ python
	import nltk
	nltk.download()
	# gui will pop up prompting selection of download, choose corpus or just stopwords & wordnet




Making a Search:


	
	import indeed
	# Search class:
	
	
	# pass "e" for an exact search, "ne" for not exact
	# num_res: number of results per indeed page
	# pages: number of indeed pages to go through
	search = indeed.Search(("type of job","e_ne"), loc="Austin,TX", num_res=100, pages=1)
	
	# member variables: 
	# constructed url searched
	search.urls

	# indeed's html files
	search.html_files

	# job urls found
	search.job_urls

	# job html files for each url, generator
	search.job_htmls

	# public functions:
	# get the next html file of the job in search result
	search.next()

	# get the cleaned version of the html file
	search.raw_employer_data()

	# get the indeed url associated to the current html file
	search.current_job_url()
	.
	.
	 


Non-class functions which may be useful randomly



	html_file = indeed.get_html(url)
	
	cleaned_file = indeed.clean_html(html_file)
	
	# remove unimportant words in a string using nltk stopwords
	indeed.remove_stopwords(string,language="english")

	# get important words from a raw html file
	# uses previous two directly
	indeed.get_important_words(html_file)

	# get bigram version of pool of words in 1D list
	indeed.bigramify(words)

	# will soon add ability to see num of search results for same query across cities

Automating the search, Extract and get the data in a good format for storage/analysis:

	### Extract class, extracts some data out of html files: words and their freqs

	p = indeed.Extract(sleep = (2,10))  # same params as Search, with addition of a sleep period to deter blocks
	p.dump()  # collects all the words into a 1D list for counting, etc
	# dumping without specifying number of results to go through may (will) take a long time
	# pass an integer to work through files a bit at a time

	# if anything fails just pick up where you left off
	p.continue_dump()

	p.see_pool() # see current state of pool

	# may want to collect all words together to not skew freqs/counts -- keep caps to check for prop_nouns
	p.lower_pool()

	p.filter_stopwords(words) # supply words to filter out of pool, can import stopwords if you want to use suggested

	p.pool_summary(print_out = True)  # returns string to print/writeout if True, stores data in analy.summary
	p.pool_summary(pos = True) # includes part of speech tags in data
	p.pool_summary(log_freqs = True) # includes log freqs
	p.pool_summary(with_filter = True) # applies strong stopword filter
	p.pool_summary(lower = True)  # lower a bunch of words to reduce spread
	p.pool_summary(with_bigrams = True) # adjusts pool to bigram

	p.counts() # sorted list of counts -- separate from word 
	p.words() # ranked list of words -- separate from counts
	p.pos_tags() # pos tags given in order they appear

	# can add different Extract objects, if locations are the same, can add to pool via dump function
	# if locations are different will just pool the pools for access to other functions
	q = indeed.Extract(("Java","e"))
	q.dump()
	c = p+q
	c.dump()
	
	p.identify_NNP() # returns list of proper nouns
	p.identify_NNP(counts=True) # includes counts in tuple in list
 

	# Database interface in indeed_project/
	#
