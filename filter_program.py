import json
import config
import nltk
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

stemmer = PorterStemmer()

def stem_text(text):
    words = nltk.word_tokenize(text.lower())
    stemmed = [stemmer.stem(word) for word in words]
    return " ".join(stemmed)

def stem_keywords(keywords):
    return [stemmer.stem(word.lower()) for word in keywords]

def filter_metadata(index):
    with open("video_metadata.json", "r", encoding="utf-8") as f:
        videos = json.load(f)

    stemmed_keywords = stem_keywords(config.keywords[index])

    matching_indexes = []
    for idx, video in enumerate(videos):
        title = video.get("title", "")
        description = video.get("description", "")
        combined_text = f"{title} {description}"

        stemmed_text_result = stem_text(combined_text)

        if any(kw in stemmed_text_result for kw in stemmed_keywords):
            matching_indexes.append(idx)

    print("Output indices:", matching_indexes)
    print(str(len(matching_indexes)) + f"/{len(videos)}")
    return matching_indexes

def filter_metadata_old(index):
    with open("video_metadata.json", "r", encoding="utf-8") as f:
        videos = json.load(f)

    matching_indexes = []
    for idx, video in enumerate(videos):
        title = video.get("title", "").lower()
        description = video.get("description", "").lower()
        combined_text = f"{title} {description}"

        if any(keyword in combined_text for keyword in config.keywords[index]):
            matching_indexes.append(idx)

    print("Output indices:", matching_indexes)
    print(str(len(matching_indexes)) + "/15")
    return matching_indexes

'''
    Filter dát s metódou váženého slovníka - Použitý pri našich výsledkoch
    index: určuje tému relevancie
    treshold: hodnota, ktorú potrebuje prekročiť, aby považoval video za relevantné
'''
def filter_weighted_matching(index, threshold=5):
    with open("video_metadata.json", "r", encoding="utf-8") as f:
        videos = json.load(f)

    important_words = config.keyword_weights[index]
    weighted_keywords = {stemmer.stem(word.lower()): weight for word, weight in important_words.items()}

    matching_indexes = []
    for idx, video in enumerate(videos):
        title = video.get("title", "")
        stemmed_title = nltk.word_tokenize(title.lower())
        stemmed_title = [stemmer.stem(word) for word in stemmed_title]

        description = video.get("description", "")
        stemmed_description = nltk.word_tokenize(description.lower())
        stemmed_description = [stemmer.stem(word) for word in stemmed_description]

        score = sum(weighted_keywords.get(word, 0) for word in stemmed_title)
        score_description = sum(weighted_keywords.get(word, 0) for word in stemmed_description)
        if score_description < 5 : score += score_description
        elif score > 3 : score += 4

        if score >= threshold:
            matching_indexes.append(idx)

    print("Weighted matching indices:", matching_indexes)
    print(str(len(matching_indexes)) + f"/{len(videos)}")
    return matching_indexes


def run_filter(method_name, index=0):
    if method_name == "basic":
        return filter_metadata(index)
    elif method_name == "old":
        return filter_metadata_old(index)
    elif method_name == "weighted":
        return filter_weighted_matching(index)
    else:
        raise ValueError(f"Unknown filter method: {method_name}")
