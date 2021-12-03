using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;
using System.IO;

namespace Tests
{
    class Utils
    {
        public static void PerformTest(string input, string expectedResult)
        {
            File.WriteAllText("input.txt", input);

            Program.Main(Array.Empty<string>());

            string output = File.ReadAllText("output.txt");

            Assert.AreEqual(expectedResult, output);
        }
    }
	
    [TestClass]
    public class Example
    {
		<testcase>
        [TestMethod]
        [TestCategory("example")]
        public void Test_<num>()
        {
            string[] input = {
                "<inputarr>",
            };
            string expectedResult = "<expected>";
            Utils.PerformTest(string.Join("\n", input), expectedResult);
        }
		</testcase>
    }
}