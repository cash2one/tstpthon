from newchama.settings import LANGUAGE_COOKIE_NAME,CHINESE_STRING,ENGLISH_STRING


class LangChoiceMiddleware(object):
	def process_request(self,request):
		request.lang=get_template_lang(request)
		request.is_cn=is_cn(request)


def get_template_lang(request):
	lang = request.COOKIES.get(LANGUAGE_COOKIE_NAME,None)
	if lang ==None:
		lang_str=request.META.get('HTTP_ACCEPT_LANGUAGE',None)
		if lang_str:
			if(CHINESE_STRING in lang_str.lower()):
				lang=CHINESE_STRING
			else:
				lang=ENGLISH_STRING
		else:
			lang=ENGLISH_STRING
	else:
		if 	lang not in (CHINESE_STRING,ENGLISH_STRING):
			lang=ENGLISH_STRING
	return lang

def is_cn(request):
	if get_template_lang(request)==CHINESE_STRING:
		return True
	else:
		return False