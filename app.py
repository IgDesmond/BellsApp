import pandas as pd
import streamlit as st

try:
    # Define the navigation pages
    pages = {
        "Home Page": [
            st.Page("home.py", title="Home"),
        ],
        "Sections": [
            st.Page("university.py", title="University Analytics"),
            st.Page("college.py", title="Colleges Analytics"),
            st.Page("dept.py", title="Departmental Analytics"),
            st.Page("prog.py", title="Programme Analytics"),
        ],
        "Resources": [
            st.Page("help.py", title="Help"),
        ],
    }

    # Widgets shared by all pages
    with st.sidebar:
        st.header(":red[NAVIGATION BAR]")
        
        uploaded_data = st.file_uploader("Upload your file", type={"csv"})

        if uploaded_data is not None:
            # Load the CSV data
            df = pd.read_csv(uploaded_data)

            # Ensure required columns exist
            required_columns = [
                "Degree", "State", "Department", "Program", "Admission Mode",
                "Nationality", "Marital Status", "Date of Birth"
            ]
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                st.error(f"Missing required columns: {', '.join(missing_columns)}")
            else:
                # Standardize and clean data
                df['Degree'] = df['Degree'].str.upper().str.replace(r'\W', '', regex=True)
                df['State'] = df['State'].str.upper()
                df['Department'] = df['Department'].str.upper()
                df['Program'] = df['Program'].str.rstrip()
                df['Admission Mode'] = df['Admission Mode'].str.upper()
                df['Nationality'] = df['Nationality'].str.rstrip().str.upper()
                df['Marital Status'] = df['Marital Status'].str.upper()

                # Calculate age
                df['dob'] = pd.to_datetime(df['Date of Birth'], errors='coerce')
                if df['dob'].isna().any():
                    st.warning("Some invalid dates were found in 'Date of Birth'.")
                now = pd.Timestamp('now')
                df['Age'] = ((now - df['dob']).dt.days / 365.25).astype(float).round().fillna(0).astype(int)

                # Group ages
                def group_age(ages):
                    """
                    Group ages into predefined categories.
                    """
                    grouped_ages = []
                    for age in ages:
                        if age > 19:
                            grouped_ages.append(19)
                        elif 18 <= age <= 19:
                            grouped_ages.append(18)
                        elif 17 <= age < 18:
                            grouped_ages.append(17)
                        elif 16 <= age < 17:
                            grouped_ages.append(16)
                        else:
                            grouped_ages.append(15)
                    return grouped_ages

                df['Age'] = group_age(df['Age'])

                # Share dataframe in session state
                if "shared_df" not in st.session_state:
                    st.session_state["shared_df"] = df

    # Render the navigation bar and pages
    pg = st.navigation(pages)
    pg.run()

except Exception as e:
    st.write("An error occurred: ", e)