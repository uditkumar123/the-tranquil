import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class SiteTests(unittest.TestCase):
    def test_site_has_two_distinct_enquiry_paths_and_gallery(self):
        page = (ROOT / 'index.html').read_text() if (ROOT / 'index.html').exists() else ''
        for item in ('Enquire to buy', 'Enquire to stay', 'wa.me/919811458901', 'id="gallery"', 'assets/'):
            self.assertIn(item, page)

    def test_gallery_is_browsable_and_uses_local_images_with_alt_text(self):
        from html.parser import HTMLParser

        class GalleryParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.in_gallery = False
                self.images = []
                self.buttons = []

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if tag == 'section' and attrs.get('id') == 'gallery':
                    self.in_gallery = True
                if self.in_gallery and tag == 'img':
                    self.images.append(attrs)
                if self.in_gallery and tag in ('button', 'a'):
                    self.buttons.append(attrs)

            def handle_endtag(self, tag):
                if tag == 'section' and self.in_gallery:
                    self.in_gallery = False

        parser = GalleryParser()
        parser.feed((ROOT / 'index.html').read_text())
        self.assertGreaterEqual(len(parser.images), 4)
        self.assertTrue(all(i.get('alt') and (ROOT / i['src']).is_file() for i in parser.images))
        self.assertTrue(all(i.get('role') == 'button' and i.get('aria-label') for i in parser.images))

    def test_location_section_uses_confirmed_address_and_directions_link(self):
        page = (ROOT / 'index.html').read_text()
        self.assertIn('id="location"', page)
        self.assertIn('Duwakoti, Uttarakhand, India', page)
        self.assertIn('maps.google.com/?q=', page)

    def test_video_uses_existing_snow_footage_with_controls_and_poster(self):
        page = (ROOT / 'index.html').read_text()
        self.assertIn('<video class="film" controls playsinline', page)
        self.assertIn('video/Snow.mp4', page)
        self.assertIn('poster="assets/property-5.jpg"', page)

    def test_buy_and_stay_enquiries_have_distinct_prefilled_messages(self):
        page = (ROOT / 'index.html').read_text()
        self.assertIn('enquire%20about%20buying', page)
        self.assertIn('enquire%20about%20a%20stay', page)

if __name__ == '__main__':
    unittest.main()
