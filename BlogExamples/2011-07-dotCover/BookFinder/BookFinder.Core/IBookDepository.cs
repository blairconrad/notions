using System.Collections;

namespace BookFinder
{
    public interface IBookDepository
    {
        ICollection Find(string titleSubstring);
        string Details(string title);
    }
}