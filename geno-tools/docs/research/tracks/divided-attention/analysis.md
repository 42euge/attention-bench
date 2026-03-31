# Divided Attention — Full Analysis

#attention #divided-attention #analysis

## Overview

Divided attention is the ability to split cognitive resources across multiple concurrent demands. In humans, this capacity is fundamentally limited — performing two attention-demanding tasks simultaneously always incurs a cost, whether measured as slower response times, reduced accuracy, or both. The question for LLMs is whether analogous limitations exist despite their fundamentally different architecture.

Transformers process all input tokens in parallel through self-attention, which might suggest unlimited divided attention capacity. However, generation is autoregressive (serial at output), attention heads have finite capacity per layer, and recent work on retrieval heads (Wu et al. 2024) shows that fewer than 5% of attention heads handle long-range information retrieval. These architectural constraints create potential bottlenecks that our benchmark aims to expose.

Divided attention is distinct from selective attention (filtering relevant from irrelevant) and sustained attention (maintaining focus over time). It specifically asks: what happens when the model must do two things at once?

## Existing Work

| Paper | Year | Key Finding | Relevance |
|---|---|---|---|
| Multi-Task Inference (arXiv:2402.11597) | 2024 | SOTA models can sometimes improve with multi-task prompts; smaller models degrade significantly | Direct evidence of dual-task effects in LLMs |
| Multi-Turn Conversation Loss (arXiv:2505.06120) | 2025 | 39% average performance drop in multi-turn vs single-turn evaluation | Sustained + divided attention degradation over conversation |
| Retrieval Head Mechanism (arXiv:2404.15574) | 2024 | <5% of attention heads handle long-range retrieval; removing them collapses performance | Architectural basis for attention bottlenecks |
| Lost in the Middle (Liu et al. 2023) | 2023 | Models struggle to use information placed in the middle of long contexts | Position-dependent attention allocation failures |
| Needle in a Haystack (Kamradt 2023) | 2023 | Simple retrieval degrades with context length | Baseline for single-target attention in long contexts |
| RULER (Hsieh et al. 2024) | 2024 | Multi-key, multi-value retrieval tasks at various context lengths | Tests parallel retrieval but not true dual-task paradigms |

### Gap in Existing Work

The table above reveals a critical gap: no existing benchmark directly tests divided attention in LLMs using established cognitive psychology paradigms. Multi-task inference studies look at instruction-following with multiple tasks, but they don't systematically vary the attentional demands or measure interference curves. Lost-in-the-middle and needle-in-a-haystack test retrieval, not concurrent task execution. RULER comes closest with multi-key retrieval, but still frames the problem as a single retrieval task rather than two genuinely independent tasks competing for resources.

Our benchmark fills this gap by adapting two of the most well-validated paradigms from human attention research: the attentional blink and dual-task interference.

## Cognitive Science Foundations

### The Attentional Blink

Discovered by Raymond, Shapiro, and Arnell (1992), the attentional blink (AB) is one of the most replicated phenomena in attention research. The paradigm uses rapid serial visual presentation (RSVP): items appear one at a time at a rate of ~10 items/second. Two targets (T1 and T2) are embedded in the stream. When T2 appears 200-500ms after T1 (lags 2-5), detection drops to 50% or below, even though single-target detection is near ceiling.

Key features of the AB:
- **Lag-1 sparing**: T2 detection is paradoxically high when T2 immediately follows T1 (lag 1). This suggests a brief attentional "gate" that stays open for the item immediately following T1.
- **Blink magnitude**: The depth of the accuracy dip at lags 2-5 varies by individual and task difficulty, typically 20-50% below baseline.
- **Recovery**: By lag 6-8, T2 accuracy returns to near-baseline levels.
- **T1 dependency**: The blink only occurs when T1 is successfully detected. If T1 is missed, T2 accuracy is unaffected.

Theoretical accounts include:
- **Two-stage model** (Chun & Potter 1995): T1 enters a capacity-limited second stage; T2 is lost during this consolidation.
- **Boost and bounce theory** (Olivers & Meeter 2008): Detecting T1 triggers an attentional boost, followed by an inhibitory bounce that suppresses subsequent items.
- **Temporal attention** (Wyble et al. 2009): An episodic distinctiveness account where T2 fails to be encoded as a separate event.

### The Psychological Refractory Period (PRP)

When two tasks require responses in rapid succession, the response to the second task is delayed. This is the psychological refractory period (Telford 1931, extensively studied by Pashler 1994). The PRP effect is remarkably robust and has been used to map the architecture of human information processing.

The standard interpretation invokes a central bottleneck: while perceptual processing can run in parallel for both tasks, response selection for the second task must wait until response selection for the first task completes. This serial bottleneck produces the characteristic PRP curve — as the stimulus onset asynchrony (SOA) between tasks decreases, the response time for the second task increases linearly.

### Dual-Task Paradigms

Beyond PRP, dual-task research encompasses a broad range of paradigms:
- **Concurrent task performance**: Two continuous tasks performed simultaneously (e.g., tracking + detection). Performance is measured as the decrement relative to single-task baseline.
- **Task switching**: Alternating between two tasks. Switch costs (slower RT and lower accuracy on switch trials) reveal the overhead of reconfiguring task sets.
- **Resource competition**: When two tasks draw on the same cognitive resource (e.g., both require verbal working memory), interference is greater than when they use different resources (e.g., verbal + spatial).

### Capacity Theories

- **Kahneman (1973)**: A single, undifferentiated pool of attentional resources. Dual-task costs arise when total demand exceeds capacity.
- **Wickens (1984)**: Multiple resource theory. Different tasks draw on different resource pools (visual vs. auditory, verbal vs. spatial, perceptual vs. response). Interference is maximal when tasks share resources.
- **Lavie (2005)**: Load theory of attention. Under high perceptual load, attention is fully consumed by the primary task, leaving no resources for the secondary task or for processing distractors.

## Our Approach

### Task 1: Attentional Blink

We adapt the RSVP paradigm to text. A stream of 20 sentences is presented, with two target sentences (T1 and T2) embedded among distractors. T1 and T2 belong to different semantic categories (e.g., animals and cities), while distractors come from unrelated domains (science, history, technology). The model must identify both targets.

The critical manipulation is lag: the number of distractor sentences between T1 and T2, ranging from 1 to 8. By plotting T2 accuracy (conditional on correct T1 identification) as a function of lag, we can determine whether LLMs show a blink-like curve.

Design parameters:
- 3 category pairs (animals/cities, foods/professions, etc.)
- 5 T1 variants per category pair
- 8 lags
- Up to 120 items total

This task is novel because it tests temporal recovery — how quickly the model can re-engage attention after processing a first target. No existing benchmark measures this.

### Task 2: Dual-Task Interference

We present passages with two simultaneous task demands: (1) answer comprehension questions about the content, and (2) count occurrences of specific words. Three conditions allow us to isolate the dual-task cost:
- Single comprehension: answer questions only
- Single counting: count words only
- Dual: do both simultaneously

The dual-task cost is the difference between single-task and dual-task accuracy. We predict:
- Comprehension will be relatively preserved (it aligns with the model's primary training objective)
- Counting will suffer more (it requires a different processing mode — exact enumeration rather than semantic understanding)
- The asymmetry of interference will vary by model architecture and size

Design parameters:
- 3 passages of moderate complexity
- 4 comprehension questions per passage
- 2 counting targets per passage
- 42 total items across conditions

## Novel Ideas for Future Work

### 1. N-Back Dual Task
Combine an N-back working memory task with a concurrent semantic judgment task. This would test the intersection of divided attention and working memory, two constructs that are theoretically distinct but practically intertwined.

### 2. Task-Switching Costs
Rather than simultaneous performance, alternate between two task types across items. Measure switch costs (performance on switch trials vs. repeat trials). This would test cognitive flexibility — a component of executive function — through the lens of attention allocation.

### 3. Graded Dual-Task Load
Systematically vary the difficulty of both the primary and secondary tasks. If LLMs have a fixed attention budget, increasing primary task difficulty should disproportionately harm secondary task performance (consistent with Lavie's load theory).

### 4. Modality-Specific Interference
Test whether interference is greater when both tasks are linguistically similar (two verbal tasks) vs. when they differ in processing type (verbal comprehension + numerical counting). This would test whether LLMs show resource-specificity analogous to Wickens' multiple resource theory.

### 5. Attentional Blink with Emotional Targets
In humans, emotionally salient T2 items (e.g., threat words) can break through the attentional blink. Testing whether semantically loaded targets (e.g., safety-relevant content) show reduced blink in LLMs would reveal something about priority processing mechanisms.

### 6. Cross-Modal Divided Attention
Present interleaved code and natural language, requiring the model to answer questions about both. This tests real-world divided attention in a domain where LLMs are commonly deployed (code review with documentation).

## Cross-Cutting Themes

### Connection to Selective Attention
Divided attention and selective attention are complementary. Selective attention asks "can you focus on X while ignoring Y?" — divided attention asks "can you focus on X and Y simultaneously?" A model that excels at selective attention (strong filtering) might actually struggle with divided attention (because it filters out the secondary task). Our benchmark design allows cross-comparison.

### Connection to Sustained Attention
As divided attention tasks extend over longer sequences, sustained attention becomes a factor. The attentional blink task at longer lags tests sustained attention to some degree — the model must maintain the task goal across 20 sentences. Our dual-task interference task also requires sustained engagement with both task demands throughout the passage.

### Connection to Executive Function
Dual-task performance is sometimes classified under executive function rather than attention. The distinction is somewhat arbitrary — managing two concurrent tasks requires both attentional allocation and executive control. Our benchmark contributes to the broader question of whether LLMs have executive control mechanisms that can be isolated and measured.

### Architectural Implications
Different transformer architectures may show different divided attention profiles:
- **Dense models** (GPT-4, Claude): all parameters active, potentially more capacity for dual tasks
- **Mixture-of-experts** (Gemini, Mixtral): sparse activation might create different bottleneck patterns
- **Smaller models**: expected to show larger dual-task costs due to fewer parameters/heads
- **Reasoning models** (o1, DeepSeek-R1): chain-of-thought might serialize dual-task demands, increasing interference

## Key Papers

1. Raymond, J. E., Shapiro, K. L., & Arnell, K. M. (1992). Temporary suppression of visual processing in an RSVP task: An attentional blink? *Journal of Experimental Psychology: Human Perception and Performance*, 18(3), 849-860.

2. Pashler, H. (1994). Dual-task interference in simple tasks: Data and theory. *Psychological Bulletin*, 116(2), 220-244.

3. Kahneman, D. (1973). *Attention and effort*. Prentice-Hall.

4. Broadbent, D. E. (1958). *Perception and communication*. Pergamon Press.

5. Wickens, C. D. (1984). Processing resources in attention. In R. Parasuraman & D. R. Davies (Eds.), *Varieties of attention* (pp. 63-102). Academic Press.

6. Lavie, N. (2005). Distracted and confused?: Selective attention under load. *Trends in Cognitive Sciences*, 9(2), 75-82.

7. Chun, M. M., & Potter, M. C. (1995). A two-stage model for multiple target detection in rapid serial visual presentation. *Journal of Experimental Psychology: Human Perception and Performance*, 21(1), 109-127.

8. Wu, Y., et al. (2024). Retrieval Head Mechanistically Explains Long-Context Factuality. *arXiv:2404.15574*.

9. Liu, N. F., et al. (2023). Lost in the Middle: How Language Models Use Long Contexts. *arXiv:2307.03172*.

10. Deng, Y., et al. (2024). Multi-Task Inference: Can Large Language Models Follow Multiple Instructions at Once? *arXiv:2402.11597*.

11. Chen, L., et al. (2025). Multi-Turn Conversation Loss in Large Language Models. *arXiv:2505.06120*.

12. Hsieh, C.-P., et al. (2024). RULER: What's the Real Context Size of Your Long-Context Language Models? *arXiv:2404.06654*.

---

## Changelog
- 2026-03-29: Initial analysis from full research sweep
