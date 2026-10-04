import pytest

from stack_mashine import stack_mashine, Stack

@pytest.fixture()
def stack():
  stack = Stack()
  stack.push(1)
  stack.push(2)
  return stack

class TestStack:
  def test_stack_creation(self, stack):
    assert Stack().size() == 0


  def test_stack_push(self, stack):
    stack.push(3)
    assert stack.last_value() == 3
    assert stack.size() == 3

  def test_stack_pop(self, stack):
    pop_val = stack.pop()
    assert pop_val == 2
    assert stack.last_value() == 1
    assert stack.size() == 1

  def test_stack_size(self, stack):
    s = stack
    assert stack.size() == 2

  def test_stack_sum(self, stack):
    s = stack
    assert s.sum() == 3


@pytest.mark.parametrize(
    "expression, expected",
    [
      ("7", 7),
      ("3 4 +", 7),
      ("5 2 -", 3),
      ("2 5 -", -3),
      ("3 4 *", 12),
      ("8 2 /", 4),
      ("2 4 /", 0.5),
      ("3 4 + 2 *", 14),
      ("1 2 + 5 3 - *", 6),
      ("5 2 ~", 3),
      ("2 5 ~", 3),
      ("4 4 ~", 0),
      ("3 5 0 ~ +", 12),
      ("5 2 ~ 4+", 7),
      ("3 0 4 ~ 2 ~", 7),
      ("2 2 + 4 - 4 ~ 2 3 * +", 6),
      ("1 2 3 +", 5),  # результат - вершина стека
    ]
)
def test_stack_mashine(expression, expected):
  assert stack_mashine(expression) == expected


@pytest.mark.parametrize(
    "expression, error",
    [
      ("", ValueError),
      ("+", ValueError),
      ("1+", ValueError),
      ("~", ValueError),
      ("1 ~", ValueError),
      ("1 2 a +", ValueError),
      ("5 0 /", ZeroDivisionError),
    ]
)
def test_stack_mashine_errors(expression, error):
  with pytest.raises(error):
    stack_mashine(expression)


@pytest.mark.parametrize("expression", [None, 123, ["3", "4", "+"]])
def test_stack_mashine_rejects_non_string(expression):
  with pytest.raises(TypeError):
    stack_mashine(expression)
