import pytest
import requests
from unittest.mock import patch
from main import (
    clean_topic_input, determine_topics, fetch_api_data,
    is_word_related_to_topic, get_words_by_topic, nlp_based_sentence,
    create_sentence, generate_paragraphs
)

DATAMUSE_API = "https://api.datamuse.com/words"
STOP_WORDS = {"the", "a", "an", "and", "of", "in", "on", "at", "to", "is", "for"}


@pytest.fixture
def mock_requests_get():
    """Fixture to mock requests.get."""
    with patch("requests.get") as mock_get:
        yield mock_get


def test_clean_topic_input():
    sentence = "The quick brown fox jumps over the lazy dog"
    result = clean_topic_input(sentence)
    assert result == ["quick", "brown", "fox", "jumps", "over", "lazy", "dog"]


def test_fetch_api_data(mock_requests_get):
    """Test fetching data from API."""
    mock_response_data = [{"word": "test"}]
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = mock_response_data

    result = fetch_api_data({"rel_trg": "test"})
    assert result == mock_response_data
    mock_requests_get.assert_called_once_with(DATAMUSE_API, params={"rel_trg": "test"})


def test_determine_topics(mock_requests_get):
    """Test determining topics with and without threads."""
    mock_response_data = [{"word": "related"}]
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = mock_response_data

    words = ["apple", "banana"]
    
    # Test without threading
    result = determine_topics(words, use_threads=False)
    assert "related" in result
    
    # Test with threading
    result = determine_topics(words, use_threads=True)
    assert "related" in result


def test_is_word_related_to_topic(mock_requests_get):
    """Test checking if a word is related to a topic."""
    mock_response_data = [{"word": "related"}]
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = mock_response_data

    result = is_word_related_to_topic("test", "related")
    assert result is True


def test_get_words_by_topic(mock_requests_get):
    """Test fetching words by topic."""
    mock_response_data = [{"word": "related"}]
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = mock_response_data

    result = get_words_by_topic("test", part_of_speech="n", max_words=5)
    assert result == ["related"]


@patch("main.nlp", autospec=True)
def test_nlp_based_sentence(mock_nlp, mock_requests_get):
    """Test generating an NLP-based sentence."""
    mock_nlp.return_value = [{"pos_": "NOUN", "text": "[NOUN]"}, {"pos_": "VERB", "text": "[VERB]"}]
    mock_response_data = [{"word": "test"}, {"word": "run"}]
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = mock_response_data

    result = nlp_based_sentence("The [ADJ] [NOUN] [VERB] the [NOUN] [ADV].", "test")
    assert isinstance(result, str)


def test_create_sentence(mock_requests_get):
    """Test creating a sentence based on NLP."""
    mock_response_data = [{"word": "related"}]
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = mock_response_data

    result = create_sentence("test", use_threads=False)
    assert isinstance(result, str)


def test_generate_paragraphs(mock_requests_get):
    """Test generating paragraphs."""
    mock_response_data = [{"word": "related"}]
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = mock_response_data

    topics = ["apple", "banana"]
    result = generate_paragraphs(topics, num_paragraphs=2, use_threads=False)
    assert len(result) == 2
    assert all(isinstance(p, str) for p in result)
