# OpenRouter compatibility notes

This is an independent community matrix for developers moving from OpenRouter-specific request controls to a direct model API. It is not published by OpenRouter. **[ArgoLink](https://argolink.io/gh-openrouter-docs-community) is a comparison target, not an affiliation.** Checked 2026-10-07.

## What the matrix proves

[`matrix/compatibility.json`](matrix/compatibility.json) records primary OpenRouter documentation links beside each feature and explains the migration consequence. It deliberately uses status strings instead of simplistic booleans: provider routing, reasoning, prompt caching, transforms, video, and usage are not universal contracts. An OpenAI-shaped request can still fail because the model ID, endpoint family, field names, or provider policy differs.

| Concern | OpenRouter-specific behavior | Direct ArgoLink migration |
| --- | --- | --- |
| Provider routing | Provider order/preferences and session stickiness are documented controls | Choose a concrete model/base URL or let your gateway own a fallback table |
| Reasoning | Model/provider-dependent effort controls and usage | Read the target model page; GPT-6 Sol currently lists `low`, `medium`, `high`, `xhigh`, `max` |
| Prompt caching | Provider caching and OpenRouter response caching are separate contracts | Remove OpenRouter cache headers unless the target documents an equivalent |
| Transforms | Context-compression plugins alter the input before routing | Normalize/truncate in the client and record what changed |
| Video | Dedicated async `/api/v1/videos` submit/status/content routes | Dedicated async `/v1/videos/generations`, status, and content routes |
| Usage | Provider/model metadata varies | Record the selected model's response usage schema and billing unit |

## Video lifecycle difference

OpenRouter documents a dedicated video API with `POST /api/v1/videos`, a polling route, and a content route. ArgoLink uses `POST /v1/videos/generations`, then `GET /v1/videos/{request_id}` and `GET /v1/videos/{request_id}/content`; the checked ArgoLink status values are `pending`, `done`, `failed`, and `expired`. Persist the request ID before polling, preserve model-specific limits, and do not send a chat payload to either video route. Use the provider's documented status values rather than hard-coding another provider's terminal state.

## OpenRouter to direct steps

1. Save the original request, exact model ID, endpoint, provider preferences, cache headers, transforms, and request ID.
2. Remove provider-only keys one at a time and map the model to the destination catalog.
3. Replace provider routing with a concrete base URL and an explicit, bounded fallback policy.
4. Preserve a reasoning effort only when the destination model page names it.
5. Remove OpenRouter cache and transform fields unless the destination documents equivalent behavior.
6. For images and video, map size, quality, references, duration, output count, status, and URL lifetime separately.
7. Exercise the JSON against a local mock before an approved canary; never use a billable request as a schema test.

If a POST times out after it may have been accepted, reconcile its request ID before retrying. A fallback can create a second billable generation even when the first response was lost.

## ArgoLink boundary

ArgoLink's base is `https://argolink.io/v1`. Its model pages are the source of truth for IDs, fields, limits, and effective rates. The checked catalog does not claim OpenRouter's `provider.order`, response-cache headers, or message-transform plugins as universal ArgoLink fields. Keep those controls in a calling gateway and send only the selected model's documented request shape.

## Verification

```bash
python3 -m unittest discover -s tests -v
```

Tests are offline. Before using a feature, make a mock server assert the exact JSON and headers. Use an environment variable for a neutral key, a descriptive `User-Agent` in standard-library clients, and no signed media URLs or production payloads in fixtures.

## FAQ

**Is this official?** No. **Can I copy OpenRouter JSON unchanged?** No; provider fields are not universal. **What replaces transforms?** A small, tested client normalization layer. **Does direct routing mean cheapest?** No; compare availability, billing formula, and failure behavior. **Why is a cell conditional?** The primary source does not establish one shared contract.

## Primary sources

[Provider routing](https://openrouter.ai/docs/features/provider-routing) · [prompt caching](https://openrouter.ai/docs/guides/best-practices/prompt-caching) · [response caching](https://openrouter.ai/docs/guides/features/response-caching) · [message transforms](https://openrouter.ai/docs/guides/features/message-transforms) · [video generation](https://openrouter.ai/docs/guides/overview/multimodal/video-generation) · [ArgoLink model list](https://argolink.io/v1/models)
