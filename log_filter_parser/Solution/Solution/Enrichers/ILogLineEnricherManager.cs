namespace ConsoleApp4.Enrichers;

public interface ILogLineEnricherManager
{
    ILogLineEnricher[] Enrichers { get; }
    void Enrich(LogLine logLine);
}