from fastapi import FastAPI
from schema import  RequsetHistory
from fastapi.middleware.cors import CORSMiddleware
from agent.graphs import ConsultantGraph

app = FastAPI(title='Proxima')

origins = ["http://0.0.0.0:80","http://localhost:4200"]
agent = ConsultantGraph()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin","Authorization"],
)


@app.post("/api/v1/agent/get_answer")
async def generate_text(request: RequsetHistory):
    prompt = " ".join([msg.content for msg in request.history if msg.role == "user"])
    answer = agent.invoke(prompt).content
    agent.clear_history()
    return {"answer": answer}