import unittest
import sys
from types import ModuleType
from unittest.mock import patch


class StubModel:
    def predict(self, _texts):
        return ["Genuine"]

    def predict_proba(self, _texts):
        return [[0.5, 0.5]]


joblib_stub = ModuleType("joblib")
joblib_stub.load = lambda _path: StubModel()
sys.modules["joblib"] = joblib_stub
from analyzer import analyze_job


class AnalyzeJobConfidenceTests(unittest.TestCase):
    @patch("analyzer.model.predict_proba", return_value=[[0.95, 0.05]])
    @patch("analyzer.model.predict", return_value=["Genuine"])
    def test_high_confidence_genuine_prediction_is_preserved(
        self, _predict, _predict_proba
    ):
        result = analyze_job("Apply for the role through the company website.")

        self.assertEqual(result["ml_prediction"], "Genuine")
        self.assertEqual(result["confidence"], 95.0)
        self.assertEqual(result["confidence_note"], "")

    @patch("analyzer.model.predict_proba", return_value=[[0.539, 0.461]])
    @patch("analyzer.model.predict", return_value=["Genuine"])
    def test_low_risk_genuine_prediction_is_not_overridden_by_confidence(
        self, _predict, _predict_proba
    ):
        result = analyze_job("Apply for the role through the company website.")

        self.assertEqual(result["ml_prediction"], "Genuine")
        self.assertEqual(result["prediction"], "Genuine")
        self.assertEqual(result["confidence"], 53.9)
        self.assertIn("below 90%", result["confidence_note"])

    @patch("analyzer.model.predict_proba", return_value=[[0.05, 0.95]])
    @patch("analyzer.model.predict", return_value=["Likely Scam"])
    def test_high_confidence_scam_prediction_is_preserved(
        self, _predict, _predict_proba
    ):
        result = analyze_job("Apply for the role through the company website.")

        self.assertEqual(result["ml_prediction"], "Likely Scam")
        self.assertEqual(result["confidence"], 95.0)


if __name__ == "__main__":
    unittest.main()
