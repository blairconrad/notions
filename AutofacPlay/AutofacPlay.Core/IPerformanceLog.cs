using System;

namespace AutofacPlay.Core
{
    public interface IPerformanceLog
    {
        void Begin(string operation);
        void End(string operation);
    }

    public class PerformanceLog : IPerformanceLog
    {
        ILog logger;
        public PerformanceLog(ILog logger)
        {
            this.logger = logger;
        }

        public void Begin(string operation)
        {
            logger.Log(DateTime.Now + " starting " + operation);
        }

        public void End(string operation)
        {
            logger.Log(DateTime.Now + " ending " + operation);
        }
    }
}
