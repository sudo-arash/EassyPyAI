# README for EasyPy AI

## Overview

**EasyPy AI** is a Python application that generates paragraphs based on user-defined topics. By using the Datamuse API, it fetches related words and constructs meaningful(sometimes) sentences, allowing for creative text generation on various subjects.

## Features

- Fetches words related to a given topic using the Datamuse API.
- Cleans user input by removing common stop words.
- Analyzes and determines relevant topics from the input.
- Generates structured sentences with specified grammatical rules.
- Outputs a set number of paragraphs containing sentences related to identified topics.

## Requirements

To run this application, ensure you have the following:

- Python 3.x
- `requests` library (install via `pip install requests`)

## Installation

1. Clone the repository or download the script file.
2. Install the required dependencies:
   ```bash
   pip install requests
   ```

## Usage

1. Run the script:
   ```bash
   python main.py
   ```

2. When prompted, enter a topic:
   ```
   Enter a topic: Your chosen topic here
   ```

3. The application will:
   - Clean the input by removing stop words.
   - Identify related topics using the Datamuse API.
   - Generate and display paragraphs based on the identified topics.

## Functions

- `get_words_by_topic(topic_word, part_of_speech=None)`: Fetches words related to a topic, optionally filtered by part of speech (noun, verb, adjective, or adverb).

- `clean_topic_input(topic_sentence)`: Cleans the input sentence by removing common stop words and splitting it into meaningful words.

- `determine_topics(words)`: Analyzes filtered words to identify related topics using the Datamuse API.

- `create_sentence(topic)`: Constructs a structured sentence from related words (2 nouns, 1 verb, up to 2 adjectives, and 1 adverb).

- `generate_paragraphs(topics, num_paragraphs=5)`: Generates a specified number of paragraphs by creating sentences based on selected topics.

- `main()`: The entry point of the application, handling user interaction and invoking other functions.

## Logging

The application uses Python's built-in logging module to provide detailed logs at various levels (DEBUG, INFO, WARNING, ERROR). Logs are outputted in the console and include timestamps.

## Example

When the user inputs a topic, the application may generate paragraphs like the following:

```
Generated paragraphs:

Paragraph 1:
The beautiful entity acts quickly. The lovely object does its task carefully.

Paragraph 2:
The strange thing moves gracefully. The amazing creature acts swiftly.
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Thanks to the [Datamuse API](https://www.datamuse.com/api/) for providing the word-fetching capabilities.
- Special thanks to the Python community for their ongoing support and contributions.
