using System.Collections;

namespace BookFinder
{
    public class BookDepository: IBookDepository
    {
        static IDictionary details;


        public BookDepository()
        {
            details = new Hashtable();
            details["The Time Traveler's Wife"] = "naked in the Newberry";
            details["Ender's Game"] = "little kid saves the world";
            details["Maus"] = "why pigs?";
        }

        public ICollection Find(string titleSubstring)
        {
            ArrayList titles = new ArrayList();
            foreach ( string title in details.Keys )
            {
                if ( title.IndexOf(titleSubstring) >= 0 )
                {
                    titles.Add(title);
                }
            }
            return titles;
        }

        public string Details(string title)
        {
            return (string) details[title];
        }
    }
}