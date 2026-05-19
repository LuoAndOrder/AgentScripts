---
name: readable-python
description: Use when writing or modifying any Python code, including small local edits, single-line bug fixes, refactors, and new features. Applies on every Python change, not only large restructures.
---

# Readable Python

**Readability is attention allocation.** Code has *foreground* (domain logic) and *background* (plumbing). Make foreground prominent and background invisible, so the reader spends cognitive load only on what's load-bearing.

## Rule scope

Not every rule applies with equal force on every edit.

- **Apply on every edit**: rules 1, 2, 3, 5, 6, 7, 9, 12 — renames, naming, hoisting, parameter order, docstring hygiene, method placement. Cheap to do inline, even on a three-line bug fix.
- **Flag as review opportunities**: rules 4, 8, 10, 11 — extractions, module splits, TypedDict introductions, class extractions. These are structural changes; don't silently do them in an unrelated bug fix. Do them when the task is a refactor, a new feature, or when the cost of leaving the smell matches the size of the current change.

These rules describe the readability **ceiling**. Existing code that doesn't meet them all isn't broken; it's an opportunity. New code you write should aim for the ceiling where scope allows.

## Rules

### 1. Collapse background, expand foreground

Background (transforms, accumulators, glue): compress. Use comprehensions, `.extend()` / `.update()`, capture `setdefault`'s return instead of setdefault+index, inline single-use variables.

Foreground (domain logic, invariants): give it its own named function, a clear signature with types, and room to breathe. Shorter is better for background; **clearer** is better for foreground even at the cost of lines.

**Background is plumbing, not silent work.** Before collapsing a per-iteration loop into `.extend()`, `.update()`, or a comprehension, verify the loop body isn't doing implicit work. The classic trap is unpacking: `for a, b in rows: list.append((a, b))` is often doing type coercion (e.g. SQLAlchemy `Row` → real `tuple`) that `.extend(rows)` silently drops. Other hidden work: filtering inside the body, triggering lazy-loads via attribute access, per-item validation, side effects on each iteration. If the loop body looks like pointless plumbing, pause and ask whether the iteration itself is doing something load-bearing. When in doubt, run the type checker — if `.extend()` produces a type error that the explicit loop didn't, the loop was doing work.

### 2. Side effects are an anti-pattern — name them when justified

Prefer pure functions that return values. Side-effect functions read as no-ops at the call site and hide mutation from the type system.

**"Side effect" means logic, not observability.** A function that emits a metric, writes a log line, or pushes a span is *not* doing a side effect for the purposes of this rule — that's observability/debugging, not behavior the caller's correctness depends on. If you removed every `metrics.put_metric(...)` and `logger.info(...)` call, the function's contract would be unchanged. Don't rename `_build_candidate_urls` to `_build_candidate_urls_and_record_unmapped` because it logs warnings; that's noise.

A side effect for this rule is something that mutates state the caller (or some other reader of the world) will observe through code paths other than the return value: dict mutation, DB writes, file I/O, in-memory cache updates, environment manipulation, queue puts. Those need the naming discipline below.

If a side effect is justified (e.g. tight inner-loop accumulator where returning+merging per iteration is wasteful), **the name must signal mutation**: `merge_into_`, `add_to_`, `append_to_`, `record_`, `mark_`, `update_`. Never use observation verbs (`traverse`, `inspect`, `check`, `compute`) for mutating functions.

**Mutating functions return `None`, never the mutated parameter.** Mutate-and-return is a confusion trap — the caller cannot tell at a glance whether to use the return value or trust that the argument was updated. Pick one: either return the result (pure function) or mutate in place (returns `None`). Don't blur the line.

### 3. Parameter order communicates meaning

After `self`:
1. **Context carrier first** — `db_session`, `ctx`, `config`. Burying it invites future edits to create a new session instead of threading the existing one.
2. **Primary operand next** — the thing acted on. For side-effect functions, the mutated parameter.
3. **Grouped by role** — conceptually-paired params adjacent.

### 4. Extract by change axis; stop before tuple returns or duplicate I/O

Extract — at the function *or module* level — when two units of logic evolve for different reasons (query shape vs pagination strategy; DB schema vs S3 format). Stop when further splits would force tuple returns of tightly-related values, duplicate I/O, or parameter lists that only exist to re-thread state. The main method becomes a 3–5-step table of contents.

**A wider signature is NOT the same as "threading state across artificial boundaries."** If every parameter a helper takes is load-bearing to the helper's job — it reads or mutates that value — the signature can grow to 5, 6, 7 parameters and the extraction is still honest. The anti-pattern is parameters that exist only to shuttle state *through* the helper without being used. If you're on the fence about extracting and the blocker feels like "too many parameters," ask: would the helper need each of these if called from a *different* context? If yes, the signature is honest. Don't reject a valid extraction just because the argument list is long.

**Corollary: don't use tuple returns as an escape hatch.** If you find yourself wanting to return `(dict_a, dict_b)` from a helper because both are needed downstream, the choice is *not* between "tuple return" and "don't extract." The third option is "pass both dicts in as parameters that the helper mutates or reads" — often the cleanest answer when the two outputs are populated together and consumed together.

**Module-level application.** The same change-axis test applies to files. A module holding three axes (DB queries + S3 serialization + output formatting) is a read trap — a reader investigating one concern scrolls past the other two. Split when the concerns have historically changed for different reasons, not when they *could* in theory. Bias toward keeping code together until divergence is real — over-splitting produces dumping-ground files (`models.py`, `utils.py`) and forces navigation between arbitrary boundaries.

### 5. Names describe shape and outcome

- **Dicts: `key_to_value`, not `value_by_key`.** `package_version_to_reachable_definitions` exposes shape; `reachable_definitions_by_package_version` reads like a filter.
- **Methods: describe outcome, not mechanism.** `_merge_call_graph_symbols` (what changes) beats `_traverse_python_call_graph` (what the function internally does).
- **Parameter names: shape usually wins over role.** A dict parameter named `accumulator` or `result` describes its *role* (what the function does with it); a name like `package_to_version_to_count` describes its *shape* (what it holds). Default to **shape** — it lets a reader understand the parameter without reading the function body. Use role names only when the mutation verb + position (e.g. `merge_into_x(..., x)`) already make the structure obvious, or when the shape is trivial (`items`, `records`).
- **Domain nouns beat generic storage words.** Once a layer knows it's dealing with `Vulnerability` objects, stop calling them `record`/`entry`/`item`/`row`. A reader holding "record = vulnerability" in their head pays cognitive rent on every line. `_coerce_record_types` tells you nothing about what it coerces; `_coerce_vulnerability_types` tells you what. Generic storage words stay correct at storage-layer boundaries (the DAO returning `records` is fine) and in genuinely generic helpers (`chunked(items)`). Once the domain is in scope, use the domain word.
- **Mechanism vocabulary stays at the mechanism layer.** The verb that produces a result lives at the producer; once the result crosses into a data class, field, consumer method, or downstream local variable, name it by what it **is**, not how it was produced. A type called `ProbeHit` becomes `ReleaseFile`; a field `probe_hits: tuple[...]` becomes `release_files`; `_persist_probe_results` becomes `_persist_release_files`; a loop variable `hit` becomes `release_file`. The producer's verb (`probe`, `scrape`, `parse`, `fetch`, `extract`, `derive`) earns its keep at the layer where the action happens (the prober, the parser) and in observability of that action (metrics named `*Probed*`, log lines saying "HEAD probe failed", prose docstrings describing how state was produced). It does not earn its keep at the consumer layer — by the time we're persisting the result we already have the file, and forcing every reader to translate "probe hit = file confirmed via HEAD" is cognitive rent on every line where the noun appears. **Substitution test:** mentally swap the verb-flavored name for the bare domain noun (`the file` instead of `the hit`). If reading flows better, the verb was contagion. Sibling to the previous bullet — both replace the wrong noun with the right one; "domain nouns beat generic storage words" targets *generic storage* nouns (`record`, `entry`), this bullet targets the *producer's verb* leaking past its boundary.
- **Symmetric pair naming makes the axis of difference visible at the signature.** `export_to_s3` + `export_from_snapshot` forces a reader to open the first function to learn it's a DB read. `export_from_db_to_s3` + `export_from_snapshot_to_s3` puts the `(source → sink)` pair at the name level and makes grep'ing for all export paths trivial. Apply when you have a genuine pair (`save_X`/`load_X`, `read_Y`/`write_Y`, `to_dto`/`from_domain`). Don't manufacture symmetry for unrelated functions.
- **Interaction with rule 6.** Rule 6 strips context already implied by the enclosing scope (filename, class, parameter). The two "wrong noun → right noun" bullets above *replace* the wrong noun with the domain word: generic storage nouns (`record`, `entry`) and producer verbs (`probe_hits`, `scrape_results`) both get swapped for the domain noun. In a vulnerability-export file, `vulnerability_record` collapses to `vulnerability` — not to `record`. Strip context, keep the domain.

### 6. Strip redundant prefixes

If context (filename, enclosing class, a parameter already in scope) constrains a variable, don't also prefix the variable with that context. In a Python-only file, `python_callgraph` → `callgraph`. If `language` is a parameter, don't bake `python_` into the names below it.

### 7. Hoist constants to the top of the function

```python
def process(self, partition):
    ecosystem = SafetyEcosystem.PYPI
    language = Language.python
    ...
```

Three benefits: scope clarity, surfaces genericity (easy future refactor to parameterize), and prevents the cognitive speed-bump of a surprise `Language.python` literal mid-method.

**Env-var reads belong inside the function, not at module load.** `X = os.environ.get("X")` at module level silently binds to `None` and crashes downstream with a confusing `NoneType` error. It also runs at import time, which can fail test collection before any test runs. Read inside the function that needs the value, and raise explicitly when required:

```python
# Anti-pattern — silent None at module load
S3_BUCKET = os.environ.get("S3_BUCKET")

# Preferred — read at use, fail loud
def upload(...):
    bucket = os.environ.get("S3_BUCKET")
    if not bucket:
        raise OSError("S3_BUCKET environment variable is required")
```

Exception: env vars that genuinely need to be read at import time (e.g., `LOG_LEVEL` for a module-level logger config) are fine at module scope, provided the read has a default and isn't treated as non-None downstream.

### 8. Parameterize what varies — even for a single caller

If a method has a hardcoded value on an axis that could legitimately vary (language, ecosystem, format), promote it to a parameter. Pairs with rule 7: the top-of-function constant in the caller becomes the parameter the method accepts.

### 9. Horizontal density within the project's existing line-length

Use the room already set by the project's `ruff` config for logs, call sites, and type annotations that fit cleanly. **Do not modify the project's line-length** to make things fit — that's a project-wide decision. Don't force single-line signatures dogmatically; long parameter lists with types often read better vertically.

**Docstrings: one line of purpose, not a prose restatement of types.** When the signature is typed, `Args:/Returns:/Raises:` blocks restate what mypy already knows. The foreground a docstring should carry is *why the function exists and any non-obvious invariant*. Everything else is boilerplate — common in AI-generated code and almost always dead weight.

```python
# Before — 15 lines restating the signature
def export_to_s3(self, db_session, ecosystem=None, target=..., batch_size=500):
    """
    Export vulnerabilities to S3 in Safety CLI JSON database format...
    Args:
        db_session: Database session to use for queries
        ecosystem: Optional ecosystem filter...
    Returns:
        Dict containing export results:
            - vulnerabilities_exported: ...
    Raises:
        ClientError: If S3 upload fails
    """

# After — what and why, one line
def export_from_db_to_s3(...) -> JsonDBExportResult:
    """Export vulnerabilities to S3 in Safety CLI JSON database format using streaming writers."""
```

The rule is about **redundancy**, not length. Public-API / library code that appears in `help()`, IDE tooltips, or auto-generated docs legitimately needs richer docstrings. Internal code does not.

### 10. Types at boundaries

When a return value or public parameter has a fixed, known shape, name the shape. `dict[str, Any]` and `dict[str, T]` with unknown keys make the signature unreadable — the reader has to scan the body to learn the structure.

Pick the right tool:
- **TypedDict** — when the value is genuinely a dict and keys are fixed.
- **NamedTuple** — when positional access and immutability fit the use case.
- **dataclass** — when you want defaults or mutability without validation overhead.
- **Pydantic model** — when the boundary needs validation (external input, config).

```python
# Before — reader opens the body to learn the shape
def read_manifest(...) -> dict[str, str]: ...
def export(...) -> dict[str, Any]: ...

# After — shape at the signature
class JsonDBExportSnapshotManifest(TypedDict):
    timestamp: str
    vulnerabilities_key: str
    severities_key: str

class JsonDBExportResult(TypedDict):
    vulnerabilities_exported: int
    export_size_bytes: int
    s3_key: str
    unique_packages: int
```

Bonus: typos like `manifest["records_key"]` become compile-time errors after a rename to `vulnerabilities_key`.

**`dict[str, Any]` stays correct when the shape is genuinely dynamic** — parsing arbitrary external JSON (webhooks, user uploads), opaque metadata passthrough (`Metadata={"beta": "true"}` to boto3), Lambda `event: dict[str, Any]` handlers where the shape varies by invocation source. The test: *do I know the keys at this boundary?* If yes, name the shape. If no, `Any` is honest.

**Where TypedDicts live.** If the project already has a `types.py` (or similar centralized types module), define TypedDicts there rather than colocating with the function that returns them. Types are a shared vocabulary — scattering them by call site means readers and future callers have to grep to find what shape a function returns. One canonical location makes the type graph discoverable. Types tightly scoped to one private helper (single file, never exported) can stay colocated; anything that crosses a module boundary belongs in the shared types module.

**Enum-keyed dicts over string-keyed dicts when the key set is finite and known.** `dict[Target, bool]` beats `dict[str, bool]` when `Target` is already defined. Pydantic coerces JSON string keys to enum on load; handler code does typed `.get(config.target, default)` lookups; missing-key drift between enum and config becomes a type error instead of a silent `None`. Not applicable when keys are user-supplied or open-ended.

### 11. Shared leading args → a class

When a cluster of module functions all take the same 2–3 leading args (e.g., `(s3_client, bucket, prefix)` appearing across five or more functions), consider a class that captures them once in `__init__`. Call sites read as *what the object does* (`snapshot.read_manifest()`), not *where it lives* (`read_manifest(s3_client, bucket, prefix)`).

```python
# Before — seven functions, same three leading args
def write_records(records_iter, s3_client, bucket, key): ...
def read_records(s3_client, bucket, key): ...
def write_severities(severities_dict, s3_client, bucket, key): ...
def read_severities(s3_client, bucket, key): ...
def write_manifest(s3_client, bucket, prefix, timestamp, ...): ...
def read_manifest(s3_client, bucket, prefix): ...

# After — one class owns the shared context
class JSONDBSnapshotService:
    def __init__(self, s3_client: S3Client, bucket: str, prefix: str): ...
    def read_manifest(self) -> Manifest: ...
    def read_vulnerabilities(self, manifest: Manifest) -> Iterator[...]: ...
    def build_snapshot(self, vulnerabilities, fetch_severities, timestamp): ...
```

**Acknowledge alternatives before reaching for a class:**
- **`functools.partial` / closures** — lighter than a class when the functions are pure and the shared args are pure config.
- **A `@dataclass` config object passed as one parameter** — keeps functions pure; reduces signature width without adding instance state.
- **Module-level singletons** — rare, but correct for true application-scoped clients.

Class is the right choice when the shared args form a **natural thing** (an "S3 snapshot location", a "DB query context"). If they're coincidentally-shared configs with no common identity, a dataclass or closure is cleaner. Classes carry instance state and test overhead; use them when the modeling earns it.

### 12. Method order mirrors the call tree

Inside a class (or a module of related top-level functions), order methods to match the call tree of the entry point. Pick **BFS** (every directly-called method first, then helpers-of-helpers grouped after) or **DFS** (each method's helpers immediately below it before the next sibling). Apply one consistently — don't mix.

**Why.** A reader scrolling top-to-bottom is reading the program in execution order. Random ordering — chronological by when each method was added, alphabetical, "all the persistence methods at the bottom because they're boring" — forces a grep or jump-to-definition for every call, which breaks comprehension flow. If `_process_package` calls `_get_known_repositories`, then `_fetch_packages_across_repositories`, then `_persist_fetched_packages`, those three should appear in that exact order immediately after `_process_package` — not scattered through the file by historical accident.

**DFS vs BFS.** Pick based on the shape of the work:

- **DFS** (default for pipelines): each phase's orchestrator method is followed by its own helpers before the next phase begins. Best when the entry method is a linear pipeline and each phase has its own self-contained helper set. Reads as a series of self-contained sections.
- **BFS** (default for flat APIs): all directly-called methods first (siblings together), then the next layer of helpers, then the next. Best when the top-level methods are siblings in a flat API (CRUD class with `create`/`read`/`update`/`delete`) and helpers are shared across them.

When in doubt, prefer DFS. Pipelines are more common than flat APIs in service code, and DFS keeps the "fetch + persist" pattern visually adjacent within each phase.

**Edge cases.**

- **Helper called from two siblings** (e.g., a static helper used by both the fetcher and the persister of the same phase): place at **first-DFS-visit position**. The second caller back-references it. Don't duplicate; don't lift it out unless the call set crosses non-adjacent phases.
- **Adding a new method to existing code**: place it where the call tree puts it, not at the end. "End of file" is not a valid position; it's a refactoring debt your future-self pays.
- **Existing class is incoherently ordered**: reorder the cluster you're touching as part of the current change. Don't reorder methods you don't otherwise need to touch — that's noise on the diff.

```python
# DFS for a pipeline class — each phase orchestrator followed by its helpers.
class MavenPackageProcessor:
    def process_package(self, name): ...
    def _process_package(self, group, artifact): ...

    def _get_known_repositories(self, db): ...

    def _fetch_packages_across_repositories(self, ...): ...
    def _process_package_for_repository(self, ...): ...
    def _fetch_package_metadata(self, ...): ...
    def _persist_fetched_packages(self, ...): ...
    def _persist_package(self, ...): ...

    # ... versions phase, probe phase ...
```

**Don't narrate the structure.** If the order is correct, the reader sees the call sequence by scrolling. Adding `# Phase 1`, `# === fetchers ===`, or a class docstring saying "method order below mirrors the call tree (DFS)" is restating what the order already shows. Same instinct as Rule 9's "docstring restates the signature" trap, applied to structure. Phase-marking inline comments inside the *orchestrator method body* (e.g. `# Phase 2` inside `_process_package` between `with` blocks that handle different phases) are fine — those mark non-obvious transitions in linear code, not section dividers between method definitions.

**Module-level helpers in the same file.** If the module also has top-level `_helper(...)` functions used only by the class, the same call-tree principle applies between the module helpers and the class — but the natural Python layout is "module helpers above the class, in the order they're first encountered by a reader walking the class." Don't try to interleave module functions with class methods.

### 13. Exceptions over multi-state sentinels

A function that needs to distinguish more than one outcome should return a richer type, or raise. Don't extend a binary return into a tri-state by tacking on `| None` to encode "I couldn't compute the answer." That overloads the return type with two unrelated jobs (the answer + an error channel) and silently drops every detail of *why* the answer wasn't available.

```python
# Anti-pattern — tri-state hides the diagnostic
def head_object_exists(self, key: str) -> bool | None:
    try:
        s3().head_object(Bucket=self.bucket, Key=key)
    except ClientError as exc:
        if exc.response.get("Error", {}).get("Code") in {"404", "NoSuchKey", "NotFound"}:
            return False
        return None  # auth, throttle, transport — ALL collapsed to None, exception detail gone
    except BotoCoreError:
        return None  # transport detail also discarded
    return True

# Better — raise; caller catches with full detail
def check_object_presence(self, key: str) -> bool:
    try:
        s3().head_object(Bucket=self.bucket, Key=key)
    except ClientError as exc:
        if exc.response.get("Error", {}).get("Code") in {"404", "NoSuchKey", "NotFound"}:
            return False
        raise
    return True

# Caller has the full diagnostic
try:
    present = downloader.check_object_presence(key)
except (ClientError, BotoCoreError):
    metrics.put_metric("S3HeadObjectError", 1.0, ...)
    logger.warning(f"head_object error for {key}", exc_info=True)  # exc detail preserved
    continue
```

The "but the caller has to handle None anyway" defense is its own indictment: if every caller treats None the same as the exception path, the sentinel is a dishonest exception. Use the actual exception.

**Optional generally.** `Optional[T]` (or `T | None`) is honest when there is exactly one well-defined "no value" state — e.g., a lookup that returns `None` for "not found" with no other failure modes. It becomes dishonest the moment None is paired with multiple distinct conditions (auth-error, throttle, transport-flake, parse-failure). Each of those conditions carries diagnostic information the caller will want to log or branch on; folding them into a single None discards it.

**Alternatives when raising is awkward:**

- **Discriminated union** — `Hit(metadata)` | `Miss()` | `Unauthorized(reason)` | `Throttled(retry_after)`. Verbose but every return state carries its own data. Useful when callers branch richly on the outcome.
- **Result/Either type** — `Result[T, ErrorClass]`. Honest when the caller is structurally pattern-matching every error case.
- **Exception** — almost always the right answer in Python. The traceback is a feature, not a cost.

Don't use:
- `bool | None` to encode `True / False / "I don't know"`
- `T | None` where None means "any of several errors" rather than one specific absence
- A sentinel value (`-1`, `""`, `(False, None)`, `MISSING`) to encode "computation failed"

The same rule applies to docstrings: if you find yourself defending "we considered raising but went with a sentinel because callers can handle it," delete the defense and raise instead.

**Distinct from Optional-as-"didn't act."** A function that genuinely chose not to do anything (e.g., `try_short_circuit_via_s3` returning `None` when no S3 hit was found, signalling "fall through to the upstream path") is honest — None there means "no action taken, no data produced," not "I encountered N possible errors." That's a single well-defined absence.

## Example: outcome of applying all rules

```python
# Hoisted constants; clear parameter order; outcome-oriented name; mutated param first.
def _merge_call_graph_symbols(
    self,
    reachable_symbols: dict[str, ReachableSymbolDTO],
    language: Language,
    vulnerable_release: PackageRelease,
    reachable_definition: ReachabilityDefinition,
    reachable_file: ReachabilityFile,
    callgraph: Graph,
):
    reachable_vertices = callgraph.symbol_reachable_symbols(...)
    for v in reachable_vertices:
        merge_reachable_symbols(reachable_symbols, ReachableSymbolDTO(..., language=language, ...))
```

## When refactoring existing code

Apply these rules with the same willingness to restructure that you'd have when writing fresh. **Refactoring is not lower-stakes than greenfield writing** — the reader who lands on the result can't tell whether the code was written from scratch or the product of a refactor. They judge what they see.

Specifically, when refactoring:

- Don't stop after the mechanical wins (renames, hoisting, parameter reorder) if the rules call for a structural change (extraction, flattening, restructuring). The mechanical changes are the easy part; the structural ones are where the readability gains compound.
- If you notice `process()` or another method is doing three conceptually-distinct things in sequence, extract — even if it requires a wider signature or passing dicts in as mutable parameters. "The existing method was one blob, so my refactor should also be one blob" is refactoring inertia, not judgment.
- If applying the rules would make the diff noisier than you're comfortable with, that's about code churn, not correctness. Flag it and ask — don't silently do the half-measure version.

### PR scope can override review-scope rules

When you're already inside a large refactor PR, applying every readable-python opportunity to the surrounding code can inflate the diff past what reviewers can absorb. The trade-off:

- **Apply readable-python** → tighter code, but reviewers have to track refactoring changes alongside functional changes, and the functional changes get harder to audit.
- **Skip readable-python on the unchanged surrounding code** → keep the PR diff focused on the functional change, but leave a known-suboptimal pattern in place.

This trade-off is real and not always resolvable in favor of "apply the rule." On a big PR, optimizing for reviewer cognitive load often beats optimizing for code structure — a refactor opportunity that would have been a clean win on a small PR becomes a distraction on a 1500-line PR.

**Decision rule**: when the refactor opportunity is in code that's adjacent to (but not part of) your functional change, surface the trade-off to the human operator. Don't decide unilaterally to apply or skip. The reviewer's bandwidth is part of the optimization function and only the human knows their team's tolerance.

This applies to **review-scope rules** (rule 4 extractions, rule 8 parameterization, rule 10 TypedDict introductions, rule 11 class extractions). The **every-edit rules** (1, 2, 3, 5, 6, 7, 9, 12) still apply to lines you actually touch — those are cheap, mechanical, and don't add diff bulk.

## Rationalizations — STOP if you think these

| Excuse | Reality |
|--------|---------|
| "This is just a small edit; the rules don't apply" | The every-edit rules (1, 2, 3, 5, 6, 7, 9) apply. Structural rules are scoped to the size of the task. |
| "Renaming the surrounding code is out of scope" | Correct — don't rename untouched code. But the code you *are* writing follows the rules. |
| "The existing file uses `python_` prefixes; I'll match the style" | The existing file is wrong. Your new code follows the rules; flag the surrounding code for separate cleanup if appropriate. |
| "`setdefault` + index is fine, it's just two lines" | Two lookups when one suffices = background noise stealing attention. Capture the return. |
| "This function mutates but it's called in a loop so it's fine" | Loop-accumulation justifies the side effect. It does not justify hiding it. Rename to `merge_into_*` / `add_to_*`. |
| "Putting `db_session` first would require reordering other args" | Yes. Do it. Call sites update mechanically; the structural signal matters long-term. |
| "The dict name is fine, types document the shape" | Types document the type. The name documents how the dict is *used* (key → value lookup). Both matter. |
| "I'll leave the hardcoded `Language.python` since this file is Python-only" | The file being Python-only is exactly why the literal is noise. Hoist it; the body reads smoother. |
| "Extracting this helper is over-engineering" | Maybe. Check the independent-change-axis test. If the inner logic changes for a different reason than the outer, extract. |
| "A tuple return would make this cleaner" | Almost always a trap. Ask whether the two outputs belong together. If yes, don't extract *or* pass both dicts in as mutable parameters. |
| "Extraction would require 5+ parameters, so leave it inline" | 5+ load-bearing parameters is an honest signature. Only decline extraction if parameters exist purely to shuttle state without being used. |
| "I'll collapse this `for a, b in rows: list.append((a, b))` into `list.extend(rows)`" | The unpacking was coercing `Row` objects into real tuples. `extend(rows)` puts `Row` objects into a `list[tuple[...]]` — type error. Keep the loop when the body is doing implicit work. |
| "The original method was one big blob; my refactor matching that is fine" | Refactoring inertia. The reader of the result can't tell it used to be worse. Hold the refactor to the same bar as a fresh write. |
| "I'll keep calling them `records` since the DAO returns records" | The DAO's generic noun is correct at its boundary. Once the layer above knows it's a vulnerability, use the domain noun. |
| "I'll keep calling them `probe_hits` / `scrape_results` since that's how they were produced" | The producer's verb is correct at the producer (and in metrics/logs that observe the producer). The consumer layer just sees release files / pages — name them that. Producer verbs are contagion the moment they cross into a data class, field, or consumer method. |
| "`dict[str, Any]` is fine — the shape is in the docstring" | Docstrings rot; TypedDicts don't. The signature is where the reader looks first. |
| "Strings are fine as dict keys, I'll add a comment listing the valid values" | The enum is the comment — and type-checked. |
| "This module's three concerns are related — splitting feels like overkill" | Related ≠ same change axis. Check history before splitting, *and* before refusing to. |
| "`Args:/Returns:/Raises:` is the standard format, I'll keep it" | Typed signatures make the sections redundant. Keep what isn't restatement. |
| "These seven functions all take `(s3_client, bucket, prefix)` but they're pure, so module functions are fine" | Repeated leading args across a function cluster are repeated plumbing. Capture once in a class or config object; methods take what varies. |
| "I'll just append the new method at the bottom of the class — it's where I happened to be editing" | Method order encodes the call tree. Appending to the end forces every future reader to grep for callees instead of reading top-to-bottom. Place the new method where its caller's call sequence puts it. |
| "The class is already disordered, no point reordering one method" | If you're already restructuring the cluster you're touching, reorder it. The diff cost is one-time; the readability cost compounds with every future reader. |
| "I'll add `# Phase 1` / `# === fetchers ===` comments so the structure is obvious" | If the method order is correct, the structure *is* obvious — the reader sees it by scrolling. Section banners narrating what the names already say are noise. Same family as docstring restatements (rule 9). |
| "I'll return None instead of raising — the caller can handle it more cleanly" | If "the caller can handle it" means "the caller catches None and treats it identically to an exception," the sentinel is a worse exception. Raise. The traceback carries the diagnostic; None carries nothing. (Rule 13.) |
| "Tri-state `bool \| None` is fine — the docstring explains what None means" | The docstring explains what was discarded. The exception path carries `exc.response`, the request id, the endpoint, the stack — all visible to the caller's logger. None erases that. (Rule 13.) |
| "I'll defend the sentinel-vs-raise choice in the docstring" | If the docstring needs to defend a rejected design, the design is wrong. Delete the defense and raise. (Rule 13 + Rule 9.) |

## Red flags — self-check before finishing

- Any `_traverse_`, `_inspect_`, `_check_`, `_compute_` method whose last parameter is a dict and whose body does `dict[key] = ...`? Rename + reorder.
- Any variable named `foo_by_bar` where it's a dict? Rename to `bar_to_foo`.
- Any `python_`-prefixed variable in a file that's already Python-specific? Strip the prefix.
- Any hardcoded `Language.X` / `Ecosystem.Y` deep in a method that could plausibly take it as a parameter? Hoist and/or parameterize.
- Any `db_session` / `ctx` / `config` parameter in position 3+ (after `self`)? Move to first.
- Any helper whose only output is two tightly-related values returned as a tuple? Reconsider — probably should stay inline.
- Any `dict[str, Any]` in a public signature where the keys are actually known? Define a `TypedDict` / `NamedTuple` / dataclass.
- Any `dict[str, T]` where the keys come from a finite, known set? Use the enum as the key type.
- Any module with 5+ functions sharing the same 2–3 leading args? Candidate for a class (or a config dataclass passed as one parameter).
- Any module-level `os.environ.get(...)` without a default that gets treated as non-None downstream? Inline the read and raise on missing.
- Any multi-line `Args:/Returns:/Raises:` block paired with a fully-typed signature? Collapse to one line of purpose; keep only the non-obvious semantics.
- Any generic storage noun (`record`, `entry`, `item`, `row`) at a layer where the domain noun is already known? Rename to the domain word.
- Any data class, field, consumer method, or local variable carrying a producer's verb (`ProbeHit`, `probe_hits`, `_persist_probe_results`, `scrape_results`, `parse_output`) past the producer's boundary? Replace with the domain noun (`ReleaseFile`, `release_files`, `_persist_release_files`). The verb stays at the prober/scraper/parser and in observability of that action; consumers see the noun.
- Any asymmetric pair of related operations (`save_X` / `load_from_Y`, `export_to_s3` / `export_from_snapshot`)? Fix the asymmetry so the `(source → sink)` axis is visible at the name.
- Any file whose concerns have historically changed at different times for different reasons? Candidate for a module split by change axis.
- Any class where reading top-to-bottom doesn't follow the call sequence of the entry method? Reorder DFS-by-call-tree (or BFS for flat APIs).
- Any `# Phase N` / `# === ... ===` banners between method definitions, or a class docstring describing the method ordering? Delete; the order is the documentation.
- Any `bool | None` return where None encodes "error/transient/unknown" rather than one specific absence? Anti-pattern — raise instead. (Rule 13.)
- Any `T | None` where None is paired with multiple distinct error conditions, each with its own diagnostic? Replace with raise + exception, or a discriminated union of named result types. (Rule 13.)
- Any docstring that explains *why we didn't raise* rather than what the function does? The defense is the smell. Delete the defense and raise. (Rule 13 + Rule 9.)