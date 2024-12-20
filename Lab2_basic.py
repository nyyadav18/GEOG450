# -*- coding: utf-8 -*-
"""Copy of Yelp_API Crawler_Yifan.ipynb

By Yifan Shen

### My explanation: 
- output is a list or a table
- basic API crawling with simple data output (Pandas df or CSV)
- directly pulls and processes data from Yelp
- focuses on fetching max amount of allowable data

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TWTayzuP_7lYcAFeN95pxY8KsPA5H4Lu

# Yelp Web Scraping

**In the practice we will use requests+json to develop a simple but efficient Yelp crawler (offical API based)**

In lots of situation, we can get data from popular platforms such as google map, Yelp etc. using their official Web APIs. To use these Web APIs, you will need a developer account for the target platform, and in general, there are QPS and amount limit for the free quota. Of course you can always buy more quota if your want (a little expensive for students).

For google and Yelp's APIs such as Yelp's "Bussiness Search", each request will just return a small amount of data (the entire data is divied into a bunch of pages), and there is a limitation of the total results you can get in a single research. For example, in Seattle, WA, there may be 30000 restuarants, however in a single search your can get no more than 1000 resturants, and the result is divided into 20 pages, each page contains 50 records (one request, one page). To approximate the real number "30,000", you will need advanced techniques such as grid search algorithm or recursive search algorithm. We wouldn't learn about thse advanced techniques in this turtorial, but we will manage to get the allowed max num in one single serach by simply retrieve data in different pages.

### Key Knowledges:
- Workflow of a web crawler
  - send request-> recieve response-> extract needed information from the response->reformat and storage
- Yelp Fusion API
  - the official web APIs of Yelp, you can get Yelp's data using these APIs
  - more info refer to: https://www.yelp.com/developers/documentation/v3/business_search
  - in the practice, we will use two API called "Bussiness Search" and "Comments"
- Request
  - send a request to a server and get the response
  - the content of the response can be json, html, image etc.
- Json
  - A key-value style data format, used widely in transmit web data
  - We use libary json in python to extract needed information from returned data of a web request

by Yifan
"""

#Read the following source code to learn basic skills of developing a web crawler based on official API

#pip install requests json pandas
#For colab, requests,json,pandas are pre-installed

import requests
import json
import math
import pandas as pd
import time


# API Path
BUSINESS_SEARCH="https://api.yelp.com/v3/businesses/search"
REVIEWS="https://api.yelp.com/v3/businesses/id/reviews"

# API Key (Please change to your own key)
# See https://www.yelp.com/developers/v3/manage_app
# To acquire API KEY, open https://docs.developer.yelp.com/docs/fusion-authentication page and follow steps to Create an app on Yelp Developers site
API_KEY='7FYXYsDjkEW_kIbK2_3GZPUnHWXsyxftyUrujJbXlXuBEvjWpRLqY0f3EerLSCh7cABXowaKUEk7bWnxy7KRKpZZGSksOh2O7W_jSDASg2ss0mcLfToOxQ-3Oh64ZXYx'
HEADER = {
      'Authorization': 'Bearer %s' % API_KEY,
  }

# constant params
MAX=1000
LIMIT=50


def yelp_search(term='bar',location='georgetown, WA 98108',pause=0.25,includeComments=False):
  """Extract information of Yelp (By Yifan)

  Retrieves basic information (max 1000 items) and attached comments (max 3 comments each item) of Yelp search
  Key reference: https://www.yelp.com/developers/documentation/v3/business_search

  Args:
    term: Search term, for example "food" or "restaurants". The term may also be business names, such as "Starbucks".
    location: Geographic area to be used when searching for businesses. Examples: "New York City", "NYC", "350 5th Ave, New York, NY 10118". Businesses returned in the response may not be strictly within the specified location.
    pause: Speed contral, single pause time (s) for avoiding overheated QPS
    includeComments: whether to retrived attached comments

  Returns:
    A pandas dataframe
    if includesComments=False: the dataframe will contains 12 columns(content_id,name,rating,reviews,phone,address,city,state,country,postcode,latitude,longitude)
    else: the dataframe will contains addtional 5 columns (comment_id,user_id,user_name,user_rating,comment)
    A list, which contains 9 items (content_id,name,rate,review,tags,address,city,state,postcode)
    the content_id is important - we need it to further request comments
  """

  params = {
        'term': term,
        'location': location,
        'limit': LIMIT,
        }
  #determine how many term are at the location and how many we can get
  # the "total" in current API is limited to 240, in other words, it no long reflect the real number of bussiness in the area
  # if it works, the alternative code for "total=MAX" should work
  #--------------------alternative code----------
  # total= json.loads(requests.request('GET',BUSINESS_SEARCH, headers=headers,params=params).text)['total']
  # print('there are {} {} at {}'.format(total,term,location))
  # if total>MAX:
  #   total=MAX

  total=MAX

  #calculate the offset list we need to retrive the research list
  offsets=[i*LIMIT for i in range(math.ceil(total/LIMIT))]

  # initial the result list
  rst=[]
  print('**********Start**********')
  #retrive data according to offset list
  for offset in offsets:
    print("Retrieving: {}/{}".format(offset,total))
    time.sleep(pause)
    params['offset']=offset
    response = requests.request('GET',BUSINESS_SEARCH, headers=HEADER,params=params)
    data = json.loads(response.text)['businesses'] # turn the responese's json string to dictionary
    for item in data:             # extract data we need in loop
      # get basic information
      content_id=item['id']
      name=item['name']
      rating=item['rating']
      reviews=item['review_count']
      phone=item['phone']
      address=item['location']['address1']
      city=item['location']['city']
      state=item['location']['state']
      country=item['location']['country']
      postcode=item['location']['zip_code']
      latitude=item['coordinates']['latitude']
      longitude=item['coordinates']['longitude']
      rst.append([content_id,name,rating,reviews,phone,address,city,state,country,postcode,latitude,longitude])
  # rst=rst[0:total] #drop redundant duplicates which is due to the mechanism of offset
  # reformate the result list to a pandas dataframe
  df=pd.DataFrame(data=rst,columns=["content_id","name","rating","reviews",
                                    "phone","address","city","state","country",
                                    "postcode","latitude","longitude"])
  df.drop_duplicates('content_id','first',inplace=True)
  print("{} {} at {} Retrieved.".format(len(df),term,location))
  #retrive additional comments
  if includeComments:
    rst=[]
    for i,content_id in zip(range(len(df['content_id'])),df['content_id']):
      if (i+1)%5==0:
        print("Comments Retrieving: {}/{}".format(i+1,len(df['content_id'])))
        time.sleep(pause)
      response = requests.request('GET',REVIEWS.replace('id',content_id), headers=HEADER)
      data = json.loads(response.text)['reviews']
      cmts=[]
      for comment in data:
        comment_id=comment['id']
        user_id=comment['user']['id']
        user_name=comment['user']['name']
        user_rating=comment['rating']
        comment=comment['text']
        rst.append([content_id,comment_id,user_id,user_name,user_rating,comment])
    cdf=pd.DataFrame(data=rst,columns=["content_id","comment_id","user_id",
                                     "user_name","user_rating","comment"])
    print('{} attached comments retrieved.'.format(len(cdf)))
    df=pd.merge(df,cdf,on='content_id')
  print('**********FINISH**********')
  return df

#Excute Demo: Extract basic information of Yelp search result
#MAX=100 # Just for demo to reduce API usage. Please delete this line in real practice, or set "MAX=1000".
df1=yelp_search(term='bar',location='georgetown, WA 98108',pause=0.25,includeComments=False)
df1

"""## The following code cell will return 100 businesses and costomer reviews. Revise search term and location accordingly and excute the code cell.

**Note**
How many API requests do I receive?

Yelp Fusion API keys registered after May 15, 2023 receive 500 API calls per day by default. These API calls are STRICTLY FOR EVALUATION AND NOT FOR COMMERCIAL DEPLOYMENT. (https://docs.developer.yelp.com/docs/fusion-faq)

--> Do not set "MAX=1000"
"""

#Excute Demo: Extract basic information with comments of Yelp search result
MAX=100 # Just for demo to reduce API usage. Please delete this line in real practice, or set "MAX=1000".
df1=yelp_search(term='things to do',location='georgetown, WA',pause=0.25,includeComments=True)
df1

"""Now the following code will filter the scraped data and store the columns that we need in the next step into a new data frame with myData."""

myData=df1.filter(items=['name','rating','comment', 'latitude', 'longitude'])
myData

"""# **Now you will download data in CSV or JSON and clean.**
1. Don't remember how to download? Review 'Learn Python and Pandas Basic' in Module 1.
2. Open the step 2: Contextualize Your Data in the course Canvas Module 3.
3. Clean your data and upload it to your google drive
4. Load your file as Pandas dataframe.
5. Build a nested database section will guide you to convert the data nested in JSON to feed them into the radial dendrogram template.





"""

# making pd df into csv file
myData.to_csv('/content/drive/MyDrive/GEOG450Lab2/csv/activities.csv')

"""The folloing code cells will save pandas df in csv into your google drive.  """

# Import Drive API and authenticate.
from google.colab import drive

# Mount your Drive to the Colab VM.
drive.mount('/gdrive')

# Write the DataFrame to CSV file.
# Check the file path
with open('/gdrive/MyDrive/GEOG450Lab2/csv/activities.csv', 'w') as f:
  myData.to_csv(f)

from google.colab import drive
drive.mount('/content/drive')

# Download csv in your local drive.
# Check the file path.
from google.colab import files
files.download('/content/drive/MyDrive/GEOG450Lab2/csv/activies.csv')

"""# Build a nested database

This is a process after cleaning the raw data

The following code is a method to create a nested data by a business name. The data includes name, lat, lon, and review and the column review has two nested data of ratings and comment.  
Our particular radial dendrogram creates nodes with the column with 'name'. Note that business names and comments are stored in 'name' column at a different depth in the data hierarchy.
"""

def add_root(df_root):
    for row in df_root.itertuples():
        yield {"name": 'review',
               "children":list(pd_to_review_dict(df_root))
        }
def pd_to_review_dict(df):
    for (name), df_name_grouped in df.groupby(["name"]):
        yield {
            "name": name,
            #"latitude": df.loc[df['name'] == name, 'latitude'].iloc[0],  # if your dataset does not include latitude, comment out this line
            #"longitude": df.loc[df['name'] == name, 'longitude'].iloc[0], # if your dataset does not include longitude, comment out this line
            "children": list(split_line_items(df_name_grouped))
        }

def split_line_items(df_review):
    for row in df_review.itertuples():
        yield {
            "value": row.rating,
            "name": row.comment
        }

"""Now you will ~~pass the data frame from the crawler~~
upload your cleaned csv and read it as pandas dataframe and pass it
  into the method above by running the following code block and it will print the data in json in an output cell and name the data in json format to 'myYepData.
"""

# when pd is not defined, import pandas again
import pandas as pd

# with NameError: name 'json' is not defined, import json
import json

df_pd = pd.read_csv('/content/drive/MyDrive/GEOG450Lab2/csv/finalActivities.csv')  # replace myData with the file path to your csv like pd.read_csv('/content/drive/MyDrive/495/data/myData.csv')
review_list = list(add_root(df_pd))
review_dict = {}
for sub_dict in review_list:
        review_dict.update(sub_dict)
print(json.dumps(review_dict, indent=4))
YelpDataCollection=json.dumps(review_dict)

"""Check if myYelpData has created successfully."""

YelpDataCollection

"""Our data is ready to store in an physical form and download it."""

from google.colab import files

with open('YelpDataCollection.json', 'w') as f:
  f.write(YelpDataCollection)
  files.download('YelpDataCollection.json')

"""myYelpData.json should be in your download folder. Open it in a text editor and begin to develop a context of your neighborhood story.

Last updated Oct. 21. 2022. (Yelp Crawler)
Last updated July 10, 2023 (a nested json conversion)
"""
