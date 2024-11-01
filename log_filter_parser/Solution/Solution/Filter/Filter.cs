namespace ConsoleApp4.Filter;

public abstract class Filter
{
    protected Filter(bool include)
    {
        Include = include;
    }

    public bool Include { get; }

    public abstract bool IsMatch(LogLine line);
}