# AI Builder Certification

A hands-on certification for learning to identify, design, and build reusable Claude agent skills — from workflow analysis through to a deployable skill file.

## Overview

This repo documents the AI Builder Certification journey: learning to analyze real business workflows, identify the best candidates to package as Claude agent skills, and build those skills as reusable bundles of instructions, context, and reference material that Claude loads on demand to handle a repeatable task consistently.

The practical focus is a **job search workflow** — a multi-step process that maps cleanly onto discrete, automatable skills.

## Skills

| Skill | Purpose |
|---|---|
| [`job-listing-filter`](skills/job-listing-filter.skill) | Analyzes job listings and filters them against a target profile to surface the best-fit opportunities |
| [`job-application-tailor`](skills/job-application-tailor.skill) | Tailors a resume and cover letter to a specific job listing and company |
| [`interview-prep`](skills/interview-prep.skill) | Generates role-specific interview preparation materials based on the job listing and company research |

## Getting Started

1. Clone this repo
2. Open [Claude Code](https://claude.ai/code) or the Claude desktop app
3. Load a skill by referencing the `.skill` file path in your Claude Code project
4. Run the skill against your own inputs (job listing, resume, etc.)

## Prerequisites

- A Claude account (Pro or above recommended for agent skill usage)
- Claude Code CLI or Claude desktop app
- Basic familiarity with prompt-based workflows

## About the Certification

The AI Builder Certification is structured around the [AI Workflow Framework](https://www.handsonai.co) — a 7-step process for turning business workflows into production-ready AI automations:

1. **Analyze** — identify workflow candidates
2. **Deconstruct** — define requirements
3. **Design** — choose orchestration and building blocks
4. **Build** — create the skill or agent artifacts
5. **Test** — validate against real inputs
6. **Run** — deploy and operate
7. **Improve** — measure and iterate

## Contributing

This is a personal certification project. Feel free to fork and adapt the skills for your own workflows.

## License

MIT — see [LICENSE](LICENSE)
