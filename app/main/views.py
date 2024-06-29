import random

from flask import render_template, redirect, url_for, request, session, flash
from app.main import main_bp
from app.forms import FlashCardForm
from app.services import FlashCardService
from app.extensions import db


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    form = FlashCardForm()
    if form.validate_on_submit():
        flash_card = FlashCardService.create_flash_card(
            form.english_word.data,
            form.translation.data,
            form.category.data
        )
        return redirect(url_for('main.index'))
    flash_cards = FlashCardService.get_all_flash_cards()
    return render_template('index.html', form=form, flash_cards=flash_cards)


@main_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    flash_card = FlashCardService.get_flash_card_by_id(id)
    form = FlashCardForm(obj=flash_card)
    if form.validate_on_submit():
        FlashCardService.update_flash_card(
            flash_card,
            form.english_word.data,
            form.translation.data,
            form.category.data
        )
        return redirect(url_for('main.index'))
    return render_template('edit.html', form=form)


@main_bp.route('/delete/<int:id>')
def delete(id):
    flash_card = FlashCardService.get_flash_card_by_id(id)
    FlashCardService.delete_flash_card(flash_card)
    return redirect(url_for('main.index'))


@main_bp.route('/study', methods=['GET', 'POST'])
def study():
    words = FlashCardService.get_all_words()
    if request.method == 'POST':
        current_word_id = int(request.form['current_word_id'])
        if current_word_id < len(words) - 1:
            return redirect(url_for('main.study', current_word_id=current_word_id + 1))
        else:
            return redirect(url_for('main.index'))
    current_word_id = request.args.get('current_word_id', 0, type=int)
    current_word = words[current_word_id]
    return render_template('study.html', word=current_word, current_word_id=current_word_id)


@main_bp.route('/test', methods=['GET', 'POST'])
def test():
    words = FlashCardService.get_all_words()

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
        return redirect(url_for('main.test'))

    random_index = FlashCardService.get_random_word_index(words)
    current_word = words[random_index]
    incorrect_answers = FlashCardService.get_incorrect_answers(current_word, words)
    answers = [current_word.translation] + incorrect_answers
    random.shuffle(answers)
    return render_template('test.html', word=current_word, answers=answers, current_word_id=random_index)

