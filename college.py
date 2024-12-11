import streamlit as st   
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

    # College options
    options = [
        "College Of Engineering",
        "College Of Environmental Sciences",
        "College Of Food, Agricultural Science And Technology",
        "College of Management Sciences",
        "College of Natural and Applied Sciences",
    ]

    # Multiselect with a default value
    select_options = st.multiselect(
        "Select one or two items to perform analytics",
        options,
        default=["College Of Engineering"],
        max_selections=1
    )

    # Check if a value is selected
    if not select_options:
        st.warning("Please select a value to proceed.")
        st.stop()

    st.success(f"You selected: {select_options[0]}")
    college = select_options[0]

    # Filter dataframe by selected college
    df = df[df.College == college]

    # Display statistics
    left_col, right_col = st.columns(2)

    with left_col:
        rows, _ = df.shape
        st.markdown(f"### Total number of admitted students: :red[{rows}]")

        total_departments = df['Department'].nunique()
        st.markdown(f"### Total number of Departments: :red[{total_departments}]")

        total_admission_modes = df['Admission Mode'].nunique()
        st.markdown(f"### Total number of Admission Modes: :red[{total_admission_modes}]")

    with right_col:
        total_states = df['State'].nunique()
        st.markdown(f"### Total number of states: :red[{total_states}]")

        total_programs = df['Program'].nunique()
        st.markdown(f"### Total number of Programs: :red[{total_programs}]")

        total_nationalities = df['Nationality'].nunique()
        st.markdown(f"### Total number of Nationalities: :red[{total_nationalities}]")

    st.markdown("---")

    # Analytics options
    opt = [
        "Admission Mode", "Age", "Blood Group", "Current Level", "Degree", 
        "Denomination", "Department", "Gender", "Genotype", "Kin Relationship", 
        "Marital Status", "Religion"
    ]

    select_opt = st.multiselect(
        "Select one or two items to perform analytics",
        opt,
        max_selections=2
    )

    # Handle analytics based on selection
    if len(select_opt) == 1:
        x1 = select_opt[0]
        stat = df[x1].value_counts().reset_index(name="Counts")
        stat.columns = [x1, "Counts"]
        fig = px.pie(stat, values="Counts", names=x1, title=f"Distribution of {x1}")
        st.plotly_chart(fig, use_container_width=True)

    elif len(select_opt) == 2:
        x1, x2 = select_opt
        stat = df.groupby([x1, x2]).size().reset_index(name="Counts")
        fig = px.bar(stat, x=x1, y="Counts", color=x2, title=f"{x1} vs {x2}")
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("Please select one or two items for analytics.")

    st.markdown("---")

    # Department and program data display
    col1, col2 = st.columns(2)
    with col1:
        df['Department'] = df['Department'].str.upper()
        department_stat = df['Department'].value_counts().reset_index(name="Counts")
        department_stat.columns = ['Department', 'Counts']
        st.dataframe(department_stat.style.highlight_max(axis=0, color='yellow'))

    with col2:
        df['Program'] = df['Program'].str.upper()
        program_stat = df['Program'].value_counts().reset_index(name="Counts")
        program_stat.columns = ['Program', 'Counts']
        st.dataframe(program_stat.style.highlight_max(axis=0, color='yellow'))

    st.markdown("---")

    # State distribution visualization
    chart_type = st.selectbox('Choose another chart view for state distribution', ['Bar', 'Table'])
    df['State'] = df['State'].str.upper()
    state_stat = df['State'].value_counts().reset_index(name="Counts")
    state_stat.columns = ['State', 'Counts']

    if chart_type == 'Bar':
        fig = px.bar(state_stat, x='Counts', y='State', title='State Distribution')
        st.plotly_chart(fig, use_container_width=True)
    elif chart_type == 'Table':
        st.dataframe(state_stat.style.highlight_max(axis=0, color='yellow'))

    st.markdown("---")

except Exception as e:
    st.error(f"An error occurred: {e}")


