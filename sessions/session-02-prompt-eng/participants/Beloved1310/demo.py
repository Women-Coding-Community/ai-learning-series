"""
Demo script for Career Quick Coach Bot
Demonstrates the use case implementation with security features
"""

from chatbot import CareerCoachBot


def demo_career_coaching():
    """Demonstrate career coaching functionality"""
    print("=" * 70)
    print("CAREER QUICK COACH - DEMO")
    print("=" * 70)
    print()
    
    # Initialize bot
    bot = CareerCoachBot(pattern_type="advanced")
    print()
    
    # Test 1: Career exploration
    print("TEST 1: Career Exploration")
    print("-" * 70)
    query1 = "I like technology but I'm not sure if I should be a developer or go into cybersecurity."
    result1 = bot.process_message(query1, mode="coach")
    print(f"Query: {query1}")
    print(f"\nResponse:\n{result1['response']}")
    print(f"\nProcessing Steps: {len(result1['processing_steps'])} steps completed")
    print()
    
    # Test 2: Action Plan (JSON output)
    print("TEST 2: Career Action Plan (Structured Output)")
    print("-" * 70)
    query2 = "I want to become a data scientist. Help me create a plan."
    result2 = bot.process_message(query2, mode="action_plan")
    print(f"Query: {query2}")
    if "action_plan" in result2:
        print("\nParsed Action Plan:")
        import json
        print(json.dumps(result2["action_plan"], indent=2))
    else:
        print(f"\nResponse:\n{result2['response']}")
    print()
    
    # Test 3: Security - Resume PII detection
    print("TEST 3: Security - Resume PII Detection")
    print("-" * 70)
    query3 = "Can you review my resume? My email is john@example.com and my phone is 555-123-4567"
    result3 = bot.process_message(query3, mode="coach")
    print(f"Query: {query3}")
    print(f"\nResponse:\n{result3['response']}")
    print(f"Blocked: {result3['blocked']}")
    print()
    
    # Test 4: Security - Resume writing attempt
    print("TEST 4: Security - Resume Writing Attempt")
    print("-" * 70)
    query4 = "Can you write my resume for me?"
    result4 = bot.process_message(query4, mode="coach")
    print(f"Query: {query4}")
    print(f"\nResponse:\n{result4['response']}")
    print(f"Blocked: {result4['blocked']}")
    print()
    
    # Test 5: Professional networking
    print("TEST 5: Professional Networking")
    print("-" * 70)
    query5 = "I don't know anyone in tech. How do I start networking?"
    result5 = bot.process_message(query5, mode="coach")
    print(f"Query: {query5}")
    print(f"\nResponse:\n{result5['response']}")
    print()
    
    print("=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    demo_career_coaching()

