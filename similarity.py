import glob
import csv

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def find_similar(tfidf_matrix, index, top_n = 5):
    cosine_similarities = linear_kernel(tfidf_matrix[index:index+1], tfidf_matrix).flatten()
    related_docs_indices = [i for i in cosine_similarities.argsort()[::-1] if i != index]
    return [(index, cosine_similarities[index]) for index in related_docs_indices][0:top_n]

corpus = []
for file in glob.glob("papers/*.txt"):
    with open(file, "r") as paper:
        corpus.append((file, paper.read()))

tf = TfidfVectorizer(analyzer='word', ngram_range=(1,3), min_df = 0, stop_words = 'english')
tfidf_matrix =  tf.fit_transform([content for file, content in corpus])

with open("similarities.csv", "w") as similarities_file:
    writer = csv.writer(similarities_file, delimiter = ",")

    for me_index, item in enumerate(corpus):
        similar_documents =  [(corpus[index], score) for index, score in find_similar(tfidf_matrix, me_index)]
        me = corpus[me_index]

        document_id = me[0].split("/")[1].split(".")[0]

        for ((raw_similar_document_id, title), score) in similar_documents:
            similar_document_id = raw_similar_document_id.split("/")[1].split(".")[0]
            writer.writerow([document_id, me[1], similar_document_id, title, score])
