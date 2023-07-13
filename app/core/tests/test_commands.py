"""
Test Django custome commands
"""
from unittest.mock import patch

from psycropg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTetCase

"""mock behaviour/command of database"""
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTetCase):
    """Test Commands"""
    
    def test_wait_for_db_ready(self, patched_check):
        """Test wiating for db ready"""
        patched_check.return_value = True # mock the behaviour of the check function

        call_command('wait_for_db') # call the command

        patched_check.assert_called_once_with(database=['default'])  # check if the command is called with the right database
        