import requests
import sys
import json
import re
from unidecode import unidecode
import urllib3

# Deshabilitar advertencias SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ============================================================
# VALIDACIÓN DE ARGUMENTOS
# ============================================================
if len(sys.argv) < 2:
    print('Uso: python consulta_completa.py "NOMBRE APELLIDO_PATERNO APELLIDO_MATERNO"')
    print('Ejemplo: python consulta_completa.py "Juan Perez Garcia"')
    sys.exit(1)

nombre_completo = sys.argv[1].strip()
partes_busqueda = [p.strip().lower() for p in nombre_completo.split() if p.strip()]

if len(partes_busqueda) < 3:
    print("[!] Advertencia: Se recomienda usar NOMBRE + APELLIDO_PATERNO + APELLIDO_MATERNO")
    print(f"[!] Usted ingresó: {nombre_completo}")
    print("[!] Continuando con búsqueda flexible...\n")

# ============================================================
# FUNCIONES COMPARTIDAS
# ============================================================
def format_mxn(value):
    try:
        return f"${float(value):,.2f} MXN"
    except (TypeError, ValueError):
        return str(value)

def normalizar_texto(texto):
    """Normaliza texto: elimina acentos, convierte a minúsculas y elimina caracteres especiales"""
    if not texto:
        return ""
    texto = unidecode(texto.lower())
    texto = re.sub(r'[^a-z0-9\s]', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

def es_coincidencia_exacta(nombre_persona, partes_busqueda):
    """
    Verifica si el nombre de la persona coincide EXACTAMENTE con los términos de búsqueda
    en el orden correcto: nombre + apellido paterno + apellido materno
    """
    if not nombre_persona or not partes_busqueda:
        return False
    
    nombre_normalizado = normalizar_texto(nombre_persona)
    partes_persona = nombre_normalizado.split()
    
    if len(partes_persona) < len(partes_busqueda):
        return False
    
    for i, termino in enumerate(partes_busqueda):
        if i >= len(partes_persona):
            return False
        if partes_persona[i] != termino:
            if not partes_persona[i].startswith(termino[:3]):
                return False
    
    return True

def es_coincidencia_aproximada(nombre_persona, partes_busqueda):
    """Verifica si el nombre contiene TODOS los términos de búsqueda en cualquier orden"""
    if not nombre_persona or not partes_busqueda:
        return False
    
    nombre_normalizado = normalizar_texto(nombre_persona)
    partes_persona = nombre_normalizado.split()
    
    for termino in partes_busqueda:
        encontrado = False
        for parte in partes_persona:
            if parte == termino or parte.startswith(termino[:3]):
                encontrado = True
                break
        if not encontrado:
            return False
    
    return True

# ============================================================
# FUNCIÓN 1: CONSULTA NÓMINA (buengobierno.gob.mx)
# ============================================================
def consultar_nomina(nombre_completo, partes_busqueda):
    """Consulta la API de nómina transparente"""
    print("\n" + "=" * 70)
    print("🔍 CONSULTANDO NÓMINA TRANSPARENTE")
    print("=" * 70)
    
    url = "https://services.buengobierno.gob.mx/nomina/consultas"
    
    payload = {
        "operationName": "consultaNombre",
        "query": """query consultaNombre($nombre: String!, $sn: Boolean!) {
          consultaNominaPorNombre(
            nombre: $nombre
            sn: $sn
          ) {
            servPubTotalSector
            listDtoServidorPublicoDto {
              institution: dependencia
              puesto: nombrePuesto
              nombre
              sueldoBruto
              sueldoNeto
            }
          }
        }""",
        "variables": {
            "nombre": nombre_completo,
            "sn": False
        }
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "Referer": "https://nominatransparente.rhnet.gob.mx/",
        "Origin": "https://nominatransparente.rhnet.gob.mx",
        "apikey": "vAYBrRwL4dfeYB8uYZ8xSpCuhwbDU2"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            print(f"[!] Error: Status {response.status_code}")
            return
        
        data = response.json()
        
        if "errors" in data:
            print("[!] GraphQL devolvió errores:")
            print(json.dumps(data["errors"], indent=2, ensure_ascii=False))
            return
        
        resultados = data.get("data", {}).get("consultaNominaPorNombre", {})
        total = resultados.get("servPubTotalSector", 0)
        lista = resultados.get("listDtoServidorPublicoDto", [])
        
        print(f"\n[+] Total de resultados de la API: {total}")
        print(f"[+] Procesando {len(lista)} registros...")
        
        if not lista:
            print("\n[!] No se encontraron resultados.")
            return
        
        # Filtrar coincidencias
        exactos = []
        aproximados = []
        
        for persona in lista:
            nombre_persona = persona.get('nombre', '')
            if not nombre_persona:
                continue
            
            if es_coincidencia_exacta(nombre_persona, partes_busqueda):
                exactos.append(persona)
            elif es_coincidencia_aproximada(nombre_persona, partes_busqueda):
                aproximados.append(persona)
        
        # Mostrar resultados
        if exactos:
            print(f"\n[✓] Coincidencias EXACTAS encontradas: {len(exactos)}")
            print("-" * 70)
            for i, persona in enumerate(exactos, 1):
                print(f"\n[{i}] Nombre       : {persona.get('nombre')}")
                print(f"    Institución : {persona.get('institution')}")
                print(f"    Puesto      : {persona.get('puesto')}")
                print(f"    Sueldo Bruto: {format_mxn(persona.get('sueldoBruto'))}")
                print(f"    Sueldo Neto : {format_mxn(persona.get('sueldoNeto'))}")
                print("-" * 70)
        elif aproximados:
            print(f"\n[!] No se encontraron coincidencias EXACTAS.")
            print(f"[i] Mostrando {len(aproximados)} coincidencias APROXIMADAS:\n")
            for i, persona in enumerate(aproximados[:10], 1):
                print(f"[{i}] Nombre       : {persona.get('nombre')}")
                print(f"    Institución : {persona.get('institution')}")
                print(f"    Puesto      : {persona.get('puesto')}")
                print(f"    Sueldo Bruto: {format_mxn(persona.get('sueldoBruto'))}")
                print(f"    Sueldo Neto : {format_mxn(persona.get('sueldoNeto'))}")
                print("-" * 70)
            if len(aproximados) > 10:
                print(f"\n[i] Mostrando 10 de {len(aproximados)} coincidencias aproximadas")
        else:
            print("\n[!] No se encontraron coincidencias exactas ni aproximadas.")
            print("[i] Mostrando primeros 5 resultados de la API como referencia:\n")
            for i, persona in enumerate(lista[:5], 1):
                print(f"[{i}] Nombre       : {persona.get('nombre')}")
                print(f"    Institución : {persona.get('institution')}")
                print("-" * 70)
                
    except requests.exceptions.RequestException as e:
        print(f"[!] Error de conexión: {e}")
    except json.JSONDecodeError as e:
        print(f"[!] Error al decodificar JSON: {e}")

# ============================================================
# FUNCIÓN 2: CONSULTA SANCIONADOS (datos.gob.mx)
# ============================================================
def consultar_sancionados(nombre, apellido_paterno, apellido_materno):
    """Consulta la API de servidores públicos sancionados"""
    print("\n" + "=" * 70)
    print("🔍 CONSULTANDO SERVIDORES PÚBLICOS SANCIONADOS")
    print("=" * 70)
    
    URL = "https://www.datos.gob.mx/datatables/ajax/34fccf9c-4d8c-42e2-8faa-e115ae7ae19f"
    
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) Gecko/20100101 Firefox/151.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-CSRF-Token": "Ijc2ZDNlYWRkYmQ1MGExM2QwNmJmZTA2MmY2NDE0ZThiODUyMWYyOTEi.ajdJGg.idhBnKZpg43VHLPgUEpX2WklN_s",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://www.datos.gob.mx",
        "Referer": "https://www.datos.gob.mx/dataset/servidores_publicos_sancionados_vigentes/resource/d5da6695-1a3b-4a86-93e2-4297e9463370/view/34fccf9c-4d8c-42e2-8faa-e115ae7ae19f",
        "Cookie": ("ckan=eyJfY3NyZl90b2tlbiI6Ijc2ZDNlYWRkYmQ1MGExM2QwNmJmZTA2MmY2NDE0ZThiODUyMWYyOTEiLCJfZnJlc2giOmZhbHNlLCJfcGVybWFuZW50Ijp0cnVlfQ.ajdH4Q.MPWFIrQG-Q8116sfQzVlQ6iTVeI; "
                   "visid_incap_3334407=SrSO3wMNQBuLM3+61de4DaIjEWoAAAAAQUIPAAAAAAAFvag1Jg0r6qUmDhLpnar3; "
                   "_ga_R1V0DG3C17=GS2.1.s1782008341$o2$g1$t1782008655$j17$l0$h0; "
                   "_ga=GA1.1.201058801.1779508129; "
                   "INGRESS_STICKY=1782007776.878.3367.619737|1da8c1effd9495956a1d69379862658c; "
                   "incap_ses_1809_3334407=0KX6UaZ9sHmutO5blNwaGRJKN2oAAAAA38mdOjRr6nzJ766FkZlOyQ=="),
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers"
    }
    
    # Construir payload con filtros
    payload = {
        "draw": 1,
        "columns[0][data]": "_id",
        "columns[0][name]": "_id",
        "columns[0][searchable]": "false",
        "columns[0][orderable]": "true",
        "columns[0][search][value]": "",
        "columns[0][search][regex]": "false",
        "columns[1][data]": "expediente",
        "columns[1][name]": "expediente",
        "columns[1][searchable]": "true",
        "columns[1][orderable]": "true",
        "columns[1][search][value]": "",
        "columns[1][search][regex]": "false",
        "columns[2][data]": "fecha_resolucion",
        "columns[2][name]": "fecha_resolucion",
        "columns[2][searchable]": "true",
        "columns[2][orderable]": "true",
        "columns[2][search][value]": "",
        "columns[2][search][regex]": "false",
        "columns[3][data]": "apellido_paterno",
        "columns[3][name]": "apellido_paterno",
        "columns[3][searchable]": "true",
        "columns[3][orderable]": "true",
        "columns[3][search][value]": apellido_paterno if apellido_paterno else "",
        "columns[3][search][regex]": "false",
        "columns[4][data]": "apellido_materno",
        "columns[4][name]": "apellido_materno",
        "columns[4][searchable]": "true",
        "columns[4][orderable]": "true",
        "columns[4][search][value]": apellido_materno if apellido_materno else "",
        "columns[4][search][regex]": "false",
        "columns[5][data]": "nombre",
        "columns[5][name]": "nombre",
        "columns[5][searchable]": "true",
        "columns[5][orderable]": "true",
        "columns[5][search][value]": nombre if nombre else "",
        "columns[5][search][regex]": "false",
        "columns[6][data]": "autoridad",
        "columns[6][name]": "autoridad",
        "columns[6][searchable]": "true",
        "columns[6][orderable]": "true",
        "columns[6][search][value]": "",
        "columns[6][search][regex]": "false",
        "columns[7][data]": "dependencia",
        "columns[7][name]": "dependencia",
        "columns[7][searchable]": "true",
        "columns[7][orderable]": "true",
        "columns[7][search][value]": "",
        "columns[7][search][regex]": "false",
        "columns[8][data]": "sancion_impuesta",
        "columns[8][name]": "sancion_impuesta",
        "columns[8][searchable]": "true",
        "columns[8][orderable]": "true",
        "columns[8][search][value]": "",
        "columns[8][search][regex]": "false",
        "columns[9][data]": "causa",
        "columns[9][name]": "causa",
        "columns[9][searchable]": "true",
        "columns[9][orderable]": "true",
        "columns[9][search][value]": "",
        "columns[9][search][regex]": "false",
        "columns[10][data]": "inicio",
        "columns[10][name]": "inicio",
        "columns[10][searchable]": "true",
        "columns[10][orderable]": "true",
        "columns[10][search][value]": "",
        "columns[10][search][regex]": "false",
        "columns[11][data]": "fin",
        "columns[11][name]": "fin",
        "columns[11][searchable]": "true",
        "columns[11][orderable]": "true",
        "columns[11][search][value]": "",
        "columns[11][search][regex]": "false",
        "columns[12][data]": "ley",
        "columns[12][name]": "ley",
        "columns[12][searchable]": "true",
        "columns[12][orderable]": "true",
        "columns[12][search][value]": "",
        "columns[12][search][regex]": "false",
        "order[0][column]": 0,
        "order[0][dir]": "asc",
        "start": 0,
        "length": 100,
        "search[value]": "",
        "search[regex]": "false",
        "filters": ""
    }
    
    try:
        response = requests.post(URL, headers=HEADERS, data=payload, timeout=30, verify=False)
        
        if response.status_code != 200:
            print(f"[!] Error: Status {response.status_code}")
            return
        
        data = response.json()
        total = data.get('recordsTotal', 0)
        records = data.get('data', [])
        
        print(f"\n[+] Total de registros con filtros: {total}")
        print(f"[+] Registros obtenidos: {len(records)}")
        
        if not records:
            print("\n[!] No se encontraron resultados.")
            return
        
        # Filtrar coincidencias exactas
        exactos = []
        for persona in records:
            nombre_persona = persona.get('nombre', '')
            if not nombre_persona:
                continue
            # Construir nombre completo de la persona para la comparación
            nombre_completo_persona = f"{persona.get('nombre', '')} {persona.get('apellido_paterno', '')} {persona.get('apellido_materno', '')}".strip()
            if es_coincidencia_exacta(nombre_completo_persona, partes_busqueda):
                exactos.append(persona)
        
        if exactos:
            print(f"\n[✓] Coincidencias EXACTAS encontradas: {len(exactos)}")
            print("-" * 70)
            for i, persona in enumerate(exactos, 1):
                print(f"\n[{i}] Nombre           : {persona.get('nombre', '')} {persona.get('apellido_paterno', '')} {persona.get('apellido_materno', '')}")
                print(f"    Expediente      : {persona.get('expediente', '')}")
                print(f"    Dependencia     : {persona.get('dependencia', '')}")
                print(f"    Autoridad       : {persona.get('autoridad', '')}")
                print(f"    Sancion Impuesta: {persona.get('sancion_impuesta', '')}")
                print(f"    Causa           : {persona.get('causa', '')}")
                print(f"    Fecha Resolución: {persona.get('fecha_resolucion', '')}")
                print(f"    Período         : {persona.get('inicio', '')} - {persona.get('fin', '')}")
                print("-" * 70)
        else:
            print("\n[!] No se encontraron coincidencias exactas.")
            print("[i] Mostrando primeros 5 resultados con los filtros aplicados:\n")
            for i, persona in enumerate(records[:5], 1):
                print(f"[{i}] {persona.get('nombre', '')} {persona.get('apellido_paterno', '')} {persona.get('apellido_materno', '')}")
                print(f"    Dependencia: {persona.get('dependencia', '')}")
                print(f"    Sancion    : {persona.get('sancion_impuesta', '')}")
                print("-" * 50)
        
    except requests.exceptions.RequestException as e:
        print(f"[!] Error de conexión: {e}")
    except json.JSONDecodeError as e:
        print(f"[!] Error al decodificar JSON: {e}")

# ============================================================
# EJECUCIÓN PRINCIPAL
# ============================================================
if __name__ == "__main__":
    # Extraer partes para la búsqueda
    if len(partes_busqueda) >= 3:
        nombre = partes_busqueda[0]
        apellido_paterno = partes_busqueda[1]
        apellido_materno = partes_busqueda[2]
    else:
        nombre = partes_busqueda[0] if len(partes_busqueda) >= 1 else ""
        apellido_paterno = partes_busqueda[1] if len(partes_busqueda) >= 2 else ""
        apellido_materno = partes_busqueda[2] if len(partes_busqueda) >= 3 else ""
    
    print("\n" + "=" * 70)
    print(f"🔍 BUSCANDO: {nombre_completo}")
    print(f"📋 Términos: {' + '.join(partes_busqueda)}")
    print("=" * 70)
    
    # Consultar ambas fuentes
    consultar_nomina(nombre_completo, partes_busqueda)
    consultar_sancionados(nombre, apellido_paterno, apellido_materno)
    
    print("\n" + "=" * 70)
    print("✅ BÚSQUEDA COMPLETADA")
    print("=" * 70)
