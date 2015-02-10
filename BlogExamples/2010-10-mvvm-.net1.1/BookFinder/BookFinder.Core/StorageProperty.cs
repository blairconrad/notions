using BookFinder;

namespace BookFinder
{
    /// <summary>
    /// A <see cref="Property"/> implementation that provides its
    /// own storage for the <see cref="Value"/>.
    /// </summary>
    public class StorageProperty: Property
    {
        private object value;

        public StorageProperty(object value)
        {
            this.value = value;
        }

        public override object Value
        {
            get { return value; }
            set { this.value = value; }
        }
    }
}

