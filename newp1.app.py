import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

# Title
st.title("🌍 Earthquakes Analysis Dashboard")

# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="12345678",
    database="earth_quake_dp"
)

# Header
st.header("Select any problem statement to run the SQL Query")

# Dictionary of Queries
queries = {

"Top 10 Strongest Earthquakes":
"""
SELECT place, mag
FROM earthquakes
ORDER BY mag DESC
LIMIT 10
""",

"Top 10 Deepest Earthquakes":
"""
SELECT place, depth_km
FROM earthquakes
ORDER BY depth_km DESC
LIMIT 10
""",

"Shallow Earthquakes":
"""
SELECT place, depth_km
FROM earthquakes
WHERE depth_km < 70
ORDER BY depth_km ASC
LIMIT 10
""",

"Average Depth Per Place":
"""
SELECT place, ROUND(AVG(depth_km),2) AS avg_depth
FROM earthquakes
GROUP BY place
ORDER BY avg_depth DESC
LIMIT 10
""",

"Average Magnitude per Magnitude Type":
"""
SELECT magType, ROUND(AVG(mag),2) AS avg_mag
FROM earthquakes
GROUP BY magType
LIMIT 10
""",

"Year with Most Earthquakes":
"""
SELECT year, COUNT(*) AS total_quakes
FROM earthquakes
GROUP BY year
ORDER BY total_quakes DESC
LIMIT 10
""",

"Month with Highest Number of Earthquakes":
"""
SELECT month, COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY month
ORDER BY total_earthquakes DESC
LIMIT 10
""",

"Day of Week with Most Earthquakes":
"""
SELECT day, COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY day
ORDER BY total_earthquakes DESC
LIMIT 1
""",

"Count of Earthquakes per Hour":
"""
SELECT hour, COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY hour
ORDER BY hour
LIMIT 1
""",

"Most Active Reporting Network":
"""
SELECT net, COUNT(*) AS total_events
FROM earthquakes
GROUP BY net
ORDER BY total_events DESC
LIMIT 1
""",

"Top 5 Places with Highest Casualties":
"""
SELECT place, SUM(cdi) AS total_casualties
FROM earthquakes
GROUP BY place
ORDER BY total_casualties DESC
LIMIT 5
""",

"Total Estimated Economic Loss per Place":
"""
SELECT place, SUM(mmi) AS total_loss
FROM earthquakes
GROUP BY place
ORDER BY total_loss DESC
""",

"Count of Reviewed vs Automatic Earthquakes":
"""
SELECT status, COUNT(*) AS total
FROM earthquakes
GROUP BY status
""",

"Count by Earthquake Type":
"""
SELECT type, COUNT(*) AS total
FROM earthquakes
GROUP BY type
""",

"Number of Earthquakes by Data Type":
"""
SELECT magType, COUNT(*) AS total
FROM earthquakes
GROUP BY magType
""",

"Events with High Station Coverage":
"""
SELECT place, nst
FROM earthquakes
ORDER BY nst DESC
LIMIT 1
""",

"Tsunamis Triggered per Year":
"""
SELECT year, SUM(tsunami) AS tsunami_events
FROM earthquakes
GROUP BY year
ORDER BY tsunami_events DESC
""",

"Earthquakes by Alert Level":
"""
SELECT alert, COUNT(*) AS total
FROM earthquakes
GROUP BY alert
""",

"Deep Focus Earthquakes (>300km)":
"""
SELECT place, depth_km
FROM earthquakes
WHERE depth_km > 300
ORDER BY depth_km DESC
"""
}

# Select Query
option = st.selectbox("Select Analysis", list(queries.keys()))

# Run Button
if st.button("Run Query"):

    query = queries[option]

    df = pd.read_sql(query, conn)

    st.subheader("Query Results")
    st.dataframe(df)

  # -------- BAR CHART --------
    st.subheader("Bar Chart")

    if len(df.columns) >= 2:

        x = df.iloc[:,0]
        y = df.iloc[:,1]

        fig, ax = plt.subplots()

        ax.bar(x, y)

        ax.set_xlabel(df.columns[0])
        ax.set_ylabel(df.columns[1])
        ax.set_title(option)

        plt.xticks(rotation=45)

        st.pyplot(fig)