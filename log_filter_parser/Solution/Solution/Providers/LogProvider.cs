namespace ConsoleApp4.Providers;

class LogProvider : ILogProvider
{
    public string[] FilePaths { get; }

    public LogProvider(string[] filePaths)
    {
        FilePaths = filePaths;
    }

    // Lazy load files and return a stream for each
    public IEnumerable<StreamReader> GetLogs()
    {
        foreach (var filePath in FilePaths)
        {
            //Dispose of each reader/file-handle once the caller is done
            using (var reader = new StreamReader(filePath))
            {
                yield return reader;
            }
        }
    }
}