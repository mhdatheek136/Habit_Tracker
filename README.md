# Habit Tracker Backend

Developing and maintaining good habits is essential for a healthy and successful lifestyle. The Habit Tracker, part of IU University's DLBDSOOFPP01 course, is designed to assist users in tracking and managing their habits. The program utilizes Python 3.7 as its backend.


## Habit Tracker's Core Functionality
The habit tracker allows a user to:

* Create Habit 
* Delete Habit
* Customize Habit Information 
* Check-in Habit
* View and Analyse Habit

### Analytics
User can view and analyse the following:
* List of all currently tracked habits
* List of all currently tracked habits with information
* List of all habits with the same periodicity
* Longest run streak of all defined habits
* Longest run streak for a given habit



# Getting Started
**Important**: Make sure that Python 3.7 + is installed on your OS. You can download the latest version of Python from [this link.](https://www.python.org/downloads/)

## Installing All Requirements
Run the following command in terminal:
```
pip install -r requirements.txt
```


## How To Run the Program
After installing the requirements, download the files from this repository and store them in a separate folder. Open your terminal window and [cd](https://www.digitalcitizen.life/command-prompt-how-use-basic-commands/) to your downloaded folder. After that, type the following command to execute the program:
```
python main.py
```
After using the above command, You will get the main menu of the Habit Tracker in CLI (Command Line Interface)

```
*** Welcome to the Habit Tracker ***

? Select an option below: (Use arrow keys)
 » Create New Habit
   Delete Existing Habit
   Customize Habit Information
   Check-in Habit
   Analytics
   Exit
```
You can try different options in main menu

## Running tests
To run the test, type the following command in terminal:
```
pytest
```
To run test separately on following modules:
* test_habit.py
    ```
    pytest test_habit.py
    ```
* test_analytics.py
    ```
    pytest test_analytics.py
    ``` 
# Usage

**Important**: You can choose to keep or remove the **main.db** file as it contains the following pre-defined habits: Coding, Studying, Swimming, Camping, and Reading. <br>

# Contact

Atheek Mohamed Rafi - [Email](mhdatheek@gmail.com)

Project Link: [https://github.com/mhdatheek136/Habit_Tracker](https://github.com/mhdatheek136/Habit_Tracker)
