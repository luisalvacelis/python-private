import pandas as pd
import glob

def ordenar_columnas(path):
    file_paths=glob.glob(path+"\*csv")
    list_columns = ["CALC_SISTEMA", "FLAG_RECLAMO_PRINCIPAL", "NUMERO_RECLAMO", "CASO_NUMERO",
                      "CALC_FECHA_RECLAMO", "CALC_FECHA_HORA_RECLAMO", "MONTO_RECLAMADO_CARGO",
                      "MONTO_RECLAMADO", "MOTIVO1", "MOTIVO3", "MEDIO_UTILIZADO_INFO",
                      "TELEFONO", "CLIENTE_KEY", "TIPO_DOCUMENTO_RECLAMANTE",
                      "NUMERO_DOCUMENTO_RECLAMANTE", "APELLIDOS_RECLAMANTE",
                      "NOMBRES_RECLAMANTE", "DIRECCION_PREFERIDA", "CALC_DEPARTAMENTO_INEI",
                      "CALC_PROVINCIA_INEI", "CALC_DISTRITO_INEI", "ID", "FECHA_CREACION_CASO",
                      "FECHA_ULTIMA_MODIFICACION", "MODIFICADO_POR", "MOTIVO_REAL",
                      "SUBTIPIFICACION", "ESTADO_RECLAMO", "RESULTADO_DEL_RECLAMO", "PAUTA1",
                      "PAUTA2", "ORDER_ID_1", "MONTO_TOTAL", "ESTADO_ACTUAL", "FLAG_APAGADO_URA",
                      "FLAG_ROBOT_LIQUIDACION", "FECHA_FIN_ROBOT", "RESOLUCION",
                      "FECHA_SOLICITUD_BAJA", "TIPO_RECLAMANTE", "FECHA_ORDEN", "TRANSACCION",
                      "ESTADO_TICKETDOIT", "ESTADO_ORDER_ID", "FECHA_DESCUENTO", "TIPO_DESCUENTO"]
    dfs=[]
    for file in file_paths:
        df=pd.read_csv(file)
        df=df[list_columns]
        dfs.append(df)
    merged_df = pd.concat(dfs)
    merged_df.to_csv(path+"\datos_ordenados.csv", index=False)