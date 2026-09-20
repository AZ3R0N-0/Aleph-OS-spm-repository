
print('--- Calculator ---')
print("type 'exit' to exit calculator")
print()
while True:
  try:
    num1 = float(input('First number: '))
    op = input('Operation (+ - * / ** //): ')
    num2 = float(input('Second number: '))
    if op == '+':
      print(f'Result: {num1 + num2}')
    elif op == '-':
      print(f'Result: {num1 - num2}')
    elif op == '*':
      print(f'Result: {num1 * num2}')
    elif op == '/':
      print(f'Result: {num1 / num2}')
    elif op == '**':
      print(f'Result: {num1 ** num2}')
    elif op == '//':
      print(f'Result: {num1 // num2}')
    elif op == 'exit' or num1 == 'exit' or num2 == 'exit:
      break
    else:
      raise ValueError('invalid operator')
    print('\\033[2m~\\033[0m')
  except Exception as e:
    print(f'[ERROR]: {e}')
