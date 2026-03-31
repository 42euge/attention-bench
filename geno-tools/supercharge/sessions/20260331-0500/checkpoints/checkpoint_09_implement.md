# Checkpoint 09 — Strengthen Writeup

## Cycle: 9 (Implement)
## Timestamp: 2026-03-31T06:15Z

## What was done

Strengthened `writeup.md` from 1,110 to 1,386 words (under 1,500 limit) with the following improvements:

### 1. Problem Statement — More provocative framing
- Reframed around the paradox: transformers have no attentional bottleneck, so why test for attention failures?
- Key insight added: "attention is not just about input access -- it is about selective processing under cognitive load"
- Lists all four cognitive paradigms with citations upfront

### 2. Task Descriptions — Tighter cognitive science connections
- Each task now names the seminal paper and explains the human finding it's based on
- Each task explains WHY the paradigm transfers to LLMs (e.g., "We test whether LLMs show an analogous cost despite having no reconfiguration delay")
- Broadbent (1958) added for Noise Filtering, human switch cost explanation for Context Switching

### 3. Technical Details — Clearer scoring narrative
- Emphasized flexible matching ("No task relies on brittle exact-string matching")
- Named `strip_thinking()` function explicitly with example model (Gemini 2.5 Flash Thinking)

### 4. Results Section — Expected patterns added
- Each PLACEHOLDER now has a specific "Expected pattern" paragraph
- Predictions are concrete (e.g., "adversarial noise at 10x outperforms unrelated noise at 50x")
- Shows judges we understand the design even before results arrive

### 5. Conclusion — "So what?" implications
- Connects findings to agent architectures, AI code review, and long-context applications
- Final sentence reframes attention as a universal challenge, not a biological limitation

## Commit
- `c7d62ec` — Strengthen writeup: sharper problem statement, tighter cog-sci links, expected results
- Pushed to remote

## Word count
- Before: 1,110
- After: 1,386
- Budget remaining: 114 words

## Status
Ready for results data to replace PLACEHOLDERs. The writeup structure and argumentation are now competition-ready.
