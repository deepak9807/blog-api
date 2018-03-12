import datetime
import math
import re

from django.utils.html import strip_tags


def count_words(html_string):
	#html_string =""" <h> This is word coutn </h> """
	word_string = strip_tags(html_string)
	matching_list = re.findall(r'\w',word_string)
	count = len(matching_list) #here count the word
	return count




def get_read_time(html_string):

	word = count_words(html_string)
	read_time_min = math.ceil((word/200.0))#assuming 200 reading word persecond
	# read_time_sec = read_time_min * 60
	# read_time = str(datetime.timedelta(seconds = read_time_sec))
	read_time = str(datetime.timedelta(minutes = read_time_min))
	return read_time

