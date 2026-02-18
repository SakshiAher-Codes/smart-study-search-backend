from fastapi import FastAPI, UploadFile, File
from sentence_transformers import SentenceTransformer
import faiss
import os
import PyPDF2

app = FastAPI(title="Smart Study Search API")

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

DIM = 384
index = faiss.IndexFlatL2(DIM)

documents = []

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def extract_text_pdf(path):
    text = ""

    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)

        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()

    return text


@app.get("/")
def home():
    return {"status": "Backend Running"}


@app.post("/upload/")
async def upload(file: UploadFile = File(...)):

    path = os.path.join(UPLOAD_DIR, file.filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    if file.filename.endswith(".pdf"):
        text = extract_text_pdf(path)
    else:
        text = file.filename

    vector = model.encode([text])

    index.add(vector)

    documents.append({
        "name": file.filename,
        "content": text[:500]
    })

    return {"message": "Uploaded", "file": file.filename}


@app.get("/search/")
def search(query: str):

    vector = model.encode([query])

    k = 3
    distances, ids = index.search(vector, k)

    results = []

    for i in ids[0]:
        if i < len(documents):
            results.append(documents[i])

    return {
        "query": query,
        "results": results
    }
