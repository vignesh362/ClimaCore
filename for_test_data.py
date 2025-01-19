import requests
import streamlit as st
from neo4j import GraphDatabase
from GoogleScrapper import PermitTimeFrameFetcher
from get_bio_diversity_data import get_bio_diversity_data

# Neo4j connection setup
uri = "bolt://localhost:7687"
username = "neo4j"
password = "user1234"  # Replace with your actual password
driver = GraphDatabase.driver(uri, auth=(username, password))

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

def handle_submission_test(responses):
    """Handle form submission for the Test dataset and update session state."""
    st.session_state.submitted = True
    st.session_state.responses = responses
    # Update answers in Neo4j Test dataset
    update_answers_in_neo4j_test(responses)

# Streamlit app setup
st.title("Energy Project Developer ESG Survey (Test Dataset)")

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
    st.header("Survey Results (Test Dataset)")

    # Fetch scores from Neo4j Test dataset
    indicators, overall_score = fetch_scores_from_neo4j_test()

    # Display indicator scores
    st.subheader("Indicator Scores")
    for ind in indicators:
        st.write(f"**{ind['Indicator']}**: {ind['Score']}")

    # Display overall ESG score
    st.subheader("Overall ESG Score")
    st.write(f"**Total Score**: {overall_score:.2f}")

# Close Neo4j driver
driver.close()
