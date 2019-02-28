from support_functions_1 import Strat_0
import numpy as np
import pytest

class TestStrat_0(object):
    
    # Run this method once, before all other tests in the class
    @pytest.fixture(scope="class")
    def file_list(self):
        this_strat = Strat_0() 
        this_strat.params.folder_path = 'strats_output'
        this_strat.adjust_folders()
        this_strat.reset_envnmt()
        this_strat.reset_augmented_data()
        this_strat.set_universum()
        file_list  = this_strat.build_data_set()
        return file_list
    
    # Test build_data_set method to ensure no overlap between fit and test set
    def test_build_data_set(self, file_list):
         fit_set = file_list['fit_set'][24180]
         test_set = file_list['test_set'][24181]
          # Get max begin and end index of fit test
         fit_begin_index = fit_set['index_begin'].max()
         fit_end_index = fit_set['index_end'].max()
          # Get min begin and end index of test set
         test_begin_index = test_set['index_begin'].min()
         test_end_index = test_set['index_end'].min()
         # Sort fit and test set by t-strings and compare
         fit_set.sort_values('t_string', inplace=True)
         test_set.sort_values('t_string', inplace=True)

         assert fit_begin_index < test_begin_index
         assert fit_end_index < test_end_index
         assert np.array_equal(fit_set['t_string'].values, test_set['t_string'].values) is True