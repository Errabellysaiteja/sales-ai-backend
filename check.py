packages = [
    "fastapi",
    "uvicorn",
    "multipart",
    "boto3",
    "langchain",
    "langchain_google_genai",
    "langchain_community",
    "faiss",
    "dotenv",
    "requests"
]

for package in packages:
    try:
        __import__(package)
        print(f"{package} ✅ Installed")
    except ImportError:
        print(f"{package} ❌ Not Installed")
