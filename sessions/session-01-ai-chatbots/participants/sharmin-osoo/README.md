# Welcome! This AI chatbot is here as your networking and community finder mini assistant! 

## What is Event&Community Finder all about?

This is a conversational tool that asks a user three things, or at least ensure it has these three things: their location, which days they’re free, and whether they want tech, business, or career-focused events. The more specific the more tailored the response, for example under 'Tech event' you could want one focused on AI agents.  Once it has those inputs, the ai chatbot searches for available events on platforms like Meetup and Eventbrite. It then returns a short, useful list of matches, in the form of a table — ideally with event titles/name, dates, times, and links and a brief summary of what it's about. Over time, this may develop so that users can refine their taste, save preferences to a csv file, or subscribe to weekly digests, but the core is simply: “Tell me where you are and when you’re free; I’ll find the interesting rooms you could walk into.”. 

# How to set up 

### 1. Install Dependencies

```bash
pip install -r code/requirements.txt
```

### 2. Set Up Your API Key

Create a `.env` file in the project root:

```bash
GEMINI_API_KEY=your-gemini-api-key-here
```

Get your API key: [Gemini API Key Setup Guide](../../getting-started/gemini-api-key-setup.md)


#### what is included:
chatbot.py - building of the chatbot, where we call the api, create conversation memory, and add parameters
requirements.txt - ptyhon dependencies
.env - where the API key is kept


### 3. Run the Demo

```bash
python wcc_demo.py
```


# How to run it 



# What i learned 


# Challenges faced
My first system prompt, was not giving explicit enough instructions on searching for events, therefore the model resulted to giving advice and recommend which sites to use for events, rather than suggesting the actual events using the sites recommended.

# Future improvements

For future improvements from Version 1, i am keen to create a more user friendly interface. I would like to add a context window that the AI model can leverage for more extra information to give the user a more well rounded response, that is tailored to what the app's purpose. 


