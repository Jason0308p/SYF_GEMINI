import unittest
import psycopg2
from unittest.mock import patch, MagicMock
from python_example import etl_pipeline

class TestEtlPipeline(unittest.TestCase):

    @patch('psycopg2.connect')
    def test_etl_pipeline(self, mock_connect):
        # Arrange
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        mock_cur.fetchall.return_value = [(1, 'John', 'Doe', 'john.doe@example.com')]

        # Act
        etl_pipeline()

        # Assert
        mock_connect.assert_called_with("dbname=week_long_project user=your_user password=your_password")
        mock_conn.cursor.assert_called_once()
        mock_cur.execute.assert_any_call("SELECT id, first_name, last_name, email FROM raw_data")
        mock_cur.execute.assert_any_call("INSERT INTO clean_data (id, first_name, last_name, email) VALUES (%s, %s, %s, %s)", (1, 'John', 'Doe', 'john.doe@example.com'))
        mock_conn.commit.assert_called_once()
        mock_cur.close.assert_called_once()
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
