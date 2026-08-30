# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import concurrent.futures
import json
import logging
import os
import threading
import pandas as pd
from collections import defaultdict
from typing import Dict, List, Any, Optional

import hydra
from omegaconf import DictConfig

from memora.utils.llm import get_aoai_chat_completion_client
from memora.utils.log import configure_logging
from metrics.llm_judge import evaluate_llm_judge
from metrics.utils import calculate_bleu_scores, calculate_metrics
from tqdm import tqdm

logger = logging.getLogger(__name__)

# Question type-specific evaluation prompts (from Nemori/Zep)
TEMPORAL_REASONING_PROMPT = """
I will give you a question, a correct answer, and a response from a model. Please answer yes if the response contains the correct answer. Otherwise, answer no. If the response is equivalent to the correct answer or contains all the intermediate steps to get the correct answer, you should also answer yes. If the response only contains a subset of the information required by the answer, answer no. In addition, do not penalize off-by-one errors for the number of days. If the question asks for the number of days/weeks/months, etc., and the model makes off-by-one errors (e.g., predicting 19 days when the answer is 18), the model's response is still correct.

<QUESTION>
B: {question}
</QUESTION>
<CORRECT ANSWER>
{gold_answer}
</CORRECT ANSWER>
<RESPONSE>
A: {response}
</RESPONSE>

Please answer 'yes' or 'no':"""

KNOWLEDGE_UPDATE_PROMPT = """
I will give you a question, a correct answer, and a response from a model. Please answer yes if the response contains the correct answer. Otherwise, answer no. If the response contains some previous information along with an updated answer, the response should be considered as correct as long as the updated answer is the required answer.

<QUESTION>
B: {question}
</QUESTION>
<CORRECT ANSWER>
{gold_answer}
</CORRECT ANSWER>
<RESPONSE>
A: {response}
</RESPONSE>

Please answer 'yes' or 'no':"""

SINGLE_SESSION_PREFERENCE_PROMPT = """
I will give you a question, a rubric for desired personalized response, and a response from a model. Please answer yes if the response satisfies the desired response. Otherwise, answer no. The model does not need to reflect all the points in the rubric. The response is correct as long as it recalls and utilizes the user's personal information correctly.

<QUESTION>
B: {question}
</QUESTION>
<RUBRIC>
{gold_answer}
</RUBRIC>
<RESPONSE>
A: {response}
</RESPONSE>

Please answer 'yes' or 'no':"""

DEFAULT_PROMPT = """
I will give you a question, a correct answer, and a response from a model. Please answer yes if the response contains the correct answer. Otherwise, answer no. If the response is equivalent to the correct answer or contains all the intermediate steps to get the correct answer, you should also answer yes. If the response only contains a subset of the information required by the answer, answer no.

<QUESTION>
B: {question}
</QUESTION>
<CORRECT ANSWER>
{gold_answer}
</CORRECT ANSWER>
<RESPONSE>
A: {response}
</RESPONSE>

Please answer 'yes' or 'no':"""


def evaluate_with_question_type_prompt(model_client, question: str, gold_answer: str, 
                                       response: str, question_type: str, eval_model: str) -> bool:
    """
    Evaluate response using question type-specific prompts (Nemori/Zep style).
    
    Args:
        model_client: OpenAI client
        question: Question text
        gold_answer: Gold standard answer
        response: Model response
        question_type: Question type (temporal-reasoning, knowledge-update, etc.)
        eval_model: Evaluation model
        
    Returns:
        Boolean indicating if response is correct
    """
    system_prompt = "You are an expert grader that determines if answers to questions match a gold standard answer"
    
    # Select prompt based on question type
    if question_type == 'temporal-reasoning':
        prompt = TEMPORAL_REASONING_PROMPT.format(
            question=question, gold_answer=gold_answer, response=response
        )
    elif question_type == 'knowledge-update':
        prompt = KNOWLEDGE_UPDATE_PROMPT.format(
            question=question, gold_answer=gold_answer, response=response
        )
    elif question_type == 'single-session-preference':
        prompt = SINGLE_SESSION_PREFERENCE_PROMPT.format(
            question=question, gold_answer=gold_answer, response=response
        )
    else:
        prompt = DEFAULT_PROMPT.format(
            question=question, gold_answer=gold_answer, response=response
        )
    
    try:
        response_obj = model_client.chat.completions.create(
            model=eval_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=10,  # We only need "yes" or "no"
        )
        
        answer = response_obj.choices[0].message.content.strip().lower()
        return 'yes' in answer
        
    except Exception as e:
        logger.error(f"Error in question type evaluation: {e}")
        return False


def process_item(model_client, eval_model, entry, use_question_type_eval: bool = False):
    """
    Process a single item for evaluation.
    
    Args:
        model_client: OpenAI client
        eval_model: Evaluation model name
        entry: Single data entry dict
        use_question_type_eval: Whether to use question type-specific evaluation prompts
    """
    question = str(entry["question"])

    gt_answer = entry["answer"]
    generated_answer = entry["generated_answer"]
        
    # LongMemEval uses question_type instead of category
    question_type = entry.get("question_type", "")
    question_id = entry.get("question_id", "")

    # Calculate metrics
    metrics = calculate_metrics(generated_answer, gt_answer)
    bleu_scores = calculate_bleu_scores(generated_answer, gt_answer)
    
    # Use question type-specific evaluation if enabled
    if use_question_type_eval:
        is_correct = evaluate_with_question_type_prompt(
            model_client, question, gt_answer, generated_answer, question_type, eval_model=eval_model
        )
        llm_score = 1.0 if is_correct else 0.0
    else:
        # Use original LLM judge evaluation
        llm_score = evaluate_llm_judge(model_client=model_client,
                                        question=question,
                                        gold_answer=gt_answer,
                                        generated_answer=generated_answer,
                                        model=eval_model)

    result = {
        "question_id": question_id,
        "question": question,
        "answer": gt_answer,
        "generated_answer": generated_answer,
        "question_type": question_type,
        "bleu_score": bleu_scores["bleu1"],
        "f1_score": metrics["f1"],
        "llm_score": llm_score,
    }

    return result


def _load_input_data(input_file: str) -> List[Dict]:
    """
    Load input data from JSON dict (sequential mode) or JSONL (parallel mode).
    Returns a flat list of entry dicts.
    """
    with open(input_file, "r") as f:
        content = f.read().strip()

    if not content:
        return []

    # Try standard JSON first (sequential mode writes a dict)
    try:
        json_data = json.loads(content)
        if isinstance(json_data, dict):
            return [v for v in json_data.values() if isinstance(v, dict)]
        if isinstance(json_data, list):
            return json_data
    except json.JSONDecodeError:
        pass

    # Fall back to JSONL (parallel mode writes one JSON object per line)
    data = []
    for line in content.split("\n"):
        line = line.strip()
        if line:
            data.append(json.loads(line))
    return data


def evaluate(cfg: DictConfig, input_file: str, output_file: str,
             use_question_type_eval: bool = False, score_file: str = None):
    """
    Evaluate the predictions using multiple threads and save the results.

    Args:
        cfg: Configuration object
        input_file: Path to input results file
        output_file: Path to output evaluation file
        use_question_type_eval: Whether to use longmemeval style question type evaluation
        score_file: Path to output score file (optional, auto-generated if not provided)
    """

    # Auto-generate score file path if not provided
    if score_file is None:
        output_dir = os.path.dirname(output_file)
        output_basename = os.path.basename(output_file)
        if output_basename.endswith('_eval.json'):
            score_filename = output_basename.replace('_eval.json', '_scores.json')
        else:
            name, ext = os.path.splitext(output_basename)
            score_filename = f"{name}_scores{ext}"
        score_file = os.path.join(output_dir, score_filename)

    max_workers = cfg.eval.max_workers
    eval_model = cfg.eval.get("model", "gpt-4o-mini")

    data = _load_input_data(input_file)

    if not data:
        logger.warning(f"No data loaded from {input_file}")
        return None

    model_client = get_aoai_chat_completion_client(cfg)

    if use_question_type_eval:
        logger.info("Using LongMemEval-style question type-specific evaluation prompts")
    else:
        logger.info("Using standard LLM judge evaluation")

    results = []
    results_lock = threading.Lock()

    # Use ThreadPoolExecutor with specified workers
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_item, model_client, eval_model, entry, use_question_type_eval)
            for entry in data
        ]

        for future in tqdm(
            concurrent.futures.as_completed(futures), total=len(futures),
            desc="Evaluating responses"
        ):
            result = future.result()
            with results_lock:
                results.append(result)

    # Save results to JSON file
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)

    logger.info(f"Results saved to {output_file}")

    # Calculate and print aggregated scores
    scores_data = generate_scores(data=results, score_file=score_file)
    return scores_data


def generate_scores(metrics_file: str = None, score_file: str = None, data: List[Dict] = None):
    """
    Generate evaluation scores from metrics file or data.
    
    Args:
        metrics_file: Path to metrics file (optional if data is provided)
        score_file: Path to output score file (optional)
        data: List of evaluation results (optional if metrics_file is provided)
    """
    # Load the evaluation metrics data
    if data is None:
        with open(metrics_file, "r") as f:
            json_data = json.load(f)

        # Handle both list and dict formats
        if isinstance(json_data, dict):
            all_items = []
            for key in json_data:
                if isinstance(json_data[key], list):
                    all_items.extend(json_data[key])
                else:
                    all_items.append(json_data[key])
            data = all_items
        elif isinstance(json_data, list):
            data = json_data

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Use question_type for grouping (LongMemEval format)
    group_by_col = "question_type"

    # Calculate mean scores by question type
    result = (
        df.groupby(group_by_col)
        .agg({"bleu_score": "mean", "f1_score": "mean", "llm_score": "mean"})
        .round(4)
    )

    # Add count of questions per type
    result["count"] = df.groupby(group_by_col).size()

    # Print the results
    logger.info(f"\n{'='*60}")
    logger.info(f"Mean Scores Per Question Type:")
    logger.info(f"{'='*60}")
    for qtype in result.index:
        stats = result.loc[qtype]
        logger.info(f"{qtype:30s} | Count: {stats['count']:4.0f} | "
                   f"BLEU: {stats['bleu_score']:.4f} | "
                   f"F1: {stats['f1_score']:.4f} | "
                   f"LLM: {stats['llm_score']:.4f}")

    # Calculate overall means
    overall_means = df.agg(
        {"bleu_score": "mean", "f1_score": "mean", "llm_score": "mean"}
    ).round(4)

    logger.info(f"\n{'='*60}")
    logger.info(f"Overall Mean Scores:")
    logger.info(f"{'='*60}")
    logger.info(f"BLEU Score:  {overall_means['bleu_score']:.4f}")
    logger.info(f"F1 Score:    {overall_means['f1_score']:.4f}")
    logger.info(f"LLM Score:   {overall_means['llm_score']:.4f}")
    logger.info(f"Total Questions: {len(df)}")
    logger.info(f"{'='*60}\n")

    # Prepare results for saving to file
    scores_data = {
        "mean_scores_per_question_type": result.to_dict(),
        "overall_mean_scores": overall_means.to_dict(),
        "summary": {
            "total_questions": len(df),
            "question_types_evaluated": sorted(df[group_by_col].unique().tolist()),
            "evaluation_timestamp": pd.Timestamp.now().isoformat(),
        },
    }

    # Save results to score file
    if score_file:
        with open(score_file, "w") as f:
            json.dump(scores_data, f, indent=4)
        logger.info(f"Scores saved to {score_file}")

    return scores_data


@hydra.main(version_base=None, config_path="./conf", config_name="config")
def run(cfg: DictConfig):
    """
    Main evaluation function.
    
    Args:
        cfg: Hydra configuration object
    """

    # configure logging
    configure_logging()

    input_file = os.path.join(cfg.general.output_path, cfg.eval.result_file)
    output_file = os.path.join(cfg.general.output_path, cfg.eval.metrics_file)
    score_file = os.path.join(
        cfg.general.output_path, cfg.eval.get("score_file", "scores.json")
    )

    # Check if we should use question type-specific evaluation
    use_question_type_eval = cfg.eval.get("use_question_type_eval", False)
    
    if use_question_type_eval:
        logger.info("Using Nemori-style question type-specific evaluation prompts")
    else:
        logger.info("Using standard LLM judge evaluation")

    # evaluate
    evaluate(cfg, input_file, output_file, use_question_type_eval=use_question_type_eval)

    # generate scores
    scores_data = generate_scores(output_file, score_file)

    return scores_data


if __name__ == "__main__":
    run()