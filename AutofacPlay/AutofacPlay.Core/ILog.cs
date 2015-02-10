using System;

namespace AutofacPlay.Core
{
    public interface ILog
    {
        void Log(string message);
    }

    public class ConsoleLogger: ILog
    {
        public void Log(string message)
        {
            Console.WriteLine(message);
        }
    }

    public interface ILoggerFactory
    {
        ILog CreateFor(Type containingType);
    }

    public class TypedLoggerFactory : ILoggerFactory
    {
        public ILog CreateFor(Type containingType)
        {
            return new TypedLogger(containingType);
        }
    }

    public class TypedLogger: ILog 
    {
        public TypedLogger(Type type)
        {
            TypeName = type.FullName;
        }

        public string TypeName { get; set; }

        public void Log(string message)
        {
            throw new NotImplementedException();
        }
    }
}
