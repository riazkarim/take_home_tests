using ConsoleApp4.Util;

namespace ConsoleApp4.Enrichers;

public class DomainLogLineEnricher : ILogLineEnricher
{
    public IDnsManager DnsManager { get; }

    public DomainLogLineEnricher(IDnsManager dnsManager)
    {
        DnsManager = dnsManager;
    }

    public void Enrich(LogLine logLine)
    {
        if (!logLine.Domain.HasValue)
        {
            logLine.Domain = DnsManager.Get(logLine.SourceIp.ToString());
        }
    }
}