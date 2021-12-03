# OE-report-scraper

Generate Unit Test files from html reports used by the University of Óbuda.

## Usage

Requires `beautifulsoup4` to run!

Template examples can be found in the [examples](examples) directory.

`./oe_report_scraper.py -t ./examples/template.cs -o ./out.cs oehtmlreport1.html oehtmlreport2.html`

The `-t`/`--template` parameter can be omitted, then the output is written to the current working directory as `res.cs`.

### Template parameters

- `<testcase>` and `</testcase>` - Surrounds the body of the test case
- `<input>` - The unit test input from the report
- `<expected>` - The  expected output from the report
- `<num>` - Number, going from 1 and incremented for each test case
- `<inputarr>` - The unit test input from the report in array format. The line of this placeholder is used as an array item and repeated for each item.