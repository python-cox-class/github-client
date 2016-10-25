import requests
import uritemplate


class Client(object):
    root = 'https://api.github.com'

    def __init__(self, access_token):
        self.sess = requests.Session()
        # Set the Authorization header in the session
        # YOUR CODE HERE
        self.resources = self.get(root)

    def get(self, url):
        """HTTP GET a resource and return its decoded JSON representation.

        This function should GET the given URL, raise an exception on any
        4xx or 5xx errors, and return the decoded JSON representation of
        the response.
        """
        # YOUR CODE HERE

    def get_resource(self, resource_type, **parameters):
        return Resource(
            self, self.resources['{}_url'.format(resource_type)], **parameters)


class Resource(object):

    def __init__(self, client, resource_url, **parameters):
        self.client = client
        self.resource_url = uritemplate.expand(resource_url, **parameters)

    def get(self):
        return self.client.get(self.resource_url)
