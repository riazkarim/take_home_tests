using System.Net;
using System.Text.RegularExpressions;

namespace ConsoleApp4;

public class LogLine
{
    public LogLine(string log)
    {
        string pattern = @"(?<Key>\b\w+)\=(?<Value>[^\s]+)";
        var regex = new Regex(pattern, RegexOptions.Compiled);
        Direction = ParseDirection(log);
        if (Direction != Direction.Other)
        {
            MatchCollection matches = regex.Matches(log);

            foreach (Match match in matches)
            {
                string key = match.Groups["Key"].Value;
                string value = match.Groups["Value"].Value;
                if (key == "SRC")
                {
                    SourceIp = IPAddress.Parse(value);
                }
                else if (key == "DST")
                {
                    DestinationIp = IPAddress.Parse(value);
                }
                else if (key == "USER")
                {
                    User = value;
                }
                else if (key == "DOMAIN")
                {
                    Domain = value;
                }
            }
        }
    }

    public string? User { get; }

    public ServiceDomain? Domain { get; set; }

    public IPAddress DestinationIp { get; }

    public IPAddress SourceIp { get; }

    public Direction Direction { get; }

    public List<string> Log { get; }

    private static Direction ParseDirection(string line)
    {
        if (line.Contains("INBOUND")) return Direction.Inbound;
        if (line.Contains("OUTG")) return Direction.Outbound;
        return Direction.Other;
    }
}