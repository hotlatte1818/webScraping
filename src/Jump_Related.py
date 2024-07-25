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

def Jump_Preprocess(year):
    mongo13 = get_mongo_collection(13)
    mongo14 = get_mongo_collection(14)
    mongo15 = get_mongo_collection(15)
    mongo16 = get_mongo_collection(16)

    if year == 13:
        for item in mongo13.find({'JumpRaw': {'$exists': False}}):

            jump = item['Jump']

            jump_precessed = int()
            try:
                jump_float = float(jump)
                jump_precessed = round(jump_float * 100, 2)
                print(jump_precessed)
            except:
                print(jump_precessed)

            mongo13.update_one(
                {'_id': item['_id']},
                {'$set': {'Jump': jump_precessed, 'JumpRaw': jump}}
            )

    elif year == 14:
        for item in mongo14.find({'JumpRaw': {'$exists': False}}):

            jump = item['Jump']
            jump_processed = int()
            try:
                jump_processed = int(jump)
                print(jump_processed)
            except:
                try:
                    jump_processed = int(jump.split('.')[0])
                    print(jump_processed)
                except:
                    print(jump_processed)


            mongo14.update_one(
                {'_id': item['_id']},
                {'$set': {'Jump': jump_processed, 'JumpRaw': jump}}
            )



    elif year == 15:
        for item in mongo15.find({'JumpRaw': {'$exists': False}}):

            jump = item['Jump']

            jump_processed = int()
            try:
                jump_processed = int(jump)
                print(jump_processed)
            except:
                print(jump_processed)


            mongo15.update_one(
                {'_id': item['_id']},
                {'$set': {'Jump': jump_processed, 'JumpRaw': jump}}
            )


    elif year == 16:
        for item in mongo16.find():
            jump = item['JumpRaw']
            jump_precessed = int()
            try:
                jump_float = float(jump)
                jump_precessed = round(jump_float * 100, 2)
                print(jump_precessed)
            except:
                print(jump_precessed)

            mongo16.update_one(
                {'_id': item['_id']},
                {'$set': {'Jump': jump_precessed, 'JumpRaw': jump}}
            )

def Jump_Insert(year):

    mongo = get_mongo_collection(year)

    marks = ['100', '95', '90', '85', '80', '78', '76', '74', '72', '70', '68',
             '66', '64', '62', '60', '50', '40', '30', '20', '10']

    male_standard = {
        "100": 273,
        "95": 268,
        "90": 263,
        "85": 256,
        "80": 248,
        "78": 244,
        "76": 240,
        "74": 236,
        "72": 232,
        "70": 228,
        "68": 224,
        "66": 220,
        "64": 216,
        "62": 212,
        "60": 208,
        "50": 203,
        "40": 198,
        "30": 193,
        "20": 188,
        "10": 183
    }

    female_standard = {
        "100": 207,
        "95": 201,
        "90": 195,
        "85": 188,
        "80": 181,
        "78": 178,
        "76": 175,
        "74": 172,
        "72": 169,
        "70": 166,
        "68": 163,
        "66": 160,
        "64": 157,
        "62": 154,
        "60": 151,
        "50": 146,
        "40": 141,
        "30": 136,
        "20": 131,
        "10": 126
    }

    for item in mongo.find():
        jump_dist = item['Jump']
        sex = item['Sex']

        mark = int()
        grade = str()

        standard = dict()
        if sex == '男':
            standard = male_standard
        elif sex == '女':
            standard = female_standard

        if jump_dist == 0:
            grade = 'N\A'

        elif jump_dist >= standard['90']:
            grade = '优秀'

        elif jump_dist >= standard['80']:
            grade = '良好'

        elif jump_dist >= standard['60']:
            grade = '及格'

        else:
            grade = '不及格'

        if jump_dist == 0:
            mark = -1

        elif jump_dist >= standard['100']:
            mark = 100

        elif jump_dist < standard['10']:
            mark = 0

        else:
            for i in range(0, len(marks) - 1):
                if jump_dist < standard[marks[i]] and jump_dist >= standard[marks[i + 1]]:
                    mark = int(marks[i + 1])

        print(mark, grade)


        mongo.update_one(
            {'_id': item['_id']},
            {'$set': {'JumpScore': mark, 'JumpGrade': grade}}
        )

def Jump_in_Lines():
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
        marks_num_13.append(mongo13.count({'JumpScore': int(mark)}))
        marks_num_14.append(mongo14.count({'JumpScore': int(mark)}))
        marks_num_15.append(mongo15.count({'JumpScore': int(mark)}))
        marks_num_16.append(mongo16.count({'JumpScore': int(mark)}))

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
        title='立定跳远成绩分布(2D)',
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

    py.iplot(fig, filename='Jump in 2D')


def Jump_in_3DScatter():
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
        marks_num_13.append(mongo13.count({'JumpScore': int(mark)}))
        marks_num_14.append(mongo14.count({'JumpScore': int(mark)}))
        marks_num_15.append(mongo15.count({'JumpScore': int(mark)}))
        marks_num_16.append(mongo16.count({'JumpScore': int(mark)}))

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
        title='立定跳远成绩分布(3D)',
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

    py.iplot(fig, filename='Jump in 3D')


def Jump_Sex_Compare(year):

    mongo = get_mongo_collection(year)

    marks = ['100', '95', '90', '85', '80', '78', '76', '74', '72', '70',
             '68', '66', '64', '62', '60', '50', '40', '30', '20', '10']

    male_nums = list()
    female_nums = list()

    for mark in marks:
        male_num = mongo.count({'$and': [{'JumpScore': int(mark)}, {'Sex': '男'}]})
        female_num = mongo.count({'$and': [{'JumpScore': int(mark)}, {'Sex': '女'}]})

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
        title='立定跳远 20'+ str(year) + '年男女分数对比',
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
    py.iplot(fig, filename='20'+str(year)+'年立定跳远男女对比')


if __name__ == '__main__':
    for year in [13, 14, 15, 16]:
        Jump_Sex_Compare(year)


