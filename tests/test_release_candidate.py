from pathlib import Path
import unittest, hashlib, zipfile, json, re
ROOT=Path(__file__).resolve().parents[1]
SKILLS=ROOT/'skills'
ZIP=ROOT/'dist'/'cino-academy-1.2.0-review-candidate.zip'

class CandidateTests(unittest.TestCase):
    def test_six_distinct_skills(self):
        dirs=sorted(p.name for p in SKILLS.iterdir() if p.is_dir())
        self.assertEqual(dirs,['cino-academy','cino-essay-planner','cino-literature-scout','cino-literature-synthesiser','cino-reference-auditor','cino-writing-master'])
    def test_frontmatter_identity(self):
        for d in SKILLS.iterdir():
            if not d.is_dir(): continue
            s=(d/'SKILL.md').read_text('utf-8')
            self.assertTrue(s.startswith('---\n'),d)
            self.assertRegex(s,rf'(?m)^name: {re.escape(d.name)}$')
            self.assertRegex(s,r'(?m)^description: .{40,}')
            self.assertGreater(s.count('---'),1)
    def test_references(self):
        missing=[]
        for p in SKILLS.rglob('*.md'):
            s=p.read_text('utf-8')
            for ref in re.findall(r'`((?:references/|\.\./cino-academy/references/)[^\x60\s]+\.md)`',s):
                if '*' in ref: continue  # documented wildcard, not a concrete file path
                if not (p.parent/ref).resolve().is_file(): missing.append((str(p),ref))
        self.assertEqual(missing,[])
    def test_skill_roles(self):
        tests={'cino-academy':['literature-synthesiser','Research/Evidence','GenAI'],
          'cino-literature-scout':['ABSTRACT_ONLY','METADATA_ONLY','Do not'],
          'cino-literature-synthesiser':['one evidence-origin chain','thematic','UNVERIFIED'],
          'cino-reference-auditor':['APA 7','UNVERIFIED','references/APA7-CHECKLIST.md'],
          'cino-writing-master':['citation','GenAI','detectors'],
          'cino-essay-planner':['rubric','word','claim']}
        for k,words in tests.items():
            s=(SKILLS/k/'SKILL.md').read_text('utf-8')
            for w in words:self.assertIn(w,s,(k,w))
    def test_no_prohibited_inclusion(self):
        for path in SKILLS.rglob('*'):
            if path.is_file():self.assertNotIn(path.suffix.lower(),['.exe','.dll','.pyd','.pyc','.bat','.ps1'])
    def test_version_and_manifest(self):
        p=json.loads((ROOT/'plugin.json').read_text('utf-8'))
        self.assertEqual(p['version'],'1.2.0')
        self.assertEqual(p['name'],'cino-academy')
        self.assertNotIn('mcpServers',p)
        self.assertTrue((ROOT/'assets/icon.svg').is_file())
        self.assertTrue(p['extensions']['com.openai']['interface']['privacyPolicyURL'])
    def test_zip_crc_and_exact_inventory(self):
        m=json.loads((ROOT/'dist'/'CANDIDATE-MANIFEST.json').read_text('utf-8'))
        self.assertEqual(hashlib.sha256(ZIP.read_bytes()).hexdigest(),m['zip_sha256'])
        with zipfile.ZipFile(ZIP) as z:
            self.assertIsNone(z.testzip())
            self.assertEqual(set(z.namelist()),{f['path'] for f in m['files']})
            for f in m['files']:
                self.assertEqual(hashlib.sha256(z.read(f['path'])).hexdigest(),f['sha256'])
    def test_zip_without_test_artifacts(self):
        with zipfile.ZipFile(ZIP) as z:
            self.assertFalse(any('/tests/' in n or n.startswith('tests/') or '.git/' in n for n in z.namelist()))
    def test_citation_modes_distinct(self):
        s=(SKILLS/'cino-reference-auditor'/'SKILL.md').read_text('utf-8')
        for term in ['METADATA_ONLY','ABSTRACT_ONLY','USER_SUMMARY_ONLY','FULL_TEXT_INSPECTED','PARTIAL_TEXT_INSPECTED']:
            self.assertIn(term,s)
        self.assertIn('bibliographic identity',s)
    def test_assessed_writing_stop_rules(self):
        for k in ['cino-academy','cino-writing-master','cino-literature-synthesiser']:
            s=(SKILLS/k/'SKILL.md').read_text('utf-8').lower()
            self.assertIn('policy',s)
            self.assertIn('unknown',s)
    def test_package_utf8(self):
        with zipfile.ZipFile(ZIP) as z:
            for n in z.namelist():
                if n.endswith(('.md','.json','.svg')):z.read(n).decode('utf-8')

if __name__=='__main__':
    unittest.main(verbosity=2)
