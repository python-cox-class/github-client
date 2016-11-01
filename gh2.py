import requests
import uritemplate


class Client(object):
    root = 'https://api.github.com'

    def __init__(self, access_token):
        self.sess = requests.Session()
        # Set the Authorization header in the session
        self.sess.headers['Authorization'] = 'token {}'.format(access_token)
        self.resources = self.get(self.root)

    def get(self, url):
        """HTTP GET a resource and return its decoded JSON representation.

        This function should GET the given URL, raise an exception on any
        4xx or 5xx errors, and return the decoded JSON representation of
        the response.
        """
        resp = self.sess.get(url)
        resp.raise_for_status()
        return resp.json()

    def get_resource(self, resource_type, **parameters):
        return Resource(
            self, self.resources['{}_url'.format(resource_type)], **parameters)


class Resource(object):

    def __init__(self, client, resource_url, **parameters):
        self.client = client
        self.resource_url = uritemplate.expand(resource_url, **parameters)

    def get(self):
        return self.client.get(self.resource_url)

    def get_resource(self, resource_type, **parameters):
        data = self.get()
        return Resource(
            self.client, data['{}_url'.format(resource_type)], **parameters)


def get_kens_repos(access_token=None):
    if access_token is None:
        access_token = raw_input('What is your access token? ')
    cli = Client(access_token)
    ken = cli.get_resource('user', user='kennethreitz')
    for repo in ken.get_resource('repos').get():
        print repo['name'], repo['watchers_count']
    return repo


def get_requests_commits(access_token=None):
    if access_token is None:
        access_token = raw_input('What is your access token? ')
    cli = Client(access_token)
    repo = cli.get_resource(
        'repository', owner='kennethreitz', repo='requests')
    for commit in repo.get_resource('commits').get():
        print commit['sha'], commit['commit']['message'].splitlines()[0]
