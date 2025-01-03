import os

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tqdm import tqdm

nltk.download('punkt')
nltk.download('stopwords')


def process_file(file_path, language='en'):
    # Read and process the content of a file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Strip whitespace and join lines into a single text
    lines = [line.strip() for line in lines]
    text = ' '.join(lines)

    # Get the stopwords for the specified language
    stop_words = get_stopwords(language)

    # Tokenize the text into individual words
    word_tokens = word_tokenize(text)

    # Filter the tokens: keep only alphabetic words not in stopwords and convert to lowercase
    filtered_text = [word.lower() for word in word_tokens if word not in stop_words and word.isalpha()]
    
    # Join the filtered words with a single space
    return ' '.join(filtered_text)


def get_stopwords(language):
    # Map language codes to their respective stopword sets
    language_map = {
        'es': 'spanish',
        'gr': 'german',
        'fr': 'french',
        'fi': 'finnish',
        'hu': 'hungarian',
        'du': 'dutch',
        'en': 'english',
        'it': 'italian'
    }

    # Retrieve the stopwords for the given language or default to English
    stop_words = set(stopwords.words(language_map.get(language, 'english')))
    return stop_words


def main():
    # Directory containing raw book files
    original_books_dir = '../books/original_books/'
    for filename in tqdm(os.listdir(original_books_dir)):
        if filename.endswith('.txt'):
            # Infer the language from the filename or default to English
            lang = filename.split('_')[0] if '_' in filename else 'en'

            # Process the file and write the filtered content to a new file
            processed_file = process_file(os.path.join(original_books_dir, filename), lang)
            with open(os.path.join('../books/processed_books', filename), 'w') as file:
                file.write(processed_file)


if __name__ == '__main__':
    main()