---
name: avoid-ai-writing-tropes
description: Use when writing or editing prose documents (READMEs, design docs, PR descriptions, blog posts, comments-as-prose, status updates, emails, wiki pages). Avoids the patterns that make text read as AI-generated. NOT for writing code — this is about documents.
---

# Avoid AI Writing Tropes

LLM-generated prose has a distinctive shape: ornate vocabulary, theatrical sentence structures, formulaic transitions, and decorative formatting. Readers notice. The patterns below are statistically overrepresented in model output and signal AI authorship even when the underlying content is fine.

Source: https://tropes.fyi/tropes-md

## Core principle

Any one of these patterns used once may be fine. The problem is **clustering** — multiple tropes in the same document — and **repetition** — the same pattern firing many times in one piece.

Effective writing is varied, specific, and slightly imperfect. If your draft reads like it was assembled from a template, it probably was.

## When to apply

- Writing or editing any document a human will read as prose: READMEs, design docs, RFCs, PR descriptions, status updates, blog posts, wiki pages, emails, Slack messages of any length, commit messages longer than a line.
- Editing prose someone else wrote — flag tropes you find rather than silently leaving them.
- **Not for code.** Code comments that explain *why* are fine; this skill is about prose documents. Variable names, code structure, and inline comments follow other rules.

## Tropes to avoid

### Word choice

**Magic adverbs.** "Quietly," "deeply," "fundamentally," "profoundly," "carefully" used to inflate ordinary descriptions. They add atmosphere without information.
- Bad: "quietly orchestrating workflows"
- Better: "orchestrating workflows" — or describe what it actually does

**Formal LLM vocabulary.** "Delve," "utilize," "leverage," "robust," "harness," "facilitate," "elucidate." These are statistically overrepresented in model output.
- Bad: "Let's delve into the details" / "We utilize this approach"
- Better: "Let's look at the details" / "We use this approach"

**Grandiose nouns.** "Tapestry," "landscape," "ecosystem," "realm," "journey" substituted for ordinary words.
- Bad: "the rich tapestry of human experience"
- Better: "human experience"

**"Serves as" / "marks" / "represents"** instead of plain "is/are."
- Bad: "The building serves as a reminder"
- Better: "The building reminds us" or "The building is a reminder"

### Sentence structure

**Negative parallelism: "It's not X — it's Y."** Framing claims as surprise reveals.
- Bad: "It's not bold. It's backwards."
- Better: State the claim directly: "It's backwards."

**"Not X. Not Y. Just Z."** Dramatic countdown that negates options before revealing the answer.
- Bad: "Not a bug. Not a feature. A design flaw."
- Better: "It's a design flaw."

**"The X? A Y."** Self-posed rhetorical questions answered immediately.
- Bad: "The result? Devastating."
- Better: "The result was devastating."

**Anaphora abuse.** Repeating identical sentence openings in close succession.
- Bad: "They could expose... They could offer... They could provide..."
- Better: Vary the openings.

**Tricolon abuse.** Stacking rule-of-three constructions back-to-back, or extending to four/five items.
- One tricolon is fine. Three in a row reads as formula.

**Empty transitions.** "Importantly," "Interestingly," "Notably," "It's worth noting that..." — used as filler instead of logical connection.
- Bad: "Interestingly, this pattern repeats across industries."
- Better: Connect ideas explicitly, or just state the pattern.

**Tacked-on "-ing" significance.** Phrases like "highlighting its enduring legacy," "underscoring the importance of," "marking a pivotal moment."
- Bad: "...highlighting its enduring legacy of transformative power"
- Better: Cut it, or explain the actual significance with specifics.

**False ranges: "from X to Y."** When X and Y don't form a real spectrum.
- Bad: "from innovation to cultural transformation"
- Better: List the items separately if they aren't a continuum.

### Paragraph structure

**Short punchy fragments.** One-sentence paragraphs strung together for fake emphasis.
- Bad: "He published this. Openly. In a book."
- Better: "He published this openly in a book."

**Listicle in a trench coat.** Hiding lists in prose with "The first... The second... The third..."
- Use an actual list, or integrate the points into flowing prose.

### Tone

**"Here's the kicker" / "Here's the thing" / "Here's where it gets interesting."** Manufactured suspense before unremarkable points.
- Just present the point.

**"Think of it as..." / "Imagine a..."** Patronizing analogies, especially when the original concept is already clear.
- Use analogies only when they genuinely clarify. Don't simplify what doesn't need simplifying.

**"Imagine a world where..."** Marketing-style futurist framing.
- Bad: "Imagine a world where every tool has quiet intelligence..."
- Better: Describe the scenario concretely, or skip the framing.

**False vulnerability.** Performative self-awareness — "I'll be honest with you...", "Full disclosure: I love this product."
- Either make a genuine, specific admission or skip it.

**"The truth is simple" / "The reality is..."** Asserting clarity instead of demonstrating it.
- If you have to claim your point is clear, it isn't.

**Stakes inflation.** "This will fundamentally reshape everything," "a paradigm shift," "world-changing."
- Match the claim to the actual significance.

**"Let's break this down" / "Let's unpack" / "Let's explore."** Teacher-student framing.
- Just proceed to the analysis.

**Vague attributions.** "Experts say...", "Industry observers note...", "Studies show..."
- Name specific sources, or omit attribution.

**Invented concept labels.** Coining "the X paradox" or "the Y trap" without defining them, then using them as if they were established terms.
- Define new concepts, or use established ones.

### Formatting

**Em-dash addiction.** Human writers use 2–3 em dashes per piece. AI drafts often have 20+.
- Use em dashes sparingly for genuine parenthetical emphasis.

**Bold-first bullets.** Every bullet starting with a bolded label.
- Bad: every bullet formatted as "**Label**: explanation"
- Better: bold strategically, not uniformly.

**Unicode decoration.** Smart quotes, unicode arrows (→), bullet glyphs (•) where ASCII would do.
- Use ASCII unless the document genuinely benefits from typographic characters.

### Composition

**Fractal summaries.** Restating the same content at multiple document levels — section intro, body, section conclusion, document conclusion.
- Trust the reader. Say it once.

**Dead metaphor.** Riding one metaphor through an entire piece (10+ uses of "walls and doors," "the orchestra," "the journey").
- Introduce a metaphor, use it, move on.

**Historical analogy stacking.** Rapid-fire "Apple didn't build X. Facebook didn't build Y. Google didn't build Z."
- Use one well-developed historical example.

**One-point dilution.** Restating the same argument 10 different ways across a long piece.
- Develop the argument with new evidence or perspectives, or make the piece shorter.

**Signposted conclusions.** "In conclusion," "To sum up," "In summary," "Wrapping up."
- End naturally. Competent writing signals its ending without announcement.

**"Despite its challenges..."** Formula that acknowledges problems then immediately dismisses them.
- Engage with the tension instead of waving it away.

## Self-check before finishing

Read your draft and look for:

- More than 3–4 em dashes? Cut some.
- Any "delve," "utilize," "leverage," "robust," "harness," "tapestry," "landscape," "realm"? Replace with plainer words.
- "It's not X — it's Y" pattern? Restate as a direct claim.
- "Here's the thing" / "Here's the kicker" / "Imagine a world"? Cut the framing, keep the content.
- "Let's break this down" / "Let's unpack" / "Let's explore"? Just do the analysis.
- "In conclusion" / "To sum up"? Delete.
- Every bullet starting with bolded text? Vary the formatting.
- One-sentence paragraphs in a row for emphasis? Combine where the emphasis isn't earned.
- Same metaphor used 5+ times? Cut the repetitions.
- "Experts say" / "Studies show" without naming sources? Name them or drop them.
- Any sentence that could be deleted without loss? Delete it.

## Rationalizations — STOP if you think these

| Excuse | Reality |
|--------|---------|
| "The em dashes add rhythm" | Two add rhythm. Twenty signal AI. |
| "'Delve' is a perfectly good word" | It is. It's also statistically AI-flagged. Use "look at" or "examine." |
| "The reader won't notice" | They will. Tropes are noticeable precisely because they cluster. |
| "I need a transition here" | Most "Importantly," / "Notably," transitions can be deleted with no loss. |
| "The conclusion section needs to summarize" | If the body was clear, the summary is redundant. End with the last point worth making. |
| "Bold-first bullets are scannable" | Scannable when used selectively. Uniform bolding = AI signal + reduced scannability. |
| "I'm using the metaphor consistently" | Consistent ≠ good. After 5 uses it's a crutch. |
| "Three parallel sentences sound powerful" | Once. Doing it three times in a row is the formula speaking. |
