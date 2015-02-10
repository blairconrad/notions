using System;
using System.Reflection;
using System.Collections;

namespace BookFinder.Tests
{
   public class ValuePropertyBinder
   {
         public static void Bind(ViewModelBase viewModel)
         {
             foreach ( FieldInfo field in viewModel.PropertyFields() )
             {
                 ValuePropertyStrategy propertyStorageStrategy = new ValuePropertyStrategy(MakeStartingValue(field.FieldType));

                 ConstructorInfo propertyConstructor = field.FieldType.GetConstructor(new Type[] {typeof (PropertyStorageStrategy)});
                 object propertyField = propertyConstructor.Invoke(new object[] {propertyStorageStrategy});
                 field.SetValue(viewModel, propertyField);
             }
         }

         private static object MakeStartingValue(Type fieldType)
         {
            Type propertyType = fieldType.GetProperty("Value").PropertyType;
            
            if ( propertyType == typeof(IList) ) { return new ArrayList(); }
            if ( propertyType == typeof(string) ) { return ""; }
            if ( propertyType == typeof(bool) ) { return false; }
            else { return null; }
         }
   }
}
