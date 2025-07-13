from flask import Flask, render_template, abort, request, redirect, url_for, session  # Import Flask and helpers for web app, error handling, and sessions
import json  # For reading JSON files
import os    # For file path operations

# Create the Flask web app
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session

# Define a simple Project class to hold project info
class Project:
    def __init__(self, name, description, url, tech_stack):
        # Save the project details as attributes
        self.name = name
        self.description = description
        self.url = url
        self.tech_stack = tech_stack

    @classmethod
    def from_dict(cls, d):
        # Create a Project from a dictionary (like from JSON)
        return cls(
            d.get("name", ""),           # Get name or empty string
            d.get("description", ""),    # Get description or empty string
            d.get("url", ""),            # Get url or empty string
            d.get("tech_stack", [])      # Get tech_stack or empty list
        )

# Function to load profile data from a JSON file
def load_profile_data(filepath):
    # If the file doesn't exist, show a 500 error
    if not os.path.exists(filepath):
        abort(500, "Profile data file not found.")
    # Open and read the JSON file
    with open(filepath, "r") as f:
        data = json.load(f)
    # Convert each project dictionary to a Project object
    data["projects"] = [Project.from_dict(p) for p in data.get("projects", [])]
    return data

# Define the route to toggle dark mode
@app.route("/toggle-dark-mode")
def toggle_dark_mode():
    dark_mode = session.get("dark_mode", False)
    session["dark_mode"] = not dark_mode
    return redirect(url_for("home"))

# Define the main route for the website
@app.route("/")
def home():
    # Figure out the location of the data.json file
    data_path = os.path.join(os.path.dirname(__file__), "data.json")
    # Load the profile data from the file
    profile = load_profile_data(data_path)
    # Convert Project objects back to dictionaries for the template
    profile["projects"] = [vars(p) for p in profile["projects"]]
    dark_mode = session.get("dark_mode", False)
    # Render the hello.html template, passing in the profile data and dark mode flag
    return render_template("hello.html", profile=profile, dark_mode=dark_mode)

# If this file is run directly, start the Flask web server
if __name__ == "__main__":
    app.run(debug=True)