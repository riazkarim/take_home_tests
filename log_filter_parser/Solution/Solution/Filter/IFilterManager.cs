namespace ConsoleApp4.Filter;

public interface IFilterManager
{
    bool ShouldInclude(LogLine logLine);
}