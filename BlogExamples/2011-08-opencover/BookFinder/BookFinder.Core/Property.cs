using System.Collections;

namespace BookFinder
{
    public abstract class Property
    {
        protected PropertyStorageStrategy storage;

        protected Property(PropertyStorageStrategy storage)
        {
            this.storage = storage;
        }
    }

    public class StringProperty : Property
    {
        public StringProperty(PropertyStorageStrategy storage) : base(storage)
        {}

        public string Value
        {
            get { return (string) storage.Get(); }
            set { storage.Set(value); }
        }
    }

    public class BoolProperty : Property
    {
        public BoolProperty(PropertyStorageStrategy storage) : base(storage)
        {}

        public bool Value
        {
            get { return (bool) storage.Get(); }
            set { storage.Set(value); }
        }
    }

    public class ListProperty : Property
    {
        public ListProperty(PropertyStorageStrategy storage) : base(storage)
        {}

        public IList Value
        {
            get { return (IList) storage.Get(); }
            set { storage.Set(value); }
        }
    }
}
