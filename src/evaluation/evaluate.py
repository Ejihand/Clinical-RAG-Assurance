import pandas as pd
import sys
from pathlib import Path
from datasets import Dataset 
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,  # <--- FIXED: Added 'y'
    context_precision,
    context_recall,
)

# Path Setup
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.rag import get_rag_chain

def run_evaluation():
    print(f"\n{'='*60}")
    print(" 🏥 CLINICAL RAG ASSURANCE: Running Evaluation")
    print(f"{'='*60}")

    # 1. Load the Test Set
    testset_path = PROJECT_ROOT / "data" / "clinical_testset.csv"
    if not testset_path.exists():
        raise FileNotFoundError("run generate_testset.py first!")
    
    df = pd.read_csv(testset_path)
    
    # Limit for quick testing (Answering 3 questions to save time/cost)
    # You can remove [:3] later to run the full exam
    subset_df = df.head(3)
    
    questions = subset_df['question'].tolist()
    # Ragas requires ground_truths to be a list of lists (e.g., [['Answer A'], ['Answer B']])
    ground_truths = [[gt] for gt in subset_df['ground_truth'].tolist()]

    print(f"📝 Taking the exam... ({len(questions)} questions)")

    # 2. Get the RAG Chain
    rag_chain, retriever = get_rag_chain()

    answers = []
    contexts = []

    # 3. Generate Answers
    for i, q in enumerate(questions):
        print(f"   [{i+1}/{len(questions)}] Answering: {q[:50]}...")
        
        # Get Answer
        response = rag_chain.invoke(q)
        answers.append(response)
        
        # Get Contexts (The exact text chunks the AI used)
        docs = retriever.invoke(q)
        contexts.append([d.page_content for d in docs])

    # 4. Prepare Data for Ragas
    # STRICT FORMATTING: 'ground_truths' must be plural and a list of lists
    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truths": ground_truths 
    }
    dataset = Dataset.from_dict(data)

    # 5. Calculate Scores
    print("\n⚖️  Grading the exams (using GPT-4o)...")
    results = evaluate(
        dataset=dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        ],
    )

    print(f"\n{'='*60}")
    print(" 🏆 FINAL CLINICAL SCORE CARD")
    print(f"{'='*60}")
    print(results)
    
    # Save Results
    results_df = results.to_pandas()
    output_file = PROJECT_ROOT / "data" / "evaluation_results.csv"
    results_df.to_csv(output_file, index=False)
    print(f"\n💾 Detailed results saved to: {output_file.name}")

if __name__ == "__main__":
    run_evaluation()