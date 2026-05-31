def calculate(expression: str) -> str:
    try:
        # Safety: only allow math characters
        allowed = "0123456789+-*/(). "
        if not all(c in allowed for c in expression):
            return "Error: Expression contains invalid characters."

        result = eval(expression)
        return str(result)

    except Exception as e:
        return f"Error: {e}"
