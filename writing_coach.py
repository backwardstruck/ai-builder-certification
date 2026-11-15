#!/usr/bin/env python3
"""
Writing Coach - provides feedback on writing quality and style.
"""

class WritingCoach:
    """A coach that analyzes and provides feedback on writing."""

    def __init__(self):
        self.feedback_areas = [
            "clarity",
            "conciseness",
            "tone",
            "structure",
            "grammar",
            "vocabulary",
        ]

    def analyze(self, text: str) -> dict:
        """Analyze writing and return feedback."""
        return {
            "word_count": len(text.split()),
            "sentence_count": len([s for s in text.split('.') if s.strip()]),
            "feedback": self._get_feedback(text),
            "suggestions": self._get_suggestions(text),
        }

    def _get_feedback(self, text: str) -> dict:
        """Generate feedback on each area."""
        feedback = {}

        # Clarity
        feedback["clarity"] = {
            "score": self._check_clarity(text),
            "notes": "Are the main points easy to understand?"
        }

        # Conciseness
        feedback["conciseness"] = {
            "score": self._check_conciseness(text),
            "notes": "Is every word earning its place?"
        }

        # Tone
        feedback["tone"] = {
            "score": self._check_tone(text),
            "notes": "Does the voice match your intent?"
        }

        # Structure
        feedback["structure"] = {
            "score": self._check_structure(text),
            "notes": "Do ideas flow logically?"
        }

        return feedback

    def _check_clarity(self, text: str) -> int:
        """Score clarity (1-10)."""
        # Stub: return middle score
        return 5

    def _check_conciseness(self, text: str) -> int:
        """Score conciseness (1-10)."""
        # Stub: check for redundancy
        return 6

    def _check_tone(self, text: str) -> int:
        """Score tone consistency (1-10)."""
        # Stub: analyze voice
        return 5

    def _check_structure(self, text: str) -> int:
        """Score structure/flow (1-10)."""
        # Stub: check paragraph breaks
        return 5

    def _get_suggestions(self, text: str) -> list:
        """Return specific suggestions."""
        suggestions = []

        # Example suggestions
        lines = text.split('\n')
        if len(lines) > 10:
            suggestions.append("Break this into shorter paragraphs for readability.")

        if len(text.split()) > 500:
            suggestions.append("Consider tightening — aim for clarity over length.")

        return suggestions

    def coach_on_rewrite(self, original: str, rewrite: str) -> dict:
        """Compare original vs rewrite and give feedback."""
        return {
            "original_score": self.analyze(original),
            "rewrite_score": self.analyze(rewrite),
            "improvements": self._compare(original, rewrite),
        }

    def _compare(self, original: str, rewrite: str) -> dict:
        """Compare two versions."""
        orig_words = len(original.split())
        rewrite_words = len(rewrite.split())

        return {
            "word_reduction": orig_words - rewrite_words,
            "percent_change": round(((orig_words - rewrite_words) / orig_words * 100), 1) if orig_words else 0,
        }


if __name__ == "__main__":
    coach = WritingCoach()

    sample = """
    The writing that we have written here is something that needs
    to be improved. It is important to make sure that the words we use
    are clear and concise.
    """

    result = coach.analyze(sample)
    print("Analysis:", result)
