using System;
using System.Windows.Forms;

namespace BookFinder
{
	/// <summary>
	/// Summary description for BookListView.
	/// </summary>
	public class BookListView : System.Windows.Forms.Form
	{
        private System.Windows.Forms.TextBox Title;
        private System.Windows.Forms.Button Find;
        private System.Windows.Forms.ListBox BookList;
        private System.Windows.Forms.TextBox Details;
		/// <summary>
		/// Required designer variable.
		/// </summary>
		private System.ComponentModel.Container components = null;

		public BookListView()
		{
			//
			// Required for Windows Form Designer support
			//
			InitializeComponent();

			//
			// TODO: Add any constructor code after InitializeComponent call
			//
		}

		/// <summary>
		/// Clean up any resources being used.
		/// </summary>
		protected override void Dispose( bool disposing )
		{
			if( disposing )
			{
				if (components != null) 
				{
					components.Dispose();
				}
			}
			base.Dispose( disposing );
		}

		#region Windows Form Designer generated code
		/// <summary>
		/// Required method for Designer support - do not modify
		/// the contents of this method with the code editor.
		/// </summary>
		private void InitializeComponent()
		{
            this.Title = new System.Windows.Forms.TextBox();
            this.Find = new System.Windows.Forms.Button();
            this.BookList = new System.Windows.Forms.ListBox();
            this.Details = new System.Windows.Forms.TextBox();
            this.SuspendLayout();
            // 
            // Title
            // 
            this.Title.Location = new System.Drawing.Point(16, 16);
            this.Title.Name = "Title";
            this.Title.Size = new System.Drawing.Size(256, 20);
            this.Title.TabIndex = 0;
            this.Title.Text = "";
            // 
            // Find
            // 
            this.Find.Enabled = false;
            this.Find.Location = new System.Drawing.Point(304, 16);
            this.Find.Name = "Find";
            this.Find.Size = new System.Drawing.Size(96, 24);
            this.Find.TabIndex = 1;
            this.Find.Text = "Find";
            // 
            // BookList
            // 
            this.BookList.Location = new System.Drawing.Point(24, 56);
            this.BookList.Name = "BookList";
            this.BookList.Size = new System.Drawing.Size(248, 251);
            this.BookList.TabIndex = 2;
            // 
            // Details
            // 
            this.Details.Enabled = false;
            this.Details.Location = new System.Drawing.Point(304, 56);
            this.Details.Multiline = true;
            this.Details.Name = "Details";
            this.Details.Size = new System.Drawing.Size(100, 256);
            this.Details.TabIndex = 3;
            this.Details.Text = "";
            // 
            // BookListView
            // 
            this.AutoScaleBaseSize = new System.Drawing.Size(5, 13);
            this.ClientSize = new System.Drawing.Size(448, 350);
            this.Controls.Add(this.Details);
            this.Controls.Add(this.BookList);
            this.Controls.Add(this.Find);
            this.Controls.Add(this.Title);
            this.Name = "BookListView";
            this.Text = "BookListView";
            this.ResumeLayout(false);

        }
		#endregion
	}
}
