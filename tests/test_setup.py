import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('profile_setup',ROOT/'setup.py')
setup=importlib.util.module_from_spec(spec);spec.loader.exec_module(setup)

class SetupTests(unittest.TestCase):
    def setUp(self):self.temp=tempfile.TemporaryDirectory();self.home=Path(self.temp.name)
    def tearDown(self):self.temp.cleanup()
    def test_clean_and_repeat_install(self):
        self.assertTrue(setup.run('install',self.home)['files_ok'])
        self.assertTrue(setup.run('install',self.home)['files_ok'])
        self.assertEqual(len(list((self.home/'.claude/skills').glob('*/SKILL.md'))),3)
    def test_existing_rules_and_settings_preserved_and_restored(self):
        folder=self.home/'.claude';folder.mkdir();rules=folder/'CLAUDE.md';rules.write_text('existing rules')
        settings=folder/'settings.json';settings.write_text('{"unrelated":true}')
        setup.run('install',self.home);setup.run('install',self.home)
        self.assertTrue(rules.read_text().startswith('existing rules'))
        self.assertEqual(rules.read_text().count('@claude-setting/instructions.md'),1)
        self.assertEqual(settings.read_text(),'{"unrelated":true}')
        self.assertFalse(setup.run('uninstall',self.home)['conflicts'])
        self.assertEqual(rules.read_text(),'existing rules')
    def test_owner_changes_refused_and_preserved(self):
        setup.run('install',self.home);p=self.home/'.claude/skills/project-check/SKILL.md';p.write_text('owner edit')
        with self.assertRaisesRegex(ValueError,'OWNER_EDIT'):setup.run('install',self.home)
        self.assertIn('.claude/skills/project-check/SKILL.md',setup.run('uninstall',self.home)['conflicts'])
        self.assertEqual(p.read_text(),'owner edit')
    def test_foreign_skill_is_not_overwritten(self):
        p=self.home/'.claude/skills/frontend-work/SKILL.md';p.parent.mkdir(parents=True);p.write_text('existing')
        with self.assertRaisesRegex(ValueError,'EXISTING_SKILL'):setup.run('install',self.home)
        self.assertEqual(p.read_text(),'existing');self.assertFalse((self.home/'.claude/CLAUDE.md').exists())
    def test_install_lock_refuses_concurrent_operation(self):
        p=self.home/'.claude/.claude-setting.lock';p.parent.mkdir();p.write_text('locked')
        with self.assertRaises(FileExistsError):setup.run('install',self.home)
    def test_manifest_only_contains_claude_text_files(self):
        manifest=setup.load(ROOT/'manifest.json')
        for rel,digest in manifest['files'].items():
            self.assertTrue(rel.startswith('.claude/'));self.assertEqual(setup.sha((ROOT/'profile'/rel).read_bytes()),digest)
            self.assertNotIn('auth',rel);self.assertTrue(rel.endswith('.md'))

if __name__=='__main__':unittest.main()
