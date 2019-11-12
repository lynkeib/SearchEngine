# -*- coding: utf-8 -*-
from urllib import parse
import json
import re

import scrapy
from scrapy import *
import requests
from ..items import JobBoleArticleItem


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['news.cnblogs.com']
    start_urls = ['http://news.cnblogs.com/']

    def parse(self, response):
        '''
        1. download all the new urls from the response and pass the urls to the next parse method
        2. get the next page url
        '''

        post_nodes = response.xpath('//div[@class="news_block"]')[:1]

        for post_node in post_nodes:
            a = post_node
            image_url = post_node.xpath('div[@class="content"]/div[@class="entry_summary"]/a/img/@src').extract_first(
                "")
            post_url = post_node.xpath('div[@class="content"]/h2[@class="news_entry"]/a/@href').extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url),
                          meta={"front_image_url": image_url},
                          callback=self.parse_detail)  # self-defined callback method

            # Extract next page and pass to scrapy to download
            # next_url = response.xpath('//div[@class="pager"]/a[last()]/text()').extract_first("")
            # # next_url = response.xpath('//a[contains(test(), "Next >"")]/@href').extract_first("")
            # if next_url == "Next >":
            #     next_url_res = response.xpath('//div[@class="pager"]/a[last()]/@href').extract_first("")
            #     yield Request(url=parse.urljoin(response.url, next_url_res),
            #                   callback=self.parse)  # self-defined callback method
            # next_url = response.xpath('//div[@class="pager"]/a[last()]/text()').extract_first("")

            # next_url = response.xpath('//a[contains(text(), "Next >")]/@href').extract_first("")
            # yield Request(url=parse.urljoin(response.url, next_url),
            #               callback=self.parse)  # self-defined callback method

    def parse_detail(self, response):

        match_re = re.match(".*?(\d+)", response.url)
        if match_re:
            article_item = JobBoleArticleItem()

            title = response.xpath('//div[@id="news_title"]/a/text()').extract_first("")

            create_date = response.xpath('//div[@id="news_info"]//span[@class="time"]/text()').extract_first("")
            content = response.xpath('//div[@id="news_content"]').extract()[0]
            tag_list = response.xpath('//div[@class="news_tags"]/a/text()').extract()
            tags = ",".join(tag_list)

            post_id = match_re.group(1)

            article_item['title'] = title
            article_item['create_date'] = create_date
            article_item['content'] = content
            article_item['tags'] = tags
            article_item['front_image_url'] = response.meta.get('front_image_url', '')
            # html = requests.get(parse.urljoin(response.url, f"/NewsAjax/GetAjaxNewsInfo?contentId={post_id}"))
            # j_data = json.loads(html.text)
            nums_url = parse.urljoin(response.url, f"/NewsAjax/GetAjaxNewsInfo?contentId={post_id}")
            yield Request(url=parse.urljoin(response.url, nums_url),
                          meta={'article_item': article_item},
                          callback=self.parse_nums)

            # praise_nums = j_data['DiggCount']
            # fav_nums = j_data['TotalViews']
            # comment_nums = j_data['CommentCount']

            pass

    def parse_nums(self, response):

        article_item = response.meta.get('article_item')

        j_data = json.loads(response.text)
        praise_nums = j_data['DiggCount']
        fav_nums = j_data['TotalViews']
        comment_nums = j_data['CommentCount']

        article_item['praise_nums'] = praise_nums
        article_item['fav_nums'] = fav_nums
        article_item['comment_nums'] = comment_nums



        pass
