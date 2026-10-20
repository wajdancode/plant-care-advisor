import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="🌿 Plant Care Advisor", page_icon="🌱")

# --- API Key Setup ---
api_key = st.secrets.get("GOOGLE_API_KEY", "")
if not api_key:
    api_key = st.sidebar.text_input("🔑 Enter your Google Gemini API Key", type="password")

if not api_key:
    st.sidebar.warning("⚠️ Add your API key to use the app")
else:
    genai.configure(api_key=api_key)
    # ✅ Using recommended latest model: Gemini 3.5 Flash
    model = genai.GenerativeModel("gemini-3.5-flash")

# --- Page Layout ---
st.title("🌿 Plant Care Advisor")
st.markdown("Upload a photo of your plant OR type its name — I'll tell you exactly how to care for it!")

# --- Input Section ---
tab1, tab2 = st.tabs(["📸 Upload Photo", "✍️ Type Plant Name"])
plant_name = ""
plant_image = None

with tab1:
    uploaded_image = st.file_uploader("Upload plant image", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        plant_image = Image.open(uploaded_image)
        st.image(plant_image, caption="Your Plant", use_container_width=True)

with tab2:
    plant_name = st.text_input("Enter plant name (e.g. Monstera Deliciosa, Aloe Vera)")

# --- Get AI Advice ---
def get_care_advice(name="", image=None):
    base_prompt = """
You are a friendly plant expert. Give clear, easy-to-read plant care advice in this format:

🌿 Plant Name & Identification:
[What plant it is / likely is]

💧 Watering:
- How often:
- How much:
- Pro tip:

☀️ Light Needs:
- Best light:
- Avoid:

🌡️ Temperature & Humidity:
- Ideal temp:
- Humidity preference:

🪴 Soil & Fertilizer:
- Soil type:
- Feeding schedule:

⚠️ Common Problems & Fixes:
- Yellow leaves:
- Brown tips:
- Drooping:

✅ Quick Summary:
[1–2 sentence recap]
"""
    if name and image:
        prompt = f"Identify and care for this plant named: {name}\n{base_prompt}"
        response = model.generate_content([prompt, image])
    elif name:
        prompt = f"Plant to research: {name}\n{base_prompt}"
        response = model.generate_content(prompt)
    elif image:
        prompt = f"Identify this plant and give full care instructions\n{base_prompt}"
        response = model.generate_content([prompt, image])
    else:
        return None
    return response.text

# --- Display Results ---
if st.button("🌱 Get Care Advice"):
    if not api_key:
        st.error("❌ Please enter your API key in the sidebar first!")
    else:
        if not plant_name and not plant_image:
            st.warning("⚠️ Upload an image OR type your plant's name first!")
        else:
            with st.spinner("🔍 Identifying plant & checking care tips..."):
                try:
                    advice = get_care_advice(plant_name, plant_image)
                    if advice:
                        st.success("✅ Plant Found! Here's your care guide:")
                        st.markdown(advice)
                    else:
                        st.error("Could not get advice — please try again.")
                except Exception as e:
                    st.error(f"❌ Something went wrong: {str(e)}")
