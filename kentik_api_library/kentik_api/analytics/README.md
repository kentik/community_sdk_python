# Support for Advanced Analytics

The `analytics` sub-module provides support for processing of Kentik time series data using pandas DataFrames.
The sub-module requires `pandas` and `pyyaml` modules which are automatically installed when `kentik-api`
is installed with the `analytics` option (`kentik-api[analytics]`).

The sub-module provides:

## Retrieval of Kentik query results in pandas DataFrame
Retrieval of Kentik data in a DataFrame is supported via "mapped queries". Mapped queries are provided both for `topXdata`
queries (class `DataQueryDefinition`) and `sql` queries (class `SQLQueryDefinition`). Behavior differs due to inherent
differences in those 2 query methods. In both cases, the `*QueryDefinition` classes contain:
- query template
- response mapping for constructing DataFrame from returned data
For both query types, mapped query objects can be constructed based on YAML formatted files.

### Query templates
Query templates obviously differ for both types of queries, however in both cases they can be parametrized by
inserting `str.format` style directives which allow to insert specific values at runtime. For example, if you
want to insert beginning of the queried interval, include `{start_time}` placeholder where the value is expected in
the query and then provide `start_time=<desired_start_time>` among arguments to the `{Data|SQL}MappedQuery.get_data()`
method. Any value that can be expanded using `str.format` syntax can be interpolated at runtime.

#### Response mapping
Result mapping represented by `ResultMapping` class is (basically) a dictionary keyed by output DataFrame columns names
with entries providing data for constructing values of the column from Kentik API query responses. Individual
mapping entries are represented by the `MappingEntry` class. Mapping entries contain following attributes:
- `source`: string containing `str.format`-style formatting string for extracting specific result data fields. Special
          directives, prefixed with `@TS` allow extracting data from `topXdata` result `timeSeries` blocks (and hence are
          applicable only in the context of `DataMappedQuery`)
- `type`: optional string containing desired data type for column values. Any `numpy.dtype` and Python
          type name is accepted. In addition, following special type strings are provided:
          - `time`: converts string to pandas.datetime object
          - `unix_timestamp`: converts integer Unix epoch timestamp to pandas.datetime object
          - `unix_timestamp_millis`: converts integer Unix epoch millisecond timestamp to pandas.datetime object
          - `@fixup: <python lambda>`: allows applying a lambda function to every value in the columns. Example:
                 type: `@fixup: lambda x: x.split(".")[0]` results in calling
                 `DataFrame.transform(lambda x: x.split(".")[0])` for all values in the column

- `index`: boolean indicating whether columns should be used as index for resulting DataFrame. If multiple entries
           in a mapping have it set, resulting DataFrame is multi-indexed.

#### DataQueryDefinition
This class allows issuing `topXdata` query (which allows to issue one or more KDE queries) and mapping results to
DataFrames (one DataFrame per result entry). Query template can be specified either as JSON string or an equivalent
dictionary. An easy way to get valid JSON for a specific query is to use Kentik Data Explorer to construct it.
JSON payload can be exported using`Actions -> Show API Call -> JSON Input` menu item.
Result mapping for `topXdata` query results allows constructing DataFrames both based on aggregate values and
time series data (returned if `raw` attribute is set to `true` in definition of an aggregate in the query). Time series
data are extracted by specifying `@TS.<variable>.*` in `source` field of a mapping entry. There are 3 types of `@TS`
source specifications:
- `@TS.<variable>.timestamp` extracts timestamp field
- `@TS.<variable>.value` extracts variable value field
- `@TS.<variable>.period` extracts sampling period field

In all cases, the `<variable>` refers to the name of the `timeSeries` keys in the response block. Time series names
correspond with aggregates specified in the query (for which `raw` attribute was set to `true`). Unfortunately
names of time series cannot be easily established and must be figured out by issuing a query and inspecting response.
If mapping specifies at least one `@TS` source, number of rows in the resulting DataFrame is equal to number of
entries in the result time number of entries in a time series (all time series have the same length in each result set).
Values for any non-`@TS` columns are replicated for each timestamp.

Each instance of `DataQueryDefinition` contains a dictionary keyed by query `bucket` values and containing instance of
`ResultMapping` for the specific query. Result mapping for an result entry is matched by value of the `bucket`
attribute. If no match is found in the mapping dictionary, mapping with key `all` is used if present. Result mapping is
mandatory in `DataQueryDefinition` as there is no meaningful canonical way to map `topXdata` responses to DataFrames.

The `DataQueryDefinition.get_data(api, **kwargs)` method executes query after expanding the template using parameters
provided in `kwargs` and then maps returned data (if any) to DataFrames. It returns dictionary keyed by values of
the `bucket` attribute in each response entry (which corresponds to `bucket` attribute in query).

Example `DataQueryDefinition` in YAML format:
```yaml
query:
  queries:
  - bucket: simple
    query:
      aggregates:
      - column: f_sum_both_bytes
        fn: average
        name: avg_bits_per_sec
        raw: true
      all_devices: true
      dimension:
      - Traffic
      ending_time: '{end}'
      fastData: Full
      metric:
      - bytes
      starting_time: '{start}'
      time_format: UTC
      topx: 125
  version: 4

mappings:
  all:
    ts:
      source: '@TS.both_bits_per_sec.timestamp'
      index: true
    bps:
      source: '@TS.both_bits_per_sec.value'
      type: float
    period:
      source: '@TS.both_bits_per_sec.period'
      type: int64
    avg_bps:
      source: '{avg_bits_per_sec}'
      type: float64
```
The query template in the definition above has 2 parameters `start` and `end`. Output from
`DataQueryDefinition.get_data(api, start=<time>, end=,=<time>)` call is a dictionary with one key `simple` containing
DataFrame with`bps`, `period` and `avg_bps` columns and indexed by time.

#### SQLQueryDefinition
This class allows issuing SQL query via Kentik API and mapping response data into DataFrame. Instance of `SQLMappedQuery`
class can be constructed either based on dictionary (the `SQLQueryDefinition.from_dict` factory method) or YAML data
(`SQLQueryDefinition.from_file` method). The format is the same in both cases:

```yaml
query: <verbatim text of SQL query with optional {str.format} placeholders>,
mapping:
<DataFrame column name>:
  - source: <str.format string constructing value from SQL row>
  - type: <data type specification>
  - index: <bool>
...
```
Where:
- the `query` field is required. It is expected to contain Kentik SQL query template. Final SQL query is constructed by
  the `SQLQueryDefinition.to_sql(**kwargs)` method. The content of the `query` field is used as `str.format` format string
  and `kwargs` are passed as arguments. `kwargs` must provide value for each named variable used in formatting constructs
  in the query template. For example, for `query`:
  ```sql
  SELECT i_start_time, i_device_name, i_output_interface_description, sum(both_bytes) FROM all_devices
  WHERE i_start_time >= '{start}' AND i_start_time <= '{end}'
  ```
  `kwargs` passed to `SQLQueryDefinition.to_sql(**kwargs)` must provide at least keys `start` and `end`.
  
- `mapping` is optional, if present output DataFrame will have only columns specified in the mapping.
  Every mapping entry must contain the `source` field, `type` and `index` fields are optional.
  `source` field defines how values of the column are constructed from SQL response columns. The content of the
  field is `str.format` expression. Key-value pairs representing all columns in a SQL response row are passed as
  values to the `str.format`. Example mapping entry:
  ```yaml
  link:
    source: '{i_device_name}:{i_output_interface_description}'
  ```
  defines that output DataFrame will have column `link` with values constructed by joining values of columns
  `i_device_name` and `i_output_interface_description` in each SQL response row.
  
  If the `type` field is not specified, data type is not explicitly set in the resulting `DataFrame` column. If no mapping entry
  has `index` field set to `true`, the resulting DataFrame will have default index. The last column with `index` set to
  true (as listed in the mapping) is used as index for the DataFrame (Multi-indexes are not directly supported)

### Using `SQLMappedQuery` to load data to `DFCache`

- `SQLMappedQuery.make_query_fn` method returns curried function suitable for passing to the `DFCache.fetch` method to retrieve data from the Kentik API.

## Caching of Pandas DataFrames on local disk
The `DFCache` class implements simple DataFrame cache. It supports:
- storing DataFrames on local disk in Apache parquet format (method: `store`)
- retrieving merged and de-duplicated DataFrame from cached data for specific time interval (method: `get`)
- retrieving data from KentikAPI using a mapped query (method: `fetch`)
All cached DataFrames are expected to have identical format (`DFCache.get()` fails otherwise)

## Analytic methods processing Pandas DataFrames
At the moment, only one analytic method is provided

### Detection of constant link utilization (`flatness`)
This method allows to detect intervals of constant traffic on a set of network links. Network link = `device:interface` tuple.
Non-zero and non-saturating "flat" traffic in outbound direction on perimeter links can be used as an indication of
bandwidth constraint in peer networks.

The actual analysis is performed by the `flatness_analysis` function. Results are returned  in an instance of the
`FlatnessResults` class. See the inline documentation of the  `flatness_analysis` function for futher details.
The `flatness_analysis` function internally uses following functions:
- `set_link_utilization`: adds "speed" and "utilization" column to DataFrame based on "bps_out" column values and interface speeds obtained from DeviceCache
- `compute_stats`: computes mean, min and max over a column using rolling window and grouping by a column
- `analyze_flatness`: produces list on time intervals in which traffic in the input DataFrame was deemed to be "flat" based on provided criteria and returns `FlatnessResults` instance.

The above functions allow to customize names of DataFrame columns and can be used individually to construct analysis for different use cases.
  