# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re
class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancies2808

    def process_item(self, item, spider):
        item['site'] = spider.allowed_domains[0]
        if spider.name == 'hhru':
            item['salary_min'], item['salary_max'], item['salary_cur'] = self.process_salary(item['salary'])
        elif spider.name == 'superjobru':
            item['salary_min'], item['salary_max'], item['salary_cur'] = self.process_superjobru_salary(item['salary'])
        del item['salary']
        collection = self.mongobase[spider.name]
        collection.insert_one(item)

        return item

    def process_superjobru_salary(self, salary):
        salary = [i.replace('\xa0', '') for i in salary]
        if '—' in salary:
            salary_min = float(salary[0])
            salary_max = float(salary[4])
            salary_cur = salary[6]
        elif salary[0] == 'от':
            salary_min = float(''.join([x for x in salary[2] if x.isdigit()]))
            salary_max = None
            salary_cur = float(''.join(re.findall('\D', str(salary[2]))))
        elif salary[0] == 'до':
            salary_max = float(''.join([x for x in salary[2] if x.isdigit()]))
            salary_min = None
            salary_cur = float(''.join(re.findall('\D', str(salary[2]))))
        else:
            salary_min = None
            salary_max = None
            salary_cur = None


        return salary_min, salary_max, salary_cur

    def process_salary(self, salary):
        salary = salary.replace('\xa0', '').split()
        if len(salary) == 5:
            salary_min = float(salary[1])
            salary_max = float(salary[3])
            salary_cur = salary[-1]
        elif salary[0] == 'от':
            salary_min = float(salary[1])
            salary_max = None
            salary_cur = salary[-1]
        elif salary[0] == 'до':
            salary_min = None
            salary_max = float(salary[1])
            salary_cur = salary[-1]
        else:
            salary_min = None
            salary_max = None
            salary_cur = None

        return salary_min, salary_max, salary_cur
