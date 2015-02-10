using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using NUnit.Framework;
using Autofac;
using AutofacPlay.Core;

namespace AutofacPlay.Core
{
    [TestFixture]
    public class TestAssumptions
    {
        [Test]
        public void TwoBuilders_SingletonsAreDifferent()
        {
            var builder1 = new ContainerBuilder();
            builder1.RegisterType<ConsoleLogger>().As<ILog>().SingleInstance();
            var container1 = builder1.Build();
            ILog log1 = container1.Resolve<ILog>();

            var builder2 = new ContainerBuilder();
            builder2.RegisterType<ConsoleLogger>().As<ILog>().SingleInstance();
            var container2 = builder2.Build();
            ILog log2 = container2.Resolve<ILog>();

            Assert.That(log1, Is.Not.SameAs(log2));
        }

        [Test]
        public void OneBuilder_SingletonsAreSame()
        {
            var builder = new ContainerBuilder();
            builder.RegisterType<ConsoleLogger>().As<ILog>().SingleInstance();
            var container1 = builder.Build();
            ILog log1 = container1.Resolve<ILog>();
            ILog log2 = container1.Resolve<ILog>();
            Assert.That(log1, Is.SameAs(log2));
        }

        [Test]
        public void InstancePerDependency_GetsSamePropertyInstancesEvenIfSingleton()
        {
            var builder = new ContainerBuilder();
            builder.RegisterType<ConsoleLogger>().As<ILog>().SingleInstance();
            builder.RegisterType<BaseService>().InstancePerDependency().PropertiesAutowired();

            var container1 = builder.Build();
            BaseService service1 = container1.Resolve<BaseService>();
            BaseService service2 = container1.Resolve<BaseService>();
            Assert.That(service1, Is.Not.SameAs(service2));
            Assert.That(service1.Log, Is.SameAs(service2.Log));
        }

    }
}
