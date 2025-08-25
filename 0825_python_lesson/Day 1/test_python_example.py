import unittest
import pandas as pd
from python_example import clean_data

class TestCleanData(unittest.TestCase):

    def test_clean_data(self):
        data = {'id': [1, 2, 3],
                'first_name': ['Deb', 'Ulises', 'Moishe'],
                'last_name': ['Headley', 'Botterill', 'Botting'],
                'email': ['dheadley0@symantec.com', 'ubotterill1@g.co', 'mbotting2@live.com'],
                'gender': ['Female', 'Male', 'Male'],
                'ip_address': ['37.215.73.225', '124.21.194.244', '128.216.234.239']}
        df = pd.DataFrame(data)

        cleaned_df = clean_data(df)

        self.assertEqual(len(cleaned_df.columns), 4)
        self.assertNotIn('gender', cleaned_df.columns)
        self.assertNotIn('ip_address', cleaned_df.columns)

if __name__ == '__main__':
    unittest.main()
