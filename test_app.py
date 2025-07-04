import unittest
from app import app

class TodoAppTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)

    def test_add_todo(self):
        res = self.client.post('/todos', json={"task": "Study DevOps"})
        self.assertEqual(res.status_code, 201)

    def test_get_todos(self):
        self.client.post('/todos', json={"task": "Test App"})
        res = self.client.get('/todos')
        self.assertTrue(len(res.get_json()) > 0)

if __name__ == '__main__':
    unittest.main()
