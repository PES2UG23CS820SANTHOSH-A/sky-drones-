from typing import Dict, List
import pandas as pd


class UrgentReassigner:
    def __init__(self):
        pass

    def suggest_alternatives(
        self,
        available_pilots: pd.DataFrame,
        available_drones: pd.DataFrame,
        mission: Dict,
        top_k: int = 2
    ) -> List[Dict]:
        """
        Suggest alternative pilot-drone pairs for urgent missions.
        Location constraints are relaxed, but skill constraints remain.
        """

        suggestions = []
        required_skill = mission.get("required skill")

        for _, pilot in available_pilots.iterrows():
            # Keep skill constraint even in urgent mode
            if required_skill and required_skill.lower() not in str(pilot["skills"]).lower():
                continue

            for _, drone in available_drones.iterrows():
                score = 0

                # Skill-capability match
                if required_skill and required_skill.lower() in str(drone["capabilities"]).lower():
                    score += 1

                suggestions.append({
                    "pilot_name": pilot["name"],
                    "drone_id": drone["drone id"],
                    "note": "Urgent reassignment (location constraint relaxed)",
                    "score": score
                })

        # Sort by score and return top_k
        suggestions = sorted(suggestions, key=lambda x: x["score"], reverse=True)

        return suggestions[:top_k]
