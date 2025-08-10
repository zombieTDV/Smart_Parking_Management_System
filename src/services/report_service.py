from config.setting import settings

def print_report(title: str, value: str):
    border = "=" * 40
    padding = " " * ((38 - len(title)) // 2)
    print(f"\n{border}")
    print(f"|{padding}{title}{padding}|")
    print(border)
    print(f"\n💰 Doanh Thu: {value} VND\n")
    print(border + "\n")

def day_revenue_report():
    print_report("📅 Báo cáo doanh thu theo ngày", settings.day_p)

def month_revenue_report():
    print_report("🗓️ Báo cáo doanh thu theo tháng", settings.month_p)

def year_revenue_report():
    print_report("📈 Báo cáo doanh thu theo năm", settings.year_p)