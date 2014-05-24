import os, sys, threading
#include access to root programs
sys.path.insert(1, os.path.join(sys.path[0], '../../'))

import indeed

# generator for grouping n tuples in list, will collect all possible
def group(lst, n):
  for i in range(0, len(lst), n):
    val = lst[i:i+n]
    yield tuple(val)
          
def get_locations_from_file():
    try:
        f = open("../../locations.txt")
        f_s = f.read().strip()
        f_s = [i.strip() for i in f_s.split('\n')]
        f.close()
        return f_s
    except:
        print "Failed to open locations file"

def get_job_titles_from_file():
    try:
        f = open("../../job_title.txt")
        f_s = f.read().strip()
        f_s = [i.strip() for i in f_s.split('\n')]
        f.close()
        return f_s
    except:
        print "Failed to open job_titles file"

# hold search-term constant, vary locations
class Extraction_Robot(object):
    def __init__(self, term, e_ne, locs=get_locations_from_file()):
        self.term = term
        self.e_ne = e_ne
        self.locs = locs
        self.data = []

    def vary_by_locations(self):
        # options: lowers, with_filter
        queries = [indeed.Extract(terms=(self.term,self.e_ne),loc=l) for l in self.locs]
        threads = [threading.Thread(target=q) for q in queries]
        grouped_threads = list(group(threads,10))
        for g in grouped_threads:
            # start threads, wait till finished, store in database, continue
            for t in g:
                t.start()
            for t in g:
                t.join()

            #all threads started, program running.    
        self.data = queries

    def save(self):
        # store in db
        pass







