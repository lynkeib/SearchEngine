# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from scrapy.exceptions import DropItem
import codecs
import json
from scrapy.exporters import JsonItemExporter
import MySQLdb
import re
from twisted.enterprise import adbapi
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class JsonWithEncodingPipeline(object):
    # self-define json file export

    def __init__(self):
        self.file = codecs.open('article.json', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


class JsonExporterPipeline(object):
    def __init__(self):
        self.file = open("articleexport.json", 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect("127.0.0.1", 'root', '123456', 'article_spider', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into jobbole_article(title, url, url_object_id, front_image_url, front_image_path, parise_nums, comment_nums, fav_nums, tags, content, create_date)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = list()
        params.append(item.get('title', ""))
        params.append(item.get('url', ""))
        params.append(item.get('url_object_id', ""))
        front_image = ",".join(item.get('front_image_url', []))
        params.append(front_image)
        params.append(item.get('front_image_path', ""))
        params.append(item.get('parise_nums', 0))
        params.append(item.get('comment_nums', 0))
        params.append(item.get('fav_nums', 0))
        params.append(item.get('tags', ""))
        params.append(item.get('content', ""))
        # datetime = re.findall('.*?(\d{4}-\d{2}-\d{2}\s\d{1,2}:\d{1,2}).*', item.get('create_date', "1900-01-01"))[0]
        # params.append(datetime)
        params.append(item.get('create_date', "1900-01-01"))
        self.cursor.execute(insert_sql, tuple(params))
        self.conn.commit()
        return item


class MysqlTwistedPipeline(object):
    @classmethod
    def from_settings(cls, settings):
        from MySQLdb.cursors import DictCursor
        dbparms = {
            "host": settings['MYSQL_HOST'],
            "db": settings['MYSQL_DBNAME'],
            'user': settings['MYSQL_USER'],
            'passwd': settings['MYSQL_PASSWORD'],
            'charset': "utf8",
            'cursorclass': DictCursor,
            'use_unicode': True
        }

        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def __init__(self, dbpool):
        self.dbpool = dbpool

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        # failure will be passed automatically
        print(failure)

    def do_insert(self, cursor, item):
        # cursor will be passed automatically
        # Primary duplicate handle
        insert_sql = """
                    INSERT INTO jobbole_article(title, url, url_object_id, front_image_url, front_image_path, parise_nums, comment_nums, fav_nums, tags, content, create_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE parise_nums = VALUES(parise_nums)
                """
        params = list()
        params.append(item.get('title', ""))
        params.append(item.get('url', ""))
        params.append(item.get('url_object_id', ""))
        front_image = ",".join(item.get('front_image_url', []))
        params.append(front_image)
        params.append(item.get('front_image_path', ""))
        params.append(item.get('parise_nums', 0))
        params.append(item.get('comment_nums', 0))
        params.append(item.get('fav_nums', 0))
        params.append(item.get('tags', ""))
        params.append(item.get('content', ""))
        datetime = re.findall('.*?(\d{4}-\d{2}-\d{2}\s\d{1,2}:\d{1,2}).*', item.get('create_date', "1900-01-01"))[0]
        params.append(datetime)
        cursor.execute(insert_sql, tuple(params))
        return item


class ArticleImagePipeline(ImagesPipeline):
    # default_headers = {
    #     'accept': 'image/webp,image/*,*/*;q=0.8',
    #     'accept-encoding': 'gzip, deflate, sdch, br',
    #     'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
    #     'cookie': 'bid=yQdC/AzTaCw',
    #     # 'referer': 'https://www.douban.com/photos/photo/2370443040/',
    #     'referer': "https://news.cnblogs.com/",
    #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    # }

    default_headers = {'referer': "https://news.cnblogs.com/"}

    def get_media_requests(self, item, info):
        if 'front_image_url' in item:
            for image_url in item['front_image_url']:
                self.default_headers['referer'] = image_url
                yield Request(image_url, headers=self.default_headers)

    def item_completed(self, results, item, info):
        # image_file_paths = [x['path'] for ok, x in results if ok]
        # if not image_file_paths:
        #     raise DropItem("Item contains no images")
        # item['front_image_path'] = image_file_paths
        # return item
        if "front_image_url" in item:
            image_file_path = ""
            for ok, value in results:
                image_file_path = value['path']
            item["front_image_path"] = image_file_path
        return item
