from twitter import Twitter
from twitter import OAuth

t = Twitter(auth=OAuth(
    '1539088022-I8k9xAUGjAfxGfgHQj69YMaTHZcLUsR2Nz9bvst',
    'n44jnA3XPrLV2eXmS8Xqn1SKDj2GDD9WJk432FySfPkt4',
    'jjMY07Ck9Zb41CyL8cWxAcwNl',
    '2ie5wUbzdTR2Y8hpBBeeoQLXc0UO8WFizhdgx9mYFaxyHqIxsG'
    ))
pythonTweets = t.search.tweets(q='#python')
# print(str(pythonTweets).encode('GBK', 'ignore'))

statusUpdate = t.statuses.update(status='Hello, world kkk!')
print(str(statusUpdate).encode('GBK', 'ignore'))