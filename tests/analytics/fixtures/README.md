<!-- HAND-WRITTEN: not modified by [`uv run poe generate`](../../../pyproject.toml). Edit directly. -->

# Analytics golden fixtures

The `golden_*.json` files are the output of the 1.x analytics code, so that the
2.x tests can prove the same columns and values (spec 005, SC-003).

| File | What it is |
| --- | --- |
| [`topx_response.json`](topx_response.json) | A fixed `topXdata` response with two buckets, one with time series |
| [`topx_definition.yaml`](topx_definition.yaml) | A 1.x `DataQueryDefinition` file for that response |
| `golden_topx_*.json` | The 1.x `data_result_to_df` DataFrames, one per bucket (`orient="table"`) |
| [`golden_topx_expanded_query.json`](golden_topx_expanded_query.json) | The 1.x `expand_query` output for a fixed start and end |
| [`flatness_input.json`](flatness_input.json) | Two links, 6 hours of 5-minute `bytes_out` samples. `router1:eth0` is flat for 3 hours |
| [`golden_flatness.json`](golden_flatness.json) | The 1.x `flatness_analysis` result for that input |

[`make_golden.py`](make_golden.py) made them. It reads the 1.x modules from git at commit
`b48cfd912b162f99290ff00170916abf9cd67d23` (kentik-api 1.0.7) and runs them
with pandas 2.3.3, outside this project's environment:

```bash
uv run --no-project --with pandas==2.3.3 --with pyyaml \
    python tests/analytics/fixtures/make_golden.py
```

Do not regenerate them to make a failing test pass. A difference from these
files is a difference from 1.x behavior.
