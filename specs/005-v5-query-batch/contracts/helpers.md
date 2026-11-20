# Contract: hand-written helpers

**Feature**: [../spec.md](../spec.md) | **Models**: [../data-model.md](../data-model.md)

Every helper that calls the API calls the generated wrapper, so every request
goes through `request_json()` (Principle II). No helper module imports
`httpx` or `request_json` (FR-007, checked by T027a).

## `kentik_api.v5_tools` (base install)

```python
def decode_chart(response: ChartResponse) -> ChartImage: ...
```

- Returns the image bytes and the image type from the data URI.
- Raises `HTTPException(502)` with a message that names the problem when the
  data URI is not valid.

```python
def split_batch(
    upserts: Sequence[BatchUpsert],
    deletes: Sequence[BatchDelete] = (),
    *,
    replace_all: bool = False,
    max_bytes: int = 4_000_000,
) -> list[BatchPart]: ...
```

- Every part serializes to at most `max_bytes`. Only the last part has
  `complete=True`. Every part has the same `replace_all`.
- Deletes follow every upsert. The API applies deletes only after the last
  part arrives, so their position does not change the result.
- Raises `ValueError` when one upsert or delete alone is larger than
  `max_bytes`.

```python
def send_batch(
    send: Callable[..., BatchResponse],
    parts: Sequence[BatchPart],
) -> str: ...
```

- Calls `send(data=part)` for each part, in order. It copies the `guid`
  from the first response into every later part, and returns the `guid`.
- Raises `BatchSendError(guid, sent, cause)` on the first failure. It never
  resends.
- Usage: `send_batch(client.v5.batch_tags, parts)` or
  `send_batch(partial(client.v5.batch_populators, dimensionName="c_x"), parts)`.

```python
def wait_for_batch(
    client: KentikAPI,
    guid: str,
    *,
    timeout: float = 600.0,
    interval: float = 5.0,
) -> BatchStatus: ...
```

- Polls `client.v5.batch_status(guid=guid)` until `is_complete` is true, and
  returns that status.
- Raises `BatchWaitTimeout(guid, last_status)` when `timeout` expires.
- Raises the error of a failed status call at once. It never resends the
  batch.

## `kentik_api.devices` (base install)

```python
class DeviceLookup:
    @classmethod
    def from_api(cls, client, labels=None, include_deleted=False) -> "DeviceLookup": ...
    def __getitem__(self, id_or_name: str | int) -> DeviceDetailed | None: ...
    def get_by_id(self, device_id: str | int) -> DeviceDetailed | None: ...
    def interfaces(self, device: DeviceDetailed) -> list[Interface]: ...
    @staticmethod
    def make_link(device: DeviceDetailed, interface: Interface) -> str: ...
    def parse_link(
        self, link: str
    ) -> tuple[DeviceDetailed | None, Interface | None]: ...
    # bits/s, NaN if unknown
    def get_link_speeds(self, links=None) -> dict[str, float]: ...
    def save(self, path: str | os.PathLike[str]) -> None: ...
    @classmethod
    def load(cls, path: str | os.PathLike[str]) -> "DeviceLookup": ...
```

- The method names follow 1.x `DeviceCache`, for a low-friction port.
- `DeviceDetailed` and `Interface` are the generated V6 models.
- `save()` and `load()` use JSON only.

## `kentik_api.analytics` (extra `analytics`)

The names follow 1.x `kentik_api.analytics`, for a low-friction port.

- Importing the package without the extra raises `ImportError` with the text
  `pip install "kentik-api[analytics]"`. The rest of the SDK still imports.
- `DataQueryDefinition.from_dict(d)`, `from_file(path)` (`yaml.safe_load`),
  and `get_data(client, **kwargs) -> dict[str, DataFrame]` (one DataFrame for
  each bucket, with typed columns and a time index).
- `DFCache(directory)` with `fetch(query_fn, start, end, step=None,
  dedup_columns=None)`, `get`, `store`, `drop`, and `fetch_latest`. With
  `step`, a step that one cached file holds is not fetched again.
- `flatness_analysis(devices, data, flatness_limit, window, ...)`: the 1.x
  signature and output.
- `SQLQueryDefinition`, or a definition whose query is SQL text, raises
  `ValueError` that says Kentik retired the V5 SQL query endpoint.
- An `@fixup:` mapping raises `ValueError` that names the safe options:
  `source`, `type`, or a change to the DataFrame in the caller's code.
