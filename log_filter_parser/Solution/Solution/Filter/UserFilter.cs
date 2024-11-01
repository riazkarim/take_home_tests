using System.Text.RegularExpressions;

namespace ConsoleApp4.Filter;

public class UserFilter : Filter
{
    public UserFilter(string regex, bool include) : base(include)
    {
        Regex = new Regex(regex, RegexOptions.Compiled);
    }

    public Regex Regex { get; private set; }
    public override bool IsMatch(LogLine line)
    {
        return line.User != null && this.Regex.IsMatch(line.User);
    }
}