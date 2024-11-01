using System.Net;

namespace ConsoleApp4.Filter;

public class IpRangeFilter : IpFilter
{
    public IpRangeFilter(string cidr, bool include) : base(include)
    {
        this.Range = IPNetwork.Parse(cidr);
    }
    
    public IPNetwork Range { get; }
    public override bool IsMatch(LogLine line)
    {
        return this.Range.Contains(line.SourceIp) || this.Range.Contains(line.DestinationIp);
    }
}