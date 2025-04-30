import streamlit as st
import google.generativeai as genai

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Jerry the AGI Assistant", layout="wide")

# ─── GEMINI CONFIG ─────────────────────────────────────────────────────────────
GOOGLE_API_KEY = "AIzaSyDlyyh_V98h8EPQNxQtkTyvIOykKVKhKKk"  # Replace with your real API key
genai.configure(api_key=GOOGLE_API_KEY)

# ─── DISCOVER AVAILABLE MODELS ─────────────────────────────────────────────────
@st.cache_data
def get_supported_models():
    all_models = genai.list_models()
    return [m.name for m in all_models if "generateContent" in m.supported_generation_methods]

available_models = get_supported_models()
if not available_models:
    st.error("❌ No models available for generate_content with your API key.")
    st.stop()

# ─── BASE PROMPT FOR EXPANDED AGI FUNCTIONALITY ───────────────────────────────
base_prompt = """
You are Jerry, an AI assistant designed to help the user with a wide range of tasks, from personal finance advice to technical troubleshooting. Your tone is clear, mature, and explanatory. You focus on providing thorough, actionable insights and adapting to the user’s needs. 

While you currently have a deep knowledge of finance, insurance, and business-related queries, you are capable of expanding your understanding and providing meaningful answers on a variety of topics. You can engage in intelligent, context-aware conversations and assist with complex problem-solving scenarios.

Your goal is to guide the user through their queries by breaking down problems, offering advice, and helping them make informed decisions across multiple domains.
"""

# ─── UI ────────────────────────────────────────────────────────────────────────
st.title("🤖 Jerry the AGI Assistant")
st.caption("Engage with Jerry — the adaptable AI assistant helping you with anything from insurance to business planning.")

model_choice = st.selectbox("Select model", available_models)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ─── DISPLAY CHAT HISTORY ──────────────────────────────────────────────────────
for msg in st.session_state.chat_history:
    role_label = "You" if msg["role"] == "user" else "Jerry"
    with st.chat_message(msg["role"]):
        st.markdown(f"**{role_label}:** {msg['content']}")

# ─── BOTTOM TEXT BOX & SEND ────────────────────────────────────────────────────
st.text_area("What do you want Jerry to help with today?", key="user_input", height=100)

if st.button("Send"):
    user_input = st.session_state.user_input

    if not user_input.strip():
        st.warning("Please enter a question or scenario.")
    else:
        with st.spinner("Jerry is thinking..."):
            try:
                # Combine base prompt with chat history for context
                full_prompt = base_prompt + "\n\n" + "\n".join(
                    [f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.chat_history]
                ) + f"\n\nUser: {user_input}\nJerry:"

                model = genai.GenerativeModel(model_name=model_choice)
                response = model.generate_content(full_prompt)
                assistant_reply = response.text.strip()

                # Add to chat history
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                st.session_state.chat_history.append({"role": "assistant", "content": assistant_reply})

                # Display Jerry's response
                st.markdown(f"**Jerry:** {assistant_reply}")

            except Exception as e:
                st.error(f"❌ Gemini error: {e}")
