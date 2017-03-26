#encoding:utf-8
import os,sys
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('/var/www/newchama'))
import newchama.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")

import csv
from recommond.models import MatchingWord

fname = "matchingword3.csv"
_is_update=False

word_list=[]
for row in csv.reader(open(fname,'rU'), delimiter=','):

    
    word1 = row[0].strip()
    word2= row[1].strip()
    rank1=int(row[2].strip())
    rank2=int(row[3].strip())
    
    word_list.append([word1,word2,rank1])
    word_list.append([word2,word1,rank2])



for item  in word_list:
    print item

    rec_num=MatchingWord.objects.filter(word1=item[0],word2=item[1]).count()
    
    if rec_num>0:
        if _is_update:
            _matchingword=MatchingWord.objects.filter(word1=item[0],word2=item[1]).first()
            _matchingword.rank=(item[2]+_matchingword.rank)/2
            _matchingword.save()
    else:
        _matchingword=MatchingWord()
        _matchingword.word1=item[0]
        _matchingword.word2=item[1]
        _matchingword.rank=item[2]
        _matchingword.save()

