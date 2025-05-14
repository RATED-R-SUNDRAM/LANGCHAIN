import langchain 
print(langchain.__version__)

from sklearn.metrics.pairwise import cosine_similarity

a= [1,2,3]
b=[2,4,6]

print(cosine_similarity([a],[b])[0][0])