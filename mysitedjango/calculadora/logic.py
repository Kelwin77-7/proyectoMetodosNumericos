import sympy as sp
import plotly.graph_objects as go
import numpy as np


def calcular_taylor_maclaurin(funcion_str, punto_a, n_terminos=5):
    """
    Calcula la serie de Taylor. Si punto_a = 0, es Maclaurin.
    """
    x = sp.symbols('x')
    try:
        # Convertimos el texto (ej: "sin(x)") en una expresión matemática
        f_procesada = funcion_str.replace("^", "**")
        f = sp.sympify(f_procesada, locals={'x': sp.symbols('x')})

        serie = 0
        pasos = []

        for i in range(n_terminos):
            # 1. Derivada i-ésima
            derivada = sp.diff(f, x, i)
            # 2. Evaluar en el punto a
            valor_en_a = derivada.subs(x, punto_a)
            # 3. Construir el término
            termino = (valor_en_a / sp.factorial(i)) * (x - punto_a)**i
            serie += termino

            pasos.append({
                'n': i,
                'derivada': str(derivada),
                'valor_derivada': str(valor_en_a),
                'termino_latex': sp.latex(termino)
            })

        return {
            'resultado_final': sp.latex(serie),
            'resultado_final_raw': serie,  # <-- AGREGAMOS ESTO PARA LA GRÁFICA
            'pasos': pasos,
            'error': None
        }
    except Exception as e:
        return {'error': str(e)}


def generar_grafica(funcion_str, punto_a, serie_sympy):
    x_sym = sp.symbols('x')
    try:
        # Convertimos las funciones de SymPy a funciones que NumPy entienda
        f_num = sp.lambdify(x_sym, sp.sympify(
            funcion_str.replace("^", "**")), "numpy")
        p_num = sp.lambdify(x_sym, serie_sympy, "numpy")

        # Rango de la gráfica (5 unidades a la izquierda y derecha del punto a)
        x_vals = np.linspace(float(punto_a) - 5, float(punto_a) + 5, 400)

        y_original = f_num(x_vals)
        y_taylor = p_num(x_vals)

        # Si f_num devuelve un solo número (función constante), lo convertimos en array
        if isinstance(y_original, (int, float, complex)):
            y_original = np.full_like(x_vals, y_original)
        if isinstance(y_taylor, (int, float, complex)):
            y_taylor = np.full_like(x_vals, y_taylor)

        fig = go.Figure()
        # Línea de la función original
        fig.add_trace(go.Scatter(x=x_vals, y=y_original,
                      name="f(x) Original", line=dict(color='#007bff')))
        # Línea de la aproximación de Taylor
        fig.add_trace(go.Scatter(x=x_vals, y=y_taylor, name="Aprox. Taylor", line=dict(
            color='#ff7f0e', dash='dash')))

        fig.update_layout(
            title="Visualización: Función vs Aproximación",
            xaxis_title="x",
            yaxis_title="y",
            template="plotly_white",
            autosize=True,  # <-- Esto es clave
            # Ajustamos márgenes para que no se corte
            margin=dict(l=40, r=20, t=40, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        xanchor="right", x=1)  # Leyenda arriba
        )

        return fig.to_html(full_html=False)
    except:
        return "<p class='text-danger'>No se pudo generar la gráfica para esta función.</p>"
