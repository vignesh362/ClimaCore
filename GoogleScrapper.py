import requests
from TextSummrizer import summarize_text

class PermitTimeFrameFetcher:
    # Class-level variables for Google API (adjust with your actual credentials)
    MY_API_KEY = "AIzaSyCqRlP1kqDSj6A3-NLhcRnrrLE_KmP8nKo"
    MY_CSE_ID = "63cb67bae11e44d04"

    def __init__(self, loc, re_type, query_option=1):

        self.loc = loc
        self.re_type = re_type
        self.query_option = query_option

    def _build_query(self):

        if self.query_option == 1:
            return f"Typical time frame to obtain permits for a large-scale {self.re_type} in {self.loc}"
        elif self.query_option == 2:
            # You can customize a second query style here
            return f"Process to obtain approvals for a {self.re_type} in {self.loc}"
        else:
            return f"Typical time frame to obtain permits for a large-scale {self.re_type} in {self.loc}"

    def _google_custom_search(self, query, num_results=5):

        print("Final Query: ",query)
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self.MY_API_KEY,
            "cx": self.MY_CSE_ID,
            "q": query,
            "num": num_results
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("items", [])

    def get_TimeLine(self):

        query = self._build_query()
        search_results = self._google_custom_search(query, num_results=5)

        if search_results:
            combined_snippets = ""
            for item in search_results:
                snippet = item.get("snippet", "")
                combined_snippets += f"{snippet}\n"

            # Summarize combined snippets
            summary = summarize_text(combined_snippets,self.query_option)
            return summary
        else:
            return "No results found."


# Example Usage
if __name__ == "__main__":
    # You can vary `query_option` to switch between queries.
    fetcher = PermitTimeFrameFetcher(loc="California", re_type="solar farm", query_option=1)
    timeframe_summary = fetcher.get_TimeLine()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(timeframe_summary)