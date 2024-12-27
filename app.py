import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler

# Set up Streamlit page configuration
st.set_page_config(page_title="General Knowledge Assistant", page_icon="🧭")
st.title("General Knowledge Assistant")

# API Key input for Groq
groq_api_key = st.sidebar.text_input(label="Groq API Key", type="password")

if not groq_api_key:
    st.info("Please add your Groq API key to continue")
    st.stop()

# Initialize the LLM (Groq API - llama-3.1-70b)
llm = ChatGroq(model="llama-3.1-70b-versatile", groq_api_key=groq_api_key)

# Initialize Wikipedia tool for information retrieval
wikipedia_wrapper = WikipediaAPIWrapper()
wikipedia_tool = Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="A tool for searching the Internet to find information on various topics, including general knowledge."
)

# Prompt template for general knowledge questions
prompt = """
You are a knowledgeable assistant. Your task is to answer the user's questions accurately, using your general knowledge.
If the answer is not readily available in your knowledge base, search Wikipedia for relevant information.
Your information should be accurate and up to date.Whenever I tell ypu to write essay give a title also to the essay.
Question: {question}
Answer:
"""

# Initialize the prompt template
prompt_template = PromptTemplate(
    input_variables=["question"],
    template=prompt
)

# Combine all the tools into a chain for answering general knowledge questions
chain = LLMChain(llm=llm, prompt=prompt_template)

# Reasoning tool for logic-based or factual questions
reasoning_tool = Tool(
    name="Reasoning tool",
    func=chain.run,
    description="A tool for answering general knowledge questions using logical reasoning and factual information.Try to use the latest information"
)

# Initialize the agent with the tools and LLM
assistant_agent = initialize_agent(
    tools=[wikipedia_tool, reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True
)

# Initialize session state for message history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm your general knowledge assistant. Feel free to ask me any question!"}
    ]

# Display the conversation history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])

# Get the user's question
question = st.text_area("Enter your question:", "Please enter your general knowledge question here")

# Handle the button click to process the question
if st.button("find my answer"):
    if question:
        with st.spinner("Generate response.."):
            st.session_state.messages.append({"role":"user","content":question})
            st.chat_message("user").write(question)

            st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
            response=assistant_agent.run(st.session_state.messages,callbacks=[st_cb]
                                         )
            st.session_state.messages.append({'role':'assistant',"content":response})
            st.write('### Response:')
            st.success(response)

    else:
        st.warning("Please enter the question")
