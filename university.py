import streamlit as st
import pandas as pd
import plotly.express as px  # pip install plotly-express


try:
    st.markdown(
        """
        # Welcome to Elnalitics: Empowering Student Success through Data  
        At Elnalitics, we believe data is the key to unlocking the full potential of student populations in universities.  
        Our platform provides comprehensive analytics at the **university**, **college**, and **departmental levels**,  
        helping institutions gain actionable insights to drive academic excellence, foster equity, and enhance student outcomes.  
        """,
        unsafe_allow_html=True
    )
    
    # Check if data exists in session state
    if "shared_df" in st.session_state:
        df = st.session_state["shared_df"]
    else:
        st.error("No data found. Please upload your data.")
        st.stop()

    # Analytics options
    options = [
        "Admission Mode", "Age", "Blood Group", "College", "Current Level", "Degree",
        "Denomination", "Department", "Gender", "Genotype", "Kin Relationship", 
        "Marital Status", "Religion"
    ]

    # Display summary statistics in two columns
    left_col, right_col = st.columns(2)

    with left_col:
        total_students = df.shape[0]
        st.markdown(f"### Total number of admitted students: :red[{total_students}]")

        total_departments = df["Department"].nunique()
        st.markdown(f"### Total number of Departments: :red[{total_departments}]")

        total_admission_modes = df["Admission Mode"].nunique()
        st.markdown(f"### Total number of Admission Modes: :red[{total_admission_modes}]")

    with right_col:
        total_states = df["State"].nunique()
        st.markdown(f"### Total number of States: :red[{total_states}]")

        total_programs = df["Program"].nunique()
        st.markdown(f"### Total number of Programs: :red[{total_programs}]")

        total_nationalities = df["Nationality"].nunique()
        st.markdown(f"### Total number of Nationalities: :red[{total_nationalities}]")

    st.markdown("---")

    # Multiselect for analytics
    st.markdown("## Select Parameters for Analysis")
    select_options = st.multiselect(
        "Select one or two items to perform analytics",
        options,
        max_selections=2
    )

    # Handle analytics based on selection
    if len(select_options) == 1:
        x1 = select_options[0]
        stat = df[x1].value_counts().reset_index(name="Counts")
        stat.columns = [x1, "Counts"]
        fig = px.pie(stat, values="Counts", names=x1, title=f"Distribution of {x1}")
        st.plotly_chart(fig, use_container_width=True)

    elif len(select_options) == 2:
        x1, x2 = select_options 
        stat = df.groupby([x1, x2]).size().reset_index(name="Counts")
        fig = px.bar(stat, x=x1, y="Counts", color=x2, title=f"{x1} vs {x2}")
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("Please select one or two items for analytics.")

    st.markdown("---")

    # Department and Program analytics
    st.markdown("## Department & Program Analytics")
    col1, col2 = st.columns(2)

    with col1:
        df["Department"] = df["Department"].str.upper()
        dept_stat = df["Department"].value_counts().reset_index(name="Counts")
        dept_stat.columns = ["Department", "Counts"]
        st.dataframe(dept_stat.style.highlight_max(axis=0, color="yellow"))

    with col2:
        df["Program"] = df["Program"].str.upper()
        program_stat = df["Program"].value_counts().reset_index(name="Counts")
        program_stat.columns = ["Program", "Counts"]
        st.dataframe(program_stat.style.highlight_max(axis=0, color="yellow"))

    st.markdown("---")

    # State distribution analytics
    st.markdown("## State Analytics")
    chart_type = st.selectbox("Choose chart type for state distribution", ["Bar", "Table"])

    df["State"] = df["State"].str.upper()
    state_stat = df["State"].value_counts().reset_index(name="Counts")
    state_stat.columns = ["State", "Counts"]

    if chart_type == "Bar":
        fig = px.bar(state_stat, x="Counts", y="State", title="State Distribution")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.dataframe(state_stat.style.highlight_max(axis=0, color="yellow"))

    st.markdown("---")


except Exception as e:
    st.error(f"An error occurred: {e}")
