import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
import numpy as np
import pandas as pd
from typing import Literal

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from table_generator import MarkdownTable


class MarkdownTableTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.base_path = Path(self.temp_dir.name)
        self.md_file = self.base_path / "report.md"
        self.md_file.write_text("# Report\n", encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    def generate_table(self, data_file:str, align:Literal["left", "center", "right"]="center", 
                       line_num=0, append=True, col_headers=[], excel_sheets=[]):
        
        MarkdownTable(str(data_file), str(self.md_file), align, line_num, 
                      append, col_headers, excel_sheets,)
        return self.md_file.read_text(encoding="utf-8")


    def test_csv_no_given_headers(self):
        data_file = self.base_path / "data.csv"
        data_file.write_text("Name,Score\nAda,10\nGrace,12\n", encoding="utf-8")

        content = self.generate_table(str(data_file))

        self.assertIn(
            "| Name | Score |\n| :-: | :-: |\n| Ada | 10 |\n| Grace | 12 |",
            content,
        )


    def test_csv_with_given_headers(self):
        data_file = self.base_path / "data.csv"
        data_file.write_text("Name,Score,Rank\nAda,10,2\nGrace,12,1\n", encoding="utf-8")

        content = self.generate_table(str(data_file), align="right", col_headers=["Rank", "Name"])

        self.assertIn( "| Rank | Name |\n| -: | -: |\n| 2 | Ada |\n| 1 | Grace |", content)


    def test_line_insertion(self):
        self.md_file.write_text("First\nSecond\nThird\n", encoding="utf-8")
        data_file = self.base_path / "data.csv"
        data_file.write_text("Name,Score\nAda,10\n", encoding="utf-8")

        content = self.generate_table( str(data_file), align="left", line_num=2, 
                                      append=False, col_headers=["Name", "Score"])

        self.assertTrue(content.startswith("First\n\n| Name | Score |"))
        self.assertIn("| :- | :- |\n| Ada | 10 |", content)
        self.assertTrue(content.endswith("\nSecond\nThird\n"))

    def test_np_array(self):
        data_file = self.base_path / "data.npy"
        np.save(data_file, np.array([[1, 2], [3, 4]]))

        content = self.generate_table(str(data_file), col_headers=["A", "B"])

        self.assertIn("| A | B |\n| :-: | :-: |\n| 1 | 2 |\n| 3 | 4 |", content)

    def test_np_array_transposed(self):
        data_file = self.base_path / "data.npy"
        np.save(data_file, np.array([[1, 2, 3], [4, 5, 6]]))

        with redirect_stdout(io.StringIO()):
            content = self.generate_table(str(data_file), col_headers=["A", "B"])

        self.assertIn("| A | B |\n| :-: | :-: |\n| 1 | 4 |\n| 2 | 5 |\n| 3 | 6 |", content)

    def test_excel_given_sheets_headers(self):
        data_file = self.base_path / "data.xlsx"
        with pd.ExcelWriter(data_file) as writer:
            pd.DataFrame({"Name": ["Ada"], "Score": [10]}).to_excel(
                writer, sheet_name="Scores", index=False
            )
            pd.DataFrame({"Name": ["Ignored"], "Score": [0]}).to_excel(
                writer, sheet_name="Other", index=False
            )

        content = self.generate_table(str(data_file), col_headers=["Name", "Score"], excel_sheets=["Scores"])

        self.assertIn("| Name | Score |\n| :-: | :-: |\n| Ada | 10 |", content)
        self.assertNotIn("Ignored", content)

    def test_np_array_no_headers_assert_error(self):
        data_file = self.base_path / "data.npy"
        np.save(data_file, np.array([[1]]))

        with self.assertRaises(SystemExit) as raised, redirect_stdout(io.StringIO()) as output:
            MarkdownTable(str(data_file), str(self.md_file), "center", 0, True, [], [])

        self.assertEqual(raised.exception.code, 1)
        self.assertIn("Column headers must be given for NumPy file.", output.getvalue())


    def test_given_wrong_header_assert_error(self):
        data_file = self.base_path / "data.csv"
        data_file.write_text("Name,Score\nAda,10\n", encoding="utf-8")

        with self.assertRaises(SystemExit) as raised, redirect_stdout(io.StringIO()) as output:
            MarkdownTable(str(data_file), str(self.md_file), "center", 0, True, ["Missing"], [])

        self.assertEqual(raised.exception.code, 1)
        self.assertIn( 'Category "Missing" is not a column header in', output.getvalue())


if __name__ == "__main__":
    unittest.main()
