from unittest.mock import patch, MagicMock
from urlinformation.utils import extract_url_information, is_safe_url, normalize_url


def test_extract_url_information():
    url = 'https://example.com'

    html = '''
    <html>
        <head>
            <title>Test Title</title>
            <link rel='stylesheet' href='style.css' />
        </head>
        <body>
            <img src='img1.png' />
            <img src='img2.jpg' />
        </body>
    </html>
    '''

    mock_response = MagicMock()
    mock_response.content = html.encode('utf-8')

    with patch('urlinformation.utils.requests.get', return_value=mock_response):
        data = extract_url_information(url)

    assert data['title'] == 'Test Title'
    assert data['domain_name'] == 'example.com'
    assert data['protocol'] == 'https'
    assert data['images'] == ['img1.png', 'img2.jpg']
    assert data['stylesheets'] == 1


def test_is_safe_url_safe():
    url = 'https://example.com'

    post_response = MagicMock()
    post_response.status_code = 200
    post_response.json.return_value = {
        'data': {'id': 'analysis-123'}
    }

    get_response = MagicMock()
    get_response.json.return_value = {
        'data': {
            'attributes': {
                'stats': {
                    'malicious': 0,
                    'suspicious': 0
                }
            }
        }
    }

    with patch('urlinformation.utils.requests.post', return_value=post_response):
        with patch('urlinformation.utils.requests.get', return_value=get_response):
            assert is_safe_url(url) is True


def test_is_safe_url_malicious():
    url = 'https://malicious.com'

    post_response = MagicMock()
    post_response.status_code = 200
    post_response.json.return_value = {
        'data': {'id': 'analysis-malicious'}
    }

    get_response = MagicMock()
    get_response.json.return_value = {
        'data': {
            'attributes': {
                'stats': {
                    'malicious': 2,
                    'suspicious': 0
                }
            }
        }
    }

    with patch('urlinformation.utils.requests.post', return_value=post_response):
        with patch('urlinformation.utils.requests.get', return_value=get_response):
            assert is_safe_url(url) is False


def test_is_safe_url_api_failure():
    url = 'https://fail.com'

    post_response = MagicMock()
    post_response.status_code = 500  # simulate error

    with patch('urlinformation.utils.requests.post', return_value=post_response):
        assert is_safe_url(url) is False


def test_normalized_url_with_backslash():
    url = 'https://test.com/'
    expected = 'https://test.com'
    assert normalize_url(url) == expected


def test_normalized_url_without_backslash():
    url = 'https://test.com'
    assert normalize_url(url) == url
