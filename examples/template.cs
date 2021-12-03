using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;
using System.IO;

namespace Tests
{
    class Utils
    {
        public static void PerformTest(string input, string expectedResult)
        {
            using StringReader tr = new StringReader(input);
            using StringWriter sw = new StringWriter();
            Console.SetOut(sw);
            Console.SetIn(tr);

            Program.Main(Array.Empty<string>());
            Assert.AreEqual(expectedResult, sw.ToString());
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
            string input = "<input>";
            string expectedResult = "<expected>";
            Utils.PerformTest(input, expectedResult);
        }
		</testcase>
    }
}