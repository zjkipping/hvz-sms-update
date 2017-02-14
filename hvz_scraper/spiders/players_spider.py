import scrapy


class PlayerInfo(scrapy.Item):
    name = scrapy.Field(serializer=str)
    status = scrapy.Field(serializer=str)
    link = scrapy.Field(serializer=str)

class PlayersSpider(scrapy.Spider):
    name = "players"
    custom_settings = {
        'FEED_URI' : 'players.json',
        'FEED_FORMAT' : 'json',
        'FEED_EXPORT_ENCODING' : 'utf-8'
    }
    start_urls = [
        'http://muzombies.org/playerlist?filterBy=all&sortBy=name&pageBy=1000',
    ]

    def parse(self, response):
        players = response.xpath('body/div[@id="body_container"]/div[@class="content_column"]/div[@id="content"]/div[@id="body_content"]/div[@id="playerlist_table_container"]/table')
        x = 1
        for player in players.xpath('tr[@class="playerlist_table_row"]'):
            x += 1
            y = 1
            player_object = PlayerInfo(name="", status="")
            for td in player.xpath('td[@class="playerlist_table_cell"]'):
                if y == 1:
                    player_object['name'] = td.xpath('a/text()')[0].extract()
                    player_object['link'] = td.xpath('a/@href')[0].extract()
                elif y == 3:
                    player_object['status'] = td.xpath('text()')[0].extract()
                y+=1
            player_object['status'] = ''.join(player_object['status'].split())
            player_object['link'] = player_object.replace("//", "")
            yield player_object
