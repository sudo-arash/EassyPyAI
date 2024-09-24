import requests
import random
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# API URLs for Datamuse
DATAMUSE_API = "https://api.datamuse.com/words"
STOP_WORDS = {"the", "a", "an", "and", "of", "in", "on", "at", "to", "is", "for"}

def get_words_by_topic(topic_word, part_of_speech=None):
    """Fetch words related to a given topic word using Datamuse API, optionally filtered by part of speech."""
    logging.info(f"Fetching related {part_of_speech or 'words'} for topic: {topic_word}")

    params = {"ml": topic_word}
    if part_of_speech:
        params["sp"] = f"*{part_of_speech}"

    response = requests.get(DATAMUSE_API, params=params)

    if response.status_code == 200:
        data = response.json()
        words = [item['word'] for item in data if 'word' in item]
        logging.debug(f"Received {len(words)} {part_of_speech or 'words'} related to {topic_word}")
        return words
    else:
        logging.error(f"Failed to fetch related words for {topic_word}. Status code: {response.status_code}")
        return []

def clean_topic_input(topic_sentence):
    """Remove stop words and split input sentence into meaningful words."""
    logging.info("Cleaning input sentence.")
    words = topic_sentence.lower().split()
    filtered_words = [word for word in words if word not in STOP_WORDS]
    logging.debug(f"Filtered words: {filtered_words}")
    return filtered_words

def determine_topics(words):
    """Analyze the topics of filtered words using the Datamuse API."""
    topics = set()

    for word in words:
        # Make the API call to get related topics from Datamuse
        try:
            logging.info(f"Fetching topics for word: {word}")
            response = requests.get(f"{DATAMUSE_API}?rel_trg={word}")
            if response.status_code == 200:
                data = response.json()
                topics.update([item['word'] for item in data])
                logging.debug(f"Related topics found for {word}: {[item['word'] for item in data]}")
            else:
                logging.warning(f"Datamuse API error for word: {word}. Status code: {response.status_code}")
        except Exception as e:
            logging.error(f"Error fetching topics for {word}: {e}")

    return list(topics)  # Return a list of unique topics

def create_sentence(topic):
    """Form a sentence from related words with a specific structure: 2 nouns, 1 verb, 2 adjectives (optional), 1 adverb."""

    # Fetch at least 2 nouns, 1 verb, 2 adjectives (optional), and 1 adverb related to the topic
    nouns = get_words_by_topic(topic, 'n') or ['thing']
    verbs = get_words_by_topic(topic, 'v') or ['does']
    adjectives = get_words_by_topic(topic, 'adj') or []
    adverbs = get_words_by_topic(topic, 'adv') or ['']

    if len(nouns) < 2:
        logging.warning(f"Not enough nouns for {topic}, filling with defaults.")
        nouns.extend(['object', 'entity'])

    if not verbs:
        logging.warning(f"No verbs found for {topic}, filling with default.")
        verbs.append('acts')

    # Select 2 nouns, 1 verb, up to 2 adjectives, and 1 adverb to form a structured sentence
    chosen_nouns = random.choices(nouns, k=2)
    chosen_verb = random.choice(verbs)
    chosen_adjectives = random.choices(adjectives, k=min(2, len(adjectives)))
    chosen_adverb = random.choice(adverbs)

    # Construct the sentence
    sentence = f"{chosen_adjectives[0] if chosen_adjectives else ''} {chosen_nouns[0]} {chosen_adjectives[1] if len(chosen_adjectives) > 1 else ''} {chosen_verb} {chosen_nouns[1]} {chosen_adverb}."
    sentence = " ".join(sentence.split())  # Clean up any extra spaces
    logging.debug(f"Generated sentence: {sentence}")

    return sentence.capitalize()

def generate_paragraphs(topics, num_paragraphs=5):
    """Generate paragraphs by fetching related words for each topic and forming sentences."""
    paragraphs = []

    logging.info(f"Generating {num_paragraphs} paragraphs.")
    for _ in range(num_paragraphs):
        paragraph = []
        selected_topic = topics[random.randint(0, len(topics)-1)]
        logging.info(f"Generating sentences for topic: {selected_topic}")
        for _ in range(random.randint(2, 3)):  # 2 to 3 sentences per paragraph
            paragraph.append(create_sentence(selected_topic))
        paragraphs.append(" ".join(paragraph))  # Join sentences into a paragraph
    return paragraphs

def main():
    print("""
        dGGGGMMb     ,"""""""""""""".
       @p~qp~~qMb    |  EassyPy AI  |
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
    topics = determine_topics(filtered_words)

    if not topics:
        logging.warning("No valid topics found. Please enter a valid input.")
        return

    logging.info(f"Identified topics: {topics}")

    # Step 3: Generate paragraphs based on the topics
    paragraphs = generate_paragraphs(topics)

    # Step 4: Output the generated paragraphs
    logging.info("Generated paragraphs successfully.")
    print("\nGenerated paragraphs:\n")
    for i, paragraph in enumerate(paragraphs, start=1):
        print(f"Paragraph {i}:\n{paragraph}\n")

if __name__ == "__main__":
    main()
