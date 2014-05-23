import os, sys, threading

sys.path.insert(1, os.path.join(sys.path[0], '../../'))

import indeed


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

