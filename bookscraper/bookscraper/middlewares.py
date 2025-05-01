# bookscraper/middlewares.py

import random
import requests
from scrapy import signals
from urllib.parse import urlencode


class ScrapeOpsFakeUserAgentMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = settings.get(
            'SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT',
            'https://headers.scrapeops.io/v1/browser-headers'
        )
        self.scrapeops_fake_user_agents_active = settings.getbool(
            'SCRAPEOPS_FAKE_USER_AGENT_ENABLED', False)
        self.scrapeops_num_results = settings.getint('SCRAPEOPS_NUM_RESULTS', 10)
        self.user_agent_list = []

        if self.scrapeops_fake_user_agents_active and self.scrapeops_api_key:
            self._get_user_agents_list()

    def _get_user_agents_list(self):
        payload = {
            'api_key': self.scrapeops_api_key,
            'num_results': self.scrapeops_num_results
        }
        try:
            response = requests.get(self.scrapeops_endpoint, params=payload)
            json_response = response.json()
            self.user_agent_list = json_response.get('result', [])
        except Exception as e:
            print(f"Error fetching user agents: {e}")

    def _get_random_user_agent(self):
        if self.user_agent_list:
            return random.choice(self.user_agent_list)
        return None

    def process_request(self, request, spider):
        user_agent = self._get_random_user_agent()
        if user_agent:
            request.headers['User-Agent'] = user_agent
            print('***********NEW HEADER ATTACHED*************')
            print(user_agent)