from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def article_list(request: HttpRequest) -> HttpResponse:
    """Simple public listing of newsletter / article content.

    For ahora usamos contenido estatico tipo blog educativo sobre AI aplicada.
    Mas adelante se puede conectar a un modelo o CMS.
    """

    # Articulos estaticos iniciales pensados para educar a directores y duenos.
    articles = [
        {
            "slug": "tipos-proyectos-ai-planta",
            "title": "Tres tipos de proyectos de AI en planta y cuando usar cada uno",
            "summary": "Analiticos descriptivos, predictivos y prescriptivos: cuando sirve cada uno y que datos necesitan.",
            "reading_time": "4 min",
            "category": "Conceptos",
        },
        {
            "slug": "checklist-mantenimiento-predictivo",
            "title": "Checklist basico para un piloto de mantenimiento predictivo",
            "summary": "Sensores, frecuencia de datos, ventanas de tiempo y como medir el impacto en paros no planificados.",
            "reading_time": "5 min",
            "category": "Casos de uso",
        },
        {
            "slug": "hablar-ai-consejo",
            "title": "Como hablar de AI con tu consejo o socios sin caer en buzzwords",
            "summary": "Manera simple de traducir algoritmos en impacto financiero y riesgos entendibles.",
            "reading_time": "3 min",
            "category": "Gestion",
        },
        {
            "slug": "vision-artificial-calidad",
            "title": "Vision artificial para control de calidad: cuando vale la pena?",
            "summary": "Criterios para decidir si tu linea de produccion se beneficia de camaras e inspeccion automatica.",
            "reading_time": "6 min",
            "category": "Casos de uso",
        },
        {
            "slug": "datos-erp-ai",
            "title": "Como aprovechar los datos de tu ERP para proyectos de AI",
            "summary": "Tu sistema ya guarda anos de informacion valiosa. Aqui te decimos como extraerla y prepararla.",
            "reading_time": "5 min",
            "category": "Datos",
        },
        {
            "slug": "prediccion-demanda-pymes",
            "title": "Prediccion de demanda para pymes: lo que si funciona",
            "summary": "Modelos simples que puedes implementar hoy para reducir inventario muerto y faltantes.",
            "reading_time": "7 min",
            "category": "Casos de uso",
        },
        {
            "slug": "equipo-interno-vs-consultoria",
            "title": "Armo equipo interno de datos o contrato consultoria?",
            "summary": "Pros, contras y costos reales de cada opcion para una pyme industrial mexicana.",
            "reading_time": "4 min",
            "category": "Gestion",
        },
        {
            "slug": "seguridad-datos-industria",
            "title": "Seguridad de datos en proyectos industriales de AI",
            "summary": "Buenas practicas para proteger informacion sensible de produccion y clientes.",
            "reading_time": "5 min",
            "category": "Seguridad",
        },
    ]

    return render(request, "newsletter/list.html", {"articles": articles})
