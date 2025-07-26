import streamlit as st
import os
from pathlib import Path

# Simulate a simple user database
USER_DB = {}

# File Operations
def create_user(username, password):
    if username not in USER_DB:
        USER_DB[username] = {"password": password, "files": []}
        os.makedirs(f"./users/{username}", exist_ok=True)  # Create a directory for the user
        return "User created successfully!"
    else:
        return "User already exists."

def verify_user(username, password):
    if username in USER_DB and USER_DB[username]["password"] == password:
        return True
    return False

def readfileandfolder(username):
    path = Path(f'./users/{username}')
    items = list(path.rglob('*'))
    return items

def createfile(username, name, data):
    try:
        p = Path(f'./users/{username}/{name}')
        if not p.exists():
            with open(p, "w") as fs:
                fs.write(data)
            USER_DB[username]["files"].append(name)
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

def updatefile(username, name, choice, new_name=None, new_data=None):
    try:
        p = Path(f'./users/{username}/{name}')
        if p.exists() and p.is_file():
            if choice == 1:  # Rename
                p.rename(f'./users/{username}/{new_name}')
                USER_DB[username]["files"].remove(name)
                USER_DB[username]["files"].append(new_name)
            elif choice == 2:  # Overwrite
                with open(p, "w") as fs:
                    fs.write(new_data)
            elif choice == 3:  # Append
                with open(p, "a") as fs:
                    fs.write(" " + new_data)
            return f"File '{name}' updated successfully!"
        else:
            return "File doesn't exist"
    except Exception as err:
        return f"Error: {err}"

def deletefile(username, name):
    try:
        p = Path(f'./users/{username}/{name}')
        if p.exists() and p.is_file():
            os.remove(p)
            USER_DB[username]["files"].remove(name)
            return f"File '{name}' removed successfully!"
        else:
            return "File doesn't exist"
    except Exception as err:
        return f"Error: {err}"

# Streamlit UI

def app():
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
    st.title("🌐 File Management System")
    st.subheader("Secure and Personal File Management")

    choice = st.selectbox("Select Operation", ["Login", "Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Register":
        if st.button("Create Account"):
            message = create_user(username, password)
            st.success(message)

    elif choice == "Login":
        if st.button("Login"):
            if verify_user(username, password):
                st.success(f"Welcome back, {username}!")
                user_files = readfileandfolder(username)
                if user_files:
                    st.sidebar.header("Your Files:")
                    for file in USER_DB[username]["files"]:
                        st.sidebar.text(file)
                else:
                    st.sidebar.text("No files yet. Create one!")
                
                option = st.sidebar.selectbox("Choose an operation", ("Create File", "Read File", "Update File", "Delete File"))

                if option == "Create File":
                    st.header("Create a New File")
                    filename = st.text_input("Enter file name", placeholder="E.g., file.txt")
                    filecontent = st.text_area("Enter content for the file", placeholder="Type your content here...")

                    if st.button("Create File"):
                        message = createfile(username, filename, filecontent)
                        st.success(message)

                elif option == "Read File":
                    st.header("Read a File")
                    filename = st.text_input("Enter file name to read", placeholder="E.g., file.txt")

                    if st.button("Read File"):
                        content = readfile(username, filename)
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
                            message = updatefile(username, filename, 1, new_filename)
                        elif operation_choice == "Overwrite":
                            message = updatefile(username, filename, 2, new_data=new_content)
                        elif operation_choice == "Append":
                            message = updatefile(username, filename, 3, new_data=new_content)
                        st.success(message)

                elif option == "Delete File":
                    st.header("Delete a File")
                    filename = st.text_input("Enter file name to delete", placeholder="E.g., file.txt")

                    if st.button("Delete File"):
                        message = deletefile(username, filename)
                        st.success(message)

            else:
                st.error("Invalid credentials. Please try again.")

if __name__ == "__main__":
    app()
