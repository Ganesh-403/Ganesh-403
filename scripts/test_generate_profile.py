import unittest
from unittest.mock import patch
from xml.etree import ElementTree as ET
import generate_profile as profile


class ProfileTests(unittest.TestCase):
    def setUp(self):
        self.data = {'number': 42, 'title': 'Handle <script> & "quotes" in titles',
                     'url': 'https://github.com/flidai/leapview/pull/42',
                     'state': 'open', 'updated_at': '2026-09-08T00:00:00Z'}

    def test_untrusted_titles_are_text_in_both_themes(self):
        for theme in profile.THEMES:
            root = ET.fromstring(profile.activity(theme, self.data))
            self.assertFalse(any(e.tag.endswith('script') for e in root.iter()))
            self.assertIn(self.data['title'], ''.join(root.itertext()))

    def test_rejects_unexpected_links_and_states(self):
        for override in ({'url': 'https://example.com'}, {'state': 'unknown'}, {'number': -1}):
            with self.assertRaises(ValueError):
                profile.validate_activity({**self.data, **override})

    def test_private_repository_is_never_queried_for_activity(self):
        with patch('generate_profile.subprocess.check_output', return_value='{"private": true}') as call:
            with self.assertRaises(ValueError):
                profile.refresh()
            self.assertEqual(call.call_count, 1)

    def test_long_titles_and_all_artwork_are_valid_svg(self):
        data = {**self.data, 'title': 'A long pull request title ' * 100}
        out = profile.outputs(data)
        self.assertEqual(out, profile.outputs(data))
        self.assertEqual(len(out), 29)
        for name, contents in out.items():
            if name.endswith('.svg'):
                root = ET.fromstring(contents)
                self.assertEqual(root.attrib['viewBox'], '0 0 240 160' if '-mobile.svg' in name else '0 0 480 200')
                self.assertTrue(root.find('{http://www.w3.org/2000/svg}title') is not None)
        self.assertIn('…', out['assets/currently-building-dark.svg'])


if __name__ == '__main__':
    unittest.main()
