"""
Name:                       Katasha Kime
Date:                       10/19/2020
Description:                Program takes in a data file and processes which items each family member should carry,
                            depending on their weight capacity and maximum value.
"""


def main():
    process_file("data.txt")


def process_file(data_file):
    """
       Takes a data file and processes each line while writing the output to a file.
       :param data_file: user-defined file
    """

    # read file
    infile = open(data_file, "r")

    num_cases = int(infile.readline().strip())

    test_cases = {}
    index = 0

    # grab data from file
    for line in infile:
        case = []

        # grab num of items
        num_items = int(line.strip())

        prices = []
        weights = []

        # grab the prices and weights
        for i in range(num_items):
            # split whitespace
            price_weight = infile.readline().strip()
            price_weight = price_weight.split(' ')

            # convert to integers
            price_weight[0] = int(price_weight[0])
            prices.append(price_weight[0])

            price_weight[1] = int(price_weight[1])
            weights.append(price_weight[1])

        case.append(prices)
        case.append(weights)

        # grab the capacities
        num_capacities = int(infile.readline().strip())

        max_capacities = []

        for i in range(num_capacities):
            capacity = int(infile.readline().strip())
            max_capacities.append(capacity)

        case.append(max_capacities)

        test_cases[index] = case
        index += 1

    # close file
    infile.close()

    out = ""

    # iterate through test cases and grab the prices and items
    for i in range(len(test_cases)):
        case = test_cases[i]
        results = shopping(case[0], case[1], case[2])

        out += "Test Case: " + str(i + 1) + "\n"
        out += "Total Price: " + str(results[0]) + "\n"
        out += "Member Items:" + "\n"

        # iterate through capacities - add person to out
        for i in range(len(results[1])):
            out += str(i + 1) + ": "
            items = results[1][i]

            for j in range(len(items)):
                if items[j] == 1:
                    out += str(j) + " "

            out += "\n"

        out += "\n"

        # iterate through items, add carried items to out

    outfile = open("results.txt", "w")
    outfile.write(out)
    outfile.close()
    print(out)


def shopping(prices, weights, capacities):
    """
    Computes and prints the optimal amount of items each family member should carry to obtain a maximum total price, constrained by
    the maximum amount each family member can carry.
    :param prices: given set of prices for each item
    :param weights: given set of weights for each item
    :param capacities: given set of maximum capacity for each family member
    :return: List of item distributions for each family member
    """
    total_price = 0

    # calculate max price per capacity
    max_prices = calculate_max_price(prices, weights, max(capacities))

    # determine which items are included for each capacity
    items = []

    for i in range(len(capacities)):
        # grab the price at this capacity
        price = max_prices[len(prices) - 1][capacities[i]]
        total_price += price

        # grab the items
        carried_items = get_items(max_prices, weights, capacities[i])
        items.append(carried_items)

    # return values
    return [total_price, items]


def calculate_max_price(prices, weights, capacity):
    """
    Builds a spread of maximum prices based on a range of capacities
    :param prices: given set of prices for each item
    :param weights: given set of weights for each item
    :param capacity: given capacity
    :return: grid of maximum prices to capacity
    """
    # insert 0 at first value of prices and weights
    prices.insert(0, 0)
    weights.insert(0, 0)

    # build price distribution grid
    max_prices = []

    for i in range(len(prices)):
        temp = []

        for j in range(capacity + 1):
            temp.append(float('-inf'))

        max_prices.append(temp)

    # calculate values
    # iterate through items
    item = 0
    while item < len(weights):

        # iterate through capacities
        cap = 0
        while cap < len(max_prices[0]):

            if item == 0 or cap == 0:
                max_prices[item][cap] = 0

            # if the item can still fit, the maximum price is either without the item or with the item
            # (plus whatever optimal price you can get at remaining weight)
            elif weights[item] <= cap:
                max_prices[item][cap] = max(max_prices[item - 1][cap], max_prices[item - 1][cap - weights[item]] +
                                            prices[item])

            # if weight is greater than capacity, use previous maximum price
            else:
                max_prices[item][cap] = max_prices[item - 1][cap]

            cap += 1

        item += 1

    return max_prices


def get_items(price_distribution, weights, capacity):
    """
    Determines the items carried at a given capacity that maximizes total price.
    :param price_distribution: data of maximum price
    :param prices: list of prices per item
    :param weights: list of weights per item
    :param capacity: given capacity
    :return: a list of items that are present (or not) in the carried items
    """
    item = len(price_distribution) - 1
    cap = capacity
    items = []

    for weight in weights:
        items.append(0)

    # iterate backwards through items
    while item > 0:

        # compare max price at current item (and capacity) to previous item
        curr_price = price_distribution[item][cap]
        prev_price = price_distribution[item - 1][cap]
        
        # if prices are the same, item is not included
        if curr_price == prev_price:
            items[item] = 0

        # if items are different, item is included
        else:
            items[item] = 1

            # subtract current item's weight from current capacity
            cap -= weights[item]

        # iterate backwards
        item -= 1

    return items


if __name__ == "__main__":
    main()


