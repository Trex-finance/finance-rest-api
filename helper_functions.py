def build_url(base_url, url_components):
    url = base_url
    for component in url_components:
        url = '{}/{}'.format(url, component)
    return url