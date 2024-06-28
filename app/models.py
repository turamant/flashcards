from app import db


class FlashCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_word = db.Column(db.String(100), nullable=False)
    translation = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    attempts = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<FlashCard %r>' % self.english_word
