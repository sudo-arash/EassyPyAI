import spacy
import requests
import random
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import nltk

# Load the NLP model
nlp = spacy.load("en_core_web_lg")
nltk.download("punkt")

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

DATAMUSE_API = "https://api.datamuse.com/words"
STOP_WORDS = {"the", "a", "an", "and", "of", "in", "on", "at", "to", "is", "for"}

def fetch_api_data(params):
    """Helper function to fetch data from the Datamuse API."""
    response = requests.get(DATAMUSE_API, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"API request failed with status code {response.status_code}.")
        return []

def clean_topic_input(topic_sentence):
    """Remove stop words and split input sentence into meaningful words."""
    logging.info("Cleaning input sentence.")
    words = topic_sentence.lower().split()
    filtered_words = [word for word in words if word not in STOP_WORDS]
    logging.debug(f"Filtered words: {filtered_words}")
    return filtered_words

def determine_topics(words, use_threads=False):
    """Analyze the topics of filtered words using the Datamuse API."""
    topics = set()

    if use_threads:
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(fetch_api_data, {"rel_trg": word}) for word in words]
            for future in as_completed(futures):
                data = future.result()
                topics.update([item['word'] for item in data])
    else:
        for word in words:
            logging.info(f"Fetching topics for word: {word}")
            response = requests.get(f"{DATAMUSE_API}?rel_trg={word}")
            if response.status_code == 200:
                data = response.json()
                topics.update([item['word'] for item in data])
                logging.debug(f"Related topics found for {word}: {[item['word'] for item in data]}")
            else:
                logging.warning(f"Datamuse API error for word: {word}. Status code: {response.status_code}")

    return list(topics)

def is_word_related_to_topic(word, topic):
    """Check if the word is closely related to the given topic."""
    logging.info(f"Checking if word '{word}' is related to topic '{topic}'")
    response = requests.get(f"{DATAMUSE_API}?ml={topic}&max=10")
    if response.status_code == 200:
        related_words = [item['word'] for item in response.json()]
        return word in related_words
    return False

def get_words_by_topic(topic_word, part_of_speech=None, max_words=10, use_threads=False):
    """Fetch a limited number of words related to a given topic word using Datamuse API, optionally filtered by part of speech."""
    logging.info(f"Fetching related {part_of_speech or 'words'} for topic: {topic_word}")

    params = {"ml": topic_word, "max": max_words}
    if part_of_speech:
        params["sp"] = f"*{part_of_speech}"

    if use_threads:
        with ThreadPoolExecutor() as executor:
            future = executor.submit(fetch_api_data, params)
            return [item['word'] for item in future.result() if 'word' in item]

    # Sequential fetch (default)
    response = requests.get(DATAMUSE_API, params=params)
    if response.status_code == 200:
        return [item['word'] for item in response.json() if 'word' in item]
    else:
        logging.error(f"Failed to fetch related words for {topic_word}. Status code: {response.status_code}")
        return []

def nlp_based_sentence(template_sentence, topic):
    """
    Improve sentence structure using NLP.
    - Use Spacy for parsing and replacing with more natural words.
    - Fill sentence templates more intelligently.
    """
    doc = nlp(template_sentence)
    logging.debug(f"Original Sentence Structure: {[token.text for token in doc]}")

    # Create a dictionary of POS -> words from Datamuse API
    pos_map = {
        "NOUN": get_words_by_topic(topic, 'n', max_words=10),
        "VERB": get_words_by_topic(topic, 'v', max_words=5),
        "ADJ": get_words_by_topic(topic, 'adj', max_words=5),
        "ADV": get_words_by_topic(topic, 'adv', max_words=5)
    }

    # Default fallback words
    pos_fallback = {
        "NOUN": ["thing", "object", "item"],
        "VERB": ["does", "is"],
        "ADJ": ["nice", "good"],
        "ADV": ["quickly"]
    }

    # Construct the sentence by replacing each part of speech
    generated_sentence = []
    for token in doc:
        if token.pos_ in pos_map and pos_map[token.pos_] and pos_map[token.pos_]:
            generated_sentence.append(pos_map[token.pos_].pop(0))  # Sequential selection
        else:
            generated_sentence.append(token.text)  # Keep the original if no word is available

    final_sentence = " ".join(generated_sentence)
    logging.debug(f"Generated NLP Sentence: {final_sentence}")
    return final_sentence.capitalize()

def create_sentence(topic, use_threads=False):
    """
    Form a sentence using NLP techniques to make it more natural.
    Structure: 2 nouns, 1 verb, 2 adjectives, 1 adverb.
    """
    # Template sentence to be modified by NLP
    template_sentence = "The [ADJ] [NOUN] [VERB] the [NOUN] [ADV]."

    # Use NLP to parse and replace placeholders with more natural words
    return nlp_based_sentence(template_sentence, topic)

def generate_paragraphs(topics, num_paragraphs=5, use_threads=False):
    """Generate paragraphs by fetching related words for each topic and forming sentences."""
    paragraphs = []
    logging.info(f"Generating {num_paragraphs} paragraphs.")

    for _ in range(num_paragraphs):
        paragraph = []
        selected_topic = topics[random.randint(0, len(topics)-1)]
        logging.info(f"Generating sentences for topic: {selected_topic}")

        for _ in range(2):  # Fixed at 2 sentences per paragraph
            paragraph.append(create_sentence(selected_topic, use_threads=use_threads))

        paragraphs.append(" ".join(paragraph))
    return paragraphs

def main():
    print("""
        dGGGGMMb     ,"""""""""""""".
       @p~qp~~qMb    |  EssayPy AI  |
       M|@||@) M|   _;..............'
       @,----.JM| -'
      JS^\__/  qKL
     dZP        qKRb
    dZP          qKKb
   fZP            SMMb
   HZM            MMMM
   FqM            MMMM
 __| ".        |\dS"qML
 |    `.       | `' \Zq
_)      \.___.,|     .'
\____   )MMMMMM|   .'
     `-'       `--' hjm
    """)

    # Get user input for the topic sentence
    user_input = input("Enter a topic: ")

    # Step 1: Clean the input by removing stop words (articles, conjunctions, etc.)
    filtered_words = clean_topic_input(user_input)

    # Step 2: Determine topics from the filtered words
    use_threads = input("Do you want to use threads to speed up (yes/no)? ").lower() == "yes"
    topics = determine_topics(filtered_words, use_threads=use_threads)

    if not topics:
        logging.warning("No valid topics found. Please enter a valid input.")
        return

    logging.info(f"Identified topics: {topics}")

    # Step 3: Generate paragraphs based on the topics
    paragraphs = generate_paragraphs(topics, use_threads=use_threads)

    # Step 4: Output the generated paragraphs
    logging.info("Generated paragraphs successfully.")
    print("\nGenerated paragraphs:\n")
    for i, paragraph in enumerate(paragraphs, start=1):
        print(f"Paragraph {i}:\n{paragraph}\n")

if __name__ == "__main__":
    main()
