import streamlit as st
from google import genai

client = genai.Client(api_key=st.secrets["AQ.Ab8RN6LFgwep76-5_Iy2tf8ViTy6LpI244P5zQrAnXKLKPLls"])

SYSTEM_PROMPT = """You are a weather intelligence assistant for an India weather dashboard.
The 5 cities tracked are: Kochi, Chennai, Bangalore, Delhi, Mumbai.
You help users:
1. Compare weather conditions across these cities
2. Answer what-if questions (e.g. What if AQI crosses 200 in Delhi?)
3. Explain indices: Storm Alert, Water Stress, Outdoor Health Risk, Global Warming Signal
4. Give practical weather recommendations
Be concise and helpful."""

st.set_page_config(page_title="Weather AI Assistant", page_icon="🌦")
st.title("🌦 Weather AI Assistant")
st.caption("Ask me anything about weather across Kochi, Chennai, Bangalore, Delhi and Mumbai")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("e.g. Which city has the worst air quality?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    full_prompt = SYSTEM_PROMPT + "\n\n" + "\n".join(
        [f"{m['role']}: {m['content']}" for m in st.session_state.messages]
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=full_prompt
    )
    reply = response.text

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)