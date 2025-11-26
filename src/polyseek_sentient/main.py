"""Entry point for the Polyseek Sentient agent."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import uuid
from dataclasses import dataclass
from typing import Optional, List

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import TYPE_CHECKING
import logging
import ulid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .analysis_agent import AnalysisRequest
    from .fetch_market import MarketData
    from .scrape_context import MarketContext
    from .signals_client import SignalRecord


try:  # pragma: no cover - optional dependency
    # Try standard import
    from sentient_agent_framework import AbstractAgent, Query, ResponseHandler, Session
except ImportError:
    try:
        # Try importing from src if standard import fails
        from src.sentient_agent_framework import AbstractAgent, Query, ResponseHandler, Session
    except ImportError:  # pragma: no cover
        # Fallback dummy classes
        class AbstractAgent:  # type: ignore
            def __init__(self, name: str = ""):
                self.name = name

            async def assist(self, session, query, response_handler):
                raise RuntimeError("Sentient Agent Framework not installed")

        class Session:  # type: ignore
            ...

        class Query:  # type: ignore
            def __init__(self, prompt: str):
                self.prompt = prompt

        class ResponseHandler:  # type: ignore
            async def emit_text_block(self, event_name: str, content: str):
                print(f"[{event_name}] {content}")

            async def emit_json(self, event_name: str, data: dict):
                print(f"[{event_name}] {json.dumps(data, indent=2, ensure_ascii=False)}")

            def create_text_stream(self, event_name: str):
                return self

            async def emit_chunk(self, chunk: str):
                print(chunk)

            async def complete(self):
                print("[COMPLETE]")


class CLIResponseHandler:
    """Simple handler for local CLI runs without Sentient stack."""

    async def emit_text_block(self, event_name: str, content: str):
        print(f"[{event_name}] {content}")

    async def emit_json(self, event_name: str, data: dict):
        print(f"[{event_name}] {json.dumps(data, indent=2, ensure_ascii=False)}")

    def create_text_stream(self, event_name: str):
        return _CLIStream(event_name)

    async def complete(self):
        print("[COMPLETE]")


class _CLIStream:
    def __init__(self, name: str):
        self.name = name

    async def emit_chunk(self, chunk: str):
        print(f"[{self.name}] {chunk}")

    async def complete(self):
        print(f"[{self.name}] (end)")


from .analysis_agent import AnalysisRequest, run_analysis
from .config import Settings, load_settings
from .fetch_market import MarketData, fetch_market_data
from .report_formatter import format_response
from .scrape_context import fetch_market_context
from .signals_client import gather_signals


@dataclass
class AgentInput:
    market_url: str
    depth: str = "quick"
    perspective: str = "neutral"


class PolyseekSentientAgent(AbstractAgent):
    """Sentient-compatible agent implementation."""

    def __init__(self, settings: Optional[Settings] = None):
        super().__init__(name="Polyseek Sentient Agent")
        self.settings = settings or load_settings()

    async def assist(self, session, query, response_handler):
        # Lazy import to prevent startup crashes
        from .analysis_agent import AnalysisRequest, run_analysis
        from .fetch_market import fetch_market_data
        from .scrape_context import fetch_market_context
        from .signals_client import fetch_signals

        payload = _parse_prompt(query.prompt)
        await response_handler.emit_text_block("RECEIVED", f"Analyzing {payload.market_url}")

        market = await fetch_market_data(payload.market_url, self.settings)
        await response_handler.emit_json(
            "MARKET_METADATA",
            {
                "title": market.title,
                "deadline": str(market.deadline),
                "prices": {"yes": market.prices.yes, "no": market.prices.no},
            },
        )

        context = await fetch_market_context(payload.market_url, self.settings)
        signals = await gather_signals(market, self.settings)
        
        if payload.depth == "deep":
            await response_handler.emit_text_block("DEEP_MODE", "Starting deep analysis (Planner → Critic → Follow-up → Final)")

        analysis_payload = await run_analysis(
            AnalysisRequest(
                market=market,
                context=context,
                signals=signals,
                depth=payload.depth,
                perspective=payload.perspective,
            ),
            self.settings,
        )

        model, markdown = format_response(analysis_payload)
        await response_handler.emit_json("ANALYSIS_JSON", model.model_dump())
        stream = response_handler.create_text_stream("ANALYSIS_MARKDOWN")
        await stream.emit_chunk(markdown)
        await stream.complete()
        await response_handler.complete()


def _parse_prompt(prompt: str) -> AgentInput:
    try:
        data = json.loads(prompt)
        return AgentInput(
            market_url=data["market_url"],
            depth=data.get("depth", "quick"),
            perspective=data.get("perspective", "neutral"),
        )
    except (json.JSONDecodeError, KeyError):
        return AgentInput(market_url=prompt.strip())


async def _run_cli(url: str, depth: str, perspective: str):
    agent = PolyseekSentientAgent()
    handler = CLIResponseHandler()
    payload = json.dumps({"market_url": url, "depth": depth, "perspective": perspective})

    class _SimpleQuery:
        def __init__(self, prompt: str):
            self.prompt = prompt

    class _SimpleSession:
        id = "cli-session"

    query = _SimpleQuery(prompt=payload)
    await agent.assist(_SimpleSession(), query, handler)


def main():
    parser = argparse.ArgumentParser(description="Polyseek Sentient agent demo CLI")
    parser.add_argument("market_url")
    parser.add_argument("--depth", default="quick", choices=("quick", "deep"))
    parser.add_argument("--perspective", default="neutral", choices=("neutral", "devils_advocate"))
    args = parser.parse_args()
    asyncio.run(_run_cli(args.market_url, args.depth, args.perspective))


# ==========================================
# FastAPI Application
# ==========================================

app = FastAPI(title="Polyseek Sentient API")

import os

# CORS configuration: Get from environment variable in production, allow all in development
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    market_url: str
    depth: str = "quick"
    perspective: str = "neutral"


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


@app.get("/api/trending")
async def get_trending():
    """Return mock trending markets for the frontend."""
    return [
        {
            "id": 1,
            "title": "Will Bitcoin hit $100k in 2024?",
            "price": "0.65",
            "volume": "$12M",
            "url": "https://polymarket.com/event/will-bitcoin-hit-100k-in-2024",
        },
        {
            "id": 2,
            "title": "Russia x Ukraine Ceasefire in 2025?",
            "price": "0.15",
            "volume": "$5M",
            "url": "https://polymarket.com/event/russia-x-ukraine-ceasefire-in-2025",
        },
        {
            "id": 3,
            "title": "Will AI surpass human performance in coding by 2026?",
            "price": "0.42",
            "volume": "$1.8M",
            "url": "https://polymarket.com/event/ai-coding-2026",
        },
    ]


@app.post("/api/analyze")
async def analyze_market(request: AnalyzeRequest):
    try:
        settings = load_settings()
        
        # Check for common configuration issues
        if not settings.llm.api_key:
            raise HTTPException(
                status_code=500,
                detail="LLM API key not configured. Please set POLYSEEK_LLM_API_KEY, OPENROUTER_API_KEY, or OPENAI_API_KEY environment variable."
            )
        
        # 1. Fetch Market Data
        try:
            market = await fetch_market_data(request.market_url, settings)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch market data: {str(e)}"
            )
        
        # 2. Fetch Context
        try:
            context = await fetch_market_context(request.market_url, settings)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch market context: {str(e)}"
            )
        
        # 3. Gather Signals
        try:
            signals = await gather_signals(market, settings)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to gather signals: {str(e)}"
            )
        
        # 4. Run Analysis
        try:
            analysis_payload = await run_analysis(
                AnalysisRequest(
                    market=market,
                    context=context,
                    signals=signals,
                    depth=request.depth,
                    perspective=request.perspective,
                ),
                settings,
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Analysis failed: {str(e)}"
            )
        
        # 5. Format Response
        try:
            model, markdown = format_response(analysis_payload)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to format response: {str(e)}"
            )
        
        # Construct response matching frontend expectation
        return {
            "markdown": markdown,
            "json": model.model_dump()
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        error_message = str(e)
        print(f"Unexpected error in /api/analyze: {error_message}")
        print(f"Traceback: {error_trace}")
        # Log to stderr for Vercel logs
        import sys
        print(f"Error: {error_message}", file=sys.stderr)
        print(f"Traceback: {error_trace}", file=sys.stderr)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {error_message}"
        )





# SSE Response Handler
# ==========================================

class SSEResponseHandler(ResponseHandler):
    def __init__(self, queue: asyncio.Queue):
        self.queue = queue

    async def emit_text_block(self, event_name: str, content: str):
        data = json.dumps({"type": event_name, "content": content})
        await self.queue.put(f"event: message\ndata: {data}\n\n")

    async def emit_json(self, event_name: str, data: dict):
        payload = json.dumps({"type": event_name, "data": data})
        await self.queue.put(f"event: message\ndata: {payload}\n\n")

    def create_text_stream(self, event_name: str):
        return SSEStream(event_name, self.queue)

    async def emit_chunk(self, chunk: str):
        # Fallback for direct chunk emission if needed
        pass

    async def complete(self):
        await self.queue.put(None)  # Signal end of stream


class SSEStream:
    def __init__(self, name: str, queue: asyncio.Queue):
        self.name = name
        self.queue = queue

    async def emit_chunk(self, chunk: str):
        data = json.dumps({"type": self.name, "chunk": chunk})
        await self.queue.put(f"event: message\ndata: {data}\n\n")

    async def complete(self):
        # Stream completion is handled by the parent handler's complete
        pass


class AssistRequest(BaseModel):
    prompt: str
    stream: bool = True


@app.post("/assist")
async def assist_endpoint(request: AssistRequest):
    """
    MCP-compatible assist endpoint that streams responses via SSE.
    """
    settings = load_settings()
    agent = PolyseekSentientAgent(settings)
    
    # Create a queue to bridge the agent's callbacks to the SSE stream
    queue = asyncio.Queue()
    handler = SSEResponseHandler(queue)
    
    # Create session and query objects
    class SimpleSession:
        def __init__(self):
            self.id = str(ulid.ULID())

    session = SimpleSession()
    
    # Query seems to be a Pydantic model requiring 'id'.
    # We need to handle the case where Query might be the fallback class or the real one
    # The fallback class in this file takes 'prompt' in __init__
    # The real Query class likely takes 'prompt' and 'id'
    
    try:
        # Try to instantiate with id first (for real framework)
        query = Query(id=str(ulid.ULID()), prompt=request.prompt)
    except TypeError:
        # Fallback for dummy class or if signature differs
        query = Query(prompt=request.prompt)
        if hasattr(query, 'id'):
            query.id = str(ulid.ULID())
    
    async def event_generator():
        # Start the agent in a background task
        task = asyncio.create_task(agent.assist(session, query, handler))
        
        try:
            while True:
                # Wait for the next event from the queue
                data = await queue.get()
                
                if data is None:
                    break
                    
                yield data
                
        except asyncio.CancelledError:
            logger.info("Client disconnected")
            task.cancel()
            raise
        except Exception as e:
            logger.error(f"Error in event generator: {e}")
            yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"
        finally:
            # Ensure the agent task is finished
            try:
                await task
            except Exception as e:
                logger.error(f"Agent task error: {e}")

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )


@app.get("/assist")
async def assist_check():
    """
    GET endpoint for SSE connection verification.
    """
    async def event_generator():
        yield "event: connected\ndata: {}\n\n"
        try:
            while True:
                await asyncio.sleep(15)
                yield "event: ping\ndata: {}\n\n"
        except asyncio.CancelledError:
            pass

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )

if __name__ == "__main__":
    main()

