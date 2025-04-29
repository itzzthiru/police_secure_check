# police_secure_check
Police Stoplist Data Analysis Web App:
This project is a Streamlit-based web application that analyzes Police Stoplist data sourced from a MySQL database. It provides visualizations, data exploration tools, predictive features, and direct SQL querying — all through an interactive interface.

Features:
Dashboard Navigation: Move between different sections easily using a sidebar.

Project Introduction: Overview of the purpose and functionalities.

Data Visualization:

Explore traffic stops categorized by violation type.

View gender distribution of drivers.

SQL Query Execution:

Predefined SQL queries for deep insights (e.g., most searched vehicles, drug-related stop rates, arrest trends by age group, etc.).

New Ledger & Prediction Tool:

Add a new police stop record.

Predict the likely violation type and stop outcome based on provided attributes (driver age, search conducted, drug-related status, etc.).

Tech Stack:
Python

Streamlit (Frontend)

Pandas (Data Manipulation)

MySQL Connector (Database Connection)

Matplotlib (Visualization)

MySQL (Backend Database)

How to Run:
Install Required Libraries:

pip install streamlit pandas mysql-connector-python matplotlib
Set up MySQL:

Ensure you have a MySQL server running.

Create a database named projects.

Create and populate a table Police_checklist.

Run the App:

streamlit run police_checklist.py
Interact with the app:

Browse data

Generate graphs

Run SQL queries

Simulate a new police stop entry and get predictive outcomes

Sample Visualizations:
Bar Chart: Number of traffic stops by violation type.

Pie Chart: Gender distribution among stopped drivers.

Author:
Name: Thirukumaran

Skills: Python, SQL, Streamlit, Pandas.
