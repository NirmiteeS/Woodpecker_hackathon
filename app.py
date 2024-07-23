import streamlit as st
from src.data_loader import load_csv_data
from src.database import create_database, get_tables
from src.chatbot import initialize_chatbot
from langchain_core.messages import AIMessage, HumanMessage

@st.cache_resource
def setup():
    # Load CSV data
    dataframes = load_csv_data()
    # Create database and get the tables
    engine = create_database(dataframes)
    tables = get_tables(engine)
    # Initialize chatbot
    agent_executor, final_prompt = initialize_chatbot()
    return agent_executor, final_prompt, tables

agent_executor, final_prompt, tables = setup()

st.title("Business Data Chatbot")

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Input field for user questions
user_query = st.chat_input("Type a message...")

# Process the question when the submit button is clicked
if user_query is not None and user_query.strip() != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))
        
    response = agent_executor.run(final_prompt.format(question=user_query))
        
    st.session_state.chat_history.append(AIMessage(content=response))

# Display chat history
if not st.session_state.chat_history:
    with st.chat_message("AI"):
        st.markdown("Hi, I'm Chatbot. Ask me anything about the business data!")
else:
    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.markdown(message.content)
