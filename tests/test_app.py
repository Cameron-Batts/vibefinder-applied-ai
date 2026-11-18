"""Test the Streamlit app. Skipped when Streamlit is not installed."""

from pathlib import Path

import pytest

pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest  # noqa: E402

APP = str(Path(__file__).resolve().parents[1] / "app.py")


def test_app_shows_ok_for_default_request():
    at = AppTest.from_file(APP, default_timeout=30).run()
    assert not at.exception
    assert "Status: ok" in at.success[0].value


def test_app_warns_for_unknown_labels():
    at = AppTest.from_file(APP, default_timeout=30).run()
    at.selectbox(key="genre").select("Other (type your own)").run()
    at.text_input(key="genre_text").input("opera").run()
    assert any("needs_review" in item.value for item in at.warning)


def test_app_blocks_invalid_energy():
    at = AppTest.from_file(APP, default_timeout=30).run()
    at.checkbox[0].check().run()
    assert "Status: blocked" in at.error[0].value
