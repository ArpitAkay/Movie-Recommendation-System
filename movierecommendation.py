from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
df1=pd.read_csv('credits.csv')
print(df1.head())
print(df1.shape)
print(df1.info())
df2=pd.read_csv('movies.csv')
print(df2.head())
print(df2.shape)
print(df2.info())
df1.columns=['id', 'title', 'cast', 'crew']
df2=df2.merge(df1,on="id")
print(df2.head())
print(df2.shape)
print(df2.columns)
C= df2['vote_average'].mean()
print(C)
m= df2['vote_count'].quantile(0.9) #movies having vote count greater than 90% from the list will be taken
print(m)
lists_movies = df2.copy().loc[df2['vote_count'] >= m]
lists_movies.shape
def weighted_rating(x ,m=m, C=C):
    v = x['vote_count']
    R = x['vote_average']
    #Calculation based on the IMDB Formula(m=1838, c=6.09)
    return (v/(v+m) * R) + (m/(m+v) * C)
#define a new feature 'score' and calculate its value with 'weighted rating()'
lists_movies['score'] = lists_movies.apply(weighted_rating, axis=1)
print(lists_movies.head(3))
print(lists_movies.shape)
lists_movies=lists_movies.sort_values('score',ascending=False)
li=[]
for i in range(0,len(df2)):
    li.append(i)
df2["sno"]=li

def movieteller(title):
    tfidf=TfidfVectorizer(stop_words='english')

    #Replace NaN with an empty string
    df2['overview']=df2['overview'].fillna('')

    #construct the required TF-IDF matrix  by fitting and transforming the data
    tfidf_matrix = tfidf.fit_transform(df2['overview'])

    #Output the shape of fidf matrix
    print(tfidf_matrix.shape)
    cosine_sim = cosine_similarity(tfidf_matrix)
    indices = pd.Series(df2.index, index=df2['title_x'])
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))
    # Sort the movies based on the similarity scores
    sim_scores = sorted (sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]

    # Get the movie indices

    movie_indices = [i[0] for i in sim_scores]
    print(movie_indices)
    # Return the top 10 most similar movies
    l1=[]
    li=[]
    for i in range(0, len(movie_indices)):
        for j in range(0, len(df2)):
            if movie_indices[i]==df2.iloc[j][""]:
                li.append(df2.iloc[j]["original_title"])
                l1.append(df2.iloc[j]["overview"])
                break
    return li,l1
def popular_movies():
        l3=[]
        for i in range(0,10):
            l3.append(lists_movies.iloc[i]["original_title"])
        return l3

