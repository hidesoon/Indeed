from data_collector.models import Search,Location,Links,Results
from django.utils import timezone

import os, sys
Distance_to_root = "../"
#include access to root programs
sys.path.insert(1, os.path.join(sys.path[0], Distance_to_root))

import indeed, encouragement

# generator for grouping n tuples in list, will collect all possible
def group(lst, n):
  for i in range(0, len(lst), n):
    val = lst[i:i+n]
    yield tuple(val)
          
def file_grabber(f):
    try:
        f = open(Distance_to_root+f)
        f_s = f.read().strip()
        f_s = [i.strip() for i in f_s.split('\n')]
        f.close()
        return f_s
    except:
        print "Failed to open %s file" %f



# Little robot to extract all the data from indeed and store it in a database set up in the django file
# First function to be able to search according to a variation on location, holding the search term constant
# This will allow to see what trends cluster around a particular job across the locations in a certain time window
# Future functions should allow for the complementary case, vary search terms within a location to see spread of terms across jobs 
# and see how they cluster
# Of course, can run different search terms held while varying location around each term to get a macroscopic spread that combines the two.

# will need to have it check recently gathered data or write a report for user to keep track of, don't want duplicated data in db
class Extraction_Robot(object):
    def __init__(self, terms = file_grabber("job_titles.txt"), e_ne = "e", locs=file_grabber("locations.txt"), pos=True, with_filter=True, lower=True, with_bigrams=False):
        self.terms = terms
        self.e_ne = e_ne
        self.locs = locs
        self.pos = pos
        self.with_filter=with_filter
        self.lower = lower
        self.with_bigrams = with_bigrams
        # will hold each Extract object to manipulate and store in db
        self.data = []

# hold search-terms constant, vary locations
    def vary_by_locations(self):
        if not isinstance(self.terms,basestring):
            while len(self.terms) != 1:
                term = raw_input("Too many search terms found, supply one search term to hold: ")
                self.terms = (term.strip()+" ").split(" ")[:-1]
            self.terms = self.terms[0]
        # options: lowers, with_filter
        queries = [indeed.Extract(terms=(self.terms,self.e_ne),loc=l,pages=5) for l in self.locs]
        for q in queries:
            q.dump()

        self.data = queries    
        self.save_to_db(const="search_term")
        print encouragement.get_encouragement()

    def save_to_db(self,const):
        # store in db, uses self.data Extract objects, iterate through and generate the appropriate injections for the db
        
        if const is "search_term":
            s_db = Search(date=timezone.now(),term=self.data[0].search_term)
            print s_db
            s_db.save()
            for q in self.data:
                print q
                # save data around Search term for each Extract object in self.data
                # each Extract object has multiple links, get them all and associate to the created search term
                try:
                    for url in q.job_urls:
                        l_db = Links(search=s_db, link=url)
                        l_db.save()
                    # each Extract object has a single location, get it and associate it to search term
                    if q.loc != "":
                        loc_db = Location(city=q.city,state=q.state)
                        loc_db.save()
                    # each Extract object has a summary attribute that has all the data, modify the data pool to fit the parameters specified by user
                    # and store the data in a Results table associated to its Search table
                    summary = q.pool_summary(pos=self.pos, with_filter=self.with_filter, lower=self.lower, with_bigrams=self.with_bigrams)
                    data = summary[('Word', 'Word_Count', 'POS_Tag')]
                    for tup in data:
                        w = str(tup[0])
                        c = tup[1]
                        try:
                            p = str(tup[2])
                        except:
                            p = ""
                        r_db = Results(search=s_db,location=loc_db,word=w,count=c,pos=p,is_bigram=self.with_bigrams)
                        r_db.save()
                except:
                    if q.loc != "":
                        loc_db = Location(city=q.city,state=q.state)
                        loc_db.save()
                    r_db = Results(search=s_db,location=loc_db,word="N/A",count=0,pos="",is_bigram=False)
                    r_db.save()

    def clear(self):
        self.data = []


######
#
# Allow to be run as a script from terminal, would be neat to allow itself to initiate an extraction during a time window and then send
# a report of the results further down the road. 
#

