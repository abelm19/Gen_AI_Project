#Streamlit for simple UI creation, website application with python
import streamlit as st
#Useful for loading external web based scripts or documents into the LLM
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    #title for the web app
    st.title("📧 Cold Mail Generator App")
    url_input = st.text_input("Enter a URL:", value="https://careers.nike.com/lead-data-scientist/job/R-56462")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            #exctract documents from website given by the user
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
