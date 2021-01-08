
def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x if x.isupper() else x.title() for x in components[1:])
