using System.Net;

namespace ConsoleApp4.Filter;

public class SingleIpFilter : IpRangeFilter
{
    public SingleIpFilter(string ip, bool include) : base(string.Format("{ip}/32"), include)
    {
    }
}