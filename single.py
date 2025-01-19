import requests
from neo4j import GraphDatabase

# Neo4j connection setup
uri = "bolt://localhost:7687"
username = "neo4j"
password = "user1234"  # Replace with your actual password
driver = GraphDatabase.driver(uri, auth=(username, password))

def calculate_esg_score(responses):
    """
    Takes user responses as input, updates the Neo4j database, and returns ESG scores.

    Args:
        responses (dict): A dictionary of questions and their corresponding "Yes" or "No" answers.

    Returns:
        tuple: A tuple containing:
            - A list of dictionaries with indicator scores.
            - The overall ESG score as a float.
    """
    # Update answers in Neo4j
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

    # Fetch scores from Neo4j
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

# Example Usage
# if __name__ == "__main__":
#     # Example responses dictionary
#     example_responses = {
#         "Does the project have a materials recycling program?": "Yes",
#         "Does the project follow wage standards that meet or exceed the Davis-Bacon Act guidelines?": "No",
#         "Does the project have an apprenticeship program?": "Yes",
#         "Are vendors educated about ESG guidelines or given any specific ESG-related requirements?": "No",
#         "Is there any monitoring of or reporting from vendors required in relation to ESG requirements?": "Yes",
#     }

#     # Calculate scores
#     indicators, overall_score = calculate_esg_score(example_responses)

#     # Print results
#     print("Indicator Scores:")
#     for ind in indicators:
#         print(f"{ind['Indicator']}: {ind['Score']}")

#     print(f"\nOverall ESG Score: {overall_score:.2f}")

# Close Neo4j driver
