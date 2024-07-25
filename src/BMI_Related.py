import pymongo
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.io as pio
import plotly
import plotly.offline as offline
from subprocess import call
import json


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

def BMI_Insert(year):
    mongo = get_mongo_collection(year)

    for data in mongo.find():

        try:
            height = float(data['Height']) / 100
            weight = float(data['Weight'])

            bmi = round(weight / (height * height), 4)

            bmi_state_en = str()
            bmi_state_ch = str()

            if bmi < 15:
                bmi_state_en = 'Very severely underweight'
                bmi_state_ch = '非常严重的体重不足'

            if bmi >= 15 and bmi < 16:
                bmi_state_en = 'Severely underweight'
                bmi_state_ch = '严重体重不足'

            if bmi >= 16 and bmi < 18.5:
                bmi_state_en = 'Underweight'
                bmi_state_ch = '体重过轻'

            if bmi >= 18.5 and bmi < 25:
                bmi_state_en = 'Normal (healthy weight)'
                bmi_state_ch = '体重正常 (健康体重)'

            if bmi >= 25 and bmi < 30:
                bmi_state_en = 'Overweight'
                bmi_state_ch = '体重过重'

            if bmi >= 30 and bmi < 35:
                bmi_state_en = 'Obese Class I (Moderately obese)'
                bmi_state_ch = '肥胖I级（中等肥胖)'

            if bmi >= 35 and bmi < 40:
                bmi_state_en = 'Obese Class II (Severely obese)'
                bmi_state_ch = '肥胖II级（严重肥胖)'

            if bmi >= 40 and bmi < 45:
                bmi_state_en = 'Obese Class III (Very severely obese)'
                bmi_state_ch = '肥胖III级（非常严重肥胖）'

            if bmi >= 45 and bmi < 50:
                bmi_state_en = 'Obese Class IV (Morbidly Obese)'
                bmi_state_ch = '肥胖IV级（病态肥胖）'

            if bmi >= 50 and bmi < 60:
                bmi_state_en = 'Obese Class V (Super Obese)'
                bmi_state_ch = '肥胖V级（超级肥胖）'

            if bmi >= 60:
                bmi_state_en = 'Obese Class VI (Hyper Obese)'
                bmi_state_ch = '肥胖VI级（究极肥胖）'

            print(bmi_state_en, bmi_state_ch)

            mongo.update_one(
                {'_id': data['_id']},
                {'$set': {'BMI': bmi, 'BMI_en': bmi_state_en, 'BMI_ch': bmi_state_ch}}
            )

            print('Progress: {:.2%}'.format(mongo.count({'BMI_en': {'$exists': True}}) / mongo.count()))

        except:
            print(data['_id'])
            mongo.delete_one({'_id': data['_id']})



def BMI_Year_Analysis(year, both_angle, male_angle, female_angle):
    mongo = get_mongo_collection(year)

    _bmi_ch_list = ['非常严重的体重不足', '严重体重不足', '体重过轻', '体重正常 (健康体重)', '体重过重', '肥胖I级（中等肥胖)',
                   '肥胖II级（严重肥胖)', '肥胖III级（非常严重肥胖）', '肥胖IV级（病态肥胖）', '肥胖V级（超级肥胖）', '肥胖VI级（究极肥胖）']

    bmi_ch_list = ['非常严重的体重不足', '严重体重不足', '体重过轻', '体重正常 (健康体重)', '体重过重', '肥胖I级（中等肥胖)',
                    '肥胖II级（严重肥胖)']

    colors = ['#8B7355', '#CDAA7D', '#FF7F24', '#228B22', '#FF6A6A', '#8B3A3A', '#8B2323']

    bmi_whole_num = list()
    bmi_male_num = list()


    bmi_female_num = list()

    for i in range(len(bmi_ch_list)):
        bmi_state = bmi_ch_list[i]

        whole_num = mongo.count({'BMI_ch': bmi_state})
        male_num = mongo.count({'$and': [{'BMI_ch': bmi_state}, {'Sex': "男"}]})
        female_num = mongo.count({'$and': [{'BMI_ch': bmi_state}, {'Sex': "女"}]})

        bmi_whole_num.append(whole_num)
        bmi_male_num.append(male_num)
        bmi_female_num.append(female_num)

    fig = {
        "data": [
            {
                'values': bmi_whole_num,
                "domain": {
                    'x': [.23, .77],
                    'y': [0, .47]
                },

                'labels': bmi_ch_list,
                'name': '总体BMI',
                'hoverinfo': 'label+percent+name+value',
                'textinfo': 'label+percent+value',
                'textfont': {
                    'size': 13,
                },
                'rotation': both_angle,
                'hole': .3,
                'marker': {'colors': colors, 'line': {'color': '#000000', 'width': 2}},
                'type': 'pie'
            },
            {
                'values': bmi_male_num,
                "domain": {
                    "x": [.52, 1],
                    'y': [.53, 1]
                },
                'rotation': male_angle,
                'labels': bmi_ch_list,
                'name': '男性BMI',
                'hoverinfo': 'label+percent+name+value',
                'textinfo': 'label+percent+value',
                'textfont': {
                    'size': 13,
                },
                'hole': .3,
                'marker': {'colors': colors, 'line': {'color': '#000000', 'width': 2}},
                'type': 'pie'
            },
            {
                'values': bmi_female_num,
                "domain": {
                    "x": [0, .48],
                    'y': [.53, 1]
                },
                'labels': bmi_ch_list,
                'rotation': female_angle,
                'name': '女性BMI',
                'hoverinfo': 'label+percent+name+value',
                'textinfo': 'label+percent+value',
                'textfont': {
                    'size': 13,
                },
                'hole': .3,
                'marker': {'colors': colors, 'line': {'color': '#000000', 'width': 2}},
                'type': 'pie'
            },

        ],
        'layout': {
            'title': 'BMI ' + str(20) + str(year) + '年男女对比',
            "annotations": [
                {
                    "font": {
                        "size": 20
                    },
                    "showarrow": False,
                    "text": "总体",
                    "x": 0.5,
                    "y": 0.215
                },
                {
                    "font": {
                        "size": 20
                    },
                    "showarrow": False,
                    "text": "男性",
                    "x": 0.788,
                    "y": 0.775
                },
                {
                    "font": {
                        "size": 20
                    },
                    "showarrow": False,
                    "text": "女性",
                    "x": 0.212,
                    "y": 0.775
                }
            ]
        }
    }

    py.iplot(fig, filename='BMI ' + str(20) + str(year))

    '''
    offline.plot(fig, auto_open=False, image='png', image_filename='image_file_name',
                 output_type='file', image_width=800, image_height=600, validate=False,
                 filename='BMI ' + str(20) + str(year))
    '''
    # pio.write_image(fig, file='BMI ' + str(20) + str(year) + '.png')
    # print(json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder))
    # call(['orca', 'graph', json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder), '-o', 'out.png'])

def BMI_Whole_Analysis():
    mongo13 = get_mongo_collection(13)
    mongo14 = get_mongo_collection(14)
    mongo15 = get_mongo_collection(15)
    mongo16 = get_mongo_collection(16)

    colors = ['#F5DEB3', '#CD5C5C', '#7FFF00']

    fig = {
        "data": [
            {
                'values': [
                    mongo13.count({'BMI': {'$lte': 18.5}}),
                    mongo13.count({'BMI': {'$gte': 25}}),
                    mongo13.count({'$and': [{'BMI': {'$lt': 25}}, {'BMI': {'$gt': 18.5}}]})
                ],
                "domain": {
                    'x': [0, .48],
                    'y': [0, .49]
                },

                'labels': ['体重过轻', '体重超重', '体重正常'],
                'name': '2013年BMI',
                'hoverinfo': 'label+percent+name',
                'textinfo': 'label+percent',
                'textfont': {
                    'size': 13,
                },
                'hole': .3,
                'marker': {'colors': colors, 'line': {'color': '#000000', 'width': 2}},
                'type': 'pie'
            },
            {
                'values': [
                    mongo14.count({'BMI': {'$lte': 18.5}}),
                    mongo14.count({'BMI': {'$gte': 25}}),
                    mongo14.count({'$and': [{'BMI': {'$lt': 25}}, {'BMI': {'$gt': 18.5}}]})
                ],
                "domain": {
                    "x": [.52, 1],
                    'y': [0, .49]
                },
                'labels': ['体重过轻', '体重超重', '体重正常'],
                'name': '2014年BMI',
                'hoverinfo': 'label+percent+name',
                'textinfo': 'label+percent',
                'textfont': {
                    'size': 13,
                },
                'hole': .3,
                'marker': {'colors': colors, 'line': {'color': '#000000', 'width': 2}},
                'type': 'pie'
            },
            {
                'values': [
                    mongo15.count({'BMI': {'$lte': 18.5}}),
                    mongo15.count({'BMI': {'$gte': 25}}),
                    mongo15.count({'$and': [{'BMI': {'$lt': 25}}, {'BMI': {'$gt': 18.5}}]})
                ],
                "domain": {
                    "x": [0, .48],
                    'y': [.51, 1]
                },
                'labels': ['体重过轻', '体重超重', '体重正常'],
                'name': '2015年BMI',
                'hoverinfo': 'label+percent+name+value',
                'textinfo': 'label+percent',
                'textfont': {
                    'size': 13,
                },
                'hole': .3,
                'marker': {'colors': colors, 'line': {'color': '#000000', 'width': 2}},
                'type': 'pie'
            },
            {
                'values': [
                    mongo16.count({'BMI': {'$lte': 18.5}}),
                    mongo16.count({'BMI': {'$gte': 25}}),
                    mongo16.count({'$and': [{'BMI': {'$lt': 25}}, {'BMI': {'$gt': 18.5}}]})
                ],
                "domain": {
                    "x": [.52, 1],
                    'y': [.51, 1]
                },
                'labels': ['体重过轻', '体重超重', '体重正常'],
                'name': '2016BMI',
                'hoverinfo': 'label+percent+name+value',
                'textinfo': 'label+percent',
                'textfont': {
                    'size': 13,
                },
                'hole': .3,
                'marker': {'colors': colors, 'line': {'color': '#000000', 'width': 2}},
                'type': 'pie'
            }

        ],
        "layout": {
            'hoverlabel': {
                'font': {'size': 14}
            },
            "title": "BMI",
            'legend': {'font': {'size': 14}},
            "annotations": [
                {
                    "font": {
                        "size": 20
                    },
                    "showarrow": False,
                    "text": "2013",
                    "x": 0.215,
                    "y": 0.22
                },
                {
                    "font": {
                        "size": 20
                    },
                    "showarrow": False,
                    "text": "2014",
                    "x": 0.785,
                    "y": 0.22
                },
                {
                    "font": {
                        "size": 20
                    },
                    "showarrow": False,
                    "text": "2015",
                    "x": 0.215,
                    "y": 0.78
                },
                {
                    "font": {
                        "size": 20
                    },
                    "showarrow": False,
                    "text": "2016",
                    "x": 0.785,
                    "y": 0.78
                }
            ]
        }
    }

    py.iplot(fig, filename='BMI总体分析.png')


if __name__ == '__main__':
    # BMI_Year_Analysis(13, -238, -195, -120)
    # BMI_Year_Analysis(14, -198, -171, -90)
    # BMI_Year_Analysis(15, -174, -150, -90)
    BMI_Year_Analysis(16, -174, -150, -90)