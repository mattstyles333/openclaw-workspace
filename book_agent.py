#!/usr/bin/env python3
"""Use browser-use Agent to book the court"""
import asyncio
from browser_use import Agent

async def book_court():
    # Create agent with task
    agent = Agent(
        task="""
        Navigate to https://www.smartclubcloud.com/
        Login with username: matthew.styles.1963, password: James333
        Click on Bookings
        Click Book Now button
        Select Squash from the dropdown
        Navigate to Friday 20 Feb 2026
        Click on Court 1, 18:00-19:00 time slot
        Click Extend button to make it 1 hour
        Click Book button to confirm
        """,
        llm=None,  # Use default
    )
    
    print("🤖 Starting agent...")
    result = await agent.run()
    print(f"✅ Agent result: {result}")

if __name__ == "__main__":
    asyncio.run(book_court())
