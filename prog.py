
import streamlit as st 
import plotly.express as px  # pip install plotly-express

try:
    # Header Section
    st.markdown(
        """
        # Welcome to Elnalitics: Empowering Student Success through Data  
        At Elnalitics, we believe data is the key to unlocking the full potential of student populations in universities.  
        Our platform provides comprehensive analytics at the **university**, **college**, and **departmental levels**,  
        helping institutions gain actionable insights to drive academic excellence, foster equity, and enhance student outcomes.  
        """,
        unsafe_allow_html=True
    )

    # Load Data
    if "shared_df" in st.session_state:
        df = st.session_state["shared_df"]
    else:
        st.error("No data found. Please upload your data.")
        st.stop()


    departments = [
        "AGRICULTURE AND AGRICULTURAL TECHNOLOGY","BIOLOGICAL SCIENCES", "BUSINESS ADMINISTRATION", 
        "CHEMICAL SCIENCES", "COMPUTER SCIENCE AND INFORMATION TECHNOLOGY", "ECONOMICS, ACCOUNTING AND FINANCE", 
        "ELECTRICAL ELECTRONICS AND TELECOMMUNICATION ENGINEERING", "FOOD SCIENCE AND TECHNOLOGY", "MANAGEMENT TECHNOLOGY",
        "PHYSICAL SCIENCES",
    ]

 
    selected_dept = st.multiselect(
        "Select a department to perform analytics",
        departments,
        default=["AGRICULTURE AND AGRICULTURAL TECHNOLOGY"],
        max_selections=1
    )

    # Ensure a department is selected
    if not selected_dept:
        st.warning("Please select a department to proceed.")
        st.stop()

    st.success(f"You selected: {selected_dept[0]}")


    left_col, right_col = st.columns(2)
    df = df[df.Department == selected_dept[0]]

    with left_col:
        total_students = df.shape[0]
        st.markdown(f"### Total number of admitted students: :red[{total_students}]")

        admission_modes = df["Admission Mode"].nunique()
        st.markdown(f"### Total number of Admission Modes: :red[{admission_modes}]")

    with right_col:
        states = df["State"].nunique()
        st.markdown(f"### Total number of States: :red[{states}]")

        programs = df["Program"].nunique()
        st.markdown(f"### Total number of Programs: :red[{programs}]")

        nationalities = df["Nationality"].nunique()
        st.markdown(f"### Total number of Nationalities: :red[{nationalities}]")

    st.markdown("---")
   
    # Analytical Options
    opt = [
        "Admission Mode", "Age", "Blood Group", "Current Level", "Degree", "Denomination",
        "Gender", "Genotype", "Kin Relationship", "Marital Status", "Religion"
    ]

    select_opt = st.multiselect(
        "Select one or two items to perform analytics",
        opt,
        max_selections=2
    )

    # Generate Analytics
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
        st.warning("Select one or two items to generate analytics.")

    st.markdown("---")
    st.markdown(f"### Programs in the Department of {selected_dept[0]}")
    programs = df["Program"].unique()
    st.write(programs)


    st.markdown("---")
    lcol, Rcol = st.columns([2,1])
    with lcol:
    # State Distribution Chart
        chart_type = st.selectbox("Choose chart type for State Distribution", ["Bar", "Table"])

        df["State"] = df["State"].str.upper()  # Convert to uppercase
        state_stat = df["State"].value_counts().reset_index(name="Counts")
        state_stat.columns = ["State", "Counts"]

        if chart_type == "Bar":
            fig = px.bar(state_stat, x="Counts", y="State", title="State Distribution")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.dataframe(state_stat.style.highlight_max(axis=0, color="yellow"))

        st.markdown("---")
    
        # st.markdown(f"### States of Origin of admitted students in the Department of {selected_dept[0]}")
        # states = df["State"].unique()
        # st.write(states)

except Exception as e:
    st.error(f"An error occurred: {e}")
