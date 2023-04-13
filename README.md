# Finnish Dolly dataset

Finnish version of the [databricks-dolly-15k instruction dataset](<https://github.com/databrickslabs/dolly/tree/master/data>), machine translated from the original English using [DeepL](<https://www.deepl.com/>).

## Data

The data is found in the file `dolly-15k-fi.jsonl`. The format and
uses of this data match those of the original English dataset. For
more information, please see
<https://github.com/databrickslabs/dolly/tree/master/data>.

## Processing

The data was processed from the original as follows:

1. Convert original data from JSONL to DOCX files

```
python3 jsonl2doc.py original-data/databricks-dolly-15k.jsonl
```

2. Translate DOCX files from `dolly-doc-in/` using [DeepL](<https://www.deepl.com/>) and save outputs in `dolly-doc-out/`.

3. Convert back to JSONL

```
python3 doc2jsonl.py \
    original-data/databricks-dolly-15k.jsonl \
    dolly-doc-out/dolly-000*.docx \
    > dolly-15k-fi.jsonl
```

## License

This dataset is licensed under the [Creative Commons Attribution-ShareAlike 3.0 Unported License](https://creativecommons.org/licenses/by-sa/3.0/legalcode) (CC BY-SA).

Note that under the [DeepL terms and conditions](https://www.deepl.com/en/pro-license), this data may not be used to develop, market or train a machine
translation algorithm.
