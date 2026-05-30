from django.shortcuts import render
from .logic import (
    calcular_taylor_maclaurin,
    generar_grafica,
    generar_grafica_secante,
    biseccion,
    secante
)
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
            n_terminos = int(request.POST.get("n_terminos", 5))

            try:
                punto_a = sp.sympify(punto_a_input) if punto_a_input else 0

                resultado_taylor = calcular_taylor_maclaurin(
                    funcion,
                    punto_a,
                    n_terminos
                )

                if resultado_taylor and not resultado_taylor.get("error"):
                    serie_obj = resultado_taylor["resultado_final_raw"]

                    resultado_taylor["grafica"] = generar_grafica(
                        funcion,
                        punto_a,
                        serie_obj
                    )

                resultado.update(resultado_taylor)

                historial.append({
                    "metodo": "Taylor",
                    "funcion": funcion,
                    "resultado": resultado_taylor.get("resultado_final"),
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
                })

            except Exception as e:
                resultado["error"] = str(e)

   
        elif funcion and metodo == "biseccion":
            a = request.POST.get("a")
            b = request.POST.get("b")

            try:
                a = float(a)
                b = float(b)

                resultado_biseccion = biseccion(funcion, a, b)

                resultado.update(resultado_biseccion)

                historial.append({
                    "metodo": "Bisección",
                    "funcion": funcion,
                    "resultado": resultado_biseccion.get("raiz_aproximada"),
                    "intervalo": f"[{a}, {b}]",
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
                })

            except Exception as e:
                resultado["error"] = str(e)
        
        elif funcion and metodo == "secante":

            x0 = request.POST.get("x0")
            x1 = request.POST.get("x1")

            try:
                x0 = float(x0)
                x1 = float(x1)

                resultado_secante = secante(funcion, x0, x1)

                resultado_secante["grafica"] = generar_grafica_secante(
                    funcion,
                    x0,
                    x1
                )

                resultado.update(resultado_secante)
                historial.append({
                    "metodo": "Secante",
                    "funcion": funcion,
                    "resultado": resultado_secante.get("raiz_aproximada"),
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
                })

            except Exception as e:
                resultado["error"] = str(e)

    # guardar historial en sesión
    request.session["historial"] = historial

    return render(request, "calculadora/index.html", {
        "resultado": resultado,
        "historial": historial
    })