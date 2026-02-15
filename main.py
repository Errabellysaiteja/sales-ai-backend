import os
import time
import boto3
import json
import requests
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# LangChain & AI Imports
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.messages import HumanMessage, SystemMessage

# 1. Load environment variables (Your keys)
load_dotenv()

# 2. Initialize the App
app = FastAPI()

# 3. Allow the frontend to talk to this backend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("✅ Setup Complete: Libraries loaded.")

# 4. AWS Clients (Connects to your AWS account)
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

transcribe_client = boto3.client(
    'transcribe',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

# 5. Initialize Gemini AI (The Brain)
# We use a low temperature (0.3) so the AI is factual and consistent.
# Initialize Mistral AI
llm = ChatMistralAI(
    model="mistral-large-latest", # Mistral's flagship model
    temperature=0.3, 
    mistral_api_key=os.getenv('MISTRAL_API_KEY')
)

embeddings = MistralAIEmbeddings(
    model="mistral-embed", # Mistral's embedding model
    mistral_api_key=os.getenv('MISTRAL_API_KEY')
)

print("✅ AWS and Google AI Clients initialized.")

# 6. Create the Knowledge Base (RAG)
sales_knowledge_base = """
Effective Sales Techniques & Knowledge Base:
1. Objection Handling: If a customer says "It's too expensive", do not drop the price immediately. Instead, ask "expensive compared to what?" or highlight the ROI.
2. Empathy: Always validate the customer's feelings. Say "I understand why that is a concern."
3. Closing: Use the 'Assumptive Close' like "When would you like to start implementation?"
4. Discovery: Ask open-ended questions. "What is your biggest pain point right now?"
5. Competitors: If they mention a competitor, focus on our unique strengths, do not bash the competition.
"""

# Split text into chunks
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
texts = text_splitter.split_text(sales_knowledge_base)

# Create the vector store (The Search Engine)
print("...Building Vector Store (this may take a moment)...")
vectorstore = FAISS.from_texts(texts, embeddings)
retriever = vectorstore.as_retriever()
print("✅ Knowledge Base built.")


# 7. Helper Function to Transcribe Audio
def transcribe_audio(job_name, file_uri):
    print(f"Starting transcription job: {job_name}")
    
    # Start the job
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': file_uri},
        MediaFormat='mp3', 
        LanguageCode='en-US'
    )

    # Loop and wait for it to finish (Polling)
    while True:
        status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = status['TranscriptionJob']['TranscriptionJobStatus']
        
        if job_status in ['COMPLETED', 'FAILED']:
            break
        print("Waiting for transcription...")
        time.sleep(5) # Check every 5 seconds

    if job_status == 'COMPLETED':
        transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        # Fetch the actual text from the URL AWS gives us
        response = requests.get(transcript_uri)
        data = response.json()
        return data['results']['transcripts'][0]['transcript']
    else:
        raise Exception("Transcription Job Failed")
    
# 8. Define the AI Agents

# Agent 1: The Analyzer (Summarizes)
def agent_analyzer(transcript):
    prompt = f"""
    You are an expert Sales Analyzer. Summarize this sales call. 
    Identify the customer's name (if mentioned) and their core problem.
    Transcript: {transcript}
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content

# Agent 2: The Objection Expert (Uses RAG)
def agent_objection_expert(transcript):
    # Search the knowledge base for "objection handling"
    docs = retriever.invoke("objection handling")
    knowledge = "\n".join([d.page_content for d in docs])
    
    prompt = f"""
    You are an Objection Handling Expert. 
    Reference this internal training material:
    {knowledge}
    
    Now review the transcript below. Did the sales rep handle objections according to our training material?
    Transcript: {transcript}
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content

# Agent 3: The Sales Coach (The Boss)
def agent_sales_coach(transcript, analysis, objection_notes):
    prompt = f"""
    You are a Senior Sales Manager. Write a final feedback report for the sales rep.
    
    Use the Analysis: {analysis}
    Use the Objection Report: {objection_notes}
    
    Format the output as valid JSON with these fields:
    - score (1-100)
    - summary
    - strengths (list)
    - weaknesses (list)
    - next_steps
    """
    # Note: We ask for JSON, but in a basic app, we might get text. 
    # For simplicity, we will treat it as text.
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content

# 9. Main API Endpoint
@app.post("/analyze")
async def analyze_call(file: UploadFile = File(...)):
    print(f"--- STARTING ANALYSIS FOR {file.filename} ---")
    bucket_name = os.getenv('S3_BUCKET_NAME')
    file_key = f"uploads/{int(time.time())}_{file.filename}"
    job_name = f"job_{int(time.time())}"

    # 1. Upload
    print("Step 1: Uploading to S3...")
    try:
        s3_client.upload_fileobj(file.file, bucket_name, file_key)
        file_uri = f"s3://{bucket_name}/{file_key}"
        print("✅ Upload Successful")
    except Exception as e:
        print(f"❌ Upload Failed: {e}")
        return {"error": f"S3 Upload failed: {str(e)}"}

    # 2. Transcribe
    print("Step 2: Starting Transcription...")
    try:
        transcript_text = transcribe_audio(job_name, file_uri)
        print(f"✅ Transcription Complete (Length: {len(transcript_text)} characters)")
        print(f"TRANSCRIPT PREVIEW: {transcript_text[:100]}...") # Print first 100 chars
    except Exception as e:
        print(f"❌ Transcription Failed: {e}")
        return {"error": f"Transcription failed: {str(e)}"}

    # 3. AI Agents
    print("Step 3: Running AI Agents...")
    
    try:
        print("   - Agent 1 (Analyzer) running...")
        analysis = agent_analyzer(transcript_text)
        print(f"   ✅ Analysis Result: {analysis[:50]}...") # Print preview
        time.sleep(1)

        print("   - Agent 2 (Objection Expert) running...")
        objections = agent_objection_expert(transcript_text)
        print(f"   ✅ Objections Result: {objections[:50]}...") # Print preview
        time.sleep(1)

        print("   - Agent 3 (Sales Coach) running...")
        final_report = agent_sales_coach(transcript_text, analysis, objections)
        print(f"   ✅ Final Report Result: {final_report[:50]}...") # Print preview

    except Exception as e:
        print(f"❌ AI AGENT FAILED: {e}")
        import traceback
        traceback.print_exc()
        return {"error": f"AI Generation failed: {str(e)}"}

    # 4. Return Data
    result_payload = {
        "transcript": transcript_text,
        "analysis": analysis,
        "objections": objections,
        "final_report": final_report
    }
    
    print("Step 4: Sending response to browser...")
    return result_payload
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)