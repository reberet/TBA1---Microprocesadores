# Ejercicio 04
Estudiantes: Beretta, Renzo. Chiappini, Lucas. Silva, Ignacio.  
Universidad Católica  
Asignatura: Microprocesadores  
Docente: Jhonatan Piuma  
Fecha: 24 de octubre de 2025

---

## 📋 Descripción del Proyecto

Sistema de monitoreo en tiempo real para datacenters desarrollado con Python y Tkinter. El sistema recibe datos de sensores vía UDP, los procesa y los visualiza en una interfaz gráfica intuitiva con sistema de alarmas configurable.

---

## 🎯 Objetivos

- Implementar un servidor UDP que reciba datos de sensores en formato JSON
- Desarrollar una interfaz gráfica para visualización en tiempo real
- Crear un sistema de alarmas con umbrales configurables
- Registrar historial de eventos y alarmas
- Permitir monitoreo simultáneo de múltiples parámetros

---

## 🏗️ Arquitectura del Sistema

### Backend (Servidor UDP)
- **Puerto**: 5005
- **Protocolo**: UDP
- **Formato de datos**: JSON
- **Función**: Recibe datos de sensores y actualiza `datos.json` en tiempo real

### Frontend (Interfaz Gráfica)
- **Framework**: Tkinter (Python)
- **Actualización**: Cada 2 segundos
- **Navegación**: 6 secciones principales
- **Función**: Visualiza datos y gestiona alarmas

---

## 📡 Formato de Datos

El sistema recibe datos en formato JSON con la siguiente estructura:
```json
