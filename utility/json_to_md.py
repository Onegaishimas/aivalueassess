import json

def json_to_md(json_file, md_file):
    """
    Convert a JSON file to Markdown format and save the result to an output Markdown file.

    Parameters:
        json_file (str): Path to the input JSON file.
        md_file (str): Path to the output Markdown file.
    """
    try:
        # Read and parse the JSON file
        with open(json_file, 'r', encoding='utf-8') as f:
            use_cases = json.load(f)

        # Open the output Markdown file
        with open(md_file, 'w', encoding='utf-8') as md:
            # Iterate through each use case
            for case in use_cases:
                # Write the header and basic details to the Markdown file
                md.write(f"## Use Case ID: {case.get('Use Case ID', 'N/A')}\n\n")
                md.write(f"**Agency:** {case.get('Agency', 'N/A')}\n\n")
                md.write(f"**Bureau / Department:** {case.get('Bureau / Department', 'N/A')}\n\n")
                md.write(f"**Use Case Name:** {case.get('Use Case Name', 'N/A')}\n\n")

                # Write the prompt and response details
                md.write("### Prompt\n\n")
                md.write(f"{case.get('Prompt', 'N/A')}\n\n")

                md.write("### Response\n\n")
                md.write(f"{case.get('Response', 'N/A')}\n\n")

                # Add a separator between use cases
                md.write("---\n\n")

        print(f"Markdown file saved to {md_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
json_file = '../artifact/ai_use_case_analysis.openai.json'  # Path to your JSON file
md_file = '../artifact/ai_use_case_analysis.md'  # Path to your Markdown file

json_to_md(json_file, md_file)
