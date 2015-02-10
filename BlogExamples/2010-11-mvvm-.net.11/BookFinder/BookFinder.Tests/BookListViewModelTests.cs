using System.Windows.Forms;
using NUnit.Framework;

namespace BookFinder.Tests
{
   [TestFixture]
   public class BookListViewModelTests
   {
         private BookListViewModel vm;
         [SetUp]
         public void SetUp()
         {
            vm = new BookListViewModel(new Control(), new FakeBookDepository());
            ValuePropertyBinder.Bind(vm);
         }

         [Test]
         public void FindClick_WithTitleG_FindsEndersGame()
         {
            vm.TitleText.Value = "G";
            vm.FindClick(null, null);

            Assert.IsTrue(vm.BookListItems.Value.Contains("Ender's Game"));
         }

         [Test]
         public void FindClick_WithTitleZ_DoesNotFindEndersGame()
         {
            vm.TitleText.Value = ("Z");
            vm.FindClick(null, null);

            Assert.IsFalse(vm.BookListItems.Value.Contains("Ender's Game"));
         }
   }
}
