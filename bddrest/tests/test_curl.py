from bddrest import FirstCall, Call
from bddrest.documentary.curl import CURL

def test_curl():
    curl = CURL(
        url='example.com',
        query=dict(c=1, d=2),
        verb='POST',
        form=dict(a=1, b=2),
        headers=['A: B', 'C: D'],
        content_type='text/plain',
        authorization='TOKEN'
    )
    import pudb; pudb.set_trace()  # XXX BREAKPOINT
    print(curl)

#def test_curl_from_call():
#    call = FirstCall(
#        'Testing Call to_curl',
#        url='/id: 1',
#        query=dict(c=1, d=2),
#        verb='POST',
#        form=dict(a=1, b=2),
#        headers=['A: B', 'C: D'],
#        content_type='text/plain',
#        authorization='TOKEN'
#    )
#    curl = CURL.from_call(call)

