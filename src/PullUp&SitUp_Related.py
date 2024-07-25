import pymongo
import plotly.plotly as py
import plotly.graph_objs as go
import traceback


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


def Pullup_and_Situp_Preprocess(year):
    mongo = get_mongo_collection(year)

    if year == 13:
        for item in mongo.find({'Pullup': {'$exists': False}}):

            raw = item['Chin']
            sex = item['Sex']

            pullup = -1
            situp = -1

            if sex == '男':
                try:
                    pullup = int(raw)
                    print(pullup)
                except:
                    print(raw)

            elif sex == '女':
                try:
                    situp = int(raw)
                    print(situp)
                except:
                    print(raw)


            mongo.update_one(
                {'_id': item['_id']},
                {'$set': {'Pullup': pullup, 'Situp': situp}}
            )


    elif year in [14, 15, 16]:
        for item in mongo.find():

            raw_pullup = item['PullupRaw']
            raw_situp = item['SitupRaw']
            sex = item['Sex']

            pullup = -1
            situp = -1

            try:
                pullup = int(raw_pullup)
            except:
                pass

            try:
                situp = int(raw_situp)
            except:
                pass

            print(sex, pullup, situp)

            mongo.update_one(
                {'_id': item['_id']},
                {'$set': {'Pullup': pullup, 'Situp': situp, 'PullupRaw': raw_pullup, 'SitupRaw': raw_situp}}
            )


def Situp_and_Pullup_Insert(year):

    mongo = get_mongo_collection(year)

    situp_marks = ['100', '95', '90', '85', '80', '78', '76', '74', '72', '70', '68',
             '66', '64', '62', '60', '50', '40', '30', '20', '10']

    pullup_marks = ['100', '95', '90', '85', '80', '76', '72', '68',
             '64', '60', '50', '40', '30', '20', '10']

    situp_standard = {
        "10": 14,
        "20": 16,
        "30": 18,
        "40": 20,
        "50": 22,
        "60": 24,
        "62": 26,
        "64": 28,
        "66": 30,
        "68": 32,
        "70": 34,
        "72": 36,
        "74": 38,
        "76": 40,
        "78": 42,
        "80": 44,
        "85": 49,
        "90": 52,
        "95": 54,
        "100": 56
    }

    pullup_standard = {
        "10": 5,
        "20": 6,
        "30": 7,
        "40": 8,
        "50": 9,
        "60": 10,
        "64": 11,
        "68": 12,
        "72": 13,
        "76": 14,
        "80": 15,
        "85": 16,
        "90": 17,
        "95": 18,
        "100": 19
    }

    for item in mongo.find({'$and': [{'Sex': '男'}, {'PullupScore': {'$exists': False}}]}):
        pullup_num = item['Pullup']

        mark = int()
        grade = str()

        if pullup_num == -1:
            grade = 'N\A'

        elif pullup_num >= pullup_standard['90']:
            grade = '优秀'

        elif pullup_num >= pullup_standard['80']:
            grade = '良好'

        elif pullup_num >= pullup_standard['60']:
            grade = '及格'

        elif pullup_num < pullup_standard['60']:
            grade = '不及格'

        if pullup_num == -1:
            mark = -1

        elif pullup_num >= pullup_standard['100']:
            mark = 100

        elif pullup_num < pullup_standard['10']:
            mark = 0

        else:
            for i in range(0, len(pullup_marks) - 1):
                if pullup_num < pullup_standard[pullup_marks[i]] and pullup_num >= pullup_standard[pullup_marks[i + 1]]:
                    mark = int(pullup_marks[i+1])

        print('P', pullup_num, mark, grade)


        mongo.update_one(
            {'_id': item['_id']},
            {'$set': {'PullupScore': mark, 'PullupGrade': grade}}
        )



    for item in mongo.find({'$and': [{'Sex': '女'}, {'SitupScore': {'$exists': False}}]}):
        situp_num = item['Situp']

        mark = int()
        grade = str()

        if situp_num == -1:
            grade = 'N\A'

        elif situp_num >= situp_standard['90']:
            grade = '优秀'

        elif situp_num >= situp_standard['80']:
            grade = '良好'

        elif situp_num >= situp_standard['60']:
            grade = '及格'

        elif situp_num < situp_standard['60']:
            grade = '不及格'

        if situp_num == -1:
            mark = -1

        elif situp_num >= situp_standard['100']:
            mark = 100

        elif situp_num < situp_standard['10']:
            mark = 0

        else:
            for i in range(0, len(situp_marks) - 1):
                if situp_num < situp_standard[situp_marks[i]] and situp_num >= situp_standard[situp_marks[i + 1]]:
                    mark = int(situp_marks[i+1])

        print('S', situp_num, mark, grade)

        mongo.update_one(
            {'_id': item['_id']},
            {'$set': {'SitupScore': mark, 'SitupGrade': grade}}
        )


def Situp_in_Lines():
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
        marks_num_13.append(mongo13.count({'SitupScore': int(mark)}))
        marks_num_14.append(mongo14.count({'SitupScore': int(mark)}))
        marks_num_15.append(mongo15.count({'SitupScore': int(mark)}))
        marks_num_16.append(mongo16.count({'SitupScore': int(mark)}))

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
        title='仰卧起坐成绩分布(2D)',
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

    py.iplot(fig, filename='Situp in 2D')


def Situp_in_3DScatter():
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
        marks_num_13.append(mongo13.count({'SitupScore': int(mark)}))
        marks_num_14.append(mongo14.count({'SitupScore': int(mark)}))
        marks_num_15.append(mongo15.count({'SitupScore': int(mark)}))
        marks_num_16.append(mongo16.count({'SitupScore': int(mark)}))

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
        text='y',
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
        text='y',
        surfacecolor=colors[3],
        line={
            'width': 5,
            'color': '#8B3A3A'
        }
    )

    layout = go.Layout(
        title='仰卧起坐成绩分布(3D)',
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
                'ticklen': 7,
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

    py.iplot(fig, filename='Situp in 3D')


def Pullup_in_Lines():
    mongo13 = get_mongo_collection(13)
    mongo14 = get_mongo_collection(14)
    mongo15 = get_mongo_collection(15)
    mongo16 = get_mongo_collection(16)

    marks = ['100', '95', '90', '85', '80', '76', '72', '68',
             '64', '60', '50', '40', '30', '20', '10']

    colors = ['#98F5FF', '#7CFC00', '#FFFF00', '#FF6347']

    marks_num_13 = list()
    marks_num_14 = list()
    marks_num_15 = list()
    marks_num_16 = list()

    for mark in marks:
        marks_num_13.append(mongo13.count({'PullupScore': int(mark)}))
        marks_num_14.append(mongo14.count({'PullupScore': int(mark)}))
        marks_num_15.append(mongo15.count({'PullupScore': int(mark)}))
        marks_num_16.append(mongo16.count({'PullupScore': int(mark)}))

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
        title='引体向上成绩分布(2D)',
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

    py.iplot(fig, filename='Pullup in 2D')


def Pullup_in_3DScatter():
    mongo13 = get_mongo_collection(13)
    mongo14 = get_mongo_collection(14)
    mongo15 = get_mongo_collection(15)
    mongo16 = get_mongo_collection(16)

    marks = ['100', '95', '90', '85', '80', '76', '72', '68',
             '64', '60', '50', '40', '30', '20', '10']

    colors = ['#98F5FF', '#7CFC00', '#FFFF00', '#FF6347']

    marks_num_13 = list()
    marks_num_14 = list()
    marks_num_15 = list()
    marks_num_16 = list()

    for mark in marks:
        marks_num_13.append(mongo13.count({'PullupScore': int(mark)}))
        marks_num_14.append(mongo14.count({'PullupScore': int(mark)}))
        marks_num_15.append(mongo15.count({'PullupScore': int(mark)}))
        marks_num_16.append(mongo16.count({'PullupScore': int(mark)}))

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
        text='y',
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
        text='y',
        surfacecolor=colors[3],
        line={
            'width': 5,
            'color': '#8B3A3A'
        }
    )

    layout = go.Layout(
        title='引体向上成绩分布(3D)',
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
                'ticklen': 7,
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

    py.iplot(fig, filename='Pullup in 3D')

if __name__ == '__main__':
    Pullup_in_3DScatter()
