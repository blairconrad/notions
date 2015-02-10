namespace BookFinder
{
    public interface PropertyStorageStrategy
    {
        object Get();
        void Set(object value);
    }
}