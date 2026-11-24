"""Source-linked distillation and local neural retrieval; no embedding API calls."""
import argparse
from contextlib import closing
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sqlite3
import struct
import sys
import tempfile
import urllib.request

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FILTERS = {'kind', 'status', 'area', 'project', 'source_date'}


def source_path(root, relative):
    path = (Path(root) / relative).resolve()
    if not path.is_relative_to(Path(root).resolve()) or Path(relative).is_absolute():
        raise ValueError('Source must be inside the vault')
    return path


def source_text(path):
    return path.read_bytes().decode('utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')


def text_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def materialize_record(spec, root):
    text = source_text(source_path(root, spec['source']))
    if spec.get('source_sha256') and spec['source_sha256'] != text_hash(text):
        raise ValueError('Source changed; review the distillation: ' + spec['source'])
    start, stop = spec['start'], spec.get('stop')
    if not start or text.count(start) != 1:
        raise ValueError('Start locator must occur exactly once: ' + spec['id'])
    begin = text.index(start)
    if stop:
        if text.count(stop) != 1 or text.index(stop) <= begin:
            raise ValueError('End locator must uniquely follow the start: ' + spec['id'])
        end = text.index(stop)
    else:
        end = len(text)
    quote = text[begin:end].rstrip()
    end = begin + len(quote)
    citation = dict(path=spec['source'], start_char=begin, end_char=end,
                    start_line=text.count('\n', 0, begin) + 1,
                    end_line=text.count('\n', 0, max(begin, end - 1)) + 1,
                    source_sha256=text_hash(text), quote_sha256=text_hash(quote),
                    offset_basis='Unicode characters in UTF-8 text with BOM removed and LF newlines')
    keys = ['id', 'title', 'text', 'kind', 'status', 'area', 'project', 'source_date', 'tags']
    result = {key: spec.get(key) for key in keys}
    if any(not isinstance(result[k], str) or not result[k].strip() for k in keys[:7]):
        raise ValueError('Missing record identity, text, or classification')
    return result | dict(record_type='distillation', citation=citation, source_quote=quote,
                         boundary_method='reviewed_semantic_unit', distillation_author='assistant',
                         review_status='agent-reviewed; user review pending', prepared_date=spec.get('prepared_date'))


def source_current(record, root):
    try:
        c = record['citation']
        text = source_text(source_path(root, c['path']))
        return (text_hash(text) == c['source_sha256'] and
                text_hash(text[c['start_char']:c['end_char']]) == c['quote_sha256'])
    except (OSError, UnicodeError, ValueError, KeyError):
        return False


def normalized(vector):
    vector = [float(v) for v in vector]
    if not vector or not all(math.isfinite(v) for v in vector):
        raise ValueError('Vectors must be nonempty and finite')
    norm = math.sqrt(math.fsum(v * v for v in vector))
    if not math.isfinite(norm) or norm <= 0:
        raise ValueError('Cannot use a zero or overflowing vector')
    return [v / norm for v in vector]


def write_index(records, vectors, path, profile):
    vectors = [normalized(v) for v in vectors]
    if not records or len(records) != len(vectors) or len({r['id'] for r in records}) != len(records):
        raise ValueError('Need one vector per uniquely identified record')
    dims = len(vectors[0])
    if any(len(v) != dims for v in vectors):
        raise ValueError('Vector dimensions differ')
    path = Path(path).resolve()
    if path.suffix not in ['.sqlite3', '.sqlite', '.db']:
        raise ValueError('Use a database filename, not a source-note path')
    if path.exists():
        with closing(sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)) as conn:
            try: owner = conn.execute("select value from meta where key='owner'").fetchone()
            except sqlite3.DatabaseError as exc: raise ValueError('Refusing to replace an unrelated database') from exc
            if owner != ('mine2ndmind-semantic-pilot',): raise ValueError('Unrelated database')
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(prefix='index-', suffix='.sqlite3', dir=path.parent, delete=False)
    temp = Path(handle.name); handle.close()
    try:
        with closing(sqlite3.connect(temp)) as conn, conn:
            conn.executescript('create table meta (key text primary key,value text not null);'
                               'create table records (id text primary key,kind text,status text,area text,'
                               'project text,source_date text,payload text not null,vector blob not null);')
            conn.executemany('insert into meta values (?,?)', [('owner','mine2ndmind-semantic-pilot'),
                ('profile',json.dumps(profile,sort_keys=True)),('dimensions',str(dims))])
            for record, vector in zip(records, vectors):
                conn.execute('insert into records values (?,?,?,?,?,?,?,?)',
                    (record['id'], record['kind'], record['status'], record['area'], record['project'],
                     record['source_date'], json.dumps(record,ensure_ascii=False), struct.pack('<'+'f'*dims,*vector)))
        os.replace(temp, path)
    finally:
        if temp.exists(): temp.unlink()


def search_index(path, vector, root, profile, filters=None, k=5, include_evidence=False):
    if not 1 <= k <= 50: raise ValueError('k must be between 1 and 50')
    filters = filters or {}
    if set(filters) - FILTERS: raise ValueError('Unknown metadata filter')
    vector = normalized(vector)
    with closing(sqlite3.connect(Path(path).resolve().as_uri() + '?mode=ro', uri=True)) as conn:
        meta = dict(conn.execute('select key,value from meta'))
        if json.loads(meta['profile']) != profile: raise ValueError('Embedding model profile mismatch; rebuild the index')
        dims = int(meta['dimensions'])
        if len(vector) != dims: raise ValueError('Query vector has the wrong dimensions')
        conditions = ['"'+key+'" = ?' for key in filters]
        query = 'select payload,vector from records'+(' where '+' and '.join(conditions) if conditions else '')
        rows = conn.execute(query,list(filters.values())).fetchall()
    hits = []; stale = 0
    for payload, blob in rows:
        record = json.loads(payload)
        if not source_current(record, root): stale += 1; continue
        if not include_evidence:record.pop('source_quote',None)
        stored = struct.unpack('<'+'f'*dims,blob)
        score = math.fsum(a*b for a,b in zip(vector,stored))
        hits.append(record | {'score': score})
    hits.sort(key=lambda record: (-record['score'],record['id']))
    return dict(hits=hits[:k], excluded_stale=stale, metadata_candidates=len(rows),
                score_meaning='Cosine similarity, not confidence or factual certainty')


def semantic_groups(units, vectors, threshold=.5, max_words=150):
    if len(units) != len(vectors) or not -1 <= threshold <= 1: raise ValueError('Invalid semantic inputs')
    vectors = [normalized(v) for v in vectors]
    if any(len(v)!=len(vectors[0]) for v in vectors): raise ValueError('Mixed dimensions')
    groups = []; current = []; words = 0; reason = 'document_start'
    for i, unit in enumerate(units):
        count = len(unit.split())
        if count > max_words: raise ValueError('A whole unit exceeds the budget; review its semantic boundaries')
        similarity = math.fsum(a*b for a,b in zip(vectors[i-1],vectors[i])) if i else 1.
        boundary = 'semantic_shift' if similarity < threshold else 'whole_unit_budget' if words+count > max_words else None
        if current and boundary:
            groups.append(dict(units=current, reason=reason));current=[];words=0;reason=boundary
        current.append(unit);words+=count
    if current: groups.append(dict(units=current,reason=reason))
    return groups


def paragraph_spans(text):
    front = re.match(r'\A---\n.*?\n---\n', text, re.S)
    offset = front.end() if front else 0
    spans = []; start = None; fence = None
    def emit(end):
        nonlocal start
        if start is not None:
            while end > start and text[end-1] in '\r\n': end -= 1
            if end > start: spans.append((start,end))
            start = None
    for line in text[offset:].splitlines(keepends=True):
        marker = re.match(r'^\s{0,3}(`{3,}|~{3,})',line)
        if fence:
            if marker and marker.group(1)[0]==fence[0] and len(marker.group(1))>=len(fence):
                emit(offset+len(line));fence=None
        elif marker:
            emit(offset);start=offset;fence=marker.group(1)
        elif not line.strip(): emit(offset)
        elif start is None: start=offset
        offset+=len(line)
    emit(len(text))
    grouped=[];i=0
    while i<len(spans):
        begin,end=spans[i]
        while i+1<len(spans) and re.fullmatch(r'(?:#{1,6}\s+|Phase \d+: )[^\n]+',text[spans[i][0]:spans[i][1]]):
            i+=1;end=spans[i][1]
        grouped.append((begin,end));i+=1
    return grouped


def model_dir(profile):
    cache = Path(os.environ.get('LOCALAPPDATA', str(Path.home()/'.cache')))
    return cache/'Mine2ndMind/models'/('all-MiniLM-L6-v2-'+profile['revision'])


def prepare_model(profile):
    directory = model_dir(profile);directory.mkdir(parents=True,exist_ok=True)
    for name, item in profile['files'].items():
        target=directory/name
        if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest()==item['sha256']:continue
        temp=directory/(name+'.download')
        try:
            with urllib.request.urlopen(item['url'],timeout=60) as response, temp.open('wb') as out:
                while block:=response.read(1024*1024):out.write(block)
            if hashlib.sha256(temp.read_bytes()).hexdigest()!=item['sha256']:raise ValueError('Model checksum mismatch')
            os.replace(temp,target)
        finally:
            if temp.exists():temp.unlink()
    return directory


class Encoder:
    def __init__(self, profile):
        import numpy as np
        import onnxruntime as ort
        from tokenizers import Tokenizer
        self.np=np;self.profile=profile;directory=model_dir(profile)
        for name, item in profile['files'].items():
            if not (directory/name).exists() or hashlib.sha256((directory/name).read_bytes()).hexdigest()!=item['sha256']:
                raise ValueError('Pinned model missing or changed; run prepare-model')
        self.tokenizer=Tokenizer.from_file(str(directory/'tokenizer.json'))
        self.tokenizer.no_truncation();self.tokenizer.enable_padding(pad_id=0,pad_token='[PAD]')
        ort.disable_telemetry_events()
        options=ort.SessionOptions();options.intra_op_num_threads=4;options.inter_op_num_threads=1
        self.session=ort.InferenceSession(str(directory/'model.onnx'),sess_options=options,providers=['CPUExecutionProvider'])

    def encode(self, texts):
        if not texts:return []
        encoded=self.tokenizer.encode_batch(texts)
        if max(len(e.ids) for e in encoded)>self.profile['max_tokens']:
            raise ValueError('Input exceeds the model token window; refine the semantic unit, never silently truncate')
        np=self.np
        candidates={'input_ids':np.array([e.ids for e in encoded],dtype=np.int64),
                    'attention_mask':np.array([e.attention_mask for e in encoded],dtype=np.int64),
                    'token_type_ids':np.array([e.type_ids for e in encoded],dtype=np.int64)}
        output=self.session.run(None,{i.name:candidates[i.name] for i in self.session.get_inputs()})[0]
        if output.ndim==3:
            mask=candidates['attention_mask'][...,None]
            output=(output*mask).sum(axis=1)/np.maximum(mask.sum(axis=1),1)
        if output.ndim!=2 or output.shape[1]!=self.profile['dimensions']:raise ValueError('Unexpected model output')
        return [normalized(v) for v in output.tolist()]


def embedding_text(record):return record['title']+'\n'+record['text']


def export_records(records, root):
    directory=Path(root)/'Atlas/Knowledge/Pilot';directory.mkdir(parents=True,exist_ok=True)
    prepared=[];names=set()
    for record in records:
        name=re.sub(r'[<>:"/\\|?*#\[\]^]','-',record['title']).strip(' .')+'.md'
        if name.casefold() in names:raise ValueError('Distillation note filenames collide')
        names.add(name.casefold())
        target=directory/name
        metadata={k:record[k] for k in ['id','kind','status','area','project','source_date','prepared_date','review_status']}
        header='---\n'+''.join(k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in metadata.items())+'---\n\n'
        c=record['citation'];path=c['path'][:-3]
        body='# '+record['title']+'\n\n'+record['text']+'\n\n## Source\n\n[['+path+'|'+Path(path).name+f']] · lines {c["start_line"]}–{c["end_line"]}\n\n'
        body+='> [!note] Status\n> This is an assistant-authored distillation. Its status describes the source’s claim; documented implementation is not a fresh runtime verification.\n'
        content=header+body
        if target.exists() and target.read_text(encoding='utf-8')!=content:raise ValueError('Edited generated note; preserve changes before rebuilding: '+name)
        prepared.append((target,content))
    for target,content in prepared:target.write_text(content,encoding='utf-8')
    export=Path(root)/'Atlas/Retrieval'
    (export/'records.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records),encoding='utf-8')
    source_keys=['title','kind','status','area','project','source_date','prepared_date','tags','citation','boundary_method']
    sources=[{k:r[k] for k in source_keys}|dict(id=r['id']+'.source',record_type='source_chunk',text=r['source_quote']) for r in records]
    (export/'source_chunks.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in sources),encoding='utf-8')


def load_records(root):
    specs=json.loads((Path(root)/'Atlas/Retrieval/pilot.json').read_text(encoding='utf-8'))
    return [materialize_record(spec,root) for spec in specs]


def main():
    if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr,'reconfigure'):sys.stderr.reconfigure(encoding='utf-8')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['prepare-model','build','search','segment','evaluate'])
    parser.add_argument('text',nargs='?');parser.add_argument('--kind');parser.add_argument('--status');parser.add_argument('--project')
    parser.add_argument('--root',type=Path,default=ROOT);parser.add_argument('--k',type=int,default=5)
    parser.add_argument('--include-evidence',action='store_true',help='Include exact source quotes in search results')
    args=parser.parse_args();root=args.root.resolve()
    profile=json.loads((root/'Atlas/Retrieval/model.json').read_text(encoding='utf-8'))
    db=root/'Atlas/Retrieval/.local/index.sqlite3'
    if args.command=='prepare-model':print(prepare_model(profile));return
    if args.command=='build':
        records=load_records(root);encoder=Encoder(profile)
        vectors=encoder.encode([embedding_text(r) for r in records]);export_records(records,root)
        write_index(records,vectors,db,profile)
        print(json.dumps(dict(records=len(records),sources=len({r['citation']['path'] for r in records}),dimensions=profile['dimensions'],database=str(db))))
    elif args.command=='search':
        if not args.text:parser.error('search requires a question')
        filters={k:getattr(args,k) for k in ['kind','status','project'] if getattr(args,k) is not None}
        result=search_index(db,Encoder(profile).encode([args.text])[0],root,profile,filters,k=args.k,include_evidence=args.include_evidence)
        print(json.dumps(result,ensure_ascii=False,indent=2))
    elif args.command=='segment':
        if not args.text:parser.error('segment requires a vault-relative source path')
        text=source_text(source_path(root,args.text));spans=paragraph_spans(text);units=[text[a:b] for a,b in spans]
        encoder=Encoder(profile);groups=semantic_groups(units,encoder.encode(units))
        # Verify complete candidate chunks fit too; never hide model-side truncation.
        encoder.encode(['\n\n'.join(g['units']) for g in groups])
        candidates=[];position=0
        for group in groups:
            start=spans[position][0];position+=len(group['units']);end=spans[position-1][1];quote=text[start:end]
            candidates.append(dict(id=text_hash(args.text+':'+str(start)+':'+quote)[:24],record_type='source_chunk',
                kind='unclassified',status='unreviewed_boundary_candidate',source_date=None,processed_at_utc=datetime.now(timezone.utc).isoformat(),
                text=quote,boundary_reason=group['reason'],boundary_method='adjacent-block neural similarity with whole-block budget',
                citation=dict(path=args.text,start_char=start,end_char=end,start_line=text.count('\n',0,start)+1,
                    end_line=text.count('\n',0,max(start,end-1))+1,source_sha256=text_hash(text),quote_sha256=text_hash(quote),
                    offset_basis='Unicode characters in UTF-8 text with BOM removed and LF newlines')))
        print(json.dumps(dict(source=args.text,method='adjacent-block neural similarity; candidates require review',chunks=candidates),ensure_ascii=False,indent=2))
    else:
        cases=json.loads((root/'Atlas/Retrieval/queries.json').read_text(encoding='utf-8'));encoder=Encoder(profile)
        vectors=encoder.encode([case['query'] for case in cases]);results=[]
        for case,vector in zip(cases,vectors):
            hits=search_index(db,vector,root,profile,case.get('filters'),k=3)['hits']
            ids=[h['id'] for h in hits];rank=ids.index(case['expected'])+1 if case['expected'] in ids else None
            results.append(case|dict(rank=rank,top_three=ids))
        report=dict(scope='Small authored pilot sanity check, not a corpus-wide benchmark',cases=len(cases),
                    top_one=sum(r['rank']==1 for r in results),top_three=sum(r['rank'] is not None for r in results),results=results)
        (root/'Atlas/Retrieval/Evaluation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,sqlite3.Error) as exc:raise SystemExit(str(exc))
