import requests
import streamlit as st
from WindSpeed import get_climate_data
from GoogleScrapper import PermitTimeFrameFetcher
from get_bio_diversity_data import get_bio_diversity_data
from LatestSoilData import Findmain
from single import calculate_esg_score


def suggest_alternative_locations():
    # Main locations and scores
    locations = [
        {"Rank": 1, "Location": "Mojave Desert, California", "Suitability Score": 92.32},
        {"Rank": 2, "Location": "West Texas", "Suitability Score": 91.89},
        {"Rank": 3, "Location": "Gila Bend, Arizona", "Suitability Score": 91.55},
    ]

    # Alternative suggestion
    alternative_location = {
        "Location": "Desert Center, California",
        "Reason": "High solar irradiance, flat terrain, and proximity to infrastructure.",
        "Suitability Score": 91.00,
    }

    # Generate the table rows as HTML
    table_rows = ""
    for loc in locations:
        table_rows += f"""
        <tr style='border-bottom: 1px solid #ddd;'>
            <td style='padding: 10px;'>{loc['Rank']}</td>
            <td style='padding: 10px;'>{loc['Location']}</td>
            <td style='padding: 10px;'>{loc['Suitability Score']}</td>
        </tr>
        """

    # Display the main table in a box
    st.markdown("### 🌞 Suggested Locations for Solar Farms")
    st.markdown(
        f"""
        <div style='border: 2px solid #4CAF50; padding: 15px; border-radius: 10px; background-color: #f9f9f9;'>
        <table style='width: 100%; border-collapse: collapse;'>
            <tr style='background-color: #4CAF50; color: white;'>
                <th style='padding: 10px; text-align: left;'>Rank</th>
                <th style='padding: 10px; text-align: left;'>Location</th>
                <th style='padding: 10px; text-align: left;'>Suitability Score</th>
            </tr>
            {table_rows}
        </table>
        </div>
        """,
        unsafe_allow_html=True,  # Ensures proper HTML rendering
    )

    # Display the alternative location
    st.markdown("### 🌟 Alternative Suggested Location")
    st.markdown(
        f"""
        <div style='border: 2px dashed #FFA500; padding: 15px; border-radius: 10px; background-color: #fffaf0;'>
            <strong>Location:</strong> {alternative_location['Location']}<br>
            <strong>Reason:</strong> {alternative_location['Reason']}<br>
            <strong>Suitability Score:</strong> {alternative_location['Suitability Score']}
        </div>
        """,
        unsafe_allow_html=True,  # Ensures proper HTML rendering
    )

def get_alternative_projects():
    # Top 3 renewable energy sources for New York
    renewable_sources = [
        {
            "Source": "Offshore Wind Energy",
            "Description": "New York’s coastal waters offer substantial potential for offshore wind farms, leveraging consistent wind patterns to generate clean energy.",
        },
        {
            "Source": "Hydropower",
            "Description": "Utilizing existing resources like the Niagara Falls hydroelectric plant and exploring small-scale hydropower systems in other parts of the state.",
        },
        {
            "Source": "Solar Rooftop Installations",
            "Description": "Focused on urban rooftops, commercial buildings, and residential areas to harness solar energy without requiring large land areas.",
        },
    ]

    # Display the renewable energy sources
    st.markdown("### 🌟 Top 3 Renewable Energy Sources for New York")
    for source in renewable_sources:
        st.markdown(
            f"""
            <div style='border: 2px solid #4CAF50; padding: 15px; border-radius: 10px; background-color: #f9f9f9; margin-bottom: 15px;'>
                <strong>Source:</strong> {source['Source']}<br>
                <strong>Description:</strong> {source['Description']}
            </div>
            """,
            unsafe_allow_html=True,  # Ensures proper HTML rendering
        )

st.title("Energy Project Developer ESG Survey")

def display_dict_data(title, data):
    with st.expander(title):
        for key, value in data.items():
            col1, col2 = st.columns([1, 3])
            col1.markdown(f"**{key}**")
            col2.markdown(f"{value}")

def display_timeline(content, bg_color="#e6e6fa", heading_color="#6a0dad", text_color="#333"):
    """
    Display a timeline box that dynamically adjusts to fit all the content.
    """
    st.markdown(
        f"""
        <div style="
            background-color: {bg_color};
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #d3d3d3;
            font-family: Arial, sans-serif;
            margin-bottom: 15px;
            overflow-wrap: break-word;
            word-wrap: break-word;
            word-break: break-word;
        ">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <span style="font-size: 18px; margin-right: 10px;">⏰</span>
                <h4 style="margin: 0; color: {heading_color}; font-size: 18px;">Timeline</h4>
            </div>
            <p style="margin: 0; font-size: 16px; color: {text_color}; line-height: 1.5;">
                {content}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


def display_tip(content, bg_color="#d4edda", heading_color="#155724", text_color="#333"):
    """
    Display a tip box that dynamically adjusts to fit all the content.
    """
    st.markdown(
        f"""
        <div style="
            background-color: {bg_color};
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #c3c3c3;
            font-family: Arial, sans-serif;
            margin-bottom: 15px;
            overflow-wrap: break-word;
            word-wrap: break-word;
            word-break: break-word;
        ">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <span style="font-size: 18px; margin-right: 10px;">💡</span>
                <h4 style="margin: 0; color: {heading_color}; font-size: 18px;">Tip</h4>
            </div>
            <p style="margin: 0; font-size: 16px; color: {text_color}; line-height: 1.5;">
                {content}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

def display_dict(data, bg_color="#f0f8ff", key_color="#0056b3", value_color="#333"):
    html_content = f"""
    <div style="
        background-color: {bg_color};
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #d1d1d1;
        font-family: Arial, sans-serif;
        margin-bottom: 15px;
    ">
        <table style="width: 100%; border-spacing: 10px;">
    """
    for key, value in data.items():
        html_content += f"""
        <tr>
            <td style="font-weight: bold; color: {key_color}; text-align: left; width: 30%;">{key}</td>
            <td style="color: {value_color}; text-align: left; width: 70%;">{value}</td>
        </tr>
        """
    html_content += "</table></div>"
    
    # Enable HTML rendering in Streamlit
    st.markdown(html_content, unsafe_allow_html=True)


def get_suggestions(query):
    """Fetch location suggestions from Nominatim API."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "addressdetails": 1,
        "limit": 5,  # Limit the number of suggestions
    }
    headers = {
        "User-Agent": "YourAppName/1.0 (your_email@example.com)"  # Replace with your app name and email
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    return []


# Initialize session state
if "submitted" not in st.session_state:
    st.session_state.submitted = False


def handle_submission(responses, selected_location, project_name, project_type):
    """Handle form submission and update session state."""
    st.session_state.submitted = True
    st.session_state.project_name = project_name
    st.session_state.project_type = project_type
    st.session_state.project_location = selected_location["display_name"]
    st.session_state.state = selected_location.get("address", {}).get("state", "State not found")
    st.session_state.lan = float(selected_location["lat"])
    st.session_state.lon = float(selected_location["lon"])
    st.session_state.responses = responses


# Display form only if not submitted
if not st.session_state.submitted:
    # Project Details
    st.header("Project Information")
    project_name = st.text_input("Project Name:")
    st.header("Project Location")
    location_query = st.text_input("Type to search for a location:")
    selected_location = None

    if location_query:
        suggestions = get_suggestions(location_query)
        if suggestions:
            options = [f"{loc['display_name']}" for loc in suggestions]
            selected_option = st.selectbox("Suggestions:", options, key="location_selection")
            selected_location = next((loc for loc in suggestions if loc["display_name"] == selected_option), None)
        else:
            st.warning("No suggestions found. Try refining your search.")

    project_type = st.selectbox(
        "Project Type:",
        [
            "Solar Farm",
            "Wind Farm",
            "Hydropower Plant",
            "Geothermal Plant",
            "Biomass Energy Plant",
            "Tidal Energy Plant",
            "Wave Energy Plant",
            "Other",
        ],
    )

    # Budget and land area
    st.header("Project Budget and Land")
    col1, col2, col3 = st.columns([3, 2, 2])
    with col1:
        project_budget = st.text_input("Project Budget (in USD):", placeholder="Enter budget")
    with col2:
        budget_exceedance = st.text_input("Exceedable By (in USD):", placeholder="Enter amount")
    with col3:
        land_area = st.text_input("Land Area (in Acres):", placeholder="Enter acres")

    # Define questions grouped by subtopics
    survey_data = {
        "Standard ESG Variables": [
            "Does the project have a materials recycling program?",
            "Does the project follow wage standards that meet or exceed the Davis-Bacon Act guidelines?",
            "Does the project have an apprenticeship program?",
            "Are vendors educated about ESG guidelines or given any specific ESG-related requirements?",
            "Is there any monitoring of or reporting from vendors required in relation to ESG requirements?",
            "Does the project implement energy efficiency measures, such as using renewable energy sources or optimizing energy use?",
            "Is there a biodiversity impact assessment conducted, and are there measures in place to mitigate negative impacts on local ecosystems?",
            "Are there programs in place for community engagement or contributions to local social initiatives?",
            "Does the project have a system in place to monitor and report greenhouse gas emissions?",
            "Are there measures to ensure ethical sourcing of materials, including rare earth elements, and how is this monitored?",
            "Are ESG principles formalized in project documentation, such as an ESG manual or employee handbook?",
            "Are there obligations written into the project finance documents that require certification, representations, or reporting to project funding partners regarding ESG compliance?",
            "Does the project include a formal human rights policy, particularly in relation to labor practices and supply chain management?",
            "Is there a diversity and inclusion policy in place?",
            "Are there any certifications or audits required by third parties to validate ESG practices?",
        ],
        "European ESG Requirements": [
            "Does the project align with the EU Taxonomy for sustainable activities?",
            "Is compliance documented?",
            "Are there specific measures in place to address the EU’s Corporate Sustainability Reporting Directive (CSRD) requirements?",
            "How does the project ensure alignment with the EU’s Green Deal, particularly in terms of reducing carbon emissions?",
            "Are there mechanisms for stakeholder engagement, including reporting to or involving local communities and NGOs?",
            "How does the project address the EU’s focus on circular economy principles, such as waste reduction and resource efficiency?",
        ],
        "High-Level US ESG Indicators - Environmental Indicators": [
            "Does the project adhere to a sustainable land use policy, including site selection that prioritizes ecological conservation and the use of previously disturbed sites?",
            "Is there a documented Net Zero Improvement Plan in place, including third-party assessments and measures for carbon capture and sequestration?",
            "Does the project have a comprehensive Site Waste Management Plan, including partnerships with organizations to ensure sustainable waste practices?",
            "Are there documented processes for the ethical sourcing of rare earth materials, including supplier evaluations and environmental impact assessments?",
        ],
        "High-Level US ESG Indicators - Social Indicators": [
            "Does the project include a framework for engaging with local communities and stakeholders to align with environmental and socio-economic goals?",
            "Are there guidelines ensuring fair labor practices, safe working conditions, and respect for human rights within the project and its supply chain?",
        ],
        "High-Level US ESG Indicators - Governance Indicators": [
            "Is there a system in place for ensuring compliance with all relevant environmental and social regulations, including regular monitoring and reporting?",
            "Does the project enforce a Supplier Code of Conduct that covers areas such as human rights, environmental responsibility, and anti-corruption measures?",
            "Are there clear policies and procedures for whistleblowing and handling grievances, ensuring protection against retaliation and maintaining confidentiality?",
            "Is there an anti-bribery and corruption policy that includes training, monitoring, and enforcement mechanisms to prevent improper payments and corruption?",
        ],
        "Community Engagement": [
            "Does the project have a documented history of engagement with the community around the project, or a specific plan for such engagement?",
            "Has the project held public information or education meetings with the community around the project?",
            "Has the project issued any press releases, or given media interviews about the projects?",
            "Has the project generated any related educational or informational materials related to the impact of the project?",
        ],
    }

    # Store responses in a dictionary
    responses = {}

    # Display questions by subtopic
    for subtopic, questions in survey_data.items():
        st.header(subtopic)
        for idx, question in enumerate(questions, start=1):
            response = st.radio(f"{question}", ["Yes", "No"], key=f"{subtopic}_{idx}")
            responses[question] = response

    # Submit button
    if st.button("Submit"):
        if selected_location:
            handle_submission(responses, selected_location, project_name, project_type)
        else:
            st.warning("Please select a valid location before submitting.")

# Processing and Results Display
if st.session_state.submitted:
    # Step-by-step loading UI

    st.header("Evaluating Your ESG Project Proposal....")
    progress_bar = st.progress(0)

    with st.spinner(f"Gathering Biodiversity Data for : {st.session_state.project_location}..."):
        bio_diversity_data = get_bio_diversity_data(st.session_state.lan, st.session_state.lon)
    progress_bar.progress(1 / 4)

    with st.spinner(f"Gathering Timeline Data for : {st.session_state.project_location}..."):
        print(st.session_state.state)
        print(st.session_state.project_type)
        permit_time_frame_fetcher = PermitTimeFrameFetcher(st.session_state.state, st.session_state.project_type, 1)
        time_frame_summary = permit_time_frame_fetcher.get_TimeLine()
        print("-------------time_frame_summary---------------")
        print(time_frame_summary)
        print("----------------------------------------------")
    progress_bar.progress(2 / 4)

    with st.spinner("Tips..."):
        permit_time_frame_fetcher = PermitTimeFrameFetcher(st.session_state.state, st.session_state.project_type, 2)        
        tips = permit_time_frame_fetcher.get_TimeLine()
        print("------------------tips-------------------------")
        print(tips)
        print("------------------------------------------------")
    progress_bar.progress(3 / 4)

    # with st.spinner("Soil Data..."):
    #     Soil_data = Findmain(st.session_state.lan, st.session_state.lon)
    #     print("------------------tips-------------------------")
    #     print(Soil_data)
    #     print("------------------------------------------------")
    # progress_bar.progress(4 / 5)

    with st.spinner(f"Climate Data for : {st.session_state.project_location}..."):
        climate_data = get_climate_data(st.session_state.lan, st.session_state.lon)
    progress_bar.progress(4 / 4)
    # st.session_state.responses["Climate Data"]=climate_data
    # st.session_state.responses["bio_diversity Data"]=bio_diversity_data
    # st.session_state.responses["time_frame_summary Data"]=time_frame_summary
    # st.session_state.responses["Soil_data Data"]=Soil_data
    indicators, overall_score = calculate_esg_score(st.session_state.responses)
    st.header(f"The Project's Evaluation Score for the given Location is: {overall_score}")
    display_timeline(time_frame_summary)
    display_tip(tips)
    display_dict_data("Bio Diversity Data", bio_diversity_data)
    display_dict_data("Climate Data", climate_data)
    suggest_alternative_locations()
    get_alternative_projects()

