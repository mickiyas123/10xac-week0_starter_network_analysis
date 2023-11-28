import unittest
import pandas as pd
import os, sys

rpath = os.path.abspath('..')
if rpath not in sys.path:
    sys.path.insert(0, rpath)

from src.loader import SlackDataLoader

class TestColumnName(unittest.TestCase):

    def test_columns(self):
        slackLoader = SlackDataLoader("../anonymized")
        df  = slackLoader.slack_parser("../anonymized/Week8and9/")

        actual_columns = list(df.columns)

        expected_columns = ['msg_type','msg_content','sender_name','msg_sent_time','msg_dist_type','time_thread_start',
                            'reply_count','reply_users_count','reply_users','tm_thread_end','channel']
        self.assertListEqual(actual_columns, expected_columns)
if __name__ == '__main__':
    unittest.main()
