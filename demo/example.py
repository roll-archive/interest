import sys
import asyncio
import logging
from aiohttp.web import Response, HTTPException, HTTPCreated, HTTPServerError
from interest import Service, Resource, Middleware, get, put


class Interface(Middleware):

    # Public

    @asyncio.coroutine
    def __call__(self, request):
        try:
            response = Response()
            payload = yield from self.next(request)
        except HTTPException as exception:
            response = exception
            payload = {'message': str(response)}
        except Exception as exception:
            response = HTTPServerError()
            payload = {'message': 'Something went wrong!'}
        response.text = self.service.formatter.encode(payload)
        response.content_type = self.service.formatter.content_type
        return response


class Comment(Resource):

    # Public

    @get('/{id}')
    def read(self, request):
        return {'id': request.match['id']}

    @put
    def upsert(self, request):
        raise HTTPCreated()


try:
    hostname = sys.argv[1]
except Exception:
    hostname = '127.0.0.1'
try:
    port = int(sys.argv[2])
except Exception:
    port = 9000

logging.basicConfig(level=logging.DEBUG)
service = Service(path='/api/v1')
service.add_middleware(Interface)
service.add_resource(Comment)
service.listen(hostname=hostname, port=port)
