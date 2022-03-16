def preprocess(input_text, debug):
    if debug is True:
        print(f'**** PREPROCESSOR ****\n\nInput text before preprocessing:\n---\n{input_text}\n---\n')
    line_not_empty = False
    should_skip = False
    result_string = ''
    for char in input_text:
        # <#> character
        if char == '#':
            should_skip = True
        # <\n> character
        elif char == '\n':
            if line_not_empty is True or (line_not_empty is False and should_skip is False):
                result_string += char
            line_not_empty = False
            should_skip = False
        # normal characters
        elif should_skip is False and char.isprintable() and not char.isspace():
            if line_not_empty is False:
                line_not_empty = True
            result_string += char
            
    if debug is True:
        print(f'Input text after preprocessing:\n---\n{result_string}\n---\n')
    return result_string
                    
        