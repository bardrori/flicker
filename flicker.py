from flickrapi import FlickrAPI
from datetime import datetime
import flickrapi
import mysql.connector
from mysql.connector import errorcode

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Bar7drori!",
  database='mydatabase'
)
if not mydb.is_connected():
    print("Not connected")

mycursor = mydb.cursor()
FLICKR_PUBLIC = '53ad925ee2473b9fa877364a3326adbb'
FLICKR_SECRET = 'c265622669812fe9'


def scrape(keyword, size):
  if size > 0:
    flickr = FlickrAPI(FLICKR_PUBLIC, FLICKR_SECRET, format='parsed-json')
    extras='url_sq'
    try:
      takepic = flickr.photos.search(text=keyword,extras=extras,per_page=size)
    except flickrapi.exceptions.Flickr:
      print("could not get photos")
      return
    for i in range(size):
        photo = takepic['photos']['photo'][i]['url_sq']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO images (imageUrl, scrapeTime, keyword) VALUES (%s, %s, %s)"
        val = [(photo, timestamp, keyword)]
        mycursor.executemany(sql, val) 
        mydb.commit()
    print(mycursor.rowcount, "was inserted.")
  else :
    print("your number is lower than 0")


def search(minScrapeTime, maxScrapeTime, keyword, size):

  minScrapeTime_date = datetime.strptime(minScrapeTime, '%Y-%m-%d %H:%M:%S')
  maxScrapeTime_date = datetime.strptime(maxScrapeTime, '%Y-%m-%d %H:%M:%S')
  
  keyword = str(keyword)
  if size > 0:
    if maxScrapeTime_date>minScrapeTime_date: 
        mycursor = mydb.cursor()
        sql = "select * from images where keyword = '" + keyword + "' and scrapeTime between '" + minScrapeTime + "' and '" + maxScrapeTime+"'"
        mycursor.execute(sql)
        myresult = mycursor.fetchmany(size)
        count = len(myresult)
        if size>count:
          print("found only", count)
        return myresult
    else:
        print("maxScrapeTime smaller than minScrapeTime")
  else:
    print("your number is lower than 0")
print(search('2022-04-10 23:32:50', '2022-04-11 11:00:40', 'bird', 3))