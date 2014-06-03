from data_collector.extractNstore_T import Extraction_Robot
from data_collector.extractNstore_T import file_grabber

    # make a list that has robots in it and run vary by location
def vbl(bigrammed=False):
    job_titles = file_grabber("job_titles.txt")
    robots = [Extraction_Robot(terms=title,with_bigrams=bigrammed) for title in job_titles]
    for robot in robots:
        robot.vary_by_locations()