import streamlit as st
import pandas as pd

# Student information
student_info = """
1,e20211125,AN HENGHENG,M
2,e20210200,BAN BUNRONG,M
3,e20210271,BO SANE,F
4,e20210320,BUN RATNATEPY,F
5,e20211081,CHAN SOPHARA,M
6,e20210871,CHEA PISETH,M
7,e20210742,CHHIN VISAL,M
8,e20211474,CHHON MENGHOUT,M
9,e20210537,CHHORN SOLITA,F
10,e20210294,CHHRAN MOSES,M
11,e20211464,CHOUV YOU Y,F
12,e20211542,CHUM RATANAKCHENTRIA,F
13,e20201096,DEN SOKUNPIDOR,M
14,e20210337,DOK DOMINIQUE,F
15,e20210085,EN SREY TOCH,F
16,e20210084,EN SREYTHOM,F
17,e20210914,ENG SIVE EU,F
18,e20211502,HAYSAVIN RONGRAVIDWIN,M
19,e20210329,HENG SEAKLONG,M
20,e20210931,HENG SOPHANHA,M
21,e20200291,HENGPA VISAL,M
22,e20210954,HUON SITHAI,M
23,e20210603,HUTH SAKDA,M
24,e20210519,ING VITOUROTANAK,M
25,e20210527,KANG PENGKHEANG,M
26,e20211040,KHEM LYHOURT,M
27,e20211015,KHOEM SIVIN,M
28,e20210176,KHON KHENGMENG,M
29,e20211527,KHUN SITHANUT,M
30,e20200497,KONG CHANRAKSA,F
31,e20210963,KONG SATTHA,M
32,e20211537,KONG SEREYRATHA,M
33,e20210574,KOSAL CHANSOTHAY,M
34,e20211754,KOUM SOKNAN,M
35,e20200014,LAB THAVRITH,M
36,e20200413,LENG MOUYHONG,M
37,e20210086,LONG RATANAKVICHEA,M
38,e20210684,LUN CHANPOLY,M
39,e20211077,LY SOKPHENG,M
40,e20210359,MA OUSA,M
41,e20210207,MAK NIMOL,F
42,e20211621,MAO SEDTHA,M
43,e20210249,MORK MONGKUL,M
44,e20210134,NGORN PANHA,M
45,e20210490,NOM MENGHOUY,F
46,e20210635,OEUN PAO,M
47,e20211548,PAV LIMSENG,M
48,e20210072,PEANG RATTANAK,M
49,e20201314,PEL BUNKHLOEM,M
50,e20211572,PEN VIRAK,M
51,e20211154,PHALLY MAKARA,M
52,e20210227,PHAO CHANTHIN,F
"""

# Parse the provided student information into a DataFrame
student_data = [line.split(",") for line in student_info.strip().split("\n")]
df_students = pd.DataFrame(student_data, columns=[
                           "Index", "ID", "Name", "Gender"])
df_students.index = df_students.index + 1  # Adjust index to start from 1
# Initialize all students as absent
df_students["Attendance Status"] = "Absence"

# Cache the DataFrame to improve app performance


@st.cache(allow_output_mutation=True)
def get_student_df():
    return df_students

# Function to reset the attendance status

def reset_table():
    st.session_state.df_students["Attendance Status"] = "Absence"
    st.experimental_rerun()

def main():

    st.set_page_config(layout="wide")  # Adjust layout to widescreen
    
    st.title("Department of Applied Mathematics and Statistics")
    st.title("Student Attendance System")
    # Initialize df_students in session state if it doesn't exist
    if 'df_students' not in st.session_state:
        st.session_state.df_students = get_student_df().copy()

    # Implement restricted access to reset functionality using a form
    with st.sidebar:
        st.write("")  # Add some space at the top
        st.subheader("Reset Attendance")
        with st.form("reset_form"):
            password = st.text_input("Enter the password:", type="password")
            submit_button = st.form_submit_button("Reset Attendance")
            if submit_button:
                if password == "e20210635":  # Check if the entered password is correct
                    reset_table()
                    st.success("Attendance has been reset.")
                else:
                    st.error("Incorrect password.")
        st.write("")  # Add some space at the bottom
    # Manual autocomplete simulation
    st.sidebar.subheader("Select Your Name")
    name_query = st.sidebar.text_input("Search your name here :")
    filtered_names = st.session_state.df_students[st.session_state.df_students["Name"].str.contains(
        name_query, case=False)]["Name"]
    selected_name = st.sidebar.selectbox(
        "Or Select your name here :", options=filtered_names)
    if selected_name:
       student_id = st.session_state.df_students.loc[st.session_state.df_students["Name"]
                                                  == selected_name, "ID"].iloc[0]
    # Display the corresponding student ID
    student_name = df_students.loc[df_students["ID"]
                                   == student_id, "Name"].iloc[0]
    st.write(
        f"**You are selecting with :**\n\nStudent Name: {student_name}\n\n Student ID: {student_id}")
    if st.sidebar.button("Submit Attendance"):
        # Check if the student has already submitted their attendance
        if st.session_state.df_students.loc[st.session_state.df_students["Name"] == selected_name, "Attendance Status"].iloc[0] == "Present":
            st.info("You have already submitted your attendance.")
            st.balloons()
        else:
            # Update the attendance status to "Present"
            st.session_state.df_students.loc[st.session_state.df_students["Name"] ==
                                             selected_name, "Attendance Status"] = "Present"
            st.success("Attendance submitted successfully.")
            st.experimental_rerun()  # Refresh data to reflect the changes immediately
    # if st.button(""):
    # # Display success message with student's name and ID
    #    st.success(f"Attendance submitted successfully for {student_name} (ID: {student_id}).")

    # No need to display the table again, as the sidebar table will automatically update

    # Display student list
    st.sidebar.subheader("Student List")
    st.sidebar.table(st.session_state.df_students[["Name", "ID", "Attendance Status"]].style.applymap(
        lambda x: 'color: red' if x.strip() == 'Absence' else 'color: blue'))

    # Add credit information
    st.markdown("---")
    st.write("Project Holder by: OEUN PAO")
    st.write("Student of Department of Applied Mathematics and Statistics, ITC")
    
if __name__ == "__main__":
    main()
