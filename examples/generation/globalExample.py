from textblob import TextBlob


def analyse_sentiment(text: str):
    blob = TextBlob(text)
    senti = blob.sentiment
    return f"Polarity: {round(senti.polarity,3)} <br /> Subjectivity: {round(senti.subjectivity,3)}"
