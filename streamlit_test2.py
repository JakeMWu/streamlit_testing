import streamlit as st
import math

# UI
st.title('Paint it Black')

# Input for the user's name
name = st.text_input('What is your name?', '')

# Dropdown for selecting favorite color
color = st.selectbox(
    'What is your favorite color?',
    ('Blue', 'Green', 'Red', 'Yellow', 'Orange', 'Purple', 'Pink')
)

# When both inputs are provided, change the background color and print the message
# A submit button
submitted = st.button('Submit')

# When the button is clicked and both inputs are provided
if submitted and name and color:
    # Changing the background color to black
    st.markdown(
        """
        <style>
        .stApp {
            background-color: black;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Display the message
    st.write(f"Hi {name}, I hope your favourite colour was black!")