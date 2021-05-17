"""Routes for parent Flask app."""
from flask import render_template, request, redirect, url_for
from flask import Blueprint
from flask_login import login_required, current_user
from flask_paginate import Pagination, get_page_parameter
from models.database import engine
from datetime import date, timedelta, datetime

main = Blueprint('main', __name__)

# Load current state of covid
today = date.today()
# display results of yesterday because the site is updated the next day
yesterday = today - timedelta(days=1)
searchDate = yesterday


@main.route('/', methods=['post', 'get'])
def index():
    global searchDate
    """Loading page."""

    pagination, data = setupSearch(searchDate)
    if (request.method == 'POST') and 'searchDate' in request.form:
        searchDate = request.form.get("searchDate")

    if (request.method == 'GET') and 'searchDate' in request.args:
        searchDate = request.args.get('searchDate')

    pagination, data = setupSearch(searchDate)
    return render_template(
        'index.html',
        res=data,
        pagination=pagination,
        searchDate=searchDate,
        today=yesterday
    )


def setupSearch(date__):
    query = """SELECT *
                    FROM "CleanDataByRegion"
                    WHERE date= %s LIMIT %s OFFSET %s"""
    count_query = """SELECT count(*) 
                    FROM "CleanDataByRegion"
                    WHERE date= %s ;"""
    count = engine.execute(count_query, date__).scalar()

    # Setting up the pagination variable,
    page = request.args.get(get_page_parameter(), type=int, default=1)
    limit = 9  # define how many results you want per page
    offset = page * limit - limit  # offset for SQL query

    data = engine.execute(query, (date__, limit, offset)).fetchall()
    pagination = Pagination(page=page, per_page=limit, total=count, css_framework='bulma')
    return pagination, data


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
