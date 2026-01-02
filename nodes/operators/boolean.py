import ast
import operator

# Operadores de comparación: <, <=, >, >=, ==, !=, in, not in, is, is not
CMP = {
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.In: lambda a, b: a in b,
    ast.NotIn: lambda a, b: a not in b,
    ast.Is: operator.is_,
    ast.IsNot: operator.is_not,
}

# Operadores booleanos: and, or
BOOL = {
    ast.And: all,
    ast.Or: any,
}

# Operadores unarios: not, +, -
UNARY = {
    ast.Not: operator.not_,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Métodos seguros para strings
SAFE_STR_METHODS = {
    "islower", "isupper", "isdigit", "isalpha", "isalnum", "isspace",
    "startswith", "endswith", "strip", "lstrip", "rstrip",
    "lower", "upper", "find", "count", "replace",
}

# Funciones globales permitidas
SAFE_GLOBAL_FUNCS = {
    "len": len,
    "int": int,
    "float": float,
    "str": str,
    "bool": bool,
}