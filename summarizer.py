import os
import fire
import string
import chardet
from typing import Union
from heapq import nlargest
from langdetect import detect
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

# A frozenset containing the supported languages for text summarization.
LANG = frozenset(["en", "ru"])
# An integer specifying the maximum number of lines allowed in the buffer before summarizing the text.
BUFFER_LIMIT = 1000
# A frozenset containing the allowed file extensions for text summarization.
ALLOWED_FILE_EXTENTIONS = frozenset([".txt"])
# A float value between 0 and 1 representing the percentage of sentences to be included in the summary.
CONTENT_AMOUNT = 0.3


class Summarizer:
    """
    This class provides methods for text summarization using Luhn's Heuristic Method.
    """

    def __init__(self) -> None:
        pass

    def __select_stopword_lang(self, lang) -> str:
        """
        Selects the appropriate stopword language based on the input language.

        Parameters:
            lang (str): The language identifier.

        Returns:
            str: The corresponding stopword language.

        """
        languages = { 'ru' : 'russian',
                      'en' : 'english'}
        if lang not in languages.keys():
            return languages['en']
        return languages[lang]

    def __luhn_summarizer(self, text, num_sentences, lang: Union["en", "ru"]) -> str:
        """
        Generates a summary of the given text using Luhn's Heuristic Method.

        Parameters:
            text (str): The input text to be summarized.
            num_sentences (int): The desired number of sentences in the summary.
            lang (str): The language of the input text.

        Returns:
            str: The generated summary.

        Raises:
            NotImplementedError: If the language is not supported.

        """
        if lang not in LANG:
            raise NotImplementedError('Wrong language')

        # Preprocessing the text
        stopwords_lang = self.__select_stopword_lang(lang)
        sentences = sent_tokenize(text)
        stemmer = PorterStemmer()
        stop_words = list(stopwords.words(stopwords_lang))
        vectorizer = TfidfVectorizer(stop_words=stop_words, tokenizer=word_tokenize)

        # Calculating TF-IDF scores for the sentences
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            # Remove punctuation and convert to lowercase
            sentence = sentence.translate(str.maketrans('', '', string.punctuation)).lower()
            stemmed_sentence = ' '.join([stemmer.stem(word) for word in word_tokenize(sentence) if word.isalnum()])
            sentence_scores[i] = vectorizer.fit_transform([stemmed_sentence]).sum()

        # Selecting the most important sentences
        selected_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)

        # Joining the selected sentences to create the summary
        summary = ' '.join([sentences[i] for i in selected_sentences])
        return summary

    def __summary_file(self, file_path, lang, encoding) -> None:
        """
        Generates a summary file for the given input file.

        Parameters:
            file_path (str): The path to the input file.
            lang (str): The language of the input text.
            encoding (str): The encoding of the input file.

        Raises:
            NotImplementedError: If the language is not supported.

        """
        if lang not in LANG:
            raise NotImplementedError('Wrong language')
        # Open the input file
        with open(file_path, 'r', encoding=encoding) as file:
            # Open a new file to write the summary
            with open(file_path.replace('.txt', '_abstract.txt'), 'w', encoding=encoding) as summary_file:
                buffer = ""
                for line in file:
                    # Accumulate lines in the buffer
                    buffer += line

                    # Check if buffer size exceeds a threshold (e.g., 1000 lines)
                    if buffer.count('\n') > BUFFER_LIMIT:
                        # Preprocess and summarize the buffer
                        senences_amount = int(CONTENT_AMOUNT * buffer.count('\n'))
                        if senences_amount <= 0:
                            senences_amount = 1
                        summary = self.__luhn_summarizer(buffer, senences_amount, lang)

                        # Write the summary to the output file
                        summary_file.write(summary + '\n')

                        # Reset the buffer
                        buffer = ""

                # Process the remaining lines in the buffer
                if buffer:
                    # Preprocess and summarize the remaining buffer
                    senences_amount = int(CONTENT_AMOUNT * buffer.count('\n'))
                    if senences_amount <= 0:
                        senences_amount = 1
                    summary = self.__luhn_summarizer(buffer, senences_amount, lang)

                    # Write the summary to the output file
                    summary_file.write(summary + '\n')

    def __get_file_extension(self, file_path) -> str:
        """
        Retrieves the file extension from the given file path.

        Parameters:
            file_path (str): The path to the file.

        Returns:
            str: The file extension.

        """
        _, file_extension = os.path.splitext(file_path)
        return file_extension

    def __allowed_extenstion(self, file_path) -> bool:
        """
        Checks if the given file has an allowed extension.

        Parameters:
            file_path (str): The path to the file.

        Returns:
            bool: True if the extension is allowed, False otherwise.

        """
        extention = self.__get_file_extension(file_path)
        return extention in ALLOWED_FILE_EXTENTIONS

    def __get_message_lang(self, message) -> str:
        """
        Detects the language of the given text message.

        Parameters:
            message (str): The input text message.

        Returns:
            str: The detected language.

        """
        lang = detect(message)
        if lang not in LANG:
            lang = 'en'
        return lang

    def __get_message_encoding(self, message) -> str:
        """
        Detects the encoding of the given text message.

        Parameters:
            message (str): The input text message.

        Returns:
            str: The detected encoding.

        """
        return chardet.detect(message.encode())['encoding']

    def __get_first_line(self, file_path) -> str:
        """
        Retrieves the first line of the given file.

        Parameters:
            file_path (str): The path to the file.

        Returns:
            str: The first line of the file.

        """
        with open(file_path, 'rb') as file:
            for line in file:
                # Flag to track if the line has been successfully decoded
                decoded = False

                # Detect the encoding of the line
                result = chardet.detect(line)
                encoding = result['encoding']

                # List of encodings to try
                encodings_to_try = [encoding, 'utf-8', 'latin-1']

                for encoding_to_try in encodings_to_try:
                    try:
                        # Decode the line using the current encoding
                        decoded_line = line.decode(encoding_to_try)
                        decoded_line = decoded_line.strip()
                        decoded = True
                        if decoded_line:
                            return decoded_line

                    except UnicodeDecodeError:
                        print(f"Error decoding line in {encoding_to_try} encoding")

                # Check if the line was successfully decoded
                if not decoded:
                    # Handle the situation when none of the encodings worked
                    print("Unable to decode the line with any of the encodings")

    def process_file(self, file_path) -> None:
        """
        Processes the given file by generating a summary.

        Parameters:
            file_path (str): The path to the file.

        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"No file: {file_path}")

            if not self.__allowed_extenstion(file_path):
                raise ValueError("Wrong extenstion")
            line = self.__get_first_line(file_path)
            lang = self.__get_message_lang(line)
            encoding = self.__get_message_encoding(line)
            self.__summary_file(file_path, lang, encoding)
        except Exception as e:
            print(e)


class CliWrapper(object):
    """
    This class is a CLI (Command Line Interface) wrapper for the `KeywordSpotter` class.
    It allows the user to interact with the `KeywordSpotter` class using command line arguments.
    """

    def __init__(self) -> None:
        self.summarizer = Summarizer()

    def summarize(self, path='./files/es.txt') -> None:
        """
        Summarizes the text file at the specified path.

        Parameters:
            path (str): The path to the text file.

        """
        self.summarizer.process_file(path)


if __name__ == "__main__":
    """
    This block of code checks if the script is being run as the main program, and if it is,
    it creates an instance of the CliWrapper class and uses the Google's python-fire library
    to enable CLI commands.
    """
    fire.Fire(CliWrapper)