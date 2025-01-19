import streamlit as st

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



suggest_alternative_locations()
get_alternative_projects()