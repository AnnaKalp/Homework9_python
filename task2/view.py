def get_value():
    print("Привет,это калькулятор.")
    kind_operation = input("Для комплексных чисел нажми 1, для рациональных 2: ")
    
    while True:
        inp = input("Пожалуйста, вводите числа отделяя от знака операции пробелом: ")
        try_act = inp
        data = try_act.split()

        if len(data) == 3:
            if data[1] == "+" or data[1] == "-" or data[1] == "*" or data[1] == "/":
                break

        print("Ваш ввод неверен, попробуйте ещё раз.")

    return inp, kind_operation



def output(result):
    try:
        if result.is_integer():
            print(f"Your result is:", int(result))
        elif isinstance(result, float):
            print(f"Your result is:", result)
        else: print(result)
    except:
        print(result)