import streamlit as st
import openai


'''standards_dict = {
    'Kindergarten': {
        'ELA': {
            'Reading: Literature': 'Understand and appreciate literature.',
            'Reading: Informational Text': 'Analyze, comprehend, and evaluate informational texts.'
        },
        'Math': {
            'Counting and Cardinality': 'Develop understanding of numbers and number systems.',
            'Operations and Algebraic Thinking': 'Understand and apply arithmetic operations and algebraic properties.'
        }
    },
    'Grade 1': {
        'ELA': {
            'Writing': 'Develop clear and coherent writing skills.',
            'Speaking and Listening': 'Cultivate effective communication skills.'
        },
        'Math': {
            'Number and Operations in Base Ten': 'Comprehend the place value system, perform operations with multi-digit whole numbers.',
            'Geometry': 'Understand and apply properties, measurement, and classification of geometric shapes.'
        }
    },
    'Grade 2': {
        'ELA': {
            'Language': 'Refine understanding and application of standard English grammar and usage.',
            'Reading: Literature': 'Understand and appreciate literature.'
        },
        'Math': {
            'Measurement and Data': 'Convert, interpret, and represent various types of measurement and data.',
            'Statistics and Probability': 'Develop the ability to investigate patterns, make inferences, and draw conclusions based on data.'
        }
    }
}

grade = st.selectbox('Select Grade', list(standards_dict.keys()))

subject = st.selectbox('Select Subject', list(standards_dict[grade].keys()))

standard = st.selectbox('Select Standard', list(standards_dict[grade][subject].keys()))

st.write('Description: ', standards_dict[grade][subject][standard])'''
# Set up the OpenAI API key
openai.api_key = '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'
if 'student_answers' not in st.session_state:
    st.session_state.student_answers = ""

if 'standard' not in st.session_state:
    st.session_state.standard = ""

if 'interest' not in st.session_state:
    st.session_state.interest = ""

if "Generate Content" not in st.session_state:
    st.session_state["Generate Content"] = False

if "Submit" not in st.session_state:
    st.session_state["Submit"] = False

if "Explain Evaluation Metrics" not in st.session_state:
    st.session_state["Explain Evaluation Metrics"] = False

if "Start Answering Questions" not in st.session_state:
    st.session_state["Start Answering Questions"] = False

if "Test using AI Answer" not in st.session_state:
    st.session_state["Test using AI Answer"] = False

if "Submit Answers" not in st.session_state:
    st.session_state["Submit Answers"] = False

# Session State also supports attribute based syntax
if 'content' not in st.session_state:
    st.session_state.content = ""

if 'rubric_content' not in st.session_state:
    st.session_state.rubric_content = ""



def generate_content_with_gpt(standard, interest):
    # Constructing the prompt for GPT-3.5
    
    # Define the system message
    system_msg = f" You are an expert at designing quizzes for any given common core learning standard: '{standard}' and interest topic : '{interest}' of a student. You excel at designing free response questions , providing context for each FRQ that can be used by the student answer the quesiton. FRQs produced should be of high-quality - including an introduction, context, and open-ended question. Provide atleast 3 questions"
    # Define the user message
    user_msg = f"Consider the following  Learning standard : '{standard}'  Interest : '{interest}'."

    # Calling GPT-3.5
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[{"role": "system", "content": system_msg},
                                            {"role": "user", "content": user_msg}])
    

    return response["choices"][0]["message"]["content"]
    #return "abc"

def generate_rubric_with_gpt(standard, interest, content):
    # Constructing the prompt for GPT-3.5
    
    # Define the system message
    system_msg = f" You are an expert at designing evaluation Metrics for any given common core learning standard: '{standard}' and interest topic : '{interest}'.  You need to design a good rubric for evaluating student responses to questions mentioned in '{content}'. Consider all questions and design a overall rubric. Dont design rubric for individual questions "
    # Define the user message
    user_msg = f"Consider the following  Learning standard : '{standard}'  Interest : '{interest}'."

    # Calling GPT-3.5
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[{"role": "system", "content": system_msg},
                                            {"role": "user", "content": user_msg}])
    

    return response["choices"][0]["message"]["content"]
    #return "abc"



def take_student_input(standard, interest, content, rubric_content):
    st.subheader("Answers")
    st.write("Questions :", content)
    user_input = st.text_area("Please enter your text here:")
    
    if st.button('Submit'):  # Changed to 'Submit Answers' to match the button
        if user_input:
            st.write("You submitted:")
            st.write(user_input)
            return user_input
            #response = evaluate_answer(standard, interest, content, rubric_content, user_input)
            #st.write(user_input)
        else:
            st.warning("Please enter your answers.")             


def evaluate_answer(standard,interest,content,rubric_content,input):
    # Taking input
    # Chat interface for student responses
                # Evaluate student responses using the rubric    
                # Define the system message
    
    system_msg = f"Consider the evaluation Metrics '{rubric_content}' for the given common core learning standard: '{standard}' and Questions in : '{content}'.  You need to evaluate and score this answer  '{input}' Provide step by step evaluation and score each answer and provide a final score . Provide the result in following form - Question :  Answer :  Result :  and then the overall result."
                # Define the user message
                
                # Calling GPT-3.5
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                        messages=[{"role": "system", "content": system_msg}]) 
    return response["choices"][0]["message"]["content"]
    #return input


def ai_agent_answer(standard,interest,content,rubric_content):
    # Taking input
    # Chat interface for student responses
    st.subheader("Agent Answers")

    system_msg = f"Act like a student who has been interest in '{interest}'. You have to Answer the questions given in '{content} by considering the introduction and context about the respective question ' "
                # Define the user message            
                # Calling GPT-3.5
    agent_answer = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                        messages=[{"role": "system", "content": system_msg}])
    
    st.write(agent_answer["choices"][0]["message"]["content"])
    response =  evaluate_answer(standard,interest,content,rubric_content,agent_answer["choices"][0]["message"]["content"])
    return response
# Streamlit UI

st.set_page_config(page_title="Edugenie", page_icon="👩‍🏫", layout="centered", initial_sidebar_state="auto", menu_items=None)

# Streamlit UI
st.title('Edugenie')

# Take user inputs
st.session_state.standard = st.text_input('Enter the learning standard (e.g., CCSS.ELA-LITERACY.W.4.9):')
st.session_state.interest = st.text_input('Enter the interest topic (e.g., baseball):')




if st.button('Generate Content'):
    st.session_state["Generate Content"] = not st.session_state["Generate Content"]
    with st.spinner("Thinking..."):
        st.session_state.content = generate_content_with_gpt(st.session_state.standard, st.session_state.interest)
        st.write(st.session_state.content)

if st.session_state["Generate Content"]:
        if st.button('Explain Evaluation Metrics'):
            st.session_state["Explain Evaluation Metrics"] = not st.session_state["Explain Evaluation Metrics"]
            with st.spinner("Gathering Evaluation Metircs"):
                st.session_state.rubric_content = generate_rubric_with_gpt(st.session_state.standard, st.session_state.interest, st.session_state.content)
                st.write(st.session_state.rubric_content)

if st.session_state["Explain Evaluation Metrics"]:
    if st.button('Start Answering Questions'):
        st.session_state["Start Answering Questions"] = True

if st.session_state["Start Answering Questions"]:
    with st.spinner("Loading..."):
        st.write("Questions :", st.session_state.content)
        user_input = st.text_area('Enter your Answes below')
    if st.button('Submit'):
        st.session_state["Submit"] = not st.session_state["Submit"]  # Changed to 'Submit Answers' to match the button
        if user_input:
            st.write("You submitted:")
            st.write(user_input)
            with st.spinner("Evaluating..."):
                response =  evaluate_answer(st.session_state.standard,st.session_state.interest,st.session_state.content,st.session_state.rubric_content,user_input)
                st.write(response)
        else:
            st.warning("Please enter your Answers")
                    
if st.session_state["Submit"]:            
            if st.button('Test using AI Answer'):
                st.session_state["Test using AI Answer"] = not st.session_state["Test using AI Answer"]
                with st.spinner("Loading..."):
                    st.session_state.result = ai_agent_answer(st.session_state.standard,st.session_state.interest,st.session_state.content,st.session_state.rubric_content)
                    st.write(st.session_state.result)

if st.sidebar.button("Test Using AI"):
    st.session_state.standard = "CCSS.ELA-LITERACY.W.4.9"
    st.session_state.interest = "baseball"
    #st.session_state["Test using AI"] = not st.session_state["Test using AI Answer"]
    with st.spinner("Loading..."):
        st.session_state.content = generate_content_with_gpt(st.session_state.standard, st.session_state.interest)
        st.session_state.rubric_content = st.session_state.rubric_content = generate_rubric_with_gpt(st.session_state.standard, st.session_state.interest, st.session_state.content)
        st.session_state.result  =  ai_agent_answer(st.session_state.standard,st.session_state.interest,st.session_state.content,st.session_state.rubric_content)
        st.write("Standard :",  st.session_state.standard)
        st.write("Interest :",  st.session_state.interest)
        st.write("Questions :",  st.session_state.content)
        st.write("Rubric Content:",  st.session_state.rubric_content)
        st.write("Answers and Evaluation :", st.session_state.result)
