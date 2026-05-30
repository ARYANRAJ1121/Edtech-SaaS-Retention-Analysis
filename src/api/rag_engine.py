import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

load_dotenv()

# Simulate a Vector DB loaded with Course Transcripts
COURSE_KNOWLEDGE_BASE = [
    {"id": "mod1_01", "topic": "Python Basics", "content": "In Python, variables are dynamically typed. Example: x = 5 creates an integer. x = 'hello' creates a string."},
    {"id": "mod1_02", "topic": "For Loops", "content": "A for loop is used for iterating over a sequence (list, tuple, dictionary, set, or string). Example: for i in range(5): print(i)"},
    {"id": "mod2_01", "topic": "SQL Joins", "content": "An INNER JOIN returns records that have matching values in both tables. A LEFT JOIN returns all records from the left table, and matched records from the right."},
    {"id": "mod2_02", "topic": "SQL Group By", "content": "The GROUP BY statement groups rows that have the same values into summary rows, like find the number of customers in each country."},
    {"id": "mod3_01", "topic": "Machine Learning Overfitting", "content": "Overfitting happens when a model learns the detail and noise in the training data to the extent that it negatively impacts the performance of the model on new data."}
]

class LightweightRAGEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.documents = [doc["content"] for doc in COURSE_KNOWLEDGE_BASE]
        self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)
        
    def retrieve_context(self, query):
        """Find the most relevant course material based on the user's struggle"""
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        best_match_idx = similarities.argmax()
        
        if similarities[best_match_idx] > 0.1:
            return COURSE_KNOWLEDGE_BASE[best_match_idx]
        return None

    def generate_intervention(self, user_id, failed_topic):
        """Uses Groq to generate a personalized micro-lesson using RAG"""
        api_key = os.getenv("GROQ_API_KEY")
        
        # RAG Step 1: Retrieve context
        context_data = self.retrieve_context(failed_topic)
        context_text = context_data['content'] if context_data else f"General concepts regarding {failed_topic}."
        
        if not api_key or api_key == "your_groq_api_key_here":
            return f"⚠️ [RAG Agent Offline] User {user_id} failed {failed_topic}. Context retrieved: '{context_text}'. (Connect Groq API for full lesson generation)"
            
        try:
            from groq import Groq
            client = Groq(api_key=api_key)
            
            prompt = f"""
            You are an AI Tutor. The user (ID: {user_id}) just failed a quiz on: {failed_topic}.
            This increases their churn risk significantly.
            
            Based ONLY on the following course transcript material, generate a highly encouraging, 
            personalized 3-sentence micro-lesson to help them understand the concept, followed by a call to action to retake the quiz.
            
            Course Transcript Material: {context_text}
            
            Tone: Empathetic, expert, concise.
            """
            
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=250
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Agent Error: {str(e)}"

# Singleton instance
rag_agent = LightweightRAGEngine()
