import random

from app.extensions import db
from app.models import FlashCard

class FlashCardService:
    @staticmethod
    def create_flash_card(english_word, translation, category):
        flash_card = FlashCard(
            english_word=english_word,
            translation=translation,
            category=category
        )
        db.session.add(flash_card)
        db.session.commit()
        return flash_card

    @staticmethod
    def update_flash_card(flash_card, english_word, translation, category):
        flash_card.english_word = english_word
        flash_card.translation = translation
        flash_card.category = category
        db.session.commit()
        return flash_card

    @staticmethod
    def delete_flash_card(flash_card):
        db.session.delete(flash_card)
        db.session.commit()

    @staticmethod
    def get_all_flash_cards():
        return FlashCard.query.all()

    @staticmethod
    def get_flash_card_by_id(id):
        return FlashCard.query.get(id)

    @staticmethod
    def get_all_words():
        return FlashCard.query.all()

    @staticmethod
    def get_random_word_index(words):
        return random.randint(0, len(words) - 1)

    @staticmethod
    def get_incorrect_answers(current_word, words):
        return random.sample([w.translation for w in words if w.id != current_word.id], 2)
