# holiday-manager
### Connor Buxton, 1/9/2022

INTRODUCTION:
This program allows the user to track, add and remove holidays for years spanning from 2020 to 2024.
Options:
- Add: adds a holiday with the given name and date
- Remove: removes a holiday with the given name and date. NAME AND DATE MUST MATCH
- View: Views either current week, or holidays in a given year and week number
- Save: Saves the changes made to a JSON file
- Exit: Exits the program. Points out if there are unsaved changes


FUTURE WORK:
Since the functions for reading from JSON exist and are used with a read-only file, it would be very
easy to allow for reading in from JSON files that have been saved from this program. Thinking of
holidays.json as a seed, further runs might use a try except block where the try would allow the saved
file to be loaded in but the except would have the holidays.json instead.
