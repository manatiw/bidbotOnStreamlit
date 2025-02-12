import streamlit as sl

# Assign values to the session state for tender and award lists (if not already set)
if 'tender' not in sl.session_state:
    sl.session_state['tender'] = 'tender_list'
if 'award' not in sl.session_state:
    sl.session_state['award'] = 'award_list'

# Title
sl.markdown("<h2 style='text-align: center;'>Moldev相關標案下載</h2>", unsafe_allow_html=True)

# Function to toggle preview visibility
def toggle_preview():
    # Toggle the state of the preview flag in session state
    sl.session_state['preview_open'] = not sl.session_state.get('preview_open', False)

# Preview button
sl.button("Toggle Preview", on_click=toggle_preview)

# Show preview if preview_open is True
if 'preview_open' in sl.session_state and sl.session_state['preview_open']:
    if 'tender' in sl.session_state and 'award' in sl.session_state:
        sl.write(sl.session_state['tender'])
        sl.write(sl.session_state['award'])
    else:
        sl.warning("No data to preview.")