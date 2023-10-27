from wash_kitty import wash_kitty
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_similarity(file1, file2):
    content1 = open(file1, "r").read()
    content2 = open(file2, "r").read()
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([content1, content2])
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix).flatten()
    return cosine_similarities[1]


def kitty_distance(p1, p2, f1, f2):
    wash_kitty(p1, f1)
    wash_kitty(p2, f2)
    return compute_similarity(f1, f2)


if __name__ == "__main__":
    project1 = "/Users/cong.zhang/dev/autobuild/tests/testcases/2023-08-chainlink"
    project2 = "/Users/cong.zhang/dev/autobuild/tests/testcases/2023-09-Maia"
    result1 = "./result1.txt"
    result2 = "./result2.txt"
    similarity = kitty_distance(project1, project2, result1, result2)
    print(similarity)
