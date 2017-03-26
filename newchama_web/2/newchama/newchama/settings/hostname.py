# -*- coding: utf-8 -*-

def _get_hostname_shell():
    try:
        import subprocess
        bulk = subprocess.Popen(['hostname'], stdout=subprocess.PIPE).communicate()[0].strip()
        return bulk.strip().lower()
    except:
        return ''

if not 'HOSTNAME' in vars():
    HOSTNAME = _get_hostname_shell()
