"""
Test Django custome commands
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

"""mock behaviour/command of database"""
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test Commands"""
    
    def test_wait_for_db_ready(self, patched_check):
        """Test wiating for db ready"""
        patched_check.return_value = True # mock the behaviour of the check function

        call_command('wait_for_db') # call the command

        patched_check.assert_called_once_with(databases=['default'])  # check if the command is called with the right database
        
    @patch('time.sleep')  # mock the time.sleep function
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for db when getting OperationalError"""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]  
        # call the check function 6 times, the first 5 times it will raise an error and the 6th time it will return True
        
        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6) # check if the check function is called 6 times
        patched_check.assert_called_with(databases=['default'])  # check if the command is called with the right database