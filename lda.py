from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk
from gensim.models import Phrases
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from pprint import pprint
import sys

def get_docs(path):
    """Gets documents from text file
       Returns list of documents
    """
    docs= []
    file = open(path, "r")
    for line in file:
        if "bush" in line.lower() or "gore" in line.lower():
            docs.append(line)
    file.close()
    return docs


def tokenize(docs):
    new_docs = docs
    # Split the documents into tokens.
    tokenizer = RegexpTokenizer(r'\w+')
    for idx in range(len(docs)):
        new_docs[idx] = new_docs[idx].lower()  # Convert to lowercase.
        new_docs[idx] = tokenizer.tokenize(new_docs[idx])  # Split into words.

    # Remove numbers, but not words that contain numbers.
    new_docs = [[token for token in doc if not token.isnumeric()] for doc in new_docs]

    # Remove words that are 2 or less characters.
    new_docs = [[token for token in doc if len(token) > 2] for doc in new_docs]

    # Remove stop words
    # nltk.download('stopwords') REMOVE COMMENT IF NEEDING TO DOWNLOAD
    stop_words = set(stopwords.words('english'))
    new_docs = [[token for token in doc if not token in stop_words] for doc in new_docs]

    # Lemmatize the documents.
    # nltk.download('wordnet') REMOVE COMMENT IF NEEDING TO DOWNLOAD
    lemmatizer = WordNetLemmatizer()
    new_docs = [[lemmatizer.lemmatize(token) for token in doc] for doc in new_docs]

    return new_docs



if __name__ == "__main__":
    print("Building corpus...")
    # Load in data
    docs = get_docs("./data/nyt_filtered_election_docs")

    # Tokenize docs
    docs = tokenize(docs)

    # Add bigrams to docs (only ones that appear 10 times or more).
    bigram = Phrases(docs, min_count=10)
    for idx in range(len(docs)):
        for token in bigram[docs[idx]]:
            if '_' in token:
                # Token is a bigram, add to document.
                docs[idx].append(token)
    # Create a dictionary representation of the documents.
    dictionary = Dictionary(docs)

    # Filter out words that occur less than 1% of documents, or more than 50% of the documents.
    dictionary.filter_extremes(no_below=0.01, no_above=0.5)

    # Bag-of-words representation of the documents.
    corpus = [dictionary.doc2bow(doc) for doc in docs]

    print("Dictionary size: " + str(len(dictionary)))
    print("Corpus size: " + str(len(corpus)))

    model = None

    # Set training parameters.
    num_topics = 10
    chunksize = 2000
    passes = 10
    iterations = 100
    eval_every = None  # Don't evaluate model perplexity, takes too much time.

    if sys.argv[1:]:
        arg1 = sys.argv[1].strip()
        if arg1 == 'train':
            print("Training new model...")

            # Make a index to word dictionary.
            temp = dictionary[0] # This is only to "load" the dictionary.
            id2word = dictionary.id2token

            model = LdaModel(
                corpus=corpus,
                id2word=id2word,
                chunksize=chunksize,
                alpha='auto',
                eta='auto',
                iterations=iterations,
                num_topics=num_topics,
                passes=passes,
                eval_every=eval_every
            )

            model.save('./model/lda_model')

        else:
            print("Loading model...")
            model = LdaModel.load('./model/lda_model')
    else:
        print("Loading model...")
        model = LdaModel.load('./model/lda_model')

    top_topics = model.top_topics(corpus) #, num_words=20)

    # Average topic coherence is the sum of topic coherences of all topics, divided by the number of topics.
    avg_topic_coherence = sum([t[1] for t in top_topics]) / num_topics
    #print('Average topic coherence: %.4f.' % avg_topic_coherence)
    #print("\n")
    #pprint(top_topics)
    pprint(model.show_topics(num_topics = 10, num_words = 3))
