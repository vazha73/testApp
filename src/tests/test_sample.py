def func(x):
    return x + 2

def test_answer():
    assert func(3) == 5
    
class TestClass:
    def test_one(self):
        x = "this"
        assert "h" in x

    def test_two(self):
        x = "hello"
        assert not hasattr(x, "check")