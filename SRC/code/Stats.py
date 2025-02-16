import json
from pathlib import Path
from collections import Counter
from wordcloud import WordCloud
from typing import Union
from SRC.data import Data_dir
from loguru import logger

class Chat_statistics:
    
    def __init__(self, chat_path: Union[str, Path], save_path : Union[str, Path] = None):
        """
        Initializes the Stats class with chat data and stop words.
        Args:
            chat_path (Union[str, Path]): The path to the chat data file.
            save_path (Union[str, Path]): The path to save the processed data.
        Attributes:
            chat_data (dict): The loaded chat data from the chat_path file.
            stop_words (list): A list of stop words loaded from 'stop_words.txt'.
            stop_words_E (list): A list of English stop words loaded from 'stop_words_E.txt'.
        """
        logger.info("Initializing the Stats class")
        logger.info(f"Loading the chat data from {chat_path}")
        
        if save_path is None:
            
            self.save_path = chat_path.parent
        else:  
            self.save_path = Path(save_path)
        
        with open(chat_path, 'r') as file:
            self.chat_data = json.load(file)
            
        with open(Data_dir/'stop_words.txt', 'r') as f:
            self.stop_words = f.read().splitlines()
            
        with open(Data_dir/'stop_words_E.txt', 'r') as f:
            self.stop_words_E = f.read().splitlines()
                
        
    def generate_word_cloud(self):
        """
        Generates word clouds for Arabic and English text from chat data.
        This method processes the chat data to extract text messages, filters out stop words,
        and separates the text into English and Arabic words. It then generates word clouds
        for both languages and saves them as image files.
        Steps:
        1. Extracts text messages from chat data.
        2. Filters out stop words.
        3. Separates text into English and Arabic words.
        4. Generates word clouds for both languages.
        5. Saves the word clouds as image files.
        Raises:
            TypeError: If there is an issue with the type of message text.
        Logs:
            - "Generating word clouds start"
            - "Processing the chat data"
            - "Chat data processed successfully"
            - "Generating word clouds"
            - "Word clouds generated successfully"
            - "Saving the word clouds"
            - "Word clouds saved successfully"
        """
        
        logger.info("Generating word clouds start")
        logger.info("Processing the chat data") 
        data_messages = self.chat_data['messages']
        plain_text = ""
        for message in data_messages:
            try:
                if type(message['text']) == str:
                    plain_text += message['text'] 
                    plain_text += "\n" 
                else:
                    
                    for sub_message in message['text']:
                        if type(sub_message) == str:
                            plain_text += sub_message
                            plain_text += "\n"
                        else:
                            plain_text += sub_message['text']
                            plain_text += "\n"                           
            except TypeError:
                print(message['text'])
                print(sub_message)
                break
        
        adjusted_tokenized_text = [x for x in plain_text.split() if x not in self.stop_words and x not in self.stop_words_E]
        
        english_words = [word for word in adjusted_tokenized_text if all(ord(char) < 128 for char in word)]
        arabic_words = [word for word in adjusted_tokenized_text if any(ord(char) >= 128 for char in word)]
        logger.info("Chat data processed successfully")
        
        text_arabic = ' '.join(arabic_words)
        text_english = ' '.join(english_words)
        
        logger.info("Generating word clouds")
        wordcloud_arabic = WordCloud(font_path = Data_dir/'BHoma.ttf').generate(text_arabic)
        wordcloud_english = WordCloud().generate(text_english)
        logger.info("Word clouds generated successfully")
        logger.info("Saving the word clouds")
        wordcloud_arabic.to_file(self.save_path/"arabic_example.png")
        wordcloud_english.to_file(self.save_path/"english_example.png")
        logger.info("Word clouds saved successfully")
        
if __name__ == '__main__':
    
    stats = Chat_statistics(chat_path = Data_dir / 'result.json') 
    stats.generate_word_cloud()
    print("Done!")
