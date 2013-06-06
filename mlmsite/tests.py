"""
Tests for mlmsite module. These will pass when you run "manage.py test".
"""
import unittest
#from test_package import test_neo4j_tutorial
#from test_package import test_models_distributor
from test_package import test_binary_tree_logic
from test_package import test_controller
from test_package import test_position_manager


def suite():
    return unittest.TestSuite([
        #test_neo4j_tutorial.TheTestSuite(),
        test_binary_tree_logic.TheTestSuite(),
        test_controller.TheTestSuite(),
        test_position_manager.TheTestSuite(),
        #test_models_distributor.TheTestSuite(),
        ])
