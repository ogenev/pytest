from support_functions import Strat_0
import pandas as pd
import numpy as np
import pytest
import os

class TestStrat_0(object):
    
    # Run this method once, before all other tests in the class
    @pytest.fixture(scope="class")
    def preload_data(self):
        this_strat = Strat_0() 
        this_strat.params.folder_path = 'strats_output'
        this_strat.adjust_folders()
        this_strat.reset_envnmt()
        this_strat.reset_augmented_data()
        this_strat.set_universum()
        file_list  = this_strat.build_data_set()
        this_strat.make_data_files(file_set = file_list['file_set'])

        fit_set = file_list['fit_set'][24180]
        test_set = file_list['test_set'][24181]
        # Get max begin and end index of fit test
        fit_begin_index_max = fit_set['index_begin'].max()
        fit_end_index_max = fit_set['index_end'].max()
        # Get min begin and end index of test set
        test_begin_index_min = test_set['index_begin'].min()
        test_end_index_min = test_set['index_end'].min()

        return (
                fit_begin_index_max,
                  fit_end_index_max, 
               test_begin_index_min, 
                 test_end_index_min, 
                            fit_set, 
                           test_set
                )
    
    # Test build_data_set method to ensure no overlap between fit and test set
    def test_build_data_set(self, preload_data):

        fit_begin_index_max = preload_data[0]
        fit_end_index_max = preload_data[1]
        test_begin_index_min = preload_data[2]
        test_end_index_min = preload_data[3]

        assert fit_begin_index_max < test_begin_index_min
        assert fit_end_index_max < test_end_index_min
    
    def test_make_data_files(self, preload_data):

        fit_begin_index_max = preload_data[0]
        fit_end_index_max = preload_data[1]
        test_begin_index_min = preload_data[2]
        test_end_index_min = preload_data[3]
        fit_set = preload_data[4]
        test_set = preload_data[5]

        # Get file names for RHS and LHS for fit and test set
        fit_begin_index_max_file = fit_set.loc[fit_set['index_begin'] == fit_begin_index_max, 'file'].values[0]
        fit_end_index_max_file = fit_set.loc[fit_set['index_end'] == fit_end_index_max, 'file'].values[0]
        test_begin_index_min_file = test_set.loc[test_set['index_begin'] == test_begin_index_min, 'file'].values[0]
        test_end_index_min_file = test_set.loc[test_set['index_end'] == test_end_index_min, 'file'].values[0]
        
        parent_dir = os.path.dirname(os.getcwd()) # Test file should be in Strats/code folder
        path = os.path.join(parent_dir, 'strats_output/model/augmented_data/')
        
        # Load RHS files for fit and test set as Dataframe
        fit_begin_index_max_rhs = pd.read_pickle('{}rhs_data/{}'\
                                                               .format(path, fit_begin_index_max_file.rsplit('/', 1)[-1]))

        fit_begin_index_max_rhs = fit_begin_index_max_rhs.loc[fit_begin_index_max_rhs['MONTH_NUM'] == 24180]

        fit_end_index_max_rhs = pd.read_pickle('{}rhs_data/{}'\
                                                               .format(path, fit_end_index_max_file.rsplit('/', 1)[-1]))

        fit_end_index_max_rhs = fit_end_index_max_rhs.loc[fit_end_index_max_rhs['MONTH_NUM'] == 24180]                                        

        test_begin_index_min_rhs = pd.read_pickle('{}rhs_data/{}'\
                                                               .format(path, test_begin_index_min_file.rsplit('/', 1)[-1]))
        
        test_begin_index_min_rhs = test_begin_index_min_rhs.loc[test_begin_index_min_rhs['MONTH_NUM'] == 24181]  

        test_end_index_min_rhs = pd.read_pickle('{}rhs_data/{}'\
                                                               .format(path, test_end_index_min_file.rsplit('/', 1)[-1]))

        test_end_index_min_rhs = test_end_index_min_rhs.loc[test_end_index_min_rhs['MONTH_NUM'] == 24181]

        # Load LHS files
        fit_begin_index_max_lhs = pd.read_pickle('{}lhs_data/{}'\
                                                               .format(path, fit_begin_index_max_file.rsplit('/', 1)[-1]))

        fit_begin_index_max_lhs = fit_begin_index_max_lhs.loc[fit_begin_index_max_lhs['fr_month_num'] == 24180]

        fit_end_index_max_lhs = pd.read_pickle('{}lhs_data/{}'\
                                                               .format(path, fit_end_index_max_file.rsplit('/', 1)[-1]))

        fit_end_index_max_lhs = fit_end_index_max_lhs.loc[fit_end_index_max_lhs['fr_month_num'] == 24180] 

        test_begin_index_min_lhs = pd.read_pickle('{}lhs_data/{}'\
                                                               .format(path, test_begin_index_min_file.rsplit('/', 1)[-1]))

        test_begin_index_min_lhs = test_begin_index_min_lhs.loc[test_begin_index_min_lhs['fr_month_num'] == 24181]  

        test_end_index_min_lhs = pd.read_pickle('{}lhs_data/{}'\
                                                               .format(path, test_end_index_min_file.rsplit('/', 1)[-1]))

        test_end_index_min_lhs = test_end_index_min_lhs.loc[test_end_index_min_lhs['fr_month_num'] == 24181]

        # Test RHS
        assert fit_begin_index_max_rhs.index.max() < test_begin_index_min_rhs.index.min()
        assert fit_end_index_max_rhs.index.max() < test_end_index_min_rhs.index.min()

        # Test LHS
        assert fit_begin_index_max_lhs.fr_t_end.max() < test_begin_index_min_lhs.fr_t_end.min()
        assert fit_end_index_max_lhs.fr_t_end.max() < test_end_index_min_lhs.fr_t_end.min()
