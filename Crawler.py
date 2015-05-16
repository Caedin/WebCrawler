import urllib
import re
import sys
import os

from Queue import Queue
from threading import Thread
import threading

output = set()
ReadQueue = Queue()
WriteQueue = Queue()

def getURL(page):
    start_link = page.find("a href")
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1: end_quote]
    return url, end_quote

def get_tokens(page):
	tokens = []
	while True:
		url, n = getURL(page)
		page = page[n:]
		if url:
			tokens.append(url)
		else:
			break
	
	bad_tokens = []
	for k in tokens:
		if 'http://' not in k and 'https://' not in k or 'script:' in k or 'Script:' in k or k in output:
			bad_tokens.append(k)
			
	
	return list(set(tokens) - set(bad_tokens))



def read_pages():
	url = ReadQueue.get()

	try:
		page = urllib.urlopen(url)
	except Exception:
		return
		
	page = page.read()
	for k in get_tokens(page):
		ReadQueue.put(k)
		WriteQueue.put(k)
	
	return
		

	
	
if __name__ == '__main__':
	ReadQueue.put('http://www.google.com')
	
	threads = []
	
	number_of_urls = 50000
	number_of_threads = 50
	url_count = 0
	
	while url_count<number_of_urls:
		while(len(threading.enumerate())<number_of_threads):
			if ReadQueue.empty()==False or url_count>number_of_urls:
				func = read_pages
				thread = Thread(target= func)
				thread.daemon =True
				thread.start()
				threads.append(thread)
				
				while WriteQueue.qsize()>0:
					output.add(WriteQueue.get())
					url_count+=1
				
				with open('output_urls.txt', 'ab') as output_file:
					for item in output:
						output_file.write(item.strip()+'\n')
				output.clear()
						
				print url_count
			else:
				break
			

    
	for thread in threads:
		thread.join()
	
	
	
	with open('output_urls.txt', 'ab') as output_file:
		for item in output:
			output_file.write(item.strip()+'\n')