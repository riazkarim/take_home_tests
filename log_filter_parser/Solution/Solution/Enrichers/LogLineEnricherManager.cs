namespace ConsoleApp4.Enrichers;

public class LogLineEnricherManager : ILogLineEnricherManager
{
    public ILogLineEnricher[] Enrichers { get; }

    public LogLineEnricherManager(ILogLineEnricher[] enrichers)
    {
        Enrichers = enrichers;
    }

    public void Enrich(LogLine logLine)
    {
        foreach (var enricher in Enrichers)
        {
            enricher.Enrich(logLine);
        }
    }
}