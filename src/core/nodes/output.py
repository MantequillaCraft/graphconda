from dataclasses import dataclass
from src.core import BaseNode, GraphState


@dataclass
class OutputNode(BaseNode):
    output: str = ""

    def execute(self, state: GraphState) -> GraphState:
        try:
            self._log(state, 20, f"{__class__.__name__}[id={self.id}] starting ")

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

                key = text[start + 2 : end].strip()
                value = state.vars.get(key, f"<undefined:{key}>")

                value_str = str(value)
                text = text[:start] + value_str + text[end + 1 :]
                i = start + len(value_str)

            print(text)
            self._log(
                state,
                20,
                f"{__class__.__name__}[id={self.id}] completed ▶ Next[id={self.next}]",
            )
            return state
        except Exception as e:
            super()._log(state, 40, f"Error in {__class__.__name__}: {e}")
            raise RuntimeError(f"Error in {__class__.__name__}: {e}") from e
