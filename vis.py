
import csv
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

import matplotlib.pyplot as plt

DATA_FILE = Path(__file__).resolve().parent / "expenses.csv"
OUTPUT_FILE = Path(__file__).resolve().parent / "expense_pie_chart.png"


def load_expenses():
    if not DATA_FILE.exists():
        print("找不到 expenses.csv，請先新增支出資料。")
        return None

    totals = defaultdict(Decimal)

    with DATA_FILE.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row_number, row in enumerate(reader, start=2):
            category = (row.get("category") or "").strip()
            amount_text = (row.get("amount") or "").strip()

            if not category or not amount_text:
                print(f"第 {row_number} 列資料不完整，已略過。")
                continue

            try:
                amount = Decimal(amount_text)
                if amount <= 0:
                    print(f"第 {row_number} 列金額無效，已略過。")
                    continue
            except InvalidOperation:
                print(f"第 {row_number} 列金額格式錯誤，已略過。")
                continue

            totals[category] += amount

    if not totals:
        print("目前沒有可供統計的支出資料。")
        return None

    return totals


def create_pie_chart(totals):
    categories = list(totals.keys())
    amounts = [float(totals[c]) for c in categories]

    plt.rcParams["font.sans-serif"] = [
        "Microsoft JhengHei", "Microsoft YaHei", "Arial"
    ]
    plt.rcParams["axes.unicode_minus"] = False

    plt.figure(figsize=(8, 6))

    plt.pie(
        amounts,
        labels=categories,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Expenses by Category")
    plt.axis("equal")
    plt.tight_layout()

    plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches="tight")

    print(f"圓餅圖已儲存至：{OUTPUT_FILE}")

    print("\n各類別支出統計：")
    for category, amount in totals.items():
        print(f"{category}: {amount:.2f}")

    plt.show()


def main():
    totals = load_expenses()

    if totals is not None:
        create_pie_chart(totals)


if __name__ == "__main__":
    main()
