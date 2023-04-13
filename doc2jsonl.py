import docx
import sys
import json
import tqdm

from logging import warning
from argparse import ArgumentParser


def argparser():
    ap = ArgumentParser()
    ap.add_argument('jsonl', help='original-data/databricks-dolly-15k.jsonl')
    ap.add_argument('docxs', nargs="+", help='All translated docx files in correct order')
    return ap


def load_original_data(fn):
    data = []
    with open(fn) as f:
        for l in f:
            data.append(json.loads(l))
    return data


def yield_translations(fnames):
    expected_doc_idx = 0

    for fname in tqdm.tqdm(fnames):
        d = docx.Document(fname)

        curr_doc, curr_field = None, None
        for p in d.paragraphs:
            if p.runs[0].bold and p.text.startswith("Asiakirja "):
                doc_idx = int(p.text[len("Asiakirja "):])
                if expected_doc_idx != doc_idx:
                    warning(f'index mismatch: {expected_doc_idx} != {doc_idx}')
                expected_doc_idx += 1

                if curr_doc:
                    yield curr_doc
                curr_doc={
                    "instruction": None,
                    "context": None,
                    "response": None,
                    "category": None,
                }
                curr_field = None
            elif p.runs[0].bold and p.text.startswith("Ohjeet"):
                curr_field = "instruction"
            elif p.runs[0].bold and p.text.startswith("Konteksti"):
                curr_field = "context"
            elif p.runs[0].bold and p.text.startswith("Vastaus"):
                curr_field = "response"
            elif p.runs[0].bold:
                raise ValueError(f'unexpected section: {p.text}')
            elif p.text.isspace() or not p.text:
                pass
            else:
                assert curr_field is not None
                assert curr_doc[curr_field] is None
                curr_doc[curr_field] = p.text
        else:
            yield curr_doc


def main(argv):
    args = argparser().parse_args(argv[1:])

    original_data = load_original_data(args.jsonl)

    # confirm sync and copy in category
    for i, d in enumerate(yield_translations(args.docxs)):
        o = original_data[i]

        if d['context'] is None:
            assert o['context'].isspace() or not o['context'], 'desync'
        else:
            assert o['context'] and not o['context'].isspace(), 'desync'

        d['category'] = o['category']

        print(json.dumps(d, ensure_ascii=False))
    count = i + 1

    if count != len(original_data):
        print(f'''
##############################################################################
#
# WARNING: incomplete: got {count} documents, original is {len(original_data)}
#
##############################################################################
''', file=sys.stderr)


if __name__=="__main__":
    sys.exit(main(sys.argv))
