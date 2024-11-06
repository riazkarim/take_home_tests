from datetime import datetime
from statistics import median

from model.customer import CustomerStat
from log_data import LogDataProvider


class CustomerStatsProvider:

    def __init__(self, log_provider: LogDataProvider):
        self.log_provider = log_provider

    def get_customer_stats(self, customer_id: int, from_date: datetime) -> CustomerStat:
        data = self.log_provider.get_customer_data(customer_id, from_date)

        if not data:
            return None

        success_count = sum(1 for _, status, _ in data if status == 200)
        total_count = len(data)
        fail_count = total_count - success_count

        uptimes = [status == 200 for _, status, _ in data]
        uptime = sum(uptimes) / len(uptimes) * 100 if uptimes else 0

        durations = [duration for _, status, duration in data if status == 200]
        average_latency = sum(durations) / len(durations) if durations else 0
        median_latency = median(durations) if durations else 0
        p99_latency = sorted(durations)[int(0.99 * len(durations))] if durations else 0

        return CustomerStat(total_count=total_count, success_count=success_count, fail_count=fail_count, uptime=uptime,
                            average_latency=average_latency, median_latency=median_latency, p99_latency=p99_latency)
