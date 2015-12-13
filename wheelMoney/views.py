# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from django.http import HttpResponse
 
from wheelMoney.models import User
from settings import Session
import json

import random

import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from datetime import datetime, timedelta

from random import randint

ad = ["<script type=\"text/javascript\">var uid = '84931';var wid = '167389';</script><script type=\"text/javascript\" src=\"http://cdn.popcash.net/pop.js\"></script>",
"<script type='text/javascript' src='//go.pub2srv.com/apu.php?zoneid=462693'></script>", 
"<script type=\"text/javascript\">(function() {    var configuration = {    \"token\": \"182b1b658c016dfc8e4542bd0d92334f\",    \"entryScript\": {        \"type\": \"timeout\",        \"timeout\": 3000,        \"capping\": {            \"limit\": 5,            \"timeout\": 24        }    },    \"exitScript\": {        \"enabled\": true    },    \"popUnder\": {        \"enabled\": true    }};    var script = document.createElement('script');    script.async = true;    script.src = '//cdn.shorte.st/link-converter.min.js';    script.onload = script.onreadystatechange = function () {var rs = this.readyState; if (rs && rs !='complete' && rs != 'loaded') return; shortestMonetization(configuration);};    var entry = document.getElementsByTagName('script')[0];    entry.parentNode.insertBefore(script, entry);})();</script>", 
"<script type=\"text/javascript\">  var _pop = _pop || [];  _pop.push(['siteId', 950598]);  _pop.push(['minBid', 0.000000]);  _pop.push(['popundersPerIP', 0]);  _pop.push(['delayBetween', 0]);  _pop.push(['default', false]);  _pop.push(['defaultPerDay', 0]);  _pop.push(['topmostLayer', false]);  (function() {    var pa = document.createElement('script'); pa.type = 'text/javascript'; pa.async = true;    var s = document.getElementsByTagName('script')[0];     pa.src = '//c1.popads.net/pop.js';    pa.onerror = function() {      var sa = document.createElement('script'); sa.type = 'text/javascript'; sa.async = true;      sa.src = '//c2.popads.net/pop.js';      s.parentNode.insertBefore(sa, s);    };    s.parentNode.insertBefore(pa, s);  })();</script>"]
 
def home(request):
    if "css" in request.path or "jss" in request.path or "images" in request.path:
        return
    print "Requesting new page %s" % request.path
    cookie = request.COOKIES.get('csrftoken')
    cachedUserData = validateCookie(cookie)
    randNum = randint(0,3)

    if cachedUserData is not False:
        randNum = cachedUserData.AdIndex
        updateValueForUser(cachedUserData.Username, "AdIndex", (randNum + 1) % 4)

    if request.path == "/withdraw" and request.method == "POST":
        method = request.POST.get("method")
        message = "Username : " + cachedUserData.Username + "\n" + "Method : " + method;
        send_email(message, "Withdrawal Request : " + cachedUserData.Username, cachedUserData.Email)
        content = {
            'username' : cachedUserData.Username,
            'Balance' : cachedUserData.Balance,
            'spinsLeft' : cachedUserData.Spinsleft,
            'email' : cachedUserData.Email,
            'disabled' : "disabled",
            'ads' : ad[randNum]
        }
        return render(request, 'withdrawal_success.html', content)

    if request.path == "/contact" and request.method == "POST":
        message = request.POST.get("message")
        email = request.POST.get("email")
        name = request.POST.get("name")
        send_email(message, name + " - contact us", email)
        if cachedUserData == False:
            content = {
                    'visib' : "hidden",
                    'ads' : ad[randNum]
            }
        else:
            content = {
                    'username' : cachedUserData.Username,
                    'Balance' : cachedUserData.Balance,
                    'spinsLeft' : cachedUserData.Spinsleft,
                    'visib' : "",
                    'ads' : ad[randNum]
            }
        return render(request, 'contact_success.html', content)

    if request.path == "/advertiser" and request.method == "POST":
        message = request.POST.get("message")
        email = request.POST.get("email")
        name = request.POST.get("name")
        send_email(message, name + " - advertiser", email)

        if cachedUserData == False:
            content = {
                    'visib' : "hidden",
                    'ads' : ad[randNum]
            }
        else:
            content = {
                    'username' : cachedUserData.Username,
                    'Balance' : cachedUserData.Balance,
                    'spinsLeft' : cachedUserData.Spinsleft,
                    'visib' : "",
                    'ads' : ad[randNum]
            }

        return render(request, 'contact_success.html', content)

    if request.path == "/":
        if cachedUserData == False:
            content = {
                    'visib' : "hidden",
                    'ads' : ad[randNum]
            }
        else:
            content = {
                    'username' : cachedUserData.Username,
                    'Balance' : cachedUserData.Balance,
                    'spinsLeft' : cachedUserData.Spinsleft,
                    'visib' : "",
                    'ads' : ad[randNum]
            }
        return render(request, 'index.html', content)

    if request.method == "POST" and request.path == "/spinRes":
        res = float(request.POST.get('res'))
        winner_balance = res % 2
        winner_spins = int(res)/10
        modifyBalance(cookie, winner_balance, winner_spins)
        return HttpResponse("Success")

    if request.path == "/game_wi_spin":
        return HttpResponse(isWinner())

    if request.path == "/faqs":
        if cachedUserData == False:
            content = {
                    'visib' : "hidden",
                    'ads' : ad[randNum]
            }
        else:
            content = {
                    'username' : cachedUserData.Username,
                    'Balance' : cachedUserData.Balance,
                    'spinsLeft' : cachedUserData.Spinsleft,
                    'visib' : "",
                    'ads' : ad[randNum]
            }

        return render(request, 'faqs.html', content)

    if request.path == "/login":
        if request.method == "GET":
            cachedUserData = validateCookie(cookie)
            if cachedUserData == False:
                return render(request, 'login.html')
            else:
                content = {
                        'username' : cachedUserData.Username,
                        'Balance' : cachedUserData.Balance,
                        'spinsLeft' : cachedUserData.Spinsleft,
                        'ang' : isWinner(),
                        'ads' : ad[randNum]
                }
            return render(request, 'game.html', content)

        if(request.method == "POST"):
            username = request.POST.get('username')
            password = request.POST.get('password')
            if request.POST.has_key('email'):
                firstName = request.POST.get('firstName')
                lastName = request.POST.get('lastName')
                username = request.POST.get('username')
                address = request.POST.get('address')
                email = request.POST.get('email')
                referral = request.POST.get('referral')
                flag = registerUser(username, password, firstName, lastName, address, email, cookie, referral)

                if(flag == False):
                    return render(request, 'invalid_login.html')

                return render(request, 'account_created.html')
            else:
                if isValidUser(username, password, cookie):
                    session = Session()
                    user_query = session.query(User).filter_by(Username=username)
                    content = {
                        'username' : username,
                        'Balance' : user_query.first().Balance,
                        'spinsLeft' : user_query.first().Spinsleft,
                        'ang' : isWinner(),
                        'ads' : ad[randNum]
                    }
                    return render(request, 'game.html', content)
                else:
                    return render(request, 'invalid_login.html')


        return render(request, 'login.html')

    if request.path == "/logout":
        logUserOut(cookie)        
        content = {
                'visib' : "hidden",
                'ads' : ad[randNum]
        }

        return render(request, 'index.html', content)

    if request.path == "/withdraw":
        session = Session()
        user_query = session.query(User).filter_by(Cookie=cookie)
        disabled = ''

        if(user_query.first().Balance < 2):
            disabled = 'disabled',
            
        content = {
            'username' : user_query.first().Username,
            'Balance' : user_query.first().Balance,
            'spinsLeft' : user_query.first().Spinsleft,
            'email' : user_query.first().Email,
            'disabled' : disabled,
            'ads' : ad[randNum]
        }
        return render(request, 'withdraw.html', content)

    # if request.path == "/" and request.method == "POST":
    #     username = request.POST.get("username")
    #     password = request.POST.get("password")

    #     if len(username) <= 0 or len(password) <= 0:
    #         return render(request, 'invalid_login.html')

    #     # Register new account
    #     if request.POST.has_key('email'):
    #         firstName = request.POST.get("firstName")
    #         lastName = request.POST.get("lastName")
    #         address = request.POST.get("address")
    #         email = request.POST.get("email")
    #         registerUser(username, password, firstName, lastName, address, email, cookie)
    #         content = {
    #             'username' : username
    #         }
    #         return render(request, 'game.html', content)
    #     else:
    #         if isValidUser(username, password, cookie):
    #             content = {
    #                 'username' : username
    #             }
    #             return render(request, 'game.html', content)
    #         else:
    #             return render(request, 'invalid_login.html')

    content = {
        'path' : request.path
    }
    if request.path == '/contact':
        if cachedUserData == False:
            content = {
                    'visib' : "hidden",
                    'ads' : ad[randNum]
            }
        else:
            content = {
                    'username' : cachedUserData.Username,
                    'Balance' : cachedUserData.Balance,
                    'spinsLeft' : cachedUserData.Spinsleft,
                    'visib' : "",
                    'ads' : ad[randNum]
            }
        return render(request, 'contact_us.html', content)
    elif request.path == '/advertiser':
        if cachedUserData == False:
            content = {
                    'visib' : "hidden"
            }
        else:
            content = {
                    'username' : cachedUserData.Username,
                    'Balance' : cachedUserData.Balance,
                    'spinsLeft' : cachedUserData.Spinsleft,
                    'visib' : ""
            }
        return render(request, 'advertiser.html', content)

    return render(request, 'index.html')

def validateCookie(cookie):
    session = Session()
    user_query = session.query(User).filter_by(Cookie=cookie)
    if user_query.count() > 0:
        user = user_query.first()
        spinsLeft = user.Spinsleft
        if spinsLeft == 0:
            refreshTime = user.TimeLeft
            present = datetime.now()
            if refreshTime is not None and present > refreshTime:
                user_query.update({"Spinsleft": 3})
                user_query.update({"TimeLeft": None})
                session.commit()
        return user_query.first()

    return False

def logUserOut(cookie):
    session = Session()
    user_query = session.query(User).filter_by(Cookie=cookie)
    if user_query.count() > 0:
        user_query.update({"Cookie": ""})
        session.commit()

def isValidUser(username, password, cookie):
    session = Session()
    user_query = session.query(User).filter_by(Username=username)
    if user_query.count() != 0 and (user_query.first().Password == password):
            user_query.update({"Cookie": (cookie)})
            session.commit()
            return True

    return False

def registerUser(username, password, firstName, lastName, address, email, cookie, referral):
    session = Session()
    user_query = session.query(User).filter_by(Username=username)
    email_query = session.query(User).filter_by(Email=email)
    if(user_query.count() > 0 or email_query.count() > 0):
        return False

    spinsLeft = 3

    if len(referral) > 0:
        ref_user = session.query(User).filter_by(Username=referral)
        if ref_user.count > 0:
            ref_spins = ref_user.first().Spinsleft
            ref_spins += 10
            ref_user.update({'Spinsleft' : ref_spins})
            spinsLeft += 10


    new_user = User(Username=username, Email = email, Password=password, firstName = firstName, lastName = lastName, AdIndex = 0, Spinsleft = spinsLeft, Balance = 0.0, Cookie = cookie)
    session.add(new_user)
    session.commit()
    return True

def result(ang):
    bal_amounts = [0, 1.0, 0, 0, 0.05, 0.20, 0, 0, 0, 0.01, 0.10, 0]
    spins_amounts = [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0]

    picked = int((ang % 360)/36)

    return [bal_amounts[picked], spins_amounts[picked]]

def modifyBalance(cookie, amount, spins):
    session = Session()
    user_query = session.query(User).filter_by(Cookie=cookie)
    queried_user = user_query.first()
    spinsLeft = int(queried_user.Spinsleft);
    if(spinsLeft > 0):
        bal = float(queried_user.Balance)
        spinsLeft = spinsLeft - 1 + spins
        bal += amount
        user_query.update({'Spinsleft' : spinsLeft})
        user_query.update({'Balance' : bal})
        if spinsLeft == 0:
            user_query.update({'TimeLeft' : (datetime.now() + timedelta(hours=2))})

        session.commit()

def isWinner():
    winners = [45,75,105,195,225]
    losers = [15,135,165,255,285,345]

    my_list = winners * 100 + losers * 9900
    chosen = random.choice(my_list)

    return (chosen % 360) + 360

def send_email(message, subject, email):
    fromaddr = email
    toaddr = "gvarun92@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = toaddr
    msg['Subject'] = subject
    body = email + "\n\n" + message
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("gvarun92@gmail.com", "Jakevane#5")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)

def updateValueForUser(username, columnName, columnValue):
    session = Session()
    user_query = session.query(User).filter_by(Username=username)
    user_query.update({columnName : columnValue})
    session.commit()
