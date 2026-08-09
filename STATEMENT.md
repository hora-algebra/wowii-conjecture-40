# STATEMENT — the claim to be proved

Package metadata (not part of the claim): the block below is reproduced
**verbatim** from `paper/paper.tex` lines 553–557 — the statement block of §4,
`\section{The two open lemmas}` — at blob
`54b241e50bafd884c1e48f4d022a00e97b846781`, as frozen at commit `00856f9` (the
last commit touching that file on the sealed `main`, whose head is `64eb3da`).
The whole of `paper/paper.tex` is included in this package, so the block can be
read in its own context. No proof, argument, derivation, partial route, or
recorded attempt at the statement appears anywhere in this package.

---

## Lemma A°, stated exactly

```latex
\begin{problem}[Lemma A$^{\circ}$]\label{prob:A}
Let $G$ be a finite simple bipartite graph, \emph{not necessarily connected},
$S$ a minimum FVS, $H=G-S$, and $e$ a fixed edge of $H$ with capacities as in
Definition~\ref{def:selection}. Prove that the forced incidence core is acyclic.
\end{problem}
```

SHA-256 of the five extracted lines:
`e9e498b2b53a2ef05d5715704084b67b77d2ed665b8e5f23667ea20e3eae0cc8`.

---

## Imported definitions

**None required.** Every defined term and symbol occurring in the statement
above resolves inside a document already included in this package. The closure
was computed mechanically; the resolution table is reproduced here for the
prover's convenience, with file and line provenance.

| term / symbol | resolved in | line |
|---|---|---|
| `FVS`, `\FVS` `=` `\tau` (decycling number, minimum feedback vertex set) | `paper/paper.tex` — "Here `$\FVS$` is the \emph{decycling number} (minimum size of a feedback vertex set…)"; macro at line 22 | 137–138 |
| minimum FVS `S`, `H := G-S` a forest, `G[H\cup X]` | `paper/paper.tex` — `\subsection{The incidence-selection model}` | 245–248 |
| fixed edge `e=(x,y)`, demand, **capacities** `c(h)` | `paper/paper.tex` — `\begin{definition}[Selection model]\label{def:selection}` | 250–257 |
| feasible selection `J`, selected cycle | `paper/paper.tex` — same definition block | 253–256 |
| `\deg_X(h)`, `\rho(X)`, `\delta(X)` | `paper/paper.tex` | 301–304 |
| `ρ`-tight set (`\delta(X)=0`), exposing | `paper/paper.tex` — `\begin{lemma}[Forced $\iff$ tight-set exposed, F1]\label{lem:F1}` | 327–331 |
| **forced** incidence; **forced core** | `paper/paper.tex` — "An incidence `$a=(s,h)$` is \emph{forced} if it belongs to every feasible selection; the \emph{forced core} is the graph of all forced incidences." | 324–325 |
| bipartite, simple, connected, acyclic, edge | standard graph-theoretic terms; used with their usual meaning throughout `paper/paper.tex` | — |

Note on wording: the statement says "forced incidence core"; `paper/paper.tex`
line 325 defines "forced core" as "the graph of all forced incidences". The two
names refer to the same object; §4 uses both spellings (line 536,
`\subsection{Lemma A: the forced core is a forest}`).
