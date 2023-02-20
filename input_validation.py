import re


def true_false():
    return ["yes", "y", "true", 1, "no", "n", "false", 0]


def validate_input(prompt, valid_inputs=None, cap_sense=False, input_count=None):
    if valid_inputs is None:
        valid_inputs = true_false()
        input_count = 1
        formatted_valid_inputs = format_valid_inputs(valid_inputs.copy(), cap_sense)
        input_prompt = " (y, n): "

    else:
        if not isinstance(valid_inputs, list):
            valid_inputs = [valid_inputs]
        formatted_valid_inputs = format_valid_inputs(valid_inputs.copy(), cap_sense)
        input_prompt = generate_prompt(formatted_valid_inputs)

    prompt = prompt + input_prompt

    while True:
        input_to_validate = input(prompt).rstrip(" ")
        if len(input_to_validate) == 0:
            print(f"You must write something")
            continue

        else:
            if input_to_validate[0] == "[" or "," in input_to_validate or " " in input_to_validate or isinstance(
                    input_to_validate, list):
                input_to_validate = re.split(';|,|\*|\n|\s', input_to_validate)
                for i in range(len(input_to_validate)):
                    input_to_validate[i] = input_to_validate[i].strip("[, ]")

            else:
                if not isinstance(input_to_validate, list):
                    input_to_validate = [input_to_validate]

            validated_input, valid = validate_inputs_in_list(input_to_validate, valid_inputs, formatted_valid_inputs,
                                                             cap_sense)

            if valid:
                if input_count is None or len(validated_input) == input_count:
                    if len(validated_input) == 1:
                        validated_input = validated_input[0]
                    return validated_input, True
                else:
                    print(f"{input_count} inputs expected, you gave {len(validated_input)}")
                    continue

            else:
                print(f"{validated_input} is not a valid input")
                continue


def validate_inputs_in_list(input_to_validate, valid_inputs, formatted_valid_inputs, cap_sense):
    validated_inputs = []

    for i in range(len(input_to_validate)):

        input_to_validate[i] = convert_input_type(input_to_validate[i], cap_sense)
        input_content_valid, validated_input = validate_input_content(input_to_validate[i], valid_inputs,
                                                                      formatted_valid_inputs)

        validated_inputs.append(validated_input)

        if not input_content_valid:
            return input_to_validate[i], False

        elif i == len(input_to_validate) - 1:
            return validated_inputs, True

        else:
            continue

    return input_to_validate, False


def convert_input_type(input_to_validate, cap_sense):
    try:
        input_to_validate = int(input_to_validate)
    except ValueError:
        try:
            input_to_validate = float(input_to_validate)
        except ValueError:
            try:
                input_to_validate = str(input_to_validate)
                if cap_sense is False:
                    input_to_validate = input_to_validate.lower()
            except Exception as e:
                print(f"Unknown input type, please try again:\n{e}")
    return input_to_validate


def validate_input_content(input_to_validate, valid_inputs, formatted_valid_inputs):
    if input_to_validate not in formatted_valid_inputs:
        print("Invalid input, try again")
        return False, input_to_validate

    else:
        for i in range(len(formatted_valid_inputs)):
            if formatted_valid_inputs[i] == input_to_validate:
                return True, valid_inputs[i]
            else:
                continue

    return False, input_to_validate


def format_valid_inputs(valid_inputs_to_format, cap_sense):
    for i in range(len(valid_inputs_to_format)):
        if cap_sense is False and isinstance(valid_inputs_to_format[i], str):
            try:
                valid_inputs_to_format[i] = valid_inputs_to_format[i].lower()
            except AttributeError as e:
                print(f"Formatting valid input error:\n{e}")
                pass

    return valid_inputs_to_format


def generate_prompt(formatted_valid_inputs):
    input_prompt = " ("
    for i in range(len(formatted_valid_inputs)):
        input_prompt += str(formatted_valid_inputs[i]).strip("[' ]")
        if i != len(formatted_valid_inputs) - 1:
            input_prompt += ", "
        else:
            input_prompt += "): "
    return input_prompt