# Sources checked for the 15 September revision

The user requested a shorter, drier related-work section during revision.
The main text therefore retains only two short paragraphs on motivation
and nearby methods. The fuller checks below document what was consulted;
they are not an additional field-history section for the paper. Earlier
mathematical source checks remain in ../source-notes.md.

Primary materials were read at the depth stated below. This is neither
an exhaustive history nor a claim to have audited every source's proofs.
Downloaded PDFs remain in the ignored local build cache, not the distributed
source archives. source-inputs.json records their URLs and byte digests.

- **MPTPChallenge**, Josef Urban and Geoff Sutcliffe, designed 2006,
  competition 2007: https://josefurban.eu/MPTPChallenge/ . Read the rules,
  problem description and results page. The 252 problems are related
  first-order translations from Mizar. The overall allowance is
  252 × 300 CPU seconds per division, with internal problem scheduling,
  reuse of results and system retuning permitted. This is not a 48-hour
  wall-clock protocol. The motivation for the present experiment comes
  from Urban's account to the authors, not an inference from the website.
- **MaLARea: a Metasystem for Automated Reasoning in Large Theories**,
  Josef Urban, ESARLT 2007, CEUR volume 257:
  https://ceur-ws.org/Vol-257/05_Urban.pdf . Read abstract, introduction
  and Sections 2.1–2.2. The original loop alternates E/SPASS proofs with
  SNoW naive-Bayesian premise learning, resetting small axiom/time limits
  after a new solution and expanding them after unsuccessful rounds.
  This source itself acknowledges earlier learning in E; no exclusive
  claim that MaLARea originated all proof-learning feedback is made.
- **Machine Learner for Automated Reasoning 0.4 and 0.5**, Cezary
  Kaliszyk, Josef Urban and Jiří Vyskočil:
  https://doi.org/10.29007/shxj . Read the author's preprint introduction,
  system and competition sections, and checked the published EasyChair
  record and PDF at https://easychair.org/publications/paper/W7 . The
  publication is EPiC 31, 60–66 (2015), for the PAAR-2014 workshop.
  The paper discusses the learning/proving loop, countermodels, premise
  strategies, earlier LTB settings, and Turing100. The latter supplied
  1,000 preparation problems with 13,455 proofs and 400 competition
  problems. The manuscript needs only the methodological description.
- **CASC-J6 proceedings**, Geoff Sutcliffe, 2012:
  https://tptp.org/CASC/J6/Proceedings.pdf . Read the title/abstract,
  division rules and batch-execution sections (especially 2.1 and 3.2).
  Mizar@Turing100 permits unordered attempts and revisiting under a shared
  wall-clock limit without a per-problem limit. Ordinary LTB uses ordered
  batches. These are distinct protocols; a single uniform characterization
  of every LTB competition would be inaccurate.
- **GRUNGE: A Grand Unified ATP Challenge**, Chad E. Brown, Thibault
  Gauthier, Cezary Kaliszyk, Geoff Sutcliffe and Josef Urban, CADE 2019,
  LNCS 11716, 123–141: https://doi.org/10.1007/978-3-030-29436-6_8 .
  Read the abstract and introduction of arXiv:1903.02539v2 and checked
  bibliographic metadata. This translates HOL4 material into several
  first-order/higher-order and typed/untyped formalisms, with opportunities
  to combine proving and learning. No detailed result comparison is used.
- **CASC-J10 proceedings**, Geoff Sutcliffe, 2020:
  https://tptp.org/CASC/J10/Proceedings.pdf . Read the title/abstract,
  LTB problem specification and batch rules. Eight HOL4-derived versions
  of each problem can be tried in parallel; success in any version counts
  for that underlying problem. This is not evidence that all problems
  themselves can be reordered freely. The detailed competition discussion
  was removed from the main text to meet the user's requested scope.
- **TacticToe: Learning to Reason with HOL4 Tactics**, Thibault Gauthier,
  Cezary Kaliszyk and Josef Urban: https://doi.org/10.29007/ntlb . Read
  the abstract and introduction of arXiv:1804.00595v1 and checked the
  original EasyChair publication record. Publication is LPAR-21, EPiC 46,
  125–143 (2017); the 2018 arXiv upload is not its first publication.
  Learned tactic selection guides proof search directly in HOL4.
- **TacticToe: Learning to Prove with Tactics**, Gauthier, Kaliszyk,
  Urban, Ramana Kumar and Michael Norrish:
  https://doi.org/10.1007/s10817-020-09580-x . Read the journal-version
  abstract/introduction in arXiv:1804.00596v2 and checked the publication
  record, JAR 65(2), 257–286 (2021). This version uses learned guidance
  and Monte Carlo tree search. The main text cites only the earlier
  conference work; neither citation asserts unique priority or direct
  architectural borrowing by later systems.
- **DreamCoder: Bootstrapping Inductive Program Synthesis with Wake-Sleep
  Library Learning**, Kevin Ellis, Catherine Wong, Maxwell Nye, Mathias
  Sablé-Meyer, Lucas Morales, Luke Hewitt, Luc Cary, Armando Solar-Lezama,
  Joshua B. Tenenbaum: https://doi.org/10.1145/3453483.3454080 . Read
  the author PDF abstract, introduction and Section 2.1, including the
  two sleep phases. It jointly develops a program library and neural
  search policy; it should not be reduced to ordinary genetic programming.
  Bibliography follows the printed author list and PLDI 2021, 835–850.
- **Alien coding**, Thibault Gauthier, Miroslav Olšák and Josef Urban:
  https://doi.org/10.1016/j.ijar.2023.109009 . Read arXiv:2301.11479v2
  abstract/introduction, task specification and related-work section;
  inspected the checking/generalization discussion. It starts from random
  programs and iterates neural translation, execution and training on
  discovered programs. Agreement on sampled OEIS terms is not a proof of
  an infinite-sequence identity. Publisher metadata gives IJAR **162**
  (2023), 109009. The paper credits DreamCoder and the older proof-learning
  loop. The manuscript makes a brief methodological comparison only.
- **Genetic Programming**, John R. Koza, MIT Press, 1992: inspected the
  publisher description at https://mitpress.mit.edu/9780262527910/genetic-programming/ .
  Not cited in the shortened manuscript; no claim to have read the book.

## Usage conventions and rates

- https://ccusage.com/guide/codex/ : read the documented Codex parsing
  behavior, event_msg/token_count deltas, model context, subcounter and
  service-tier descriptions. This explains the supplied row's ledger
  basis, independently confirmed against all raw response records.
  The exact installed version and command used by the organizer are unknown.
- https://developers.openai.com/api/docs/models/gpt-6-astra : checked the
  default rates on 15 September: USD 10 uncached input, USD 1 cached input,
  USD 50 output per million tokens; long-input threshold 272,000. The
  trace's maximum request input is 259,244. The manuscript deliberately
  reconstructs a flat API-equivalent estimate, not an actual bill.
  The supplied row agrees to the cent without adding reasoning tokens
  again. No claim about actual subscription allocation, discounts or
  provider-side hardware is inferred from these calculations.
