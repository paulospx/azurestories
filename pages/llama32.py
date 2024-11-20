import streamlit as st
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_1.work_item_tracking.models import JsonPatchOperation
import ollama
import logging
import requests
from datetime import datetime
from logging import getLogger, FileHandler
from config import azure


file_handler = logging.handlers.RotatingFileHandler(f'./data/delta-dash-log-{datetime.now().strftime("%Y%m%d%H")}.log', maxBytes=1024*10, backupCount=5)
logger = getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
for h in logger.handlers:
    if isinstance(h, FileHandler):
        logger.removeHandler(h)
logger.addHandler(file_handler)

organization_url =  azure['organization_url']
personal_access_token = azure['personal_access_token']

suggestion = 'Question here.'

st.title("💻 Llama 3.2")

credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)
wit_client = connection.clients.get_work_item_tracking_client()


def update_workitem(id, state):
  url = f"https://dev.azure.com/fabrikam/_apis/wit/workitems/{id}?api-version=7.1"
  st.text(url)
  token = personal_access_token.encode("ascii", "ignore")
  headers = {
    'Authorization': f'Bearer {token}',
    'Content-type': 'application/json'
    }  
  data = [  
     {
      "op": "add",
      "path": "/fields/System.State",
      "value": state
      }]
  result = requests.patch(url,json=data,headers=headers)
  st.text(result)


def create_workitem(title, description, assign_to):
  work_item_data = [
    JsonPatchOperation(
        op="add",
        path="/fields/System.Title",
        value=title,
        ),
    JsonPatchOperation(
        op="add",
        path="/fields/System.Description",
        value=description,
        ),
    JsonPatchOperation(
        op="add",
        path="/fields/System.AssignedTo",
        value=assign_to
    )
  ]  


question = st.text_area('Prompt please', suggestion, height=150)
if st.button('Send ⬆️', type='primary'):
  story = "Story Description Here"
  st.subheader("🧑 "+question)
  with st.spinner('Wait for it...'):
    response = ollama.chat(model='llama3.2', messages=[
      {
        'role': 'user',
        'content': question,
      },
    ])
    st.subheader("🤖 Answer")
    story = response['message']['content']
    story.replace("\n","<br>")
    logger.info("################################################################################")
    logger.info(question)
    logger.info(response['message']['content'])
    st.markdown(response['message']['content'])

  st.markdown("---")
  
  st.success("Done.")





