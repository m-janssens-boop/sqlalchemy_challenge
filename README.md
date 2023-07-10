# sqlalchemy_challenge

Background
--------
A climate analysis on Honolulu, Hawaii.

## Objective ##
### Part 1: Analyze and Explore the Climate Data ###
Use Python and SQLAlchemy to do a basic climate analysis and data exploration of the climate database. Specifically, use SQLAlchemy ORM queries, Pandas, and Matplotlib to do the following:
* Use the SQLAlchemy create_engine() function to connect to the SQLite database.
* Use the SQLAlchemy automap_base() function to reflect the tables into classes, and then save references to the classes named station and measurement.
* Link Python to the database by creating a SQLAlchemy session.
* Perform a precipitation analysis and then a station analysis
#### Precipitation Analysis ####
- Find the most recent date in the dataset.
- Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.
- Select only the "date" and "prcp" values.
- Load the query results into a Pandas DataFrame, explicitly setting the column names.
- Sort the DataFrame values by "date".
- Plot the results by using the DataFrame plot method

- Use Pandas to print the summary statistics for the precipitation data.

#### Station Analysis ####
- Design a query to calculate the total number of stations in the dataset.
- Design a query to find the most-active stations.
- Design a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.
- Design a query to get the previous 12 months of temperature observation (TOBS) data.


### Part 2: Design Climate App ###
Design a Flask API based on the queries developed above, that:
- Starts at the homepage.
- Lists all the available routes.
- `/api/v1.0/precipitation`
  - Converts the query results from the precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
  - Return the JSON representation of the dictionary.
- `/api/v1.0/stations`
  - Return a JSON list of stations from the dataset.
- `/api/v1.0/tobs`
  - Query the dates and temperature observations of the most-active station for the previous year of data.
  - Return a JSON list of temperature observations for the previous year.
- `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
  - Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
  - For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
  - For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
