def make_response(response):
    headers = dict(response.headers)
    content_encoding = headers.get('Content-Encoding')
    if content_encoding == 'gzip' or content_encoding == 'deflate':
        del headers['Content-Encoding']
    if headers.get('Transfer-Encoding'):
        del headers['Transfer-Encoding']
    if headers.get('Accept-Ranges'):
        del headers['Accept-Ranges']
    headers['Content-Length'] = len(response.content)
    return response.content, response.status_code, headers.items()
