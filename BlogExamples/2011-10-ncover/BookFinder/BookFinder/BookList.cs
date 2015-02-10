using System;
using System.Collections;
using System.Windows.Forms;
using BookFinder;

namespace BookFinder
{
	public class BookList
	{
           /// <summary>
           /// The main entry point for the application.
           /// </summary>
           [STAThread]
           private static void Main()
           {
              IBookDepository depository = new BookDepository();
              BookListView view = new BookListView();
               
              new BookListViewModel(view, depository);
              Application.Run(view);
           }
        }
}

