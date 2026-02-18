# Explanation: A discount function that takes any numeric type (int/float) for price & discount 

def calculate_discount(price, discount):
    return price - (price * discount / 100)

