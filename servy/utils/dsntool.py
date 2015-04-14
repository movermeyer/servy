import collections
import re
import urlparse


class DSN(collections.MutableMapping):
    ''' Hold the results of a parsed dsn.
    This is very similar to urlparse.ParseResult tuple.

    http://docs.python.org/2/library/urlparse.html#results-of-urlparse-and-urlsplit

    It exposes the following attributes:

        scheme
        schemes -- if your scheme has +'s in it, then this will contain a list of schemes split by +
        path
        paths -- the path segment split by /, so "/foo/bar" would be ["foo", "bar"]
        host -- same as hostname (I just like host better)
        hostname
        hostloc -- host:port
        username
        password
        netloc
        query -- a dict of the query string
        query_str -- the raw query string
        port
        fragment
    '''
    DSN_REGEXP = re.compile(r'^\S+://\S+')
    FIELDS = ('scheme', 'netloc', 'path', 'params', 'query', 'fragment')

    def __init__(self, dsn, **defaults):
        ''' Parse a dsn to parts similar to urlparse.
        This is a nuts function that can serve as a good basis to parsing a custom dsn

        :param dsn: the dsn to parse
        :type dsn: str
        :param defaults: any values you want to have defaults for if they aren't in the dsn
        :type defaults: dict
        '''

        assert self.DSN_REGEXP.match(dsn), \
            "{} is invalid, only full dsn urls (scheme://host...) allowed".format(dsn)

        first_colon = dsn.find(':')
        scheme = dsn[0:first_colon]
        dsn_url = dsn[first_colon+1:]
        url = urlparse.urlparse(dsn_url)

        options = {}
        if url.query:
            for k, kv in urlparse.parse_qs(url.query, True, True).iteritems():
                if len(kv) > 1:
                    options[k] = kv
                else:
                    options[k] = kv[0]

        self.scheme = scheme
        self.hostname = url.hostname
        self.path = url.path
        self.params = url.params
        self.query = options
        self.fragment = url.fragment
        self.username = url.username
        self.password = url.password
        self.port = url.port
        self.query_str = url.query

        for k, v in defaults.iteritems():
            self.set_default(k, v)

    def __iter__(self):
        for f in self.FIELDS:
            yield getattr(self, f, '')

    def __len__(self):
        return len(iter(self))

    def __getitem__(self, field):
        return getattr(self, field, None)

    def __setitem__(self, field, value):
        setattr(self, field, value)

    def __delitem__(self, field):
        delattr(self, field)

    @property
    def schemes(self):
        '''the scheme, split by plus signs'''
        return self.scheme.split('+')

    @property
    def netloc(self):
        '''return username:password@hostname:port'''
        s = ''
        prefix = ''
        if self.username:
            s += self.username
            prefix = '@'

        if self.password:
            s += ":{}".format(self.password)
            prefix = '@'

        s += "{}{}".format(prefix, self.hostloc)
        return s

    @property
    def paths(self):
        '''the path attribute split by /'''
        return filter(None, self.path.split('/'))

    @property
    def host(self):
        '''the hostname, but I like host better'''
        return self.hostname

    @property
    def hostloc(self):
        '''return host:port'''
        hostloc = self.hostname
        if self.port:
            hostloc = '{}:{}'.format(hostloc, self.port)

        return hostloc

    def set_default(self, key, value):
        ''' Set a default value for key.

        This is different than dict's setdefault because it will set default either
        if the key doesn't exist, or if the value at the key evaluates to False, so
        an empty string or a None will value will be updated.

        :param key: the item to update
        :type key: str
        :param value: the items new value if key has a current value that evaluates to False
        '''
        if not getattr(self, key, None):
            setattr(self, key, value)

    def get_url(self):
        '''return the dsn back into url form'''
        return urlparse.urlunparse((
            self.scheme,
            self.netloc,
            self.path,
            self.params,
            self.query_str,
            self.fragment,
        ))

    def copy(self):
        return DSN(self.get_url())

    def __str__(self):
        return self.get_url()
