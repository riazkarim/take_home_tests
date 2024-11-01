namespace ConsoleApp4.Providers;

internal interface ILogProvider
{
    string[] FilePaths { get; }
    IEnumerable<StreamReader> GetLogs();
}