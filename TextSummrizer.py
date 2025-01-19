import requests
import logging
def summarize_text(text,prompt_type):
    try:
        url = "http://127.0.0.1:1234/v1/completions"  # Update with LLaMA 3.2 endpoint
        headers = {"Content-Type": "application/json"}
        prompt2 = (
            "Summarize the following text on the process to obtain approvals for a renewable energy farm in "
            "the specified state, focusing on key tips, relevant rules and regulations, and best practices to "
            "ensure the project's approval. Be concise but make sure to retain accuracy on any critical details, give it in few lines:\n\n"
            f"{text}"
        )
        prompt1 = (
            "Analyze the following text to identify all key project phases for a renewable energy construction project "
            "(e.g., Pre-Planning, Planning & Permitting, Procurement, Construction, Post-Construction). For each phase, ensure the following details are included completely:\n"
            "1. Summarize the main activities involved for each phase.\n"
            "2. Include any explicitly mentioned or implied timeframes, such as specific durations, deadlines, or operational windows "
            "(e.g., '60-day window,' 'one-year limit,' or average time durations for each phase).\n"
            "3. Organize the information into a clear and complete timeline, showing the sequence of phases and their approximate durations.\n"
            "4. Ensure that all phases and their details are presented in full and exclude unrelated or extraneous details., give it in few lines\n\n"
            "TEXT:\n"
            f"{text}"
        )
        # prompt1 = (
        #     "From the following text, extract and summarize all key project phases and their associated activities "
        #     "(e.g., Pre-Planning, Planning & Permitting, Procurement, Construction, Post-Construction). "
        #     "For each phase, ensure the following:\n"
        #     "1. Summarize the main activities involved.\n"
        #     "2. Note any explicitly mentioned or implied timeframes (e.g., '60-day window,' 'one-year limit,' or average time durations for each phase).\n"
        #     "3. Organize the timeframes into a clear timeline, showing the sequence of phases and their approximate durations.\n"
        #     "4. Exclude any unrelated details not relevant to the project’s timeline or key activities., must include the time frames\n\n"
        #     "TEXT:\n"
        #     f"{text}"
        # )

        print("final prompt: ",prompt1 if prompt_type==1 else prompt2 )
        payload = {
            "model": "meta-llama-3.1-8b-instruct",
            "prompt": prompt1 if prompt_type==1 else prompt2,
            "max_tokens": 100,  # Adjust for desired length
            "temperature": 0.7  # Controls creativity
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            summary = response.json()["choices"][0]["text"].strip()
            logging.info("Successfully summarized text.")
            return summary
        else:
            logging.error(
                "Text summarization failed: %s, %s",
                response.status_code,
                response.text
            )
            return None
    except Exception as e:
        logging.error("Error in text summarization: %s", e)
        return None


