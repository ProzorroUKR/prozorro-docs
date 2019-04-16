import json

from openprocurement.api.constants import VERSION
from webtest import TestApp, TestRequest

API_HOST = 'lb-api-sandbox.prozorro.gov.ua'
DOCS_HOST = 'public-docs-sandbox.prozorro.gov.ua'
AUCTIONS_HOST = 'auction-sandbox.prozorro.gov.ua'


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
