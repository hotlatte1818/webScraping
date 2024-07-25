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

def Kmrun_Preprocessed(year):
    mongo13 = get_mongo_collection(13)
    mongo14 = get_mongo_collection(14)
    mongo15 = get_mongo_collection(15)
    mongo16 = get_mongo_collection(16)

    if year == 13:
        for item in mongo13.find():
            data = int()
            kmrun = item['Kmrun']

            if kmrun == '4' or kmrun == '3' or kmrun == '2':
                data = 60 * int(kmrun)
            else:
                try:
                    split = kmrun.split('\'')
                    data = int(split[0]) * 60 + int(split[1])
                    print(data)
                except:
                    print(kmrun)
            mongo13.update_one(
                {'_id': item['_id']},
                {'$set': {'LongRun': data}}
            )

    elif year == 14:
        for item in mongo14.find():
            sex = item['Sex']
            data = int()
            kmrun = str()
            if sex == '男':
                kmrun = item['Thousand']
            elif sex == '女':
                kmrun = item['Eighty']

            if kmrun == '4' or kmrun == '3':
                data = 60 * int(kmrun)

            else:
                try:
                    split = kmrun.split('\'')
                    data = int(split[0]) * 60 + int(split[1])
                    print(data)
                except:
                    try:
                        split = kmrun.split('′')
                        data = int(split[0]) * 60 + int(split[1])
                        print(data)
                    except:
                        print(kmrun)
            mongo14.update_one(
                {'_id': item['_id']},
                {'$set': {'LongRun': data}}
            )


    elif year == 15:
        for item in mongo15.find():
            sex = item['Sex']
            kmrun = str()
            if sex == '男':
                kmrun = item['Thousand']
            elif sex == '女':
                kmrun = item['Eighty']

            try:
                data = int(kmrun)
            except:
                data = int()
            print(data)
            mongo15.update_one(
                {'_id': item['_id']},
                {'$set': {'LongRun': data}}
            )

    elif year == 16:
        for item in mongo16.find():
            sex = item['Sex']
            data = int()
            kmrun = str()
            if sex == '男':
                kmrun = item['Thousand']
            elif sex == '女':
                kmrun = item['Eighty']

            if kmrun == '4' or kmrun == '3' or kmrun == '2':
                data = 60 * int(kmrun)

            else:
                try:
                    split = kmrun.split('\'')
                    data = int(split[0]) * 60 + int(split[1])
                    print(data)
                except:
                    try:
                        split = kmrun.split('′')
                        data = int(split[0]) * 60 + int(split[1])
                        print(data)
                    except:
                        print(kmrun)
            mongo16.update_one(
                {'_id': item['_id']},
                {'$set': {'LongRun': data}}
            )



def Kmrun_Insert(year):
    mongo = get_mongo_collection(year)

    marks = ['100', '95', '90', '85', '80', '78', '76', '74', '72', '70', '68',
             '66', '64', '62', '60', '50', '40', '30', '20', '10']

    thousand_standard_raw = {
        100: "3'17",
        95: "3'22",
        90: "3'27",
        85: "3'34",
        80: "3'42",
        78: "3'47",
        76: "3'52",
        74: "3'57",
        72: "4'02",
        70: "4'07",
        68: "4'12",
        66: "4'17",
        64: "4'22",
        62: "4'27",
        60: "4'32",
        50: "4'52",
        40: "5'12",
        30: "5'32",
        20: "5'52",
        10: "6'12"
    }

    thousand_standard = {
        "10": 372,
        "20": 352,
        "30": 332,
        "40": 312,
        "50": 292,
        "60": 272,
        "62": 267,
        "64": 262,
        "66": 257,
        "68": 252,
        "70": 247,
        "72": 242,
        "74": 237,
        "76": 232,
        "78": 227,
        "80": 222,
        "85": 214,
        "90": 207,
        "95": 202,
        "100": 197
    }

    eighty_standard_raw = {
        100: "3'18",
        95: "3'24",
        90: "3'30",
        85: "3'37",
        80: "3'44",
        78: "3'49",
        76: "3'54",
        74: "3'59",
        72: "4'04",
        70: "4'09",
        68: "4'14",
        66: "4'19",
        64: "4'24",
        62: "4'29",
        60: "4'34",
        50: "4'44",
        40: "4'54",
        30: "5'04",
        20: "5'14",
        10: "5'24"
    }

    eighty_standard = {
        "10": 324,
        "20": 314,
        "30": 304,
        "40": 294,
        "50": 284,
        "60": 274,
        "62": 269,
        "64": 264,
        "66": 259,
        "68": 254,
        "70": 249,
        "72": 244,
        "74": 239,
        "76": 234,
        "78": 229,
        "80": 224,
        "85": 217,
        "90": 210,
        "95": 204,
        "100": 198
    }

    '''
    for mark, time in thousand_standard_raw.items():
        split = time.split('\'')
        data = int(split[0]) * 60 + int(split[1])
        thousand_standard_raw[mark] = data

    print(json.dumps(thousand_standard_raw, indent=2, sort_keys=True))
    '''

    for item in mongo.find():
        long_run_time = item['LongRun']
        sex = item['Sex']

        mark = int()
        grade = str()

        standard = dict()
        if sex == '男':
            standard = thousand_standard
        elif sex == '女':
            standard = eighty_standard

        if long_run_time == 0:
            grade = 'N\A'

        elif long_run_time <= standard['90']:
            grade = '优秀'

        elif long_run_time <= standard['80']:
            grade = '良好'

        elif long_run_time <= standard['60']:
            grade = '及格'

        else:
            grade = '不及格'

        if long_run_time == 0:
            mark = -1

        elif long_run_time <= standard['100']:
            mark = 100

        elif long_run_time > standard['10']:
            mark = 0

        else:
            for i in range(0, len(marks) - 1):
                if long_run_time >= standard[marks[i]] and long_run_time < standard[marks[i + 1]]:
                    mark = int(marks[i + 1])

        print(mark, grade)

        mongo.update_one(
            {'_id': item['_id']},
            {'$set': {'LongRunScore': mark, 'LongRunGrade': grade}}
        )


def Kmrun_in_Lines():
    mongo13 = get_mongo_collection(13)
    mongo14 = get_mongo_collection(14)
    mongo15 = get_mongo_collection(15)
    mongo16 = get_mongo_collection(16)

    marks = ['100', '95', '90', '85', '80', '78', '76', '74', '72', '70',
             '68', '66', '64', '62', '60', '50', '40', '30', '20', '10']

    colors = ['#98F5FF', '#7CFC00', '#FFFF00', '#FF6347']

    marks_num_13 = list()
    marks_num_14 = list()
    marks_num_15 = list()
    marks_num_16 = list()

    for mark in marks:
        marks_num_13.append(mongo13.count({'LongRunScore': int(mark)}))
        marks_num_14.append(mongo14.count({'LongRunScore': int(mark)}))
        marks_num_15.append(mongo15.count({'LongRunScore': int(mark)}))
        marks_num_16.append(mongo16.count({'LongRunScore': int(mark)}))

    trace13 = go.Scatter(
        x=marks,
        y=marks_num_13,
        name='2013年',
        line={
            'color': colors[0],
            'width': 3
        }
    )

    trace14 = go.Scatter(
        x=marks,
        y=marks_num_14,
        name='2014年',
        line={
            'color': colors[2],
            'width': 3
        }
    )

    trace15 = go.Scatter(
        x=marks,
        y=marks_num_15,
        name='2015年',
        line={
            'color': colors[2],
            'width': 3
        }
    )

    trace16 = go.Scatter(
        x=marks,
        y=marks_num_16,
        name='2016年',
        line={
            'color': colors[3],
            'width': 3
        }
    )

    data = [trace13, trace14, trace15, trace16]

    layout = go.Layout(
        title='800M/1000M跑成绩分布(2D)',
        scene={
            'xaxis': {
                'title': '成绩',
                'titlefont': {
                    'family': "黑体",
                    'size': 15
                }
            },
            'yaxis': {
                'title': '人数',
                'range': [0, 1500],
                'titlefont': {
                    'family': "黑体",
                    'size': 15
                }
            },
        },
        showlegend=True,
        legend={
            'font': {
                'size': 13
            }
        }
    )

    fig = {'data': data, 'layout': layout}

    py.iplot(fig, filename='LongRun in 2D')


def Kmrun_in_3DScatter():
    mongo13 = get_mongo_collection(13)
    mongo14 = get_mongo_collection(14)
    mongo15 = get_mongo_collection(15)
    mongo16 = get_mongo_collection(16)

    marks = ['100', '95', '90', '85', '80', '78', '76', '74', '72', '70',
             '68', '66', '64', '62', '60', '50', '40', '30', '20', '10']

    colors = ['#98F5FF', '#7CFC00', '#FFFF00', '#FF6347']

    marks_num_13 = list()
    marks_num_14 = list()
    marks_num_15 = list()
    marks_num_16 = list()

    for mark in marks:
        marks_num_13.append(mongo13.count({'LongRunScore': int(mark)}))
        marks_num_14.append(mongo14.count({'LongRunScore': int(mark)}))
        marks_num_15.append(mongo15.count({'LongRunScore': int(mark)}))
        marks_num_16.append(mongo16.count({'LongRunScore': int(mark)}))

    trace13 = go.Scatter3d(
        x=marks,
        y=['2013'] * len(marks),
        z=marks_num_13,
        mode='lines',
        name='2013年',
        surfaceaxis=1,
        surfacecolor=colors[0],
        line={
            'width': 5,
            'color': '#191970'
        }
    )

    trace14 = go.Scatter3d(
        x=marks,
        y=['2014'] * len(marks),
        z=marks_num_14,
        mode='lines',
        name='2014年',
        surfaceaxis=1,
        surfacecolor=colors[1],
        line={
            'width': 5,
            'color': '#006400'
        }
    )

    trace15 = go.Scatter3d(
        x=marks,
        y=['2015'] * len(marks),
        z=marks_num_15,
        mode='lines',
        name='2015年',
        surfaceaxis=1,
        surfacecolor=colors[2],
        line={
            'width': 5,
            'color': '#8B6914'
        }
    )

    trace16 = go.Scatter3d(
        x=marks,
        y=['2016'] * len(marks),
        z=marks_num_16,
        mode='lines',
        name='2016年',
        surfaceaxis=1,
        surfacecolor=colors[3],
        line={
            'width': 5,
            'color': '#8B3A3A'
        }
    )

    layout = go.Layout(
        title='800M/1000M跑成绩分布(3D)',
        scene={
            'xaxis': {
                'title': '成绩',
                'titlefont': {
                    'family': "黑体",
                    'size': 15
                }
            },
            'yaxis': {
                'title': '年份',
                'tickvals': ['2013', '2014', '2015', '2016'],
                'ticklen': 5,
                'titlefont': {
                    'family': "黑体",
                    'size': 15
                }
            },
            'zaxis': {
                'title': '人数',
                'range': [0, 1500],
                'titlefont': {
                    'family': "黑体",
                    'size': 15
                }
            },
            'camera': {
                'eye': {
                    'x': -1.7, 'y': -1.7, 'z': 0.5
                }
            }
        },
        showlegend=True
    )

    data = [trace13, trace14, trace15, trace16]

    fig = {
        'data': data,
        'layout': layout
    }

    py.iplot(fig, filename='LongRun in 3D')


def Kmrun_Analysis_in_Pie():
    mongo13 = get_mongo_collection(13)
    mongo14 = get_mongo_collection(14)
    mongo15 = get_mongo_collection(15)
    mongo16 = get_mongo_collection(16)

    colors = ['#76EE00', '#6A5ACD', '#EEEE00', '#FF3030']

    fig = {
        "data": [
            {
                'values': [
                    mongo13.count({'LongRunGrade': '优秀'}),
                    mongo13.count({'LongRunGrade': '良好'}),
                    mongo13.count({'LongRunGrade': '及格'}),
                    mongo13.count({'LongRunGrade': '不及格'})
                ],
                "domain": {
                    'x': [0, .48],
                    'y': [0, .49]
                },

                'labels': ['优秀', '良好', '及格', '不及格'],
                'name': '2013年长跑',
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
                    mongo14.count({'LongRunGrade': '优秀'}),
                    mongo14.count({'LongRunGrade': '良好'}),
                    mongo14.count({'LongRunGrade': '及格'}),
                    mongo14.count({'LongRunGrade': '不及格'})
                ],
                "domain": {
                    "x": [.52, 1],
                    'y': [0, .49]
                },
                'labels': ['优秀', '良好', '及格', '不及格'],
                'name': '2014年长跑',
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
                    mongo15.count({'LongRunGrade': '优秀'}),
                    mongo15.count({'LongRunGrade': '良好'}),
                    mongo15.count({'LongRunGrade': '及格'}),
                    mongo15.count({'LongRunGrade': '不及格'})
                ],
                "domain": {
                    "x": [0, .48],
                    'y': [.51, 1]
                },
                'labels': ['优秀', '良好', '及格', '不及格'],
                'name': '2015年长跑',
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
                    mongo16.count({'LongRunGrade': '优秀'}),
                    mongo16.count({'LongRunGrade': '良好'}),
                    mongo16.count({'LongRunGrade': '及格'}),
                    mongo16.count({'LongRunGrade': '不及格'})
                ],
                "domain": {
                    "x": [.52, 1],
                    'y': [.51, 1]
                },
                'labels': ['优秀', '良好', '及格', '不及格'],
                'name': '2016年长跑',
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
            "title": "1000m/800m跑",
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

    py.iplot(fig, filename='KMrun Basix')

def LongRun_Sex_Compare(year):

    mongo = get_mongo_collection(year)

    marks = ['100', '95', '90', '85', '80', '78', '76', '74', '72', '70',
             '68', '66', '64', '62', '60', '50', '40', '30', '20', '10']

    male_nums = list()
    female_nums = list()

    for mark in marks:
        male_num = mongo.count({'$and': [{'LongRunScore': int(mark)}, {'Sex': '男'}]})
        female_num = mongo.count({'$and': [{'LongRunScore': int(mark)}, {'Sex': '女'}]})

        male_nums.append(-male_num)
        female_nums.append(female_num)

    annotations = []
    for female_num, male_num, mark in zip(female_nums, male_nums, marks):
        annotations.append(
            dict(
                x=female_num+20,
                y=int(mark),
                xref='x',
                yref='y',
                text=str(female_num),
                showarrow=False
            )
        )
        annotations.append(
            dict(
                x=male_num-20,
                y=int(mark),
                xref='x',
                yref='y',
                text=str(-male_num),
                showarrow=False
            )
        )

    layout = go.Layout(
        title='长跑(800m/1000m) 20'+ str(year) + '年男女分数对比',
        yaxis=go.layout.YAxis(
            title='分数',
            tickvals=marks,
            titlefont={'size': 16, 'family': '黑体'}
        ),
        xaxis=go.layout.XAxis(
            range=[-1100, 1100],
            tickvals=[-1000, -800, -600, -400, -200, 0, 200, 400, 600, 800, 1000],
            ticktext=[1000, 800, 600, 400, 200, 0, 200, 400, 600, 800, 1000],
            title='人数',
            titlefont={'size': 16, 'family': '黑体'}
        ),
        barmode='overlay',
        bargap=0.1,
        legend={
            'x': 1,
            'bgcolor': '#CDCDB4',
            'borderwidth': 1,
            'bordercolor': '#4F4F4F',
            'font': {'size': 12},
        },
        annotations=annotations
        )

    male_data13 = go.Bar(
        y=marks,
        x=male_nums,
        orientation='h',
        hoverinfo='x+name+y',
        name='男',
        width=1.5,
        marker={'color': '#00FF7F'}
    )

    female_data13 = go.Bar(
        y=marks,
        x=female_nums,
        orientation='h',
        hoverinfo='x+name+y',
        name='女',
        width=1.5,
        marker={'color': '#8470FF'}
    )

    fig = {'data': [male_data13, female_data13], 'layout': layout}
    py.iplot(fig, filename='20'+str(year)+'年长跑男女对比')

if __name__ == '__main__':
    LongRun_Sex_Compare(13)