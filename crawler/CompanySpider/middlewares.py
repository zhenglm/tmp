import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.conf import settings


class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua = random.choice(settings.get('USER_AGENT_LIST'))
        if ua:
            # print ua
            request.headers.setdefault('User-Agent', ua)