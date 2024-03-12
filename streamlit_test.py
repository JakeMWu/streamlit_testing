import streamlit as st
import math

# Initialize or increment the count
def increment_counter():
    if 'count' not in st.session_state:
        st.session_state.count = 1
    else:
        st.session_state.count += 1 * math.sqrt(st.session_state.count)

# UI
st.title('Simple Streamlit App')

# Display the count, initializing it if necessary
if 'count' not in st.session_state:
    st.session_state.count = 0
st.write(f'Button has been clicked {st.session_state.count} times.')

# Button to increment the counter
st.button('Click me!', on_click=increment_counter)