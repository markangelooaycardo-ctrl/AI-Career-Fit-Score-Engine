from streamlit import st

import requests
import time
import json

# API token for O*NET API access
ONET_TOKEN = st.secrets["ONET_TOKEN"]

# Define headers for API requests
headers = {
    "X-API-Key": ONET_TOKEN,
    "Accept": "application/json"
}

# Function to fetch all SOC codes from the O*NET API
# Each career in O*NET is identified by a unique SOC code. This function retrieves all available SOC codes for further data fetching.
def get_soc_codes():

    print("Fetching SOC codes from O*NET API...")

    # API endpoint to retrieve career data.
    careers_url = "https://api-v2.onetcenter.org/mnm/careers"

    # Handle potential errors during the API request and data extraction process.
    try:

        soc_codes = []

        # Loop through paginated results to fetch all SOC codes from the O*NET API.
        while careers_url:
            response = requests.get(careers_url, headers=headers)
            if response.status_code != 200:
                print(f"Failed to retrieve SOC codes: {response.status_code}")
                return []

            careers_data = response.json()

            for career in careers_data.get("career", []):
                soc_code = career.get("code")
                if soc_code:
                    soc_codes.append(soc_code)

            careers_url = careers_data.get("next")   # Get the next page URL if available

            print(f"Fetched {len(soc_codes)} SOC codes so far...")

        print(f"Total SOC codes fetched: {len(soc_codes)}")
        return soc_codes
    
    except Exception as e:
        print(f"An error occurred while fetching SOC codes: {e}")
        return []


# Helper function to fetch the salary data for a given SOC code from the O*NET API.
def fetch_career_salary(soc_code):

    # API endpoint to retrieve salary data for a specific career identified by its SOC code.
    salary_url = f"https://api-v2.onetcenter.org/mnm/careers/{soc_code}/job_outlook"

    # Handle potential errors during the API request and data extraction process.
    try:
        salary_response = requests.get(salary_url, headers=headers)

        if salary_response.status_code != 200:
            print(f"Salary data failed for {soc_code}: {salary_response.status_code}")
            return None
        
        # saved the salary data as a dictionary to extract the annual median salary, monthly median salary, or hourly median salary.
        salary_data = salary_response.json()
        
        salary = salary_data.get("salary", None)

        if salary.get("annual_median", None) is not None:

            return salary.get("annual_median", None)*61.46   # Conver to PHP if available
        
        elif salary.get("monthly_median", None) is not None:

            return salary.get("monthly_median", None)*12*61.46  # Covert to PHP, and to annual salary if available if salary is saved as monthly rate
        
        elif salary.get("hourly_median", None) is not None:

            return salary.get("hourly_median", None)*8*20*12*61.46  # Covert to PHP, and to annual salary if salary is saved as hourly rate
    
    except Exception as e:
        print(f"An error occurred while fetching salary data for {soc_code}: {e}")
        return None
    
# Helper function to fetch the skills data for a given SOC code from the O*NET API.
def fetch_career_skills(soc_code):

    # API endpoint to retrieve skills data for a specific career identified by its SOC code.
    skills_url = f"https://api-v2.onetcenter.org/mnm/careers/{soc_code}/skills"

    # Handle potential errors during the API request and data extraction process.
    try:
        skills_response = requests.get(skills_url, headers=headers)

        if skills_response.status_code != 200:
            print(f"Skills data failed for {soc_code}: {skills_response.status_code}")
            return None
        
        # saved the skills data as a lists of dictionary to extract the skills associated with the career.
        skills_data = skills_response.json()
        
        skills = [skill.get("name") for skill in skills_data]

        return ", ".join(skills) if skills else None # Return the skills as a comma-separated string if available, otherwise return None.
    
    except Exception as e:
        print(f"An error occurred while fetching skills data for {soc_code}: {e}")
        return None

# Helper function to fetch the details data for a given SOC code from the O*NET API.
def fetch_career_details(soc_code):

    # API endpoint to retrieve details data for a specific career identified by its SOC code.
    details_url = f"https://api-v2.onetcenter.org/mnm/careers/{soc_code}"

    # Handle potential errors during the API request and data extraction process.
    try:
        details_response = requests.get(details_url, headers=headers)

        if details_response.status_code != 200:
            print(f"Details data failed for {soc_code}: {details_response.status_code}")
            return None
        
        # saved the details data as a dictionary to extract the title and description associated with the career.
        details_data = details_response.json()
        return {"Title": details_data.get("title", ""), "Description": " ".join(details_data.get("on_the_job", []))}

    except Exception as e:
        print(f"An error occurred while fetching details data for {soc_code}: {e}")
        return None
    

# Main function to fetch the career data for a given SOC code and ID, including the title, description, skills, and salary.
def fetch_career_data(soc_code, ID):
    details = fetch_career_details(soc_code)
    skills = fetch_career_skills(soc_code)
    salary = fetch_career_salary(soc_code)

    if details is None:
        return None

    return {
        "ID": ID,
        "Title": details.get("Title", ""),
        "Description": details.get("Description", ""),
        "Skills": skills,
        "Salary": salary
    }


if __name__ == "__main__":
    all_career_data = []
    counter = 0
    
    print("Starting to fetch career data for all SOC codes...")

    # Iterate through all SOC codes and fetch the career data for each one, including the title, description, skills, and salary. 
    # The data is saved in a list of dictionaries and then written to a JSON file for further use.
    for soc_code in get_soc_codes():
        career_data = fetch_career_data(soc_code,counter)

        counter += 1

        if career_data:
            all_career_data.append(career_data)

        time.sleep(1)  # To avoid hitting the API rate limit
        print(f"Processed {counter} careers. Current SOC code: {soc_code}")

    output_file = "career_data.json"
    with open(output_file, "w") as f:
        json.dump(all_career_data, f, indent=4)