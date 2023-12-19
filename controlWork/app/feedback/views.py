from flask import flash, render_template, redirect, url_for
from flask_login import login_required

from . import feedback_blueprint
from .forms import CreateFeedbackForm
from .models import db, Feedback

@feedback_blueprint.route("/")
@login_required
def feedback():
    feedback_form = CreateFeedbackForm()
    feedback_list = Feedback.query.all()

    return render_template('feedback.html', feedback_form=feedback_form, feedback_list=feedback_list)

@feedback_blueprint.route("/create_feedback", methods=['POST'])
def create_feedback():
    feedback_form = CreateFeedbackForm()

    if feedback_form.validate_on_submit():
        name = feedback_form.name.data
        email = feedback_form.email.data
        description = feedback_form.description.data
        rate = feedback_form.rate.data

        new_feedback = Feedback(name=name, email=email, description=description, rate=rate, useful=False)

        db.session.add(new_feedback)
        db.session.commit()
        flash("Створення виконано", category=("success"))
        return redirect(url_for("feedback_bp.feedback"))
    
    flash("Помилка при створенні", category=("danger"))
    return redirect(url_for("feedback_bp.feedback"))

@feedback_blueprint.route("/read_feedback/<int:feedback_id>")
def read_feedback(feedback_id=None):
    feedback = Feedback.query.get_or_404(feedback_id)
    return redirect(url_for("feedback"))

@feedback_blueprint.route("/update_feedback/<int:feedback_id>")
def update_feedback(feedback_id=None):
    feedback = Feedback.query.get_or_404(feedback_id)

    feedback.useful = not feedback.useful
    db.session.commit()
    flash("Оновлення виконано", category=("success"))
    return redirect(url_for("feedback"))

@feedback_blueprint.route("/delete_feedback/<int:feedback_id>")
def delete_feedback(feedback_id=None):
    feedback = Feedback.query.get_or_404(feedback_id)

    db.session.delete(feedback)
    db.session.commit()
    flash("Видалення виконано", category=("success"))
    return redirect(url_for("feedback"))