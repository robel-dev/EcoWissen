import streamlit as st
from model import model_response, dummy_model_response
import streamlit as st
import os
import json
import requests
import time
# from localize import translations
# from utils import chatbot_sidebar, chatbot_display, chat_log_display
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from translations import translations






language = st.radio('Choose a language / Wählen Sie eine Sprache', list(translations.keys()))
# Initialize the sidebar for saving/loading conversations

st.sidebar.title(translations[language]["sidebar_title"])
# Add a sidebar button for navigation
# Export conversation
pdf_name = st.sidebar.text_input(translations[language]["name_this_pdf"], key="pdf_name")
if st.sidebar.button(translations[language]["export_pdf"]):
    if pdf_name:
        pdf_path = f"{pdf_name}.pdf"
        c = canvas.Canvas(pdf_path, pagesize=letter)
        textobject = c.beginText()
        textobject.setTextOrigin(10, 700)
        textobject.setFont("Helvetica", 14)

        # for message in st.session_state.get('chat_log', []):
        #     textobject.textLine(message)
        def split_string(s, max_length):
            return [s[i:i+max_length] for i in range(0, len(s), max_length)]
        y = 700
        for message in st.session_state.get('chat_log', []):
            lines = split_string(message, 60)  # split the message into lines of max 60 characters
            for line in lines:
                if y < 40:  # if we're close to the bottom, start a new page
                    c.drawText(textobject)
                    c.showPage()
                    textobject = c.beginText()
                    textobject.setTextOrigin(10, 700)
                    y = 700
                textobject.textLine(line)
                y -= 20  # decrease y by 20 units for each line


        c.drawText(textobject)
        c.save()

        with open(pdf_path, "rb") as f:
            pdf_data = f.read()

        st.sidebar.download_button(
            label=translations[language]["pdf_exported"],
            data=pdf_data,
            file_name=f"{pdf_name}.pdf",
            mime="application/pdf",
        )

        os.remove(pdf_path)  


# Initialize carbon_footprint to 0
if 'carbon_footprint' not in st.session_state:
    st.session_state['carbon_footprint'] = 0


# Title of the chat application
st.title(translations[language]["chatbot_title"])
# Encapsulating inputs in a form for automatic reset
with st.form(key='chat_form'):
    user_input = st.text_input(translations[language]["type_your_message"], value=st.session_state.get('user_input', ''))
    submit_button = st.form_submit_button(translations[language]["send"])


# Processing after form submission
if submit_button and user_input:
    # Adding user input to chat log
    st.session_state['chat_log'] = st.session_state.get('chat_log', []) + [f"User: {user_input}"]
    try:

        #measure the time it takes to get a response
        start_time = time.time()
        # Fetching response from bot
    
        llm_response = model_response(user_input)
        end_time = time.time()

        # Calculate the elapsed time in seconds
        prompting_time = end_time - start_time
        
        # Calculate the carbon footprint
        total_power_consumption = float(json.loads(llm_response)['gpu_data'][3]['total_power_draw'])
        
        emission_factor = 0.233 # kg CO2 per kWh
        
        st.session_state['carbon_footprint'] = total_power_consumption * prompting_time * emission_factor / 3.6
        bot_response = json.loads(llm_response)['response']
    except Exception as e:
        # If an error occurs, display the error message
        bot_response = "Entschuldigung, ich habe derzeit technische Schwierigkeiten. Bitte versuchen Sie es später noch einmal. Sorry, I'm currently experiencing technical difficulties. Please try again later."

    st.session_state['chat_log'] += [f"Bot: {bot_response}"]  

    # Reset the form input
    st.session_state['user_input'] = ''


   
if 'chat_log' in st.session_state:
    for message in st.session_state['chat_log']:
        if "Bot:" in message:
            st.markdown(f'<p style="border-radius: 20px; padding: 10px; color: white; background-color: #1f2629;">🤖: {message[5:]}</p>', unsafe_allow_html=True)
        else:
            st.markdown(f'<p style="border-radius: 20px; padding: 10px; color: white; background-color: #008080;">👤: {message[6:]}</p>', unsafe_allow_html=True)

    st.text(f"The total carbon footprint for this prompt is {st.session_state['carbon_footprint']} mg.")
