import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import ast

class PandasParser:

    def __init__(self, json_output: dict):
        self.df = pd.read_csv('files/input/2fccfd0e-f03a-4043-b323-2db0b6a072b0.csv', encoding='utf-8', delimiter=';')
        self.data = json_output

    def parse(self) -> None:
        local_vars = {"df": self.df}
        results = []

        for command in data["commands"]:
            try:
                if self._is_expression(command):
                    print(f'{command} command is expression')
                    result = eval(command, local_vars)
                    results.append(f"{result}")
                else:
                    exec(command, local_vars)
            except Exception as ex:
                results.append(f"{command} = ERROR: {ex}")

        output_string = "\n".join(results)
        print(output_string)
            

    def _is_expression(self, command: str) -> bool:
        try:
            parsed = ast.parse(command)
            return isinstance(parsed.body[0], ast.Expr)
        except:
            return False


if __name__ == '__main__':
    data = {
        "type": "TEXT",
        "commands": [
            "df[df['YEAR_ID'] == 2003]['SALES'].sum()",
            "df[df['YEAR_ID'] == 2003]['SALES'].mean()",
            "df[df['YEAR_ID'] == 2003].groupby('MONTH_ID')['SALES'].sum().idxmax()",
            "df[df['YEAR_ID'] == 2003].groupby('MONTH_ID')['SALES'].sum().idxmin()",
            "sum_2004 = df[df['YEAR_ID'] == 2004]['SALES'].sum()",
            "sum_2004"
        ]
    }

    parser = PandasParser(json_output=data).parse()