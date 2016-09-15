#!/usr/bin/env python
# -- coding: utf-8 --



import urllib2
import BeautifulSoup
import csv
import time
import os



if os.path.isfile('fte_books_download-count.html'):
	os.remove('fte_books_download-count.html')

if os.path.isfile('books.txt'):
	os.remove("books.txt")

if os.path.isfile('all_files.csv'):
	os.remove("all_files.csv")
                           

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
    all_files = open('all_files.csv','wb')
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


csvFile = open('all_files.csv')#enter the csv filename
csvReader = csv.reader(csvFile,delimiter = '~')
csvData = list(csvReader)


timestamp = time.strftime("%d/%m/%Y %H:%M:%S")

with open('fte_books_download-count.html', 'w') as html: #enter the output filename
    html.write(''' <head>
	<meta charset="UTF-8">
	</head> ''')
    html.write("<h1> <a href='http://FreeTamilEbooks.com' target='_blank'>FreeTamilEbooks.com</a></h1>")
    html.write(timestamp)
    html.write("<p>&nbsp;</p>")

    html.write('''<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.8.1/bootstrap-table.min.css">

<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
''')    
    html.write('<table data-toggle = "table" data-pagination = "true">\r')
    r = 0
    for row in csvData:
        if r == 0:
            html.write('\t<thead>\r\t\t<tr>\r')
            for col in row:
                html.write('\t\t\t<th data-sortable="true">' + col + '</th>\r')
            html.write('\t\t</tr>\r\t</thead>\r')
            html.write('\t<tbody>\r')
        else:
            html.write('\t\t<tr>\r')
            for col in row:
                html.write('\t\t\t<td>' + col + '</td>\r')
            html.write('\t\t</tr>\r')

        r += 1
    html.write('\t</tbody>\r')
    html.write('</table>\r')
    
    html.write('''
<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.0/jquery.min.js"></script>

<!-- Latest compiled and minified JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>

<!-- Latest compiled and minified JavaScript -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.8.1/bootstrap-table.min.js"></script>
''')

os.remove("books.txt")
os.remove("all_files.csv")
