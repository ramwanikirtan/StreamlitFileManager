import streamlit as st
import os
import json
from pathlib import Path

# Load the user database from a JSON file
def load_user_db():
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    else:
        return {}

# Save the user database to a JSON file
def save_user_db(user_db):
    with open("users.json", "w") as f:
        json.dump(user_db, f, indent=4)

# Create user in the database
def create_user(user_db, username, password):
    if username not in user_db:
        user_db[username] = {"password": password, "files": []}
        os.makedirs(f"./users/{username}", exist_ok=True)  # Create a directory for the user
        save_user_db(user_db)  # Save changes to the file
        return "User created successfully!"
    else:
        return "User already exists."

# Verify user credentials
def verify_user(user_db, username, password):
    if username in user_db and user_db[username]["password"] == password:
        return True
    return False

# File operations (create, read, update, delete)
def readfileandfolder(username):
    path = Path(f'./users/{username}')
    items = list(path.rglob('*'))
    return items

def createfile(username, name, data, user_db):
    try:
        p = Path(f'./users/{username}/{name}')
        if not p.exists():
            with open(p, "w") as fs:
                fs.write(data)
            user_db[username]["files"].append(name)
            save_user_db(user_db)  # Save user data with new file
            return f"File '{name}' created successfully!"
        else:
            return "File already exists"
    except Exception as err:
        return f"Error: {err}"

def readfile(username, name):
    try:
        p = Path(f'./users/{username}/{name}')
        if p.exists() and p.is_file():
            with open(p, "r") as fs:
                data = fs.read()
            return data
        else:
            return "File doesn't exist"
    except Exception as err:
        return f"Error: {err}"

def updatefile(username, name, choice, user_db, new_name=None, new_data=None):
    try:
        p = Path(f'./users/{username}/{name}')
        if p.exists() and p.is_file():
            if choice == 1:  # Rename
                p.rename(f'./users/{username}/{new_name}')
                user_db[username]["files"].remove(name)
                user_db[username]["files"].append(new_name)
            elif choice == 2:  # Overwrite
                with open(p, "w") as fs:
                    fs.write(new_data)
            elif choice == 3:  # Append
                with open(p, "a") as fs:
                    fs.write(" " + new_data)
            save_user_db(user_db)  # Save user data with updated file list
            return f"File '{name}' updated successfully!"
        else:
            return "File doesn't exist"
    except Exception as err:
        return f"Error: {err}"

def deletefile(username, name, user_db):
    try:
        p = Path(f'./users/{username}/{name}')
        if p.exists() and p.is_file():
            os.remove(p)
            user_db[username]["files"].remove(name)
            save_user_db(user_db)  # Save user data with updated file list
            return f"File '{name}' removed successfully!"
        else:
            return "File doesn't exist"
    except Exception as err:
        return f"Error: {err}"

# Streamlit UI

def app():
    # Load or create the user database
    user_db = load_user_db()

    # Set up session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""

    # Custom CSS for the app
    st.markdown("""
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f0f4f8;
            }
            .stButton>button {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                border: none;
            }
            .stTextInput, .stTextArea {
                border-radius: 5px;
                padding: 10px;
            }
            .stTextArea {
                background-color: #ffffff;
                border: 1px solid #ddd;
            }
            .stSelectbox, .stRadio {
                border-radius: 5px;
                padding: 10px;
            }
            .stExpander {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                padding: 10px;
                margin: 10px 0;
            }
        </style>
        """, unsafe_allow_html=True)

    # User authentication (login or register)
    if st.session_state.logged_in:
        # Show file management system
        st.title("🌐 File Management System")
        st.subheader(f"Welcome {st.session_state.username}!")
        
        user_files = readfileandfolder(st.session_state.username)
        if user_files:
            st.sidebar.header("Your Files:")
            for file in user_db[st.session_state.username]["files"]:
                st.sidebar.text(file)
        else:
            st.sidebar.text("No files yet. Create one!")
        
        option = st.sidebar.selectbox("Choose an operation", ("Create File", "Read File", "Update File", "Delete File"))

        if option == "Create File":
            st.header("Create a New File")
            filename = st.text_input("Enter file name", placeholder="E.g., file.txt")
            filecontent = st.text_area("Enter content for the file", placeholder="Type your content here...")

            if st.button("Create File"):
                message = createfile(st.session_state.username, filename, filecontent, user_db)
                st.success(message)

        elif option == "Read File":
            st.header("Read a File")
            filename = st.text_input("Enter file name to read", placeholder="E.g., file.txt")

            if st.button("Read File"):
                content = readfile(st.session_state.username, filename)
                if content != "File doesn't exist":
                    st.text_area("File Content", content, height=300)
                else:
                    st.error(content)

        elif option == "Update File":
            st.header("Update an Existing File")
            filename = st.text_input("Enter file name to update", placeholder="E.g., file.txt")
            operation_choice = st.radio("Choose operation", ("Rename", "Overwrite", "Append"))

            if operation_choice == "Rename":
                new_filename = st.text_input("Enter new file name", placeholder="E.g., newfile.txt")
            elif operation_choice in ["Overwrite", "Append"]:
                new_content = st.text_area("Enter new content", placeholder="Type new content here...")

            if st.button("Update File"):
                if operation_choice == "Rename":
                    message = updatefile(st.session_state.username, filename, 1, user_db, new_filename)
                elif operation_choice == "Overwrite":
                    message = updatefile(st.session_state.username, filename, 2, new_data=new_content, user_db=user_db)
                elif operation_choice == "Append":
                    message = updatefile(st.session_state.username, filename, 3, new_data=new_content, user_db=user_db)
                st.success(message)

        elif option == "Delete File":
            st.header("Delete a File")
            filename = st.text_input("Enter file name to delete", placeholder="E.g., file.txt")

            if st.button("Delete File"):
                message = deletefile(st.session_state.username, filename, user_db)
                st.success(message)

    else:
        # Display login/register form if not logged in
        choice = st.selectbox("Select Operation", ["Login", "Register"])

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if choice == "Register":
            if st.button("Create Account"):
                message = create_user(user_db, username, password)
                st.success(message)

        elif choice == "Login":
            if st.button("Login"):
                if verify_user(user_db, username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.experimental_rerun()  # Rerun the app after login to show the file management system
                else:
                    st.error("Invalid credentials. Please try again.")

if __name__ == "__main__":
    app()
