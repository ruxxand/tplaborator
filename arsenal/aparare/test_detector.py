from collections import Counter
import pytest
from arsenal.aparare.detector import suspecti

# Test 1: Verificam daca pragul taie elementele sub valoarea specificata
def test_pragul_taie():
    c = Counter({"a": 13, "b": 2})
    assert suspecti(c, 10) == [("a", 13)]

# Test 2: Verificam daca pragul invalid ridica exceptia ValueError
def test_prag_invalid():
    with pytest.raises(ValueError):
        suspecti({}, 0)
