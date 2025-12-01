#Codigo ejemplo para cargar CFDI en la base de datos

import os
import xml.etree.ElementTree as ET
import psycopg2
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime

# -------------------------
# CONFIG DB
# -------------------------
DB_HOST = "tu host"
DB_NAME = "tu base de datos"
DB_USER = "tu usuario"
DB_PASS = "tu contraseña"

# -------------------------
# Conexión DB
# -------------------------
conn = psycopg2.connect(
    host=DB_HOST,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)
cur = conn.cursor()

# -------------------------
# Helpers
# -------------------------
def to_float(v):
    if v is None or v == "":
        return 0.0
    try:
        return float(v)
    except:
        try:
            return float(str(v).replace(",", ""))
        except:
            return 0.0

def obtener_impuestos_concepto(concepto_elem, ns):
    """
    Extrae impuestos trasladados y retenciones del nodo Concepto.
    Devuelve dict con columnas que coinciden con tus tablas.
    """
    imp = {
        "iva_16": 0.0, "iva_8": 0.0, "iva_4": 0.0, "iva_0": 0.0,
        "iva_exento": 0.0, "iva_no_objeto": 0.0,
        "ieps_cuota": 0.0, "ieps_tasa": 0.0, "ieps_millar": 0.0,
        "ish_tasa": 0.0, "ish_importe": 0.0,
        "retencion_isr_10": 0.0, "retencion_isr_125": 0.0,
        "retencion_iva": 0.0, "retencion_ieps": 0.0
    }

    nodo_imp = concepto_elem.find("cfdi:Impuestos", ns)
    if nodo_imp is None:
        return imp

    # Traslados
    traslados = nodo_imp.find("cfdi:Traslados", ns)
    if traslados is not None:
        for t in traslados.findall("cfdi:Traslado", ns):
            impuesto = (t.attrib.get("Impuesto") or "").strip().upper()
            tipo_factor = (t.attrib.get("TipoFactor") or "").strip().lower()
            tasa = (t.attrib.get("TasaOCuota") or t.attrib.get("Tasa") or "").strip()
            importe = to_float(t.attrib.get("Importe"))

            if impuesto in ("002", "IVA"):
                # Normalizar tasas conocidas
                if tasa in ("0.160000", "0.16"):
                    imp["iva_16"] += importe
                elif tasa in ("0.080000", "0.08"):
                    imp["iva_8"] += importe
                elif tasa in ("0.040000", "0.04"):
                    imp["iva_4"] += importe
                elif tasa in ("0.000000", "0.0", "0", ""):
                    if tipo_factor == "exento":
                        imp["iva_exento"] += importe
                    elif tipo_factor in ("noobjeto", "no objeto", "no_objeto"):
                        imp["iva_no_objeto"] += importe
                    else:
                        imp["iva_0"] += importe
                else:
                    imp["iva_0"] += importe

            elif impuesto in ("003", "IEPS"):
                # IEPS puede venir al millar, tasa o cuota
                try:
                    ft = float(tasa) if tasa else None
                    if ft is not None and abs(ft - 0.005) < 1e-9:
                        imp["ieps_millar"] += importe
                    elif ft is not None and ft < 1:
                        imp["ieps_tasa"] += importe
                    else:
                        imp["ieps_cuota"] += importe
                except:
                    imp["ieps_cuota"] += importe

            elif impuesto in ("004", "ISH") or "HOSPE" in impuesto:
                imp["ish_importe"] += importe
                try:
                    imp["ish_tasa"] += float(tasa) if tasa else 0.0
                except:
                    pass
            else:
                # otros trasladados no mapeados (se pueden agregar si aparecen)
                pass

    # Retenciones
    retenciones = nodo_imp.find("cfdi:Retenciones", ns)
    if retenciones is not None:
        for r in retenciones.findall("cfdi:Retencion", ns):
            impuesto = (r.attrib.get("Impuesto") or "").strip().upper()
            tasa = (r.attrib.get("TasaOCuota") or "").strip()
            importe = to_float(r.attrib.get("Importe"))

            if impuesto in ("002", "IVA"):
                imp["retencion_iva"] += importe
            elif impuesto in ("001", "ISR"):
                if tasa in ("0.100000", "0.10"):
                    imp["retencion_isr_10"] += importe
                elif tasa in ("0.012500", "0.0125"):
                    imp["retencion_isr_125"] += importe
                else:
                    imp["retencion_isr_10"] += importe
            elif impuesto in ("003", "IEPS"):
                imp["retencion_ieps"] += importe
            else:
                pass

    return imp

# -------------------------
# Parser XML general
# -------------------------
def parsear_archivo_xml(path):
    """
    Retorna (tipo_comprobante, registros, mensaje_error)
    - tipo_comprobante: 'I','E','P','N', etc.
    - registros: lista de dicts, uno por concepto con impuestos ya separados.
    - mensaje_error: None o texto de error
    """
    try:
        tree = ET.parse(path)
        root = tree.getroot()
    except Exception as e:
        return None, [], f"Error parseando XML: {e}"

    # Detectar versión y namespaces
    version = root.attrib.get("Version", root.attrib.get("version", ""))
    ns = {
        "cfdi": "http://www.sat.gob.mx/cfd/4" if version == "4.0" else "http://www.sat.gob.mx/cfd/3",
        "tfd": "http://www.sat.gob.mx/TimbreFiscalDigital"
    }

    tipo_comprobante = (root.attrib.get("TipoDeComprobante") or "").upper()

    # CFDI relacionados (si existen) -> tomar primer CfdiRelacionado encontrado
    cfdi_rel_uuid = ""
    cfdi_rel_serie = ""
    cfdi_rel_folio = ""
    for cr in root.findall("cfdi:CfdiRelacionados", ns):
        rel = cr.find("cfdi:CfdiRelacionado", ns)
        if rel is not None:
            cfdi_rel_uuid = rel.attrib.get("UUID") or rel.attrib.get("Uuid", "") or ""
            cfdi_rel_serie = rel.attrib.get("Serie", "") or rel.attrib.get("serie", "") or ""
            cfdi_rel_folio = rel.attrib.get("Folio", "") or rel.attrib.get("folio", "") or ""
            break

    # Timbre (UUID principal)
    nodo_timbre = root.find(".//tfd:TimbreFiscalDigital", ns)
    timbre = nodo_timbre.attrib if nodo_timbre is not None else {}

    comprobante = root.attrib
    conceptos = root.findall(".//cfdi:Concepto", ns)

    # ====== CORRECCIÓN: Definir 'emisor' y 'receptor' correctamente ======
    emisor = root.find("cfdi:Emisor", ns)
    receptor = root.find("cfdi:Receptor", ns)
    # Si los nodos no existen, se devuelve un dict vacío para evitar errores.
    emisor = emisor.attrib if emisor is not None else {}
    receptor = receptor.attrib if receptor is not None else {}

    registros = []
    subtotal_comprobante = to_float(comprobante.get("SubTotal"))
    total_comprobante = to_float(comprobante.get("Total"))

    # Buscar IVA total dentro de Impuestos del comprobante
    nodo_imp_comprobante = root.find("cfdi:Impuestos", ns)
    if nodo_imp_comprobante is not None:
        try:
            iva_total_comprobante = to_float(nodo_imp_comprobante.attrib.get("TotalImpuestosTrasladados"))
        except:
            iva_total_comprobante = 0.0

    # Descuentos e IVA total del comprobante
    descuento_global = to_float(comprobante.get("Descuento"))
    iva_total_comprobante = 0.0

    # Buscar IVA total dentro de Impuestos del comprobante
    nodo_imp_comprobante = root.find("cfdi:Impuestos", ns)
    if nodo_imp_comprobante is not None:
        try:
            iva_total_comprobante = to_float(nodo_imp_comprobante.attrib.get("TotalImpuestosTrasladados"))
        except:
            iva_total_comprobante = 0.0

    for c in conceptos:
        impuestos = obtener_impuestos_concepto(c, ns)

        reg = {
            "cfdi_relacionado_uuid": cfdi_rel_uuid,
            "cfdi_relacionado_serie": cfdi_rel_serie,
            "cfdi_relacionado_folio": cfdi_rel_folio,

            "uuid": (timbre.get("UUID") or timbre.get("Uuid") or ""),
            "fecha": comprobante.get("Fecha"),
            "serie": comprobante.get("Serie", ""),
            "folio": comprobante.get("Folio", ""),
            "tipo_comprobante": tipo_comprobante,

            "rfc_emisor": emisor.get("Rfc", ""),
            "nombre_emisor": emisor.get("Nombre", ""),
            "rfc_receptor": receptor.get("Rfc", ""),
            "nombre_receptor": receptor.get("Nombre", ""),

            "claveprodserv": c.attrib.get("ClaveProdServ", ""),
            "cantidad": to_float(c.attrib.get("Cantidad")),
            "claveunidad": c.attrib.get("ClaveUnidad", ""),
            "descripcion": c.attrib.get("Descripcion", ""),
            "valorunitario": to_float(c.attrib.get("ValorUnitario")),
            "importe": to_float(c.attrib.get("Importe")),
            "descuento_concepto": to_float(c.attrib.get("Descuento")),
            "subtotal_comprobante": subtotal_comprobante,
            "total_comprobante": total_comprobante,
            "descuento_global": descuento_global,
            "iva_total_comprobante": iva_total_comprobante
        }

        # anexar impuestos/retenciones por columnas
        reg.update(impuestos)
        registros.append(reg)

    return tipo_comprobante, registros, None

# -------------------------
# Inserciones (facturas / notas)
# -------------------------
def insertar_facturas_conceptos(registros, datos_generales):
    if not registros:
        return 0, 0
    uuid = registros[0].get("uuid", "")
    # comprobar existencia en tabla facturas
    cur.execute("SELECT 1 FROM facturas WHERE uuid = %s LIMIT 1", (uuid,))
    if cur.fetchone():
        log_write(f"⚠ UUID ya existe en tabla facturas -> {uuid} (se omiten todos sus conceptos)")
        return 0, len(registros)

    insertados = 0
    for r in registros:
        payload = {**datos_generales, **r}
        cur.execute("""
            INSERT INTO facturas (
                unidad_operativa, num_comprobacion, responsable_del_gasto, tipo_comprobacion, contrato,
                cfdi_relacionado_uuid, cfdi_relacionado_serie, cfdi_relacionado_folio,
                uuid, fecha, serie, folio, tipo_comprobante,
                rfc_emisor, nombre_emisor, rfc_receptor, nombre_receptor,
                claveprodserv, cantidad, claveunidad, descripcion,
                valorunitario, importe, descuento_concepto,
                iva_16, iva_8, iva_4, iva_0, iva_exento, iva_no_objeto,
                ieps_cuota, ieps_tasa, ieps_millar,
                ish_tasa, ish_importe,
                retencion_isr_10, retencion_isr_125, retencion_iva, retencion_ieps,
                subtotal_comprobante, total_comprobante, descuento_global, iva_total_comprobante
            ) VALUES (
                %(unidad_operativa)s, %(num_comprobacion)s, %(responsable_del_gasto)s, %(tipo_comprobacion)s, %(contrato)s,
                %(cfdi_relacionado_uuid)s, %(cfdi_relacionado_serie)s, %(cfdi_relacionado_folio)s,
                %(uuid)s, %(fecha)s, %(serie)s, %(folio)s, %(tipo_comprobante)s,
                %(rfc_emisor)s, %(nombre_emisor)s, %(rfc_receptor)s, %(nombre_receptor)s,
                %(claveprodserv)s, %(cantidad)s, %(claveunidad)s, %(descripcion)s,
                %(valorunitario)s, %(importe)s, %(descuento_concepto)s,
                %(iva_16)s, %(iva_8)s, %(iva_4)s, %(iva_0)s, %(iva_exento)s, %(iva_no_objeto)s,
                %(ieps_cuota)s, %(ieps_tasa)s, %(ieps_millar)s,
                %(ish_tasa)s, %(ish_importe)s,
                %(retencion_isr_10)s, %(retencion_isr_125)s, %(retencion_iva)s, %(retencion_ieps)s,
                %(subtotal_comprobante)s, %(total_comprobante)s, %(descuento_global)s, %(iva_total_comprobante)s
            );
        """, payload)
        insertados += 1

    conn.commit()
    return insertados, 0

def insertar_notas_conceptos(registros, datos_generales):
    if not registros:
        return 0, 0
    uuid = registros[0].get("uuid", "")
    # comprobar existencia en tabla notas_credito
    cur.execute("SELECT 1 FROM notas_credito WHERE uuid = %s LIMIT 1", (uuid,))
    if cur.fetchone():
        log_write(f"⚠ UUID ya existe en tabla notas_credito -> {uuid} (se omiten todos sus conceptos)")
        return 0, len(registros)

    insertados = 0
    for r in registros:
        payload = {**datos_generales, **r}
        cur.execute("""
            INSERT INTO notas_credito (
                unidad_operativa, num_comprobacion, responsable_del_gasto, tipo_comprobacion, contrato,
                cfdi_relacionado_uuid, cfdi_relacionado_serie, cfdi_relacionado_folio,
                uuid, fecha, serie, folio, tipo_comprobante,
                rfc_emisor, nombre_emisor, rfc_receptor, nombre_receptor,
                claveprodserv, cantidad, claveunidad, descripcion,
                valorunitario, importe, descuento_concepto,
                iva_16, iva_8, iva_4, iva_0, iva_exento, iva_no_objeto,
                ieps_cuota, ieps_tasa, ieps_millar,
                ish_tasa, ish_importe,
                retencion_isr_10, retencion_isr_125, retencion_iva, retencion_ieps,
                subtotal_comprobante, total_comprobante, descuento_global, iva_total_comprobante
            ) VALUES (
                %(unidad_operativa)s, %(num_comprobacion)s, %(responsable_del_gasto)s, %(tipo_comprobacion)s, %(contrato)s,
                %(cfdi_relacionado_uuid)s, %(cfdi_relacionado_serie)s, %(cfdi_relacionado_folio)s,
                %(uuid)s, %(fecha)s, %(serie)s, %(folio)s, %(tipo_comprobante)s,
                %(rfc_emisor)s, %(nombre_emisor)s, %(rfc_receptor)s, %(nombre_receptor)s,
                %(claveprodserv)s, %(cantidad)s, %(claveunidad)s, %(descripcion)s,
                %(valorunitario)s, %(importe)s, %(descuento_concepto)s,
                %(iva_16)s, %(iva_8)s, %(iva_4)s, %(iva_0)s, %(iva_exento)s, %(iva_no_objeto)s,
                %(ieps_cuota)s, %(ieps_tasa)s, %(ieps_millar)s,
                %(ish_tasa)s, %(ish_importe)s,
                %(retencion_isr_10)s, %(retencion_isr_125)s, %(retencion_iva)s, %(retencion_ieps)s,
                %(subtotal_comprobante)s, %(total_comprobante)s, %(descuento_global)s, %(iva_total_comprobante)s
            );
        """, payload)
        insertados += 1

    conn.commit()
    return insertados, 0

# -------------------------
# Logging en UI
# -------------------------
def log_write(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    txt_log.configure(state="normal")
    txt_log.insert("end", f"[{ts}] {msg}\n")
    txt_log.see("end")
    txt_log.configure(state="disabled")
    root.update_idletasks()

# -------------------------
# Procesar archivo (UI)
# -------------------------
def procesar_archivo_ui():
    path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if not path:
        return

    unidad = cb_unidad.get().strip()
    numero = entry_comprobacion.get().strip()
    responsable = entry_responsable.get().strip()
    tipo_comp = cb_tipo.get().strip()
    contrato = entry_contrato.get().strip()

    if not unidad or not numero or not responsable:
        messagebox.showerror("Error", "Completa Unidad, Número de comprobación y Responsable.")
        return

    datos_generales = {
        "unidad_operativa": unidad,
        "num_comprobacion": numero,
        "responsable_del_gasto": responsable,
        "tipo_comprobacion": tipo_comp,
        "contrato": contrato
    }

    txt_log.configure(state="normal")
    txt_log.delete("1.0", "end")
    txt_log.configure(state="disabled")

    prog['maximum'] = 1
    prog['value'] = 0
    root.update_idletasks()

    tipo, registros, err = parsear_archivo_xml(path)
    if err:
        log_write(f"ERROR: {err}")
        return

    if tipo in ("P", "N"):
        log_write(f"Omitido (Tipo {tipo}): {os.path.basename(path)}")
        prog['value'] = 1
        return

    if tipo == "I":  # Factura
        ins, omit = insertar_facturas_conceptos(registros, datos_generales)
    elif tipo == "E":  # Nota de crédito
        ins, omit = insertar_notas_conceptos(registros, datos_generales)
    else:
        log_write(f"Tipo desconocido ({tipo}) -> omitido: {os.path.basename(path)}")
        prog['value'] = 1
        return

    prog['value'] = 1
    log_write(f"Archivo: {os.path.basename(path)} Insertados: {ins} Omitidos: {omit}")
    messagebox.showinfo("Finalizado", f"Insertados: {ins}\nOmitidos: {omit}")

# -------------------------
# Procesar carpeta (UI)
# -------------------------
def procesar_carpeta_ui():
    carpeta = filedialog.askdirectory()
    if not carpeta:
        return

    unidad = cb_unidad.get().strip()
    numero = entry_comprobacion.get().strip()
    responsable = entry_responsable.get().strip()
    tipo_comp = cb_tipo.get().strip()
    contrato = entry_contrato.get().strip()

    if not unidad or not numero or not responsable:
        messagebox.showerror("Error", "Completa Unidad, Número de comprobación y Responsable.")
        return

    archivos = [os.path.join(carpeta, f) for f in os.listdir(carpeta) if f.lower().endswith(".xml")]
    if not archivos:
        messagebox.showinfo("Info", "No se encontraron archivos XML.")
        return

    datos_generales = {
        "unidad_operativa": unidad,
        "num_comprobacion": numero,
        "responsable_del_gasto": responsable,
        "tipo_comprobacion": tipo_comp,
        "contrato": contrato
    }

    txt_log.configure(state="normal")
    txt_log.delete("1.0", "end")
    txt_log.configure(state="disabled")

    prog['maximum'] = len(archivos)
    prog['value'] = 0
    root.update_idletasks()

    tot_ins = 0
    tot_omit = 0

    for i, path in enumerate(archivos, start=1):
        tipo, registros, err = parsear_archivo_xml(path)
        if err:
            log_write(f"ERROR parseando {os.path.basename(path)} -> {err}")
            tot_omit += 1
            prog['value'] = i
            root.update_idletasks()
            continue

        if tipo in ("P", "N"):
            log_write(f"Omitido (Tipo {tipo}): {os.path.basename(path)}")
            tot_omit += 1
            prog['value'] = i
            root.update_idletasks()
            continue

        if tipo == "I":
            ins, omit = insertar_facturas_conceptos(registros, datos_generales)
        elif tipo == "E":
            ins, omit = insertar_notas_conceptos(registros, datos_generales)
        else:
            log_write(f"Tipo desconocido ({tipo}) -> {os.path.basename(path)}")
            ins = 0
            omit = 1

        tot_ins += ins
        tot_omit += omit
        log_write(f"{os.path.basename(path)} -> Insertados: {ins}, Omitidos: {omit}")
        prog['value'] = i
        root.update_idletasks()

    messagebox.showinfo("Finalizado", f"Insertados: {tot_ins}\nOmitidos: {tot_omit}")
    log_write(f"Proceso carpeta completado -> Insertados: {tot_ins}, Omitidos: {tot_omit}")

# -------------------------
# Tkinter UI
# -------------------------
root = tk.Tk()
root.title("CFDI Loader")
root.geometry("820x620")
root.resizable(True, True)

frm = ttk.Frame(root, padding=10)
frm.pack(fill="both", expand=True)

# Unidades y tipos (según tu petición)
UNIDADES = [
    "Unidad Operativa 1", "Unidad Operativa 2", "Unidad Operativa 3",
    "Unidad Operativa 4", "Unidad Operativa 5", "Unidad Operativa 6",
    "Unidad Operativa 7", "Unidad Operativa 8", "Unidad Operativa 9",
    "Unidad Operativa 10"
]
TIPOS = [
    "Fondo rotatorio", "Viaticos", "Gastos a comprobar",
    "Contratos", "Honorarios", "Por definir"
]

ttk.Label(frm, text="Unidad Operativa:").grid(row=0, column=0, sticky="w")
cb_unidad = ttk.Combobox(frm, values=UNIDADES, state="readonly", width=40)
cb_unidad.grid(row=0, column=1, sticky="ew", pady=4)

ttk.Label(frm, text="Número de Comprobación:").grid(row=1, column=0, sticky="w")
entry_comprobacion = ttk.Entry(frm, width=42)
entry_comprobacion.grid(row=1, column=1, sticky="ew", pady=4)

ttk.Label(frm, text="Responsable del gasto:").grid(row=2, column=0, sticky="w")
entry_responsable = ttk.Entry(frm, width=42)
entry_responsable.grid(row=2, column=1, sticky="ew", pady=4)

ttk.Label(frm, text="Tipo de comprobación:").grid(row=3, column=0, sticky="w")
cb_tipo = ttk.Combobox(frm, values=TIPOS, state="readonly", width=40)
cb_tipo.grid(row=3, column=1, sticky="ew", pady=4)

ttk.Label(frm, text="Contrato (opcional):").grid(row=4, column=0, sticky="w")
entry_contrato = ttk.Entry(frm, width=42)
entry_contrato.grid(row=4, column=1, sticky="ew", pady=4)

btn_frame = ttk.Frame(frm)
btn_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")
btn_frame.columnconfigure((0,1,2,3), weight=1)

ttk.Button(btn_frame, text="Seleccionar Archivo XML", command=procesar_archivo_ui).grid(row=0, column=0, padx=4)
ttk.Button(btn_frame, text="Seleccionar Carpeta XML", command=procesar_carpeta_ui).grid(row=0, column=1, padx=4)
ttk.Button(btn_frame, text="Limpiar Log", command=lambda: (txt_log.configure(state="normal"), txt_log.delete("1.0", "end"), txt_log.configure(state="disabled"))).grid(row=0, column=2, padx=4)
ttk.Button(btn_frame, text="Cerrar y Salir", command=lambda: (cur.close(), conn.close(), root.destroy())).grid(row=0, column=3, padx=4)

prog = ttk.Progressbar(frm, orient="horizontal", mode="determinate")
prog.grid(row=6, column=0, columnspan=2, sticky="ew", pady=8)

ttk.Label(frm, text="Registro:").grid(row=7, column=0, sticky="w")
txt_log = tk.Text(frm, height=20, state="disabled", wrap="word", bg="#f8f8f8")
txt_log.grid(row=8, column=0, columnspan=2, sticky="nsew", pady=6)

frm.rowconfigure(8, weight=1)
frm.columnconfigure(1, weight=1)

# Nota informativa
ttk.Label(frm, text="Nota: se insertan 'I' → facturas, 'E' → notas de crédito. 'P' y 'N' se omiten.").grid(row=9, column=0, columnspan=2, sticky="w", pady=6)

root.mainloop()
