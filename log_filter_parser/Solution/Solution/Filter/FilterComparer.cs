namespace ConsoleApp4.Filter;

internal class FilterComparer : IComparer<Filter>
{
    public int Compare(Filter? x, Filter? y)
    {
        // Return an order such that Include == True means that it comes before Include == False
        if (x.Include) return -1;
        else if (y.Include) return 1;
        else return 0;
    }
}