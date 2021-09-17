import scrapy
import re
import json
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from copy import deepcopy
from Lesson_8.instaparser.items import InstaparserItem


class FollowSpider(scrapy.Spider):

    name = 'instaparser_follow'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = 'Onliskill_udm'
    insta_pass = '#PWD_INSTAGRAM_BROWSER:10:1631677250:AbhQAIIbpF11dsMD3yrAy4SvZPXAaP4iaOnWwi3cnx9iOPgXarq9wTPTVyzemU1HS0ME13FD3wZDIKHSyJ63D8cRZsT0ZtPdC70VrKt9vRitDx9ttBAbk+zMrwA5ZB5KbFv5yfrlHt5Lphg/OpMe'
    insta_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    users_parse = ['ezhatinkaliza', 'zhannidze']
    api_url = 'https://i.instagram.com/api/v1/'

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.insta_login_link,
                                 method='POST',
                                 callback=self.user_login,
                                 formdata={'username': self.insta_login,
                                           'enc_password': self.insta_pass},
                                 headers={'X-CSRFToken': csrf})

    def user_login(self, response: HtmlResponse):
        j_body = response.json()
        if j_body['authenticated']:
            for user in self.users_parse:
                yield response.follow(f'/{user}',
                                      callback=self.user_parse,
                                      cb_kwargs={'username': user})


    def user_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {
            'count': 12,
            'search_surface': 'follow_list_page'
                    }

        for user_status in ('following', 'followers'):
            url = f'https://i.instagram.com/api/v1/friendships/{user_id}/{user_status}/?{urlencode(variables)}'
            yield response.follow(url,
                                  callback=self.parse_follow,
                                  cb_kwargs={'user_id': user_id,
                                             'username': username,
                                             'variables': deepcopy(variables),
                                             'target': user_status})

    def parse_follow(self, response: HtmlResponse, username, user_id, variables, target):
        if response.status == 200:
            js_data = response.json()

            # print(j_data.get('next_max_id'), user_id, variables, target)
            if js_data.get('users'):
                variables['max_id'] = js_data.get('next_max_id')
                url = f'https://i.instagram.com/api/v1/friendships/{user_id}/{target}/?{urlencode(variables)}'
                yield response.follow(url,
                                      callback=self.parse_follow,
                                      cb_kwargs={'username': username,
                                                 'user_id': user_id,
                                                 'variables': deepcopy(variables),
                                                 'target': target})

            users = js_data.get('users')
            for user in users:
                item = InstaparserItem(
                                       id=user.get('pk'),
                                       name=user.get('full_name'),
                                       photo=user.get('profile_pic_url'),

                                       status=target,
                                       user_parse=username,
                                       all_data=user,

                                        )
                yield item

    # Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    # Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')