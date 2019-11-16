
def urljoin(path, part):
    """
    returns joined url
    """
    path = path if path[-1] == '/' else '{}/'.format(path)
    return '{}{}'.format(path, part)