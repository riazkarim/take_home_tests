using System.Net;
using ConsoleApp4.Enrichers;
using ConsoleApp4.Filter;
using ConsoleApp4.Providers;
using ConsoleApp4.Util;

namespace ConsoleApp4;

class LogCorrelator
{
    public ICloudServiceProvider CloudServiceProvider { get; }
    public IFilterManager FilterManager { get; }
    public ILogLineEnricherManager LogLineEnricherManager { get; }
    public ILogProvider LogProvider { get; }

    public LogCorrelator(ICloudServiceProvider cloudServiceProvider, IFilterManager filterManager, ILogLineEnricherManager logLineEnricherManager, ILogProvider logProvider)
    {
        CloudServiceProvider = cloudServiceProvider;
        FilterManager = filterManager;
        LogLineEnricherManager = logLineEnricherManager;
        LogProvider = logProvider;
    }
    
    public Dictionary<ServiceName, HashSet<IPAddress>> Correlate()
    {
        var correlatedData = new Dictionary<ServiceName, HashSet<IPAddress>>();

        foreach (var reader in LogProvider.GetLogs())
        {
            while (!reader.EndOfStream)
            {
                var line = reader.ReadLine();
                if (string.IsNullOrEmpty(line)) continue; // Skip blank lines in the log file
                
                var logLine = new LogLine(line);
                
                // Enrich the log lines with any missing data. We do this before we check the filters, so that we have 
                // option of using any of the enriched fields in a future filter.
                LogLineEnricherManager.Enrich(logLine);
                
                // Check if we should process this line according to the filters
                if (!FilterManager.ShouldInclude(logLine))
                {
                    // Skip things the filter says to exclude
                    continue;
                }
                
                if (logLine.Domain.HasValue)
                {
                    var serviceName = CloudServiceProvider.GetServiceName(logLine.Domain.Value);
                    if (!correlatedData.ContainsKey(serviceName))
                    {
                        correlatedData.Add(serviceName, new HashSet<IPAddress>());
                    }

                    correlatedData[serviceName].Add(logLine.SourceIp);
                }
            }
        }
        return correlatedData;
    }

    public static void PrintCorrelation(Dictionary<ServiceName,HashSet<IPAddress>> correlatedData)
    {
        foreach (var service in correlatedData)
        {
            Console.WriteLine($"{service.Key}: {string.Join(", ", service.Value)}");
        }
    }
}