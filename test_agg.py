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
        files_dict = this_merger.make_file_list()
        keys = files_dict.keys()
        tick_df_list = []
        for key in keys:
            for file_name in files_dict[key].FILE_NAME:
                file_in     =  os.path.join(*[this_merger.folder.input_folder, file_name])
                tick_df = pandas.read_csv(file_in,
                                              compression  = 'gzip')

                #Fill expiration date
                tick_df['EXPIRATION_DATE'] = 20190616

                #Drop non-trade columns
                tick_df = tick_df.dropna(subset = ['TRADE_SIZE'])

                tick_df_list.append(tick_df)

        return tick_df_list
        
    def test_aggreg_data(self, load_data):
        #this_merger.aggregation_time_factor = '1min'
        print(load_data)
        assert 1 == 1
