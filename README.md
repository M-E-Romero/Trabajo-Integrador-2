# API Carrito de Compras

###  Arquitectura elegida
Arquitectura cliente-servidor

![Arquitectura cliente-servidor](./static/img/SPA.png)

---

### Tecnologías utilizadas
- **Python + Flask** → servidor web y API REST  
- **SQLite** → base de datos ligera y embebida  
- **HTML5 + CSS3** → estructura y estilos de la interfaz  
- **JavaScript (ES6)** → lógica de interacción (botones +, -, vaciar, filtros)  
- **Cypress** → pruebas end-to-end para validar el flujo de compra y el carrito  

---

### Dificultades encontradas y cómo se resolvieron
- **Sincronización frontend-backend en pruebas**  
  - Problema: Cypress leía el DOM antes de que el `fetch("/carrito/total")` terminara.  
  - Solución: se usó `cy.intercept` y `cy.wait` para esperar explícitamente la respuesta del backend antes de validar.  

- **Acceso a la base de datos SQLite**  
  - Problema: no se puede inspeccionar la base directamente , se debe  descarga SQLite en https://www.sqlite.org/download.html (sqlite.org in Bing); O crear un archivo para conectarse a la base desde la terminal.

- **Problemas con la versión de Python e intérprete**  
  - Problema: la versión 3.13 presentaba errores al activar entornos virtuales (`venv`) y generaba incompatibilidades.  
  - Solución: se actualizó a la versión estable más reciente (3.14), lo que resolvió los problemas de activación y garantizó compatibilidad con Flask y las librerías utilizadas.  
