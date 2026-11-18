# Primary-source check, November 2026

Checked 2026-11-18 by an AI agent, reading the pages below directly (not search summaries). Not reviewed by a named expert. Tables in this file have fewer than 8 columns on purpose, so the stale-claims job in `.github/workflows/maintenance.yml` does not read them as claim rows.

## 1. Rows changed in this check

| row id | old status | new status | note |
|---|---|---|---|
| vibe-03-001 | open | checked | Changelog entry "Cache multiple versions of a URL with Vary", dated July 2, 2026, read. Confirms: Cache Rules honour the origin's Vary header when "you have enabled Vary using a cache rule"; actions normalize, passthrough, bypass per header; "Vary: * continues to bypass cache"; "available on all plans (Free, Pro, Business, and Enterprise)". The blog post https://blog.cloudflare.com/vary-support (dated September 22, 2026) agrees: "Vary: * always bypasses cache". |
| aigp-06-001 | open | checked | Regulation (EU) 2026/1744 of 8 July 2026, "Digital Omnibus on AI", OJ L, 2026/1744, 24.7.2026. Secondary URL replaced by EUR-Lex. |
| aigp-06-002 | open | checked | Art. 4 of 2026/1744: enters into force "on the third day following that of its publication" (24.7.2026, so 27 July 2026). The act itself also uses 27 July 2026 in amended Art. 97(2) and new Art. 113(d). |
| aigp-06-003 | open | checked | Amended Art. 113, third para., point (c)(i): Chapter III Sections 1 to 3 apply from 2 December 2027 for Annex III systems. Original date 2 August 2026 (general date) confirmed in 2024/1689. |
| aigp-06-004 | open | checked | Amended Art. 113(c)(ii): 2 August 2028 for Art. 6(1) and Annex I systems. Original 2 August 2027 (Art. 113(c) of 2024/1689) confirmed. |
| aigp-06-005 | open | checked | New Art. 5(1)(ba) (non-consensual realistic intimate material of an identifiable person) and (bb) (child sexual abuse material within Directive 2011/93/EU), with Art. 5(1a) and (1b), apply from 2 December 2026 (amended Art. 113(a)). |
| aigp-06-006 | open | changed | No conflict in the act: Art. 50 applies from 2 August 2026. New Art. 111(4): providers of generative systems placed on the market before 2 August 2026 must comply with Art. 50(2) by 2 December 2026. Lesson wording ("sources conflict") needs an edit. |
| aigp-06-007 | open | checked | Art. 113(b) (Chapter V GPAI from 2 August 2025, Art. 101 excepted) and Art. 101 are not amended by 2026/1744. |
| aigp-06-008 | open | checked | Art. 99 amended: para. 1 replaced (adds SMCs), point (da) added to para. 4 (Art. 25(2) and (4)), new para. 6a (SMCs: lower of percentage or amount). Fine maxima unchanged. |
| aigp-02-001 | open | changed | Art. 4 replaced: "shall take measures to support the development of AI literacy"; "does not require ... to guarantee any specific level". No 2 August 2027 date for Art. 4 in the act. Lesson wording ("sources conflict") needs an edit. |
| aigp-06-009 | open | checked | Art. 113 of 2024/1689 read: in force 20th day after publication; applies from 2 August 2026; (a) Chapters I and II 2 February 2025; (b) Chapter III Section 4, Chapter V, Chapter VII, Chapter XII and Art. 78 from 2 August 2025, except Art. 101; (c) Art. 6(1) from 2 August 2027. |

Rows left unchanged: vibe-05-001, vibe-05-002, vibe-05-003, vibe-05-004 (still `open`, see section 4).

## 2. EU sources read

- Regulation (EU) 2024/1689 (AI Act), OJ L, 2024/1689, 12.7.2024: https://eur-lex.europa.eu/eli/reg/2024/1689/oj (Article 113 read).
- Regulation (EU) 2026/1744 of the European Parliament and of the Council of 8 July 2026 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 as regards the simplification of the implementation of harmonised rules on artificial intelligence (Digital Omnibus on AI), OJ L, 2026/1744, 24.7.2026: https://eur-lex.europa.eu/eli/reg/2026/1744/oj (recitals on Art. 4, Art. 5, Art. 50(2) and Art. 113; Article 1 points amending Art. 4, 4a, 5, 6, 97, 99, 111, 113; Article 4 read).
- The Commission page on digital-strategy.ec.europa.eu was not needed, since the act itself was read. The IAPP AIGP Body of Knowledge was not opened, because no row cites it.

## 3. OWASP GenAI lists (genai.owasp.org)

### OWASP Top 10 for LLM Applications 2026

- Official title on the resource page: "OWASP GenAI LLM Top 10 2026"; described there as "OWASP Top 10 for LLM Applications 2026". https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/
- Publication date on the resource page: August 3, 2026.
- Press release, blog dated September 1, 2026 (dateline "WILMINGTON, Del. — Sept. 2, 2026"): https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/ . It says the 2026 edition has "updated rankings" and quotes Zenity: "Excessive Agency, now number three".
- The full ordered list could NOT be confirmed. The PDF (download link https://genai.owasp.org/download/56857/) redirects to a "no-access" page (registration required), and genai.owasp.org has no per-entry 2026 pages (the /llm-top-10/ page still lists 2025). The codes below are as OWASP's own blog posts use them; LLM07 to LLM09 were not found anywhere on the site.

| code | title | where seen |
|---|---|---|
| LLM01:2026 | Prompt Injection | Q2 and Q3 2026 exploit roundups |
| LLM02:2026 | Sensitive Information Disclosure | Q2 and Q3 2026 exploit roundups |
| LLM03:2026 | Excessive Agency | Q2 and Q3 2026 exploit roundups; press release ("now number three") |
| LLM04:2026 | Supply Chain | Q2 and Q3 2026 exploit roundups |
| LLM05:2026 | Data and Model Poisoning | Q3 2026 exploit roundup |
| LLM06:2026 | Unbounded Consumption | Q3 2026 exploit roundup |
| LLM07:2026 | not found | not confirmed |
| LLM08:2026 | not found | not confirmed |
| LLM09:2026 | not found | not confirmed |
| LLM10:2026 | Improper Output Handling | Q2 2026 exploit roundup only (dated July 8, 2026, before the August 3 publication date; treat with care) |

Roundup URLs: Q3 https://genai.owasp.org/2026/10/08/genai-and-agentic-ai-exploit-roundup-q3-2026/ ; Q2 https://genai.owasp.org/2026/07/08/genai-and-agentic-ai-exploit-roundup-q2-2026/ . The Q3 roundup says its mappings are analyst interpretation.

### OWASP Top 10 for LLM Applications 2025 (for comparison)

Source: https://genai.owasp.org/llm-top-10/ (listed as "2025 Top 10 Risk & Mitigations for LLMs and Gen AI Apps"); resource page https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/

| code | title |
|---|---|
| LLM01:2025 | Prompt Injection |
| LLM02:2025 | Sensitive Information Disclosure |
| LLM03:2025 | Supply Chain |
| LLM04:2025 | Data and Model Poisoning |
| LLM05:2025 | Improper Output Handling |
| LLM06:2025 | Excessive Agency |
| LLM07:2025 | System Prompt Leakage |
| LLM08:2025 | Vector and Embedding Weaknesses |
| LLM09:2025 | Misinformation |
| LLM10:2025 | Unbounded Consumption |

### OWASP Top 10 for Agentic Applications for 2026 (ASI)

- Resource page "OWASP Top 10 for Agentic Applications for 2026", dated December 9, 2025: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- Press release dated December 9, 2025 (dateline "Dec. 10, 2025"): https://genai.owasp.org/2025/12/09/owasp-genai-security-project-releases-top-10-risks-and-mitigations-for-agentic-ai-security/
- Ordered list as given in the launch post https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/ (fuller titles from the Q3 2026 roundup where they differ). The PDF itself is behind registration and was not read.

| code | title |
|---|---|
| ASI01 | Agent Goal Hijack |
| ASI02 | Tool Misuse (roundup: Tool Misuse and Exploitation) |
| ASI03 | Identity & Privilege Abuse |
| ASI04 | Agentic Supply Chain Vulnerabilities |
| ASI05 | Unexpected Code Execution |
| ASI06 | Memory & Context Poisoning |
| ASI07 | Insecure Inter-Agent Communication |
| ASI08 | Cascading Failures |
| ASI09 | Human-Agent Trust Exploitation |
| ASI10 | Rogue Agents |

## 4. Could not open

- https://owasp.org/Top10/2025/ and its introduction page: owasp.org answers with a 308 redirect to https://top10.owasp.org/2025, and the proxy refuses top10.owasp.org (CONNECT 403, not on the allow-list). So rows vibe-05-001 to vibe-05-004 (2025 order, SSRF folded into A01, new A03 and A10, announcement and finalisation dates) stay `open`. The only OWASP primary text read was https://owasp.org/projects/top-ten , which says "The most current released version is the OWASP Top 10 2025." To close these rows, allow top10.owasp.org or read the pages by hand.
- The PDFs of the OWASP GenAI LLM Top 10 2026 and the Agentic Top 10 2026 (registration wall).
- LLM07:2026 to LLM09:2026 titles: not found on genai.owasp.org.
- iapp.org: reachable, but not needed (no row cites the AIGP Body of Knowledge).
