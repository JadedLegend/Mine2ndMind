import json
from contextlib import closing
import math
from pathlib import Path
import sqlite3
import tempfile
import unittest

import pilot


class PilotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'source.md').write_bytes(b'Heading\r\n\r\nA complete thought.\r\n\r\nAnother thought.\r\n')
        self.spec = dict(id='one', title='One thought', source='source.md', start='A complete thought.',
                         stop='Another thought.', text='A distilled interpretation.', kind='principle',
                         status='source_interpretation', area='Skills and AI', project='Example',
                         source_date=None, tags=['example'])

    def record(self, **updates):
        return pilot.materialize_record(self.spec | updates, self.root)

    def test_citation_is_exact_with_portable_newlines_and_no_invented_date(self):
        record = self.record()
        self.assertEqual(record['source_quote'], 'A complete thought.')
        self.assertEqual(record['citation']['start_line'], 3)
        self.assertEqual(record['citation']['end_line'], 3)
        self.assertIsNone(record['source_date'])
        self.assertEqual(record['status'], 'source_interpretation')
        self.assertTrue(pilot.source_current(record, self.root))
        (self.root / 'source.md').write_text('Heading\n\nA complete thought.\n\nAnother thought.\n', encoding='utf-8')
        self.assertTrue(pilot.source_current(record, self.root))

    def test_ambiguous_or_outside_source_is_rejected(self):
        (self.root / 'source.md').write_text('A complete thought. A complete thought.', encoding='utf-8')
        with self.assertRaises(ValueError): self.record(stop=None)
        with self.assertRaises(ValueError): self.record(source='../outside.md')

    def test_changed_source_is_excluded_from_results(self):
        r = self.record()
        db = self.root / 'index.sqlite3'
        pilot.write_index([r], [[1., 0.]], db, {'id': 'test'})
        (self.root / 'source.md').write_text('Changed source.', encoding='utf-8')
        result = pilot.search_index(db, [1., 0.], self.root, {'id': 'test'})
        self.assertEqual(result['hits'], [])
        self.assertEqual(result['excluded_stale'], 1)

    def test_metadata_filters_apply_before_ranking_and_rebuild_removes_old_rows(self):
        a = self.record()
        b = self.record(id='two', kind='hypothesis', status='proposed')
        db = self.root / 'index.sqlite3'
        profile = {'id': 'test'}
        pilot.write_index([a, b], [[1., 0.], [0., 1.]], db, profile)
        result = pilot.search_index(db, [0., 1.], self.root, profile, filters={'kind': 'principle'})
        self.assertEqual([r['id'] for r in result['hits']], ['one'])
        self.assertNotIn('source_quote', result['hits'][0])
        evidence = pilot.search_index(db, [1., 0.], self.root, profile, include_evidence=True)
        self.assertEqual(evidence['hits'][0]['source_quote'], a['source_quote'])
        with self.assertRaises(ValueError): pilot.search_index(db, [1., 0.], self.root, {'id': 'different'})
        with self.assertRaises(ValueError): pilot.search_index(db, [1., 0., 0.], self.root, profile)
        pilot.write_index([a], [[1., 0.]], db, profile)
        with closing(sqlite3.connect(db)) as conn: self.assertEqual(conn.execute('select count(*) from records').fetchone()[0], 1)

    def test_invalid_vectors_do_not_replace_a_working_index(self):
        db = self.root / 'index.sqlite3'
        pilot.write_index([self.record()], [[1., 0.]], db, {'id': 'test'})
        before = db.read_bytes()
        with self.assertRaises(ValueError): pilot.write_index([self.record()], [[math.nan, 0.]], db, {'id': 'test'})
        self.assertEqual(db.read_bytes(), before)

    def test_semantic_boundary_splits_between_whole_units(self):
        units = ['The first complete thought.', 'Its related explanation.', 'A different topic starts here.']
        groups = pilot.semantic_groups(units, [[1., 0.], [.99, .1], [0., 1.]], threshold=.5, max_words=100)
        self.assertEqual([g['units'] for g in groups], [units[:2], units[2:]])
        self.assertEqual(groups[1]['reason'], 'semantic_shift')
        with self.assertRaises(ValueError): pilot.semantic_groups(['word ' * 101], [[1., 0.]], max_words=100)

    def test_changed_source_requires_review_before_rebuilding_distillation(self):
        record = self.record()
        self.spec['source_sha256'] = record['citation']['source_sha256']
        (self.root / 'source.md').write_text('Heading\n\nA complete thought. With a changed meaning.\n\nAnother thought.\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Source changed'): self.record()

    def test_block_spans_keep_code_whole_and_attach_heading_context(self):
        text = '---\ntitle: Example\n---\n\n# Heading\n\nOne paragraph.\n\n```py\nx = 1\n\nx = 2\n```\n\nLast paragraph.\n'
        spans = pilot.paragraph_spans(text)
        units = [text[start:end] for start,end in spans]
        self.assertEqual(units, ['# Heading\n\nOne paragraph.', '```py\nx = 1\n\nx = 2\n```', 'Last paragraph.'])

    def test_invalid_filter_and_unrelated_database_are_rejected(self):
        db = self.root / 'index.sqlite3'
        pilot.write_index([self.record()], [[1., 0.]], db, {'id': 'test'})
        with self.assertRaises(ValueError): pilot.search_index(db, [1., 0.], self.root, {'id': 'test'}, {'unsupported': 'value'})
        other = self.root / 'other.sqlite3'
        with closing(sqlite3.connect(other)) as conn: conn.execute('create table user_data (value text)')
        before = other.read_bytes()
        with self.assertRaises(ValueError): pilot.write_index([self.record()], [[1., 0.]], other, {'id': 'test'})
        self.assertEqual(other.read_bytes(), before)

    def test_colliding_note_names_fail_before_overwriting_a_distillation(self):
        (self.root / 'Atlas/Retrieval').mkdir(parents=True)
        a = self.record(id='a', title='One/Idea')
        b = self.record(id='b', title='One:Idea')
        with self.assertRaisesRegex(ValueError, 'collide'): pilot.export_records([a,b], self.root)
        self.assertEqual(list((self.root / 'Atlas/Knowledge/Pilot').glob('*.md')), [])


if __name__ == '__main__': unittest.main()
