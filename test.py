import unittest
from unittest.mock import patch, Mock
from main import (get_words_by_topic, clean_topic_input,
                          determine_topics, create_sentence, generate_paragraphs)

class TestEassyPyAI(unittest.TestCase):

    @patch('main.requests.get')
    def test_get_words_by_topic_success(self, mock_get):
        # Mock the API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{'word': 'example1'}, {'word': 'example2'}]
        mock_get.return_value = mock_response

        result = get_words_by_topic('test')
        self.assertEqual(result, ['example1', 'example2'])
        mock_get.assert_called_once_with('https://api.datamuse.com/words', params={'ml': 'test'})

    @patch('main.requests.get')
    def test_get_words_by_topic_failure(self, mock_get):
        # Mock a failed response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = get_words_by_topic('test')
        self.assertEqual(result, [])
        mock_get.assert_called_once_with('https://api.datamuse.com/words', params={'ml': 'test'})

    def test_clean_topic_input(self):
        result = clean_topic_input("This is a test sentence for the topic.")
        self.assertEqual(result, ['this', 'test', 'sentence', 'topic.'])

    @patch('main.requests.get')
    def test_determine_topics_success(self, mock_get):
        # Mock the API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{'word': 'topic1'}, {'word': 'topic2'}]
        mock_get.return_value = mock_response

        result = determine_topics(['word1', 'word2'])
        self.assertIn('topic1', result)
        self.assertIn('topic2', result)

    @patch('main.requests.get')
    def test_determine_topics_failure(self, mock_get):
        # Mock a failed response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = determine_topics(['word1', 'word2'])
        self.assertEqual(result, [])

    @patch('main.get_words_by_topic')
    @patch('main.random.choice')
    def test_create_sentence(self, mock_random_choice, mock_get_words_by_topic):
        # Mocking words returned by the get_words_by_topic
        mock_get_words_by_topic.side_effect = [
            ['cat', 'dog'],  # Nouns
            ['runs'],       # Verbs
            ['happy'],      # Adjectives
            ['quickly']     # Adverbs
        ]
        mock_random_choice.side_effect = ['happy', 'cat', 'dog', 'runs', 'quickly']
        
        result = create_sentence('animal')
        self.assertTrue(result.endswith('.'))  # Check if the sentence ends with a period

    @patch('main.random.randint')
    @patch('main.create_sentence')
    @patch('main.get_words_by_topic')
    def test_generate_paragraphs(self, mock_get_words_by_topic, mock_create_sentence, mock_randint):
        mock_get_words_by_topic.return_value = ['topic']
        mock_create_sentence.side_effect = ['Sentence 1.', 'Sentence 2.']
        mock_randint.side_effect = [2, 3]  # 2 to 3 sentences

        result = generate_paragraphs(['topic'], num_paragraphs=1)
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0].startswith('Sentence'))

if __name__ == '__main__':
    unittest.main()
