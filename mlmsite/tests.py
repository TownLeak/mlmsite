"""
Tests for mlmsite module. These will pass when you run "manage.py test".
"""
import unittest
from test_package import test_models_position
from test_package import test_models_binary_position
from test_package import test_models_user
from test_package import test_binary_tree
from test_package import test_unilevel_tree
from test_package import test_tree
from test_package import test_controller


def suite():
    return unittest.TestSuite([
        test_models_binary_position.TheTestSuite(),
        test_binary_tree.TheTestSuite(),
        test_tree.TheTestSuite(),
        test_unilevel_tree.TheTestSuite(),
        test_models_position.TheTestSuite(),
        test_models_user.TheTestSuite(),
        test_controller.TheTestSuite(),
    ])
