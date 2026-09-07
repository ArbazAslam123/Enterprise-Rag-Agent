import streamlit as st
import re
from pydantic import SecretStr
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Import our modular backend
from src.config import config
from src.ingest import DocumentIngestionPipeline
from src.retriever import EnterpriseRetriever

# 1. Page Configuration
st.set_page_config(
    page_title="Enterprise Policy AI", 
    page_icon="🏢", 
    layout="centered"
)

# 2. Caching the Backend
@st.cache_resource(show_spinner="Initializing Enterprise Backend...")
def initialize_backend():
    """Loads the database and search engine only once and keeps it in RAM."""
    pipeline = DocumentIngestionPipeline()
    vs, chunks = pipeline.run("data/enterprise_policy.txt")
    return EnterpriseRetriever(vs, chunks)

# Initialize our custom search engine
retriever_engine = initialize_backend()

# 3. Setup the LLM
llm = ChatGroq(
    temperature=0, 
    model=config.llm_model,
    api_key=SecretStr(config.groq_api_key),
    max_tokens=700 
)

# 4. Strict Guardrail Prompt (Added an instruction to keep thinking concise)
system_prompt = """
You are a strict, highly accurate enterprise compliance assistant.
Use ONLY the following retrieved context to answer the user's question.
If the answer is not contained in the context, explicitly state: "I do not have enough information in the corporate policy to answer this."

IMPORTANT: Keep your internal reasoning (<think> tags) brief and concise to save tokens for the final answer.

CONTEXT:
{context}

USER QUESTION: 
{question}
"""
prompt_template = ChatPromptTemplate.from_template(system_prompt)

# 5. Build the UI
st.title("🏢 Enterprise Policy Agent")
st.markdown("Ask questions about IT security, remote work stipends, or hardware compliance.")

# Create a text box for the user to type their question
user_question = st.text_input("Enter your question here:")

if user_question:
    with st.spinner("Searching corporate knowledge base..."):
        
        # Step A: Retrieve the best chunks
        retrieved_docs = retriever_engine.search(user_question)
        
        # Step B: Combine the text from the chunks
        context_text = "\n\n".join([doc.page_content for doc in retrieved_docs])
        
        if not context_text.strip():
            st.error("No relevant policy documents found.")
        else:
            # Step C: Send the context and the question to Groq
            generation_chain = prompt_template | llm | StrOutputParser()
            
            raw_answer = generation_chain.invoke({
                "context": context_text,
                "question": user_question
            })
            
            # --- NEW FORGIVING PARSING LOGIC ---
            
            # This Regex looks for <think> and grabs everything until it hits </think> OR the end of the string
            think_match = re.search(r"<think>(.*?)(?:</think>|$)", raw_answer, flags=re.DOTALL)
            
            if think_match:
                # Extract just the thought process
                thinking_process = think_match.group(1).strip()
                
                # Remove the entire think block from the raw answer to isolate the final answer
                clean_answer = re.sub(r"<think>.*?(?:</think>|$)\n*", "", raw_answer, flags=re.DOTALL).strip()
                
                # If the AI used ALL its tokens on thinking and didn't write an answer
                if not clean_answer:
                    clean_answer = "⚠️ Generation Error: The AI used all available tokens to analyze the document and didn't have enough room left to write the final answer. Please ask a simpler question."
            else:
                thinking_process = "No internal reasoning block generated."
                clean_answer = raw_answer.strip()
            
            # --- DISPLAY LOGIC ---
            
            # 1. Thinking Process (Hidden in an expander)
            with st.expander("🧠 View AI Reasoning Process"):
                st.info(thinking_process)
            
            # 2. Final Answer (In a dynamic, resizable box)
            st.success("**Final Answer:**")
            
            # st.text_area creates a box that users can drag to resize in the bottom right corner
            st.text_area(
                label="Answer Box", 
                value=clean_answer, 
                height=200, 
                label_visibility="collapsed"
            )
            
            # 3. Raw Sources
            with st.expander("🔍 View Retrieved Sources"):
                for idx, doc in enumerate(retrieved_docs):
                    st.markdown(f"**Source {idx + 1}** (Chunk ID: `{doc.metadata.get('chunk_id', 'N/A')}`)")
                    st.info(doc.page_content)