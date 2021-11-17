from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import datetime
import calendar


# taken from github: unmonoqueteclea/calendar-telegram

def create_callback_data(action, year, month, day):
    """ Create the callback data associated to each button"""
    return ";".join([action, str(year), str(month), str(day)])


def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")


def create_calendar(year=None, month=None):
    """
    Create an inline keyboard with the provided year and month
    :param int year: Year to use in the calendar, if None the current year is used.
    :param int month: Month to use in the calendar, if None the current month is used.
    :return: Returns the InlineKeyboardMarkup object with the calendar.
    """
    now = datetime.datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.month
    data_ignore = create_callback_data("IGNORE", year, month, 0)
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton(text=calendar.month_name[month] + " " + str(year), callback_data=data_ignore))
    row = []
    for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "ВС"]:
        row.append(InlineKeyboardButton(text=day, callback_data=data_ignore))
    keyboard.row(*row)
    #
    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(" ", callback_data=data_ignore))
            else:
                row.append(InlineKeyboardButton(str(day), callback_data=create_callback_data("DAY", year, month, day)))
        keyboard.row(*row)
    row = []
    row.append(InlineKeyboardButton("<", callback_data=create_callback_data("PREV-MONTH", year, month, day)))
    row.append(InlineKeyboardButton(" ", callback_data=data_ignore))
    row.append(InlineKeyboardButton(">", callback_data=create_callback_data("NEXT-MONTH", year, month, day)))
    keyboard.row(*row)
    return keyboard
