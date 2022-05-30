# Dynamic Web Scraper
This web scraper is a Python script that scrapes [Lonely Planet](https://www.lonelyplanet.com/) and the Internet Movie Database ([IMDb](https://www.imdb.com/)), for information on world cities and TV series **statically** (scraping a given page URL's contents) and **dynamically** (scraping the results dependent on a search term, to then scrape the chosen (by user) search result's page). 

The script calls a class whose methods have been unit-tested. The tests are kept together in a single package to simplify the running of all tests and to improve reusability of any pytest configurations and fixtures across all tests.

Two of my previous projects have made use of this scraper, when it was less robust (untested at the time): [Holistars](https://github.com/emilydaykin/Holistars-Server) and [ISDb](https://github.com/emilydaykin/Internet-Series-Database-API).

https://testdriven.io/blog/modern-tdd/

