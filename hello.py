"""Cloud Foundry test"""
from flask import Flask, render_template, request
import sqlite3
import os

from trans_time_local import calculate_timezone, transfer_time
from cal_distance import calculate_distance
from kmeans import loadDataSet, kmean, plt1

app = Flask(__name__)

print(os.getenv("PORT"))
port = int(os.getenv("PORT", 5000))

conn = sqlite3.connect('myDb.db')
print("Opened database successfully")
cur = conn.cursor()
cur.execute('select * from quakes')
rows = cur.fetchall()
all_count = len(rows)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/goAssignment1')
def show_assignment_1():
    return render_template('assignment_1.html')


@app.route('/goAssignment2')
def show_assignment_2():
    return render_template('assignment_2.html')


@app.route('/list')
def list_all_data():
    conn_list = sqlite3.connect('myDb.db')
    print("Opened database successfully")
    cur_list = conn_list.cursor()
    cur_list.execute('select * from people')
    rows_list = cur_list.fetchall()
    return render_template("list.html", rows=rows_list)


@app.route('/show')
def show():
    picture_list = os.listdir('./static')
    re_list = []
    for str in picture_list:
        if ".jpg" in str:
            re_list.append((str, os.path.getsize('./static/' + str)))
    print(re_list)
    return render_template('picture.html', rows=re_list)


@app.route('/search_point', methods=['POST'])
def search_point():
    if request.method == 'POST':
        point = int(request.form.get('point'))
        conn = sqlite3.connect('myDb.db')
        print("Opened database successfully")
        cur = conn.cursor()
        cur.execute('select * from people')
        rows = cur.fetchall()

        result = []
        for row in rows:
            if row[1]:
                print(row[1])
                if point == row[1]:
                    result.append((row[0], row[4], row[5]))
        if result:
            return render_template("search_point.html", rows=result, point=point)
        else:
            return "no data"


@app.route('/search_range', methods=['POST'])
def search_range():
    if request.method == 'POST':
        range_front = int(request.form.get('front'))
        range_rear = int(request.form.get('rear'))
        in_fav = request.form.get('fav')
        conn = sqlite3.connect('myDb.db')
        print("Opened database successfully")
        cur = conn.cursor()
        cur.execute('select * from people')
        rows = cur.fetchall()
        result = []
        for row in rows:
            if row[1] and row[5]:
                print(row[1])
                print(row[5])
                if range_front <= row[1] <= range_rear and (in_fav in row[5]):
                    result.append((row[0], row[4], row[5]))
        print(result)
        return render_template("search_range.html", rows=result, front=range_front, rear=range_rear)


@app.route('/search_and_modify', methods=['POST'])
def search_and_modify():
    if request.method == 'POST':
        search_point = request.form.get('search_point')
        new_name = request.form.get('new_name')
        print(new_name)
        conn_modify = sqlite3.connect('myDb.db')
        curr = conn_modify.cursor()
        curr.execute('''UPDATE people SET Name = ? WHERE Points = ?''', (new_name, search_point))
        # curr.execute('''UPDATE people SET Picture = ? WHERE Room = ?''', (fileName.filename, search_room))
        conn_modify.commit()
        return render_template("modify.html")
    return "No Picture Found"


@app.route('/DataList')
def list_all_quakes():
    return render_template("list_quakes.html", rows=rows)


@app.route('/searchMag', methods=['POST'])
def search_over_mag():
    '''
     Quiz 2 part 5
    '''
    if request.method == 'POST':
        # inf = []
        conn = sqlite3.connect('myDb.db')
        cur = conn.cursor()
        # print("Opened database successfully")
        magNum = request.form.get('mag')
        # print("This is ", magNum)
        cursor = cur.execute("SELECT *  from quakes WHERE mag>? ORDER BY mag ASC", (magNum,))
        # print(cursor)
        row = cursor.fetchall()
        # print(row)
        return render_template("quiz_2_part_5.html", rows=row[0], count=all_count)


@app.route('/searchMagDate', methods=['POST'])
def searchMagDate():
    '''
    Part 8: modify all earthquakes within that range, to contain a mag of "999".
    '''
    if request.method == 'POST':
        # endTime = request.form.get('endTime')
        data_time = request.form.get('startTime')
        startTime = data_time + "T00:00"
        endTime = data_time + "T23:59"
        print(startTime)
        mindepth = request.form.get('magMin')
        maxdepth = request.form.get('magMax')
        conn = sqlite3.connect('myDb.db')
        cur = conn.cursor()
        print("Opened database successfully")
        cursor = cur.execute("SELECT *  from quakes WHERE depth>=? AND depth<=? AND time<=? AND time>=?",
                             (mindepth, maxdepth, endTime, startTime))
        # rows = cursor.fetchall()

        newmag = 999
        cur.execute('''UPDATE quakes SET mag = ? WHERE depth>=? AND depth<=? AND time<=? AND time>=?''',
                     (newmag, mindepth, maxdepth, endTime, startTime))
        # curr.execute('''UPDATE people SET Favorite = ? WHERE Point = ?''', (newfavorite, Point))
        conn.commit()
        conn1 = sqlite3.connect('myDb.db')
        cur1 = conn1.cursor()
        cursor1 = cur1.execute("SELECT *  from quakes WHERE depth>=? AND depth<=? AND time<=? AND time>=?",
                               (mindepth, maxdepth, endTime, startTime))
        rows = cursor1.fetchall()
        return render_template("quiz_2_part_8.html", rows=rows, minMag=mindepth, maxMag=maxdepth, count=len(rows),
                               endTime=endTime, startTime=startTime)


@app.route('/search_between_mag', methods=['POST'])
def search_between_mag():
    '''
    Quiz 2: part 6 show the number of quakes between those depth values in increments given
    '''
    if request.method == 'POST':
        front_mag = float(request.form.get('front_mag'))
        rear_mag = float(request.form.get("rear_mag"))
        increment = float(request.form.get("increment"))
        tmp = int((rear_mag - front_mag) / increment) + 1
        result = []
        range_list = []
        for i in range(tmp):
            minMag = front_mag + i * increment
            maxMag = front_mag + (i + 1) * increment
            if maxMag > rear_mag:
                maxMag = rear_mag
            range_list.append([(minMag, maxMag)])
            conn = sqlite3.connect('myDb.db')
            cur = conn.cursor()
            print("Opened database successfully")
            cursor = cur.execute("SELECT *  from quakes WHERE depth>=? AND depth<=?",(minMag, maxMag))
            rows = cursor.fetchall()
            result.append(rows)
            range_list[i].append(rows)
        print(range_list)
        return render_template("quiz_2_part_6.html", range_list=range_list, rows=range_list, lenght=len(result))



@app.route('/searchSpeLoc', methods=['POST'])
def searchSpeLoc():
    '''
    Part 7: every earthquake in that area (box).
    '''
    if request.method == 'POST':
        inf = []
        userLon1 = float(request.form.get('longitude1'))
        userLat1 = float(request.form.get('latitude1'))
        userLon2 = float(request.form.get('longitude2'))
        userLat2 = float(request.form.get('latitude2'))

        # userDis = request.form.get
        if (userLat1 > userLat2):
            maxLat = userLat1
            minLat = userLat2
        else:
            maxLat = userLat2
            minLat = userLat1

        if (userLon1 > userLon2):
            maxLon = userLon1
            minLon = userLon2
        else:
            maxLon = userLon2
            minLon = userLon1

        conn = sqlite3.connect('myDb.db')
        cur = conn.cursor()
        # print(userDis)
        print("Opened database successfully")
        cursor = cur.execute("SELECT *  from quakes ")
        for row in cursor:
            if row[1] <= float(maxLat) and row[1] >= float(minLat) and row[2] <= float(maxLon) and row[2] >= float(
                    minLon):
                print("Yes")
                inf.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        print(inf)
        count = len(inf)
        return render_template("quiz_2_part_7.html", rows=inf, Longitude1=userLon1, Latitude1=userLat1,
                               Longitude2=userLon2, Latitude2=userLat2, count=count,
                               )


@app.route('/searchPro', methods=['POST'])
def searchPro():
    if request.method == 'POST':
        night = []
        morning = []
        userMgaLevel = request.form.get('MagLevel')
        nightStart = '20:00'
        nightEnd = '07:59'
        conn = sqlite3.connect('myDb.db')
        cur = conn.cursor()
        print("Opened database successfully")
        cursor = cur.execute("SELECT *  from quakes WHERE mag>?", userMgaLevel)
        rows = cursor.fetchall()
        for row in rows:
            timeZone = calculate_timezone(row[2])
            uctTime = str(row[0])
            currentTime = transfer_time(uctTime, timeZone)
            if nightStart < str(currentTime) or str(currentTime) < nightEnd:
                night.append(row)
            else:
                morning.append(row)
        if len(night) > len(morning):
            result = 'night'
        else:
            result = 'morning'
        return render_template("searchProRes.html", rows=night, rows2=morning, timeHappen=result, morningHappen=len(morning),
                               nightHappen=len(night), tolHappen=len(morning) + len(night), magLevel=userMgaLevel)


@app.route('/clusters', methods=['POST'])
def clusters():
    if request.method == 'POST':
        numValue = int(request.form.get('Num'))
        dataMat1, x1, x2 = loadDataSet()
        label = kmean(dataMat1, numValue)
        data = plt1(label, x1, x2)
        return render_template("cluster_result.html", num=numValue, base64=data)


@app.route('/search9', methods=['POST'])
def search_part_9():
    '''
    Part 9: find all quakes within that distance of the location.
    :return:
    '''
    if request.method == 'POST':
        inf = []
        userLon = request.form.get('longitude')
        place = request.form.get('place')
        userLat = request.form.get('latitude')
        userDis = request.form.get('distance')
        conn = sqlite3.connect('myDb.db')
        cur = conn.cursor()
        # print(userDis)
        print("Opened database successfully")
        cursor = cur.execute("SELECT *  from quakes")
        for row in cursor:
            distance = calculate_distance(float(userLat), float(userLon), row[1], row[2])
            print("distan！！！", distance)
            if distance <= float(userDis):
                inf.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        count = len(inf)
        return render_template("quiz_2_part_9.html", rows=inf, Longitude=userLon, Latitude=userLat, count=count,
                               distance=userDis)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
