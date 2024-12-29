import json

def json_to_md(base_path):

    json_file = f"{base_path}.json"  # Path to your JSON file
    md_file = f"{base_path}.md"    # Path to your Markdown file

    print(json_file)
    print(md_file)

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

                # # Write the prompt and response details
                # md.write("### Prompt\n\n")
                # md.write(f"{case.get('Prompt', 'N/A')}\n\n")

                md.write("### Response\n\n")
                md.write(f"{case.get('Response', 'N/A')}\n\n")

                # Add a separator between use cases
                md.write("---\n\n")

        print(f"Markdown file saved to {md_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# base_path = '../artifact/ai_use_case_analysis.openai'   # Base path for the openai generated JSON and Markdown files
# base_path = '../artifact/global_ai_use_case_analysis.openai'   # Base path for the openai generated JSON and Markdown files
# base_path = '../artifact/ai_use_case_analysis.local'   # Base path for the local generated JSON and Markdown files
base_path = '../artifact/global_ai_use_case_analysis.local'   # Base path for the local generated JSON and Markdown files

# Convert the JSON file to Markdown
json_to_md(base_path)

