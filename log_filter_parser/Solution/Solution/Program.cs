using System.Collections.Generic;
using ConsoleApp4.Enrichers;
using ConsoleApp4.Filter;
using ConsoleApp4.Providers;
using ConsoleApp4.Util;

namespace ConsoleApp4;

class Program
{
    static void Main(string[] args)
    {
        //Instantiate dependencies. In practice, we would use DI for this using a framework such as Ninject.       
        var csp = CloudServiceProvider.Parse("ServiceDBv1.csv");
        var filterManager = new FilterManager(new List<Filter.Filter>());
        var dnsManager = new DnsManager();
        var logProvider = new LogProvider(new[] { "firewall_test.log" });
        //Enrichers
        var enricherManager = new LogLineEnricherManager([new DomainLogLineEnricher(dnsManager)]);
        
        var correlator = new LogCorrelator(csp, filterManager, enricherManager, logProvider);
        
        // Parse firewall log and correlate with cloud services
        var correlatedData = correlator.Correlate();
        LogCorrelator.PrintCorrelation(correlatedData);
    }
}