import unittest
import psycopg2
from unittest.mock import patch, MagicMock
from python_example import get_data_from_db

class TestGetDataFromDb(unittest.TestCase):

    @patch('psycopg2.connect')
    def test_get_data_from_db(self, mock_connect):
        # Arrange
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        mock_cur.fetchall.return_value = [('test',)]

        # Act
        result = get_data_from_db()

        # Assert
        self.assertEqual(result, [('test',)])
        mock_connect.assert_called_with("dbname=week_long_project user=your_user password=your_password")
        mock_conn.cursor.assert_called_once()
        mock_cur.execute.assert_called_with("SELECT * FROM raw_data")
        mock_cur.fetchall.assert_called_once()
        mock_cur.close.assert_called_once()
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
