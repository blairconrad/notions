using System;
using System.Collections;
using System.Windows.Forms;
using BookFinder;

namespace BookFinder
{
    public class BookListViewModel : ViewModelBase
    {
        private Property titleText = new StorageProperty(string.Empty);
        public string TitleText
        {
            get { return titleText; }
            set { titleText.Value = value; }
        }

        private Property findEnabled = new StorageProperty(false);
        public bool FindEnabled
        {
            get { return findEnabled; }
            set { findEnabled.Value = value; }
        }

        private Property bookListItems = new StorageProperty(new ArrayList());
        public IList BookListItems
        {
            get { return bookListItems.AsList(); }
            set { bookListItems.Value = value; }
        }


        private Property bookListSelectedItems = new StorageProperty(new ArrayList());
        public IList BookListSelectedItems
        {
            get { return bookListSelectedItems.AsList();}
            set { bookListSelectedItems.Value = value;}
        }

        private Property detailsText = new StorageProperty("");
        public string DetailsText
        {
            get { return detailsText; }
            set { detailsText.Value = value; }
        }

        IBookDepository bookDepository;
        public BookListViewModel(Control view, IBookDepository bookDepository)
            :base(view)
        {
           this.bookDepository = bookDepository;
           BindToView();
        }

        public void TitleTextChanged(object sender, EventArgs e)
        {
            string newText = TitleText;
            FindEnabled= newText != null & newText.Length > 0;
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
            ICollection books = bookDepository.Find(TitleText);
            BookListItems.Clear();
            foreach ( string book in books )
            {
                BookListItems.Add(book);
            }
        }

        public void BookListSelectedIndexChanged(object sender, EventArgs e)
        {
           string book = (string) BookListSelectedItems[0];
           DetailsText = bookDepository.Details(book);
        }

    }
}
