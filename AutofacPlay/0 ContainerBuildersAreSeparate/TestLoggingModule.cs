using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using Autofac;
using Autofac.Core;
using Autofac.Features.ResolveAnything;
using NUnit.Framework;
using Module=Autofac.Module;

namespace AutofacPlay.Core
{
    [TestFixture]
    public class TestLoggingModule
    {
        private static ContainerBuilder GetBuilder()
        {
            var builder = new ContainerBuilder();
            builder.RegisterModule(new LoggingModule());
            builder.RegisterType<TypedLoggerFactory>().As<ILoggerFactory>().SingleInstance();
            builder.RegisterSource(new AnyConcreteTypeNotAlreadyRegisteredSource());
            return builder;
        }

        [Test]
        public void BaseService_GetsRightLogger()
        {
            ContainerBuilder builder = GetBuilder();

            using ( IContainer container = builder.Build() )
            {
                var service = container.Resolve<BaseService>();
                var log = (TypedLogger) service.Log;
                Assert.That(log.TypeName, Is.EqualTo("AutofacPlay.Core.BaseService"));
            }
        }

        [Test]
        public void DerivedService_GetsRightLogger()
        {
            ContainerBuilder builder = GetBuilder();
            using ( IContainer container = builder.Build() )
            {
                var service = container.Resolve<DerivedService>();
                var log = (TypedLogger) service.Log;
                Assert.That(log.TypeName, Is.EqualTo("AutofacPlay.Core.DerivedService"));
            }
        }

        [Test]
        public void ClassWithNoILogProperty_IsCreatedWithoutOne()
        {
            ContainerBuilder builder = GetBuilder();
            using ( IContainer container = builder.Build() )
            {
                container.Resolve<NoLogger>();
            }
        }
    }

    public class NoLogger {}

    /// <summary>
    /// A module that will attach an ILog interface created for a particular type when objects
    /// of that type are resolved.
    /// </summary>
    /// <remarks>
    /// Pretty much ripped off from Louis DeJardin's post 
    /// http://whereslou.com/2009/10/25/injecting-an-ilogger-property-with-autofac
    /// </remarks>
    public class LoggingModule : Module
    {
        protected override void Load(ContainerBuilder moduleBuilder)
        {
            // call CreateLogger in response to the request for an ILog implementation
            moduleBuilder.Register((ctx, ps) => CreateLogger(ctx, ps)).As<ILog>().InstancePerLifetimeScope().OwnedByLifetimeScope();
        }

        protected override void AttachToComponentRegistration(IComponentRegistry componentRegistry, IComponentRegistration registration)
        {
            Type implementationType = registration.Activator.LimitType;

            // build an array of actions on this type to assign loggers to member properties
            Action<IComponentContext, object>[] injectors = BuildLoggerInjectors(implementationType).ToArray();

            // if there are no logger properties, there's no reason to hook the activated event
            if ( !injectors.Any() )
            {
                return;
            }

            // otherwise, when an instance of this component is activated, inject the loggers on the instance
            registration.Activated += (s, e) =>
                                          {
                                              foreach ( var injector in injectors )
                                              {
                                                  injector(e.Context, e.Instance);
                                              }
                                          };
        }

        private static IEnumerable<Action<IComponentContext, object>> BuildLoggerInjectors(Type componentType)
        {
            // Look for settable properties of type "ILog"
            var loggerProperties = componentType
                .GetProperties(BindingFlags.SetProperty | BindingFlags.Public | BindingFlags.Instance)
                .Select(p => new
                                 {
                                     PropertyInfo = p,
                                     p.PropertyType,
                                     IndexParameters = p.GetIndexParameters(),
//                                     Accessors = p.GetAccessors(false)
                                 })
                .Where(x => x.PropertyType == typeof (ILog)) // must be a logger
                .Where(x => x.IndexParameters.Count() == 0); // must not be an indexer

            // Blair - isn't this handled by asking for the SetProperty?            
            //                .Where(x => x.Accessors.Length != 1 || x.Accessors[0].ReturnType == typeof(void)); //must have get/set, or only set

            // Return an array of actions that resolve a logger and assign the property
            foreach ( var entry in loggerProperties )
            {
                PropertyInfo propertyInfo = entry.PropertyInfo;

                yield return (ctx, instance) =>
                                 {
                                     var propertyValue = ctx.Resolve<ILog>(new TypedParameter(typeof (Type), componentType));
                                     propertyInfo.SetValue(instance, propertyValue, null);
                                 };
            }
        }

        private static ILog CreateLogger(IComponentContext context, IEnumerable<Parameter> parameters)
        {
            var loggerFactory = context.Resolve<ILoggerFactory>();
            var containingType = parameters.TypedAs<Type>();
            return loggerFactory.CreateFor(containingType);
        }
    }
}
