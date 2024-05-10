def make_change(total):
    """
    Generate all distinct combinations of coins that add up to the
    specified total.

    Args:
    total (int): The total amount for which change is to be made.

    Returns:
    list of lists: A list containing all combinations of coins that sum up
    to the total.
    """
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
    """
    Filter a dictionary based on a function that takes two parameters
    and returns a boolean.

    Args:
    function (callable): A function to test each dictionary item.
    dictionary (dict): Dictionary to filter.

    Returns:
    dict: Filtered dictionary.
    """
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
    """
    Decision tree for modeling decisions based on comparison of thresholds.

    Args:
    variable (int): Index of the tuple to be inspected.
    threshold (float): Threshold for decision branching.
    lessequal (DTree): Subtree for values less than or equal to the threshold.
    greater (DTree): Subtree for values greater than the threshold.
    outcome (str, optional): Final decision if this is a leaf node.

    Raises:
    ValueError: If the initialization parameters are incorrectly provided.
    """
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
        left_depth = self.lessequal.tuple_atleast() if self.lessequal else 0
        right_depth = self.greater.tuple_atleast() if self.greater else 0
        max_child_depth = max(left_depth, right_depth)

        if self.variable is not None:
            return max(max_child_depth, self.variable + 1)
        return max_child_depth

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
