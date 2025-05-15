import streamlit as st
import pandas as pd
import pymysql
import matplotlib.pyplot as plt
import mysql.connector

#database connection
def create_connection():
    try:
        connection= mysql.connector.connect(
             host = "localhost",
             user = "root",
             password = "",
             port = "3307",
             database = "projects"
        )
        return connection
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

#fetch data from database
def fetch_data(query):
    connection = create_connection()
    if connection:
        mycursor = connection.cursor(buffered = True)
        mycursor.execute(query)
        columns = [i[0] for i in mycursor.description]
        rows = mycursor.fetchall()
        df = pd.DataFrame(rows, columns=columns)
        mycursor.close()
    else:
        st.error("Failed to connect to the database.")
        return pd.DataFrame()
    
    connection.close()
    return df

query = "SELECT * FROM Police_checklist"  
data = fetch_data(query)      


# Streamlit App Title
st.set_page_config(page_title="Police_stoplist Data Analysis", layout="wide")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Project Introduction", "Police_stoplist Data Visualization", "SQL Queries","A New Police Ledger For Prediction", "Creator Info"])


# PAGE 1: Introduction 
if page == "Project Introduction":
    st.title("👮 Police_stoplist Data Analysis")
    st.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRt_qh6lOu5YtKLJ1RTvJJ3lXh9dCTBGtvhPAGNLyJ9zYwQoBdkrVPaaawITNWKwl-A9hg&usqp=CAU')
    st.subheader("A Streamlit App for Exploring Police_stoplist Trends")
    st.write("""
    This project analyzes Police_stoplist data from different countries using an MYSQL database.
    It provides visualizations for violation, stop_outcome, and other Police_stoplist datas.

     **Features:**
    - View and filter Police_stoplist data by city, date, or month.
    - Generate dynamic visualizations.
    - Run predefined SQL queries to explore insights.

    **Data Used:** `police_checklist`
    """)



# PAGE 2: Police_stoplist Data Visualization
elif page == "Police_stoplist Data Visualization":
    st.title("Police_stoplist Data Visualizer")
    
    st.header("Data Overview")
    st.dataframe(data)

    st.subheader("Basic Insights")
    tab1, tab2 = st.tabs(["Stops by Violation", "Gender Distribution"])
    
    with tab1:
        if not data.empty and "Violation" in data.columns:
            violation_data = data["Violation"].value_counts().reset_index()
            violation_data.columns = ["Violation", "Count"]
            
            fig, ax = plt.subplots(figsize=(10,6))  
            colors = ["red", "green", "blue", "orange", "purple"] 
            ax.bar(violation_data["Violation"], violation_data["Count"], label="Stops by Violation", color=colors)

            ax.set_xlabel("Violation Type")
            ax.set_ylabel("Number of Stops")
            ax.set_title("Traffic Stops by Violation Type")
            ax.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            st.pyplot(fig)  
    with tab2:
        if not data.empty and "Gender" in data.columns:
            gender_data = data["Gender"].value_counts()

            fig2, ax2 = plt.subplots()
            ax2.pie(gender_data, labels=gender_data.index, autopct='%1.1f%%', startangle=90)
            ax2.set_title("Driver Gender Distribution")
            ax2.axis('equal')

            st.pyplot(fig2)        



#PAGE 3:SQL Queries
elif page == "SQL Queries":
     st.title("📋 SQL Query Results")



     queries = {
        "1. Total count of stops":"SELECT COUNT(*) FROM Police_checklist",
        "2. Top 10 vehicles involved in drug-related stops":"SELECT vehicle_number,COUNT(*) AS Stop_count FROM Police_checklist WHERE Drug_related = True GROUP BY Vehicle_number ORDER BY Stop_counT LIMIT 10",
        "3. Vehicles were most frequently searched": "SELECT Vehicle_number, COUNT(*) AS search_count FROM Police_checklist WHERE Search_conducted = 1 GROUP BY Vehicle_number ORDER BY search_count DESC LIMIT 10",
        "4. Age group that had the highest arrest rate": """SELECT age_group,COUNT(*) AS total_stops,SUM(CASE WHEN Is_arrested = 1 THEN 1 ELSE 0 END) AS total_arrests,ROUND(100 * SUM(CASE WHEN Is_arrested = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS arrest_rate_percent
                                                             FROM (SELECT *,CASE
                                                                                WHEN Age < 18 THEN 'Under 18'
                                                                                WHEN Age BETWEEN 18 AND 25 THEN '18-25'
                                                                                WHEN Age BETWEEN 26 AND 35 THEN '26-35'
                                                                                WHEN Age BETWEEN 36 AND 50 THEN '36-50'
                                                                                ELSE '51+' END AS age_group FROM Police_checklist WHERE Age IS NOT NULL) AS grouped
                                                             GROUP BY age_group ORDER BY arrest_rate_percent DESC LIMIT 1""",
        "5. Gender distribution of drivers stopped in each country":  "SELECT Country_name,Gender,COUNT(*) AS stop_count FROM Police_checklist WHERE gender IS NOT NULL AND Country_name IS NOT NULL GROUP BY Country_name, Gender ORDER BY Country_name, stop_count DESC",
        "6. Race and gender combination which has the highest search rate": """SELECT Driver_race,Gender,COUNT(*) AS total_stops,SUM(CASE WHEN Search_conducted = 1 THEN 1 ELSE 0 END) AS total_searches,ROUND(100 * SUM(CASE WHEN Search_conducted = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS search_rate_percent
                                                                               FROM Police_checklist WHERE Driver_race IS NOT NULL AND Gender IS NOT NULL GROUP BY Driver_race, Gender ORDER BY search_rate_percent DESC LIMIT 1""",
        "7. Time of day that sees most traffic stops": "SELECT HOUR(Stop_time) AS hour_of_day,COUNT(*) AS total_stops FROM Police_checklist WHERE Stop_time IS NOT NULL GROUP BY HOUR(Stop_time) ORDER BY total_stops DESC LIMIT 1",                                                                       
        "8. The average stop duration for different violations": "SELECT Violation,AVG(Stop_duration) FROM Police_checklist GROUP BY Violation ",
        "9. Are stops during the night more likely to lead to arrests?": """SELECT time_period,COUNT(*) AS total_stops,SUM(CASE WHEN Is_arrested = 1 THEN 1 ELSE 0 END) AS total_arrests,ROUND(100 * SUM(CASE WHEN Is_arrested = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS arrest_rate_percent
                                                                            FROM (SELECT *,CASE WHEN HOUR(Stop_time) BETWEEN 6 AND 19 THEN 'Day' ELSE 'Night' END AS time_period FROM Police_checklist WHERE Stop_time IS NOT NULL) AS sub GROUP BY time_period""",
        "10. Violations are most associated with searches or arrests": """SELECT Violation,COUNT(*) AS total_stops,ROUND(100 * SUM(CASE WHEN Search_conducted = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS search_rate_percent,ROUND(100 * SUM(CASE WHEN Is_arrested = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS arrest_rate_percent
                                                                          FROM Police_checklist WHERE Violation IS NOT NULL GROUP BY Violation ORDER BY search_rate_percent DESC, arrest_rate_percent DESC""",
        "11. Which violations are most common among younger drivers (<25)?": "SELECT Violation,COUNT(*) AS total_stops FROM Police_checklist WHERE Age < 25 AND Violation IS NOT NULL GROUP BY Violation ORDER BY total_stops DESC",
        "12. Is there a violation that rarely results in search or arrest?": """SELECT Violation,COUNT(*) AS total_stops,ROUND(100 * SUM(CASE WHEN Search_conducted = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS search_rate_percent,ROUND(100 * SUM(CASE WHEN Is_arrested = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS arrest_rate_percent
                                                                                FROM Police_checklist WHERE Violation IS NOT NULL GROUP BY Violation ORDER BY search_rate_percent ASC, arrest_rate_percent ASC LIMIT 1""",
        "13. Which countries report the highest rate of drug-related stops?": """SELECT Country_name,COUNT(*) AS total_stops,SUM(CASE WHEN Drug_related = True THEN 1 ELSE 0 END) AS drug_related_stops,ROUND(100 * SUM(CASE WHEN Drug_related = True THEN 1 ELSE 0 END) / COUNT(*), 2) AS drug_related_rate_percent
                                                                                  FROM Police_checklist WHERE Violation IS NOT NULL GROUP BY Country_name ORDER BY drug_related_rate_percent DESC""",
        "14. What is the arrest rate by country and violation?":  """SELECT Country_name,Violation,COUNT(*) AS total_stops,SUM(CASE WHEN Is_arrested = 1 THEN 1 ELSE 0 END) AS total_arrests,ROUND(100 * SUM(CASE WHEN Is_arrested = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS arrest_rate_percent
                                                               FROM Police_checklist WHERE Violation IS NOT NULL GROUP BY Country_name, Violation ORDER BY Country_name, arrest_rate_percent DESC""",
        "15. Which country has the most stops with search conducted?": """SELECT Country_name,COUNT(*) AS total_stops,SUM(CASE WHEN Search_conducted = 1 THEN 1 ELSE 0 END) AS total_searches,ROUND(100 * SUM(CASE WHEN Search_conducted = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS search_rate_percent
                                                                          FROM Police_checklist WHERE Search_conducted = 1 GROUP BY Country_name ORDER BY total_searches DESC""",
        "16. Yearly Breakdown of Stops and Arrests by Country":  """SELECT Year,Country_name,Total_stops,Total_arrests,ROUND(100*Total_arrests/Total_stops,2) AS Arrest_rate,SUM(Total_stops) OVER (PARTITION BY Country_name ORDER BY Year) AS Cumulative_stops,SUM(Total_arrests) OVER (PARTITION BY Country_name ORDER BY year) AS Cumulative_arrests
                                                                   FROM (SELECT YEAR(Stop_date) AS Year ,Country_name,COUNT(*) AS Total_stops,SUM(CASE WHEN Is_arrested = 1 THEN 1 ELSE 0 END) AS Total_arrests
                                                                   FROM Police_checklist GROUP BY Country_name,Year) AS Yearly_data ORDER BY Country_name,Year""",
        "17. Driver Violation Trends Based on Age and Race":  """SELECT Age_group,Driver_race,COUNT(*) AS Total_violations
                                                                 FROM (SELECT Violation,Driver_race,CASE
                                                                       WHEN Age < 18 THEN 'Under 18'
                                                                       WHEN Age BETWEEN 18 AND 25 THEN '18-25'
                                                                       WHEN Age BETWEEN 26 AND 35 THEN '26-35'
                                                                       WHEN Age BETWEEN 36 AND 50 THEN '36-50'
                                                                       'ELSE '51+' END AS Age_group 
                                                                 FROM Police_checklist) AS Grouped_data GROUP BY Age_group, Driver_race ORDER BY Age_group, Driver_race""",                   
        "18. Time Period Analysis of Stops": """SELECT DATE_FORMAT(DATE(stop_date), '%Y-%m-%d') AS Month,COUNT(*) AS Total_stops,SUM(CASE WHEN Is_arrested = 1 THEN 1 ELSE 0 END) AS Total_arrests,ROUND(100*SUM(CASE WHEN Is_arrested = 1 THEN 1 ELSE 0 END)/COUNT(*),2) AS Arrest_rate
                                                FROM Police_checklist GROUP BY Stop_date ORDER BY Month""",
        "19. Violations with High Search and Arrest Rate": """SELECT Violation,total_stops,search_rate_percent,arrest_rate_percent, RANK() OVER (ORDER BY search_rate_percent DESC, arrest_rate_percent DESC) AS rank_by_search_and_arrest
                                                              FROM(SELECT Violation,COUNT(*) AS total_stops,ROUND(100 * SUM(CASE WHEN Search_conducted = True THEN 1 ELSE 0 END) / COUNT(*), 2) AS search_rate_percent,ROUND(100 * SUM(CASE WHEN Is_arrested = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS arrest_rate_percent
                                                              FROM Police_checklist WHERE Violation IS NOT NULL GROUP BY Violation)AS GROUPED ORDER BY rank_by_search_and_arrest""",
        "20. Driver Demographics by Country": """SELECT Country_name,Driver_race,COUNT(*) AS total_stops,AVG(Age) AS avg_age,MIN(Age) AS youngest_driver,MAX(Age) AS oldest_driver,COUNT(CASE WHEN Age < 25 THEN 1 END) AS under_25,COUNT(CASE WHEN Age >= 25 AND age < 35 THEN 1 END) AS age_25_34,COUNT(CASE WHEN Age >= 35 THEN 1 END) AS age_35_and_up
                                                  FROM Police_checklist GROUP BY Country_name, Gender, Driver_race ORDER BY Country_name, Gender, Driver_race""",
        "21. Top 5 Violations with Highest Arrest Rates":  """SELECT Violation,COUNT(*) AS total_stops,SUM(CASE WHEN Is_arrested = 1 THEN 1 ELSE 0 END) AS total_arrests,ROUND(100 * SUM(CASE WHEN Is_arrested = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS arrest_rate_percent FROM Police_checklist WHERE Violation IS NOT NULL GROUP BY Violation ORDER BY arrest_rate_percent DESC"""                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
     }

     selected_query = st.selectbox("Select a query to run",list(queries.keys()))

     if st.button("Run Query"):
        with st.spinner("Running query..."):
            query_result = fetch_data(queries[selected_query])
            if not query_result.empty:
                st.write("Query result:")
                st.dataframe(query_result)
            else:
                st.warning("No data returned for this query.")


#PAGE 4: A New Police Ledger For Prediction 
elif page == "A New Police Ledger For Prediction":
    st.title("🚨 A New Police Ledger For Prediction")
    st.header("📝 Add New Police Log And Predict Violation")
    with st.form("prediction_form"):
        stop_date = st.date_input("Stop Date")
        stop_time = st.time_input("Stop Time")
        country_name = st.text_input("Country Name")
        driver_gender = st.selectbox("Driver Gender",["male","female"])
        driver_age = st.number_input("Driver Age",min_value=16,max_value=100,value=25)
        driver_race = st.text_input("Driver Race")
        search_conducted = st.selectbox("Was A Search Conducted",["0","1"])
        search_type = st.text_input("Search Type")
        drug_related = st.selectbox("Was It Drug Related",["0","1"])
        stop_duration = st.selectbox("Stop Duration",data["Stop_duration"].dropna().unique())
        vehicle_number = st.text_input("Vehicle Number")
        timestamp = pd.Timestamp.now()

        submitted = st.form_submit_button("Predict Stop Outcome & Violation")

        if submitted:
            filter_data = data[
                (data["Gender"] == driver_gender)&
                (data["Age"] == driver_age)&
                (data["Search_conducted"] == int(search_conducted))&
                (data["Stop_duration"] == stop_duration)&
                (data["Drug_related"] == int(drug_related))]

                
            if not filter_data.empty:
                predicted_outcome = filter_data['stop_outcome'].mode()[0]
                predicted_violation = filter_data['violation'].mode()[0]
            else:
                predicted_outcome = "warning"
                predicted_violation = "speeding"


            search_text = "A search was conducted" if int(search_conducted) else "No search was conducted"  
            drug_text = "was drug related" if int(drug_related) else "was not drug related"


            st.markdown(f"""
            🚨 **Prediction Summary**

            -> **Predicted Violation:** {predicted_violation}
            -> **Predicted Stop Outcome:** {predicted_outcome}

            A {driver_age}-years old {driver_gender} driver in {country_name} was stopped at {stop_time} on {stop_date}.
            {search_text}, and recieved a {predicted_outcome}. The stop lasted {stop_duration} minutes and was {drug_text}
            Vehicle Number: **{vehicle_number}**'
            """)


#PAGE 5: Creator Info            
elif page == "Creator Info":
     st.title("👩‍💻 Creator of this Project")
     st.write("**Developed by:** Thirukumaran")
     st.write("**Skills:** Python, SQL,Streamlit, Pandas")
     

         








    
