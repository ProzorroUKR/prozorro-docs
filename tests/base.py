import json
import traceback
import mock

from uuid import UUID
from hashlib import md5
from webtest import TestApp, TestRequest
from openprocurement.api.constants import VERSION

from tests.constants import API_HOST


class PrefixedRequestClass(TestRequest):
    @classmethod
    def blank(cls, path, *args, **kwargs):
        path = '/api/%s%s' % (VERSION, path)
        return TestRequest.blank(path, *args, **kwargs)


class DumpsWebTestApp(TestApp):
    RequestClass = PrefixedRequestClass

    hostname = API_HOST
    indent = 2
    ensure_ascii = False
    encode = 'utf8'

    def do_request(self, req, status=None, expect_errors=None):
        req.headers.environ["HTTP_HOST"] = self.hostname
        self.write_request(req)
        resp = super(DumpsWebTestApp, self).do_request(req, status=status, expect_errors=expect_errors)
        self.write_response(resp)
        return resp

    def write_request(self, req):
        if hasattr(self, 'file_obj') and not self.file_obj.closed:
            self.file_obj.write(req.as_bytes(True))
            self.file_obj.write("\n")
            if req.body:
                try:
                    obj = json.loads(req.body)
                except ValueError:
                    pass
                else:
                    self.file_obj.write('DATA:\n' + json.dumps(
                        obj, indent=self.indent, ensure_ascii=self.ensure_ascii
                    ).encode(self.encode))
                    self.file_obj.write("\n")
            self.file_obj.write("\n")

    def write_response(self, resp):
        if hasattr(self, 'file_obj') and not self.file_obj.closed:
            headers = [
                (n.title(), v)
                for n, v in resp.headerlist
                if n.lower() != 'content-length'
            ]
            headers.sort()
            self.file_obj.write(str('Response: %s\n%s\n') % (
                resp.status,
                str('\n').join([str('%s: %s') % (n, v) for n, v in headers]),
            ))
            if resp.testbody:
                try:
                    obj = json.loads(resp.testbody)
                except ValueError:
                    pass
                else:
                    self.file_obj.write(json.dumps(
                        obj, indent=self.indent, ensure_ascii=self.ensure_ascii
                    ).encode(self.encode))
                    self.file_obj.write("\n")
            self.file_obj.write("\n")


class MockUUIDWebTestMixin(object):
    uuid_patch = None
    uuid_counters = None

    whitelist = ('/openprocurement/', '/tests/')
    blacklist = ('/tests/base.py',)

    def setUpMock(self):
        self.uuid_patch = mock.patch('uuid.UUID', side_effect=self.uuid)
        self.uuid_patch.start()

    def tearDownMock(self):
        self.uuid_patch.stop()

    def uuid(self, version=None, **kwargs):
        stack = self.stack()
        hex = md5(str(stack)).hexdigest()
        count = self.count(hex)
        hash = md5(hex + str(count)).digest()
        return UUID(bytes=hash[:16], version=version)

    def stack(self):
        stack = traceback.extract_stack()
        return [(item[0], item[2], item[3]) for item in stack if all([
            any([path in item[0] for path in self.whitelist]),
            all([path not in item[0] for path in self.blacklist])
        ])]

    def count(self, name):
        if self.uuid_counters is None:
            self.uuid_counters = dict()
        if name not in self.uuid_counters:
            self.uuid_counters[name] = 0
        else:
            self.uuid_counters[name] += 1
        return self.uuid_counters[name]
