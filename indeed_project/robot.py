from data_collector.extractNstore_T import Extraction_Robot
from data_collector.extractNstore_T import file_grabber

import robot_email
    # make a list that has robots in it and run vary by location
def vbl(bigrammed=False,with_email=False):
    if with_email:
	    params = robot_email.get_email_params()
    job_titles = file_grabber("job_titles.txt")
    robots = [Extraction_Robot(terms=title,with_bigrams=bigrammed) for title in job_titles]
    for robot in robots:
        robot.vary_by_locations()
    
    if with_email:
    	robot_email.send(*params) 