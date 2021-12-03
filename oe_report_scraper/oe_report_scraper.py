#!/usr/bin/env python3

# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY
# without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import argparse
import os
from typing import List

from bs4 import BeautifulSoup
from bs4.element import Tag


class TestCase:
    input: str
    expected: str

    def __init__(self, input, expected) -> None:
        self.input = input
        self.expected = expected

    def input_as_string(self) -> str:
        return str.replace(self.input, "\n", "\\n")

    def input_as_array(self) -> List[str]:
        return str.splitlines(self.input)


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--template",
                        help="path to the template file", required=True)
    parser.add_argument("-o", "--out", help="path to the output file")
    parser.add_argument("files", nargs="*", help="html reports to process")
    return parser


def scape_reports(paths: List[str]) -> List[TestCase]:
    test_cases: List[TestCase] = []

    for path in paths:
        with open(path, encoding="utf-8") as f:
            report = f.read()

        bs = BeautifulSoup(report, "html.parser")
        content_div = bs.find("div", class_="content")
        tests_card_div = content_div.find(
            "b", text="Unit Tests").parent.parent.parent

        tests_body_div = tests_card_div.find("div", class_="card-body")

        test_div: Tag
        for test_div in tests_body_div.find_all("div", class_="card-body"):
            input = test_div.find(
                "dt", text="Input:").find_next_sibling().getText()
            #input = input.replace("\n", "\\n")

            expected = test_div.find(
                "dt", text="Expected Output:").find_next_sibling().getText()
            #expected = expected.replace("\n", "\\n")

            test_cases.append(TestCase(input, expected))

    return test_cases


def build_from_template(test_cases: List[TestCase], template: str) -> str:
    tc_tag_start = "<testcase>"
    tc_tag_end = "</testcase>"
    tc_start = template.find(tc_tag_start)
    tc_end = template.find(tc_tag_end)

    if(tc_start < 0 or tc_start > tc_end):
        raise ValueError("<testcase> tags are not in corect place or missing")

    inner = template[tc_start + len(tc_tag_start):tc_end - 1]

    counter = 1
    result: str = template[0:tc_start - 1]
    for tc in test_cases:
        new_test_case = ""
        new_test_case = inner \
            .replace("<input>", tc.input) \
            .replace("<expected>", tc.expected) \
            .replace("<num>", str(counter))

        new_test_case = gen_inputarr(new_test_case, tc.input_as_array())

        result += new_test_case
        counter += 1

    result += template[tc_end + len(tc_tag_end):]
    return result


def gen_inputarr(template: str, tc_input: List[str]) -> str:
    ret = ""
    for line in template.splitlines(True):
        if("<inputarr>" in line):
            ret += gen_array_line(line, tc_input)
        else:
            ret += line
    return ret


def gen_array_line(line: str, arr_lines: List[str]) -> str:
    ret: List[str] = []
    for arr_ln in arr_lines:
        ret.append(str.replace(line, "<inputarr>", arr_ln))
    return str.join("", ret)


def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()

    with open(args.template, encoding="utf-8") as f:
        template = f.read()

    test_cases = scape_reports(args.files)
    output_text = build_from_template(test_cases, template)

    if(args.out):
        out_path = args.out
    else:
        out_path = os.path.join(os.getcwd(), "res.cs")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(output_text)


if __name__ == "__main__":
    main()
