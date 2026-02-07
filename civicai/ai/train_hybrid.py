"""Train and persist TF-IDF artifacts for CivicAI."""
import argparse
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--data', default='../data/bbmp_reddit_data.csv')
    p.add_argument('--out', default='../backend/models/tfidf.joblib')
    args = p.parse_args()

    df = pd.read_csv(args.data)
    vec = TfidfVectorizer(stop_words='english', ngram_range=(1,2))
    vec.fit(df['text'].astype(str).tolist())
    joblib.dump({'vectorizer': vec, 'data': df}, args.out)
    print('saved', args.out)


if __name__ == '__main__':
    main()
