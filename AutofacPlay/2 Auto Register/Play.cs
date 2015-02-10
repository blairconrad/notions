using Autofac;
using AutofacPlay.Core;

namespace AutofacPlay
{
	public class Play
	{
		public static void Main()
		{
			var builder = new ContainerBuilder();
            builder.RegisterAssemblyTypes(typeof(ILog).Assembly).AsImplementedInterfaces();
			
			using ( var container = builder.Build() )
			{
				var greeter = container.Resolve<IPerformanceLog>();
				greeter.Begin("hippo");
			}
            System.Console.ReadKey();
        }
	}
}