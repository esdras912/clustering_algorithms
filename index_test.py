test = [67,45,24,47,657]
to_find = 657
position = test.index(to_find)
max_val = test.index(max(test))
print(test[max_val])
print(f"El valor {to_find} esta en la posicion: {position}")