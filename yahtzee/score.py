
# Rules for scoreboard fields
# rules = {
#     'A': lambda x: x,
#     'D': lambda x: 2 * x,
#     'S': lambda x: x ** 2,
# }

rules = {
    'A': lambda t: sum(t),
    'D': lambda t: 2 * sum(t),
    'S': lambda t: sum(t) ** 2,
}
