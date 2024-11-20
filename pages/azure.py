import streamlit as st
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_1.work_item_tracking.models import JsonPatchOperation
import ollama
import logging
import requests
import markdown
from datetime import datetime
from logging import getLogger
from config import azure


file_handler = logging.handlers.RotatingFileHandler(f'./data/azure-stories-log-{datetime.now().strftime("%Y%m%d%H")}.log', maxBytes=1024*10, backupCount=20)
logger = getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


organization_url = azure['organization_url']
personal_access_token = azure['personal_access_token']

col1, col2 = st.columns(2)

work_item_type = col2.selectbox("Select Type", ["User Story","Epic","Feature"])

suggestion = 'Please write me an Azure DevOps Story to [YOUR TEXT HERE] as a Software Engineer using Agile methodologies.\n Write in a professional Azure DevOps tone.'

if work_item_type == "Epic": 
  suggestion = 'Write me an Epic for Azure DevOps about\n [YOUR TEXT HERE] \nas a Product Owner using the good rules of the Agile methodologies.\nThe following sections are required: Title, Description, In Scope, Out of Scope, Dependencies, Success Criteria, Impact Analysis.\nWrite in a professional tone.'
if work_item_type == "Feature": 
  suggestion = 'Write me a Feature for Azure DevOps about\n [YOUR TEXT HERE] \nas a Product Owner using the good rules of the Agile methodologies. Write in a professional tone.'


st.title("💻 Azure WorkItems")

project_name = col1.selectbox(
    "Project Name",
    ("Finance", "CatGame", "SketchMarker"),
)

assign_to = col2.selectbox(
    "Assign To",
    ("pssp25@hotmail.com", "contributor1@gmail.nl","contributor2@hotmail.nl","contributor3@aegon.nl"),
)

send_azdo = st.checkbox("Send to Azure DevOps")

credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)
wit_client = connection.clients.get_work_item_tracking_client()


def find_line_with_title_or_user_story(lines):
  parts = lines.split('\n')
  for line in parts:
    new_line = line.replace("*", "").strip()
    if new_line.startswith(("Title:", "User Story:", "Story Name:")):
        return new_line[len(new_line.split(":")[0]) + 1:]
  return "User Story"


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
  created_work_item = wit_client.create_work_item(
       document=work_item_data,
       project=project_name,
       type=work_item_type
       )
  print(f"Work item created with ID: {created_work_item.id}")

  st.markdown(f"Created [{created_work_item.id}]({organization_url}{project_name}/_backlogs/backlog/{project_name}%20Team/Epics/?workitem={created_work_item.id})")


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
  title = find_line_with_title_or_user_story(story)
  
  if send_azdo:
    html_text = markdown.markdown(story.replace("\n","<br>"))
    create_workitem(title, html_text ,assign_to=assign_to)
  st.success("Done.")





