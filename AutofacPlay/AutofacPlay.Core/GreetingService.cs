using System.IO;

namespace AutofacPlay.Core
{
    public class GreetingService: BaseService
    {
        public TextWriter Writer { get; set; }

        public void Greet()
        {
            Writer.WriteLine("Hello!");
        }
    }
}
