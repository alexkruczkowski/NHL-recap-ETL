# NHL-recap-ETL
Sample ETL using Python and Airflow. Pulls previous day NHL games annd final scores with a video link to the game recap. 

At the moment the ETL is run locally, with results loaded into a SQLite database and accessed via DBeaver. 

## :floppy_disk: Data
All of the data is pulled from the NHL API with community written documenation found [here](https://gitlab.com/dword4/nhlapi/-/blob/master/stats-api.md).

## :mag: Methodology
The NHL API is called to get game info and links to the video recaps based on the games that were played the previous night. Once all the info is succesfully retrieved results are put into a pandas df and validated. If all tests pass, the results are then loaded into the local database. 

## :wave: Author
Alex Kruczkowski
