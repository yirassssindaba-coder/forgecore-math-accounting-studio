import json
import os
import tempfile

from core import QuantoraEngine


def run() -> dict:
    engine = QuantoraEngine()
    engine.clear_entries()
    engine.add_entry("2026-03-02", "Owner capital", "Cash", "Capital", 1000)
    engine.add_entry("2026-03-02", "Buy equipment", "Equipment", "Cash", 300)

    trial = engine.trial_balance()
    vat = engine.accounting_tool("VAT", {"base": 100, "rate": 11})
    expr = engine.evaluate_expression("(2+3)*4")
    linear = engine.solve_linear(2, -10)
    quadratic = engine.solve_quadratic(1, -3, 2)
    stats = engine.statistics_summary("10,20,30")

    engine.new_number_game(target=42)
    low_guess = engine.guess_number(30)
    correct_guess = engine.guess_number(42)

    engine.new_quiz_question(forced=(7, 5, "+"))
    wrong_quiz = engine.submit_quiz_answer(10)
    engine.new_quiz_question(forced=(7, 5, "+"))
    right_quiz = engine.submit_quiz_answer(12)

    temp_dir = tempfile.gettempdir()
    csv_path = os.path.join(temp_dir, "quantora_smoke_export.csv")
    engine.export_entries_csv(csv_path)

    return {
        "trial_balance_balanced": trial["balanced"],
        "trial_totals": {"debit": trial["total_debit"], "credit": trial["total_credit"]},
        "vat": vat,
        "expression": expr,
        "linear": linear,
        "quadratic": quadratic,
        "stats": stats,
        "number_game": {"low": low_guess, "correct": correct_guess},
        "quiz": {"wrong": wrong_quiz, "right": right_quiz},
        "csv_exists": os.path.exists(csv_path),
        "summary": engine.summary_counts(),
    }


if __name__ == "__main__":
    results = run()
    print(json.dumps(results, indent=2))
