import sympy as sp
import plotly.graph_objects as go
import numpy as np


def calcular_taylor_maclaurin(funcion_str, punto_a, n_terminos=5):
    x = sp.symbols('x')
    try:
        f_procesada = funcion_str.replace("^", "**")
        f = sp.sympify(f_procesada)
        serie = 0
        pasos = []

        for i in range(n_terminos):
            derivada = sp.diff(f, x, i)
            valor_en_a = derivada.subs(x, punto_a)
            termino = (valor_en_a / sp.factorial(i)) * (x - punto_a)**i
            serie += termino

            for i in range(n_terminos):
                derivada = sp.diff(f, x, i)
                valor_en_a = derivada.subs(x, punto_a)
                denominador = sp.factorial(i)
                termino = (valor_en_a / denominador) * (x - punto_a)**i
                serie += termino

                # Texto explicativo personalizado por paso
                if i == 0:
                    explicacion = f"Calculamos el valor inicial de la función en $x={punto_a}$."
                elif i == 1:
                    explicacion = f"Obtenemos la primera derivada y evaluamos la pendiente en el punto."
                else:
                    explicacion = f"Calculamos la derivada de orden {i} para ajustar la curvatura."

            pasos.append({
                "n": i,
                "derivada": sp.latex(derivada),
                "valor_derivada": sp.latex(sp.simplify(valor_en_a)),
                "denominador": sp.factorial(i),
                "potencia": sp.latex(sp.simplify((x - punto_a)**i)),
                "termino_latex": sp.latex(sp.simplify(termino))
            })

        return {
            "resultado_final": sp.latex(serie),
            "resultado_final_raw": serie,
            "pasos": pasos,
            "f_eval_a": sp.latex(sp.simplify(f.subs(x, punto_a))),
            "error": None
        }
    except Exception as e:
        return {"error": f"Error en Taylor: {str(e)}"}


def biseccion(funcion_str, a, b, tolerancia=1e-6, max_iter=100):
    x = sp.symbols('x')
    try:
        f_expr = sp.sympify(funcion_str.replace("^", "**"))
        f = sp.lambdify(x, f_expr, "numpy")

        fa_init, fb_init = float(f(a)), float(f(b))
        if fa_init * fb_init >= 0:
            return {"error": "Teorema de Bolzano no aplicable: f(a) y f(b) deben tener signos opuestos."}

        iteraciones = []
        for i in range(max_iter):
            fa = float(f(a))
            fb = float(f(b))
            c = (a + b) / 2
            fc = float(f(c))

            iteraciones.append({
                "iter": i + 1,
                "a": a,
                "b": b,
                "c": c,
                "fa": fa,
                "fb": fb,
                "fc": fc,
                "cambio_signo": "Izquierda (a, c)" if fa * fc < 0 else "Derecha (c, b)"
            })

            if abs(fc) < tolerancia or (b - a) / 2 < tolerancia:
                break

            if fa * fc < 0:
                b = c
            else:
                a = c

        return {
            "raiz_aproximada": round(c, 6),
            "iteraciones": iteraciones,
            "fa_inicial": round(fa_init, 4),
            "fb_inicial": round(fb_init, 4),
            "error": None
        }
    except Exception as e:
        return {"error": f"Error matemático: {str(e)}"}


def secante(funcion_str, x0, x1, tolerancia=1e-6, max_iter=100):
    x = sp.symbols('x')
    try:
        f_expr = sp.sympify(funcion_str.replace("^", "**"))
        f = sp.lambdify(x, f_expr, "numpy")

        iteraciones = []
        for i in range(max_iter):
            fx0, fx1 = float(f(x0)), float(f(x1))
            if fx1 - fx0 == 0:
                return {"error": "División por cero en la fórmula (pendiente nula)."}

            x2 = x1 - (fx1 * (x1 - x0)) / (fx1 - fx0)
            f_x2 = float(f(x2))

            iteraciones.append({
                "iter": i + 1, "x0": x0, "x1": x1, "x2": x2, "f_x2": f_x2
            })

            if abs(f_x2) < tolerancia:
                break
            x0, x1 = x1, x2

        return {
            "raiz_aproximada": round(x2, 6),
            "iteraciones": iteraciones,
            "fx0_inicial": round(float(f(iteraciones[0]['x0'])), 4),
            "fx1_inicial": round(float(f(iteraciones[0]['x1'])), 4)
        }
    except Exception as e:
        return {"error": f"Error en Secante: {str(e)}"}


def generar_grafica(funcion_str, punto_a, serie_sympy):
    x = sp.symbols('x')
    try:
        f_num = sp.lambdify(x, sp.sympify(
            funcion_str.replace("^", "**")), "numpy")
        p_num = sp.lambdify(x, serie_sympy, "numpy")
        x_vals = np.linspace(float(punto_a) - 5, float(punto_a) + 5, 400)
        y1, y2 = f_num(x_vals), p_num(x_vals)
        if isinstance(y1, (int, float, np.number)):
            y1 = np.full_like(x_vals, y1)
        if isinstance(y2, (int, float, np.number)):
            y2 = np.full_like(x_vals, y2)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y1,
                      name="f(x) original", line=dict(color="#007bff")))
        fig.add_trace(go.Scatter(x=x_vals, y=y2, name="Aprox. Taylor",
                      line=dict(color="#ff7f0e", dash="dash")))
        fig.update_layout(template="plotly_white", height=350,
                          margin=dict(l=10, r=10, t=40, b=10))
        return fig.to_html(full_html=False)
    except:
        return ""


def generar_grafica_raices(funcion_str, puntos, titulo):
    x_sym = sp.symbols('x')
    try:
        f_num = sp.lambdify(x_sym, sp.sympify(
            funcion_str.replace("^", "**")), "numpy")
        x_vals = np.linspace(min(puntos) - 2, max(puntos) + 2, 400)
        y_vals = f_num(x_vals)
        if isinstance(y_vals, (int, float, np.number)):
            y_vals = np.full_like(x_vals, y_vals)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals,
                      name="f(x)", line=dict(color="#28a745")))
        fig.add_hline(y=0, line_color="black")
        fig.add_trace(go.Scatter(
            x=[puntos[-1]], y=[0], mode="markers", marker=dict(color="red", size=12), name="Raíz"))
        fig.update_layout(title=titulo, template="plotly_white",
                          height=350, margin=dict(l=10, r=10, t=40, b=10))
        return fig.to_html(full_html=False)
    except:
        return ""


def generar_grafica_secante(funcion_str, x0, x1):
    x = sp.symbols('x')
    try:
        f_num = sp.lambdify(x, sp.sympify(
            funcion_str.replace("^", "**")), "numpy")
        x_vals = np.linspace(min(x0, x1) - 3, max(x0, x1) + 3, 400)
        y_vals = f_num(x_vals)
        if isinstance(y_vals, (int, float, np.number)):
            y_vals = np.full_like(x_vals, y_vals)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals,
                      name="f(x)", line=dict(color="#ffc107")))
        fig.add_hline(y=0, line_color="black")
        fig.add_trace(go.Scatter(x=[x0, x1], y=[float(f_num(x0)), float(
            f_num(x1))], mode="markers+lines", name="Secante", line=dict(dash="dot")))
        fig.update_layout(template="plotly_white", height=350,
                          margin=dict(l=10, r=10, t=40, b=10))
        return fig.to_html(full_html=False)
    except:
        return ""
