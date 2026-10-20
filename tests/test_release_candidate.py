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
                # Catch a modified SKILL.md even when the previous ZIP/manifest are internally consistent.
                current=(ROOT/f['path']).read_bytes().replace(b'\r\n',b'\n')
                self.assertEqual(z.read(f['path']),current,f['path'])
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
    def test_openai_submission_metadata_limits(self):
        p=json.loads((ROOT/'plugin.json').read_text('utf-8'))
        ui=p['extensions']['com.openai']['interface']
        for field,limit in [('displayName',30),('shortDescription',30),
                            ('developerName',80),('longDescription',4000)]:
            self.assertTrue(ui.get(field),field)
            self.assertLessEqual(len(ui[field]),limit,(field,len(ui[field])))
        self.assertEqual(ui['category'],'Productivity')
        prompts=ui.get('defaultPrompt',[])
        self.assertTrue(1<=len(prompts)<=3)
        self.assertEqual(len(set(prompts)),len(prompts))
        self.assertTrue(all(0<len(v)<=128 for v in prompts))
        self.assertTrue(all(str(ui[f]).startswith('https://')
                            for f in ['websiteURL','supportURL','privacyPolicyURL','termsOfServiceURL']))
        self.assertEqual(p['extensions']['com.openai']['publication'].get('countries'),None)
        for attr in ['logo','composerIcon']:
            self.assertTrue(ui[attr].startswith('./assets/'))
            self.assertTrue((ROOT/ui[attr]).is_file())
        svg=(ROOT/ui['logo']).read_text(encoding='utf-8')
        self.assertIn('viewBox="0 0 64 64"',svg)
        self.assertNotIn('<script',svg.lower())

    def test_release_receipt_matches_zip(self):
        record=json.loads((ROOT/'RELEASE.json').read_text('utf-8'))
        self.assertFalse(record['accepted'])
        self.assertFalse(record['published'])
        self.assertFalse(record['submitted_to_openai'])
        self.assertEqual(record['public_zip_sha256'],hashlib.sha256(ZIP.read_bytes()).hexdigest())

    def test_cross_platform_archive_format(self):
        with zipfile.ZipFile(ZIP) as z:
            for info in z.infolist():
                self.assertEqual(info.create_system,3)
                self.assertEqual(info.compress_type,zipfile.ZIP_STORED)
                self.assertEqual(info.date_time,(2020,1,1,0,0,0))
                self.assertNotIn(b'\r\n',z.read(info))

    def test_native_fixture_coverage_and_separation(self):
        cases=json.loads((ROOT/'tests/fixtures/native_cases.json').read_text('utf-8'))
        self.assertGreaterEqual(len(cases),10)
        ids=[c['id'] for c in cases]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual({c['target'] for c in cases},
                         {p.name for p in SKILLS.iterdir() if p.is_dir()})
        self.assertTrue(all(len(c['prompt'])>80 and c.get('required') for c in cases))
        self.assertFalse(any('real client' in c['prompt'].lower() for c in cases if c['id']=='A10'))

    def test_single_claim_support_vocabulary(self):
        auditor=(SKILLS/'cino-reference-auditor'/'SKILL.md').read_text('utf-8')
        reference=(SKILLS/'cino-academy'/'references'/'SOURCE-ACCESS.md').read_text('utf-8')
        allowed={'SUPPORTED','PARTIALLY_SUPPORTED','UNSUPPORTED','CONTRADICTED','UNVERIFIED'}
        for forbidden in [
            'MATCHES_USER_PROVIDED_TEXT','VERIFIED_IN_SOURCE',
            'CONTRADICTED_BY_SUPPLIED_EXCERPT','UNSUPPORTED_BY_SUPPLIED_EXCERPT',
            'USER_SUPPLIED_PUBLICATION_TYPE','NOT_INDEPENDENTLY_FETCHED'
        ]:
            self.assertNotIn(forbidden,auditor,forbidden)
        self.assertIn('comparison_note',auditor)
        self.assertIn('support_state=UNVERIFIED',auditor)
        self.assertIn('attribution_verification=NOT_VERIFIED',auditor)
        self.assertIn('USER_SUPPLIED_UNCONFIRMED',auditor)
        for status in allowed:self.assertIn(status,reference)
        self.assertIn('Publication-attributed support_state stays UNVERIFIED',reference)

    def test_synthetic_synthesis_does_not_upgrade_source_support(self):
        synth=(SKILLS/'cino-literature-synthesiser'/'SKILL.md').read_text('utf-8')
        for rule in ['support_state=UNVERIFIED','attribution_verification=NOT_VERIFIED',
                     'comparison_note','estimands','independent evidence origins']:
            self.assertIn(rule,synth)
        self.assertIn('not as PARTIALLY_SUPPORTED',synth)
        self.assertIn('cannot establish decay or persistence',synth)

    def test_package_utf8(self):
        with zipfile.ZipFile(ZIP) as z:
            for n in z.namelist():
                if n.endswith(('.md','.json','.svg')):z.read(n).decode('utf-8')

if __name__=='__main__':
    unittest.main(verbosity=2)
