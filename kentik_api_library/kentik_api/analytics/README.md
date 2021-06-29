# Support for Advanced Analytics

The `analytics` sub-module provides support for processing of Kentik time series data using pandas DataFrames.
The sub-module requires `pandas` and `pyyaml` modules which are automatically installed when `kentik-api`
is installed with the `analytics` option (`kentik-api[analytics]`).

The sub-module provides:

## Retrieval of Kentik query results in pandas DataFrame
Retrieval of Kentik data in a DataFrame is supported via "mapped queries". Currently only `SQLMappedQuery` implementation
is available. It allows to issue SQL query via Kentik API and map response data into DataFrame. Instance of `SQLMappedQuery`
class can be constructed either based on dictionary (the `SQLMappedQuery.from_dict` factory method) or YAML data
(`SQLMappedQuery.from_file` method). The format is the same in both cases:

```
query: <verbatim text of SQL query with optional {str.format} placeholders>,
mapping:
<DataFrame column name>:
  - source: <str.format string constructing value from SQL row>
  - type: <"time" or pandas.dtype string>
  - index: <bool>
...
```
Where:
- the `query` field is required. It is expected to contain Ketnik SQL query template. Final SQL query is constructed by
  the `SQLQueryDefinition.to_sql(**kwargs)` method. The content of the `query` field is used as `str.format` format string
  and `kwargs` are passed as arguments. `kwargs` must provide value for each named variable used in formatting constructs
  in the query template. For example, for `query`:
  ```
  SELECT i_start_time, i_device_name, i_output_interface_description, sum(both_bytes) FROM all_devices
  WHERE i_start_time >= '{start}' AND i_start_time <= '{end}'
  ```
  `kwargs` passed to `SQLQueryDefinition.to_sql(**kwargs)` must provide at least keys `start` and `end`.
  
- `mapping` is optional, if present output DataFrame will have only columns specified in the mapping.
  Every mapping entry must contain the `source` field, `type` and `index` fields are optional.
  `source` field defines how values of the column are constructed from SQL response columns. The content of the
  field is `str.format` expression. Key-value pairs representing all columns in a SQL response row are passed as
  values to the `str.format`. Example mapping entry:
  ```
  link:
    source: '{i_device_name}:{i_output_interface_description}'
  ```
  defines that output DataFrame will have column `link` with values constructed by joining values of columns
  `i_device_name` and `i_output_interface_description` in each SQL response row.
  
  If the `type` field is not specified, data type is not explicitly set in the resulting `DataFrame` column. If no mapping entry
  has `index` field set to `true`, the resulting DataFrame will have default index. The last column with `index` set to
  true (as listed in the mapping) is used as index for the DataFrame (Multi-indexes are not directly supported)

### Using `SQLMappedQuery` to load data to `DFCache`

  - `SQLMappedQuery.make_query_fn` method returns curried function suitable for passing to the `DFCache.fetch` method
    to retrieve data from the Kentik API.

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
  - `set_link_utilization`: adds "speed" and "utilization" column to DataFrame based on "bps_out" column values and
    interface speeds obtained from DeviceCache
  - `compute_stats`: computes mean, min and max over a column using rolling window and grouping by a column
  - `analyze_flatness`: produces list on time intervals in which traffic in the input DataFrame was
     deemed to be "flat" based on provided criteria and returns `FlatnessResults` instance.

The above functions allow to customize names of DataFrame columns and can be used individually to construct analysis for different use cases.
  