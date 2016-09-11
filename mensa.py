#!/usr/bin/env python3
from requests import get
from bs4 import BeautifulSoup
from time import strftime

DIV = "div"
STRONG = "strong"
TR = "tr"
IMG = "img"
TD = "td"

vegasign = "🌱"
vegesign = "🍇"

defaulturl = "https://www.studentenwerkfrankfurt.de/essen-trinken/speiseplaene/cafeteria-bockenheim/"


class Mensa():

    def __init__(self, url=defaulturl):
        self.soup = BeautifulSoup(get(url).text, 'lxml')

    def get_week(self):
        """Returns a dictionary with keys = dates, values = lists of foods."""
        week = {}
        for day in self.soup.find_all(DIV, class_="panel panel-default"):
            date = day.find(DIV, class_="panel-heading").find(STRONG).get_text()
            week[date] = self.get_day(day)
        return week

    def get_day(self, day):
        """Returns a list of all food items available for the day that was
        passed to the function.

        TODO: Ignore entries that contain the word "burger" in it."""

        items = []
        for food in day.find(DIV, class_="panel-body").find_all(TR, class_=""):
            #if "burger" in name.lower(): continue
            items.append(self.get_food_info(food))
        return items

    def get_today(self):
        """Returns a list of food available today, if any.
        For this, we artificially construct a German date, as this is what's
        used as identifier on the Studentenwerk website."""

        if int(strftime("%w")) in [0, 6]:
            #raise NoFoodException("No food available for this day.")
            pass

        # I know this sucks, but alternative would be
        # stackoverflow.com/questions/985505/ which sucks even more
        weekdays = ["Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag",
                "Freitag", "Samstag"]       # stupid order thanks USA
        months = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
                "August", "September", "Oktober", "November", "Dezember"]
        germandate = "{0}, {1}. {2}".format(weekdays[int(strftime("%w"))],
                strftime("%d"), months[int(strftime("%m")) - 1])
        # for testing purposes, COMMENT THIS LATER:
        germandate = "Dienstag, 06. September"

        try:
            return self.get_day(self.soup.find(STRONG, text=germandate).parent.parent)
        except AttributeError e:
            raise NoFoodException("No food available for " + germandate)

    def get_food_info(self, food):
        """Returns a dictionary with the keys
        - 'name' (name of the dish)
        - 'vega' (True if dish is vegan)
        - 'vege' (True if dish is vegetarian'
        - 'euro' (price of the dish in Euro)"""

        info = {}
        info['name'] = food.find(STRONG, class_="menu_name").get_text()
        info['vega'] = True if food.find(IMG, title="Vegan") else False
        info['vege'] = True if food.find(IMG, title="vegetarisch") else False
        info['euro'] = food.find(TD, class_="col-md-2").find(STRONG).get_text()
        return info


class NoFoodException(Exception):
    """Exception that is raised when no food is available for a selected
    day."""

    def __init__(self, message):
        self.message = message

mensa = Mensa()
#print(mensa.get_week())
print(mensa.get_today())
