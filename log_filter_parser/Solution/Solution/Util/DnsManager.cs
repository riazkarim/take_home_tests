using System.Net;
using CacheManager.Core;

namespace ConsoleApp4.Util;

class DnsManager : IDnsManager
{
    public DnsManager()
    {
        this.Cache = CacheFactory.Build<string?>("dnsCache", settings =>
        {
            // TODO: Implement a size limit on this cache, so if we exceed 256MB entries we evict the least recently used
            // Each entry will be a hostname (~16 bytes) and an IP Address (4 bytes) => 24 bytes
            // 256MB should give us about 10 million records
            settings.WithUpdateMode(CacheUpdateMode.Up).WithDictionaryHandle()
                .WithExpiration(ExpirationMode.Sliding, TimeSpan.FromMinutes(1)).Build();
        });
    }

    public ICacheManager<string?> Cache { get; set; }

    public string? Get(string ipAddress)
    {
        return Cache.GetOrAdd(ipAddress, "default", (ip, region) => LookupDns(ip));
    }

    private string? LookupDns(string ipAddress)
    {
        try
        {
            var entry = Dns.GetHostEntry(ipAddress);
            return entry.HostName; // Hostname is null if the lookup failed
        }
        catch
        {
            Console.WriteLine("Failed to lookup DNS, returning null");
            return null;
        }
    }
}