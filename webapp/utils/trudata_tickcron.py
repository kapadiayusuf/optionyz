
import requests,json
from truedata_ws.websocket.TD import TD
import pandas as pd
from datetime import date,datetime
import time
from copy import deepcopy
import random
from bs4 import BeautifulSoup

from webapp.utils.apimanager import ApiManager

class TruDataTickCron():
    username = 'wssand011'
    password = 'yusuf011'
    apimgr = ApiManager()
    realtime_port = 8082
    td_app = TD(username, password, live_port=realtime_port, historical_api=False)

    def getSymbols(self,scrip=''):
        
        screenerdata = self.apimgr.getScreenerDF(scrip)
        heatmapdata=self.apimgr.getHeatMapDF('',scrip)
        print(screenerdata)
        print(heatmapdata)

    def disconnect(self):
        try:
            self.td_app.disconnect()
        except Exception as e:
            {}

    def getTickFromTruData(self):
        # Default production port is 8082 in the library. Other ports may be given to you during trial.
        
        sampledata_str="{'symbol': 'BANKNIFTY22011338000CE', 'symbol_id': 300567792, 'timestamp': datetime.datetime(2022, 1, 11, 12, 54, 22), 'ltp': 524.55, 'ltq': 150.0, 'atp': 474.47, 'ttq': 12639200, 'open': 495.0, 'high': 647.85, 'low': 355.0, 'prev_close': 549.55, 'oi': 1128125, 'prev_oi': 1118750, 'turnover': 0.0, 'best_bid_price': 523.8, 'best_bid_qty': 75.0, 'best_ask_price': 524.7, 'best_ask_qty': 125.0}"
        
        print('Starting Real Time Feed.... ')
        print(f'Port > {self.realtime_port}')

        req_ids = self.td_app.start_live_data(self.symbols)
        live_data_objs = {}

        time.sleep(1)

        for req_id in req_ids:
            live_data_objs[req_id] = deepcopy(self.td_app.live_data[req_id])
            print(f'touchlinedata -> {self.td_app.touchline_data[req_id]}')

        while True:
        
                for req_id in req_ids:
                    if not self.td_app.live_data[req_id] == live_data_objs[req_id]:
                        print(self.td_app.live_data[req_id])  # your code in the previous version had a  print(td_app.live_data[req_id]).__dict__ here.
                        # live_data_objs[req_id] = deepcopy(self.td_app.live_data[req_id])

    if __name__ == '__main__':