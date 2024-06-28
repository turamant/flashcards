import random

from flask import render_template, redirect, url_for, request, session, flash
from app import app, db
from app.models import FlashCard
from app.forms import FlashCardForm


@app.route('/', methods=['GET', 'POST'])
def index():
    form = FlashCardForm()
    if form.validate_on_submit():
        flash_card = FlashCard(
            english_word=form.english_word.data,
            translation=form.translation.data,
            category=form.category.data
        )
        db.session.add(flash_card)
        db.session.commit()
        return redirect(url_for('index'))
    flash_cards = FlashCard.query.all()
    return render_template('index.html', form=form, flash_cards=flash_cards)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    flash_card = FlashCard.query.get(id)
    form = FlashCardForm(obj=flash_card)
    if form.validate_on_submit():
        flash_card.english_word = form.english_word.data
        flash_card.translation = form.translation.data
        flash_card.category = form.category.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', form=form)


@app.route('/delete/<int:id>')
def delete(id):
    flash_card = FlashCard.query.get(id)
    db.session.delete(flash_card)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/study', methods=['GET', 'POST'])
def study():
    words = FlashCard.query.all()
    if request.method == 'POST':
        current_word_id = int(request.form['current_word_id'])
        if current_word_id < len(words) - 1:
            return redirect(url_for('study', current_word_id=current_word_id + 1))
        else:
            return redirect(url_for('index'))
    current_word_id = request.args.get('current_word_id', 0, type=int)
    current_word = words[current_word_id]
    return render_template('study.html', word=current_word, current_word_id=current_word_id)


@app.route('/test', methods=['GET', 'POST'])
def test():
    words = FlashCard.query.all()

    if request.method == 'POST':
        current_word_id = int(request.form['current_word_id'])
        if current_word_id < len(words):
            selected_answer = request.form['answer'].lower()
            correct_answer = words[current_word_id].translation.lower()
            if selected_answer == correct_answer:
                if 'correct_answers' not in session:
                    session['correct_answers'] = 0
                session['correct_answers'] += 1
                flash('Correct!', 'success')
            else:
                if 'incorrect_answers' not in session:
                    session['incorrect_answers'] = 0
                session['incorrect_answers'] += 1
                flash('Incorrect. The correct answer is: ' + words[current_word_id].translation, 'danger')
        return redirect(url_for('test'))

    # Если это GET request
    random_index = random.randint(0, len(words) - 1)
    current_word = words[random_index]
    incorrect_answers = random.sample([w.translation for w in words if w.id != current_word.id], 2)
    answers = [current_word.translation] + incorrect_answers
    random.shuffle(answers)
    return render_template('test.html', word=current_word, answers=answers, current_word_id=random_index)
