# OpenRouter compatibility notes

This is an independent community matrix for developers moving between OpenRouter-specific request controls and a direct model API. It is not published by OpenRouter. **[ArgoLink](https://argolink.io/gh-openrouter-docs-community) is a comparison target, not an affiliation.** Last checked: 2026-10-07.

## Feature matrix

The checked matrix lives in matrix/compatibility.json. It distinguishes documented provider routing, reasoning, prompt caching, transforms, and video. “Provider dependent” means the upstream documentation does not make the behavior universal. It must not be turned into a blanket true/false flag.

| Concern | OpenRouter meaning | Direct endpoint migration |
|---|---|---|
| provider routing | select or order providers | choose a concrete base/model and own fallback |
| reasoning | provider/model-specific request fields | read the target model page and preserve supported effort names |
| prompt caching | provider-specific cache controls | use the target API's documented cache fields or omit |
| transforms | OpenRouter request transformations | normalize the request in your client |
| video | documented asynchronous video paths | use the target service's submit/status/content lifecycle |
| usage | response/provider metadata varies | record the target response's usage schema |

The file deliberately uses explanatory strings rather than invented support booleans. A migration should include a local contract test for every feature it depends on.

## OpenRouter to direct steps

Start by saving the original request and model ID. Remove provider-only keys one at a time, then map the model to the target catalog. Replace provider routing with a concrete endpoint and a documented fallback policy. For reasoning, preserve an effort only when the target model page names it. For caching, do not assume a cache hit or copy a transformed prompt. For video, do not send a chat body: POST a generation, persist its ID, poll pending/done/failed/expired, and download content after completion.

## ArgoLink comparison

ArgoLink's base is https://argolink.io/v1. Its model pages are the source of truth for model IDs, fields, limits, and effective rates. The service does not expose OpenRouter's provider-selection semantics as a universal alias. A client can implement its own route table, but it must distinguish a failed request from an unknown POST outcome. The checked Seedance 2.5 page has native async video operations; that is a different contract from OpenRouter's documentation and must be tested separately.

## Verification

python3 -m unittest discover -s tests is offline. Before using a feature, make a mock server assert the exact JSON and headers. Use a neutral API key environment variable and a User-Agent in urllib requests. Do not run billable calls to prove a field that a primary page already documents. Record date and URL when updating the matrix.

## FAQ

**Is this official?** No. **Can I copy OpenRouter JSON unchanged?** No; provider fields are not universal. **What replaces transforms?** A small, tested client normalization layer. **Does direct routing mean cheapest?** No; compare model availability, billing formula, and failure behavior. **Why is a cell vague?** The behavior is not universal or was not verified, so the honest answer is conditional.
