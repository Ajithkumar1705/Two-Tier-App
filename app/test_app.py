import unittest
from unittest.mock import patch
from app import app
class BasicTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_health_endpoint_returns_200_when_db_ok(self):
        with patch('app.get_connection') as mock_conn:
            mock_conn.return_value.close.return_value = None
            response = self.app.get('/health')
            self.assertEqual(response.status_code, 200)

    def test_health_endpoint_returns_500_when_db_down(self):
        with patch('app.get_connection', side_effect=Exception("connection refused")):
            response = self.app.get('/health')
            self.assertEqual(response.status_code, 500)

    def test_index_page_loads(self):
        with patch('app.get_connection') as mock_conn:
            mock_cursor = mock_conn.return_value.cursor.return_value
            mock_cursor.fetchall.return_value = [("test-user",)]
            response = self.app.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"test-user", response.data)