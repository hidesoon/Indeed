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
def term_locations(term,locs=get_locations_from_file()):
    # options: lowers, with_filter
    queries = [indeed.Extract(terms=(term,"ne"),loc=l,pages=10) for l in locs]
    threads = [threading.Thread(target=q) for q in queries]
    grouped_threads = list(group(threads,10))
    for group in grouped_threads:
        # start threads, wait till finished, store in database, continue
        pass








