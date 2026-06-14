import streamlit as st
from groq import Groq

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

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

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + 
                     [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            max_tokens=500
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
    except Exception as e:
        st.error(f"Error: {str(e)}")
