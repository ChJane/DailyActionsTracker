from flask import render_template
from app import app, db


@app.errorhandler(404)
def not_found_error(error):
    """!
    Обработчик ошибки 404 "File not found"

    @param error - код ошибки
    @return страницу с ошибкой (404.html)
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """!
    Обработчик ошибки 500

    @param error - код ошибки
    @return страницу с ошибкой (500.html)
    """
    db.session.rollback()
    return render_template('500.html'), 500
