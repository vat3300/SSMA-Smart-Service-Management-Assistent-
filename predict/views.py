from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SearchForm
import requests
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from .models import PredResults
from django.http import JsonResponse
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response


def Home(request):
    form = SearchForm(request.POST or None)
    response = None
    response1 = None
    response2 = None

    if form.is_valid():
        value = form.cleaned_data.get("q")

        df = pd.read_csv('all_tickets.csv')
        df.drop('business_service',axis=1, inplace=True)
        X = df['body']
        y = df['ticket_type']
        cv = CountVectorizer()
        X = cv.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
        clf = MultinomialNB()
        clf.fit(X_train,y_train)

        message = value
        data = [message]
        vect = cv.transform(data).toarray()
        my_prediction = clf.predict(vect)

        if(my_prediction== 1):
            print("Ticket-Type: Request")
            response = "Request"
        else:
            print("Ticket-Type: Incident")
            response = "Incident"

        df = pd.read_csv('all_tickets.csv')
        df.drop('business_service', axis=1, inplace=True)
        X1 = df['body']
        y1 = df['category']
        cv = CountVectorizer()
        X1 = cv.fit_transform(X1)
        X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y1, test_size=0.33, random_state=42)
        clf1 = MultinomialNB()
        clf1.fit(X1_train, y1_train)

        message = value
        data = [message]
        vect = cv.transform(data).toarray()
        my_prediction1 = clf1.predict(vect)

        if (my_prediction1 == 1):
            print("Department: Facilities")
            response1 = "Facilities"
        elif (my_prediction1 == 2):
            print("Department: Web")
            response1 = "Web"
        elif (my_prediction1 == 3):
            print("Department: Bug")
            response1 = "Bug"
        elif (my_prediction1 == 4):
            print("Department: Application Support")
            response1 = "Application Support"
        elif (my_prediction1 == 5):
            print("Department: Hardware")
            response1 = "Hardware"
        elif (my_prediction1 == 6):
            print("Department: Connectivity")
            response1 = "Connectivity"
        elif (my_prediction1 == 7):
            print("Department: Admin and Access")
            response1 = "Admin and Access"
        elif (my_prediction1 == 8):
            print("Department: Support")
            response1 = "Support"
        elif (my_prediction1 == 9):
            print("Department: General Account Update")
            response1 = "General Account Update"
        elif (my_prediction1 == 10):
            print("Department: Server Hardware")
            response1 = "Server Hardware"
        elif (my_prediction1 == 11):
            print("Department: Software")
            response1 = "Software"
        else:
            print("Department: IT Services")
            response1 = "IT Services"

        df = pd.read_csv('all_tickets.csv')
        df.drop('business_service', axis=1, inplace=True)
        X2 = df['body']
        y2 = df['urgency']
        cv = CountVectorizer()
        X2 = cv.fit_transform(X2)
        X2_train, X2_test, y2_train, y2_test = train_test_split(X2, y2, test_size=0.33, random_state=42)
        clf2 = MultinomialNB()
        clf2.fit(X2_train, y2_train)

        message = value
        data = [message]
        vect = cv.transform(data).toarray()
        my_prediction2 = clf2.predict(vect)

        if (my_prediction2 == 0):
            print("Severity: Urgent")
            response2 = "Urgent"
        elif (my_prediction2 == 1):
            print("Severity: High")
            response2 = "High"
        elif (my_prediction2 == 2):
            print("Severity: Moderate")
            response2 = "Moderate"
        else:
            print("Severity: Low")
            response2 = "Low"

        data = {"message": message, "response": response,"response1": response1,"response2":response2}

        PredResults.objects.create(message=message,response=response,response1=response1,response2=response2)
        return render(request, 'result.html', data )
    return render(request, 'index.html', {"form": form})

def view_results(request):
    # Submit prediction and show all
    data = {"dataset": PredResults.objects.all()}
    return render(request, "show.html", data)

def destroy(request, id):
    uid = PredResults.objects.get(id=id)
    uid.delete()
    return redirect("/results")