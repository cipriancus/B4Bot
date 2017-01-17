

def get_most_frequent_response(input_statement, response_list):
    matching_response = None
    occurrence_count = -1


    for statement in response_list:
        count = statement.get_response_count(input_statement)

        if count >= occurrence_count:
            matching_response = statement
            occurrence_count = count

    return matching_response


def get_first_response(input_statement, response_list):
    return response_list[0]


def get_random_response(input_statement, response_list):
    from random import choice
    return choice(response_list)
