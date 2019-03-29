import merger
import pytest
import os
import pandas
import numpy

class Test_Aggregators(object):

    @pytest.fixture(scope="class")
    def load_data(self):

        #Load Jan's data
        this_merger = merger.Merger()
        this_merger.folder.input_folder = '../test_data/'
        this_merger.params.contract = 'F_BRN_'
        this_merger.params.aggregation_time_factor = '1min'

        files_dict = this_merger.make_file_list()
        keys = files_dict.keys()
        all_tick_df = []
        
        for key in sorted(keys):
            for file_name in files_dict[key].FILE_NAME:
                file_in     =  os.path.join(*[this_merger.folder.input_folder, file_name])
                tick_df = pandas.read_csv(file_in,
                                              compression  = 'gzip')

                #Fill expiration date
                tick_df['EXPIRATION_DATE'] = 20190616

                #Drop non-trade columns
                tick_df = tick_df.dropna(subset = ['TRADE_SIZE'])

                #Set index to datetime and fill 'BA_SPREAD' and 'N_TRADES'
                tick_df['datetime'] = pandas.to_datetime(tick_df.ACTIVITY_DATETIME, format  = '%Y-%m-%d %H:%M:%S.%f UTC')
                tick_df = tick_df.set_index('datetime')
                tick_df['BA_SPREAD'] = tick_df['ASK_PRICE'] - tick_df['BID_PRICE']
                tick_df['N_TRADES'] = tick_df['TRADE_SIZE']

                all_tick_df.append(tick_df)

        #Load aggreg_data     
        all_aggreg_df = []

        for tick_df in all_tick_df:
            aggreg_df    = this_merger.aggreg_data(tick_df)
            all_aggreg_df.append(aggreg_df)

        return all_tick_df, all_aggreg_df
    
    # Test 'ASK_PRICE'
    def test_ask_price(self, load_data):
        all_tick_df = load_data[0]
        all_aggreg_df = load_data[1]
        
        for i in range(len(all_tick_df)):
            assert all_tick_df[i].ASK_PRICE[-1] == all_aggreg_df[i].ASK_PRICE[0]

    # Test 'BID_PRICE'
    def test_bid_price(self, load_data):
        all_tick_df = load_data[0]
        all_aggreg_df = load_data[1]

        for i in range(len(all_tick_df)):
            assert all_tick_df[i].BID_PRICE[-1] == all_aggreg_df[i].BID_PRICE[0]
    

    # Test low price
    def test_low_price(self, load_data):
        all_tick_df = load_data[0]
        all_aggreg_df = load_data[1]

        for i in range(len(all_tick_df)):
            assert all_tick_df[i].TRADE_PRICE.min() == all_aggreg_df[i].low[0]
    
    # Test high price
    def test_high_price(self, load_data):
        all_tick_df = load_data[0]
        all_aggreg_df = load_data[1]

        for i in range(len(all_tick_df)):
            assert all_tick_df[i].TRADE_PRICE.max() == all_aggreg_df[i].high[0]
    
    # Test open price
    def test_open_price(self, load_data):
        all_tick_df = load_data[0]
        all_aggreg_df = load_data[1]

        for i in range(len(all_tick_df)):
            assert all_tick_df[i].TRADE_PRICE[0] == all_aggreg_df[i].open[0]
    
    # Test close price
    def test_close_price(self, load_data):
        all_tick_df = load_data[0]
        all_aggreg_df = load_data[1]

        for i in range(len(all_tick_df)):
            assert all_tick_df[i].TRADE_PRICE[-1] == all_aggreg_df[i].close[0]

    # Test volume
    def test_volume(self, load_data):
        all_tick_df = load_data[0]
        all_aggreg_df = load_data[1]

        for i in range(len(all_tick_df)):
            assert all_tick_df[i].TRADE_SIZE.sum() == all_aggreg_df[i].volume[0]

    # Test N trades
    def test_n_trades(self, load_data):
        all_tick_df = load_data[0]
        all_aggreg_df = load_data[1]

        for i in range(len(all_tick_df)):
            assert all_tick_df[i].N_TRADES.sum() == all_aggreg_df[i].N_TRADES[0]

    # Test BA spreads
    def test_ba_spreads(self, load_data):
        all_tick_df = load_data[0]
        all_aggreg_df = load_data[1]

        for i in range(len(all_tick_df)):
            assert all_tick_df[i].BA_SPREAD.median() == all_aggreg_df[i].BA_SPREAD[0]

    # Test tas_seq_first
    def test_tas_seq_first(self, load_data):
        all_tick_df = load_data[0]
        all_aggreg_df = load_data[1]

        for i in range(len(all_tick_df)):
            assert all_tick_df[i].TAS_SEQ[0] == all_aggreg_df[i].tas_seq_first[0]

    # Test tas_seq_last
    def test_tas_seq_last(self, load_data):
        all_tick_df = load_data[0]
        all_aggreg_df = load_data[1]

        for i in range(len(all_tick_df)):
            assert all_tick_df[i].TAS_SEQ[-1] == all_aggreg_df[i].tas_seq_last[0]
