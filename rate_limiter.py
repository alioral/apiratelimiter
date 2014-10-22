import unittest

from redis import Redis
from time import time, sleep

TIME_LIMIT = 0.5 # In minutes
RATE_LIMIT = 5000

def is_in_rate_limits(token, redis_server):
    current_request_time = time()
    request_list_size = redis_server.llen(token)

    """
    If the user doesn't exist in redis, it means
    user hasn't made any requests, thus insert him
    and initiate with a list including the request.

    If there are a room for another request, simply
    add the request timestamp without checking any further
    information"""
    if request_list_size < RATE_LIMIT:
        redis_server.rpush(token, time())
        return True

    earliest_request_time = float(redis_server.lindex(token, 0))
    time_difference = (current_request_time - earliest_request_time) / 60

    """ Regardless whether the user was able to make the
    request in order to make sure the is window 'sliding'
    add the most recent request to the list and remove the
    earliest one from the beginning"""

    redis_server.lpop(token)
    redis_server.rpush(token, current_request_time)

    if time_difference >= TIME_LIMIT:
        return True
    return False

class TestRateLimitation(unittest.TestCase):

    def setUp(self):
        self.redis_server = Redis('localhost')
        self.token = 'nWg12cbK3i9EypGHLTNx'

    """ Creating the first request """
    def test_1(self):
        self.assertTrue(is_in_rate_limits(self.token,
                                                 self.redis_server))
    """ After creating the first request, fill up the
    list with requests in order to make sure that the
    user will encounter a rate limitation."""

    def test_2(self):
        for request_count in xrange(RATE_LIMIT - 1):
            self.assertTrue(is_in_rate_limits(self.token,
                                              self.redis_server))

        self.assertFalse(is_in_rate_limits(self.token,
                                           self.redis_server))

    def test_3(self):
        self.assertFalse(is_in_rate_limits(self.token,
                                           self.redis_server))
    """ Optional test just to make sure the window is sliding so after
    first request made if there is an opening in the window, allow request"""
    def test_4(self):
        sleep(60)
        self.assertFalse(is_in_rate_limits(self.token,
                                           self.redis_server))

if __name__ == '__main__':
    unittest.main()
