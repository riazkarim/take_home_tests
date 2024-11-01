namespace ConsoleApp4.Filter;

public abstract class IpFilter : Filter
{
    protected IpFilter(bool include) : base(include)
    {
    }
}