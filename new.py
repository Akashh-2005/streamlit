
import streamlit as st
import speech_recognition as sr
import pyttsx3
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import threading
import base64

load_dotenv()

# Load and encode your local image
@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data= f.read()
    return base64.b64encode(data).decode()

img= get_img_as_base64("priy.jpg")

# Initialize the LLM model
model = ChatGoogleGenerativeAI(model='gemini-1.5-flash')
st.title("🎀 MY POOKIEE <3")



st.markdown(f"""
<style>
  [data-testid="stMainBlockContainer"] {{
    background-image: url("https://www.fabvoguestudio.com/cdn/shop/files/pr-plor-0-pl2019-108-baby-pink-colour-pure-organza-plain-dyed-fabric-1.jpg?v=1687255519&width=1080");
    justify-content: center;
    height: auto;
    border-radius: 20px;
  }}

  [data-testid="stMain"] {{
    background-image: url("data:image/jpeg;base64,{img}");
    background-size:cover;
    background-position: ;
    margin:0;
    padding:o;
  }}

  h1 {{
    text-align: center;
  }}

  video {{
    margin-top: 20px;
    width: 100%;
    height: 100%;
    z-index: -1;
  }}
</style>
<video autoplay muted loop >
  <source src="https://motionbgs.com/media/2892/purple-sunset2.960x540.mp4" type="video/mp4">
</video>

""", unsafe_allow_html=True)




# Initialize pyttsx3 engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')

if "history" not in st.session_state:
    st.session_state.history = []

# Function to speak the AI response
lock = threading.Lock()

def speak(text):
    def _speak():
        with lock:
            engine.say(text)
            engine.runAndWait()
    
    threading.Thread(target=_speak).start()

# Set the rate and volume
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)




voices = engine.getProperty('voices')
for voice in voices:
    if 'zira' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

def transcribe_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, could not understand the audio."
    except sr.RequestError as e:
        return f"Speech recognition error: {e}"

# Initialize session state
if "listening" not in st.session_state:
    st.session_state.listening = False



# Buttons for controlling listening
def stop_speech():
    with lock:
        engine.stop()

# UI: Buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("▶️ Start Listening"):
        st.session_state.listening = True
with col2:
    if st.button("⏹️ Stop Listening"):
        st.session_state.listening = False
with col3:
    if st.button("🛑 Stop Speaking"):
        stop_speech()

# Optional text input
text_input = st.text_input("Or type your message here:")


# Decide what input to use
user_input = None
if st.session_state.listening:
    user_input = transcribe_speech()
elif text_input:
    user_input = text_input

# Process input
if user_input:
    st.markdown(f"**You:** {user_input}")
    if "Sorry" not in user_input and "error" not in user_input:
        response = model.invoke("user: " + user_input)
        text = response.content
        st.markdown(f"**PRIYAL:** {text}")
        speak(text)
    else:
        st.error(user_input)

