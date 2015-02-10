using Autofac;
using AutofacPlay.Core;

namespace ResolveDependencies
{
    public class Play
    {
        public static void Main()
        {
            var builder = new ContainerBuilder();
            builder.RegisterType<ConsoleLogger>().As<ILog>();
            builder.RegisterType<PerformanceLog>().As<IPerformanceLog>();

            using (var container = builder.Build())
            {
                var greeter = container.Resolve<IPerformanceLog>();
                greeter.Begin("hippo");
            }
            System.Console.ReadKey();
        }
    }
}