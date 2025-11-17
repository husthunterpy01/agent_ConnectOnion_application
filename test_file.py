from connectonion import Agent

class Calculator:
    def __init__(self):
        self.history = []  # Shared context across tool calls

    def calculate(self, expression: str) -> str:
        """Evaluate a mathematical expression"""
        result = str(eval(expression))
        self.history.append(f"{expression} = {result}")
        return result

    def get_history(self) -> str:
        """Get calculation history"""
        return "\n".join(self.history)

calc = Calculator()

# Agent = Prompt + Class (uses all public methods)
agent = Agent("You are a helpful assistant", tools=calc)

calc_result = agent.input("What's 42 * 17?")
agent.input("Show me the history")
print(calc_result)
# History persists across calls!