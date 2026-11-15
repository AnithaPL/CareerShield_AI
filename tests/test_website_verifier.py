import unittest

from website_verifier import verify_website


class VerifyWebsiteTests(unittest.TestCase):
    def test_https_url_is_valid(self):
        result = verify_website("https://www.ambitionbox.com/")

        self.assertTrue(result["valid_format"])
        self.assertTrue(result["uses_https"])
        self.assertEqual(result["domain"], "www.ambitionbox.com")

    def test_http_url_is_invalid_and_reports_https_disabled(self):
        result = verify_website("http://www.exportersindia.com/")

        self.assertFalse(result["valid_format"])
        self.assertFalse(result["uses_https"])
        self.assertEqual(result["domain"], "www.exportersindia.com")
        self.assertIn("HTTPS is disabled", result["message"])

    def test_url_without_scheme_defaults_to_https(self):
        result = verify_website("www.ambitionbox.com")

        self.assertTrue(result["valid_format"])
        self.assertTrue(result["uses_https"])
        self.assertEqual(result["url"], "https://www.ambitionbox.com")

    def test_malformed_url_is_invalid(self):
        result = verify_website("not-a-url")

        self.assertFalse(result["valid_format"])
        self.assertTrue(result["uses_https"])
        self.assertFalse(result["https_disabled"])
        self.assertEqual(result["message"], "Invalid website URL.")


if __name__ == "__main__":
    unittest.main()
