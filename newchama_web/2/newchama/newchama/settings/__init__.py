# -*- coding: utf-8 -*-

from newchama.settings.hostname import HOSTNAME
if HOSTNAME.startswith('tangyue'):
    from newchama.settings.tangyue import *
elif HOSTNAME.startswith('iz23r4wc9kzz'):
    from newchama.settings.test import *
elif HOSTNAME.startswith('iz232fht9xbz'):
    import os
    path = os.path.dirname(os.path.realpath(__file__))
    if 'stage' in path:
        from newchama.settings.stage import *
    elif 'pro' in path:
        from newchama.settings.pro import *
else:
    from newchama.settings.base import *
