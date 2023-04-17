# Quicknews
A spinoff of HackerNews.

## Getting Started
Create and activate a new virtual environment.
Install the requirements/dependencies using:

```
python -m pip install -r requirements.txt
```

To start fetching/syncing news:

```bash
python quicknews/manage.py get_fresh_news -ri 5 -nr 100

```
where

```bash
 -ri REFRESH_INTERVAL, --refresh-interval REFRESH_INTERVAL
                        Interval (in minutes) to fetch news
  -nr NO_RECORDS, --no-records NO_RECORDS
                        No. records to fetch per API request.
```

Update/Create the database (works perfectly fine with SQLite)

```
python quicknews/manage.py migrate
```

Start the development web server using:

```
python quicknews/manage.py runserver
```

Navigate to https://127.0.0.1/news/news to view the latest news.

## Features
A brief overview of the features I built.
 - A Django management command to start a scheduled job to sync the published news to a DB every 5 minutes. It considers and maints the relations between news items.
 
 - A view to list the latest news;
 - Allow filtering by the type of item
 - Implement a search box for filtering by text
 - Pagination for all views/endpoints
 - In the web view, only display top-level items in the list, and display their children (comments, for example) on a detail page.

## TODO
Some things I think can be improved 
 - Store/persist refresh jobs to track currently being fetched items.
 - Cache search results
 - Write tests...
 - Allow users to "Add news to Favourites".


## Summary
> This code was formatted with Black!

Been quite a week! It was a fun project. Thank you for reading :)

