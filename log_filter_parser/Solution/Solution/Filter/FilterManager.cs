using System.Collections.Generic;

namespace ConsoleApp4.Filter;

public class FilterManager : IFilterManager
{
    public List<Filter> Filters { get; }
    private readonly List<IpFilter> _ipFilters;
    private readonly List<UserFilter> _userFilters;
    
    public FilterManager(List<Filter> filters)
    {
        if (!filters.Any())
        {
            Filters = [new IpRangeFilter("0.0.0.0/0", true)];
        }
        else
        {
            // Sort the filters by Include > Exclude
            Filters = filters.OrderBy(f => f, new FilterComparer()).ToList();
        }
    }

    /**
     * Use case 1: No IP Filters, No User filters -> Everything included
     * Use case 2: No IP Filters, Exclude "sys" user -> Everything included, except if user == "sys"
     * Use case 3: No IP Filters, Exclude CEO user -> Everything included, except if user == "assaf.rappaport"
     * Use case 4: Include IP Range of test machine, Exclude specific machine within range -> Include machines with an IP in the test range, except that single test machine 
     */
    public bool ShouldInclude(LogLine logLine)
    {
        bool include = false;

        foreach (var filter in Filters)
        {
            if (filter.IsMatch(logLine))
            {
                include = filter.Include;
            }
        }

        return include;
    }
}