import os
import pandas as pd
import streamlit as st

# Custom Open Graph meta tags for the preview
st.markdown("""
    <meta property="og:title" content="07/10 All Over Again 🎗️" />
    <meta property="og:description" content="A space for all of us. Data Visualization and Safe Space." />
    <meta property="og:image" content="https://raw.githubusercontent.com/Sashaglattporteny/October7/main/IMG_6685.jpg" />
    <meta property="og:url" content="https://your-app-url.com" />
    <meta name="twitter:card" content="summary_large_image">
""", unsafe_allow_html=True)

# CSV file to store data
csv_file = 'feelings_data.csv'

# Check if the CSV file exists and has valid content (not empty or corrupted)
def load_data(csv_file):
    if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
        try:
            df = pd.read_csv(csv_file)
            if df.empty or df.columns.size == 0:
                raise ValueError("CSV file is empty or corrupted")
        except (pd.errors.EmptyDataError, ValueError):
            df = pd.DataFrame(columns=["Message", "Nationality", "Age", "Name"])
    else:
        df = pd.DataFrame(columns=["Message", "Nationality", "Age", "Name"])
    return df

df = load_data(csv_file)

# Function to save data to CSV
def save_to_csv(message, nationality, age, name):
    new_entry = pd.DataFrame({"Message": [message], "Nationality": [nationality], "Age": [age], "Name": [name]})
    df_updated = pd.concat([df, new_entry], ignore_index=True)
    df_updated.to_csv(csv_file, index=False)

# Title and Explanation
st.markdown("<h1 style='text-align: center;'>It's 7 of October All Over Again 🎗️</h1>", unsafe_allow_html=True)
st.markdown("""
<p style="text-align: center; color: white;">
This is a space for all of us to remember the names and also share whatever we are feeling today. Together, we are stronger.
</p>
""", unsafe_allow_html=True)

# Flourish Chart
st.subheader("Say their names out loud")
import streamlit.components.v1 as components
components.html("""
    <div class="flourish-embed flourish-bubble-chart" data-src="visualisation/19694302">
        <script src="https://public.flourish.studio/resources/embed.js"></script>
        <noscript><img src="https://public.flourish.studio/visualisation/19694302/thumbnail" width="100%" alt="bubble-chart visualization" /></noscript>
    </div>
    """, height=600)

# Space for sharing thoughts
st.subheader("This is a space for you")

# Form to collect user input
with st.form(key='feeling_form'):
    message = st.text_input("What's on your mind or your heart?")
    
    # Adding more countries, especially from Latin America
    nationality = st.selectbox("Where are you from?", [
        "🇺🇸 United States", "🇨🇦 Canada", "🇲🇽 Mexico", "🇮🇱 Israel", "🇦🇷 Argentina", 
        "🇧🇷 Brazil", "🇨🇱 Chile", "🇨🇴 Colombia", "🇨🇷 Costa Rica", "🇩🇴 Dominican Republic",
        "🇪🇨 Ecuador", "🇸🇻 El Salvador", "🇬🇹 Guatemala", "🇭🇳 Honduras", "🇵🇦 Panama", 
        "🇵🇾 Paraguay", "🇵🇪 Peru", "🇵🇷 Puerto Rico", "🇺🇾 Uruguay", "🇻🇪 Venezuela", 
        "🇧🇴 Bolivia", "🇨🇺 Cuba", "🇳🇮 Nicaragua"
    ])
    
    age = st.number_input("How old are you?", min_value=1, max_value=120, step=1)
    name = st.text_input("Optional: Your name")
    submit_button = st.form_submit_button(label="Share")

# Append new submission to CSV if form is submitted
if submit_button and message and nationality:
    save_to_csv(message, nationality, age, name)
    st.success("Your message has been shared!")

# Function to generate compact card design
def generate_card(message, nationality, age, name):
    name_display = f"<p style='color: black;'><strong>Name:</strong> {name}</p>" if name else ""
    return f"""
    <div style="
        background-color: white;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 3px 3px 15px rgba(0,0,0,0.1);
        max-width: 400px;
        min-height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: left;
        margin: 10px;
        color: black;
        word-wrap: break-word;
    ">
        <p style="font-size: 1em; margin: 0 0 10px; color: black;">{message}</p>
        <p style="font-size: 0.9em; margin: 0; color: black;"><strong>Nationality:</strong> {nationality}, <strong>Age:</strong> {age}</p>
        {name_display}
    </div>
    """

# Displaying the entries as compact cards
st.subheader("What other people are thinking")

if not df.empty:
    for index, row in df.iterrows():
        st.markdown(generate_card(row['Message'], row['Nationality'], row['Age'], row['Name']), unsafe_allow_html=True)
else:
    st.write("No entries yet. Be the first to share your thoughts!")

# Footer
st.markdown("""
    <hr>
    <p style="text-align: center; color: white;">This app was made by Sasha Glatt</p>
""", unsafe_allow_html=True)

