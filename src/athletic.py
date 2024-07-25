import pyexcel as p
from pyexcel_xls import get_data
import json
import pymongo
import plotly.plotly as py
import plotly.graph_objs as go

def get_mongo_collection(year_num):
    client = pymongo.MongoClient()
    if year_num == 13:
        return client.athletes.dataset2013
    if year_num == 14:
        return client.athletes.dataset2014
    if year_num == 15:
        return client.athletes.dataset2015
    if year_num == 16:
        return client.athletes.dataset2016

def to_mongo(year):
    mongo = get_mongo_collection(year)
    filepath = './datasets/data20' + str(year) + '10cleaned.xls'
    if year == 16:
        filepath = './datasets/data20' + str(year) + '10cleaned.xlsx'

    column_names = {
        '13': ['Num', 'ClassNum', 'Sex', 'Nation', 'College', 'Department', 'Major', 'Grade', 'Rxrq', 'Address',
               'Height', 'Weight', 'Kmrun', 'Pulmonary', 'Jump', 'Run', 'Arm', 'Chin', 'LeftEye', 'RightEye'],

        '14': ["GradeNum", "Major", "SchoolNum", "ClassNum", "Class", "Num", "NationNum", "Sex", "AddressNum",
                "Address", "Cancelled", "CancelledReason", "Height", "Weight", "Pulmonery", "Eighty", "Thousand",
                "Run", "Jump", "SitAndReach", "Situp", "Pullup"],

        '15': ['GradeNum', 'ClassNum', 'Num', 'Sex', 'Height', 'Weight', 'BMI', 'Pulmonery', 'Run', 'Jump',
               'SitAndReach', 'Eighty', 'Thousand', 'Situp', 'Pullup'],

        '16': ['SchoolNum', 'GradeNum', 'ClassNum', 'Class', 'CardNum', 'Num', 'NationNum', 'Sex', 'AddressNum',
               'Address', 'Cancelled', 'CancelledReason', 'Height', 'Weight', 'SitAndReach', 'Situp',
               'Pulmonary', 'Run', 'Jump', 'Pullup', 'Eighty', 'Thousand']
    }

    '''
    data = get_data(filepath)
    json_str = json.dumps(data, ensure_ascii=False)
    data_dict = json.loads(json_str, encoding='utf-8')
    '''
    records = p.iget_records(file_name=filepath)

    total_num = {
        '13': 10825,
        '14': 3474,
        '15': 15410,
        '16': 15414
    }

    for record in records:
        num = record['Num']
        if mongo.count({'Num': num}) == 0:
            traits = dict()
            for column in column_names[str(year)]:
                traits[column] = record[column]
            mongo.insert_one(traits)
        print('Progress: {:.2%}'.format(mongo.count() / total_num[str(year)]))
