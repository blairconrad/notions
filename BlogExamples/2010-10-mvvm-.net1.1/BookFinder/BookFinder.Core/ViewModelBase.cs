using System;
using System.Collections;
using System.Reflection;
using System.Windows.Forms;

namespace BookFinder
{
    public class ViewModelBase
    {
        protected Control View;
        private BindingFlags myBindingFlags = BindingFlags.Instance | BindingFlags.Public;

        public ViewModelBase(Control view)
        {
            View = view;
        }

        protected void BindToView()
        {
            ArrayList allControls = AllControlsDescendingFrom(View);
            
            foreach ( MethodInfo handler in EventHandlers() )
            {
                FindEventToListenTo(allControls, handler);
            }

            foreach ( FieldInfo field in PropertyFields() )
            {
                FindPropertyToBindTo(allControls, field);
            }
        }

        private void FindPropertyToBindTo(ArrayList allControls, FieldInfo field)
        {
            foreach ( Control control in allControls )
            {
                if ( BindFieldToControl(control, field) )
                {
                    return;
                }
            }
        }

        private void FindEventToListenTo(ArrayList allControls, MethodInfo handler)
        {
            foreach ( Control control in allControls )
            {
                if ( ListenToEvent(control, handler) )
                {
                    return;
                }
            }
        }

        private IEnumerable PropertyFields()
        {
            ArrayList fields = new ArrayList();
            foreach ( FieldInfo field in this.GetType().GetFields(BindingFlags.Instance | BindingFlags.NonPublic) )
            {
                if ( field.FieldType.IsAssignableFrom(typeof(Property)))
                {
                    fields.Add(field);
                }
            }
            return fields;
        }

        private IEnumerable EventHandlers()
        {
            ArrayList eventHandlers = new ArrayList();
            foreach ( MethodInfo method in this.GetType().GetMethods(myBindingFlags) )
            {
                if ( isEventHandler(method) )
                {
                    eventHandlers.Add(method);
                }
            }
            return eventHandlers;
        }
        
        private bool isEventHandler(MethodInfo info)
        {
            ParameterInfo[] parameters = info.GetParameters();
            return
                (info.ReturnType == typeof (void) &&
                 parameters.Length == 2 &&
                 parameters[0].ParameterType == typeof (object) &&
                 (typeof (EventArgs)).IsAssignableFrom(parameters[1].ParameterType));
        }


        private bool ListenToEvent(Control control, MethodInfo method)
        {
            string eventName = ControlAttributeName(control, method);
            if ( eventName == null )
            {
                return false;
            }
            
            EventInfo eventInfo = control.GetType().GetEvent(eventName, myBindingFlags);
            if ( eventInfo == null )
            {
                return false;
            }

            eventInfo.GetAddMethod().Invoke(control, new object[]
                                                         {
                                                             Delegate.CreateDelegate(eventInfo.EventHandlerType, this, method.Name)
                                                         });
            return true;
        }

        private bool BindFieldToControl(Control control, FieldInfo field)
        {
            string controlPropertyName = ControlAttributeName(control, field);
            if ( controlPropertyName == null )
            {
                return false;
            }

            PropertyInfo controlProperty = control.GetType().GetProperty(controlPropertyName, myBindingFlags);
            if ( controlProperty != null )
            {
                field.SetValue(this, new BoundProperty(control, controlProperty));
            }
            return true;
        }

        /// <summary>
        /// Given a control and a ViewModel member, checks to see if the control name
        /// prefixes the viewModelMember. If so, returns the remainder of the member name.
        /// Otherwise, returns <c>null</c>. 
        /// </summary>
        /// <remarks>
        /// Used to find controls that contain attributes that we can bind to. For example,
        /// given a control called "Search", and a viewModelMember called "SearchClick", this 
        /// method should return "Click", allowing us to look for the <c>control.Click</c> member.
        /// Given a control called "Save" and a viewModelMember called "SearchClick", the 
        /// method will return <c>null</c> - there's nothing here to try to bind to.
        /// </remarks>
        private string ControlAttributeName(Control control, MemberInfo viewModelMember)
        {
            if ( viewModelMember.Name.ToLower().StartsWith(control.Name.ToLower()) )
            {
                return viewModelMember.Name.Substring(control.Name.Length);
            }
            return null;
        }

        private static ArrayList AllControlsDescendingFrom(Control baseControl)
        {
            ArrayList allControls = new ArrayList();
            allControls.Add(baseControl);
            foreach ( Control control in baseControl.Controls )
            {
                allControls.AddRange(AllControlsDescendingFrom(control));
            }
            return allControls;
        }
    }
}