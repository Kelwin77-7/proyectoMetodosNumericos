from django.shortcuts import render
from .logic import *
import sympy as sp
from datetime import datetime


def home(request):
    resultado = {}
    historial = request.session.get("historial", [])

    if request.method == "POST":
        funcion = request.POST.get("funcion", "")
        metodo = request.POST.get("metodo", "")

        if funcion and metodo == "taylor":
            punto_a_input = request.POST.get("punto_a", "0")
            n = int(request.POST.get("n_terminos", 5))
            try:
                a = sp.sympify(punto_a_input)
                res = calcular_taylor_maclaurin(funcion, a, n)
                if not res.get("error"):
                    res["grafica"] = generar_grafica(
                        funcion, a, res["resultado_final_raw"])
                    res["descripcion"] = "El método de Taylor es una técnica matemática utilizada para aproximar funciones mediante polinomios. Su idea principal consiste en representar una función compleja usando derivadas calculadas en un punto específico, permitiendo obtener resultados aproximados de manera más sencilla. El método de Maclaurin es un caso especial de la serie de Taylor donde el punto de expansión es cero. Ambos métodos son ampliamente utilizados en matemáticas, física, ingeniería y programación para simplificar cálculos y analizar el comportamiento de funciones."
                    res["formula"] = r"P(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(a)}{n!}(x-a)^n"
                    # Corregido: usando \\( \\) para MathJax
                    res["ejemplo_datos"] = f"Para tu función, evaluamos \\( f({a}) = {res['f_eval_a']} \\) y calculamos {n} derivadas para construir el polinomio aproximado."
                resultado.update(res)
            except Exception as e:
                resultado["error"] = str(e)

        elif funcion and metodo == "biseccion":
            a_in, b_in = request.POST.get("a"), request.POST.get("b")
            try:
                a, b = float(a_in), float(b_in)
                res = biseccion(funcion, a, b)
                if not res.get("error"):
                    res["grafica"] = generar_grafica_raices(
                        funcion, [a, b, res["raiz_aproximada"]], "Visualización Bisección")
                    res["descripcion"] = "El método de bisección es un método numérico empleado para encontrar raíces de ecuaciones, es decir, valores donde una función se hace igual a cero. El procedimiento consiste en dividir repetidamente un intervalo en dos partes y seleccionar el subintervalo donde existe un cambio de signo en la función, ya que esto indica la presencia de una raíz."
                    res["formula"] = r"c = \frac{a+b}{2}"
                    res["ejemplo_datos"] = f"Iniciamos en \\( [{a}, {b}] \\). Como \\( f({a})={res['fa_inicial']} \\) y \\( f({b})={res['fb_inicial']} \\) tienen signos opuestos, la raíz está garantizada en este rango."
                resultado.update(res)
            except Exception as e:
                resultado["error"] = str(e)

        elif funcion and metodo == "secante":
            x0_in, x1_in = request.POST.get("x0"), request.POST.get("x1")
            try:
                x0, x1 = float(x0_in), float(x1_in)
                res = secante(funcion, x0, x1)
                if not res.get("error"):
                    res["grafica"] = generar_grafica_secante(funcion, x0, x1)
                    res["descripcion"] = "El método de la secante es un método numérico utilizado para calcular raíces de ecuaciones de manera aproximada. A diferencia del método de bisección, este utiliza dos valores iniciales cercanos a la raíz y construye una línea secante entre ellos para estimar una nueva aproximación. Este método suele converger más rápido que el de bisección y no requiere calcular derivadas, por lo que es muy utilizado en problemas de análisis numérico y programación científica."
                    res["formula"] = r"x_{n+1} = x_n - \frac{f(x_n)(x_n - x_{n-1})}{f(x_n) - f(x_{n-1})}"
                    res["ejemplo_datos"] = f"Con los puntos iniciales \\( x_0={x0} \\) y \\( x_1={x1} \\), calculamos las imágenes \\( f(x_0)={res['fx0_inicial']} \\) y \\( f(x_1)={res['fx1_inicial']} \\) para proyectar la siguiente aproximación."
                resultado.update(res)
            except Exception as e:
                resultado["error"] = str(e)

        if not resultado.get("error"):
            historial.append({"metodo": metodo.capitalize(
            ), "funcion": funcion, "fecha": datetime.now().strftime("%H:%M")})
            request.session["historial"] = historial

    return render(request, "calculadora/index.html", {"resultado": resultado, "historial": historial})
