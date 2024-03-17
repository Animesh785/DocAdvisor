import streamlit as st
import google.generativeai as genai
import os 
import plotly.graph_objects as go
from dotenv import load_dotenv
load_dotenv()   # load env varibles 
from PIL import Image 
import json


import requests


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_promt , image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_promt,image[0]])
    return response.text

def input_image_setup(upload_file):
    if upload_file is not None:
        byte_data = upload_file.getvalue()

        image_parts  = [
            {
                "mime_type" : upload_file.type,
                "data": byte_data
            }
        ]

        return image_parts  
    else :
        raise FileNotFoundError("NO File uploaded ")
    

# Set page configuration
st.set_page_config(page_title="DocAdvisor")
st.header("DocAdvisor")



# Navigation menu
page = st.sidebar.radio("Nav-Bar", ["Home", "Meal Planning", "About Us", "Contact Us",])

def parse_gemini_response(response):
    # Parse the JSON response to extract x and y values for plotting
    data = json.loads(response)
    x_values = data["data"][0]["x"]
    y_values = data["data"][0]["y"]
    return x_values, y_values


# Define the content for each page
if page == "Meal Planning":
        # Title
    st.title("Meal Planning")

    # Form for meal planning options
    with st.form("meal_planning_form"):
        # Define options for spices
        spices_options = ["No spices", "Mild", "Medium", "Spicy"]
        spices = st.selectbox("Spices", spices_options)

        # Define options for taste
        taste_options = ["Sweet", "Salty", "Sour", "Bitter", "Umami"]
        taste = st.multiselect("Taste", taste_options)

        # Define options for dietary preferences
        dietary_preferences = st.checkbox("Vegetarian")
        
        cuisine_options = ["North Indian", "South Indian", "Continental", "Chinese"]
        cuisine = st.selectbox("Choose your cuisine:", cuisine_options)
        # Define options for allergies
        allergies = st.text_input("Enter any allergies")

        # Submit button
        submitted = st.form_submit_button("Plan Meal")

    # Generate prompt string based on user selections
    prompt = f"Meal planning options:\nSpices: {spices}\nTaste: {', '.join(taste)}\nVegetarian: {'Yes' if dietary_preferences else 'No'}\nAllergies: {allergies}\nCuisines:{cuisine}"

    # Display meal planning results based on user selections
    if submitted:
        # Get response from Gemini
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)

        # Display Gemini response
        st.write("Some of the best meals option:")
        st.write(response.text)




if page == "Contact Us":
    st.header("Contact Us")
    st.write("""
    Thank you for your interest in DocAdvidor! If you have any questions, feedback, or suggestions, please feel free to reach out to us.
    
    Email: contact@docadvisor.com
    
    Phone: +91 (...........)
    
    Address: 
    XXXX
    
    We look forward to hearing from you!
    """)

 
    
if page == "Home":
    # Title
    st.title("Disease Prediction")

    # Form for disease prediction
    with st.form("disease_prediction_form"):
        # Patient information
        gender = st.radio("Gender", ["Male", "Female"])
        age = st.number_input("Age", min_value=1, max_value=150, value=25)

        # Previous major diseases
        diseases = st.multiselect("Previous major diseases", ["None", "Diabetes", "Hypertension", "Heart Disease", "Asthma", "Other"])

        # Symptoms
        symptoms = st.text_input("Symptoms")

        # Lifestyle questions
        smoke = st.checkbox("Do you smoke?")
        drink = st.checkbox("Do you drink alcohol?")

        # Allergies
        allergies_options = ["None", "Peanuts", "Shellfish", "Gluten", "Dairy", "Eggs", "Soy", "Fish", "Other"]
        allergies = st.multiselect("Allergies", allergies_options)

        # Submit button
        submitted = st.form_submit_button("Predict Disease")
        
        # Generate prompt string based on user selections
        # Analyze user inputs to suggest possible major diseases
        possible_diseases = []
        if "Diabetes" in diseases:
            possible_diseases.append("Diabetes")
        if "Hypertension" in diseases:
            possible_diseases.append("Hypertension")
        if "Heart Disease" in diseases:
            possible_diseases.append("Heart Disease")
        if "Asthma" in diseases:
            possible_diseases.append("Asthma")

        prompt = f"Patient information:\nGender: {gender}\nAge: {age}\nPossible major diseases: {', '.join(possible_diseases) if possible_diseases else 'None'}\nSymptoms: {symptoms}\nLifestyle: Smoking - {'Yes' if smoke else 'No'}, Drinking - {'Yes' if drink else 'No'}\nAllergies: {', '.join(allergies)}"


        # Display disease prediction results based on user selections
        if submitted:
            # Get response from Gemini
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)

            # Display Gemini response
            st.write("Deasese:")
            st.write(response.text)



# def load_lottiefile(filepath: str):
#     with open(filepath, "r") as f:
#         return json.load(f)


# def load_lottieurl(url: str):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()
    

# # lottie_coding = load_lottiefile("lottiefile.json")  # replace link to local lottie file
# lottie_hello = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_M9p23l.json")

# st_lottie(
#     lottie_hello,
#     speed=1,
#     reverse=False,
#     loop=True,
#     quality="low", # medium ; high
#     height=None,
#     width=None,
#     key=None,
# )


# Add a footer with hyperlinks
st.markdown(
    """
    <style>
        footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #0E1117;
            color: white;
            text-align: center;
            padding: 10px 0;
        }
    </style>
    <footer>
        <a href='https://www.linkedin.com/in/kanav-nijhawan-442046250/'>Kanav Nijhawan</a> ⚡
        <a href='https://www.linkedin.com/in/navdeep-lakhlan-568b4926b?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app'>Navdeep </a> ⚡
        <a href='https://www.linkedin.com/in/animesh-jha-6bb9721b4/'>Animesh Jha</a> ⚡
        <a href='https://www.linkedin.com/in/siddharth-dubey-5b0136216/'>Siddharth Dubey</a>
        <br>
        © Tema 4bitCoder 2024
    </footer>
    """,
    unsafe_allow_html=True
) 