from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits import create_sql_agent
from .config import DATABASE_URI, API_KEY, CSV_FILES

def initialize_chatbot():
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=API_KEY)
    db = SQLDatabase.from_uri(DATABASE_URI, include_tables=list(CSV_FILES.keys()))
    chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

    final_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", """You are a helpful AI assistant expert in querying SQL databases to find answers to user questions about company data. 
                            Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.
                            The following information is about the tables, understand this and then answer the questions asked by the user:
                            The accounts table contains columns like `accounts` which is the company name. It shows the details of the company like annual revenue (`revenue`), their subsidiaries (`subsidiary_of`), the number of employees (`employees`), the year the company was established (`year_established`), the sector they belong to (`sector`), and their office location (`office_location`).
                            The products table contains information about the products offered by the companies. It includes columns like `product`, `series`, and `sales_price`.
                            The sales_pipeline table tracks sales opportunities. It includes columns like `opportunity_id`, `sales_agent`, `product`, `accounts` (company name), `deal_stage`, `engage_date`, `close_date`, and `close_value`.
                            The sales_teams table contains information about sales agents, their managers, and their regional offices. It includes columns like `sales_agent`, `manager`, and `regional_office`.
                            
                            Key Points:
                            - The `accounts` column in the accounts table represents the company name.
                            - The `revenue` column in the accounts table indicates the annual revenue of the company.
                            - To find the most profitable company for a specific year, look at the `revenue` column for that year.
                            - The sales_pipeline table can be used to track sales activities and their outcomes.
                            - The sales_teams table provides details about sales agents and their managerial hierarchy.
                            
                            If table is asked display the sql output in table format.                            
                            Otherwise display the final sql output in natural language."""),
            ("user", "{question}\\n ai: ")
        ]
    )

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent_executor = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True, handle_parsing_errors=True)

    return agent_executor, final_prompt