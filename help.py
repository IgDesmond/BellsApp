import streamlit as st
import pandas as pd
from io import BytesIO

# Displaying the instructions using st.write
st.write("""
## Instructions for Using This Application

1. **Upload an Excel File**  
   Kindly upload an Excel file before performing any analytics. Use the **Upload File** section to upload your file.

2. **View Specific Analytics**  
   To view specific analytics, kindly use the **Navigation Bar**.

""")


import streamlit as st

# Streamlit app title
#st.markdown("Download Sample Excel File")

# Path to the stored Excel file
file_path = "Sample file.xlsx"  # Ensure this file exists in the app's directory

# Read the file to make it downloadable
try:
    with open(file_path, "rb") as file:
        excel_data = file.read()
        
    # Add a download button for the stored file
    st.download_button(
        label="Download Sample of an Excel File",
        data=excel_data,
        file_name="Sample file.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
except FileNotFoundError:
    st.error(f"The file '{file_path}' was not found. Please check the file path.")


st.markdown("### We hope you have a smooth experience!")