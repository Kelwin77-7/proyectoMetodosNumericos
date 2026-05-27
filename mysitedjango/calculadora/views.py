from django.shortcuts import render
from . logic import calcular_taylor_maclaurin, generar_grafica
import sympy as sp
# Create your views here.


from django.shortcuts import render
from .logic import calcular_taylor_maclaurin, generar_grafica


def home(request):
    resultado = None
    if request.method == "POST":
        funcion = request.POST.get("funcion")
        punto_a_input = request.POST.get("punto_a", "0")
        n_terminos = int(request.POST.get("n_terminos", 5))
        try:
            punto_a = sp.sympify(punto_a_input) if punto_a_input else 0

            # Llamamos a la lógica principal
            resultado = calcular_taylor_maclaurin(funcion, punto_a, n_terminos)

            # Si no hay errores, generamos la gráfica
            if resultado and not resultado.get('error'):
                serie_obj = resultado['resultado_final_raw']
                resultado['grafica'] = generar_grafica(
                    funcion, punto_a, serie_obj)
        except Exception as e:
            resultado = {'error': str(e)}

    return render(request, "calculadora/index.html", {"resultado": resultado})
