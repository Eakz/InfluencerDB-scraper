from scrap import InstagramScraper
import requests
import time
from typing import Dict, List


class DiscoverBot:
    def __init__(self):
        self.base_url = 'http://127.0.0.1:8000/api/'
        self.scraper = InstagramScraper()

    def start_bot(self):
        pass

    def check_if_account_exists(self, username):
        print(f"Checking if {username} is in db.")
        link = f"{self.base_url}instagram_accounts?username={username}"
        response = requests.get(link).json()
        if response:
            print("Account exists.")
            return True
        return False

    def add_account_to_db(self, account: str, category: Dict):
        print(f"Adding {account} to db")
        profile_page_metrics, profile_page_recent_posts = self.scraper.get_current_profile_info(account)
        
        pass

    def update_db_with_users(self, accounts: List[str], category: Dict):
        for account in accounts:
            if not self.check_if_account_exists(account):
                self.add_account_to_db(account, category)

    def discover_new_accounts_through_hashtags(self, hashtags: List[str], category: Dict):
        for hashtag in hashtags:
            accounts = self.scraper.discover_accounts_from_hashtag(hashtag)
            self.update_db_with_users(accounts, category)
            time.sleep(3)

    def get_categories(self):
        link_to_categories = f"{self.base_url}categories"
        categories = requests.get(link_to_categories).json()
        if categories:
            for category in categories:
                print(category)
                hashtags = self.get_hashtags_from_category(category.get("id"))

    def get_hashtags_from_category(self, category_id):
        link_to_hashtags = f"{self.base_url}hashtags?category__id={category_id}"
        hashtags = requests.get(link_to_hashtags).json()
        return [hashtag['name'] for hashtag in hashtags]

# DiscoverBot().get_categories()
# print(DiscoverBot().check_if_account_exists('jakobowskya'))
