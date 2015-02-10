using System;
using System.Collections;

namespace BookFinder
{
    /// <summary>
    /// A representation of a property on an object - can be used to proxy properties, 
    /// to create a "data-binding" effect.
    /// </summary>
    public abstract class Property
    {
        /// <summary>
        /// Access the proxied property
        /// </summary>
        public abstract object Value { get; set; }

        public static implicit operator string(Property prop)
        {
            return (string) prop.Value;
        }

        public static implicit operator bool(Property prop)
        {
            return (bool) prop.Value;
        }

        /// <summary>
        /// Return the property as a list - if the property has a non-list value, this
        /// will result in an <see cref="InvalidCastException"/> if the property value
        /// isn't an <see cref="IList"/>
        /// </summary>
        /// <remaks>This would be an implicit conversion if user-created implicit conversions
        /// to interfaces were allowed.</remaks>
        public IList AsList()
        {
             return (IList) Value;
        } 
    }
}
