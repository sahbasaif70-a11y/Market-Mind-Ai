import json
import uuid
from pathlib import Path
from typing import Dict, Any, Optional

try:
    from crewai import Agent, Task, Crew, Process
    from crewai.tools import tool
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    Agent = Task = Crew = Process = tool = None

from src.config import Config
from src.llm.client import LLMClient
from src.schemas.evidence import ResearchState
from src.agents.planner import ResearchPlanner
from src.agents.researcher import ResearchAgent
from src.agents.report_generator import ReportGenerator
from src.tools.dispatcher import ToolDispatcher
from src.tools.impl.search_tools import web_search, fetch_webpage
from src.state.persistence import StatePersistence


if CREWAI_AVAILABLE:
    @tool("Web Search Tool")
    def web_search_tool(query: str) -> str:
        """Search live web sources using DuckDuckGo or Serper for latest trends, news, and competitor data."""
        res = web_search(query)
        return json.dumps(res, indent=2)

    @tool("Web Scraper Tool")
    def fetch_webpage_tool(url: str) -> str:
        """Fetch and scrape text content from a specific webpage or competitor website URL."""
        res = fetch_webpage(url)
        return json.dumps(res, indent=2)

    @tool("Search Market Intelligence Data")
    def search_market_intelligence(query: str, target_entity: str = "", criterion: str = "") -> str:
        """Search online web sources and local corpus for market entity data, pricing, features, and CAGR forecasts."""
        dispatcher = ToolDispatcher()
        result = dispatcher.execute(
            "search_information",
            json.dumps({"query": query, "target_entity": target_entity, "criterion": criterion})
        )
        return json.dumps(result, indent=2)

    @tool("Calculate CAGR & Growth Rates")
    def calculate_cagr(start_val: float, end_val: float, start_year: int, end_year: int) -> str:
        """Calculates Compound Annual Growth Rate (CAGR %) and Total Growth Rate (%) deterministically."""
        years = end_year - start_year
        if years <= 0 or start_val <= 0:
            return json.dumps({"error": "Invalid input parameters for CAGR calculation"})

        cagr = ((end_val / start_val) ** (1 / years) - 1) * 100
        total_growth = ((end_val - start_val) / start_val) * 100

        return json.dumps({
            "start_year": start_year,
            "end_year": end_year,
            "years": years,
            "start_val": round(start_val, 2),
            "end_val": round(end_val, 2),
            "cagr_percent": round(cagr, 2),
            "total_growth_percent": round(total_growth, 2)
        })


class MarketMindCrew:
    """CrewAI Integration Engine for MarketMind AI multi-agent workflows."""

    def __init__(self, user_query: str):
        self.user_query = user_query
        self.run_id = f"crew_run_{uuid.uuid4().hex[:8]}"

    def build_crew(self) -> Any:
        """Constructs and returns the configured CrewAI instance with agents and tasks."""
        if not CREWAI_AVAILABLE:
            raise ImportError("crewai library is not installed. Please install it using 'pip install crewai'.")

        # Agent 1: Market Research Specialist
        market_researcher = Agent(
            role="Lead Market Researcher",
            goal=f"Analyze product niche for '{self.user_query}', extract latest market trends, industry size (TAM/SAM/SOM), and identify target audience segments.",
            backstory="Expert Market Intelligence Director specializing in global industry market analysis, demographic research, and emerging trends detection.",
            tools=[web_search_tool, search_market_intelligence],
            verbose=True,
            allow_delegation=False
        )

        # Agent 2: Competitor Intelligence Analyst
        competitor_analyst = Agent(
            role="Competitor Analyst",
            goal=f"Identify top 3-5 direct and indirect competitors for '{self.user_query}', analyzing their strengths, weaknesses, pricing strategy, and USPs.",
            backstory="Competitive Intelligence Strategist skilled in benchmarking SaaS & product companies, pricing breakdowns, and market gap analysis.",
            tools=[web_search_tool, fetch_webpage_tool, search_market_intelligence],
            verbose=True,
            allow_delegation=False
        )

        # Agent 3: Customer Pain Points & Sentiment Analyst
        sentiment_analyst = Agent(
            role="Consumer Insights Strategist",
            goal=f"Analyze customer reviews, social discussions, and feedback regarding '{self.user_query}' to uncover public sentiment, main pain points, complaints, and unfulfilled gaps.",
            backstory="Customer Experience Specialist proficient in analyzing user reviews, forum discussions, social sentiment, and user dissatisfaction drivers.",
            tools=[web_search_tool, search_market_intelligence],
            verbose=True,
            allow_delegation=False
        )

        # Agent 4: Chief Marketing Strategist (The Synthesizer)
        marketing_strategist = Agent(
            role="Head of Marketing & Strategy",
            goal=f"Synthesize findings from all agents into a complete Go-To-Market (GTM) Strategy, pricing recommendations, and Marketing Ad Copy / Content Plan for '{self.user_query}'.",
            backstory="CMO & Growth Strategist famous for launching multi-million dollar products with high-converting marketing campaigns and razor-sharp positioning.",
            tools=[calculate_cagr],
            verbose=True,
            allow_delegation=False
        )

        # Tasks Definition
        task1_market_research = Task(
            description=f"Conduct thorough market research for '{self.user_query}'. Identify current industry trends, estimated market size/growth metrics, and target audience segments.",
            expected_output="Detailed Market Research report covering industry size, growth trends, and target customer demographics.",
            agent=market_researcher
        )

        task2_competitor_analysis = Task(
            description=f"Identify and analyze top 3-5 competitors for '{self.user_query}'. Uncover their key strengths, weaknesses, pricing plans, and Unique Selling Propositions (USPs).",
            expected_output="Comprehensive Competitor Matrix with pricing models, strengths, weaknesses, and USPs.",
            agent=competitor_analyst
        )

        task3_sentiment_analysis = Task(
            description=f"Investigate customer sentiment, forum discussions, and product reviews for '{self.user_query}'. Identify top complaints, friction points, and feature gaps.",
            expected_output="Consumer Sentiment breakdown highlighting major customer pain points, complaints, and unmet market needs.",
            agent=sentiment_analyst
        )

        task4_gtm_strategy = Task(
            description=f"Synthesize the outputs of previous tasks into an executive Go-To-Market (GTM) strategy for '{self.user_query}'. Provide pricing recommendations, positioning strategy, and sample Marketing Ad Copies / Content Plan.",
            expected_output="Executive GTM Report with positioning strategy, pricing recommendation, marketing ad copies, and content plan formatted in clean Markdown.",
            agent=marketing_strategist
        )

        # Assemble Sequential Crew
        crew = Crew(
            agents=[market_researcher, competitor_analyst, sentiment_analyst, marketing_strategist],
            tasks=[task1_market_research, task2_competitor_analysis, task3_sentiment_analysis, task4_gtm_strategy],
            process=Process.sequential,
            verbose=True
        )

        return crew

    def run_crewai_native(self) -> str:
        """Executes the workflow via CrewAI process kickoff."""
        crew = self.build_crew()
        result = crew.kickoff(inputs={"user_query": self.user_query})
        return str(result)

    def run_marketmind_hybrid(self) -> Dict[str, Any]:
        """Hybrid Execution: Runs MarketMind AI core state engines orchestrated under CrewAI agent rules."""
        llm_client = LLMClient()
        
        # Phase 1: Planning
        planner = ResearchPlanner(llm_client)
        plan = planner.create_plan(self.user_query)
        state = ResearchState(run_id=self.run_id, plan=plan)

        # Phase 2: Research Execution Loop
        research_agent = ResearchAgent(llm_client, state)
        final_state = research_agent.run_loop()

        # Phase 3: Synthesis & Audit
        report = ReportGenerator.generate(final_state, llm_client=llm_client)

        # Phase 4: Save Outputs
        report_path = Config.RUNS_PATH / f"{self.run_id}_crew_report.md"
        markdown_text = ReportGenerator.render_markdown(report)
        report_path.write_text(markdown_text, encoding="utf-8")
        StatePersistence.save_state(final_state)

        return {
            "run_id": self.run_id,
            "report_path": str(report_path),
            "report": report,
            "markdown": markdown_text,
            "quality_audit": report.quality_audit.dict() if report.quality_audit else {}
        }
