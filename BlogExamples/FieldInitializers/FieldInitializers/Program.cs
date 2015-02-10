using System;

namespace FieldInitializers
{
    class Print
    {
        public Print(string message)
        {
            Console.Out.WriteLine(message);
        }
    }

    class Base
    {
        public Print baseField = new Print("Base Field");
        public Base()
        {
            new Print("Base Constructor");
        }
    }

    class Derived: Base
    {
        public Print derivedField = new Print("Derived Field");
        public Derived()
        {
            new Print("Derived Constructor");
        }
    }

    class ReflectorBase
    {
        public Print baseField;
        public ReflectorBase()
        {
            baseField = new Print("ReflectorBase Field");
            new Print("ReflectorBase Constructor");
        }
    }

    class ReflectorDerived: ReflectorBase
    {
        public Print derivedField;
        public ReflectorDerived()
        {
            derivedField = new Print("ReflectorDerived Field");
            new Print("ReflectorDerived Constructor");
        }
    }

    class Program
    {
        static void Main()
        {
            new Derived();
            Console.Out.WriteLine("");
            Console.Out.WriteLine("");
            new ReflectorDerived();
        }
    }
}
