from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import TGR2017
import json
import psycopg2
import requests
import base64

def index(request):
    try:
      conn = psycopg2.connect("dbname='de1120l2joq0tl' user='iblwvhvainfqbk' host='ec2-75-101-142-182.compute-1.amazonaws.com' password='d3cc75b395f3c484f93693e377087b6d9e2db7f3153f6274809bab91695c1433'")
      r ="success"
    except:
        r ="error"
    return HttpResponse(r)
    # return render(request, 'index.html')

@csrf_exempt
def postdata(request):
    if request.method == 'POST':
        param = request.POST
        id = int(param['id'])
        picture = str(param['picture'])
        del param
        try:
            conn = psycopg2.connect(
                "dbname='de1120l2joq0tl' user='iblwvhvainfqbk' host='ec2-75-101-142-182.compute-1.amazonaws.com' password='d3cc75b395f3c484f93693e377087b6d9e2db7f3153f6274809bab91695c1433'")
        except:
            print "error connect"
        cur = conn.cursor()
        try:
            sql = """UPDATE hardware SET picture = %s WHERE id = %s"""
            cur.execute(sql,(picture, id))
        except psycopg2.Error as e:
            print e.pgerror
        cur.close()
        conn.close()
        return HttpResponse(status=200)
    if request.method == 'GET':
        r = "get method"
        return HttpResponse(r)


def getdata(request):
    response = requests.get('http://api.wunderground.com/api/12b2d3c7265fb166/conditions/q/TH/Bangkok.json')
    jsonGetData = response.json()
    temperature = jsonGetData["current_observation"]["temp_c"]
    pressure = jsonGetData["current_observation"]["pressure_mb"]
    weather = jsonGetData["current_observation"]["weather"]
    try:
        conn = psycopg2.connect("dbname='de1120l2joq0tl' user='iblwvhvainfqbk' host='ec2-75-101-142-182.compute-1.amazonaws.com' password='d3cc75b395f3c484f93693e377087b6d9e2db7f3153f6274809bab91695c1433'")
    except:
        print "error"
    cur = conn.cursor()
    try:
        sql = """SELECT * FROM hardware ORDER BY id DESC LIMIT 1"""
        cur.execute(sql)
    except:
        print "ERROR query from hardware"
    row = cur.fetchone()
    if row is None:
        resBody = "No Data found"
        return HttpResponse(resBody)
    humidity = row[1]
    picture = row[2]
    try:
        sql = """SELECT MAX(id) FROM tgr2017"""
        cur.execute(sql)
    except:
        print "error select max"
    row = cur.fetchone()
    if row is None:
        id = 1
    # id = row[0]
    # if id is None:
    #     id = 1
    try:
        sql = """INSERT INTO tgr2017 VALUES (%s, %s, %s, %s)"""
        cur.execute(sql,(id+1,temperature, weather, pressure))
        conn.commit()
    except psycopg2.Error as e:
        print e.pgerror
        print "CANT INSERT"

    try:
        sql = """SELECT * FROM tgr2017 ORDER BY id DESC LIMIT 1"""
        cur.execute(sql)
    except:
        print "error select max"
    row = cur.fetchone()
    row = {
        "id":row[0],
        "temperature":row[1],
        "weather":row[2],
        "pressure":row[3],
        "humidity":humidity,
        "picture":picture
    }
    jsonData = json.dumps(row)
    print jsonData
    cur.close()
    conn.close()
    resBody = jsonData
    return HttpResponse(resBody, content_type = "application/json")


def db(request):
    tgr2017 = TGR2017()
    tgr2017.save()
    tgr2017 = TGR2017.objects.all()
    return render(request, 'db.html', {'tgr2017': tgr2017})
