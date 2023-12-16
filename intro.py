import streamlit as st

st.set_page_config(
    page_title="BADM 54 SQL Assistant",
    page_icon="👋",
)

st.write("BADM 554 SQL Assistant 👋")

st.sidebar.success("Select a page above.")

st.markdown(
    """
    # Welcome!

    This web application is designed to enhance your learning experience in BADM 554, focusing on practical applications of SQL in business analytics.

    ## What This Tool Offers:
    - **Sales Database Assistant:** A specialized interface for exploring and querying our sales database. Perfect for exercises in data analysis and SQL query optimization.
    - **Northwind Database Assistant:** Delve into the Northwind sample database, a classic learning tool for database management and SQL queries.

    ### Getting Started:
    - **Explore Interactive SQL Queries:** Use the assistants to run real SQL queries and see instant results.
    - **Hands-On Learning:** Apply the concepts learned in BADM 554 in a practical, interactive environment.
    - **Immediate Feedback:** Experiment with different SQL queries and understand the outcomes in real-time.

    ### Navigating the Tool:
    - Use the sidebar 👈 to switch between the Sales and Northwind Database Assistants.
    - Follow the prompts and instructions on each page to guide your exploration.

    ### Enhance Your Learning:
    - Compare your query results with course materials to deepen your understanding.
    - Experiment with different query structures to see how results vary.

    **Embark on your SQL journey in BADM 554 with this interactive tool! Navigate through the pages to start exploring real-world database scenarios.**
"""
)
