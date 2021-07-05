from unittest.mock import Mock, patch

def test_list():
    with patch('boto3.resource') as mock_dynamo:
        mock_table = Mock()
        mock_table.scan.return_value = {"Items": [{"title":"Mock Ad"}]}
        mock_dynamo.return_value.Table.return_value = mock_table
        from advertisement import list
        resp = list({"queryStringParameters": {}}, None)
        assert resp['statusCode'] == 200
        assert resp['body'] == '["Mock Ad"]'