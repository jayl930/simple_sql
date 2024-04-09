import os
import streamlit as st
import dotenv
import argparse
from sql import execute_sql_query
from langchain.llms import AzureOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import load_prompt
from pathlib import Path
from PIL import Image
from langchain.chains import LLMChain
import hmac

dotenv.load_dotenv()
assert os.environ.get("NORTHWIND_DATABASE_URL"), "DB_URL not found in .env file"
assert os.environ.get("AZURE_OPENAI_KEY"), "key not found in .env file"
assert os.environ.get("AZURE_OPENAI_ENDPOINT"), "endpoint not found in .env file"
assert os.getenv(
    "AZURE_DEPLOYMENT_NAME"
), "AZURE_DEPLOYMENT_NAME not found in .env file"

NORTHWIND_DB_URL = os.environ.get("NORTHWIND_DATABASE_URL")
AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_KEY")
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
AZURE_DEPLOYMENT_NAME = os.environ.get("AZURE_DEPLOYMENT_NAME")

os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2023-09-01-preview"
os.environ["OPENAI_API_BASE"] = AZURE_OPENAI_ENDPOINT
os.environ["OPENAI_API_KEY"] = AZURE_OPENAI_KEY

llm = AzureChatOpenAI(
    deployment_name=AZURE_DEPLOYMENT_NAME,
)
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()


def main():
    current_dir = Path(__file__)
    # root_dir = [p for p in current_dir.parents][0]
    # frontend
    st.set_page_config(page_title="BADM 554 SQL Assistant", page_icon="🌄")
    st.sidebar.success("Select a page above")

    tab_titles = ["Results", "Query", "ER Diagram"]

    st.title("Northwind database assistant")
    prompt = st.text_input("Enter your query")
    tabs = st.tabs(tab_titles)
    with tabs[2]:
        image = Image.open("images/northwind.png")
        st.image(image, caption="Entity Relationship")

    prompt_template = load_prompt("prompts/northwind.yaml")
    final_prompt = prompt_template.format(input=prompt)

    sql_generation_chain = LLMChain(llm=llm, prompt=prompt_template, verbose=True)

    if prompt:
        query_text = sql_generation_chain(prompt)
        output = execute_sql_query(query_text["text"], NORTHWIND_DB_URL)

        with tabs[0]:
            st.dataframe(output)
        with tabs[1]:
            st.write(query_text["text"])


if __name__ == "__main__":
    main()
