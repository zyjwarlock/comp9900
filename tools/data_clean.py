# created by z5089986 

import re
from nltk.corpus import stopwords

stoplist = stopwords.words('english')
pattern = re.compile(r'^\W+$', re.I)
pattern = re.compile(r'^\d+', re.I)

punct = set(u''':!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒﹔﹕﹖﹗﹚﹜﹞！），．＊：；Ｏ？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻︽︿﹁﹃﹙﹛﹝（｛“‘-—_…０１２３４５６７８９''')
filterpunt = lambda s: ''.join(filter(lambda x: x not in punct, s))
filterlist = lambda l: list(filter(lambda x: x not in punct, l))
stopword = lambda l: list(filter(lambda x: x.isalpha() and len(x) > 1 and x not in stoplist, l))
filterpy = lambda l: list(filter(lambda x: str(x).lower() != "python", l))



