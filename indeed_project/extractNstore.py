from data_collector.models import Search,Location,Links,Results
from django.utils import timezone
import os, sys, threading
#include access to root programs
sys.path.insert(1, os.path.join(sys.path[0], '../'))

import indeed

# generator for grouping n tuples in list, will collect all possible
def group(lst, n):
  for i in range(0, len(lst), n):
    val = lst[i:i+n]
    yield tuple(val)
          
def locations_from_file():
    try:
        f = open("../locations.txt")
        f_s = f.read().strip()
        f_s = [i.strip() for i in f_s.split('\n')]
        f.close()
        return f_s
    except:
        print "Failed to open locations file"

def job_titles_from_file():
    try:
        f = open("../job_title.txt")
        f_s = f.read().strip()
        f_s = [i.strip() for i in f_s.split('\n')]
        f.close()
        return f_s
    except:
        print "Failed to open job_titles file"

# Little robot to extract all the data from indeed and store it in a database set up in the django file
# First function to be able to search according to a variation on location, holding the search term constant
# This will allow to see what trends cluster around a particular job across the locations in a certain time window
# Future functions should allow for the complementary case, vary search terms within a location to see spread of terms across jobs 
# and see how they cluster
# Of course, can run different search terms held while varying location around each term to get a macroscopic spread that combines the two.

# will need to have it check recently gathered data or write a report for user to keep track of, don't want duplicated data in db
class Extraction_Robot(object):
    def __init__(self, terms = job_titles_from_file(), e_ne = "e", locs=locations_from_file(), pos=True, with_filter=True, lower=True, with_bigrams=False):
        self.terms = terms
        self.e_ne = e_ne
        self.locs = locs
        self.pos = pos
        self.with_filter=with_filter
        self.lower = lower
        self.with_bigrams = with_bigrams
        # will hold each Extract object to manipulate and store in db, will be cleaned out to save on memory
        self.data = []

# hold search-terms constant, vary locations: TODO:: group the locations and feed partially, save to db as locations group is finished
# make sure to keep the search term as a global while running whole process, this allows for the data to be stored as one search event even if
# the extraction takes a while
    def vary_by_locations(self,n=3):
        if type(self.terms) is not str:
            while len(self.terms) != 1:
                term = raw_input("Too many search terms found, supply one search term to hold: ")
                self.terms = (term + " ").split(" ")[:-1]
            self.terms = self.terms[0]
        # n is number of threads per group
        # options: lowers, with_filter
        queries = [indeed.Extract(terms=(self.terms,self.e_ne),loc=l,pages=5) for l in self.locs]
        threads = [threading.Thread(target=q) for q in queries]
        grouped_threads = list(group(threads,n))
        for g in grouped_threads:
            # start threads, wait till finished, store in database, continue
            for t in g:
                t.start()
            for t in g:
                t.join()
        self.data = queries    
        self.save_to_db(const="search_term")
        print "I made it through!"

    def save_to_db(self,const):
        # store in db, uses self.data Extract objects, iterate through and generate the appropriate injections for the db
        
        if const is "search_term":
            s_db = Search(date=timezone.now(),term=self.data[0].search_term)
            s_db.save()
            for q in self.data:
                # save data around Search term for each Extract object in self.data
                # each Extract object has multiple links, get them all and associate to the created search term
                for url in q.job_urls:
                    l_db = Links(search=s_db, link=url)
                    l_db.save()
                # each Extract object has a single location, get it and associate it to search term
                if q.loc != "":
                    loc_db = Location(search=s_db,city=q.city,state=q.state)
                    loc_db.save()
                # each Extract object has a summary attribute that has all the data, modify the data pool to fit the parameters specified by user
                # and store the data in a Results table associated to its Search table
                q.pool_summary(pos=self.pos, with_filter=self.with_filter, lower=self.lower, with_bigrams=self.with_bigrams)
                data = q.summary[('Word', 'Word_Count', 'POS_Tag')]
                for tup in data:
                    w = str(tup[0])
                    c = tup[1]
                    try:
                        p = tup[2]
                    except:
                        p = ""
                    r_db = Results(search=s_db,word=w,count=c,pos=p,is_bigram=self.with_bigrams)
                    r_db.save()

    def clear(self):
        self.data = []


######
#
# Allow to be run as a script from terminal, would be neat to allow itself to initiate an extraction during a time window and then send
# a report of the results further down the road. 
#

