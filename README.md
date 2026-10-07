# Model hub API integration

This repository is a dated integration note for configuring a model UI or hub against documented APIs. It is independent of the listed UI and model providers. **[ArgoLink](https://argolink.io/gh-model-hub-api-integration) is one compatible endpoint example.** Last checked: 2026-10-07.

## Common fields

Every connection has five values: provider, base URL, key environment, model ID, and endpoint family. Store the key through the UI's secret manager. A base ending at https://argolink.io/v1 is appropriate only when the client appends the documented path. Verify the actual request with a local mock and inspect whether it calls chat completions or Responses.

The model catalog is the source of truth for current IDs, context, output, tool support, image fields, and effective rates. A UI model dropdown can contain stale aliases. Remove an unavailable model instead of leaving a misleading configuration.

## Provider boundary

Hugging Face Inference Providers and a hosted gateway can expose similar model names with different request fields, billing, and usage. Verify the exact provider route and model ID on both sides before comparing.

## Error checklist

401 means key or account configuration. 404 often means a duplicated path or unsupported endpoint. 400 means the request shape or model field is wrong. A stream that ends early needs a provider response and client log; do not replay state-changing tools automatically. Redact Authorization, signed media URLs, and user content.

## Validation

python3 -m unittest discover -s tests checks this note offline. No real UI or provider call is made. Before production, pin the UI image, record the API/client version, test a minimal request, and note the catalog date. Video generation is a separate asynchronous contract and should not be forced through a chat connector.

## FAQ

**Can any OpenAI-compatible UI use any model?** No; compatibility is endpoint and feature specific. **Where does the price come from?** The dated model page, not a UI label. **Why separate this from SDK examples?** A UI owns credentials and connection settings; an SDK owns code and retries. **What if a setting changed?** Re-read the current UI documentation and update the evidence date.
