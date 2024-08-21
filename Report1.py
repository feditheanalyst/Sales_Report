import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as style
from sqlalchemy import create_engine 
import plotly.graph_objects as go
import plotly.express as px
from prophet import Prophet 
from prophet.plot import plot_plotly, plot_components_plotly 

# # Header/Title of report
# pagetitle = "Sales Report"
# st.set_page_config(page_title = pagetitle, layout = "wide")
# st.title(pagetitle)

# Header/Title of report
pagetitle = "Sales Report"
st.set_page_config(page_title=pagetitle, layout="wide")
# Create a container for the title
title_container = st.container()
# Add HTML Title with CSS Styling
with title_container:
    title_html = """
    <h1 style="text-align: center;">""" + pagetitle + """</h1>
    """
    st.markdown(title_html, unsafe_allow_html=True)


# Loading the data
df = pd.read_csv("./sales_df.csv")
# st.dataframe(df.head())


with st.container():
    st.write("The chart highlights that the majority of the profit is generated by the Adults (35-64) and Young Adults (25-34) age groups, with the Adults group being the most profitable. The Youth (<25) group contributes a moderate amount, while the Seniors (64+) group generates the least profit.")
    # Create two columns for layout
    col1, col2= st.columns(2)
    # customer segmentation by profit
    with col1:
        grp1 = df.groupby(["Age_Group"])
        df2 = grp1["Profit"].sum().reset_index().rename(columns={'Profit': 'Total Profit'})
        df2 = df2.sort_values(by="Total Profit", ascending=True)  # Ensure ascending sort

        # Create interactive bar chart with Plotly Express
        fig = px.bar(
            df2,
            x="Total Profit",  # Use correct column name for x-axis
            y="Age_Group",
            title="Customer Segmentation by Profit",
            color="Total Profit",  # Color based on profit for visual emphasis
            orientation="h",  # Horizontal bars for readability
            template="plotly_white",  # Optional theme for aesthetics
        )
        fig.update_layout(yaxis_title="Age Group", xaxis_title="Total Profit", height=500)  # Update axis labels
        st.plotly_chart(fig)

        # grp1 = df.groupby(["Age_Group"])
        # df2 = grp1["Profit"].sum().reset_index().rename(columns={'Profit': 'Profit'})
        # df2 = df2.sort_values(by= "Profit", ascending= True)
        # style.use("fivethirtyeight")
        # a = df2["Age_Group"].tolist()
        # b = df2["Profit"].tolist()
        # plt.barh(a, b, color = "g")
        # plt.ylabel("Age Group")
        # plt.xlabel("Profit")
        # plt.title("Customer Segmentation by Profit")
        # plt.show() 

    with col2:

        st.write("**Detailed Breakdown:**")
        st.write("1. **Adults (35-64)**: This age group generates the highest profit, reaching approximately 20 million. The bar representing this group is colored bright yellow, indicating the maximum profit range on the color gradient.")
        st.write("2. **Young Adults (25-34)**: The second highest profit comes from this age group, with a total profit close to 15 million. The bar is colored orange, which corresponds to the mid-to-high range on the color gradient.")
        st.write("3. **Youth (<25)**: This group contributes a moderate profit, around 10 million. The bar is colored purple, indicating a mid-range profit on the color gradient.")
        st.write("4. **Seniors (64+)**: This age group generates the least profit, with the bar barely extending beyond the 0 mark, indicating a profit close to 5 million. The bar is colored dark blue, representing the lowest range on the color gradient.")



    # The second chart/analysis
    # Create columns for layout
    col1, col2 = st.columns(2)

    # Display title or content in the first column (optional)
    with col1:
        st.write("The chart highlights that the most products were Accessories having a count value of 1,054,162 followed by the Clothings having a count value of 254,743 and bikes having the least count with a value of 36,411")
        
        st.write("1. **Accessories**:  With a whopping 1,054,162 orders, accessories hold the dominant position in terms of customer demand within the data set. This high order quantity suggests a clear customer preference for accessories compared to bikes and clothing.")
        st.write("2. **Clothing**:  Clothing has an order quantity of 254,743. Compared to accessories, this represents a significant gap (799,419 fewer orders). While not as dominant as accessories, clothing still holds a notable position in terms of order quantity. This suggests a strong customer base interested in apparel items.")
        st.write("3. **Bikes**:  Bikes have the lowest order quantity of 36,411. Compared to accessories and clothing, bikes have a considerably lower order count.")

    # Order Quantity Analysis
    with col2:
        grp2 = df.groupby(["Product_Category"])
        df3 = grp2["Order_Quantity"].sum().reset_index().rename(columns={'Order_Quantity': 'Total Orders'})
        df3 = df3.sort_values(by="Total Orders", ascending=True)  # Ensure ascending sort

        # Create interactive bar chart with Plotly Express
        fig = px.bar(
            df3,
            x="Product_Category",
            y="Total Orders",
            title="Order Quantity Count by Product Category",
            color="Total Orders",  # Color based on order quantity for emphasis
            template="plotly_white",  # Optional theme for aesthetics
        )
        fig.update_layout(yaxis_title="Total Orders", xaxis_title="Product Category")
        st.plotly_chart(fig)


    st.write("Below shows the total profit and revenue for each of the months. With july having the all time low in profit and revenue with **2.8 million** and **6.39 million** respectively and December having the all time high in both profit and revenue with over **4.4 million** and **10.1 million** respectively")
    # Create columns for layout
    col1, col2 = st.columns(2)
    with col1:
        # Group by month and calculate total profit
        grp = df.groupby(["Month"])
        df4 = (
            grp["Profit"]
            .sum()  # Calculate total profit for each month
            .reset_index()  # Convert the grouped data back to a DataFrame
            .rename(columns={"Profit": "Total Profit"})  # Rename the column
        )

        # Map month names to numerical order (optional)
        month_map = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
                    "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
        df4["Month_Number"] = df4["Month"].apply(lambda x: month_map.get(x))  # Replace month names with numerical order (optional)

        # Sort DataFrame by month number (or original month if not mapped)
        df4 = df4.sort_values(by="Month_Number", na_position="last")  # Sort by numerical month (or original month if missing)

        # Reset index (optional)
        df4 = df4.reset_index(drop=True)
        # Create Plotly bar chart
        fig = px.line(
            df4,  
            x="Month", 
            y="Total Profit", 
            title="Total Profit per Month",
            labels={"Month": "Month", "Total Profit": "Total Profit"}  # Customize axis labels
        )
        st.plotly_chart(fig)

    with col2:
        # Group by month and calculate total profit
        grp = df.groupby(["Month"])
        df5 = (
            grp["Revenue"]
            .sum()  # Calculate total profit for each month
            .reset_index()  # Convert the grouped data back to a DataFrame
            .rename(columns={"Revenue": "Total Revenue"})  # Rename the column
        )

        # Map month names to numerical order (optional)
        month_map = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
                    "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
        df5["Month_Number"] = df5["Month"].apply(lambda x: month_map.get(x))  # Replace month names with numerical order (optional)

        # Sort DataFrame by month number (or original month if not mapped)
        df5 = df5.sort_values(by="Month_Number", na_position="last")  # Sort by numerical month (or original month if missing)

        # Reset index (optional)
        df5 = df5.reset_index(drop=True)
        # Create Plotly bar chart
        fig = px.line(
            df5,  # Pass the DataFrame directly to Plotly Express
            x="Month",  # Set the x-axis based on the "Month" column
            y="Total Revenue",  # Set the y-axis based on the "Total Profit" column
            title="Total Revenue per Month",
            labels={"Month": "Month", "Total Revenue": "Total Revenue"},
            width= 700 # Customize axis labels
        )

        # Display the Plotly chart
        # (assuming you're using Streamlit or another framework)
        st.plotly_chart(fig)