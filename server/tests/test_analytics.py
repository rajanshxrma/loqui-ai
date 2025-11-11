from services.analytics import Analytics


class TestAnalytics:
    def test_initial_state(self):
        a = Analytics()
        assert a.total_requests == 0
        assert a.total_errors == 0

    def test_on_request_increments(self):
        a = Analytics()
        a.on_request(model="gpt-4o", language="en")
        a.on_request(model="claude-3.5-sonnet", language="es")
        assert a.total_requests == 2

    def test_model_usage_tracking(self):
        a = Analytics()
        a.on_request(model="gpt-4o", language="en")
        a.on_request(model="gpt-4o", language="fr")
        a.on_request(model="claude-3.5-sonnet", language="en")
        assert a.model_usage["gpt-4o"] == 2
        assert a.model_usage["claude-3.5-sonnet"] == 1

    def test_language_usage_tracking(self):
        a = Analytics()
        a.on_request(model="gpt-4o", language="en")
        a.on_request(model="gpt-4o", language="en")
        a.on_request(model="gpt-4o", language="ja")
        assert a.language_usage["en"] == 2
        assert a.language_usage["ja"] == 1

    def test_error_rate(self):
        a = Analytics()
        a.on_request(model="gpt-4o", language="en")
        a.on_request(model="gpt-4o", language="en")
        a.on_error(model="gpt-4o")
        assert a.get_error_rate() == 0.5

    def test_error_rate_no_requests(self):
        a = Analytics()
        assert a.get_error_rate() == 0.0

    def test_summary(self):
        a = Analytics()
        a.on_request(model="gpt-4o", language="en")
        a.on_success()
        summary = a.get_summary()
        assert summary["total_requests"] == 1
        assert "model_usage" in summary
        assert "language_usage" in summary
        assert "avg_response_time" in summary
