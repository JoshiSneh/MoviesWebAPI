from models import RequestCount
from models import db


'''Middleware for counting all the requests'''
def request_count():
    '''
       This is a middleware which will get activate before every request and will increment the count of the request
       made by the server till now
    '''
    request_count = RequestCount.query.first()
    if not request_count:
        request_count = RequestCount(count=0)
        db.session.add(request_count)
    print(request_count.count)
    request_count.count += 1

    db.session.commit()