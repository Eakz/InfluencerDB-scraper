import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint


class InstagramScraper(object):

    def __init__(self, **kwargs):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                          'AppleWebKit/537.11 (KHTML, like Gecko) '
                          'Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }

    def __request_url(self, link):
        try:
            response = requests.get(
                link,
                timeout=4,
                headers=self.headers,
            ).text
        except requests.HTTPError:
            raise requests.HTTPError(
                'Received non 200 status code from Instagram')
        except requests.RequestException:
            raise requests.RequestException
        else:
            return response

    @staticmethod
    def extract_json_data(html):
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find('body')
        script_tag = body.find('script')
        raw_string = script_tag.text.strip().replace(
            'window._sharedData =', '').replace(';', '')
        return json.loads(raw_string)

    def profile_page_metrics(self, link):
        # nice function but not needed for now
        results = {}
        try:
            response = self.__request_url(link)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']
        except Exception as e:
            raise e
        else:
            for key, value in metrics.items():
                if key != 'edge_owner_to_timeline_media':
                    if value and isinstance(value, dict):
                        value = value['count']
                        results[key] = value
                    elif value:
                        results[key] = value
        return results

    def profile_page_recent_posts(self, link):
        results = []
        try:
            response = self.__request_url(link)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media'][
                "edges"]
        except Exception as e:
            raise e
        else:
            for node in metrics:
                node = node.get('node')
                if node and isinstance(node, dict):
                    results.append(node)
        return results

    def discover_posts(self, hashtag):
        # get id to posts. Then we can get posts and their accounts.
        results = []
        try:
            response = self.__request_url(f"https://www.instagram.com/explore/tags/{hashtag}/")
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_top_posts'][
                "edges"]
        except Exception as e:
            raise e
        else:
            for node in metrics:
                node = node.get('node')
                if node and isinstance(node, dict):
                    results.append(node['shortcode'])
        return results

    def get_account_name_from_post(self, post_id):
        response = self.__request_url(f"https://www.instagram.com/p/{post_id}/")
        json_data = self.extract_json_data(response)
        import pdb
        pdb.set_trace()
        # metrics = json_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_top_posts'][
        #     "edges"]

x = InstagramScraper()
m1 = x.discover_posts('codingmemes')
print(m1)
# m1 = x.profile_page_metrics('https://www.instagram.com/jakobowsky/')
# m2 = x.profile_page_metrics('https://www.instagram.com/codingdays/')
