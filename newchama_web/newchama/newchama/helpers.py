#FileName helpers.py
import re

class IgnoreCrsfMiddleware(object):
     def process_request(self, request, **karg):
         URL_LIST = [r'^/a/b/$', r'^/c/d/$']
         for u in URL_LIST:
             if re.match(u, request.path):
                 request.csrf_processing_done = True
                 return None

