
import json
from webapp.utils.trendlynescraper import TrendLyneScraper
#from webapp.utils.opstascraper import OpstraScraper
import time
import os

class OptionsCron():
    
    def getFilePath(self):
        # if("E:" in os.getcwd()):
        #     # return "/Users/noaman/Documents/DATA/dev/code/Django/optionstrader/webapp/utils/"
        #     #return "/Users/noam/Documents/dev/code/django/optionstrader/webapp/utils/"
        #     return "/optionstrader/webapp/utils/"
        # else:
        #     return "/var/www/optionstrader/webapp/utils/"
        return "C://django_projects/code/optionstrader/webapp/utils/"

    def fetchTrendLyneHeatMap(self):
        timestamp = int(time.time()*1000.0)
        tScraper = TrendLyneScraper()
        data=tScraper.getTrendLyneHeatMap()
        
        json_data={"last_updated":timestamp,"data":data}
        #local
        # with open('optionsheatmap.json', 'w') as convert_file:

        #production
        with open(self.getFilePath()+'optionsheatmap.json', 'w+') as convert_file:
            convert_file.write(json.dumps(json_data))

    def fetchTrendScreeners(self):
        timestamp = int(time.time()*1000.0)
        tScraper = TrendLyneScraper()
        data=tScraper.getTrendLyneOptionScreenrs()
        print(timestamp)
        print(data)
        json_data={"last_updated":timestamp,"data":data}
        #local
        # with open('optionsheatmap.json', 'w') as convert_file:

        #production
        if not data:
            with open(self.getFilePath()+'options_screener.json', 'w') as convert_file:
                convert_file.write(json.dumps(json_data))
            
        
    def fetchTrendLyneHeatMapContracts(self):
        timestamp = int(time.time()*1000.0)
        tScraper = TrendLyneScraper()
        data=tScraper.getTrendLyneHeatMap()
        
        json_data={"last_updated":timestamp,"data":data}
        #local
        # with open('optionsheatmap.json', 'w') as convert_file:

        #production
        with open(self.getFilePath()+'optionsheatmapcontracts.json', 'w+') as convert_file:
            convert_file.write(json.dumps(json_data))
    
    
if __name__ == '__main__':
    opCron = OptionsCron()
    print(os.getcwd(), "dev" in os.getcwd())
    print(opCron.getFilePath())
    opCron.fetchTrendLyneHeatMap()
    opCron.fetchTrendScreeners()