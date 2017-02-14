import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from hvz_scraper.spiders.players_spider import PlayersSpider
from twilio.rest import TwilioRestClient
import json

class CallBack:
    def __init__(self, data, type):
        self.data = data
        self.type = type

class Change:
    def __init__(self, name, link, orig, new):
        self.name = name
        self.link = link
        self.orig = orig
        self.new = new

def getPlayerData(process):
    type = "old"
    while True:
        try:
            with open("players.json") as data_file:
                data = json.load(data_file)
        except IOError as err:
            type = "new"
            process.crawl(PlayersSpider)
            process.start()
            process.stop()
        else:
            break;
    return CallBack(data=data, type=type)

def getPlayerChanges(old_data, new_data):
    changes = []
    for old_player in old_data:
        for new_player in new_data:
            if old_player['name'] == new_player['name'] and old_player['status'] != new_player['status']:
                if new_player['status'] == 'zombie' or new_player['status'] == 'zombie(oz)':
                    change = Change(name=new_player['name'], link = new_player['link'], orig=old_player['status'], new=new_player['status'])
                    changes.append(change)
    return changes

def sendSMS_Updates(changes):
    if changes == []:
        print("No changes have occurred")
    else:
        print("Sending SMS based on Changes: ")
        client = TwilioRestClient("ACxxxxxxxxxxxxx", "xxxxxxxxxxxxxxxxxxx") # replace these values with your own Twilio Account SID and Auth Token
                                                                            # free trial can be signed up for here https://www.twilio.com/try-twilio
        for change in changes:
            client.messages.create(to="+1234567890", from_="+1234567890", # Also make sure to replace these numbers with your Twilio and personal number
                                   body=(change.name + " changed from " + change.orig.upper() + " to " + change.new.upper() + " link to profile: " + change.link))
            print(change.name, " changed from ", change.orig, " to ", change.new, " link to profile: ", change.link.replace("//", ""))

process = CrawlerProcess(get_project_settings())
print("Attempting to get Old Data")
callback = getPlayerData(process)
old_data = callback.data
if callback.type == "old":
    os.remove('players.json')
    print("Attempting to get New Data")
    new_data = getPlayerData(process).data
    changes = getPlayerChanges(old_data, new_data)
    sendSMS_Updates(changes)
    old_data = new_data
else:
    print("No old data to go off need to re run again to receive updates")
