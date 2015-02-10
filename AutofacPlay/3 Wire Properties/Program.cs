using System.IO;
using Autofac;
using AutofacPlay.Core;

namespace AutofacPlay.WireProperties
{

    class Program
    {
        static void Main()
        {
            var builder = new ContainerBuilder();
            
            builder.RegisterAssemblyTypes(typeof(ILog).Assembly).AsImplementedInterfaces().PropertiesAutowired().SingleInstance();
            
            builder.RegisterAssemblyTypes(typeof(ILog).Assembly).AsSelf().PropertiesAutowired().SingleInstance();

            builder.RegisterType<ConsoleLogger>().As<ILog>().InstancePerDependency();

            builder.RegisterInstance(System.Console.Out).As(typeof (TextWriter));
            
            

            using (var container = builder.Build())
            {
                var service = container.Resolve<BaseService>();
                service.Log.Log("I'm logging");

                var greetingService = container.Resolve<GreetingService>();
                greetingService.Writer = System.Console.Out;
                greetingService.PerformanceLog.Begin("greeting");
                greetingService.Greet();
                System.Console.Out.WriteLine(ReferenceEquals(greetingService.Log, service.Log));
                greetingService.PerformanceLog.End("greeting");



            }
            System.Console.ReadKey();
        }
    }
}
