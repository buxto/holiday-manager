from datetime import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
import config
# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
class Holiday:
      
    def __init__(self,name, date):
        #Your Code Here
        if type(date) == datetime:
            self._name = name
            self._date = date
        else:
            print('Error: Date not in correct format.')
    
    def __str__ (self):
        # String output
        _output = str(self._name) + ', ' + str(self._date)
        return _output
        # Holiday output when printed.
          
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------

class HolidayList:
    def __init__(self):
       self.innerHolidays = []
   
    def addHoliday(self, holidayObj):
        # Make sure holidayObj is an Holiday Object by checking the type
        if type(holidayObj) == Holiday:
        # Use innerHolidays.append(holidayObj) to add holiday
            self.innerHolidays.append(holidayObj)
        # print to the user that you added a holiday
            print('Added holiday.')
        else:
            print('Error: Not Holiday.')
        return

    def findHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays
        for item in self.innerHolidays:
            if item._name == HolidayName and item._date == Date:
                # found it, return
                return item



        # Return Holiday

    def removeHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays by searching the name and date combination.
        holiday_rm = self.findHoliday(HolidayName, Date)
        # remove the Holiday from innerHolidays
        if holiday_rm != None:
            self.innerHolidays.remove(holiday_rm)
            # inform user you deleted the holiday
            print('Holiday deleted.')
            success = True
            return success
        else:
            print('No holiday with that information found')
            success = False
            return success

    def read_json(self, filelocation):
        # Read in things from json file location
        with open(filelocation, 'r') as j:
            x = json.loads(j.read())
        # Use addHoliday function to add holidays to inner list.
        holiday_add = x['holidays']
        for i in range(len(holiday_add)):
            current = holiday_add[i]
            temp_name = current['name']
            temp_date = datetime.strptime(current['date'], '%Y-%m-%d')
            self.innerHolidays.append(Holiday(temp_name, temp_date))
        return


    def save_to_json(self, filelocation):
        # Write out json file to selected file.
        with open(filelocation, 'w', encoding='utf-8') as j:
            output_list = []
            for item in self.innerHolidays:
                temp = {}
                temp['name'] = item._name
                temp['date'] = str(item._date.date())
                output_list.append(temp)
            json.dump(output_list, j, indent = 4)
        print('Changes saved.')
        return

        
    def scrapeHolidays(self):
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/
        def getHTML(url):
            response = requests.get(url)
            return response.text
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        try:
            year_list = [2020, 2021, 2022, 2023, 2024]
            for year in year_list:
                req_str = 'https://www.timeanddate.com/calendar/print.html?year={current_year}&country=1&cols=3&hol=33554809&df=1'
                html = getHTML(req_str.format(current_year = year))
                soup = BeautifulSoup(html, 'html.parser')
                table = soup.find('table', attrs = {'class' : 'cht lpad'})

                for row in table.find_all('tr'):
                    cells = row.find_all('td')
                    temp_date = cells[0].string + f', {year}'
                    formatted_date = datetime.strptime(temp_date, '%b %d, %Y')
                    temp_name = cells[1].string
                    self.innerHolidays.append(Holiday(temp_name, formatted_date))
        except:
            print('Exception occurred in scraping process.')
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.
        return

    def numHolidays(self):
        # Return the total number of holidays in innerHolidays
        return len(self.innerHolidays)

    
    def filter_holidays_by_week(self, year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        filtered_holidays = list(filter(lambda a: a._date.isocalendar().week == week_number and a._date.isocalendar().year == year, self.innerHolidays))
        return filtered_holidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays

    def displayHolidaysInWeek(self, holidayList):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        for item in holidayList:
            print(item)
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.
        return

    def getWeather(self):
        api_key = config.api_key
        url = 'http://api.weatherapi.com/v1/forecast.json?key={key}&q=Milwaukee&days=7&aqi=no&alerts=no'
        response = requests.get(url.format(key = api_key))
        data = response.json()
        data_list = data['forecast']['forecastday']
        weather_list = []
        for item in data_list:
            temp_dict = {}
            temp_dict['date'] = item['date']
            temp_dict['condition'] = item['day']['condition']['text']
            weather_list.append(temp_dict)
        return weather_list

    def viewCurrentWeek(self):
        x = datetime.now()
        # Use the Datetime Module to look up current week and year
        current_week = x.isocalendar().week
        current_year = x.isocalendar().year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        current_holidays = self.filter_holidays_by_week(current_year, current_week)
        # Use your displayHolidaysInWeek function to display the holidays in the week
        user_input = input('Would you like to see the weather for the coming 7 days? [y/n]: ')
        if user_input.lower() == 'y':
            self.displayHolidaysInWeek(current_holidays)
            weather_list = self.getWeather()
            for item in weather_list:
                print(str(item['date']) + ': ' + str(item['condition']))
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
        return

def userAdd(HolidayList, save_flag):
    name_input = False
    while not name_input:
        add_name = input('Please enter the name of the holiday you\'d like to add: ')
        if type(add_name) == str:
            name_input = True
        else:
            print('That is not a name, try again.')

    date_input = False
    while not date_input:
        try:
            add_date = input('Please enter the date in YYYY-MM-DD format: ')
            frmt_date = datetime.strptime(add_date, '%Y-%m-%d')
            if type(frmt_date) == datetime:
                date_input = True
        except:
            print('Error: Date not in format.')
    
    if HolidayList.findHoliday(add_name, frmt_date) == None:
        HolidayList.addHoliday(Holiday(add_name, frmt_date))
        save_flag = False
        return save_flag
    else:
        print('Error: Holiday already in list.')
        return save_flag

def userRm(HolidayList, save_flag):
    name_input = False
    while not name_input:
        rm_name = input('Please enter the name of the holiday you\'d like to remove: ')
        if type(rm_name) == str:
            name_input = True
        else:
            print('That is not a name, try again.')

    date_input = False
    while not date_input:
        try:
            rm_date = input('Please enter the date in YYYY-MM-DD format: ')
            frmt_date = datetime.strptime(rm_date, '%Y-%m-%d')
            if type(frmt_date) == datetime:
                date_input = True
        except:
            print('Error: Date not in format.')

    success = HolidayList.removeHoliday(rm_name, frmt_date)
    if success:
        save_flag = False
        return save_flag
    else:
        return save_flag

def userView(HolidayList):
    current_year = datetime.now().year
    year_input = False
    while not year_input:
        try:
            user_year = input('Enter year in 4-digit form [YYYY]: ')
            user_year = int(user_year)
            if user_year > 2019 and user_year < 2025:
                year_input = True
            else:
                print('Error: Year outside range.')
        except:
            print('Error: Year not in format.')
    week_input = False
    while not week_input:
        try:
            user_week = input('Enter week number [1-52, leave blank for current week]: ')
            if user_week == '' and user_year == current_year:
                HolidayList.viewCurrentWeek()
                week_input = True
            elif user_week == '' and user_year != current_year:
                print('Error: can only print current week for current year.')
            elif user_week.isnumeric():
                user_week = int(user_week)
                if user_week > 0 and user_week < 53:
                    HolidayList.displayHolidaysInWeek(HolidayList.filter_holidays_by_week(user_year, user_week))
                    week_input = True
                else:
                    print('Error: Week out of range.')
            else:
                print('Error: Week not recognized.')
        except:
            print('Error: Week not in format.')
    return

def userSave(HolidayList):
    filelocation = 'cb_holiday.json'
    print('Saving Changes...')
    HolidayList.save_to_json(filelocation)
    save_flag = True
    return save_flag

def userExit(save_flag):
    good_input = False
    if save_flag == False:
        print('Unsaved Changes!!!')
    while not good_input:
        user_input = input('Are you sure you want to exit? [y/n]: ')
        if user_input.lower() == 'y':
            print('Exiting program...')
            prgm_sts = False
            good_input = True
        elif user_input.lower() == 'n':
            prgm_sts = True
            good_input = True
        else:
            print('Error: Please input a y or n.')
    return prgm_sts

def main():
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display User Menu (Print the menu)
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 

    main_holiday_list = HolidayList()
    main_holiday_list.read_json('holidays.json')
    main_holiday_list.scrapeHolidays()
    print('Holiday Tracker')
    print('Number of Holidays: ' + str(main_holiday_list.numHolidays()))
    print('----------------------------------')
    print('Option 1: Add Holiday')
    print('Option 2: Remove Holiday')
    print('Option 3: View Holidays')
    print('Option 4: Save Changes to JSON')
    print('Option 5: Exit Program')

    program_sts = True
    save_flag = True
    while program_sts:
        opt_input = False
        while not opt_input:
            user_option = input('Enter the number of the option you\'d like to perform [1-5]: ')
            if user_option.isdecimal():
                user_option = int(user_option)
                if user_option == 1:
                    save_flag = userAdd(main_holiday_list, save_flag)
                    opt_input = True
                elif user_option == 2:
                    save_flag = userRm(main_holiday_list, save_flag)
                    opt_input = True
                elif user_option == 3:
                    userView(main_holiday_list)
                    opt_input = True
                elif user_option == 4:
                    save_flag = userSave(main_holiday_list)
                    opt_input = True
                elif user_option == 5:
                    program_sts = userExit(save_flag)
                    opt_input = True
                else:
                    print('Error: Option not in range. Try again.')
        print()
        print()




    


if __name__ == "__main__":
    main();


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.





