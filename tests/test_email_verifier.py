import unittest

from email_verifier import verify_email


class VerifyEmailTests(unittest.TestCase):
    def test_public_provider_is_invalid_for_recruiter_domain_verification(self):
        result = verify_email("hr.globaljobs@gmail.com")

        self.assertFalse(result["valid_format"])
        self.assertEqual(result["domain"], "gmail.com")
        self.assertEqual(result["email_type"], "Public Email Provider")
        self.assertIn("Use the organization's domain", result["message"])

    def test_domain_specific_address_shows_its_domain(self):
        result = verify_email("hr@renaultgroup.com")

        self.assertTrue(result["valid_format"])
        self.assertEqual(result["domain"], "renaultgroup.com")
        self.assertEqual(result["email_type"], "Domain-Specific Email")
        self.assertIn("does not prove", result["message"])

    def test_invalid_address_has_no_detected_domain(self):
        result = verify_email("recruitment.abc")

        self.assertFalse(result["valid_format"])
        self.assertEqual(result["domain"], "")
        self.assertEqual(result["email_type"], "Unknown")


if __name__ == "__main__":
    unittest.main()
