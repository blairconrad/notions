using System.Reflection;
using System.Collections;

namespace BookFinder
{
    /// <summary>
   /// A property that proxies another one, referring instead to a property on a host object.
   /// </summary>
   public class BoundPropertyStrategy: PropertyStorageStrategy 
   {
         private object obj;
         private PropertyInfo propertyInfo;

         /// <summary>
         /// Create a new property that proxies a property on a host object
         /// </summary>
         /// <param name="obj">the host object</param>
         /// <param name="property">the property to proxy</param>
         public BoundPropertyStrategy(object obj, PropertyInfo property)
         {
            this.obj = obj;
            this.propertyInfo = property;
         }

         public void Set(object value)
         {
            propertyInfo.SetValue(obj, value, null);
         }

         public object Get()
         {
            return propertyInfo.GetValue(obj, null); 
         }
   }
}
