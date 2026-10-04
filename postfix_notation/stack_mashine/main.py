import operator

class Stack:

  def __init__(self):
    self.items = []

  def push(self, value: int):
    self.items.append(value)

  def __str__(self):
    return "Stack - (" + ", ".join(map(str, self.items)) + ")"

  def pop(self):
    last_value = self.items.pop()
    return last_value

  def last_value(self):
    return self.items[-1]

  def size(self):
    return len(self.items)

  def sum(self):
    return sum(self.items)

# def switch_val(num1, num2):
#   num1 = int(num1)
#   num2 = int(num2)
#   if num1 < num2:
#     return num2, num1
#   return num1, num2

def stack_mashine(expression: str):
  stack = Stack()
  ops = {
      '+': operator.add,
      '-': operator.sub,
      '*': operator.mul,
      '/': operator.truediv,
  }
  if not isinstance(expression, str):
    raise TypeError("Выражение должно быть строкой")

  expression = expression.strip()
  if not expression:
    raise ValueError("Выражение не должно быть пустым")

  for ind, val in enumerate(expression):
    if val.isspace():
      continue

    if val.isdigit():
      stack.push(int(val))
    elif val in ops or val == "~":
      if stack.size() < 2:
        raise ValueError(
          f"Недостаточно операндов для операции '{val}' (позиция {ind}): "
          "вначале должны идти значения, потом операции"
        )
      first_val = stack.pop()
      second_val = stack.pop()
      if val == "~":
        if first_val != 0 and second_val != 0:
          stack.push(abs(first_val - second_val))
        else:
          stack.push(stack.sum()**2)
      else:
        try:
          stack.push(ops[val](second_val, first_val))
        except ZeroDivisionError:
          raise ZeroDivisionError(f"Деление на ноль (позиция {ind})") from None
    else:
      raise ValueError(f"Недопустимый символ '{val}' (позиция {ind})")
    print(f"{ind}: {stack}")

  if stack.size() != 1:
    raise ValueError(
      f"В выражении лишние операнды, на стеке осталось {stack.size()} значений"
    )
  return stack.pop()


if __name__ == "__main__":
  expression = input("Введите выражение, записанное в постфиксной нотации через пробел : ")
  result = stack_mashine(expression)
  print(f"{expression} = {result}")
