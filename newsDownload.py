# Import pandas and numpy
import pandas as pd
import numpy as np
import datetime as dt
from GoogleNews import GoogleNews
import json

dates_file = open("./data/dates.json")
dates_dict = json.load(dates_file)
dates_file.close()

for each in dates_dict:
    dates_dict[each] = dt.datetime.strptime(dates_dict[each], "%Y-%m-%d")

googlenews = GoogleNews(lang='en', start=dates_dict['min_date'],end=dates_dict['max_date'])
keywords = ['Apple-Stock', 'Apple-Revenue', 'Apple-Sales', 'Apple', 'AAPL']
article_info = pd.DataFrame(columns=['Date', 'Time', 'Title', 'Articles', 'Link'])

# Gathering all the data of the current page to one dataframe
def newsfeed(article_info, raw_dictionary):
    for i in range(len(raw_dictionary)-1):
        if raw_dictionary is not None:
            # Fetch the date and time and convert it into datetime format
            date = raw_dictionary[i]['datetime']
            date = pd.to_datetime(date)
            # Fetch the title, time, description and source of the news articles
            title = raw_dictionary[i]['title']
            time = raw_dictionary[i]['date']
            articles = raw_dictionary[i]['desc']
            link = raw_dictionary[i]['link']
            # Append all the above information in a single dataframe
            article_info = article_info.append({'Date': date, 'Time': time, 'Title': title,
                            'Articles': articles, 'Link': link}, ignore_index=True)
        else:
            break
    return article_info

# Dataframe containing the news of all the keywords searched
articles = pd.DataFrame()

# Each keyword will be searched seperately and results will be saved in a dataframe
for steps in range(len(keywords)):
    string = (keywords[steps])
    googlenews.search(string)

    # Fetch the results
    result = googlenews.results()

    # Number of pages up to which you want to fetch news articles
    total_pages = 1

    for steps in range(total_pages):
        # Variable consists of pages specified by user so using "for loop" to retrieve all the data in dataframe
        googlenews.get_page(steps)
        feed = newsfeed(article_info, result)
        
    articles = articles.append(feed)

    # Clear off the search results of previous keyword to avoid duplication
    googlenews.clear()

shape = articles.shape[0]

# Resetting the index of the final result
articles.index = np.arange(shape)
articles.head()
