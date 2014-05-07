# Currently this creature has only short-term memory: not storing anything in a db to speed up query process
# maybe include pandas?

#Other
try:
    import nltk
except ImportError:
     print "Sorry, I need nltk to work at the moment. "

#Native
import urllib2, re, collections, math, random, time, socket, ssl
# import threading

#Here
import stopwords

class Search:
    """
    """
    # pass "e" for exact search or "ne" for not exact search. 
    #                          # default because num results probably low ...and it's funny?
    def __init__(self, terms=("data+scientist","e"), loc="Austin%2C+TX", num_res=100, pages=1):
        self.term_search = ""
        self.e_ne = ""
        self.loc = ""
        self.max_per_page = num_res
        # num results per page
        self.num_res = str(num_res)
        # number of pages for search result 
        self.pages = pages
        # counter for times next is called on generator
        self.count = None

        # format search term for url
        if "+" in terms[0]:
            self.term_search = terms[0].lower()
        else:
            term = terms[0].replace(" ", "+")
            self.term_search = term.lower()

        # format location in url
        if "+" in loc:
            self.loc = loc
        else:
            loc = loc.replace(" ", "+")
            loc = loc.replace(",", "%2C")
            self.loc = loc
   
        # look for whether exact or inexact criteria
        check_term = terms[1].lower()
        if check_term == "e":
            self.e_ne = "e"
        elif check_term == "ne":
            self.e_ne = "ne"
        else:
            raise SyntaxError, ("Need 'e' or 'ne' parameter for search")

        # make set of urls for search from indeed.com
        self.urls = self._construct_URL()
        
        try:
            # get html file associated with search from indeed.com
            self.html_files = [urllib2.urlopen(url).read() for url in self.urls]

            # clean the surface search  
            # self.clean_htmls =  self._clean_html_files()   
            # list of all indeed job url redirects
            self.job_urls = list(set(self._identify_job_urls()))
            self.backup_job_urls = self.job_urls

            # generator for job htmls, to access need to self.job_htmls.next(), nlp clean, process, etc
            self.job_htmls = (get_html(url) for url in self.job_urls)            
        except urllib2.HTTPError:
            print "Couldn't get indeed html files, check url accuracy."

    def _construct_URL(self):
        # defaults = {'jt':'all','radius':'25','fromage':'any','limit':'10'}
        # literal url construction, may need to build catch -> form injection: Selenium
        url_list = ['http://www.indeed.com/jobs?as_and=', '&as_phr=', '&as_any=', '&as_not=', 
        '&as_ttl=', '&as_cmp=', '&jt=all', '&st=', '&salary=', '&radius=25','&l=', '&fromage=any', '&limit=', 
        '&sort=', '&psf=advsrch']

        if self.e_ne is "e":
            url_list[1] += self.term_search
        elif self.e_ne is "ne":
            url_list[0] + self.term_search
        url_list[10] += self.loc
        url_list[12] += self.num_res

        out_url = ""
        for s in url_list:
            out_url += s
        end = int(self.num_res)*int(self.pages)
        step_size = int(self.num_res)
        slices = range(step_size,end,step_size)
        set_urls = [out_url] + [out_url+"&start="+str(i) for i in slices]
        return set_urls
    
    # specific to indeed search results?
    def _clean_html_files(self):
        pass
    """
        # take all the html tags out
        prelim_clean = [clean_html(html) for html in self.html_files]
        # remove crazy excess of \n
        cleaned_html = []
        for f in prelim_clean:
            out_html = filter(lambda s: s != "", f.split('\n'))
            out_html = [i.strip() for i in out_html]
            cleaned_html.append(out_html)

        # list of lists, each element in list is a list where each element is a sentence or empty space
        return cleaned_html"""
    # remove stopwords from given container


    def _identify_job_urls(self):
        
        raw_redirect_links = [re.findall(r'\/rc\/clk\?jk=[\w]+"',data) for data in self.html_files]
        flatten_redirect_links = [link[:-1] for page in raw_redirect_links for link in page]            
        indeedified = ["http://indeed.com"+ s for s in flatten_redirect_links]
        return indeedified

    # if you just want the raw html file from the search results
    def next(self):
        if self.count is None:
            self.count = 1
        try:
            data = self.job_htmls.next()
            print self.count
            self.count += 1
            return data
        except StopIteration:
            return None
    
    def raw_employer_data(self):
        html_file = self.next()
        if html_file is not None:
            return get_important_words(html_file)
        else:
            return None

    #TODO: find the title of each job_url link and see if good to use for {link:title} to store in db

    def current_job_url(self):
        pass

#########################    END OF "Search" CLASS     #########################
#                                                                              #
#                                                                              #
##########################             oo              #########################

def clean_html(html_file):
    return nltk.util.clean_html(html_file)

#pass a link, pretend to be someone, get the html file: independent of class just in case wants to pass random link outside of indeed
def get_html(link):
    h = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'}
    data = ""    
    try:
        #print link 
        req = urllib2.Request(link, headers=h)
        page = urllib2.urlopen(req, timeout=80)
        data = page.read()
        page.close()
    except urllib2.HTTPError:
        print "Ignoring link: %s " %link

    return data

# also removes punctuation -- may need to refine sorts of punctuation to filter out. Not handling UNICODE in international letters
def remove_stopwords(string, language="english"):
    stop_words = set(nltk.corpus.stopwords.words(language.lower()))
    words = re.findall(r'[\w\+]+', string) 
    out_string = [w for w in words if w.lower() not in stop_words]
    return out_string

def get_important_words(html):
    raw_data = clean_html(html)
    data_list = raw_data.split('\n')
    de_stopworded_data = filter(lambda l: l != [],[remove_stopwords(sentence.strip()) for sentence in data_list])
    return de_stopworded_data

def bigramify(pool):
    return [(pool[idx], pool[idx+1]) for idx in range(len(pool[:-1]))]
# would be neat to be able to see num results across several cities?
#########################       Process  class       #########################
#                                                                            #
#                                                                            #
#########################             oo             ######################### 

class Process(Search):
    """
    """
    # will need an ability to load
    def __init__(self, terms=("data+scientist", "e"), loc="Austin%2C+TX", num_res=100, pages=1, sleep=(1,2)):
        # avoid unnecessary work when there is no new search to be created: no location provided as in __add__ below
        if len(loc) > 0:
            Search.__init__(self, terms, loc, num_res, pages)
        # words that user thinks are important
        # self.user_words = set([])
        
        self.default_stopwords = set(nltk.corpus.stopwords.words('english'))

        self.sleep = sleep
        
        # words will swim in here linearly
        self.pool = []
        
        # revert to original pool
        self.backup_pool = []

        # part of speech tagged list, based on pool -- will transform to dict
        self.pos_d = []

        # part of speech tagged list for bigrams -- will transform to dict
        self.pos_bigram_d = []
        
        # summary consisting of counts, words, individual word count, etc
        self.summary = {"Total_Words":0, ("Word", "Word_Count"):[]}

        # the sleep distribution, lambda, neg log -- sort of humany?
        self.sleep_f = lambda : int(math.ceil(-math.log(random.random())*random.randint(sleep[0],sleep[1])))
        # word: wordCount
        self.wcd = {}

        self.summary_header_bool = (False, False)
   
    # allow for threading
    def __call__(self):
        self.dump()

   # add two (or More) Process objects -- may want to rethink behavior
    def __add__(self, other):
        new_e_ne = "ne" 
        new_loc = ""
        if self.loc == other.loc:
            new_loc = self.loc

        new_max_results = max([self.max_per_page, other.max_per_page])
        new_pages = max([self.pages, other.pages])
        # create new instance
        n = Process((self.term_search + "+" + other.term_search, new_e_ne), loc=new_loc, num_res=new_max_results, pages=new_pages, sleep=self.sleep)

        # Ie, locations differ, can't make a new search
        if new_loc == "":
            n.pool = self.pool + other.pool
        return n

    def __repr__(self):
        pass

    # q = quantity/num pages, v = verbose -> print out current num, total words so far....
    # memory option? -> will check if job_url has been used recently and skip     

    # dump functions: if something goes wrong, do self.continue_dump(q) and keep going
    def _pool_data(self, data, q):
        if len(data) > 5:
            self.pool += [word for sent in data for word in sent]
            self.backup_pool = self.pool[:]
            time.sleep(self.sleep_f()) 

        try:
            data = self.raw_employer_data()
            return data
        except urllib2.URLError:
            print "Bad url, skipping to next url."
            return self.continue_dump(q, rec = True)
        except socket.timeout:
            print "Connection timed out, skipping to next url."
            return self.continue_dump(q, rec = True)
        except ssl.SSLError:
            print "SSL error, skipping site."
            return self.continue_dump(q, rec = True)
 
    # may want to print self.count for each iteration while testing.
    def dump(self, q='all',rec=False):
        if q is 'all':
            # huge dump into the pool 
            data = self.raw_employer_data()
            if rec: return data
            while data is not None:
                # might want to include options for identifying information on data by data basis, might need a dict with {indeed url : cleaned html}
                data = self._pool_data(data, q)
        elif type(q) is int:
            data = self.raw_employer_data()
            if rec: return data
            while self.count < q and data is not None:
                data = self._pool_data(data, q)

    def continue_dump(self, q="all", rec=False):
        self.job_urls = self.backup_job_urls[self.count+1:]
        self.job_htmls = (get_html(url) for url in self.job_urls) 
        d = self.dump(q, rec)
        if rec: return d

    # pool manipulations, may want to adjust pool to particular purpose before storing
    def see_pool(self):
        return self.pool

    def lower_pool(self, protected=[]):
        protected = set(protected)
        # if you want to lowerase all the words before analysis. 
        # Be careful here, will lose proper noun tags unless pass list to protected
        if protected != []:
            # Ok this guy is weird maybe:            
            self.pool = [word.lower() if word not in protected else word for word in self.pool]
            # Equiv:
            """
            out = []
            for word in self.pool:
                if word not in protected:
                    out.append(word.lower())
                else:
                    out.append(word)
            self.pool = out   """
        else:
            self.pool = [word.lower() for word in self.pool]
        self.reset_summary()
    # pass True if you want to use lower case pool for analysis
    def tag_pool(self):
        self.pos_d = dict(nltk.pos_tag(list(set(self.backup_pool))))
        
    # remove more stopwords, pass as set or list, can use default collection in stopwords.py
    def filter_stopwords(self, words='default'):
        if type(words) is str:
            words = self.default_stopwords
        words = set(words)
        self.pool = [w for w in self.pool if w not in words]
        self.reset_summary()
    
    def identify_NNP(self, with_counts=False):
        #returns ranked NNPs -- good enough?
        from nltk.corpus import wordnet
        ws = self.words()
        caps = [w for w in ws if w[0].isupper()]
        f_caps = [w for w in caps if w not in stopwords.Capital_words]
        # Need to protect a few words...("Python")... if this gets too messy need to math it ... if word falls after 
        # curvature point in distribution then toss, else keep
        # Oh, could do a user feedback system...
        protected = ["Python", "Java", "Cloud", "Dell", "C", "R", "Go", "Oracle", "MS", "Apple", "Rails", "Ruby","Ebay",
        "SAS", "SPSS", "Hive", "Pig"]
        # Relies on funny portmanteaus and neologs that companies/technologies tend to use
        # wordnet.synsets(string) returns [] if word is not found in their english dictionary
        f2_caps = [w for w in f_caps if w in protected or wordnet.synsets(w) == [] ]

        if with_counts:
            f2_caps = [(w, self.wcd[w]) for w in f2_caps]
        return f2_caps

    
    def store_raw_corpus(self, file_name):
        pass

    def _print_out(self, h):
        out_str = "Total_words: %s \n" % self.summary["Total_Words"]
        out_str += "\t".join(h) + '\n'
        for tup in self.summary[h]:
            out_str += "%s\t"*len(h) %tup+'\n'
        return out_str 

    def _trans_header(self, tup_h):
        if tup_h == (False, False):
            return ("Word", "Word_Count")
        elif tup_h == (True, False):
            return ("Word", "Word_Count", "Log_Freqs")
        elif tup_h == (False, True):
            return ("Word", "Word_Count", "POS_Tag")
        elif tup_h == (True, True):
            return ("Word", "Word_Count", "Log_Freqs", "POS_Tag") 

    def _is_bigrammed(self):
        if type(self.pool[0]) is tuple:
            return True
        elif type(self.pool[0]) is str:
            return False
                            # returning a string if you must store results in txt file -> interface with db would be better
    # rename to just 'summary' ?               #the log freq of ea word, the part of speech of ea. word
    def pool_summary(self, print_out=False, log_freqs=False, pos=False, with_filter=False, lower=False, with_bigrams=False):
        # self.summary = {"Total_Words" : N , (nth, "Word_Count") : [(word1,count1),(word2,count2),(word3,count3)...(wordn,countn)] }
        # very primitive summary for all the words
        # the most basic (all params False) stores word : wordCount in self.summary.
        
        # current pool is bigrammed but user doesn't want it to be
        if not with_bigrams and self._is_bigrammed():
            self.restore_pool()
            self.pool_summary(print_out,log_freqs,pos,with_filter,lower, with_bigrams)
        # apply medium filter
        if with_filter:
            self.filter_stopwords(stopwords.Capital_words)
            self.filter_stopwords(stopwords.Lower_words)
            self.pool_summary(print_out, log_freqs, pos, False, lower, with_bigrams)
        # lowercase a bunch of words, keeps a protected set
        if lower and not with_bigrams:
            nnps = self.identify_NNP()
            self.lower_pool(protected=nnps)
            self.pool_summary(print_out, log_freqs, pos, with_filter, False, with_bigrams)  
        elif lower and (with_bigrams or self._is_bigrammed()):
            self.restore_pool()
            self.pool_summary(print_out, log_freqs, pos, with_filter, True, False)
            self.pool_summary(print_out, log_freqs, pos, with_filter, False, True)

        # user wants bigrammed version but pool is not bigrammed
        if with_bigrams and not self._is_bigrammed(): 
            self.pool = bigramify(self.pool)
            self.reset_summary()

        if pos and self._is_bigrammed and self.pos_bigram_d == []:
            self.tag_pool()
            self.pos_bigram_d = dict([((tup),(self.pos_d[tup[0]],self.pos_d[tup[1]])) for tup in self.pool])

        # in the bigram case words means bigrams
        total_words = len(self.pool)
        new_summary_header_bool = (log_freqs, pos)
        h = self._trans_header(self.summary_header_bool)
        new_h = self._trans_header(new_summary_header_bool)
        pre_data = self.summary[h]
        data = []

        if pre_data == []:
            """
            # possible style
            word_count_dict = collections.defaultdict(int)
            for word in self.pool:
                word_count_dict[word] += 1
            """
            word_count_dict = collections.Counter(self.pool)
            self.wcd = word_count_dict
            for key in word_count_dict:
                self.summary[h].append((key,word_count_dict[key]))
            self.summary[h] = sorted(self.summary[h], key=lambda t : t[1], reverse=True)
            self.summary["Total_Words"] = total_words
            pre_data = self.summary[h]

        if new_summary_header_bool == self.summary_header_bool:
            new_h = h
        elif new_summary_header_bool == (False, False):
            self.summary_header_bool = new_summary_header_bool
            # only need first two pieces of tuple and update summary
            self.summary = {"Total_Words":total_words, new_h:[(w[0], w[1]) for w in pre_data]}
        elif new_summary_header_bool == (True, False):
            self.summary_header_bool = new_summary_header_bool
            data = sorted([(w[0], w[1], math.log(w[1]/float(total_words))) for w in pre_data], key=lambda t : t[1], reverse=True)
            self.summary = {"Total_Words":total_words, new_h:data}
        elif new_summary_header_bool == (False, True):
            self.summary_header_bool = new_summary_header_bool
            self.tag_pool()
            if not self._is_bigrammed():
                data = sorted([(w[0], w[1], self.pos_d[w[0]]) for w in pre_data], key=lambda t : t[1], reverse=True)
            else:
                data = sorted([(w[0], w[1], self.pos_bigram_d[w[0]]) for w in pre_data], key=lambda t : t[1], reverse=True)
            self.summary = {"Total_Words":total_words, new_h:data}       
        elif new_summary_header_bool == (True, True):
            data = []
            self.summary_header_bool = new_summary_header_bool
            self.tag_pool()
            if not self._is_bigrammed():
                data = sorted([(w[0], w[1], math.log(w[1]/float(total_words)), self.pos_d[w[0]]) for w in pre_data], key=lambda t : t[1], reverse=True)
            else:
                data = sorted([(w[0], w[1], self.pos_bigram_d[w[0]]) for w in pre_data], key=lambda t : t[1], reverse=True)
            self.summary = {"Total_Words":total_words, new_h:data}        

        if print_out:
            return self._print_out(new_h)
    
    def summary_data(self):
        return self.summary

    def reset_summary(self):
        self.summary = {"Total_Words":0, ("Word", "Word_Count"):[]}
        self.summary_header_bool = (False, False)         
    # every pool needs a safety floatation device
    def restore_pool(self):
        self.pool = self.backup_pool
        self.reset_summary()
    
    def save(self):
        pass

    def counts(self):
        if self.wcd == {}:
            self.pool_summary()
            self.counts()
        counts_list = sorted([self.wcd[w] for w in self.wcd], reverse=True)
        return counts_list

    def words(self):
        # returns words in order of count results
        if self.summary["Total_Words"] == 0:
            self.pool_summary(False)
            self.words()
        current_h = self._trans_header(self.summary_header_bool)
        data = self.summary[current_h]
        words = [t[0] for t in data]
        return words

    def pos_tags(self):
        if self._is_bigrammed():
            if self.pos_bigram_d == [] and len(self.pool) > 0:
                self.tag_pool()
                self.pos_bigram_d = dict([((tup),(self.pos_d[tup[0]],self.pos_d[tup[1]])) for tup in self.pool])
                tags = [self.pos_bigram_d[t] for t in self.pool]
                return tags            
            else:
                tags = [self.pos_bigram_d[t] for t in self.pool]
                return tags
        else:
            if self.pos_d == [] and len(self.pool) > 0:
                self.tag_pool()
                tags = [self.pos_d[w] for w in self.pool]
                return tags               
            else:
                tags = [self.pos_d[w] for w in self.pool]
                return tags

    """
    option: strict -> use large stopwords list to remove even more words.
    option: store -> as csv or in db
    option: correlation m. 
    option: 
    """
#########################    END OF "Process" CLASS     ########################
#                                                                              #
#                                                                              #
##########################             oo              #########################



# Analysis class --> Maybe should be external to this: allows analysis of data from other sources

# Database interface
# Once database built, would be good to have python look to see if indeed job url has been searched before (recently) and use that data rather than getting it again
