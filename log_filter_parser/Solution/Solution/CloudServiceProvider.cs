using System.Globalization;
using CsvHelper;

namespace ConsoleApp4;

internal interface ICloudServiceProvider
{
    Dictionary<ServiceDomain, CloudService> Services { get; }
    ServiceName GetServiceName(ServiceDomain serviceDomain);
}

class CloudServiceProvider : ICloudServiceProvider
{
    public Dictionary<ServiceDomain, CloudService> Services { get; }

    private CloudServiceProvider(Dictionary<ServiceDomain, CloudService> services)
    {
        Services = services;
    }

    public ServiceName GetServiceName(ServiceDomain serviceDomain)
    {
        if (Services.ContainsKey(serviceDomain))
        {
            return Services[serviceDomain].ServiceName;
        }
        throw new Exception($"The service domain {serviceDomain} is not registered.");
    }
    
    public static CloudServiceProvider Parse(string filePath)
    {
        
        using (var reader = new StreamReader(filePath))
        using (var csv = new CsvReader(reader, CultureInfo.InvariantCulture))
        {
            var records = csv.GetRecords<CloudService>();
            return new CloudServiceProvider(records.ToDictionary(record => (ServiceDomain)record.ServiceDomain, record => record));
        }
    }
}