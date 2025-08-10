from config.setting import settings

def print_report(title: str, value: str):
    border = "=" * 40
    padding = " " * ((38 - len(title)) // 2)
    print(f"\n{border}")
    print(f"|{padding}{title}{padding}|")
    print(border)
    print(f"\n💰 Revenue: {value}\n")
    print(border + "\n")

def day_revenue_report():
    print_report("📅 Daily Revenue Report", settings.day_p)

def month_revenue_report():
    print_report("🗓️ Monthly Revenue Report", settings.month_p)

def year_revenue_report():
    print_report("📈 Yearly Revenue Report", settings.year_p)