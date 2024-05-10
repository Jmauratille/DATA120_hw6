def make_change(total):
    coins = [1, 5, 10, 25, 100]
    
    def change_recursion(remainder, current_combo, start):
        if remainder == 0:
            result.append(current_combo.copy())
            return
        if remainder < 0:
            return

        for i in range(start, len(coins)):
            coin = coins[i]
            current_combo.append(coin)
            change_recursion(remainder - coin, current_combo, i)
            current_combo.pop()

    result = []
    change_recursion(total, [], 0)
    return result


def checker(name, abbrev):
    return abbrev[0] == "I" and name[1] == "l"

def dict_filter(function, dictionary):
    result = {}
    for key, item in dictionary.items():
        if function(key, item) == True:
            result[key] = item
    return result


def treemap(function, tree):
    for child in tree.children:
        treemap(function, child)

    tree.key, tree.value = function(tree.key, tree.value)
    return tree


class DTree:
    def __init__(self, variable, threshold, lessequal, greater, outcome=None):
        if outcome is not None and (variable is not None or threshold is not None or lessequal is not None or greater is not None):
            raise ValueError
        if outcome is None and (variable is None or threshold is None or lessequal is None or greater is None):
            raise ValueError

        self.variable = variable
        self.threshold = threshold
        self.lessequal = lessequal
        self.greater = greater
        self.outcome = outcome

    def tuple_atleast(self):
        if self.outcome is not None:
            return 0 

        max_index = self.variable
        if self.lessequal:
            max_index = max(max_index, self.lessequal.tuple_atleast())
        if self.greater:
            max_index = max(max_index, self.greater.tuple_atleast())
        
        return max_index + 1  

    def find_outcome(self, observations):
        if self.outcome is not None:
            return self.outcome

        if observations[self.variable] <= self.threshold:
            return self.lessequal.find_outcome(observations)
        else:
            return self.greater.find_outcome(observations)

    def no_repeats(self):
        def helper(node, seen_variables):
            if node.outcome is not None:
                return True

            if node.variable in seen_variables:
                return False
            else:
                seen_variables.add(node.variable)
                left_check = helper(node.lessequal, seen_variables.copy())
                right_check = helper(node.greater, seen_variables.copy())
                return left_check and right_check
        
        return helper(self, set())