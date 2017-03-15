from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
import psycopg2
import requests

# Create your views here


def index(request):
    try:
      conn = psycopg2.connect("dbname='ds7gk4tphvn2v' user='sfszejfztqdxyo' host='ec2-23-21-220-23.compute-1.amazonaws.com' password='9e2b53c8d90e3f9ad12e7764ac7ecee875724c6d2f1d3ae3d31517ac4d88bddc'")
      cur = conn.cursor()
      sql_command =""" 
    CREATE TABLE iotdpu_data(
    rank  integer NOT NULL,
    firstname  varchar(40) NOT NULL,
    lastname   varchar(40) NOT NULL,
    university  varchar(40) NOT NULL,
    degree   integer NOT NULL,
    department   varchar(40) NOT NULL,
    gpa   double NOT NULL,
    studyORwork  varchar(40) NOT NULL) """
      cur.execute(sql_command)
      conn.commit()
      r ="success"
    
    
    except:
        r ="error"
    return HttpResponse(r)
    # return render(request, 'index.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})
