from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schema import Request
from agent.graphs import ConsultantGraph


app = FastAPI(title='Proxima')

agent = ConsultantGraph()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin","Authorization"],
)


@app.post("/api/v1/get_answer/")
async def generate_text(request: Request):
    prompt = " ".join([msg.content for msg in request.history if msg.role == "user"])
    answer = agent.invoke(prompt).content
    agent.clear_history()
    return answer
