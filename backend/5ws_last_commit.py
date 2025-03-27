import streamlit as st
import openai
import os
import json
from datetime import datetime
import pathlib
import requests  # For Flask API calls
from rules import RuleEngine  # Your rules.py

# Create logs directory if it doesn't exist
LOGS_DIR = "5ws_log"
pathlib.Path(LOGS_DIR).mkdir(exist_ok=True)

# Function to log session data
def log_session_data(session_data, step_name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_id = st.session_state.get("session_id", timestamp)
    log_file = os.path.join(LOGS_DIR, f"session_{session_id}.log")
    
    # Create a structured log entry with metadata
    log_entry = {
        "timestamp": timestamp,
        "session_id": session_id,
        "step": step_name,
        "iteration": st.session_state.get("iteration", 1),
        "data": session_data,
        "debug_info": {
            "app_state": {
                "w_entries": st.session_state["app_state"].get("w_entries", {}),
                "selected_keywords": st.session_state["app_state"].get("selected_keywords", {}),
                "current_synopsis": st.session_state["app_state"].get("current_synopsis", ""),
                "is_first_round": st.session_state["app_state"].get("is_first_round", True)
            }
        }
    }
    
    # Write to log file with pretty printing for better readability
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry, indent=2) + "\n")
    
    # Also write to a separate debug log file
    debug_log_file = os.path.join(LOGS_DIR, f"debug_{session_id}.log")
    with open(debug_log_file, "a") as f:
        f.write(json.dumps(log_entry, indent=2) + "\n")

# Set page to wide mode
st.set_page_config(layout="wide")

# Add custom CSS for the scrollable history container and reduced line spacing
st.markdown("""
    <style>
    .history-container {
        height: 600px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #e6e6e6;
        border-radius: 0.5rem;
    }
    
    /* Reduce line spacing in all text elements */
    .stMarkdown p {
        margin-bottom: 0.3rem !important;
        line-height: 1.2 !important;
    }
    
    /* Reduce spacing in bullet points */
    .stMarkdown ul {
        margin-bottom: 0.3rem !important;
        padding-left: 1.5rem !important;
    }
    
    .stMarkdown li {
        margin-bottom: 0.1rem !important;
        line-height: 1.2 !important;
    }
    
    /* Reduce spacing in expanders */
    .streamlit-expanderHeader {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
    }
    
    .streamlit-expanderContent {
        padding-top: 0.3rem !important;
        padding-bottom: 0.3rem !important;
    }
    
    /* Reduce spacing in subheaders */
    h2, h3 {
        margin-top: 0.5rem !important;
        margin-bottom: 0.3rem !important;
        line-height: 1.2 !important;
    }
    
    /* Adjust spacing in text areas */
    .stTextArea textarea {
        line-height: 1.2 !important;
        padding: 0.5rem !important;
        font-size: 0.9rem !important;
    }
    
    /* Adjust spacing in suggestions sections */
    div[data-testid="stExpander"] > div {
        padding-top: 0.3rem !important;
        padding-bottom: 0.3rem !important;
    }
    
    /* Make horizontal rules more compact */
    hr {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Additional text area styling */
    .stTextArea > div > div {
        padding: 0.3rem !important;
    }

    /* Adjust text area label spacing */
    .stTextArea label {
        margin-bottom: 0.3rem !important;
    }

    /* Add prominent styling for the current synopsis */
    .current-synopsis {
        font-size: 1.2rem !important;
        font-weight: 500 !important;
        padding: 1rem !important;
        background-color: #f0f2f6 !important;
        border-radius: 0.5rem !important;
        margin: 1rem 0 !important;
        border-left: 4px solid #1f77b4 !important;
    }
    </style>
""", unsafe_allow_html=True)

def test_custom_assistant():
    """Advanced test function with comprehensive token and error tracking."""
    try:
        # Initialize the client
        client = openai.OpenAI()
        
        # Comprehensive token tracking using API response
        token_tracking = {
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_tokens": 0,
            "message_tokens": 0,
            "instructions_tokens": 0,
            "api_responses": []  # Store detailed API response information
        }
        
        # List all assistants first
        st.write("\nChecking available assistants:")
        assistants = client.beta.assistants.list()
        for assistant in assistants.data:
            st.write(f"\nAssistant: {assistant.name}")
            st.write(f"ID: {assistant.id}")
            st.write(f"Model: {assistant.model}")
            
            # Retrieve detailed assistant configuration
            assistant_details = client.beta.assistants.retrieve(assistant.id)
            
            # Track instructions tokens if present
            if assistant_details.instructions:
                try:
                    import tiktoken
                    encoding = tiktoken.get_encoding("cl100k_base")
                    instructions_tokens = len(encoding.encode(assistant_details.instructions))
                    token_tracking["instructions_tokens"] += instructions_tokens
                    st.write(f"Instructions Token Count: {instructions_tokens}")
                except ImportError:
                    st.warning("Tiktoken not installed. Unable to precisely count instruction tokens.")
        
        # Use the specific assistant ID
        assistant_id = "asst_gBino8HQs7HoxblezP4eKrQw"
        st.write(f"\nAttempting to use assistant ID: {assistant_id}")
        
        # Prepare a multi-part test message with controlled complexity
        test_messages = [
            "Develop a clinical trial synopsis for lung cancer.",
            "Focus on the target patient population.",
            "Specify key inclusion and exclusion criteria.",
            "Outline the primary research objective."
        ]
        
        # Create thread with comprehensive error handling
        try:
            thread = client.beta.threads.create()
            st.write(f"Thread ID: {thread.id}")
        except Exception as thread_error:
            st.error(f"Thread Creation Error: {thread_error}")
            return False
        
        # Add messages to thread
        try:
            for msg in test_messages:
                message_response = client.beta.threads.messages.create(
                    thread_id=thread.id,
                    role="user",
                    content=msg
                )
                # Track message tokens using tiktoken if available
                try:
                    import tiktoken
                    encoding = tiktoken.get_encoding("cl100k_base")
                    message_tokens = len(encoding.encode(msg))
                    token_tracking["message_tokens"] += message_tokens
                    token_tracking["total_input_tokens"] += message_tokens
                except ImportError:
                    st.warning("Tiktoken not installed. Unable to precisely count message tokens.")
        except Exception as message_error:
            st.error(f"Message Creation Error: {message_error}")
            return False
        
        # Run with explicit, concise instructions
        run_instructions = (
            "Provide a concise clinical trial synopsis. "
            "Limit response to essential details. "
            "Focus on clarity and precision."
        )
        
        try:
            run = client.beta.threads.runs.create_and_poll(
                thread_id=thread.id,
                assistant_id=assistant_id,
                instructions=run_instructions
            )
        except Exception as run_error:
            st.error(f"Run Creation Error: {run_error}")
            return False
        
        # Comprehensive run status handling
        if run.status == "failed":
            st.error("Run failed")
            error_details = getattr(run, 'last_error', None)
            if error_details:
                st.write("Error Details:", error_details)
                # Log detailed error information
                log_session_data({
                    "error": str(error_details),
                    "token_tracking": token_tracking
                }, "run_failure")
            return False
        
        # Retrieve and analyze messages
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        
        # Find and analyze assistant's response
        assistant_messages = [
            msg for msg in messages.data 
            if msg.role == "assistant"
        ]
        
        for msg in assistant_messages:
            if msg.content:
                for content in msg.content:
                    if content.type == "text":
                        response_text = content.text.value
                        
                        # Track output tokens using tiktoken if available
                        try:
                            import tiktoken
                            encoding = tiktoken.get_encoding("cl100k_base")
                            response_tokens = len(encoding.encode(response_text))
                            token_tracking["total_output_tokens"] += response_tokens
                        except ImportError:
                            st.warning("Tiktoken not installed. Unable to precisely count response tokens.")
                        
                        st.write(f"Response Text: {response_text}")
        
        # Final token usage summary
        st.write("\n--- Token Usage Summary ---")
        for key, value in token_tracking.items():
            st.write(f"{key}: {value}")
        
        # Log comprehensive metrics
        log_session_data({
            "token_tracking": token_tracking,
            "thread_id": thread.id,
            "assistant_id": assistant_id
        }, "token_analysis")
        
        return True
    
    except Exception as e:
        st.error(f"Comprehensive Test Failed: {str(e)}")
        # Log unexpected errors
        log_session_data({
            "error": str(e),
            "error_type": type(e).__name__
        }, "unexpected_error")
        return False
    
# Function definitions (move these to the top, after imports and before UI code)
def get_keyword_suggestions(filled_ws, selected_keywords, iteration):
    example_json = '''
    {
        "Who": ["NSCLC patients with diabetes", "early-stage patients with smoking history"],
        "What": ["standard radiotherapy", "low-dose chemotherapy"],
        "Where": ["community oncology clinics", "rural health centers"],
        "When": ["12-month follow-up", "6-month enrollment"],
        "Why": ["improve quality of life", "reduce treatment costs"]
    }
    '''
    
    prompt = f"""
    You are an oncology clinical trial design assistant with specific expertise in developing highly focused trial design synopses for the development opragmatic clinical trials. 
    The surrenct exercise is focused on developing the core elements of the synopsis as described by 5-ws as follows:
    - Who: the target patient population in real-world clinical practice (e.g., broad patient groups, specific comorbidities).
    - What: the intervention or treatment modality applicable in routine care (e.g., standard therapies, practical combinations).
    - Where: the trial locations reflecting real-world healthcare settings (e.g., community hospitals, outpatient clinics; avoid specialized academic centers unless explicitly selected).
    - When: the planned duration or timeline of the trial in a practical context (e.g., '12-month follow-up', '6-month enrollment').
    - Why: the primary objective or endpoint relevant to real-world outcomes, prioritizing patient-centered metrics (e.g., 'improve quality of life', 'reduce hospital readmissions') over research-focused goals (e.g., 'evaluate efficacy').
    This is iteration {iteration} of refining a set of clear and definitive set of 5-w for a pragmatic trial, which evaluates intervention effectiveness in real-world settings.
    Current state of all Ws: {json.dumps(filled_ws)}.
    Previously selected keywords: {json.dumps(selected_keywords)}.
    
    Provide between 3 and 5 high-impact keyword suggestions for each W field to refine the clarity and definitive nature of a synoptic summary. The suggestions must be:
    - Be highly relevant to the current state of all Ws and tailored for a pragmatic trial.
    - Build on past decisions (e.g., selected and rejected keywords) to ensure consistency and feasibility.
    - Do not repeat previously selected keywords or current W entries unless proposing a significant enhancement (e.g., adding a new clinical characteristic or outcome).
    - Include at least 2 novel suggestions per field that introduce new clinical characteristics, treatment variations, or outcomes, enhancing the trial's real-world impact.
    - Ensure 'When' reflects practical trial durations (e.g., '12-month follow-up'), not clinical events or regulatory timelines.
    - Ensure suggestions across Ws are cohesive and feasible in a pragmatic trial setting (e.g., 'What' interventions should match the 'Who' population's routine care needs and 'Where' locations' capabilities).
    Stop making suggestions for specific w's when there are no more opportunities to improve that element of the synopsis.
    Use oncology-specific rules considering population, cancer type, tumor type, and treatment modality.
    
    Return a JSON dictionary with each W as a key and a list of keyword suggestions as values. Example format:
    {example_json}
    """
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a precise, oncology-focused assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.3
        )
        suggestion_text = response.choices[0].message.content.strip()
        if suggestion_text.startswith("```json") and suggestion_text.endswith("```"):
            suggestion_text = suggestion_text[7:-3].strip()
        keywords = json.loads(suggestion_text)
        unique_key = f"keywords_{iteration}_{datetime.now().strftime('%H%M%S%f')}"
        st.session_state["app_state"]["prompt_history"].append({
            "step": f"Keyword Suggestions (Iteration {iteration})",
            "prompt": prompt,
            "response": keywords,
            "unique_key": unique_key
        })
        # Log the keyword suggestions
        log_session_data({
            "iteration": iteration,
            "filled_ws": filled_ws,
            "selected_keywords": selected_keywords,
            "suggestions": keywords
        }, "keyword_suggestions")
        return keywords
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return {}

def reassess_ws(filled_ws, selected_keywords, iteration):
    prompt = f"""
    You are an oncology clinical trial design assistant tasked with synthesizing and refining trial elements to align with the "5 rights" of clinical trials:
    1. Right Patient (Who): Ensure clear patient selection criteria, considering demographics, disease state, and eligibility factors
    2. Right Drug/Intervention (What): Specify the intervention details, including type, administration, and any combinations
    3. Right Setting (Where): Define the appropriate clinical setting that ensures feasibility and accessibility
    4. Right Time (When): Establish clear temporal framework for both the trial and intervention timing
    5. Right Documentation (Why + How): Articulate clear objectives and endpoints that can be properly documented and measured

    Current iteration: {iteration}
    Current state of all Ws: {json.dumps(filled_ws, indent=2)}
    Selected keywords for refinement: {json.dumps(selected_keywords, indent=2)}
    
    Your task:
    1. Analyze the current entries for each W, which may contain multiple statements or overlapping criteria
    2. Synthesize these into clear, cohesive statements that align with the "5 rights" framework
    3. Identify any ambiguities or potential conflicts that need clarification
    4. Ensure each W element contributes to a pragmatic trial design
    
    For each W:
    - Combine ALL overlapping or related criteria into a SINGLE coherent narrative statement
    - If there are multiple points, combine them into one flowing sentence using appropriate conjunctions
    - Convert any list-like entries into a narrative format
    - Ensure the statement reads naturally and professionally
    - Maintain all critical information while improving readability
    
    Return a JSON object with:
    {{
        "synthesis": {{
            "Who": "Single coherent statement describing the complete patient population",
            "What": "Single coherent statement describing the complete intervention",
            "Where": "Single coherent statement describing the complete setting",
            "When": "Single coherent statement describing the complete timing",
            "Why": "Single coherent statement describing the complete objective"
        }},
        "clarifications_needed": {{
            "Who": ["List of specific clarifications needed"],
            "What": ["List of specific clarifications needed"],
            "Where": ["List of specific clarifications needed"],
            "When": ["List of specific clarifications needed"],
            "Why": ["List of specific clarifications needed"]
        }},
        "assumptions_made": {{
            "Who": ["List of assumptions made in synthesis"],
            "What": ["List of assumptions made in synthesis"],
            "Where": ["List of assumptions made in synthesis"],
            "When": ["List of assumptions made in synthesis"],
            "Why": ["List of assumptions made in synthesis"]
        }}
    }}

    IMPORTANT: 
    - Each field in the synthesis MUST be a single coherent narrative statement
    - Do NOT return lists or bullet points in the synthesis
    - Convert any list-like inputs into flowing narrative text
    - Each synthesis statement should be a complete, grammatically correct sentence
    - Maintain professional medical/scientific language while ensuring readability
    """
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a precise, oncology-focused assistant with expertise in pragmatic trial design. Always synthesize information into coherent narrative statements."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.3
        )
        
        result = json.loads(response.choices[0].message.content.strip())
        
        # Validate required fields and format
        if not isinstance(result, dict):
            st.error("Invalid response format: not a dictionary")
            return filled_ws
            
        if "synthesis" not in result or not isinstance(result["synthesis"], dict):
            st.error("Missing or invalid synthesis in response")
            return filled_ws
            
        # Ensure synthesis values are strings and contain complete sentences
        for field in result["synthesis"]:
            if not isinstance(result["synthesis"][field], str):
                result["synthesis"][field] = str(result["synthesis"][field])
            # Ensure the statement ends with proper punctuation
            if not result["synthesis"][field].endswith(('.', '?', '!')):
                result["synthesis"][field] += '.'
        
        # Log the detailed analysis
        log_session_data({
            "iteration": iteration,
            "filled_ws": filled_ws,
            "selected_keywords": selected_keywords,
            "synthesis_result": result
        }, "reassess_ws_detailed")
        
        # Log to prompt history
        unique_key = f"reassess_{iteration}_{datetime.now().strftime('%H%M%S%f')}"
        st.session_state["app_state"]["prompt_history"].append({
            "step": f"Reassess Ws (Iteration {iteration})",
            "prompt": prompt,
            "response": result,
            "unique_key": unique_key
        })
        
        # Return just the synthesized values for the UI
        return result["synthesis"]
        
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return filled_ws

def generate_final_synopsis(filled_ws, iteration):
    prompt = f"""
    You are an oncology clinical trial design assistant. After {iteration} iterations, the final state of all Ws is: {json.dumps(filled_ws)}.
    Generate a concise, polished 5W synopsis for a clinical trial. Ensure the synopsis is coherent, professionally written, 
    and adheres to oncology-specific rules, considering population, cancer type, tumor type, and treatment modality. Return a single string summarizing the 5W synopsis. Example:
    "This clinical trial targets metastatic lung cancer patients (Who) to evaluate the efficacy of immunotherapy (What) at oncology centers (Where) over a 24-month period (When), aiming to extend survival (Why)."
    """
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a precise, oncology-focused assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.3
        )
        synopsis = response.choices[0].message.content.strip()
        unique_key = f"final_synopsis_{datetime.now().strftime('%H%M%S%f')}"
        st.session_state["app_state"]["prompt_history"].append({
            "step": "Final Synopsis",
            "prompt": prompt,
            "response": synopsis,
            "unique_key": unique_key
        })
        # Log the final synopsis
        log_session_data({
            "iteration": iteration,
            "filled_ws": filled_ws,
            "final_synopsis": synopsis
        }, "final_synopsis")
        return synopsis
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return "Error generating final synopsis."

def generate_initial_synopsis(filled_ws):
    prompt = f"""
    You are an oncology clinical trial design assistant tasked with creating a clear, pragmatic trial synopsis that aligns with the "5 rights" of clinical trials.
    
    Current elements:
    Who: {filled_ws.get('Who', '')}
    What: {filled_ws.get('What', '')}
    Why: {filled_ws.get('Why', '')}
    
    Framework for analysis:
    1. Right Patient (Who):
       - Clear definition of target population
       - Relevant inclusion/exclusion criteria
       - Pragmatic considerations for real-world implementation
    
    2. Right Drug/Intervention (What):
       - Clear specification of intervention
       - Practical considerations for administration
       - Integration with standard care
    
    3. Right Setting (Where):
       - Appropriate clinical setting
       - Feasibility considerations
       - Resource requirements
    
    4. Right Time (When):
       - Trial duration and timeline
       - Intervention timing
       - Follow-up considerations
    
    5. Right Documentation (Why + How):
       - Clear objectives
       - Measurable outcomes
       - Quality metrics
    
    Return a JSON object with the following structure:
    {{
        "synopsis": "A coherent statement synthesizing the current elements",
        "analysis": {{
            "understanding": {{
                "Who": "Your interpretation of the current Who elements",
                "What": "Your interpretation of the current What elements",
                "Why": "Your interpretation of the current Why elements"
            }},
            "gaps": {{
                "Who": ["Specific missing information needed"],
                "What": ["Specific missing information needed"],
                "Why": ["Specific missing information needed"]
            }}
        }},
        "suggestions_by_element": {{
            "Who": {{
                "improvements": ["Direct suggestions to enhance clarity"],
                "confirmations": ["Elements requiring user confirmation"]
            }},
            "What": {{
                "improvements": ["Direct suggestions to enhance clarity"],
                "confirmations": ["Elements requiring user confirmation"]
            }},
            "Why": {{
                "improvements": ["Direct suggestions to enhance clarity"],
                "confirmations": ["Elements requiring user confirmation"]
            }}
        }}
    }}

    IMPORTANT: Return ONLY valid JSON. Do not include any markdown formatting or additional text.
    """
    
    try:
        # Log the prompt being sent
        log_session_data({
            "prompt": prompt,
            "filled_ws": filled_ws,
            "step": "sending_prompt"
        }, "generate_initial_synopsis")
        
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a precise, oncology-focused assistant with expertise in pragmatic trial design and the '5 rights' framework. Return only valid JSON without any additional text or formatting."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.3
        )
        
        # Log the raw response
        log_session_data({
            "raw_response": response.choices[0].message.content,
            "step": "received_response"
        }, "generate_initial_synopsis")
        
        response_text = response.choices[0].message.content.strip()
        
        # Log the cleaned response text
        log_session_data({
            "cleaned_response": response_text,
            "step": "cleaned_response"
        }, "generate_initial_synopsis")
        
        # Clean up the response if it contains markdown code blocks
        if response_text.startswith("```json"):
            response_text = response_text[7:-3] if response_text.endswith("```") else response_text[7:]
        elif response_text.startswith("```"):
            response_text = response_text[3:-3] if response_text.endswith("```") else response_text[3:]
        
        # Remove any leading/trailing whitespace
        response_text = response_text.strip()
        
        # Log the final cleaned response
        log_session_data({
            "final_cleaned_response": response_text,
            "step": "final_cleaned_response"
        }, "generate_initial_synopsis")
        
        # If the response is empty, return a default structure
        if not response_text:
            st.warning("Received empty response from API. Using default structure.")
            return {
                "synopsis": "Error: Empty response received",
                "analysis": {
                    "understanding": {
                        "Who": "Unable to interpret Who elements",
                        "What": "Unable to interpret What elements",
                        "Why": "Unable to interpret Why elements"
                    },
                    "gaps": {
                        "Who": ["Unable to analyze gaps"],
                        "What": ["Unable to analyze gaps"],
                        "Why": ["Unable to analyze gaps"]
                    }
                },
                "suggestions_by_element": {
                    "Who": {"improvements": [], "confirmations": []},
                    "What": {"improvements": [], "confirmations": []},
                    "Why": {"improvements": [], "confirmations": []}
                }
            }
            
        try:
            result = json.loads(response_text)
            # Log successful JSON parsing
            log_session_data({
                "parsed_json": result,
                "step": "json_parsed_success"
            }, "generate_initial_synopsis")
        except json.JSONDecodeError as e:
            st.error(f"Failed to parse GPT response as JSON: {str(e)}")
            print("JSON Parse Error:", str(e))
            print("Attempted to parse:", response_text)
            # Log JSON parsing error
            log_session_data({
                "error": str(e),
                "attempted_parse": response_text,
                "step": "json_parse_error"
            }, "generate_initial_synopsis")
            # Return a default structure with error message
            return {
                "synopsis": "Error: Invalid JSON response",
                "analysis": {
                    "understanding": {
                        "Who": "Unable to interpret Who elements",
                        "What": "Unable to interpret What elements",
                        "Why": "Unable to interpret Why elements"
                    },
                    "gaps": {
                        "Who": ["Unable to analyze gaps"],
                        "What": ["Unable to analyze gaps"],
                        "Why": ["Unable to analyze gaps"]
                    }
                },
                "suggestions_by_element": {
                    "Who": {"improvements": [], "confirmations": []},
                    "What": {"improvements": [], "confirmations": []},
                    "Why": {"improvements": [], "confirmations": []}
                }
            }
            
        # Validate required fields
        if not all(key in result for key in ["synopsis", "analysis", "suggestions_by_element"]):
            missing_keys = [key for key in ["synopsis", "analysis", "suggestions_by_element"] if key not in result]
            st.error(f"Missing required fields in response: {missing_keys}")
            # Log missing fields error
            log_session_data({
                "missing_keys": missing_keys,
                "step": "missing_fields_error"
            }, "generate_initial_synopsis")
            # Return a default structure with missing fields
            return {
                "synopsis": "Error: Missing required fields",
                "analysis": {
                    "understanding": {
                        "Who": "Unable to interpret Who elements",
                        "What": "Unable to interpret What elements",
                        "Why": "Unable to interpret Why elements"
                    },
                    "gaps": {
                        "Who": ["Unable to analyze gaps"],
                        "What": ["Unable to analyze gaps"],
                        "Why": ["Unable to analyze gaps"]
                    }
                },
                "suggestions_by_element": {
                    "Who": {"improvements": [], "confirmations": []},
                    "What": {"improvements": [], "confirmations": []},
                    "Why": {"improvements": [], "confirmations": []}
                }
            }
            
        # Log the final result
        log_session_data({
            "final_result": result,
            "step": "final_result"
        }, "generate_initial_synopsis")
        
        return result
        
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        print("General Error:", str(e))
        # Log general error
        log_session_data({
            "error": str(e),
            "step": "general_error"
        }, "generate_initial_synopsis")
        # Return a default structure with error message
        return {
            "synopsis": "Error: Failed to generate synopsis",
            "analysis": {
                "understanding": {
                    "Who": "Unable to interpret Who elements",
                    "What": "Unable to interpret What elements",
                    "Why": "Unable to interpret Why elements"
                },
                "gaps": {
                    "Who": ["Unable to analyze gaps"],
                    "What": ["Unable to analyze gaps"],
                    "Why": ["Unable to analyze gaps"]
                }
            },
            "suggestions_by_element": {
                "Who": {"improvements": [], "confirmations": []},
                "What": {"improvements": [], "confirmations": []},
                "Why": {"improvements": [], "confirmations": []}
            }
        }

def init_session_state():
    default_state = {
        "ws": ["Who", "What", "Where", "When", "Why"],
        "core_ws": ["Who", "What", "Why"],
        "w_entries": {"Who": "", "What": "", "Where": "", "When": "", "Why": ""},
        "show_keywords": False,
        "selected_keywords": {"Who": [], "What": [], "Where": [], "When": [], "Why": []},
        "keywords": {},
        "is_first_round": True,
        "current_synopsis": "",
        "final_synopsis": "",
        "prompt_history": []
    }
    current_state = st.session_state.get("app_state", {})
    for key, value in default_state.items():
        if key not in current_state:
            current_state[key] = value
    st.session_state["app_state"] = current_state

# Initialize session ID if not exists
if "session_id" not in st.session_state:
    st.session_state["session_id"] = datetime.now().strftime("%Y%m%d_%H%M%S")

# Initialize state at the start
init_session_state()

# Load API key from environment variables or Streamlit secrets
openai_api_key = os.getenv("OPENAI_API_KEY") if not st.secrets else st.secrets["OPENAI_API_KEY"]
if not openai_api_key:
    st.error("API Key is missing! Check your environment variables or secrets.")
    st.stop()
openai.api_key = openai_api_key
st.write("API Key Loaded Successfully (Hidden in Production)")

# Examples help section
with st.expander("Examples Help", expanded=False):
    st.write("Below are examples of different ways to structure your trial elements. Each example shows a different approach to describing the Who, What, and Why elements of your trial.")
    
    # Example 1: Complete Sentences (Metastatic Breast Cancer)
    st.subheader("Example 1: Complete Sentences (Metastatic Breast Cancer)")
    st.write("**Who:**")
    st.write("The trial will target postmenopausal women with metastatic breast cancer who are hormone receptor-positive in community care settings.")
    st.write("**What:**")
    st.write("This study will evaluate the effectiveness of endocrine therapy combined with CDK4/6 inhibitors as a first-line treatment.")
    st.write("**Why:**")
    st.write("The objective is to improve progression-free survival and enhance quality of life in a real-world population.")
    
    st.markdown("---")
    
    # Example 2: Complete Sentences (Advanced Prostate Cancer)
    st.subheader("Example 2: Complete Sentences (Advanced Prostate Cancer)")
    st.write("**Who:**")
    st.write("The trial focuses on men over 70 with advanced prostate cancer and cardiovascular comorbidities in routine outpatient care.")
    st.write("**What:**")
    st.write("The intervention involves androgen deprivation therapy paired with low-dose abiraterone as a standard care option.")
    st.write("**Why:**")
    st.write("The goal is to assess the impact on overall survival while reducing treatment-related side effects in this population.")
    
    st.markdown("---")
    
    # Example 3: Keywords (Colorectal Cancer)
    st.subheader("Example 3: Keywords (Colorectal Cancer)")
    st.write("**Who:**")
    for item in ["stage III colorectal cancer patients", "patients with Lynch syndrome", "post-surgical colorectal patients"]:
        st.write(f"• {item}")
    st.write("**What:**")
    for item in ["FOLFOX chemotherapy regimen", "adjuvant immunotherapy", "oral capecitabine therapy"]:
        st.write(f"• {item}")
    st.write("**Why:**")
    for item in ["prevent cancer recurrence", "improve disease-free survival", "reduce chemotherapy toxicity"]:
        st.write(f"• {item}")
    
    st.markdown("---")
    
    # Example 4: Keywords (Pancreatic Cancer)
    st.subheader("Example 4: Keywords (Pancreatic Cancer)")
    st.write("**Who:**")
    for item in ["locally advanced pancreatic cancer patients", "patients with ECOG performance status 1", "pancreatic cancer patients aged 60+"]:
        st.write(f"• {item}")
    st.write("**What:**")
    for item in ["FOLFIRINOX chemotherapy", "stereotactic body radiotherapy", "gemcitabine-based treatment"]:
        st.write(f"• {item}")
    st.write("**Why:**")
    for item in ["extend overall survival", "enhance quality of life", "evaluate treatment tolerability"]:
        st.write(f"• {item}")
    
    st.markdown("---")
    
    # Example 5: Combination (Lung Cancer)
    st.subheader("Example 5: Combination (Lung Cancer)")
    st.write("**Who:**")
    st.write("Early-stage non-small cell lung cancer (NSCLC) patients with a history of smoking in rural community care.")
    st.write("**What:**")
    for item in ["standard lobectomy", "post-operative radiotherapy", "low-dose adjuvant chemotherapy"]:
        st.write(f"• {item}")
    st.write("**Why:**")
    st.write("The aim is to compare disease-free survival rates and assess the feasibility of treatment in rural settings.")
    
    st.markdown("---")
    
    # Example 6: Combination (Ovarian Cancer)
    st.subheader("Example 6: Combination (Ovarian Cancer)")
    st.write("**Who:**")
    for item in ["advanced ovarian cancer patients", "patients with BRCA mutations", "recurrent ovarian cancer in outpatient care"]:
        st.write(f"• {item}")
    st.write("**What:**")
    st.write("The trial will use PARP inhibitors as maintenance therapy following platinum-based chemotherapy.")
    st.write("**Why:**")
    st.write("To improve progression-free survival while minimizing hospital visits for patients.")

# Track iteration for GPT context
if "iteration" not in st.session_state:
    st.session_state["iteration"] = 1

# Create a container for the main content
main_container = st.container()

# Add reset button at the top
if st.button("Reset Session", type="primary"):
    st.session_state.clear()
    st.session_state["session_id"] = datetime.now().strftime("%Y%m%d_%H%M%S")
    init_session_state()
    st.rerun()

# Main content section
with main_container:
    st.subheader("Current Trial Synopsis")
    if st.session_state["app_state"].get("current_synopsis"):
        if isinstance(st.session_state["app_state"]["current_synopsis"], dict):
            # Display the synopsis with enhanced styling
            st.markdown(f"""<div class="current-synopsis">
                {st.session_state["app_state"]["current_synopsis"]["synopsis"]}
                </div>""", unsafe_allow_html=True)
            
            # Remove the redundant suggestions display here since they're shown in individual sections
            
            # Keep the additional notes text area
            st.text_area(
                "Additional Notes & Confirmations",
                placeholder="Enter any additional notes, confirmations, or modifications here...",
                key="additional_notes",
                height=100
            )
            
            # Log the current state
            log_session_data({
                "synopsis": st.session_state["app_state"]["current_synopsis"]["synopsis"],
                "additional_notes": st.session_state.get("additional_notes", "")
            }, "synopsis_update")
        else:
            st.markdown(f"""<div class="current-synopsis">
                {st.session_state["app_state"]["current_synopsis"]}
                </div>""", unsafe_allow_html=True)
    elif not st.session_state["app_state"]["final_synopsis"]:
        st.info("Enter the core trial elements below to generate an initial synopsis.")

    # Core elements and keyword selection
    if not st.session_state["app_state"].get("final_synopsis", ""):
        if st.session_state["app_state"].get("is_first_round", True):
            st.subheader("Enter Core Trial Elements")
            # Input fields for Who, What, Why
            for field in st.session_state["app_state"]["core_ws"]:
                input_text = st.text_area(f"Enter {field}", value=st.session_state["app_state"]["w_entries"][field], height=100)
                st.session_state["app_state"]["w_entries"][field] = input_text

            if st.button("Generate Initial Synopsis"):
                if all(st.session_state["app_state"]["w_entries"][w] for w in st.session_state["app_state"]["core_ws"]):
                    with st.spinner("Generating initial synopsis..."):
                        synopsis_data = generate_initial_synopsis(st.session_state["app_state"]["w_entries"])
                        st.session_state["app_state"]["current_synopsis"] = synopsis_data
                        st.session_state["app_state"]["is_first_round"] = False
                        # Generate initial keyword suggestions
                        keywords = get_keyword_suggestions(
                            st.session_state["app_state"]["w_entries"],
                            st.session_state["app_state"]["selected_keywords"],
                            st.session_state["iteration"]
                        )
                        if keywords:
                            st.session_state["app_state"]["keywords"] = keywords
                            st.session_state["app_state"]["show_keywords"] = True
                        # Log the initial state
                        log_session_data({
                            "w_entries": st.session_state["app_state"]["w_entries"],
                            "synopsis_data": synopsis_data,
                            "keywords": keywords
                        }, "initial_synopsis")
                        st.rerun()
                else:
                    st.error("Please fill in all core elements (Who, What, Why) before generating the synopsis.")

        # Display keyword selection for all Ws after initial synopsis
        if st.session_state["app_state"]["show_keywords"]:
            st.subheader("Refine Trial Elements")
            keywords = st.session_state["app_state"]["keywords"]
            suggestions = st.session_state["app_state"]["current_synopsis"].get("suggestions_by_element", {})
            
            for field in st.session_state["app_state"]["ws"]:
                if field in keywords:
                    with st.expander(f"Refine {field}", expanded=True):
                        # Create three columns for the layout
                        col1, col2, col3 = st.columns([2, 2, 1])
                        
                        with col1:
                            # Current value and suggestions
                            st.write("**Current value:**")
                            current_value = st.session_state["app_state"]["w_entries"].get(field, "")
                            st.markdown(current_value)
                            
                            if field in suggestions:
                                st.write("**Suggested Improvements:**")
                                if "improvements" in suggestions[field]:
                                    for imp in suggestions[field]["improvements"]:
                                        st.markdown(f"• {imp}")
                                
                                st.write("**Needs Confirmation:**")
                                if "confirmations" in suggestions[field]:
                                    for conf in suggestions[field]["confirmations"]:
                                        st.markdown(f"• {conf}")
                        
                        with col2:
                            # Keyword selection dropdown
                            st.write("**Select improvements to apply:**")
                            if field in keywords:
                                selected = st.multiselect("", keywords[field], key=f"select_{field}")
                                st.session_state["app_state"]["selected_keywords"][field] = selected
                        
                        with col3:
                            # Free-form text input
                            st.write("**Additional input:**")
                            additional_text = st.text_area(
                                "",
                                value=st.session_state.get(f"additional_{field}", ""),
                                key=f"additional_{field}",
                                placeholder=f"Add custom {field} details...",
                                height=100
                            )
                            if additional_text:
                                st.session_state[f"additional_{field}"] = additional_text

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Update Synopsis"):
                    filled_ws = st.session_state["app_state"]["w_entries"].copy()
                    # Combine selected keywords and additional text for each W
                    for field in st.session_state["app_state"]["ws"]:
                        additional_text = st.session_state.get(f"additional_{field}", "").strip()
                        selected_keywords = st.session_state["app_state"]["selected_keywords"].get(field, [])
                        
                        # Combine current value with selected keywords and additional text
                        current_value = filled_ws.get(field, "")
                        new_value = current_value
                        
                        if selected_keywords:
                            new_value += ("\n" if new_value else "") + ", ".join(selected_keywords)
                        
                        if additional_text:
                            new_value += ("\n" if new_value else "") + additional_text
                        
                        filled_ws[field] = new_value.strip()
                    
                    with st.spinner("Updating synopsis..."):
                        revised_ws = reassess_ws(
                            filled_ws,
                            st.session_state["app_state"]["selected_keywords"],
                            st.session_state["iteration"]
                        )
                    for field, value in revised_ws.items():
                        st.session_state["app_state"]["w_entries"][field] = value
                    # Update synopsis with new suggestions
                    synopsis_data = generate_initial_synopsis(st.session_state["app_state"]["w_entries"])
                    st.session_state["app_state"]["current_synopsis"] = synopsis_data
                    # Generate new keyword suggestions
                    keywords = get_keyword_suggestions(
                        st.session_state["app_state"]["w_entries"],
                        st.session_state["app_state"]["selected_keywords"],
                        st.session_state["iteration"]
                    )
                    st.session_state["app_state"]["keywords"] = keywords if keywords else {}
                    st.session_state["iteration"] += 1
                    # Log the update
                    log_session_data({
                        "w_entries": st.session_state["app_state"]["w_entries"],
                        "selected_keywords": st.session_state["app_state"]["selected_keywords"],
                        "additional_inputs": {f: st.session_state.get(f"additional_{f}", "") for f in st.session_state["app_state"]["ws"]},
                        "synopsis_data": synopsis_data,
                        "keywords": keywords
                    }, "synopsis_update")
                    st.rerun()

            with col2:
                if st.button("Finalize Synopsis"):
                    filled_ws = st.session_state["app_state"]["w_entries"].copy()
                    with st.spinner("Generating final synopsis..."):
                        final_synopsis = generate_final_synopsis(filled_ws, st.session_state["iteration"])
                    st.session_state["app_state"]["final_synopsis"] = final_synopsis
                    # Log the final state
                    log_session_data({
                        "w_entries": st.session_state["app_state"]["w_entries"],
                        "final_synopsis": final_synopsis
                    }, "final_synopsis")
                    st.rerun()

    # Display final synopsis if generated
    if st.session_state["app_state"].get("final_synopsis", ""):
        st.subheader("Final Synopsis")
        st.write(st.session_state["app_state"]["final_synopsis"])
        
        # Add download button for the log file
        log_file = os.path.join(LOGS_DIR, f"session_{st.session_state['session_id']}.log")
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                log_content = f.read()
            st.download_button(
                label="Download Session Log",
                data=log_content,
                file_name=f"session_{st.session_state['session_id']}.log",
                mime="text/plain"
            )
        
        if st.button("Start Over"):
            st.session_state.clear()
            st.session_state["session_id"] = datetime.now().strftime("%Y%m%d_%H%M%S")
            init_session_state()
            st.rerun()