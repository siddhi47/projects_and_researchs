# utilities

Different utilities in python

<h2>Usage</h2>

<h3>insert_df_threaded</h3>

```python
insert_df_threaded(df, name = "foo_bar", con = engine, if_exists='append')
```

<h3>read_table_sql</h3>

```python
read_table_sql("foo_bar", con = engine, schema = 'schema',  if_exists='append')
```
<h3>insert_df</h3>

```python
insert_df(df, name = "foo_bar", engine, if_exists='append')
```
