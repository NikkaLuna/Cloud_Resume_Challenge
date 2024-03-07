import unittest
from unittest.mock import Mock
from lambda_function import lambda_handler

class TestLambdaHandler(unittest.TestCase):

    def test_lambda_handler_success(self):
        # Mock DynamoDB resource and table
        mock_table = Mock()
        mock_table.get_item.return_value = {'Item': {'views': 5}}
        mock_table.put_item.return_value = {}

        # Mock context object
        context = Mock()

        # Call the Lambda handler
        event = {}
        response = lambda_handler(event, context)

        # Assert the response
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], '{"views": 6}')
        mock_table.put_item.assert_called_once_with(Item={'id': '0', 'views': 6})

    def test_lambda_handler_exception(self):
        # Mock DynamoDB resource and table
        mock_table = Mock()
        mock_table.get_item.side_effect = Exception("DynamoDB Error")

        # Mock context object
        context = Mock()

        # Call the Lambda handler
        event = {}
        response = lambda_handler(event, context)

        # Assert the response
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('error', response['body'])

if __name__ == '__main__':
    unittest.main()
