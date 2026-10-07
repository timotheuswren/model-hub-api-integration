# Model hub API integration: Hugging Face Inference Providers and ArgoLink

A dated comparison of two ways to call open-model APIs: Hugging Face Inference Providers and a direct OpenAI-compatible gateway. This is an independent guide, not Hugging Face or ArgoLink documentation. **[ArgoLink](https://argolink.io/gh-model-hub-api-integration)** is the second integration shown. Last checked: 2026-10-07.

## The key distinction

A model name is not a portable endpoint contract. Hugging Face routes a Hub model through an Inference Provider, while ArgoLink exposes a provider-backed catalog with its own IDs, limits, pricing, and endpoint family. Compare the full tuple `(model ID, provider, endpoint, body schema, billing source)`, not just the display name.

The current [Hugging Face Chat Completion guide](https://huggingface.co/docs/inference-providers/tasks/chat-completion) shows an OpenAI-compatible client with base URL `https://router.huggingface.co/v1`, an HF token, and a Hub ID such as `zai-org/GLM-5.3:baseten`. The provider suffix selects a route; it is not an ArgoLink model ID. Hugging Face also documents provider routing, streaming, tools, and model-specific availability in the model UI. The [pricing guide](https://huggingface.co/docs/inference-providers/pricing) says routed requests are billed through the Hub account, while a custom provider key is billed by that provider; credits and terms differ.

ArgoLink uses `https://argolink.io/v1` and an ArgoLink catalog ID such as `glm-5.3`, `glm-5.2`, `deepseek-v4-pro`, or `deepseek-v4.1-flash` only when that ID exists in the live catalog. Its model page, not a Hub card, controls context, output, reasoning, image support, and effective rates. Re-read [GET /v1/models](https://argolink.io/v1/models) and the relevant [model pages](https://argolink.io/en/models) before shipping.

## Request shapes

`examples/requests.py` builds both payloads offline so a reviewer can see what changes before any key or request exists:

```python
from examples.requests import compare_payloads

for name, request in compare_payloads("Explain a failing test in one sentence").items():
    print(name, request["url"], request["json"])
```

Hugging Face shape:

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)
result = client.chat.completions.create(
    model="zai-org/GLM-5.3:baseten",
    messages=[{"role": "user", "content": "Hello"}],
)
```

ArgoLink shape:

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://argolink.io/v1",
    api_key=os.environ["ARGOLINK_API_KEY"],
)
result = client.chat.completions.create(
    model="glm-5.3",
    messages=[{"role": "user", "content": "Hello"}],
)
```

These examples are intentionally not executed by tests. Keep keys in environment variables, set explicit timeouts, and disable automatic retries for side-effecting calls unless the service documents idempotency. Preserve response IDs and usage fields for accounting.

## Model crosswalk at the 2026-10-07 check

| Task | Hugging Face example | ArgoLink catalog candidate | What must be rechecked |
| --- | --- | --- | --- |
| General chat / coding | `zai-org/GLM-5.3:baseten` | `glm-5.3` | provider availability, reasoning fields, context and price |
| Fast GLM chat | `zai-org/GLM-5.3-Flash:baseten` | `glm-5.3-flash` or `glm-5.3-flashx` | image support, effort aliases, throughput claims |
| DeepSeek reasoning | a Hub model ID plus selected provider | `deepseek-v4-pro` | billing window, thinking cannot be disabled, output cap |
| Lower-cost DeepSeek | a Hub model ID plus selected provider | `deepseek-v4.1-flash` | image input and `reasoning_effort: none` behavior |
| Qwen | a Hub model page and provider suffix | verify an exact ArgoLink ID first | never invent an ArgoLink alias from a Hub name |

This table is a navigation aid, not a promise that the two services host the same weights or revision. Hugging Face's provider may expose a model before, after, or with different parameters from the gateway. A model page and a dated catalog response are the evidence for a production choice.

## Pricing and usage comparison

Hugging Face's routed billing is centralized in the Hub account and passes provider rates through without an additional Hub markup according to its pricing page. Custom provider keys change who bills and whether Hub credits apply. ArgoLink's `pricing.effective` values are its own dated rates; do not compare them with a Hub estimate without aligning provider, model revision, tokenization, cache state, long-context multipliers, and billing window. Keep official and effective prices in separate columns in your worksheet. Never copy a price from a search result or an old README.

## Failure modes

- `401`: wrong token namespace (`HF_TOKEN` versus `ARGOLINK_API_KEY`) or an expired secret.
- `400`: wrong model ID, provider suffix, message shape, or unsupported reasoning/tool field.
- `404`: duplicated `/v1` or a route that belongs to a different endpoint family.
- `429` / `503`: provider capacity or rate limits; honor `Retry-After` and avoid blindly replaying writes.
- model not found: confirm Hub availability and selected provider, then separately confirm the ArgoLink catalog ID.
- usage mismatch: keep the raw response ID and token fields; neither UI totals nor a local estimate is a billing authority.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

Tests build payloads and validate documentation offline. No provider request is sent and no production key belongs in this repository.
