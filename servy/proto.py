import json

class Response(object):
    @classmethod
    def encode(cls, content):
        return json.dumps(content)

    @classmethod
    def decode(cls, content):
        return json.loads(content)


class Request(object):
    @classmethod
    def encode(cls, proc, args, kw):
        return json.dumps({
            'proc': proc,
            'args': args,
            'kw': kw,
        })

    @classmethod
    def decode(cls, content):
        content = json.loads(content)
        return (
            content['proc'],
            content['args'],
            content['kw'],
        )
