import streamlit as st
from src.data_loader import load_csv_data
from src.database import create_database, get_tables
from src.chatbot import initialize_chatbot
from langchain_core.messages import AIMessage, HumanMessage
import re

@st.cache_resource
def setup():
    # Load CSV data
    dataframes = load_csv_data()
    # Create database and get the tables
    engine = create_database(dataframes)
    tables = get_tables(engine)
    # Initialize chatbot
    agent_executor, final_prompt = initialize_chatbot()
    return agent_executor, final_prompt, tables, dataframes

agent_executor, final_prompt, tables, dataframes = setup()

st.title("CRM Data Chatbot")

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Input field for user questions
user_query = st.chat_input("Type a message...")

def plot_chart(chart_type, dataframe, x_col, y_col):
    if x_col not in dataframe.columns or y_col not in dataframe.columns:
        st.error(f"It looks like the columns '{x_col}' or '{y_col}' don't exist in the {dataframe} data. Could you double-check the column names?")
        return None
    
    if chart_type == "line":
        chart = st.line_chart(dataframe.set_index(x_col)[y_col])
    elif chart_type == "bar":
        chart = st.bar_chart(dataframe.set_index(x_col)[y_col])
    else:
        st.error(f"I'm not sure how to create a '{chart_type}' chart. Could you try 'line' or 'bar' instead?")
        return None
    return chart

def parse_command(command):
    # Regex pattern to capture natural language commands
    pattern = re.compile(r'(?P<chart_type>line|bar) chart of (?P<y_col>\w+) against (?P<x_col>\w+) from the (?P<dataframe>\w+) data', re.IGNORECASE)
    match = pattern.search(command)
    if match:
        return match.group('chart_type').lower(), match.group('dataframe'), match.group('x_col'), match.group('y_col')
    return None

# Process the question when the submit button is clicked
if user_query is not None and user_query.strip() != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    
    command = parse_command(user_query)
    if command:
        chart_type, dataframe_name, x_col, y_col = command
        if dataframe_name in dataframes:
            response = f"Here’s a {chart_type} chart of {y_col} against {x_col} from the {dataframe_name} data."
            st.session_state.chat_history.append(AIMessage(content=response))
            st.session_state.chat_history.append({
                "type": "chart",
                "chart_type": chart_type,
                "dataframe_name": dataframe_name,
                "x_col": x_col,
                "y_col": y_col
            })
        else:
            response = f"I couldn't find the data you're looking for. Could you check if the '{dataframe_name}' dataset exists?"
            st.session_state.chat_history.append(AIMessage(content=response))
    else:
        response = agent_executor.run(final_prompt.format(question=user_query))
        st.session_state.chat_history.append(AIMessage(content=response))

# Display chat history
if not st.session_state.chat_history:
    with st.chat_message("AI"):
        st.markdown("Hi there! I'm here to help you with CRM data. How can I assist you today?")
else:
    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.markdown(message.content)
        elif isinstance(message, dict) and message.get("type") == "chart":
            dataframe_name = message["dataframe_name"]
            chart_type = message["chart_type"]
            x_col = message["x_col"]
            y_col = message["y_col"]
            if dataframe_name in dataframes:
                plot_chart(chart_type, dataframes[dataframe_name], x_col, y_col)
