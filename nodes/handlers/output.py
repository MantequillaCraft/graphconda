from dataclasses import dataclass
from nodes.base import BaseNode, GraphState


@dataclass
class OutputNode(BaseNode):
    output: str = ""

    def execute(self, state: GraphState) -> GraphState:
        try:
            super().execute(state)
            text = self.output

            i = 0
            while True:
                start = text.find("${", i)
                if start == -1:
                    break

                end = text.find("}", start + 2)
                if end == -1:
                    break

                key = text[start + 2:end].strip()
                value = state.vars.get(key, f"<undefined:{key}>")

                value_str = str(value)
                text = text[:start] + value_str + text[end + 1:]
                i = start + len(value_str)

            print(text)
            return state
        except Exception as e:
            raise RuntimeError(f"Error in OutputNode: {e}") from e