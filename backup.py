import requests
import streamlit as st
from WindSpeed import get_climate_data
from GoogleScrapper import PermitTimeFrameFetcher
from get_bio_diversity_data import get_bio_diversity_data
from LatestSoilData import Findmain
from neo4j import GraphDatabase


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


# Neo4j connection setup
uri = "bolt://localhost:7687"
username = "neo4j"
password = "user1234"  # Replace with your actual password
driver = GraphDatabase.driver(uri, auth=(username, password))

st.title("Energy Project Developer ESG Survey")

# Functions for Neo4j interactions
def update_answers_in_neo4j_test(responses):
    """Update answers in the Neo4j Test dataset."""
    with driver.session() as session:
        for question, answer in responses.items():
            session.run(
                """
                MATCH (q:Question:Test {text: $question})
                SET q.answer = $answer
                """,
                question=question,
                answer=answer,
            )

def fetch_scores_from_neo4j_test():
    """Fetch indicator and overall ESG scores from Neo4j Test dataset."""
    with driver.session() as session:
        # Fetch indicator scores
        indicator_scores = session.run(
            """
            MATCH (q:Question:Test)-[:RELATES_TO]->(i:Indicator:Test)
            WITH i, SUM(CASE WHEN q.answer = "Yes" THEN q.weight ELSE 0 END) AS IndicatorScore
            RETURN i.name AS Indicator, IndicatorScore
            """
        )
        indicators = [{"Indicator": record["Indicator"], "Score": record["IndicatorScore"]} for record in indicator_scores]

        # Fetch overall ESG score
        overall_score = session.run(
            """
            MATCH (q:Question:Test)-[:RELATES_TO]->(i:Indicator:Test)
            WITH SUM(CASE WHEN q.answer = "Yes" THEN q.weight ELSE 0 END) AS TotalScore
            RETURN TotalScore * 100 AS OverallESGScore
            """
        ).single()["OverallESGScore"]

        return indicators, overall_score

# Display components
def display_dict_data(title, data):
    with st.expander(title):
        for key, value in data.items():
            col1, col2 = st.columns([1, 3])
            col1.markdown(f"**{key}**")
            col2.markdown(f"{value}")

def display_timeline(content, bg_color="#e6e6fa", heading_color="#6a0dad", text_color="#333"):
    """Display a timeline box that dynamically adjusts to fit all the content."""
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
    """Display a tip box that dynamically adjusts to fit all the content."""
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

def handle_submission_test(responses):
    """Handle form submission for the Test dataset and update session state."""
    st.session_state.submitted = True
    st.session_state.responses = responses
    # Update answers in Neo4j Test dataset
    update_answers_in_neo4j_test(responses)

# Initialize session state
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Survey questions
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
}

# Display form only if not submitted
if not st.session_state.submitted:
    st.header("Survey Questions (Test Dataset)")
    responses = {}

    # Display questions by category
    for category, questions in survey_data.items():
        st.subheader(category)
        for idx, question in enumerate(questions, start=1):
            response = st.radio(f"{question}", ["Yes", "No"], key=f"{category}_{idx}")
            responses[question] = response

    # Submit button
    if st.button("Submit"):
        handle_submission_test(responses)

# Display results if submitted
if st.session_state.submitted:
    st.header("Survey Results")

    # Fetch scores from Neo4j Test dataset
    indicators, overall_score = fetch_scores_from_neo4j_test()

    # Fetch additional data
    with st.spinner("Gathering Biodiversity Data..."):
        bio_diversity_data = get_bio_diversity_data(12.9716, 77.5946)  # Example coordinates
    with st.spinner("Gathering Timeline Data..."):
        permit_time_frame_fetcher = PermitTimeFrameFetcher(loc="Karnataka", re_type="Solar Power Plant", query_option=1)
        time_frame_summary = permit_time_frame_fetcher.get_TimeLine()
    with st.spinner("Fetching Tips..."):
        tips = permit_time_frame_fetcher.get_TimeLine()

    # Display results
    st.subheader("Indicator Scores")
    for ind in indicators:
        st.write(f"**{ind['Indicator']}**: {ind['Score']}")

    st.subheader("Overall ESG Score")
    st.write(f"**Total Score**: {overall_score:.2f}")

    display_timeline(time_frame_summary)
    display_tip(tips)
    display_dict_data("Bio Diversity Data", bio_diversity_data)


    suggest_alternative_locations()
    get_alternative_projects()

# Close Neo4j driver
