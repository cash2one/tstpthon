import webbrowser as web
import time
import os
import random

data=raw_input('Enter url:')
count=random.randint(3,5)

j=0
while j<count:
	i=0
	while i<=3:
		web.open_new_tab(data)
		i=j+1
		time.sleep(1)
	else:
		os.system('taskkill /F /IM chrome.exe')
		print j,'times closing Browser'
	j=j+1
