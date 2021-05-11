import requests
import config

from utils import update_form_date, load_courses, fetch_years, fetch_timetable

timetables = []

with requests.session() as s:
    # load session
    s.get(config.url_default)

    # load courses
    courses, web_content = load_courses(s)

    # update form data with the information coming from the web content
    form_data = update_form_date(web_content)

    # for every course fetch the available years
    for course in courses:
        years, web_content = fetch_years(s, form_data, course)

        # update form data with the information coming from the web content after loading the courses
        form_data = update_form_date(web_content)

        for year in years:
            timetable = fetch_timetable(s, form_data, course, year)
            timetables += timetable

print(timetables)
