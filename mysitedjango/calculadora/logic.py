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

            pasos.append({
                "n": i,
                "derivada": sp.latex(derivada),
                "valor_derivada": sp.latex(sp.simplify(valor_en_a)),
                "termino_latex": sp.latex(sp.simplify(termino))
            })

        return {
            "resultado_final": sp.latex(serie),
            "resultado_final_raw": serie,
            "pasos": pasos,
            "error": None
        }

    except Exception as e:
        return {"error": str(e)}


def generar_grafica(funcion_str, punto_a, serie_sympy):
    x = sp.symbols('x')

    try:
        f_num = sp.lambdify(x, sp.sympify(funcion_str.replace("^", "**")), "numpy")
        p_num = sp.lambdify(x, serie_sympy, "numpy")

        x_vals = np.linspace(float(punto_a) - 5, float(punto_a) + 5, 400)

        y1 = f_num(x_vals)
        y2 = p_num(x_vals)

        if isinstance(y1, (int, float)):
            y1 = np.full_like(x_vals, y1)
        if isinstance(y2, (int, float)):
            y2 = np.full_like(x_vals, y2)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=x_vals, y=y1,
            name="f(x)",
            line=dict(color="#007bff")
        ))

        fig.add_trace(go.Scatter(
            x=x_vals, y=y2,
            name="Taylor",
            line=dict(color="#ff7f0e", dash="dash")
        ))

        fig.update_layout(
            title="Función vs Aproximación",
            template="plotly_white",
            margin=dict(l=40, r=20, t=40, b=40)
        )

        return fig.to_html(full_html=False)

    except:
        return "<p>Error al generar gráfica</p>"


def biseccion(funcion_str, a, b, tolerancia=1e-6, max_iter=100):
    x = sp.symbols('x')

    try:
        f = sp.sympify(funcion_str.replace("^", "**"))

        def fx(val):
            return float(f.subs(x, val))

        if fx(a) * fx(b) >= 0:
            return {
                "error": "La función no cambia de signo en el intervalo."
            }

        iteraciones = []

        c = 0

        for i in range(max_iter):
            c = (a + b) / 2
            fc = fx(c)

            iteraciones.append({
                "iter": i + 1,
                "a": a,
                "b": b,
                "c": c,
                "f_c": fc
            })

            if abs(fc) < tolerancia:
                break

            if fx(a) * fc < 0:
                b = c
            else:
                a = c

        return {
            "raiz_aproximada": c,
            "iteraciones": iteraciones,
            "error": None
        }

    except Exception as e:
        return {"error": str(e)}
    
def secante(funcion_str, x0, x1, tolerancia=1e-6, max_iter=100):
    x = sp.symbols('x')

    try:
        f = sp.sympify(funcion_str.replace("^", "**"))

        def fx(val):
            return float(f.subs(x, val))

        iteraciones = []

        for i in range(max_iter):

            f_x0 = fx(x0)
            f_x1 = fx(x1)

            if (f_x1 - f_x0) == 0:
                return {
                    "error": "División entre cero en la fórmula de secante."
                }

            x2 = x1 - (f_x1 * (x1 - x0)) / (f_x1 - f_x0)

            iteraciones.append({
                "iter": i + 1,
                "x0": x0,
                "x1": x1,
                "x2": x2,
                "f_x2": fx(x2)
            })

            if abs(fx(x2)) < tolerancia:
                break

            x0 = x1
            x1 = x2

        return {
            "raiz_aproximada": x2,
            "iteraciones": iteraciones,
            "error": None
        }

    except Exception as e:
        return {"error": str(e)}
    
def generar_grafica_secante(funcion_str, x0, x1):
    x = sp.symbols('x')

    try:
        f = sp.sympify(funcion_str.replace("^", "**"))
        f_num = sp.lambdify(x, f, "numpy")

        x_vals = np.linspace(min(x0, x1) - 5, max(x0, x1) + 5, 400)
        y_vals = f_num(x_vals)

        fig = go.Figure()

        # Función
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_vals,
            name="f(x)"
        ))

        # Puntos iniciales
        fig.add_trace(go.Scatter(
            x=[x0, x1],
            y=[f_num(x0), f_num(x1)],
            mode="markers",
            name="Puntos iniciales"
        ))

        fig.update_layout(
            title="Método de la Secante",
            template="plotly_white"
        )

        return fig.to_html(full_html=False)

    except Exception:
        return "<p>Error al generar gráfica</p>"