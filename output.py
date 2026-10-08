import json
from pydantic import BaseModel


def save_insights(insights, filename="final_insights.json"):
    """Saves list of LLM insights or error dicts to a JSON file, sorted by urgency_score (High to Low)."""
    processed = []
    for item in insights:
        if isinstance(item, BaseModel):
            processed.append(item.model_dump())
        else:
            processed.append(item)

    # Sort items by urgency_score descending (High -> Low).
    # Items without urgency_score (e.g. failed fetches) get default score 0 and go to the end.
    processed.sort(
        key=lambda x: x.get("urgency_score", 0) if isinstance(x, dict) else getattr(x, "urgency_score", 0),
        reverse=True
    )

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(processed, f, indent=4, ensure_ascii=False)

    print(f"Successfully saved {len(processed)} insights (sorted by Urgency Score: High -> Low) to {filename}")
