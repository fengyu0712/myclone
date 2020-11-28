from rest_framework.test import APITestCase
from rest_framework.test import APIClient

class TestCase(APITestCase):
    '''
    test case
    '''
    def testcase(self):
        response = self.client.get('http://www.baidu.com')
        self.assertEqual(response.status, 200)
