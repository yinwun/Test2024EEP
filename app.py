from flask import Flask, render_template, request, jsonify
import logging
from werkzeug.serving import run_simple
from threading import Thread
from github import Github
import requests  # To make API calls
import json  # For handling JSON data

app = Flask(_name_)

# Set up logging
logging.basicConfig(filename='app_logs.log', level=logging.INFO)

# Add a console handler to the logger
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(console_handler)

# Set up GitHub authentication (Replace with a secure token)
g = Github('')

# Set your Google AI API key (Replace with a secure key)
GOOGLE_AI_API_KEY = ''
GOOGLE_AI_ENDPOINT = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GOOGLE_AI_API_KEY}'


@app.route('/')
def home():
    return render_template('index.html')

def extract_repo_name(url):
    # Split the URL by '/'
    parts = url.split('/')
    # The repository name is at index 3 and 4
    return f"{parts[3]}/{parts[4]}"




# Function to get all files from the GitHub repository
def get_files_from_repo(repo_name):
    repo = g.get_repo(repo_name)  # repo_name format 'owner/repo_name'
    contents = repo.get_contents("")
    files = []
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            files.append(file_content)
    return files

# Function to generate an explanation of the code using Google AI
def explain_code(file_content):
    prompt =  (
        "Generate code comments which give clear technical and functional details for each of the classes and methods present in the provided code. "
        "The comments should be formatted as Python comments or docstrings and should be added directly above the corresponding classes and methods. "
        "Please ensure to keep all the original code unchanged while generating the response, and avoid generating comments for variable initializations. "
        "Also, generate an overall README content for the repository at the end, including an index at the start to help navigate through the README file.\n\n"
        f"{file_content}"
    )
    headers = {
        'Content-Type': 'application/json',
    }

    # Prepare the payload for the request
    data = {
    "contents": [
        {
            "parts": [
                {"text": prompt}
            ]
        }
    ]
}

    # Make the API request
    response = requests.post(GOOGLE_AI_ENDPOINT, headers=headers, json=data)  # Use json= to automatically handle JSON encoding
    # print(json.dumps(response.json(), indent=2))
    # Check for response status
    if response.status_code == 200:
        # Access the explanation based on the provided response structure
        explanations = response.json()['candidates'][0]['content']['parts'][0]['text']
        return explanations
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return "Failed to get explanation."

# Function to generate explanations for each file in the repo
def generate_explanations_for_repo(repo_name):
    files = get_files_from_repo(repo_name)
    explanations = {}

    # Iterate over each file and generate explanations
    for file in files:
        if file.path.endswith('.py'):  # Adjust this to the file types you want to explain
            file_content = file.decoded_content.decode('utf-8')
            explanations[file.path] = explain_code(file_content)

    return explanations

def save_explanations_and_push(repo_name, head_branch, explanations, new_branch_name):
    repo = g.get_repo(repo_name)
    commit_message = "Add code explanations"

    # Create a new branch from the main branch
    main_branch = repo.get_branch(head_branch)
    repo.create_git_ref(ref=f"refs/heads/{new_branch_name}", sha=main_branch.commit.sha)

    # Prepare to store complete README content
    complete_readme_content = ""

    for file_path, explanation in explanations.items():
        # Extract README and explanation content
        readme_content, explanation_content = extract_readme_content(explanation)

        # Append readme content to the overall README
        complete_readme_content += f"{readme_content}\n\n"

        try:
            # Check if the file already exists in the repo
            contents = repo.get_contents(file_path, ref=head_branch)  # Specify the main branch

            # Prepare the new content by adding the explanation as comments
            updated_content = explanation_content + '\n\n'  # Only the explanation, no original code

            # Update the existing file with the new content in the new branch
            repo.update_file(file_path, commit_message, updated_content, contents.sha, branch=new_branch_name)
            print(f"Updated {file_path} in the new branch '{new_branch_name}'.")
        except Exception as e:
            print(f"Failed to update {file_path}: {e}")

    # Save README content to README.md file
    try:
        # Create or update the README.md file
        repo.create_file("README.md", commit_message, complete_readme_content, branch=new_branch_name)
        print("Created or updated README.md in the new branch.")
    except Exception as e:
        print(f"Failed to create/update README.md: {e}")

def extract_readme_content(explanation):
    # Split the explanation into lines
    lines = explanation.splitlines()
    readme_content = []
    explanation_content = []

    # Flag to check if we are in the README section
    in_readme_section = False

    for line in lines:
        # Check if the line contains a code block indicator
        if "```" in line:
            continue  # Skip this line entirely

        # Check for the start of the README section (case insensitive)
        if "## readme" in line.lower():
            in_readme_section = True
            continue  # Skip the line that starts with ## readme

        if in_readme_section:
            readme_content.append(line)  # Add lines to README content
        else:
            explanation_content.append(line)  # Add lines to code content

    return "\n".join(readme_content).strip(), "\n".join(explanation_content).strip()

def create_pull_request(repo_name, base_branch, head_branch, title="Add code explanations and README", body="This PR adds detailed explanations to the code and updates the README file."):
    repo = g.get_repo(repo_name)

    try:
        # Create a pull request
        pr = repo.create_pull(title=title, body=body, base=base_branch, head=head_branch)
        print(f"Pull request created: {pr.html_url}")
    except Exception as e:
        print(f"Failed to create pull request: {e}")

def run_app():
    run_simple('localhost', 8085, app)

@app.route('/generate_explanations', methods=['POST'])
def generate_explanations():
    try:
        # Get repository name from request
        repo_name = extract_repo_name(request.json['repo_name']);
        print(repo_name)
        explanations = generate_explanations_for_repo(repo_name)
        return jsonify(explanations)
    except Exception as e:
        logging.error(f"Error generating explanations: {str(e)}")
        return jsonify({"error": "Failed to generate explanations"}), 500

# Start the Flask application in a separate thread
thread = Thread(target=run_app)
thread.start()
