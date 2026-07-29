"""
WeatherWise AI - Main Application Entry Point
Supports running the FastAPI Web Dashboard, standalone Fetch.ai uAgent Node, or test suite.
"""

import sys
import os
import argparse
import logging

# Auto-add local venv site-packages to sys.path if venv directory exists
_workspace_dir = os.path.dirname(os.path.abspath(__file__))
_venv_site_pkgs = os.path.join(_workspace_dir, "venv", "Lib", "site-packages")
if os.path.exists(_venv_site_pkgs) and _venv_site_pkgs not in sys.path:
    sys.path.insert(0, _venv_site_pkgs)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("WeatherWise.Main")


def main():
    parser = argparse.ArgumentParser(description="WeatherWise AI - Intelligent Weather Decision Agent")
    parser.add_argument(
        "--mode",
        choices=["web", "agent", "test"],
        default="web",
        help="Execution mode: 'web' for interactive UI dashboard, 'agent' for Fetch.ai uAgent node, 'test' for unit test suite."
    )
    parser.add_argument("--port", type=int, default=8080, help="Port for web server (default: 8080)")

    args = parser.parse_args()

    if args.mode == "test":
        logger.info("Executing WeatherWise AI Test Suite...")
        from tests.test_weather_agent import (
            test_geocoding, test_weather_retrieval, test_risk_scoring,
            test_recommendation_and_activities, test_smart_decision_engine,
            test_multi_agent_payload_export
        )
        test_geocoding()
        test_weather_retrieval()
        test_risk_scoring()
        test_recommendation_and_activities()
        test_smart_decision_engine()
        test_multi_agent_payload_export()
        print("\n[SUCCESS] All WeatherWise AI system tests executed successfully!")

    elif args.mode == "agent":
        logger.info("Starting Fetch.ai uAgents Node...")
        from agents.weather_agent import weather_agent
        weather_agent.run()

    else:
        logger.info(f"Starting WeatherWise AI Interactive Web Dashboard on http://127.0.0.1:{args.port}...")
        import uvicorn
        from web.server import app
        uvicorn.run(app, host="127.0.0.1", port=args.port)


if __name__ == "__main__":
    main()
