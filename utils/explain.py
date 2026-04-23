def get_top_keywords(features, vectorizer, top_n=3):
    """
    Extract top keywords from the input features based on TF-IDF scores.
    """
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = features.toarray()[0]

    # Get indices of scores > 0, sorted by score in descending order
    sorted_indices = tfidf_scores.argsort()[::-1]
    keywords = [feature_names[i] for i in sorted_indices if tfidf_scores[i] > 0]

    return keywords[:top_n]
