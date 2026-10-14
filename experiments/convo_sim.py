#!/usr/bin/env python3
"""
Conversation drift experiment.

Two Claude instances talk: one plays a simulated user, one plays the assistant.
Starting from a single seed question, they run N turns, then a third call
summarizes the conversation with the same request Eric gave Gemini.
Optionally a judge compares the result against the real Gemini summary.

Setup:
    pip install anthropic
    export ANTHROPIC_API_KEY=...

Examples:
    python convo_sim.py                              # one run, "eric" persona
    python convo_sim.py --persona generic --runs 3   # three runs, generic user
    python convo_sim.py --assistant-style engaging   # mimic a chatty assistant
    python convo_sim.py --compare gemini_summary.txt # judge vs. the real one
"""

import argparse
import json
import pathlib
import time

import anthropic

SEED = "what do worms eat how long do they live etc"

SUMMARY_REQUEST = (
    "Summarize the conversation so far in detail as subject areas and open questions"
)

PERSONAS = {
    # Built from the style of Eric's real prompts: short, informal, follows
    # tangents, connects things to software and LLMs, jumps to big implications.
    "eric": (
        "You are role-playing a curious adult chatting with an AI assistant. "
        "You have a software and AI engineering background but no training in "
        "biology, physics or philosophy. You keep a small worm jar at home. "
        "Write the way this person texts: short, informal, sometimes one line "
        "like 'It's a computer?'. Follow whatever tangent interests you most in "
        "the last answer. You like connecting things to code and LLMs, and you "
        "sometimes jump to big implications. Now and then you ask a skeptical "
        "question, like whether something is testable or has alternatives."
    ),
    "generic": (
        "You are role-playing a curious adult chatting with an AI assistant. "
        "Ask short, natural follow-up questions based on whatever in the last "
        "answer interests you most."
    ),
    "skeptic": (
        "You are role-playing a curious but skeptical adult chatting with an AI "
        "assistant. Ask short follow-ups. When a claim sounds surprising, ask "
        "for the evidence and who disagrees before moving on."
    ),
}

USER_RULES = (
    " Output ONLY your next message to the assistant, nothing else. "
    "Never answer your own questions. If you feel the conversation is "
    "finished, output exactly [END]."
)

ASSISTANT_STYLES = {
    "default": "You are a helpful assistant.",
    # Rough approximation of a chatty consumer assistant, to test whether
    # style alone drives the drift.
    "engaging": (
        "You are a helpful, enthusiastic assistant. Make answers engaging and "
        "end each one by suggesting interesting directions to explore next."
    ),
    "careful": (
        "You are a helpful assistant. Clearly separate established findings "
        "from speculation, say how mainstream each claim is, and name the main "
        "objections to speculative ideas."
    ),
}


def flip(history):
    """The user-sim sees the assistant's turns as 'user' and its own as 'assistant'."""
    swap = {"user": "assistant", "assistant": "user"}
    flipped = [{"role": swap[m["role"]], "content": m["content"]} for m in history]
    # The seed becomes an 'assistant' turn after flipping; open with a user
    # turn so the message list starts the way the API expects.
    if flipped and flipped[0]["role"] == "assistant":
        flipped.insert(0, {"role": "user", "content": "(Start the conversation.)"})
    return flipped


def call(client, model, system, messages, max_tokens):
    resp = client.messages.create(
        model=model, max_tokens=max_tokens, system=system, messages=messages
    )
    return "".join(b.text for b in resp.content if b.type == "text").strip()


def run_once(client, args, run_id, outdir):
    user_system = PERSONAS[args.persona] + USER_RULES
    asst_system = ASSISTANT_STYLES[args.assistant_style]

    history = [{"role": "user", "content": SEED}]
    for turn in range(args.turns):
        reply = call(client, args.assistant_model, asst_system, history, 1500)
        history.append({"role": "assistant", "content": reply})
        print(f"  [run {run_id}] turn {turn + 1}: assistant replied")

        if turn == args.turns - 1:
            break
        # flip() makes the last message (assistant's) a 'user' turn for the sim
        nxt = call(client, args.user_model, user_system, flip(history), 200)
        if not nxt or nxt.strip() == "[END]":
            break
        history.append({"role": "user", "content": nxt})
        print(f"  [run {run_id}] user-sim: {nxt}")

    history.append({"role": "user", "content": SUMMARY_REQUEST})
    summary = call(client, args.assistant_model, asst_system, history, 3000)
    history.append({"role": "assistant", "content": summary})

    stem = outdir / f"run{run_id}_{args.persona}_{args.assistant_style}"
    stem.with_suffix(".json").write_text(json.dumps(history, indent=2))
    prompts = [m["content"] for m in history if m["role"] == "user"]
    stem.with_suffix(".md").write_text(
        "## Simulated user prompts\n\n"
        + "\n".join(f"- {p}" for p in prompts)
        + "\n\n## Summary\n\n"
        + summary
        + "\n"
    )
    return prompts, summary


def judge(client, model, real, simulated):
    prompt = (
        "Compare two summaries of AI chat conversations that started from the "
        "same question.\n\n<real>\n" + real + "\n</real>\n\n<simulated>\n"
        + simulated + "\n</simulated>\n\n"
        "Report briefly: (1) overlap in the topic path, (2) where they diverge, "
        "(3) which presents more speculation as established fact, with examples, "
        "(4) a 0-10 similarity score."
    )
    return call(client, model, "You are a careful analyst.", [
        {"role": "user", "content": prompt}
    ], 1500)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--persona", choices=PERSONAS, default="eric")
    p.add_argument("--assistant-style", choices=ASSISTANT_STYLES, default="default")
    p.add_argument("--turns", type=int, default=15)
    p.add_argument("--runs", type=int, default=1)
    p.add_argument("--assistant-model", default="claude-sonnet-5-5")
    p.add_argument("--user-model", default="claude-haiku-5-5")
    p.add_argument("--compare", help="path to the real Gemini summary text")
    p.add_argument("--out", default="sim_runs")
    args = p.parse_args()

    client = anthropic.Anthropic()
    outdir = pathlib.Path(args.out) / time.strftime("%Y%m%d-%H%M%S")
    outdir.mkdir(parents=True, exist_ok=True)
    real = pathlib.Path(args.compare).read_text() if args.compare else None

    for i in range(1, args.runs + 1):
        print(f"Run {i}/{args.runs}")
        _, summary = run_once(client, args, i, outdir)
        if real:
            verdict = judge(client, args.assistant_model, real, summary)
            (outdir / f"run{i}_judge.md").write_text(verdict + "\n")
            print(verdict)

    print(f"\nSaved to {outdir}")


if __name__ == "__main__":
    main()
