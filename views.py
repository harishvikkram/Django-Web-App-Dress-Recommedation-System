from django.shortcuts import render
from django.http import HttpResponse

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

import os

from Dress_Recomm_Sys.models import dress_recomm

# Create your views here.

def home_func(request):
    return render(request,'Project.html')

def res(request):
    dress_l=[]
    dress_id_var=int(request.GET['dress_id'])
    num_recomm_var=int(request.GET['num_recomm'])
  
    

    print(os.getcwd())
    ds=pd.read_csv('Test_data.csv')    
    
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(ds['Description about the dress'])

    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    results = {}

    for idx, row in ds.iterrows():
        similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
        similar_items = [(cosine_similarities[idx][i], ds['Id'][i]) for i in similar_indices]

        results[row['Id']] = similar_items[1:]
    
    print('done!')


    def item(id):
        return ds.loc[ds['Id'] == id]['Description about the dress'].tolist()[0].split(' - ')[0]
    
    # Just reads the results out of the dictionary.
    def recommend(item_id, num):
        print("Recommending " + str(num) + " products similar to " + item(item_id) + "...")
        print("-------------------------------------------------------------------")
        recs = results[item_id][:num]
        
        for rec in recs:
            print("Recommended: " + item(rec[1]) + " (score:" + str(rec[0]) + ")")
            dress_l.append(item(rec[1]))
            t=dress_recomm(dress_name=item(rec[1]),cos_sim=float(rec[0]))
            t.save()
    recommend(dress_id_var,num_recomm_var)
    d={'dress_id':dress_l}
    print('Over')
    print(dress_l)

    dress=dress_recomm.objects.all()
    print(dress)

    return render(request,'Result.html',{'dress_dict':dress})

# Create your views here.
