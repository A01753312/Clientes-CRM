#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificación Rápida del Sistema CRM
Este script realiza una verificación rápida para confirmar que el sistema está funcionando.

Uso: python verificar_crm.py
"""

import sys
from pathlib import Path
import pandas as pd

def verificar_sistema():
    """Verificación rápida del sistema CRM"""
    print("🔍 VERIFICACIÓN RÁPIDA DEL SISTEMA CRM")
    print("=" * 45)
    
    errores = 0
    
    # 1. Verificar archivo principal
    if Path("crm.py").exists():
        print("✅ Archivo crm.py encontrado")
    else:
        print("❌ Archivo crm.py NO encontrado")
        errores += 1
    
    # 2. Verificar estructura de datos
    data_dir = Path("data")
    if data_dir.exists():
        print("✅ Directorio data existe")
        
        # Verificar clientes.csv
        clientes_csv = data_dir / "clientes.csv"
        if clientes_csv.exists():
            try:
                df = pd.read_csv(clientes_csv, dtype=str)
                print(f"✅ clientes.csv válido: {len(df)} registros")
            except Exception as e:
                print(f"❌ Error en clientes.csv: {e}")
                errores += 1
        else:
            print("ℹ️ clientes.csv no existe (se creará automáticamente)")
        
        # Verificar directorio docs
        docs_dir = data_dir / "docs"
        if docs_dir.exists():
            print("✅ Directorio docs existe")
        else:
            print("ℹ️ Directorio docs no existe (se creará automáticamente)")
    else:
        print("❌ Directorio data NO existe")
        errores += 1
    
    # 3. Verificar compilación
    try:
        import py_compile
        py_compile.compile("crm.py", doraise=True)
        print("✅ Código compila sin errores")
    except Exception as e:
        print(f"❌ Error de compilación: {e}")
        errores += 1
    
    # 4. Verificar dependencias básicas
    try:
        import pandas
        print("✅ Pandas disponible")
    except ImportError:
        print("❌ Pandas NO disponible")
        errores += 1
    
    try:
        import streamlit
        print("✅ Streamlit disponible")
    except ImportError:
        print("❌ Streamlit NO disponible")
        errores += 1
    
    # Resultado final
    print("\n" + "=" * 45)
    if errores == 0:
        print("🎉 SISTEMA OK - Listo para usar")
        print("▶️ Ejecuta: streamlit run crm.py")
        return True
    else:
        print(f"⚠️ {errores} problema(s) encontrado(s)")
        print("🔧 Corrige los errores antes de usar el sistema")
        return False

if __name__ == "__main__":
    resultado = verificar_sistema()
    sys.exit(0 if resultado else 1)