using CsvHelper.Configuration.Attributes;

namespace ConsoleApp4;

class CloudService
{
    [Name("Service name")]
    public string ServiceName { get; set; }
    [Name("Service domain")]
    public string ServiceDomain { get; set; }
}

public record struct ServiceName
{
    public ServiceName(string value)
    {
        Value = value;
    }

    public string Value { get; }
    
    public static implicit operator string(ServiceName serviceName) => serviceName.Value;
    public static implicit operator ServiceName(string serviceName) => new(serviceName);
}

public record struct ServiceDomain
{
    public ServiceDomain(string value)
    {
        Value = value;
    }

    public string Value { get;}
    
    public static implicit operator string(ServiceDomain serviceDomain) => serviceDomain.Value;
    public static implicit operator ServiceDomain(string serviceDomain) => new(serviceDomain);
}