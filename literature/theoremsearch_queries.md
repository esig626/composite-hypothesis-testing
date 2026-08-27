# TheoremSearch query log

For every theorem-level search, record:

- manuscript result being checked;
- date;
- exact query;
- filters used;
- strongest returned candidates;
- candidates inspected in full;
- conclusion and residual uncertainty.

A failed search is evidence only about that query, not proof of novelty.

## Joint Rényi projection / uniform moment antecedent search — 13 August 2026

**Manuscript result:** `thm:dominated-projection-uniform-renyi-inequalities`, together with `lem:complete-feasible-directional-derivative` and its use in projected finite-blocklength achievability.

**Filters intended:** mathematical theorem statements; probability/information theory/statistics; no date restriction; searches in natural-language semantic mode rather than title matching.

**TheoremSearch availability note.** The configured server is `https://api.theoremsearch.com/mcp`.  During this run, the MCP inventory exposed no TheoremSearch method, resource, or resource template: both resource-list operations returned `[]`.  Therefore every query below was submitted to the available MCP inventory but could not be dispatched to a query method.  TheoremSearch returned no result object, candidate identifier, score, or theorem label.  General web-search fallback also returned HTTP 401, while direct scholarly API access was rejected by the environment proxy with HTTP 403.  These are search-infrastructure failures, not zero-result searches.

For clarity, `TS-UNAVAILABLE` below is a local log identifier, **not** a TheoremSearch candidate identifier.

| # | Exact query | TheoremSearch result / score | Candidates retained for source-level comparison |
|---:|---|---|---|
| 1 | `Renyi projection between two convex sets of probability measures closest pair Pythagorean variational inequality` | `TS-UNAVAILABLE`; no score | Kumar--Sason (2016); Csiszár (1975) |
| 2 | `order alpha Hellinger integral maximised jointly over two convex probability classes first order optimality inequalities` | `TS-UNAVAILABLE`; no score | Kumar--Sason (2016) |
| 3 | `Chernoff coefficient closest pair of convex distributions likelihood ratio moment bounds uniform over both sets` | `TS-UNAVAILABLE`; no score | Huber--Strassen (1973); Mosonyi--Szilágyi--Weiner (2022) |
| 4 | `joint projection two convex sets probability densities f-divergence supporting hyperplane inequalities at optimal pair` | `TS-UNAVAILABLE`; no score | Csiszár (1975); Kumar--Sason (2016) |
| 5 | `variational inequalities from an optimal pair maximising integral q^alpha p^(1-alpha) over convex sets` | `TS-UNAVAILABLE`; no score | Kumar--Sason (2016) |
| 6 | `uniform likelihood-ratio inequalities over uncertainty classes least favourable distributions robust hypothesis testing Hellinger transform` | `TS-UNAVAILABLE`; no score | Huber (1965); Huber--Strassen (1973); Fauß--Zoubir--Poor (2021) |
| 7 | `information projection between two convex probability classes rather than projection of one distribution onto one set` | `TS-UNAVAILABLE`; no score | Csiszár (1975) |
| 8 | `convex probability classes minimax distribution pair exponential moments of selected log likelihood ratio` | `TS-UNAVAILABLE`; no score | Huber--Strassen (1973); Fauß--Zoubir--Poor (2021) |
| 9 | `Hellinger transform saddle point robust test two uncertainty sets varying supports` | `TS-UNAVAILABLE`; no score | Huber--Strassen (1973) |
| 10 | `f-divergence nearest pair of convex sets directional derivative probability densities zero sets` | `TS-UNAVAILABLE`; no score | Csiszár (1975); Kumar--Sason (2016) |
| 11 | `alpha divergence projection ordinary mixture convex families versus alpha-convex families Pythagorean theorem` | `TS-UNAVAILABLE`; no score | Kumar--Sason (2016) |
| 12 | `Chernoff information between convex sets attaining pair support function optimality conditions` | `TS-UNAVAILABLE`; no score | Mosonyi--Szilágyi--Weiner (2022) |
| 13 | `least favourable pair likelihood ratio may be zero or infinity non-common supports composite testing` | `TS-UNAVAILABLE`; no score | Huber (1965); Huber--Strassen (1973) |
| 14 | `Huber Strassen capacities least favourable distributions likelihood ratio stochastic ordering Hellinger integrals` | `TS-UNAVAILABLE`; no score | Huber--Strassen (1973); Fauß--Zoubir--Poor (2021) |
| 15 | `Csiszar I-projection two sets closest distributions variational inequality extended likelihood ratio` | `TS-UNAVAILABLE`; no score | Csiszár (1975) |
| 16 | `minimise Renyi divergence jointly over P in convex null class Q in convex alternative class` | `TS-UNAVAILABLE`; no score | Kumar--Sason (2016); Mosonyi--Szilágyi--Weiner (2022) |
| 17 | `one-sided derivative of Hellinger integral at density with zeros feasible mixture direction` | `TS-UNAVAILABLE`; no score | No separately identifiable theorem candidate |
| 18 | `composite hypothesis testing joint Renyi minimizer gives one test uniform exponential moment bounds` | `TS-UNAVAILABLE`; no score | Huber--Strassen (1973); Mosonyi--Szilágyi--Weiner (2022) |

### Candidates inspected and disposition

| Local candidate identifier | Source / result inspected | Disposition |
|---|---|---|
| `KS2016-PROJECTION` | Kumar and Sason, Rényi projection/Pythagorean theorems on \(\alpha\)-convex sets; exact theorem number unavailable | `PARTIAL ANTECEDENT` |
| `C1975-IPROJECTION` | Csiszár, I-projection existence and Pythagorean geometry; exact theorem number unavailable | `RELATED BUT NOT ANTECEDENT` |
| `H1965-ROBUST-PRT` | Huber, robust probability-ratio test | `PARTIAL ANTECEDENT` |
| `HS1973-CAPACITY-NP` | Huber and Strassen, capacity least-favourable/minimax Neyman--Pearson result; exact theorem number unavailable | `PARTIAL ANTECEDENT` |
| `FZP2021-SURVEY` | Fauß, Zoubir, and Poor, least-favourable distributions and stochastic-order criteria | `RELATED BUT NOT ANTECEDENT` |
| `VEH2014-THM17` | van Erven and Harremoës, Theorem 17 (continuity), plus general Rényi properties | `RELATED BUT NOT ANTECEDENT` |
| `MSW2022-COMPOSITE-EXPONENTS` | Mosonyi, Szilágyi, and Weiner, composite Chernoff/Hoeffding exponent results; exact theorem numbers unavailable | `RELATED BUT NOT ANTECEDENT` |

**Conclusion:** No equivalent result was located in the searches performed; novelty remains unresolved.  The principal residual uncertainty is caused by the unavailable theorem-search/source-retrieval infrastructure and by the possibility that a two-set closest-pair variational statement is embedded under different terminology in convex analysis, robust statistics, or the older Hellinger-transform literature.
