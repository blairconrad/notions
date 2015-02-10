using System.Reflection;

namespace BookFinder
{
    /// <summary>
    /// A property that proxies another one, referring instead to a property on a host object.
    /// </summary>
    public class BoundProperty : Property
    {
        private object obj;
        private PropertyInfo propertyInfo;

        /// <summary>
        /// Create a new property that proxies a property on a host object
        /// </summary>
        /// <param name="obj">the host object</param>
        /// <param name="propertyName">the name of the properhy to proxy</param>
        public BoundProperty(object obj, string propertyName)
        {
            this.obj = obj;
            this.propertyInfo = obj.GetType().GetProperty(propertyName);
        }

        /// <summary>
        /// Create a new property that proxies a property on a host object
        /// </summary>
        /// <param name="obj">the host object</param>
        /// <param name="property">the property to proxy</param>
        public BoundProperty(object obj, PropertyInfo property)
        {
            this.obj = obj;
            this.propertyInfo = property;
        }

        /// <summary>
        /// Access the proxied property - calling Value directly calls the getter or setter
        /// on the property
        /// </summary>
        public override object Value
        {
            get { return propertyInfo.GetValue(obj, null); }
            set { propertyInfo.SetValue(obj, value, null); }
        }
    }
}