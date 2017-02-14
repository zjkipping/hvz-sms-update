# Mizzou Humans vs Zombies SMS Updater
A project using Python with Scrapy and Twilio API to send SMS updates when a Human turns Zombie in the Mizzou HVZ event

## Requirements
Used python version 3.5.2, can't verify other versions with latest Twilio and Scrapy  
Need to install:  
Twilio - https://www.twilio.com/docs/libraries/python  
Scrapy - https://doc.scrapy.org/en/latest/intro/install.html

## Running For Yourself
Make sure above requirements/installations are met.

To run the project yourself and receive updates, sign up for a free trial account on Twilio here:
https://www.twilio.com/signup  
After this just plug in your Account SID and Auth Token where the comments in the code of "sms-updater.py" point to.
And also fill in your Twilio given sms number and your personal number where shown by the comments.
Finally run the "run.bat" (you can change the ascribed timeouts in the file to your own preferences)

## Extra Inclusions
Included is a version (can be old) of the "http://muzombies.org/playerlist?filterBy=all&sortBy=name&pageBy=1000" page.
This is in case you want to re-use the scraper in this project and run your own processes on the data received from it.  
The html file is a great resource when figuring where to xpath to get the data from the website you want.  
More help on scraping can be found here https://doc.scrapy.org/en/latest/  

The html file can be updated with a new simple spider file with the below code:
```python
import scrapy


class PlayerPageSpider(scrapy.Spider):
    name = "playerpage"
    start_urls = [
        'http://muzombies.org/playerlist?filterBy=all&sortBy=name&pageBy=1000',
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'muzombies-playerlist.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
```
