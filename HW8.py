# Your name: Divum Mittal
# Your student id: 09885854
# Your email: divum@umich.edu
# List who you have worked with on this homework: Julia Coffmann

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    d = {}
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    #cur.execute("CREATE TABLE IF NOT EXISTS Restaurants (id INTEGER PRIMARY KEY, name TEXT, category_id INTEGER, building_id INTEGER, rating TEXT)")
    cur.execute("SELECT restaurants.name, buildings.building,  categories.category, restaurants.rating from restaurants JOIN buildings on buildings.id = restaurants.building_id JOIN categories on categories.id = restaurants.category_id")
    stuff = cur.fetchall()
    for i in stuff:
        empty = {}
        empty['category'] = i[2]
        empty['building'] = i[1]
        empty['rating'] = i[3]
        #print(i)
        name = i[0]
        d[name] = empty
    return d
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """

def plot_rest_categories(db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT categories.category, COUNT(restaurants.id) FROM restaurants JOIN categories ON restaurants.category_id = categories.id GROUP BY categories.category")
    fetched = cur.fetchall()
    bar_dict = {item[0]: item[1] for item in fetched}
    sorted_bar_dict = dict(sorted(bar_dict.items(), key = lambda x: x[1]))
    names = sorted_bar_dict.keys()
    names = list(names)
    values = sorted_bar_dict.values()
    values = list(values)
    # plt.barh(names, values)
    # plt.xlabel("Number of Restaurants")
    # plt.ylabel("Restaurant Categories")
    # plt.title("Types of Restaurants on South University Ave")
    # plt.show()
    return bar_dict


    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """

def find_rest_in_building(building_num, db):
    final = []
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT restaurants.name, restaurants.rating, buildings.building FROM restaurants JOIN buildings ON restaurants.building_id = buildings.id")
    fetched = cur.fetchall()
    fetched_sorted = sorted(fetched, key = lambda x: x[1], reverse=True)
    for x in fetched_sorted:
        if x[2] == building_num:
            final.append(x[0])
    return final
    

    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    lst = []
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT categories.category, ROUND(AVG(restaurants.rating),1) FROM restaurants JOIN categories ON restaurants.category_id = categories.id GROUP BY category")
    fetched_rating = cur.fetchall()
    fetched_sorted_ratings = sorted(fetched_rating, key = lambda x: x[1])
    cur.execute("SELECT buildings.building, ROUND(AVG(restaurants.rating),1) FROM restaurants JOIN buildings ON restaurants.building_id = buildings.id GROUP BY building")
    fetched_building = cur.fetchall()
    fetched_sorted_buildings = sorted(fetched_building, key = lambda x: x[1])


    lst.append(fetched_sorted_ratings[-1])
    lst.append(fetched_sorted_buildings[-1])

    fetched_rate = dict(fetched_sorted_ratings)
    fetched_build = dict(fetched_sorted_buildings)

    # names = fetched_rate.keys()
    # names = list(names)
    # values = fetched_rate.values()
    # values = list(values)
    # plt.barh(names, values)
    # plt.xlabel("Ratings")
    # plt.ylabel("Categories")
    # plt.title("Average Restaurant Ratings by Category")
    # plt.show()


    # names = fetched_build.keys()
    # names_string = []
    # for i in names:
    #     temp = str(i)
    #     names_string.append(temp)
    # values = fetched_build.values()
    # values = list(values)
    # plt.barh(names_string, values)
    # plt.xlabel("Ratings")
    # plt.ylabel("Buildings")
    # plt.title("Average Restaurant Ratings by Building")
    # plt.show()
    return lst
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    pass

#Try calling your functions here
def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
