import pytest

from toolmaster_of_brainerd import toolmaster_of_brainerd


class TestToolmasterofbrainerd:
    def test_add_unit(self):
        res = toolmaster_of_brainerd.add(2, 3)
        assert res == 5

    @pytest.mark.skip(reason="Test skiping test")
    def test_skip(self):
        assert False
