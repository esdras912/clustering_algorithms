import random
def random_color_generator():
    data = []; return_data = []
    with open("./colors.txt","r", encoding="utf-8") as f:
        
        for x in f:
            data.append(str(x))
        
        for clean in data:
            return_data.append(clean[0:-1])
   
    color = return_data[random.randint(0,len(return_data))]
    print(color)
