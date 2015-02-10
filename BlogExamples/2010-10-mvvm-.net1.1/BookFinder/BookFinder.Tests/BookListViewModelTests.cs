using System.Windows.Forms;
using NUnit.Framework;

namespace BookFinder.Tests
{
    [TestFixture]
	public class BookListViewModelTests
	{
        [Test]
        public void FindClick_WithTitleG_FindsEndersGame()
        {
            BookListViewModel vm = new BookListViewModel(new Control(), new FakeBookDepository());
            vm.TitleText = "G";
            vm.FindClick(null, null);

            Assert.IsTrue(vm.BookListItems.Contains("Ender's Game"));
        }
	}
}
