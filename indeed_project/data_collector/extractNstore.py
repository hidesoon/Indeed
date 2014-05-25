import os, sys, threading
#include access to root programs
sys.path.insert(1, os.path.join(sys.path[0], '../../'))

import indeed

# generator for grouping n tuples in list, will collect all possible
def group(lst, n):
  for i in range(0, len(lst), n):
    val = lst[i:i+n]
    yield tuple(val)
          
def locations_from_file():
    try:
        f = open("../../locations.txt")
        f_s = f.read().strip()
        f_s = [i.strip() for i in f_s.split('\n')]
        f.close()
        return f_s
    except:
        print "Failed to open locations file"

def job_titles_from_file():
    try:
        f = open("../../job_title.txt")
        f_s = f.read().strip()
        f_s = [i.strip() for i in f_s.split('\n')]
        f.close()
        return f_s
    except:
        print "Failed to open job_titles file"

class Extraction_Robot(object):
    def __init__(self, term, e_ne, locs=locations_from_file(), with_bigrams=False):
        self.term = term
        self.e_ne = e_ne
        self.locs = locs
        self.with_bigrams = with_bigrams
        # will hold each Extract object to manipulate and store in db, will be cleaned out to save on memory
        self.data = []

# hold search-term constant, vary locations
    def vary_by_locations(self,n=5):
        # n is number of threads per group
        # options: lowers, with_filter
        queries = [indeed.Extract(terms=(self.term,self.e_ne),loc=l) for l in self.locs]
        threads = [threading.Thread(target=q) for q in queries]
        grouped_threads = list(group(threads,n))
        for g in grouped_threads:
            # start threads, wait till finished, store in database, continue
            for t in g:
                t.start()
            for t in g:
                t.join()
            # take the corresponding queries to save to db and keep the tail for next iteration
            corres_queries = queries[:n]
            self.data = corres_queries
            self.save()
            queries = queries[n:]
            self.clear()


            # might want to pass to self.data here and then run save, then clean out data

    def save(self):
        # store in db, uses self.data Extract objects, iterate through and generate the appropriate injections for the db
        pass

    def clear(self):
        self.data = []






