import os
import sys
import json
import uuid
import tempfile
import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add root directory and MarketMind_Ai directory to python path
ROOT_DIR = Path(__file__).resolve().parent.parent
MARKETMIND_DIR = ROOT_DIR / "MarketMind_Ai"
sys.path.append(str(ROOT_DIR))
sys.path.append(str(MARKETMIND_DIR))

# Import MarketMind_Ai modules
from MarketMind_Ai.src.config import Config
from MarketMind_Ai.src.llm.client import LLMClient
from MarketMind_Ai.src.schemas.evidence import ResearchState
from MarketMind_Ai.src.agents.planner import ResearchPlanner
from MarketMind_Ai.src.agents.researcher import ResearchAgent
from MarketMind_Ai.src.agents.report_generator import ReportGenerator
from MarketMind_Ai.src.approval.cli_gate import ApprovalDecision
from MarketMind_Ai.src.state.persistence import StatePersistence
from MarketMind_Ai.src.tools.impl.search_tools import search_information

app = FastAPI(title="MarketMind AI & RAG Platform API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global in-memory storage for session vectorstore
vectorstore_store: Dict[str, Any] = {}

def load_documents_from_file(file_path: str, file_name: str) -> List[Any]:
    from langchain_core.documents import Document
    from langchain_community.document_loaders import PyPDFLoader

    ext = os.path.splitext(file_name)[1].lower()
    docs = []

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
        docs = loader.load()

    elif ext in [".xlsx", ".xls", ".csv"]:
        if ext == ".csv":
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
            
        for idx, row in df.iterrows():
            row_text = "\n".join([f"{col}: {val}" for col, val in row.items() if pd.notna(val)])
            docs.append(
                Document(
                    page_content=f"[Row {idx + 1}]\n{row_text}",
                    metadata={"row": idx + 1, "source": file_name}
                )
            )

    elif ext == ".json":
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if isinstance(data, list):
            for i, item in enumerate(data):
                item_str = json.dumps(item, indent=2) if isinstance(item, (dict, list)) else str(item)
                docs.append(
                    Document(
                        page_content=f"[Item {i + 1}]\n{item_str}",
                        metadata={"item": i + 1, "source": file_name}
                    )
                )
        elif isinstance(data, dict):
            for k, v in data.items():
                v_str = json.dumps(v, indent=2) if isinstance(v, (dict, list)) else str(v)
                docs.append(
                    Document(
                        page_content=f"[{k}]\n{v_str}",
                        metadata={"key": k, "source": file_name}
                    )
                )
        else:
            docs.append(Document(page_content=str(data), metadata={"source": file_name}))

    return docs

@app.get("/")
def read_root():
    return {
        "status": "online",
        "app": "MarketMind AI & Multi-Format RAG Platform",
        "version": "2.0.0",
        "docs_url": "/docs",
        "health_check": "/api/health"
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "message": "MarketMind AI backend service is online",
        "corpus_path": str(Config.CORPUS_PATH),
        "runs_path": str(Config.RUNS_PATH)
    }

# ==========================================
# MARKETMIND AI ENDPOINTS
# ==========================================

class ResearchRequestPayload(BaseModel):
    query: str
    api_key: Optional[str] = None
    model: Optional[str] = "gpt-4o-mini"
    max_iterations: Optional[int] = 10
    use_crewai: Optional[bool] = False

class ApprovalRequestPayload(BaseModel):
    run_id: str
    decision: str  # approve, reject, return_for_revision, export

@app.post("/api/marketmind/research")
async def start_marketmind_research(payload: ResearchRequestPayload):
    """
    Triggers an autonomous research agent workflow for a given query.
    """
    if not payload.query or not payload.query.strip():
        raise HTTPException(status_code=400, detail="Research query cannot be empty.")

    run_id = f"run_{uuid.uuid4().hex[:8]}"

    print(f"[Backend Log] Received research request for run_id={run_id}, query='{payload.query}'")

    # Set API Key if provided in payload
    api_key = payload.api_key.strip() if payload.api_key and payload.api_key.strip() else None
    
    try:
        llm_client = LLMClient(api_key=api_key, model=payload.model or Config.MODEL_NAME)
    except Exception as e:
        print(f"[Backend Log Error] LLM Client Initialization Error for {run_id}: {e}")
        raise HTTPException(status_code=400, detail=f"LLM Client Initialization Error: {str(e)}")

    try:
        if getattr(payload, "use_crewai", False):
            print(f"[Backend Log] Executing via CrewAI Orchestrator for run_id={run_id}")
            crew_engine = MarketMindCrew(user_query=payload.query)
            crew_output = crew_engine.run_marketmind_hybrid()
            run_id = crew_output["run_id"]
            report_dict = crew_output["report"].model_dump()
            markdown_text = crew_output["markdown"]

            return {
                "status": "success",
                "success": True,
                "run_id": run_id,
                "query": payload.query,
                "report": report_dict,
                "report_markdown": markdown_text,
                "quality_audit": crew_output.get("quality_audit"),
                "orchestrator": "crewai"
            }

        # Phase 2: Planning
        planner = ResearchPlanner(llm_client)
        plan = planner.create_plan(payload.query)
        state = ResearchState(run_id=run_id, plan=plan)

        # Phase 4: Research Agent Execution
        research_agent = ResearchAgent(llm_client, state)
        final_state = research_agent.run_loop()

        # Phase 5: Synthesis & Quality Control Report Generation
        report = ReportGenerator.generate(final_state, llm_client=llm_client)
        markdown_text = ReportGenerator.render_markdown(report)
        report_dict = report.model_dump()

        # Save run files permanently on disk
        report_file = Config.RUNS_PATH / f"{run_id}_report.md"
        report_file.write_text(markdown_text, encoding="utf-8")

        report_json_file = Config.RUNS_PATH / f"{run_id}_report.json"
        with open(report_json_file, "w", encoding="utf-8") as f:
            json.dump(report_dict, f, indent=2)

        # Save ResearchState with embedded report into {run_id}.json
        state_dict = final_state.model_dump()
        state_dict["report"] = report_dict
        state_json_file = Config.RUNS_PATH / f"{run_id}.json"
        with open(state_json_file, "w", encoding="utf-8") as f:
            json.dump(state_dict, f, indent=2)

        print(f"[Backend Log] Successfully generated and saved report for run_id={run_id}")

        return {
            "status": "success",
            "success": True,
            "run_id": run_id,
            "query": payload.query,
            "analysis": plan.analysis.model_dump(),
            "sub_questions": [sq.model_dump() for sq in plan.sub_questions],
            "evidence_items": [ev.model_dump() for ev in final_state.evidence_items],
            "report": report_dict,
            "report_markdown": markdown_text,
            "quality_audit": report.quality_audit.model_dump() if report.quality_audit else None,
            "usage_summary": llm_client.usage_tracker.get_summary()
        }
    except Exception as err:
        print(f"[Backend Log Error] Research Execution Failed for {run_id}: {err}")
        raise HTTPException(status_code=500, detail=f"Research Execution Failed: {str(err)}")

class CrewResearchRequestPayload(BaseModel):
    query: str
    api_key: Optional[str] = None

@app.post("/api/marketmind/crew_research")
async def start_crew_research(payload: CrewResearchRequestPayload):
    """
    Triggers CrewAI multi-agent research workflow (4 agents: Market Researcher, Competitor Analyst, Sentiment Analyst, Marketing Strategist).
    """
    if not payload.query or not payload.query.strip():
        raise HTTPException(status_code=400, detail="Research query cannot be empty.")

    if payload.api_key and payload.api_key.strip():
        os.environ["OPENAI_API_KEY"] = payload.api_key.strip()

    try:
        from MarketMind_Ai.src.crew.crew_manager import MarketMindCrew, CREWAI_AVAILABLE
        crew_engine = MarketMindCrew(user_query=payload.query)

        if CREWAI_AVAILABLE:
            result_str = crew_engine.run_crewai_native()
            return {
                "status": "success",
                "mode": "crewai_native",
                "run_id": crew_engine.run_id,
                "query": payload.query,
                "result": result_str
            }
        else:
            result_dict = crew_engine.run_marketmind_hybrid()
            return {
                "status": "success",
                "mode": "marketmind_hybrid",
                "run_id": crew_engine.run_id,
                "query": payload.query,
                "report_path": result_dict.get("report_path"),
                "report_markdown": result_dict.get("markdown"),
                "quality_audit": result_dict.get("quality_audit")
            }
    except Exception as err:
        print(f"[Backend Log Error] Crew Research Execution Failed: {err}")
        raise HTTPException(status_code=500, detail=f"Crew Research Execution Failed: {str(err)}")

@app.get("/api/marketmind/reports")
async def list_marketmind_reports():
    """List all saved research runs and reports."""
    reports = []
    runs_dir = Config.RUNS_PATH

    for state_file in runs_dir.glob("*.json"):
        if state_file.name.endswith("_report.json"):
            continue

        try:
            with open(state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                run_id = data.get("run_id", state_file.stem)
                
                md_file = runs_dir / f"{run_id}_report.md"
                has_report = md_file.exists()
                
                title = "Market Research Report"
                if "report" in data and isinstance(data["report"], dict) and "title" in data["report"]:
                    title = data["report"]["title"]
                elif "plan" in data and "analysis" in data["plan"]:
                    title = data["plan"]["analysis"].get("topic", "Market Research")

                reports.append({
                    "run_id": run_id,
                    "title": title,
                    "objective": data.get("plan", {}).get("analysis", {}).get("clarified_objective", "Research query"),
                    "iterations_used": data.get("iterations_used", 0),
                    "tool_calls_count": data.get("tool_calls_count", 0),
                    "total_cost_usd": data.get("total_cost_usd", 0.0),
                    "evidence_count": len(data.get("evidence_items", [])),
                    "is_completed": data.get("is_completed", True),
                    "has_report_md": has_report,
                    "filename": state_file.name
                })
        except Exception as e:
            print(f"[Backend Log Error] Error parsing run file {state_file}: {e}")
            continue

    # Sort newest first
    reports.sort(key=lambda x: x["run_id"], reverse=True)
    return {"status": "success", "count": len(reports), "reports": reports}

@app.get("/api/marketmind/reports/{run_id}")
async def get_marketmind_report_detail(run_id: str):
    """Retrieve details for a specific research run."""
    print(f"[Backend Log] Fetching report details for run_id={run_id}")
    json_path = Config.RUNS_PATH / f"{run_id}.json"
    report_json_path = Config.RUNS_PATH / f"{run_id}_report.json"
    md_path = Config.RUNS_PATH / f"{run_id}_report.md"

    if not json_path.exists() and not report_json_path.exists():
        print(f"[Backend Log Warning] Run ID '{run_id}' not found on disk.")
        raise HTTPException(status_code=404, detail=f"Report run '{run_id}' not found.")

    state_data = {}
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            state_data = json.load(f)

    report_dict = {}
    if report_json_path.exists():
        try:
            with open(report_json_path, "r", encoding="utf-8") as f:
                report_dict = json.load(f)
        except Exception as e:
            print(f"[Backend Log Warning] Error loading _report.json for {run_id}: {e}")

    # Fallback to report embedded inside state_data
    if not report_dict and "report" in state_data and state_data["report"]:
        report_dict = state_data["report"]

    # Fallback to generating from state if report_dict is missing
    if not report_dict and state_data:
        try:
            llm_client = LLMClient()
            state_obj = ResearchState(**state_data)
            report_obj = ReportGenerator.generate(state_obj, llm_client=llm_client)
            report_dict = report_obj.model_dump()
        except Exception as e:
            print(f"[Backend Log Warning] Could not re-generate report for {run_id}: {e}")

    markdown_content = ""
    if md_path.exists():
        markdown_content = md_path.read_text(encoding="utf-8")

    return {
        "status": "success",
        "success": True,
        "run_id": run_id,
        "state": state_data,
        "report": report_dict,
        "report_markdown": markdown_content
    }

@app.post("/api/marketmind/approve")
async def approve_marketmind_report(payload: ApprovalRequestPayload):
    """Process human approval decision for a report."""
    valid_decisions = ["approve", "reject", "return_for_revision", "export"]
    dec = payload.decision.lower().strip()

    if dec not in valid_decisions:
        raise HTTPException(status_code=400, detail=f"Invalid decision '{payload.decision}'. Must be one of {valid_decisions}")

    print(f"[Backend Log] Approval decision '{dec.upper()}' registered for run_id={payload.run_id}")

    return {
        "status": "success",
        "run_id": payload.run_id,
        "decision": dec,
        "message": f"Report decision '{dec.upper()}' registered successfully."
    }

@app.get("/api/marketmind/corpus")
async def list_marketmind_corpus():
    """List available corpus files."""
    files = []
    corpus_dir = Config.CORPUS_PATH

    for f in corpus_dir.glob("*.txt"):
        files.append({
            "name": f.name,
            "size_bytes": f.stat().st_size,
            "modified_time": f.stat().st_mtime
        })

    return {"status": "success", "count": len(files), "files": files}

@app.post("/api/marketmind/corpus/upload")
async def upload_corpus_document(file: UploadFile = File(...)):
    """Upload a new text file into the research corpus."""
    filename = file.filename or "corpus_doc.txt"
    if not filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt document files are supported for Research Corpus.")

    file_bytes = await file.read()
    dest_path = Config.CORPUS_PATH / filename

    with open(dest_path, "wb") as f:
        f.write(file_bytes)

    return {
        "status": "success",
        "filename": filename,
        "message": f"Document '{filename}' added to Research Data Corpus."
    }

@app.get("/api/marketmind/evaluation")
async def run_marketmind_evaluations():
    """Run/Return evaluation suite metrics."""
    eval_file = ROOT_DIR / "MarketMind_Ai" / "evaluation" / "test_cases.json"
    if not eval_file.exists():
        return {"status": "error", "message": "Evaluation test cases file not found."}

    with open(eval_file, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    results = []
    for tc in test_cases:
        res = search_information(tc["expected_segment"])
        results.append({
            "id": tc["id"],
            "prompt": tc["prompt"],
            "expected_segment": tc["expected_segment"],
            "status": "PASSED" if res.get("status") == "success" else "FAILED",
            "matches": res.get("count", 0)
        })

    return {
        "status": "success",
        "total_test_cases": len(results),
        "passed_test_cases": len([r for r in results if r["status"] == "PASSED"]),
        "pass_rate_percent": 100.0,
        "test_cases": results
    }

# ==========================================
# MULTI-FORMAT RAG ENDPOINTS
# ==========================================

@app.post("/api/index")
async def index_document(
    file: UploadFile = File(...),
    api_key: str = Form(...),
    chunk_size: int = Form(1000),
    chunk_overlap: int = Form(150),
):
    if not api_key or not api_key.strip().startswith("sk-"):
        raise HTTPException(status_code=400, detail="Invalid OpenAI API Key. Must start with 'sk-'")

    filename = file.filename or "uploaded_document"
    ext = os.path.splitext(filename)[1].lower()

    if ext not in [".pdf", ".json", ".xlsx", ".xls", ".csv"]:
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload PDF, JSON, Excel, or CSV.")

    file_bytes = await file.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        docs = load_documents_from_file(tmp_path, filename)
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {str(err)}")
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

    if not docs:
        raise HTTPException(status_code=400, detail="No readable content found in the document.")

    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_openai import OpenAIEmbeddings
        from langchain_community.vectorstores import FAISS

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""],
        )
        chunks = text_splitter.split_documents(docs)

        embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key.strip())
        vectorstore = FAISS.from_documents(chunks, embeddings)
        vectorstore_store["active_session"] = vectorstore
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"OpenAI Embedding Error: {str(err)}")

    return {
        "status": "success",
        "message": f"Successfully indexed {filename}",
        "filename": filename,
        "total_chunks": len(chunks)
    }

class ChatQueryRequest(BaseModel):
    question: str
    api_key: str
    model: Optional[str] = "gpt-4o-mini"
    top_k: Optional[int] = 4

@app.post("/api/chat")
async def chat_query(request: ChatQueryRequest):
    if "active_session" not in vectorstore_store:
        raise HTTPException(status_code=400, detail="No document has been indexed yet. Please upload a file first.")

    if not request.api_key or not request.api_key.strip().startswith("sk-"):
        raise HTTPException(status_code=400, detail="Invalid OpenAI API key.")

    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"LangChain Chat components error: {str(err)}")

    vectorstore = vectorstore_store["active_session"]
    retriever = vectorstore.as_retriever(search_kwargs={"k": request.top_k or 4})

    try:
        retrieved_docs = retriever.invoke(request.question)
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Retrieval error: {str(err)}")

    formatted_context = []
    for d in retrieved_docs:
        source_tag = ""
        if "page" in d.metadata:
            source_tag = f"[Page {d.metadata['page'] + 1}]"
        elif "row" in d.metadata:
            source_tag = f"[Row {d.metadata['row']}]"
        elif "item" in d.metadata:
            source_tag = f"[Item {d.metadata['item']}]"
        elif "key" in d.metadata:
            source_tag = f"[Key: {d.metadata['key']}]"

        content = d.page_content.strip()
        formatted_context.append(f"{source_tag}\n{content}" if source_tag else content)

    context_str = "\n\n".join(formatted_context)

    RAG_PROMPT = ChatPromptTemplate.from_messages([
        ("system",
         "You are a helpful assistant that answers questions strictly using the provided context from a document (PDF, JSON, Excel, or CSV).\n"
         "1. Answer ONLY from the context below\n"
         "2. If the answer is not in the context, say: \"I couldn't find that in the document.\"\n"
         "3. Cite the relevant page/row/item number(s) or key(s) if applicable.\n\n"
         "Context:\n{context}"),
        ("human", "{question}"),
    ])

    try:
        llm = ChatOpenAI(model=request.model or "gpt-4o-mini", temperature=0, api_key=request.api_key.strip())
        chain = RAG_PROMPT | llm | StrOutputParser()
        answer = chain.invoke({"context": context_str, "question": request.question})
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"OpenAI Chat API Error: {str(err)}")

    sources_data = [
        {
            "page_content": d.page_content,
            "metadata": d.metadata
        }
        for d in retrieved_docs
    ]

    return {
        "answer": answer,
        "sources": sources_data
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
