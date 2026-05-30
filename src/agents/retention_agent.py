import os
import json
from dotenv import load_dotenv

load_dotenv()

def generate_retention_email(user_data, primary_driver, risk_score):
    """
    Generates a personalized retention email using Groq LLM (if available)
    or falls back to a smart heuristic template if no API key is provided.
    """
    api_key = os.getenv("GROQ_API_KEY")
    
    # Context building
    context = f"""
    User ID: {user_data['user_id']}
    Churn Risk Score: {risk_score:.0%}
    Active Days (Tenure): {user_data['active_days']} days
    Days Since Last Activity: {user_data['days_since_last_activity']} days
    Average Sessions Per Day: {user_data['avg_sessions_per_day']:.2f}
    Total Sessions: {user_data['total_sessions']}
    
    The ML model identified that the primary reason they are at risk of churning is: {primary_driver}.
    """

    # If Groq is available
    if api_key and api_key != "your_groq_api_key_here":
        try:
            from groq import Groq
            client = Groq(api_key=api_key)
            
            prompt = f"""
            You are a senior customer success manager at an EdTech SaaS platform.
            Your goal is to write a highly personalized, empathetic, and short "win-back" email to a user who is at high risk of churning.
            
            Here is the data about the user:
            {context}
            
            Instructions:
            1. If the primary driver is "days_since_last_activity", focus on welcoming them back, offering a quick 1-minute tutorial or new content they missed.
            2. If the primary driver is "avg_sessions_per_day" (dropping engagement), ask for feedback on what's missing, or offer a 1-on-1 coaching call.
            3. Keep the tone encouraging, not accusatory. Do not mention their "churn score" or "machine learning" to them.
            4. Keep it under 100 words.
            5. Return ONLY the email body (Subject line on first line, then the body).
            """
            
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Groq API Error: {e}")
            return _fallback_template(user_data, primary_driver)
    else:
        # Fallback to local heuristic templates
        return _fallback_template(user_data, primary_driver)

def _fallback_template(user_data, primary_driver):
    if "days_since_last_activity" in primary_driver:
        return f"""Subject: We miss you on the platform!

Hi there,

I noticed it's been {user_data['days_since_last_activity']} days since your last login. Sometimes life gets in the way of learning, and that's completely okay!

We've added some great new bite-sized modules since you were last here. Would you be open to a quick 5-minute chat this week to see how we can get your momentum back up? 

Best,
Customer Success Team"""
    elif "avg_sessions_per_day" in primary_driver or "total_sessions" in primary_driver:
        return f"""Subject: Checking in on your progress

Hi there,

You've been with us for {user_data['active_days']} days, which is awesome! However, I noticed your session activity has dipped a bit recently. 

Is there anything you're struggling with, or a specific topic you're trying to master? I'd love to jump on a quick call to help you get the most out of your subscription.

Best,
Customer Success Team"""
    else:
        return """Subject: Checking in

Hi there,

Just checking in to see how you're doing with your learning journey. Let us know if you need any support!

Best,
Customer Success Team"""

if __name__ == "__main__":
    # Test
    mock_data = {
        'user_id': 123,
        'active_days': 45,
        'days_since_last_activity': 20,
        'avg_sessions_per_day': 1.1,
        'total_sessions': 50
    }
    print(generate_retention_email(mock_data, "days_since_last_activity", 0.85))
