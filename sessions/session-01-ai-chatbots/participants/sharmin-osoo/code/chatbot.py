#import libraries 
import os
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv

# setting the model name being used
MODEL_ID = 'gemini-2.5-flash-lite'

#if statememt to check the dotenv file found the env. file, and prints out a messeage in return
loaded = load_dotenv()
if loaded:
    print("env. loaded")
else:
    print("env. not found, nothing changed")

#This is done once at the start using enter your API key below, an if statement to ensure the API key is configured
api_key = os.getenv('GEMINI_API_KEY') or os.getenv( "GOOGLE_API_KEY") or os.getenv("API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    print(f"✓ API configured: {bool(api_key)}")
else:
    print("✗ WARNING: No API key found. Set GEMINI_API_KEY or GOOGLE_API_KEY environment variable.")

print("We're ready to Go!")
print("=" * 50)

#this is the prompt that will give instructions to the bot on how to respond, what context might be helpful, and a comprehensive idea of it's role and tasks
#''' SYSTEM PROMPT '''

event_system_prompt = ''' 
ABOUT
A Startup reality check Assistant, You are can be referred to as 'Bartman AI'
# GOAL : Act as a Startup Idea Reality Check Assistant and Business Mentor. Your primary function is to provide rapid, realistic market validation for new business concepts.
# You help users quickly discover their market size estimations, closest competitors, customer pain points.
# Your main focus is Market Validation (Size, Competition, Pain Points). Searches must utilise web capabilities across business websites, trusted reviews (Google/Trustpilot), relevant social platforms (Reddit, Twitter,spotify), news, and established business literature and credible business people.
# You return a well structured validation, with problem clarity, competition density you can base this in the region they are in, and give perspective on expansion, potenital customers and immediate and future risks to consider.

# OUTPUT
# Deliver a highly structured business validation and recommendation, including a summary table and strategic advice.

# RECOMMENDATIONS
# Include actionable advice on leveraging AI and specific, low-cost technology stacks for automation and efficiency.
# Quickly recognise pitfalls that could come in the near future, and give recommendation on systems that can be built to overcome them

PERSONALITY
You are friendly, practical, efficient, and supportive.
You act as a business mentor, a business coach and realistic about the business landscape and have knowledge on how the latest technology and systems can provide efficiency.
You keep explanations short, focused, avoid unnecessary filler, highly structured and pay attention to detail.
You encourage the user to review their business model, but highlight strengths with an encouraging tone you are optimistic, and give practical approach.

# HOW TO HELP 
# You answer questions about how founders, startups or small business owners can scale using online resources
# You encourage further research and show frameworks that have been practiced in business to support their research
# Provide supportive advice, but you are realistic about what can be achieved and what could require additional capabilities.
# If you don't know know anything specific then ask them to provide more context, or offer alternaive solutions that could support their research or business plan/ proposal

# SEARCH BEHAVIOR (MANDATORY)
# When the user has provided all required inputs, you MUST perform deep web searches focused on:
# 1. Business Models and Company Websites
# 2. Competitor Analysis (platforms, Trustpilot, Google Reviews)
# 3. Market Saturation, Opportunities, and Gaps
# 4. Target Audience Pain Points
# 5. Idea Feasibility based on current/future technological trends.
# 6. Search for any local or regional communities or if it is an online platform give online suggestions for funding, or programme with access to funding, based on their business idea and how they can leverage it

# RETURN FORMAT
# The final result MUST be returned in a comprehensive set of headers with a paragraph for each, ONLY USE what is appropriate.
# – Market size and potential Market size in the next 3-5 years
# – Competitors (both big and small)
# – Common customer pain points
# – Current market conditions & Feasibility
# – Recommendations on utilising Technology to stay ahead and Systems for efficiency
# – Raising Capital / Funding (local perspective, most suitable way based on their scenario) - this is optional and only return if the user requests

# STRICT OUTPUT RULES
# • DO NOT list platforms or search steps.
# • DO NOT use hypothetical or untested suggestions. ONLY return recommendations based on proven, tried-and-tested business formulas and strategies.
# • Do not add extra paragraphs outside of the structured advice. Keep it tight and helpful.

If you do not understand the business or cannot find sufficient information about competitors
- Give alternative, close competitors.
- Clearly state that research around their industry/product/service is limited.

Conversation Focus
Stay focused on business advice unless the user explicitly shifts topic.
'''
# ===================================================================================
# create a basic API call

def api_call():
#create a model instance 
    model = genai.GenerativeModel(MODEL_ID)

    # create a request 
    response = model.generate_content ("I would like to start an Ai personalised app but i don't know if it has potential to do well in this market, please help?")
        
    print(f"\n✅ Response:\n{response.text}")

    print("\n It works!🥳")

#call the function to make the API call     
#api_call()
# ===================================================================================
# Add personality using the system prompt, this allows the model to get more context and information around what you are building
def adding_personality():

    print("\n" + "=" * 100)

    model_personality = genai.GenerativeModel(
        MODEL_ID,
        system_instruction= event_system_prompt
    )
    
    #Test Questions 

    test = [
        "Where can i find useful resources that can guide me on starting an AI business. Do you need more information?"
    ]

    print("/n This test with the system prompt")

    for question in test:
        print(f"Q: {question}")
        # this generated a response based on the question asked from the test list
        response = model_personality.generate_content(question)
        print(f' Answer:✅ {response.text}\n')
        print('\n'+ "=" * 100)

    
    print('\n A friendlier response with more context from the system prompt')

adding_personality()
# ===================================================================================
# create a new function for conversation memory
# add conversation memory 
# adding conversation context, then building a multi turn conversation, including memory for improved used experience'''
def conversation_memory():

    class StartupBot:
        def __init__(self):
            self.model = genai.GenerativeModel(
                MODEL_ID,
            system_instruction = event_system_prompt
            )
            self.conversation_history = []

        def chat(self,user_prompt):
            self.conversation_history.append({'role':'user','parts':[user_prompt]})
            response = self.model.generate_content(self.conversation_history)
            self.conversation_history.append({'role':'model','parts':[response.text]})
            return response.text
    
    chatbot = StartupBot()
    
    #test messages 
    msguno = "Hi Bartman AI, I'm Sharmin"
    print('My intro',msguno)
    responseuno = chatbot.chat(msguno)
    print('First response:', responseuno)
    msgdos = "Could i get some guidance on what you can assist me with?"
    print('My second input:', msgdos)
    responsedos = chatbot.chat(msgdos)
    print('Second response:', responsedos)
    msgtres = "I would like to start a selling herbal products in the UK that are being produced in Kenya , through my own website, i don't know where to start"
    print('My third input:',msgtres)
    responsetres = chatbot.chat(msgtres)
    print('Third reasponse:',responsetres)

conversation_memory()

#pseudocode
# define a new class 
# this will be a chatbot with comversation memory
#create the first method, which will include the model id, and system instruction, using the generativemodel function. 
# create a list for the conversation to be appended/ saved.

#create a second methond/function that takes two arguments, the first being self, and the second being user input
# use the conversation history object and create a dictionary, that appends role:user, and parts and then calls the [user input]
# create a local variable called  response, we passs the instance variable self.model and generate_content and pass the self.coversation history in parethensis
# use the instance variable conversation history and append role:model and parts then pass the response.text, these are the data structure's dictated by gen AI model
#  then return the response in text 

#create a variable class instance that calls the class name, then you have the variable

# write the first message 
# test the conversation memory' 
# message one could be introducing yourself 
# message 2, can be another follow up question, the bot should store the memory of your name 
# message 3 - ask the chatbot if they remember your name
# message variable
# print the message
#create a reposne variable and callthe chatbot instance variable and the chat method
# passing the variable in line 158 
#create a second message and follow the same method
# create a third message
# print a message to say that thi step is complete
# this all needs to sit in the same conversation memory function

# ===================================================================================
# MODEL PARAMETERS 
# create a function for model parameters
#  inside the function 
# Temperature affects creativity, top_p affects diversity, how to tune parameters for different use cases'''

def model_parameters():
    question = "Give me business ideas that i can explore in areas that are currently untapped or communities that are underserved in the UK, be creative with your suggestions"
    print (f" \n Question: {question} \n ")
    print (f"Examples of different Temperature changes")

    temperature = [
        (0.0, "Deterministic, very plain and repetitive"), 
        (0.7, "Balanced, between creative and coherence"),
        (1.15, "Very Creative, Diverse and unpredictable")
    ]

    for temp, descript in temperature:
        print(f'{temp}, {descript}')
        Generation_config = genai.types.GenerationConfig(
            temperature=temp,
            top_p= 0.5,
            max_output_tokens=150
        )

        model_temp = genai.GenerativeModel(MODEL_ID,
        generation_config=Generation_config)

        response = model_temp.generate_content(question)

        print(f" The response: {response.text}")
    print('Higher temperatures are more creative')

model_parameters()

#pseudocode
#create a variable that is a question asking the modoel to write a creative message 
# print the question and say that this is the creativity level at the moment
#create a list for the temperatures, 0.0 deterministic, 0.7, 1.5, store the figures in a tuple)
#create a for loop that looks in the temperatures list and prints the temp and description
# in the same for loop create a variable called generation_config = which calls genai.types.generationconfig, and passes
# temperature which will be from the temperature key, max_output tokens and the top_p  
# then create a model temp variable - this calls the gen ai generative model and passes model id and generation config = generationconfig variable
# still inside the for loop create a variable for response, calling the model_temp variable and generate content, then pass
# the question to generate the content and create a response 
#print the reponse text in the loop 
# print the last message that shows how you can  notice a high temperature is more creative response.



# ===================================================================================
# WEB INTERFACE
def streamlit_interface ():

    try:
        import streamlit as st
    except ImportError:
        print('Streamlit not installed, import error')
        return
    
    st.set_page_config(
    page_title="Startup Reality Check Assistant",
    page_icon="💸",
    layout="centered")

    st.title("Hey I'm Bartman AI - Your Startup Reality Check assistant")
    st.markdown('#### I specialise in providing you in detail, honest and realistic feedback about your business ideas!\n I can help you with market research and provide unique suggestions on how you can leverage the latest technological platforms and tools such as AI')

    #side bar with parameters 
    st.sidebar.header('Adjust the parameters on your model to make the responses more creative or less creative')
    temp_param = st.sidebar.slider("Temperature",0.0,2.0,0.7,0.1)
    max_output_toks= st.sidebar.slider("Maximum Tokens",50,500,100,50)
    top_p_params = st.sidebar.slider("Top-p",0.1,1.0,0.7,0.1)

    # Initialize session state for conversation history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Hello! I am your go-to for all your business ideas that you would like to see flourish, but just need that extra help and direction!"
        })
    
    # Display conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("I am not sure where to start, can you give me direction on what information you need to help me"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("I am Thinking this through... bare with me.."):
                # Configure model with user settings
                generation_config = genai.types.GenerationConfig(
                    temperature=temp_param,
                    max_output_tokens=max_output_toks,
                    top_p=top_p_params
                )
                
                model_ui = genai.GenerativeModel(
                    MODEL_ID,
                    generation_config=generation_config,
                    system_instruction=event_system_prompt
                )
                
                # Create conversation context
                context = "\n".join([
                    f"{msg['role']}: {msg['content']}" 
                    for msg in st.session_state.messages[-5:]  # Last 5 messages
                ])
                
                full_prompt = f"Conversation context:\n{context}\n\nUser: {prompt}"
                response = model_ui.generate_content(full_prompt)
                
                st.markdown(response.text)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    
    # Display current settings
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Current Settings:**")
    st.sidebar.write(f"🌡️ Temperature: {temp_param}")
    st.sidebar.write(f"📝 Max Tokens: {max_output_toks}")
    st.sidebar.write(f"🎯 Top-p: {top_p_params}")
    
    # Usage instructions
    with st.expander("💡 How to use this bot"):
        st.markdown('''
        **Try asking:**
        - Where can i start with forumlating a business plan?
        - Which technologies should i leverage for my small local hair salon business to keep me competitive in Manchester?
        - Which funding opportunities are available for black female founders?
        - I have never started my own business where do i start?
        
        **Experiment with settings:**
        - 🌡️ **Temperature**: Higher = more creative responses
        - 📝 **Max Tokens**: Longer responses
        - 🎯 **Top-p**: Lower = more focused responses
        ''')

streamlit_interface()   


# create a function for streamlit interface 
# inside the function create a try and except , import streamlit for try 
# except importerror: then print not installed 
# set the page config then pass - page title, page icon and layout 
#set the title and a markdown as a subtitle 
#create a sidebar with controls for temprature, max token and top p
