from django.shortcuts import render
from . utilities import load_data ,diabetes_prediction
import pandas as pd
from .models import contact_us_tbl , prediction_chart
from django.contrib import messages

# Create your views here.

def home(request):

    return render(request,"home.html") 

def dashboard(request):
    diabetes_df = load_data()



    test_positive = diabetes_df['class'].value_counts().Positive
    test_negative = diabetes_df['class'].value_counts().Negative    

    male_positive = diabetes_df[(diabetes_df['Gender']=='Male') & (diabetes_df['class']=='Positive')].shape[0]
    female_positive = diabetes_df[(diabetes_df['Gender']=='Female') & (diabetes_df['class']=='Positive')].shape[0]

    male_negative = diabetes_df[(diabetes_df['Gender']=='Male') & (diabetes_df['class']=='Negative')].shape[0]
    female_negative= diabetes_df[(diabetes_df['Gender']=='Female') & (diabetes_df['class']=='Negative')].shape[0]



    bins= [15,30,45,60,75]
    labels = ['15-30','30-45','45-60','60-75']
    diabetes_df['AgeGroup'] = pd.cut(diabetes_df['Age'], bins=bins, labels=labels, right=False)
    positive_group = diabetes_df[diabetes_df['class']=='Positive']
    negative_group = diabetes_df[diabetes_df['class']=='Negative']

    positive_group = positive_group.groupby('AgeGroup').size()
    negative_group = negative_group.groupby('AgeGroup').size()

    labels_groups = list(positive_group.index)
    positive_values_groups = list(positive_group.values)
    negative_values_groups = list(negative_group.values)

    chart_instance = prediction_chart.objects.all()[0]
    positive_count= 0
    negative_count= 0
    if (chart_instance):
        positive_count= chart_instance.positive
        negative_count= chart_instance.negative
    pred_chart = [positive_count,negative_count]



    
 


    context = {'test_result':[test_positive,test_negative],'gender_compare':[male_positive,female_positive,male_negative,female_negative],'groups':[labels_groups,positive_values_groups,negative_values_groups],'pred_chart':pred_chart}


    return render(request,"dashboard.html",context) 

def prediction(request):
    if request.method == "POST":
        gender= request.POST["gender"]
        age= request.POST["age"]
        Polyuria= request.POST["Polyuria"]
        Polydipsia= request.POST["Polydipsia"]
        sudden_weight_loss= request.POST["sudden_weight_loss"]
        weakness= request.POST["weakness"]
        Polyphagia= request.POST["Polyphagia"]
        Genital_thrush= request.POST["Genital_thrush"]
        visual_blurring= request.POST["visual_blurring"]
        Itching= request.POST["Itching"]
        Irritability= request.POST["Irritability"]
        delayed_healing= request.POST["delayed_healing"]
        partial_paresis= request.POST["partial_paresis"]
        muscle_stiffness= request.POST["muscle_stiffness"]
        Alopecia= request.POST["Alopecia"]
        Obesity= request.POST["Obesity"]
       
        result = diabetes_prediction(gender, age, Polyuria, Polydipsia , sudden_weight_loss,weakness,Polyphagia,Genital_thrush,visual_blurring,Itching,Irritability,delayed_healing,partial_paresis,muscle_stiffness,Alopecia,Obesity)
        result = result[0]

        chart_instances = prediction_chart.objects.all()
        if (len(chart_instances) < 1):
            if result == 'Positive':
                chart_object = prediction_chart(positive=1,negative=0)
                chart_object.save()
            else:
                chart_object = prediction_chart(positive=0,negative=1)
                chart_object.save() 
        else:
            chart_instance = prediction_chart.objects.all()[0]
            if result == 'Positive':
                chart_instance.positive += 1    
                chart_instance.save()
            else:
                chart_instance.negative += 1    
                chart_instance.save()

        print("result:" ,result)

        return render(request, 'prediction.html',{'result': result})

    return render(request,"prediction.html") 

def stay_healthy(request):

    return render(request,"stay_healthy.html") 

def about_us(request):

    return render(request,"about_us.html") 

def contact_us(request):
    if request.method == "POST":
        name= request.POST["name"]
        email= request.POST["email"]
        subject= request.POST["subject"]
        phone= request.POST["phone"]
        message= request.POST["message"]
        contact_object = contact_us_tbl(name=name,email=email,subject=subject,phone=phone,message=message)
        contact_object.save()
        messages.success(request, 'Form submission successful')


    return render(request,"contact_us.html") 