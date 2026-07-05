# Download the required libraries
# !pip install streamlit
# !pip install huggingface_hub
import streamlit as st
import time

# Call the generate_career_assessment and get_top_job_matches functions from the LLM_module and embeddings_module respectively.
from LLM_module import generate_career_assessment
from embeddings_module import get_top_job_matches

#The title at the tab of the web app
st.set_page_config(page_title="AI Career Fit Score Engine", layout="centered")


# Creates a session state variable to track the current page of the app. If it doesn't exist, it initializes it to "Home".
if "App_page" not in st.session_state:
    st.session_state["App_page"] = "Home"

# Function to switch the app page to "Analytics/ AI careef fit score"
def switch_to_analytics():
    st.session_state["App_page"] = "Analytics"

# Function to switch the app page back to "Home"
def switch_to_home():
    st.session_state["App_page"] = "Home"


# This block of code is executed when the current page is "Home". 
# It creates a form for users to input their academic and professional profiles.
if st.session_state["App_page"] == "Home":
    with st.form(key="profile_form", clear_on_submit=False):

        # Title and description of the app
        st.title("AI Career Fit Score Engine")
        st.write("Please provide your academic and professional profiles below to run a compatibility analysis.")

        # Subheader for personal information section
        st.subheader("Personal Information")
        skills = st.text_input("Skills", placeholder="e.g., Python, Machine Learning, Data Analysis, etc.", key="skills")
        preferred_work_location = st.selectbox("Preferred Work Location", [
        "NCR - National Capital Region",
        "CAR - Cordillera Administrative Region",
        "Region I - Ilocos Region",
        "Region II - Cagayan Valley",
        "Region III - Central Luzon",
        "Region IV-A - CALABARZON",
        "Region IV-B - MIMAROPA",
        "Region V - Bicol Region",
        "Region VI - Western Visayas",
        "Region VII - Central Visayas",
        "Region VIII - Eastern Visayas",
        "Region IX - Zamboanga Peninsula",
        "Region X - Northern Mindanao",
        "Region XI - Davao Region",
        "Region XII - SOCCSKSARGEN",
        "Region XIII - Caraga",
        "BARMM - Bangsamoro Autonomous Region in Muslim Mindanao"], key="preferred_work_location")

        # Subheader for academic profile section
        st.subheader("Academic Profile")
        academic_degree = st.selectbox("Highest Academic Degree", ["High School", "Bachelor's", "Master's", "PhD"], key="academic_degree")
        field_of_study = st.text_input("Field of Study", placeholder="e.g., Computer Engineering, Computer Science, etc.", key="field_of_study")
        university_name = st.text_input("University Name", placeholder="e.g., Mapua University, MIT, etc.", key="university_name")
        gpa =st.slider("GPA (0.0 - 5.0) 5 being the highest", min_value=0.0, max_value=5.0, step=0.01, key="gpa")

        # Subheader for professional profile section
        st.subheader("Professional Profile")
        previous_roles = st.text_input("Previous Roles", placeholder="e.g., Software Engineer, Data Scientist, etc.", key="previous_roles")
        years_of_experience = st.number_input("Years of Professional Experience", min_value=0, step=1, key="years_of_experience")
        previous_salary = st.number_input("Previous Annual Salary (in PHP)", min_value=0, step=1000, key="previous_salary")

        # For validation, we can check if the required fields are filled before allowing submission.
        required_fields = [skills, preferred_work_location, academic_degree, field_of_study, university_name, previous_roles]
        

        submit_button = st.form_submit_button("Submit Profile")
    
    # This block of code is executed when the user clicks the "Submit Profile" button.
    # Will check if all required fields are filled. If they are, it will display a success message and redirect to the "Analytics" page.
    # If not all required fields are filled, it will display an error message prompting the user to fill in all required fields.
    if submit_button:
        if all(required_fields):
            st.success("Profile submitted successfully! Redirecting to Analytics...")
            time.sleep(1)  # Simulate a delay for redirection
            switch_to_analytics()
            st.rerun()
        else:
            st.error("Please fill in all the required fields before submitting your profile.")

# This block of code is executed when the current page is "Analytics".
if st.session_state["App_page"] == "Analytics":
    st.title("AI Career Fit Score Engine - Analytics")

    # Create a dictionary to store the user's profile information obtained from the home page.
    user_profile = {
        "Skills": st.session_state["skills"],
        "Preferred Work Location": st.session_state["preferred_work_location"],
        "Academic Degree": st.session_state["academic_degree"],
        "Field of Study": st.session_state["field_of_study"],
        "University Name": st.session_state["university_name"],
        "GPA": st.session_state["gpa"],
        "Previous Roles": st.session_state["previous_roles"],
        "Years of Experience": st.session_state["years_of_experience"],
        "Previous Salary": st.session_state["previous_salary"]
        }
    
    career_assessment = {}
    top_matches = []
    
    # Shows the status of the data fetching and analysis process to the user.
    with st.status("Analyzing your profile and the top 5 job matches..."):
        st.write("Finding relevant job matches...")
        top_matches = get_top_job_matches(user_profile, top_k=5)
        st.write("LLM is analyzing your profile and the top 5 job matches...")
        career_assessment = generate_career_assessment(user_profile, top_matches)
        st.write("Analysis complete! Displaying results below...")
        

    best_career_match = career_assessment.get("best_career_match", {}) #type: ignore
    career_ranking = career_assessment.get("career_ranking", []) #type: ignore


    # Display the best career match and the ranking of the top 5 job matches based on the fit score.
    st.header("Best Career Match")

    st.subheader(f"**Job Title:** {best_career_match['job_title']}")

    st.subheader(f"**Fit Score:** {best_career_match['fit_score']*100:.2f}%") #Display the fit score as a percentage.
    st.progress(best_career_match['fit_score']) # Display a progress bar representing the fit score as a percentage.
    
    st.subheader("**Why this job was selected:**") # Display the reason why this job was selected as the best career match.
    st.write(best_career_match.get("why", "N/A"))

    st.subheader("**Matching Skills:**") # Display the matching skills between the user's profile and the best career match.
    matching_skills = best_career_match.get("matching_skills", [])
    st.write(", ".join(matching_skills) if matching_skills else "No matching skills found.")
    
    st.subheader("**Missing Skills:**") # Display the missing skills between the user's profile and the best career match.
    missing_skills = best_career_match.get("missing_skills", [])
    st.write(", ".join(missing_skills) if missing_skills else "No missing skills found.")
    
    st.subheader("**Recommendations for Improving Fit:**") # Display recommendations for improving the fit between the user's profile and the best career match.
    st.write("\n".join(best_career_match.get("recommendations", [])) if best_career_match.get("recommendations") else "No recommendations available.")
    

    st.header("Career Ranking")
    # Create containers for each of the top 5 job matches to display their details in a structured format.
    jobct1 = st.container(border=True)
    jobct2 = st.container(border=True)
    jobct3 = st.container(border=True)
    jobct4 = st.container(border=True)
    jobct5 = st.container(border=True)

    containers = [jobct1, jobct2, jobct3, jobct4, jobct5]

    # Display the ranking of the top 5 job matches based on the fit score.
    for jobct, job in zip(containers, career_ranking):
        with jobct:
            st.subheader(f"**Rank {job.get('rank', 'N/A')}: {job.get('job_title', 'N/A')}**")
            st.subheader(f"**Fit Score:** {job.get('fit_score', 0)*100:.2f}%")
            st.progress(job.get('fit_score', 0))
            st.write(f"**Why:** {job.get('reason', 'N/A')}")
            if job.get('salary') is not None:
                st.metric("Annual Salary", 
                      f"PHP {job.get('salary', 'N/A'):,.2f}", 
                      f"{job.get('salary', 'N/A') - user_profile.get('Previous Salary', 0):,.2f} PHP change from previous salary")
            else:
                st.write("**Salary:** Not available")
            
    # If pressed, it will switch the page back to the home page where the user can input their profile again.
    st.button("Back to Home", on_click=switch_to_home)