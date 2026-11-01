import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class SiteTests(unittest.TestCase):
    def test_site_has_two_distinct_enquiry_paths_and_gallery(self):
        page = (ROOT / 'index.html').read_text() if (ROOT / 'index.html').exists() else ''
        for item in ('Enquire to buy', 'Enquire to stay', 'wa.me/919811458901', 'id="gallery"', 'assets/'):
            self.assertIn(item, page)

if __name__ == '__main__':
    unittest.main()
