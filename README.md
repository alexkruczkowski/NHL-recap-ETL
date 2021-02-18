# NHL-recap-ETL
Sample ETL using Python and Airflow. Pulls previous day NHL games annd final scores with a video link to the game recap. 

At the moment the ETL is run locally, with results loaded into a SQLite database and accessed via DBeaver. 

## :floppy_disk: Data
All of the data is pulled from the NHL API with community written documenation found [here](https://gitlab.com/dword4/nhlapi/-/blob/master/stats-api.md).

## :mag: Methodology
As the NHL API is publically accessible and requires no keys, the data is pulled directly via the appropriate endpoints. Results are validated and if all tests pass, the results are then loaded into the database. 

## :wave: Author
Alex Kruczkowski
