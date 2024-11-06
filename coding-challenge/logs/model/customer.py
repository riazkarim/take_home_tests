class CustomerStat:
    def __init__(self, total_count=None, success_count=None, fail_count=None, uptime=None, average_latency=None,
                 median_latency=None, p99_latency=None):
        self.total_requests = total_count
        self.successful_requests = success_count
        self.failed_requests = fail_count
        self.uptime_percentage = uptime
        self.average_latency = average_latency
        self.median_latency = median_latency
        self.p99_latency = p99_latency
