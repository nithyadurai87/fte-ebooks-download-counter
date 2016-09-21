#!/usr/bin/env python
# -- coding: utf-8 --



import urllib2
import BeautifulSoup
import csv
import time
import os
from time import gmtime, strftime


if os.path.isfile('fte_books_download-count.html'):
	os.remove('fte_books_download-count.html')

if os.path.isfile('books.txt'):
	os.remove("books.txt")

if os.path.isfile('./data/all_files.csv'):
	os.remove("./data/all_files.csv")
                           

def books():

    file = urllib2.urlopen('https://raw.githubusercontent.com/kishorek/Free-Tamil-Ebooks/master/booksdb.xml')
    cont = file.readlines()

    for i in cont:
        if '<link>' in i:
            fle = open("books.txt",'a')
            fle.write (i.split('<link>')[1].split('</link>')[0]+'\n')
            fle.close()

    file.close()

    return fle



def count():

    fle = open("books.txt",'r')
    all_files = open('./data/all_files.csv','wb')
    all_files.write("நூலின் பெயர்~epub~mobi~A4 PDF~6 inch PDF~மொத்தம்\n")
    counter_list = []

    for i in fle:
   
        time.sleep(2)    
    
        counter_list = []

	url = i.strip()

        req = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"}) 

        con = urllib2.urlopen(req)
        soup = BeautifulSoup.BeautifulSoup(con)
	title = soup.title.string.replace(",","_")

#	print title

        total = 0
	title_text = "<a target='_blank' href='" + url + "'>" + title.encode('utf-8') + "</a>~"

#	print title_text
#	all_files.write(title.encode('utf-8') + '~')
	all_files.write(title_text)
	counter_list.append(title.encode('utf-8'))

        for i in soup.findAll('small'):

		if "times" in str(i):
			count = str(i).split('times')[0].split('Downloaded')[1].strip()
			counter_list.append(count)
			total = total + int(count)

#			print "total = " + str(total)
			all_files.write(count)
			all_files.write('~')


#    	print counter_list

	all_files.write(str(total))
	all_files.write("\n")



books()
count()





with open('data/all_files.csv') as sample, open('data/all_files_reverse_sorted.csv', "w") as out:
    csv1=csv.reader(sample,delimiter='~')
    header = next(csv1, None)
    csv_writer = csv.writer(out,delimiter='~')
    if header:
        csv_writer.writerow(header)
    csv_writer.writerows(sorted(csv1, key=lambda x:int(x[5]),reverse=True))




timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())




with open("data/all_files_reverse_sorted.csv") as fin:
    headerline = fin.next()
    total = 0
    for row in csv.reader(fin,delimiter='~'):
        total += int(row[5])



total_time = open('data/time_total.html','w')

total_time.write('<link href="../css/bootstrap.min.css" rel="stylesheet">\n')
total_time.write("<p align='right'> இந்தப் பட்டியல் தினமும் ஒரு முறை இற்றைப்படுத்தப்படுகிறது. கடைசி இற்றை நேரம்   " + timestamp + "<br/>")
total_time.write(" மொத்தப் பதிவிறக்கங்கள் =   " + str(total) + "</p>")
total_time.close()
                  

                                                                                                                              
