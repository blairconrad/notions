using Autofac;
using NUnit.Framework;

namespace Hide_Private_Component
{
    public interface IDoSomething
    {
        void Do();
    }

    public class NullDoSomething
    {
        private class Impl : IDoSomething
        {
            private Impl() { }
            public static IDoSomething Create()
            {
                return new Impl();
            }
            public void Do() { }
        }

        public static readonly IDoSomething Service = Impl.Create();
    }
    public class PublicDoSomething : IDoSomething
    {
        public void Do() { }
    }


    [TestFixture]
    public class TestScopedContainerIsolation
    {
        [Test]
        public void RegisterAssemblyTypes_PublicAndPrivate_PublicIsFound()
        {
            var builder = new ContainerBuilder();
            builder.RegisterAssemblyTypes(GetType().Assembly)
                .Where(t => t.IsPublic) // means public and not nested!!
                .AsImplementedInterfaces();
            var container = builder.Build();
            var something = container.Resolve(typeof(IDoSomething));
            Assert.That(something.GetType(), Is.EqualTo(typeof(PublicDoSomething)));
        }
    }
}
