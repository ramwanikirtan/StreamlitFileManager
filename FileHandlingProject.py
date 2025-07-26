import streamlit as st
import os
from pathlib import Path

# Your existing functions (with minor adjustments) will go here

def readfileandfolder():
    path = Path('')
    items = list(path.rglob('*'))  # Recursively list all files and folders
    return items

def createfile(name, data):
    try:
        items = readfileandfolder()
        p = Path(name)
        if not p.exists():
            with open(p, "w") as fs:
                fs.write(data)
            return "File created successfully!"
        else:
            return "File already exists"
    except Exception as err:
        return f"Error: {err}"

def readfile(name):
    try:
        items = readfileandfolder()
        p = Path(name)
        if p.exists() and p.is_file():
            with open(p, "r") as fs:
                data = fs.read()
            return data
        else:
            return "File doesn't exist"
    except Exception as err:
        return f"Error: {err}"

def updatefile(name, choice, new_name=None, new_data=None):
    try:
        items = readfileandfolder()
        p = Path(name)
        if p.exists() and p.is_file():
            if choice == 1:  # Rename
                p.rename(new_name)
            elif choice == 2:  # Overwrite
                with open(p, "w") as fs:
                    fs.write(new_data)
            elif choice == 3:  # Append
                with open(p, "a") as fs:
                    fs.write(" " + new_data)
            return "File updated successfully!"
        else:
            return "File doesn't exist"
    except Exception as err:
        return f"Error: {err}"

def deletefile(name):
    try:
        items = readfileandfolder()
        p = Path(name)
        if p.exists() and p.is_file():
            os.remove(p)
            return "File removed successfully!"
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

    st.title("🌐 File Management System")
    st.subheader("A simple and sleek interface to manage your files with ease")

    # Sidebar for navigation and file listing
    st.sidebar.header("Available Files:")
    files = readfileandfolder()
    if files:
        for file in files:
            st.sidebar.text(file)

    # Sidebar operation options
    option = st.sidebar.selectbox("Choose an operation", ("Create File", "Read File", "Update File", "Delete File"))

    if option == "Create File":
        st.header("Create a New File")
        filename = st.text_input("Enter file name", placeholder="E.g., file.txt")
        filecontent = st.text_area("Enter content for the file", placeholder="Type your content here...")

        if st.button("Create File"):
            message = createfile(filename, filecontent)
            st.success(message)

    elif option == "Read File":
        st.header("Read a File")
        filename = st.text_input("Enter file name to read", placeholder="E.g., file.txt")

        if st.button("Read File"):
            content = readfile(filename)
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
                message = updatefile(filename, 1, new_filename)
            elif operation_choice == "Overwrite":
                message = updatefile(filename, 2, new_data=new_content)
            elif operation_choice == "Append":
                message = updatefile(filename, 3, new_data=new_content)
            st.success(message)

    elif option == "Delete File":
        st.header("Delete a File")
        filename = st.text_input("Enter file name to delete", placeholder="E.g., file.txt")

        if st.button("Delete File"):
            message = deletefile(filename)
            st.success(message)

if __name__ == "__main__":
    app()
