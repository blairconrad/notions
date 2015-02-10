using System;
using System.Collections;
using System.Windows.Forms;
using BookFinder;

namespace BookFinder
{
    public class BookListViewModel : ViewModelBase
    {
        public StringProperty TitleText;
        public BoolProperty FindEnabled;
        public ListProperty BookListItems;
        public ListProperty BookListSelectedItems;
        public StringProperty DetailsText;

        IBookDepository bookDepository;
        public BookListViewModel(Control view, IBookDepository bookDepository)
            :base(view)
        {
            this.bookDepository = bookDepository;
            BindToView();
        }

        public void TitleTextChanged(object sender, EventArgs e)
        {
            string newText = TitleText.Value;
            FindEnabled.Value = (newText != null & newText.Length > 0);
        }

        public void TitleKeyPress(object sender, KeyPressEventArgs e)
        {
            if ( e.KeyChar == (char) Keys.Enter )
            {
                FindClick(null, null);
            }
        }

        public void FindClick(object sender, EventArgs e)
        {
            ICollection books = bookDepository.Find(TitleText.Value);
            IList bookListItems = BookListItems.Value;

            bookListItems.Clear();
           foreach ( string book in books )
           {
               bookListItems.Add(book);
           }
        }

        p ublic void BookListSelectedIndexChanged(object sender, EventArgs e)
        {
            string book = (string) BookListSelectedItems.Value[0];
            DetailsText.Value = bookDepository.Details(book);
        }
    }
}
