# Specify number of use cases to process or use "All" for the entire file
num_to_process = "50" #input("Enter the number of use cases to process (or 'All' for all use cases): ").strip()

# Set the input file path
input_file = "artifact/ai_uc_inventory-dhs.xlsx"

# Set the output file paths
output_file_json = "artifact/ai_use_case_analysis.json"
output_file_jsonl = "artifact/ai_use_case_analysis.jsonl"

# # OpenAI API 
# api_url = "https://api.openai.com/v1"
# # load api key from .env_val file...syntax [OPENAI_API_KEY="your_api_key"]
# from dotenv import load_dotenv
# import os
# load_dotenv('.env_vals')
# str_api_key = os.getenv('OPENAI_API_KEY')
# model_name="gpt-4"

# Ollama API
api_url = "http://192.168.244.61:5500/v1"
str_api_key="ollama"
model_name="wizard-vicuna-uncensored:30b"

#################################################################################################

import pandas as pd
import openai
from openai import Client
import json

# Initialize the OpenAI API client
client = Client(api_key=str_api_key,base_url=api_url)

# Load the input XLSX dataset
dhs_data = pd.read_excel(input_file)

# Determine the data to process
if num_to_process.lower() == "all":
    data_to_process = dhs_data
else:
    try:
        num_to_process = int(num_to_process)
        data_to_process = dhs_data.head(num_to_process)
    except ValueError:
        print("Invalid input. Please enter a number or 'All'.")
        exit()

# List to hold the results
results = []

# Iterate through the selected use cases
for index, row in data_to_process.iterrows():
    usecase_id = row.get("Use Case ID", "Not provided")
    agency = row.get("Agency", "Not provided")
    bureau_dept = row.get("Bureau / Department", "Not provided")
    use_case_name = row.get("Use Case Name", f"Use Case {index + 1}")
    purpose_statement = row.get("Summary of Use Case", "Not provided")
    benefit_statement = row.get("What is the intended purpose and expected benefits of the AI?", "Not provided")
    system_outputs = row.get("System Outputs", "Not provided")

    # Construct the prompt
    prompt = f"""

Analyze the following AI use case comprehensively:

**Details:**
- Use Case ID: {usecase_id}
- Agency: {agency}
- Bureau / Department: {bureau_dept}
- Purpose Statement: {purpose_statement}
- Benefit Statement: {benefit_statement}
- System Outputs: {system_outputs}

Address the following key areas in your response:

1. **Categorization of Value Creation**: Categorize the use case as one of the following types—Efficiency Amplifier, Capability Enhancer, or Breakthrough Enabler. Provide a detailed justification for your categorization based on the purpose statement, system outputs, and implementation context.

2. **Operational Impact**: Identify the potential operational impact of the use case, including improvements in process efficiencies, capability expansions, or the introduction of new operational paradigms. Highlight specific benefits and implications.

3. **Transformation Potential**: Evaluate the transformation potential of the use case by assessing how it aligns with or departs from traditional workflows, operational limitations, or technological boundaries. Explain the significance of this transformation.

4. **Risks and Mitigation Strategies**: Identify potential risks associated with the use case (e.g., ethical concerns, biases, or operational dependencies). Suggest effective mitigation strategies to address these risks.

5. **Indicators of Value Creation**: Highlight key indicators of value creation, such as operational metrics, organizational benefits, or societal impacts. Distinguish between explicit and implicit value drivers.

6. **Comparison to Similar Use Cases**: Compare the use case to previously documented ones. Identify similarities and differences in objectives, outputs, and implementation contexts. Derive lessons or patterns that can be applied to enhance the effectiveness of the use case.

7. **Recommendations for Improvement**: Provide actionable recommendations to improve the clarity, alignment, and strategic articulation of the use case. Ensure that these recommendations address any identified gaps or opportunities for enhancement.

Please provide a structured and detailed response addressing all points above.
"""

    try:
        # Submit the prompt to OpenAI API using the ChatCompletion interface
        response = client.chat.completions.create(
            model=model_name,  #"gpt-4",  # Use "gpt-3.5-turbo" if preferred
            messages=[
                {"role": "system", "content": "You are an AI assistant analyzing AI use case documentation."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=5000
        )

        # Extract the response text
        response_text = response.choices[0].message.content.strip()

        # Append the result to the list
        results.append({
            "Use Case ID": usecase_id,
            "Agency": agency,
            "Bureau / Department": bureau_dept,
            "Use Case Name": use_case_name,
            "Prompt": prompt,
            "Response": response_text
        })

        # Write the result to a JSON Lines file
        with open(output_file_jsonl, mode="a", encoding="utf-8") as file:
            json.dump({
                "Use Case ID": usecase_id,
                "Agency": agency,
                "Bureau / Department": bureau_dept,
                "Use Case Name": use_case_name,
                "Prompt": prompt,
                "Response": response_text
            }, file)
            file.write("\n")

    except Exception as e:
        print(f"Error processing prompt for use case '{use_case_name}': {e}")
        print(f"Detailed error: {str(e)}")
        print(f"API Base URL: {client.base_url}")

# Write the results to a JSON file
with open(output_file_json, mode="a", encoding="utf-8") as file:
    json.dump(results, file, indent=4)

print(f"Analysis completed. Results saved to {output_file_json} and {output_file_jsonl}")

