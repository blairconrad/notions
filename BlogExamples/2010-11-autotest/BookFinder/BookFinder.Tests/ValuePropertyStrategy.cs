namespace BookFinder.Tests
{
   public class ValuePropertyStrategy: PropertyStorageStrategy 
   {
         private object obj;

         /// <summary>
         /// Create a new property that proxies a property on a host object
         /// </summary>
         /// <param name="initialValue">the initial value</param>
         public ValuePropertyStrategy(object initialValue)
         {
            this.obj = initialValue;
         }

         public void Set(object value)
         {
            obj = value;
         }

         public object Get()
         {
            return obj;
         }
   }
}
