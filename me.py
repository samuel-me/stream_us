
import crewai
import crewai_tools
from groq import Groq
from crewai import Agent
from langchain.llms import OpenAI

import os
from crewai import Agent, Task, Crew, Process

import string
from pypdf import PdfReader

from langchain_groq import ChatGroq


from docx import Document

## api keys
Groq_api_key = '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'
from langchain_groq import ChatGroq

import os
api_key = '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'
os.environ["GROQ_API_KEY"] = api_key

## the LLM

llm = ChatGroq(model="llama3-8b-8192",api_key=Groq_api_key)

## web scrapper
import requests
import bs4


def openup(name):
    topic = name
    topic = topic.replace(' ','+')
    print(topic)
    return topic

def parse(name):
    topic = openup(name)
    link = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q='+topic+'&btnG='
    res = requests.get(link)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text)

    a = 'gs_r gs_or gs_scl'
    b= 'gs_res_ccl_mid'
    all_ = soup.select('#'+b)
    some = all_[0].select('.gs_or')


    all_links = {}

    for i in range(10):
        topic = some[i].select('div > h3')[0].select('a')[0].getText()

        print(topic)
        try:

            mlink = some[i].select('.gs_or_ggsm')[0].select('a')[0].get('href')
    #         nam = some[i].select('div')[0].select('div')[0].select('div')[0].text
    #         print(nam)
            print(mlink)

        except:
            print('no topic for ', topic)
            mlink = ''

        all_links[topic] = mlink

    return all_links
# returns a lst that contains the names and links

def Sichub2(title):
    payload = { 'request': title}
    link = 'https://sci-hub.st/'
    # link = 'https://sci-hub.st/10.1109/icmla.2017.0-179'

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


    a = requests.post(link, data=payload, headers = headers)

    soup = bs4.BeautifulSoup(a.text)
    content = soup.select('embed')[0].get('src').replace('#navpanes=0&view=FitH','').replace('//','/')
    contents= 'https:/' + content
    r = requests.get(contents, stream=True)

    title = title.replace(':','')
    with open(title +'.pdf', 'wb') as file:
        file.write(r.content)

    print('DOne downloading: ', title )
    return title+'.pdf'


def google(title, url):
    dashboardFile = requests.get(url, allow_redirects=True)

    for i in string.punctuation:
        title = title.replace(i,'')

    title = title +'.pdf'
    open(title, 'wb').write(dashboardFile.content)
    print('google:', title)
    reader = PdfReader(title)
    return title


#AVX

down = []
def Avx():
  topic = openup()
  cat = classify(topic)
  link = 'https://arxiv.org/search/' + cat+ '?query=' + topic + '&searchtype=all&abstracts=show&order=-announced_date_first&size=50'
  res = requests.get(link)
  res.raise_for_status()
  soup = bs4.BeautifulSoup(res.text)
  a = soup.select('.arxiv-result')

  for i in range(10):
    b = a[i].select('p')
    topic = b[1].text
    url = a[i].select('span')[0].select('a')[0].get('href')
    topic = topic.replace('\n','')
    topic = topic.replace(' ','')
    topic = topic.replace("/","")


    dashboardFile = requests.get(url, allow_redirects=True)
    title = topic.replace(':','')
    name = topic+'.pdf'
    open(name, 'wb').write(dashboardFile.content)
    down.append(name)
    print('Done downloading:', title)

def classify(topic):
  from groq import Groq

  api_key = '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'

  client = Groq(api_key = api_key)
  completion = client.chat.completions.create(
      model="llama3-8b-8192",
      messages=[
          {
              "role": "user",
              "content": """ heyyy calssify this topic " """ +topic+ """ " appropriately and respond if it is related to the subjects: physics or computer Science or Mathematics or
              Quantitative Biology or Statistics or Electrical Engineering and Systems Science or Economics or Quantitative Finance
              limt your answer to just one subject
              give a very short output
              eg:
              output: physics"""
          }
      ],
      temperature=1,
      max_tokens=1024,
      top_p=1,
      stream=True,
      stop=None,
  )

  you = []
  for chunk in completion:
      you.append((chunk.choices[0].delta.content or ""))
  m = ''
  for j in you:
    m = m + j
  print(m)

  subjects = {'Physics':'physics',
 'Computer Science':'cs',
 'Mathematics':'math',
 'Quantitative Biology':'q-bio',
 'Statistics':'stat',
 'Electrical Engineering and Systems Science':'eess',
 'Economics':'econ',
 'Quantitative Finance':'q-fin',

 }
  for i in subjects.keys():
    if i in m:
      a = subjects[i]
      print(a)
  return (a)


# the tools 

from crewai_tools import PDFSearchTool
def ragtool(path):

  rag_tool = PDFSearchTool(pdf=path,
      config=dict(
          llm=dict(
              provider="groq", # or google, openai, anthropic, llama2, ...
              config=dict(
                  model="llama3-8b-8192",
                  # temperature=0.5,
                  # top_p=1,
                  # stream=true,
              ),
          ),
          embedder=dict(
              provider="huggingface", # or openai, ollama, ...
              config=dict(
                  model="BAAI/bge-small-en-v1.5",
                  #task_type="retrieval_document",
                  # title="Embeddings",
              ),
          ),
      )
  )
  return rag_tool


##  The agent workflow
def agents():
  agent1 =Agent(
      role="Ai guru",
      goal="find the methodology and summarize it ",
      backstory=" you are an Ai enthuisiat who is very passonate abiut te topic of the paper",
      verbose=True,
      llm = llm,
      tools = [rag_tool]
  )

  task1 = Task(
      expected_output=" a summary of the methoflogi",
      description="you are to fins and summarisze the methodology of the paper",
      agent=agent1,
  )

  agent2 =Agent(
      role="A professional technical writer ",
      goal="find the methodology and summarize it ",
      backstory=" you are a very hardworking technical writer who doesn't overlook mistakes ",
      verbose=True,
      llm = llm,
      context = [agent1]
  )

  task2 = Task(
      expected_output=" a better written content gotten from agent 1",
      description="rewrite the output of agent 1 in a better way, remove all the numbers and everything in brackets  ",
      agent=agent1,
  )

  my_crew = Crew(agents=[agent1,agent2], tasks=[task1,task2])
  inputs ={"question":"give me an email from the file "}

  crew = my_crew.kickoff()
  return crew
you = []   

def run(name):
    data = parse(name)

    err = []


    for i in data.keys():
        try:
            a = Sichub2(i)
            down.append(a)
        except:
            err.append(i)

    for i in err:
        try:
            b = google(i,data[i])
            down.append(b)
        except:
            print(i)

       
    for i in down:
        reader = PdfReader(i)
        try:
          global rag_rool
          rag_tool = ragtool(i)
          words = agents()
          you.append(words)
        except Exception as exc:
            print(exc)
          
      
            

    doc()
    download_pdf(pdf_path)

        
from docx import Document

def doc():
    documents = Document()
    file_name = 'Summary'
    documents.add_heading('AI Summary', 0)
    for i in range(len(you)):
      documents.add_heading(down[i].replace('/content/',''), level=1)
      documents.add_paragraph(you[i].raw)

    documents.save(file_name + '.docx')

import streamlit as st  # pip install streamlit


st.header(":mailbox: Hello researcher!")
topic = st.text_input(label="TOpic", placeholder="what are you working on?")




import streamlit as st
import os

def download_pdf(pdf_path):
    """your files woule be ready soon, wait for another go button ready"""
    
    
    """your files are ready"""
    if not os.path.exists(pdf_path):
        st.error(f"PDF file '{pdf_path}' not found.")
        return

    with open(pdf_path, 'rb') as f:
        pdf_bytes = f.read()

    st.download_button(
        label="Download file",
        data=pdf_bytes,
        file_name=os.path.basename(pdf_path),
        mime="application/docx"
    )

# Replace 'path/to/your/pdf.pdf' with the actual path to your PDF file
pdf_path = "Summary.docx"


# Create a Streamlit button to trigger the download
if st.button("fonwload"):
    run(topic)
    


#st.download_button('DOwnload button',data = 'h.csv', file_name = 'Summary.csv', mime ="text/docx")
# Use Local CSS File
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")





