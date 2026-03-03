import ast
import json
import math
import os
import random
import statistics
import time
import urllib.request
import shutil
import tempfile
from dataclasses import dataclass
from decimal import Decimal, getcontext, InvalidOperation
from typing import Any, Dict, List, Optional, Tuple

APP_DIR_NAME = ".forgecore_math_accounting_studio"

# higher precision for finance/accounting
getcontext().prec = 28


def get_storage_dir() -> str:
    base = os.path.expanduser("~")
    appdata = os.environ.get("APPDATA")
    if os.name == "nt" and appdata:
        base = appdata
    path = os.path.join(base, APP_DIR_NAME)
    os.makedirs(path, exist_ok=True)
    return path


def resource_path(*parts: str) -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, *parts)


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def to_decimal(value: Any) -> Decimal:
    if isinstance(value, Decimal):
        return value
    s = str(value).strip()
    if s == "":
        raise ValueError("Value is required.")
    try:
        # allow commas in input
        s = s.replace(",", "")
        return Decimal(s)
    except InvalidOperation as e:
        raise ValueError(f"Invalid number: {value}") from e


class SafeMathEvaluator:
    """
    For the "expression mode" calculator.
    Keeps evaluation safe by allowing only a small AST subset.
    """

    ALLOWED_FUNCS = {
        "abs": abs,
        "round": round,
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log,
        "log10": math.log10,
        "exp": math.exp,
        "floor": math.floor,
        "ceil": math.ceil,
        "factorial": math.factorial,
        "pi": math.pi,
        "e": math.e,
    }

    ALLOWED_NODES = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Pow,
        ast.Mod,
        ast.FloorDiv,
        ast.USub,
        ast.UAdd,
        ast.Call,
        ast.Load,
        ast.Name,
        ast.Constant,
        ast.Tuple,
        ast.List,
    )

    @classmethod
    def evaluate(cls, expression: str) -> float:
        expression = expression.strip()
        if not expression:
            raise ValueError("Expression is required.")
        tree = ast.parse(expression, mode="eval")
        for node in ast.walk(tree):
            if not isinstance(node, cls.ALLOWED_NODES):
                raise ValueError("Unsupported expression.")
            if isinstance(node, ast.Call):
                if not isinstance(node.func, ast.Name) or node.func.id not in cls.ALLOWED_FUNCS:
                    raise ValueError("Function is not allowed.")
        value = eval(compile(tree, "<safe-math>", "eval"), {"__builtins__": {}}, cls.ALLOWED_FUNCS)
        return float(value)


@dataclass
class QuizQuestion:
    qid: int
    subject: str
    prompt: str
    options: Dict[str, str]
    answer: str
    explanation: str = ""

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "QuizQuestion":
        return cls(
            qid=int(d["id"]),
            subject=str(d.get("subject", "")),
            prompt=str(d.get("prompt", "")),
            options=dict(d.get("options", {})),
            answer=str(d.get("answer", "")).strip(),
            explanation=str(d.get("explanation", "")).strip(),
        )


class ForgeCoreEngine:
    def __init__(self) -> None:
        self.storage_dir = get_storage_dir()
        self.state_file = os.path.join(self.storage_dir, "state.json")

        self.quiz_mastered: Dict[str, bool] = {}
        self.quiz_stats: Dict[str, Any] = {"attempted": 0, "correct": 0}
        self.music_playlist: List[Dict[str, str]] = []

        self.questions: List[QuizQuestion] = []
        self._load_questions()
        self._load_state()

    # -----------------------------
    # State
    # -----------------------------
    def _default_state(self) -> Dict[str, Any]:
        return {
            "quiz_mastered": {},
            "quiz_stats": {"attempted": 0, "correct": 0},
            "music_playlist": [
                {"title": "Lofi Focus (YouTube)", "url": "https://www.youtube.com/watch?v=jfKfPfyJRdk"},
                {"title": "Brown Noise (YouTube)", "url": "https://www.youtube.com/watch?v=RqzGzwTY-6w"},
            ],
        }

    def _load_state(self) -> None:
        if not os.path.exists(self.state_file):
            self._save_state(self._default_state())
        try:
            with open(self.state_file, "r", encoding="utf-8") as fh:
                raw = json.load(fh)
        except Exception:
            raw = self._default_state()
            self._save_state(raw)

        self.quiz_mastered = dict(raw.get("quiz_mastered", {}))
        self.quiz_stats = dict(raw.get("quiz_stats", {"attempted": 0, "correct": 0}))
        self.music_playlist = list(raw.get("music_playlist", []))[:200]

    def _save_state(self, payload: Dict[str, Any]) -> None:
        with open(self.state_file, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)

    def save(self) -> None:
        payload = {
            "quiz_mastered": self.quiz_mastered,
            "quiz_stats": self.quiz_stats,
            "music_playlist": self.music_playlist,
        }
        self._save_state(payload)

    # -----------------------------
    # Questions
    # -----------------------------
    def _load_questions(self) -> None:
        data_path = resource_path("data", "quiz_math_accounting_1000.json")
        with open(data_path, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
        self.questions = [QuizQuestion.from_dict(item) for item in raw.get("questions", [])]
        # sanity
        if len(self.questions) != 1000:
            # still allow run, but warn via exception so developer can notice
            raise RuntimeError(f"Question bank invalid: expected 1000 questions, got {len(self.questions)}")

    def is_mastered(self, qid: int) -> bool:
        return bool(self.quiz_mastered.get(str(qid), False))

    def mark_mastered(self, qid: int) -> None:
        self.quiz_mastered[str(qid)] = True

    def get_question_pool(self, subject: str, hide_mastered: bool) -> List[QuizQuestion]:
        subject = (subject or "Campur").strip()
        if subject == "Campur":
            pool = self.questions[:]
        else:
            pool = [q for q in self.questions if q.subject == subject]
        if hide_mastered:
            pool = [q for q in pool if not self.is_mastered(q.qid)]
        return pool

    def build_quiz_session(self, subject: str, count: int, minutes: int, hide_mastered: bool) -> Dict[str, Any]:
        pool = self.get_question_pool(subject, hide_mastered)
        if not pool:
            return {
                "ok": False,
                "error": "Tidak ada soal tersisa (semua sudah mastered atau filter terlalu ketat).",
            }
        random.shuffle(pool)
        selected = pool[: max(1, min(int(count), len(pool)))]
        now = time.time()
        return {
            "ok": True,
            "subject": subject,
            "count": len(selected),
            "minutes": int(minutes),
            "start_ts": now,
            "end_ts": now + int(minutes) * 60,
            "queue": [q.qid for q in selected],
            "index": 0,
            "attempted": 0,
            "correct": 0,
            "wrong": 0,
            "answers": {},  # qid -> chosen letter
        }

    def get_question_by_id(self, qid: int) -> Optional[QuizQuestion]:
        # questions are small, linear scan ok for 1000
        for q in self.questions:
            if q.qid == qid:
                return q
        return None

    def grade_answer(self, qid: int, chosen: str) -> Dict[str, Any]:
        q = self.get_question_by_id(qid)
        if not q:
            return {"ok": False, "error": "Soal tidak ditemukan."}
        chosen = (chosen or "").strip().upper()
        correct = q.answer.strip().upper()
        is_correct = chosen == correct
        self.quiz_stats["attempted"] = _safe_int(self.quiz_stats.get("attempted", 0), 0) + 1
        if is_correct:
            self.quiz_stats["correct"] = _safe_int(self.quiz_stats.get("correct", 0), 0) + 1
            self.mark_mastered(qid)
        self.save()
        return {
            "ok": True,
            "qid": qid,
            "chosen": chosen,
            "correct": correct,
            "is_correct": is_correct,
            "explanation": q.explanation,
        }

    # -----------------------------
    # Music playlist
    # -----------------------------
    def add_track(self, title: str, url: str) -> None:
        title = (title or "").strip() or "Untitled"
        url = (url or "").strip()
        if not url:
            raise ValueError("URL wajib diisi.")
        self.music_playlist.insert(0, {"title": title, "url": url})
        self.music_playlist = self.music_playlist[:200]
        self.save()

    def remove_track(self, index: int) -> None:
        if 0 <= index < len(self.music_playlist):
            self.music_playlist.pop(index)
            self.save()

    def export_resource_pdf(self, filename: str, dest_path: str) -> None:
        src = resource_path("resources", filename)
        if not os.path.exists(src):
            raise FileNotFoundError("PDF resource tidak ditemukan.")
        shutil.copy2(src, dest_path)

    # -----------------------------
    # Super calculator formulas
    # -----------------------------
    def formula_catalog(self) -> List[Dict[str, Any]]:
        """
        Each entry describes inputs needed. UI uses this to render fields.
        """
        return [
            # Math core
            {"id": "expr", "category": "Math • Expression", "name": "Safe Expression Evaluator", "inputs": [{"k":"expression","label":"Expression","default":"(2+3)*4"}]},
            {"id": "derivative_power", "category": "Math • Calculus", "name": "Derivative: d/dx (a*x^n)", "inputs": [{"k":"a","label":"a","default":"3"},{"k":"n","label":"n","default":"3"}]},
            {"id": "mean", "category": "Math • Statistics", "name": "Mean (average)", "inputs": [{"k":"data","label":"Data (comma separated)","default":"3,5,7,9"}]},
            {"id": "variance_sample", "category": "Math • Statistics", "name": "Sample Variance (n-1)", "inputs": [{"k":"data","label":"Data (comma separated)","default":"3,5,7,9"}]},
            {"id": "std_sample", "category": "Math • Statistics", "name": "Sample Standard Deviation", "inputs": [{"k":"data","label":"Data (comma separated)","default":"3,5,7,9"}]},
            {"id": "z_score", "category": "Math • Statistics", "name": "Z-score", "inputs": [{"k":"x","label":"X","default":"10"},{"k":"mu","label":"Mean (μ)","default":"8"},{"k":"sigma","label":"Std dev (σ)","default":"2"}]},
            {"id": "bayes", "category": "Math • Probability", "name": "Bayes: P(A|B)", "inputs": [{"k":"p_b_given_a","label":"P(B|A)","default":"0.9"},{"k":"p_a","label":"P(A)","default":"0.1"},{"k":"p_b","label":"P(B)","default":"0.2"}]},
            {"id": "combination", "category": "Math • Probability", "name": "Combination C(n,r)", "inputs": [{"k":"n","label":"n","default":"10"},{"k":"r","label":"r","default":"3"}]},
            {"id": "permutation", "category": "Math • Probability", "name": "Permutation P(n,r)", "inputs": [{"k":"n","label":"n","default":"10"},{"k":"r","label":"r","default":"3"}]},
            {"id": "binomial_pmf", "category": "Math • Probability", "name": "Binomial PMF P(X=x)", "inputs": [{"k":"n","label":"n","default":"10"},{"k":"x","label":"x","default":"3"},{"k":"p","label":"p","default":"0.5"}]},
            {"id": "poisson_pmf", "category": "Math • Probability", "name": "Poisson PMF", "inputs": [{"k":"lam","label":"λ (lambda)","default":"2.5"},{"k":"x","label":"x","default":"3"}]},
            {"id": "det_2x2", "category": "Math • Linear Algebra", "name": "Determinant 2x2", "inputs": [{"k":"a","label":"a","default":"1"},{"k":"b","label":"b","default":"2"},{"k":"c","label":"c","default":"3"},{"k":"d","label":"d","default":"4"}]},
            {"id": "inv_2x2", "category": "Math • Linear Algebra", "name": "Inverse 2x2", "inputs": [{"k":"a","label":"a","default":"1"},{"k":"b","label":"b","default":"2"},{"k":"c","label":"c","default":"3"},{"k":"d","label":"d","default":"4"}]},
            {"id": "regression_simple", "category": "Math • Modeling", "name": "Linear Regression (y=a+bx) from data", "inputs": [{"k":"x","label":"x values (comma)","default":"1,2,3,4"},{"k":"y","label":"y values (comma)","default":"2,4,5,4"}]},
            {"id": "moving_average", "category": "Math • Time Series", "name": "Moving Average", "inputs": [{"k":"data","label":"Data (comma)","default":"10,12,11,14,13"},{"k":"window","label":"Window size","default":"3"}]},
            {"id": "exp_smoothing_next", "category": "Math • Time Series", "name": "Exponential Smoothing: next forecast", "inputs": [{"k":"alpha","label":"α (0..1)","default":"0.3"},{"k":"x_t","label":"X_t (actual)","default":"120"},{"k":"f_t","label":"F_t (prev forecast)","default":"110"}]},
            {"id": "accuracy", "category": "Math • ML Metrics", "name": "Accuracy", "inputs": [{"k":"tp","label":"TP","default":"10"},{"k":"tn","label":"TN","default":"30"},{"k":"fp","label":"FP","default":"5"},{"k":"fn","label":"FN","default":"5"}]},
            {"id": "precision_recall_f1", "category": "Math • ML Metrics", "name": "Precision / Recall / F1", "inputs": [{"k":"tp","label":"TP","default":"10"},{"k":"fp","label":"FP","default":"5"},{"k":"fn","label":"FN","default":"5"}]},
            # Accounting core
            {"id": "acc_equity", "category": "Accounting • Basics", "name": "Equity = Assets - Liabilities", "inputs": [{"k":"assets","label":"Assets","default":"105"},{"k":"liabilities","label":"Liabilities","default":"42"}]},
            {"id": "net_income", "category": "Accounting • Basics", "name": "Net Income = Revenue - Expense", "inputs": [{"k":"revenue","label":"Revenue","default":"1000"},{"k":"expense","label":"Expense","default":"650"}]},
            {"id": "net_sales", "category": "Accounting • Sales", "name": "Net Sales", "inputs": [{"k":"gross_sales","label":"Gross Sales","default":"1000"},{"k":"returns","label":"Sales Returns","default":"50"},{"k":"discounts","label":"Sales Discounts","default":"20"},{"k":"allowances","label":"Other Allowances","default":"0"}]},
            {"id": "cogs_trading", "category": "Accounting • Inventory", "name": "COGS (Trading)", "inputs": [{"k":"begin_inv","label":"Beginning Inventory","default":"200"},{"k":"purchases","label":"Purchases","default":"800"},{"k":"freight_in","label":"Freight In","default":"20"},{"k":"pur_returns","label":"Purchase Returns","default":"0"},{"k":"pur_discounts","label":"Purchase Discounts","default":"0"},{"k":"end_inv","label":"Ending Inventory","default":"250"}]},
            {"id": "depreciation_sl", "category": "Accounting • Fixed Assets", "name": "Straight-line Depreciation", "inputs": [{"k":"cost","label":"Cost","default":"10000"},{"k":"residual","label":"Residual","default":"1000"},{"k":"life","label":"Useful life (years)","default":"5"}]},
            {"id": "book_value", "category": "Accounting • Fixed Assets", "name": "Book Value", "inputs": [{"k":"cost","label":"Cost","default":"10000"},{"k":"acc_dep","label":"Accumulated Depreciation","default":"3200"}]},
            {"id": "gain_loss_disposal", "category": "Accounting • Fixed Assets", "name": "Gain/Loss on Disposal", "inputs": [{"k":"sell_price","label":"Selling Price","default":"7000"},{"k":"book_value","label":"Book Value","default":"6800"}]},
            {"id": "current_ratio", "category": "Accounting • Ratios", "name": "Current Ratio", "inputs": [{"k":"current_assets","label":"Current Assets","default":"500"},{"k":"current_liab","label":"Current Liabilities","default":"250"}]},
            {"id": "quick_ratio", "category": "Accounting • Ratios", "name": "Quick Ratio", "inputs": [{"k":"cash","label":"Cash+CE","default":"100"},{"k":"sti","label":"Short-term Investments","default":"50"},{"k":"recv","label":"Receivables","default":"120"},{"k":"current_liab","label":"Current Liabilities","default":"250"}]},
            {"id": "break_even_units", "category": "Accounting • CVP", "name": "Break-even Units", "inputs": [{"k":"fixed_cost","label":"Fixed Cost","default":"10000"},{"k":"price","label":"Selling price per unit","default":"50"},{"k":"var_cost","label":"Variable cost per unit","default":"30"}]},
            {"id": "npv", "category": "Accounting • Investment", "name": "NPV", "inputs": [{"k":"rate","label":"Discount rate r (e.g. 0.1)","default":"0.1"},{"k":"cashflows","label":"Cashflows CF_t (comma; include CF0 first)","default":"-1000,300,400,500"}]},
            {"id": "audit_dr", "category": "Accounting • Audit", "name": "Detection Risk (DR) = AR / (IR*CR)", "inputs": [{"k":"ar","label":"AR","default":"0.05"},{"k":"ir","label":"IR","default":"0.70"},{"k":"cr","label":"CR","default":"0.40"}]},
            {"id": "ip_ipk", "category": "Accounting/Math • Academic", "name": "IP / IPK", "inputs": [{"k":"mutu","label":"Total bobot mutu","default":"68"},{"k":"sks","label":"Total SKS","default":"20"}]},
        ]

    def compute_formula(self, formula_id: str, inputs: Dict[str, str]) -> Dict[str, Any]:
        fid = (formula_id or "").strip()
        try:
            if fid == "expr":
                expr = inputs.get("expression", "")
                val = SafeMathEvaluator.evaluate(expr)
                return {"ok": True, "result": val, "steps": f"eval({expr})"}
            if fid == "derivative_power":
                a = to_decimal(inputs.get("a"))
                n = to_decimal(inputs.get("n"))
                # derivative: d/dx (a*x^n) = a*n*x^(n-1)
                coef = a * n
                new_pow = n - Decimal(1)
                return {"ok": True, "result": f"{coef}*x^{new_pow}", "steps": "d/dx (a*x^n)=a*n*x^(n-1)"}
            if fid in ("mean","variance_sample","std_sample"):
                data = self._parse_number_list(inputs.get("data",""))
                if not data:
                    raise ValueError("Data tidak boleh kosong.")
                if fid=="mean":
                    return {"ok": True, "result": statistics.mean(data), "steps": "mean = sum(x)/n"}
                # sample variance
                if len(data) < 2:
                    raise ValueError("Butuh minimal 2 data.")
                var = statistics.variance(data)
                if fid=="variance_sample":
                    return {"ok": True, "result": var, "steps": "variance_sample = Σ(x-mean)^2/(n-1)"}
                return {"ok": True, "result": math.sqrt(var), "steps": "std_sample = sqrt(variance_sample)"}
            if fid == "z_score":
                x=float(to_decimal(inputs.get("x")))
                mu=float(to_decimal(inputs.get("mu")))
                sigma=float(to_decimal(inputs.get("sigma")))
                if sigma==0:
                    raise ValueError("σ tidak boleh 0.")
                z=(x-mu)/sigma
                return {"ok": True, "result": z, "steps": "z = (X-μ)/σ"}
            if fid == "bayes":
                p_b_given_a=float(to_decimal(inputs.get("p_b_given_a")))
                p_a=float(to_decimal(inputs.get("p_a")))
                p_b=float(to_decimal(inputs.get("p_b")))
                if p_b==0:
                    raise ValueError("P(B) tidak boleh 0.")
                val = (p_b_given_a*p_a)/p_b
                return {"ok": True, "result": val, "steps": "P(A|B)=P(B|A)P(A)/P(B)"}
            if fid == "combination":
                n=int(to_decimal(inputs.get("n")))
                r=int(to_decimal(inputs.get("r")))
                if r<0 or n<0 or r>n:
                    raise ValueError("Pastikan 0<=r<=n.")
                val = math.comb(n,r)
                return {"ok": True, "result": val, "steps": "C(n,r)=n!/(r!(n-r)!)"}
            if fid == "permutation":
                n=int(to_decimal(inputs.get("n")))
                r=int(to_decimal(inputs.get("r")))
                if r<0 or n<0 or r>n:
                    raise ValueError("Pastikan 0<=r<=n.")
                val = math.perm(n,r)
                return {"ok": True, "result": val, "steps": "P(n,r)=n!/(n-r)!"}
            if fid == "binomial_pmf":
                n=int(to_decimal(inputs.get("n")))
                x=int(to_decimal(inputs.get("x")))
                p=float(to_decimal(inputs.get("p")))
                if not (0<=p<=1):
                    raise ValueError("p harus 0..1.")
                if not (0<=x<=n):
                    raise ValueError("x harus 0..n.")
                val = math.comb(n,x)*(p**x)*((1-p)**(n-x))
                return {"ok": True, "result": val, "steps": "C(n,x)p^x(1-p)^(n-x)"}
            if fid == "poisson_pmf":
                lam=float(to_decimal(inputs.get("lam")))
                x=int(to_decimal(inputs.get("x")))
                if lam<0 or x<0:
                    raise ValueError("λ dan x harus >= 0.")
                val = math.exp(-lam)*(lam**x)/math.factorial(x)
                return {"ok": True, "result": val, "steps": "e^-λ * λ^x / x!"}
            if fid == "det_2x2":
                a=float(to_decimal(inputs.get("a"))); b=float(to_decimal(inputs.get("b")))
                c=float(to_decimal(inputs.get("c"))); d=float(to_decimal(inputs.get("d")))
                val = a*d - b*c
                return {"ok": True, "result": val, "steps": "det = ad - bc"}
            if fid == "inv_2x2":
                a=float(to_decimal(inputs.get("a"))); b=float(to_decimal(inputs.get("b")))
                c=float(to_decimal(inputs.get("c"))); d=float(to_decimal(inputs.get("d")))
                det = a*d - b*c
                if det==0:
                    raise ValueError("Determinant = 0, matriks tidak invertible.")
                inv = [[d/det, -b/det],[-c/det, a/det]]
                return {"ok": True, "result": inv, "steps": "A^-1 = (1/det)*[[d,-b],[-c,a]]"}
            if fid == "regression_simple":
                xs = self._parse_number_list(inputs.get("x",""))
                ys = self._parse_number_list(inputs.get("y",""))
                if len(xs)!=len(ys) or len(xs)<2:
                    raise ValueError("x dan y harus sama panjang dan minimal 2 data.")
                xbar=statistics.mean(xs); ybar=statistics.mean(ys)
                num=sum((x-xbar)*(y-ybar) for x,y in zip(xs,ys))
                den=sum((x-xbar)**2 for x in xs)
                if den==0:
                    raise ValueError("Variansi x = 0 (semua x sama).")
                b=num/den
                a=ybar - b*xbar
                # Pearson r
                denr=math.sqrt(sum((x-xbar)**2 for x in xs)*sum((y-ybar)**2 for y in ys))
                r=num/denr if denr else 0.0
                return {"ok": True, "result": {"a":a,"b":b,"r":r}, "steps":"b=Σ((x-x̄)(y-ȳ))/Σ((x-x̄)^2); a=ȳ-bx̄"}
            if fid == "moving_average":
                data=self._parse_number_list(inputs.get("data",""))
                w=int(to_decimal(inputs.get("window")))
                if w<=0:
                    raise ValueError("Window harus > 0.")
                if len(data)<w:
                    raise ValueError("Data lebih sedikit daripada window.")
                ma = [sum(data[i-w+1:i+1])/w for i in range(w-1, len(data))]
                return {"ok": True, "result": ma, "steps":"MA = (x1+...+xn)/n (rolling)"}
            if fid == "exp_smoothing_next":
                alpha=float(to_decimal(inputs.get("alpha")))
                x_t=float(to_decimal(inputs.get("x_t")))
                f_t=float(to_decimal(inputs.get("f_t")))
                if not (0<=alpha<=1):
                    raise ValueError("α harus 0..1.")
                f_next = alpha*x_t + (1-alpha)*f_t
                return {"ok": True, "result": f_next, "steps":"F(t+1)=αX_t+(1-α)F_t"}
            if fid == "accuracy":
                tp=float(to_decimal(inputs.get("tp"))); tn=float(to_decimal(inputs.get("tn")))
                fp=float(to_decimal(inputs.get("fp"))); fn=float(to_decimal(inputs.get("fn")))
                denom=tp+tn+fp+fn
                if denom==0:
                    raise ValueError("Denominator 0.")
                val=(tp+tn)/denom
                return {"ok": True, "result": val, "steps":"Accuracy=(TP+TN)/(TP+TN+FP+FN)"}
            if fid == "precision_recall_f1":
                tp=float(to_decimal(inputs.get("tp"))); fp=float(to_decimal(inputs.get("fp"))); fn=float(to_decimal(inputs.get("fn")))
                prec = tp/(tp+fp) if (tp+fp)!=0 else 0.0
                rec = tp/(tp+fn) if (tp+fn)!=0 else 0.0
                f1 = (2*prec*rec/(prec+rec)) if (prec+rec)!=0 else 0.0
                return {"ok": True, "result": {"precision":prec,"recall":rec,"f1":f1}, "steps":"P=TP/(TP+FP); R=TP/(TP+FN); F1=2PR/(P+R)"}
            # Accounting
            if fid == "acc_equity":
                assets=to_decimal(inputs.get("assets")); liab=to_decimal(inputs.get("liabilities"))
                eq=assets-liab
                return {"ok": True, "result": float(eq), "steps":"Equity = Assets - Liabilities"}
            if fid == "net_income":
                rev=to_decimal(inputs.get("revenue")); exp=to_decimal(inputs.get("expense"))
                val=rev-exp
                return {"ok": True, "result": float(val), "steps":"Net Income = Revenue - Expense"}
            if fid == "net_sales":
                gross=to_decimal(inputs.get("gross_sales")); returns=to_decimal(inputs.get("returns"))
                disc=to_decimal(inputs.get("discounts")); allw=to_decimal(inputs.get("allowances"))
                val = gross - returns - disc - allw
                return {"ok": True, "result": float(val), "steps":"Net Sales = Gross - Returns - Discounts - Allowances"}
            if fid == "cogs_trading":
                begin=to_decimal(inputs.get("begin_inv"))
                purchases=to_decimal(inputs.get("purchases"))
                freight=to_decimal(inputs.get("freight_in"))
                pur_ret=to_decimal(inputs.get("pur_returns"))
                pur_disc=to_decimal(inputs.get("pur_discounts"))
                end=to_decimal(inputs.get("end_inv"))
                net_purchases = purchases + freight - pur_ret - pur_disc
                cogs = begin + net_purchases - end
                return {"ok": True, "result": {"net_purchases": float(net_purchases), "cogs": float(cogs)}, "steps":"Net Purchases = Purchases+FreightIn-Returns-Discounts; COGS=BegInv+NetPurch-EndInv"}
            if fid == "depreciation_sl":
                cost=to_decimal(inputs.get("cost")); residual=to_decimal(inputs.get("residual")); life=to_decimal(inputs.get("life"))
                if life<=0:
                    raise ValueError("Umur manfaat harus > 0.")
                dep=(cost-residual)/life
                return {"ok": True, "result": float(dep), "steps":"(Cost-Residual)/Life"}
            if fid == "book_value":
                cost=to_decimal(inputs.get("cost")); acc=to_decimal(inputs.get("acc_dep"))
                val=cost-acc
                return {"ok": True, "result": float(val), "steps":"Book Value = Cost - Accumulated Depreciation"}
            if fid == "gain_loss_disposal":
                sp=to_decimal(inputs.get("sell_price")); bv=to_decimal(inputs.get("book_value"))
                gl=sp-bv
                return {"ok": True, "result": float(gl), "steps":"Gain/Loss = Selling Price - Book Value"}
            if fid == "current_ratio":
                ca=to_decimal(inputs.get("current_assets")); cl=to_decimal(inputs.get("current_liab"))
                if cl==0:
                    raise ValueError("Liabilitas lancar tidak boleh 0.")
                val=ca/cl
                return {"ok": True, "result": float(val), "steps":"Current Ratio = Current Assets / Current Liabilities"}
            if fid == "quick_ratio":
                cash=to_decimal(inputs.get("cash")); sti=to_decimal(inputs.get("sti")); recv=to_decimal(inputs.get("recv")); cl=to_decimal(inputs.get("current_liab"))
                if cl==0:
                    raise ValueError("Current liabilities tidak boleh 0.")
                val=(cash+sti+recv)/cl
                return {"ok": True, "result": float(val), "steps":"Quick Ratio=(Cash+STI+Receivables)/CL"}
            if fid == "break_even_units":
                fixed=to_decimal(inputs.get("fixed_cost"))
                price=to_decimal(inputs.get("price"))
                var=to_decimal(inputs.get("var_cost"))
                cm = price - var
                if cm<=0:
                    raise ValueError("Contribution margin per unit harus > 0.")
                units = fixed / cm
                return {"ok": True, "result": float(units), "steps":"BEP units = Fixed Cost / (Price-Variable Cost)"}
            if fid == "npv":
                r=float(to_decimal(inputs.get("rate")))
                cfs=self._parse_decimal_list(inputs.get("cashflows",""))
                if not cfs:
                    raise ValueError("Cashflows kosong.")
                npv=Decimal(0)
                for t,cf in enumerate(cfs):
                    npv += cf / (Decimal(1)+Decimal(r))**Decimal(t)
                return {"ok": True, "result": float(npv), "steps":"NPV = Σ CF_t/(1+r)^t"}
            if fid == "audit_dr":
                ar=float(to_decimal(inputs.get("ar"))); ir=float(to_decimal(inputs.get("ir"))); cr=float(to_decimal(inputs.get("cr")))
                denom=ir*cr
                if denom==0:
                    raise ValueError("IR*CR tidak boleh 0.")
                dr=ar/denom
                return {"ok": True, "result": dr, "steps":"DR = AR / (IR*CR)"}
            if fid == "ip_ipk":
                mutu=float(to_decimal(inputs.get("mutu"))); sks=float(to_decimal(inputs.get("sks")))
                if sks==0:
                    raise ValueError("SKS tidak boleh 0.")
                ip=mutu/sks
                return {"ok": True, "result": ip, "steps":"IP/IPK = Σ(nilai_mutu*SKS)/ΣSKS"}
            return {"ok": False, "error": "Formula tidak dikenal."}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def _parse_number_list(self, s: str) -> List[float]:
        s = (s or "").strip()
        if not s:
            return []
        parts = [p.strip() for p in s.split(",")]
        out=[]
        for p in parts:
            if p=="":
                continue
            out.append(float(to_decimal(p)))
        return out

    def _parse_decimal_list(self, s: str) -> List[Decimal]:
        s=(s or "").strip()
        if not s:
            return []
        parts=[p.strip() for p in s.split(",")]
        out=[]
        for p in parts:
            if p=="":
                continue
            out.append(to_decimal(p))
        return out
