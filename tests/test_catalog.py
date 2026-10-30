import sys
import unittest
from pathlib import Path
from urllib.parse import urlparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from build_navigator import catalog, rows, embed_url

class CatalogTests(unittest.TestCase):
    def setUp(self): self.data=catalog()
    def test_complete_path(self):
        self.assertEqual([s['id'] for s in self.data['stages']],list(range(12)))
        self.assertTrue(all(s['task'] and s['evidence'] for s in self.data['stages']))
    def test_catalog_preserves_original_links(self):
        urls={r['url'] for r in self.data['resources']}
        for name in ['community-learning-resources.csv','video-resources.csv','roadmap-references.csv']:
            self.assertTrue({r['URL'] for r in rows(name)} <= urls)
        self.assertEqual(len(urls),len(self.data['resources']))
    def test_identifiers_and_phases(self):
        r=self.data['resources'];self.assertEqual(len({x['id'] for x in r}),len(r))
        self.assertTrue(all(x['phases'] and x['levels'] for x in r))
        self.assertTrue(all(0<=p<12 for x in r for p in x['phases']))
    def test_embed_allowlist(self):
        self.assertIsNone(embed_url('https://youtube.com.evil.example/watch?v=gojeTqXdBH0'))
        self.assertIsNone(embed_url('https://example.com/'))
        self.assertEqual(embed_url('https://youtu.be/gojeTqXdBH0'),'https://www.youtube-nocookie.com/embed/gojeTqXdBH0')
        self.assertTrue(all(urlparse(x['embed']).hostname=='www.youtube-nocookie.com' for x in self.data['resources'] if x['embed']))

if __name__=='__main__':unittest.main()
