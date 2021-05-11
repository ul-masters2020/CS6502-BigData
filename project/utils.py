import config

from bs4 import BeautifulSoup

timetable = []


def update_form_date(web_content):
    form_data = config.form_data

    for inp in web_content.select("input[value]"):
        form_data[inp["name"]] = inp["value"]

    return form_data


def load_courses(session):
    web_content = BeautifulSoup(session.get(config.url).content, "html.parser")

    # select options from the id - HeaderContent_CourseDropdown
    courses = [option["value"] for option in web_content.select("#HeaderContent_CourseDropdown option")]

    # remove the first option as it's -1
    courses = courses[1:]

    return courses, web_content


def fetch_years(session, form_data, course):
    form_data["ctl00$HeaderContent$CourseDropdown"] = course
    web_content = BeautifulSoup(session.post(config.url, data=form_data).content, "html.parser")

    # select options from the id - HeaderContent_CourseYearDropdown
    years = [opt["value"] for opt in web_content.select("#HeaderContent_CourseYearDropdown option")]

    # remove the first option as it's -1
    return years[1:], web_content


def _parse_info(course_info):
    """
    eg: PT4008 - LAB - 4B
    """
    dict_info = {}
    s_tokens = course_info.split("-")

    dict_info["module"] = s_tokens[0].strip()
    dict_info["type"] = s_tokens[1].strip()

    # handle cases where room number is not defined
    try:
        dict_info["room"] = s_tokens[2].strip()
    except:
        dict_info["room"] = ""

    return dict_info

def _parse_weeks(week):
    """
    function to parse weeks from the form given to actual numbers
    eg: Wks:1-3,5-7,9,11-12 => [1, 2, 3, 5, 6, 7, 9, 11, 12]
    """
    weeks = []
    tokens = week[4:].split(",")
    for token in tokens:
        if len(token) > 2:
            parts = token.split("-")
            lower = int(parts[0])
            upper = int(parts[1])
            while lower <= upper:
                weeks.append(str(lower))
                lower += 1
        else:
            weeks.append(token)
    return weeks

def _get_timetables(raw_td_values, course, year, day_number):
    for index in range(0, len(raw_td_values), 6):

        # There are cells with missing data. These cells are skipped in my analysis.
        course_break_count = 0
        for elem in raw_td_values:
            if elem == " ":
                course_break_count += 1
        expected_size = 6 * course_break_count + 5

        if len(raw_td_values) == expected_size:
            # print(raw_td_values)
            try:
                data_dict = {
                    "course": course,
                    "year": year,
                    "time": raw_td_values[index],
                    "lecturer": raw_td_values[index + 2].string.strip(),
                    "weeks": raw_td_values[index + 3],
                    "mode": raw_td_values[index + 4].string,
                    "day": config.days[day_number]
                }
                parsed = _parse_info(raw_td_values[index + 1])
                weeks = _parse_weeks(data_dict["weeks"])
                for week in weeks:
                    data_dict["weeks"] = week

                    timetable.append({**data_dict, **parsed})
            except:
                pass


def fetch_timetable(session, form_data, course, year):
    form_data["ctl00$HeaderContent$CourseYearDropdown"] = year
    web_content = BeautifulSoup(session.post(config.url, data=form_data).content, "html.parser")

    # tr_list is the list of all time slots of 30 minutes
    tr_list = web_content.find("table").find_all("tr")

    for time_slots in tr_list:
        # td_list is the week information (Monday - Saturday)
        td_list = time_slots.find_all("td")

        for day_number in range(len(td_list)):
            day_info_content = td_list[day_number].font.contents

            if len(day_info_content) > 2:
                # clean info
                cleaned_day_info_content = []
                for i in range(0, len(day_info_content), 2):
                    cleaned_day_info_content.append(day_info_content[i])

                # parse values and save it in list of dicts
                _get_timetables(cleaned_day_info_content, course, year, day_number)

    return timetable
