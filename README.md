# Buscaminas en Python

Este repositorio contiene una implementación de dificultad media del clásico
juego **Buscaminas**, escrita en Python utilizando la biblioteca gráfica
integrada `tkinter`.  El juego presenta un tablero de 9×9 con 10 minas
colocadas al azar.  Haz clic izquierdo en una celda para descubrirla.  Si
descubres todas las celdas sin minas, ganas.  Si haces clic sobre una
mina, pierdes.  Puedes marcar celdas sospechosas con una bandera
haciendo clic derecho sobre ellas.

## Características

-   **Interfaz Gráfica Avanzada**: Interfaz amigable construida con `tkinter`, que incluye una barra de menú superior.
-   **Múltiples Niveles de Dificultad**:
    * **Fácil**: Tablero de 9x9 con 10 minas.
    * **Intermedio**: Tablero de 16x16 con 40 minas.
    * **Difícil**: Tablero de 22x22 con 99 minas.
-   **Temporizador**: Lleva un registro del tiempo transcurrido en cada partida.
-   **Contador de Minas**: Muestra cuántas minas quedan por encontrar (o banderas por colocar).
-   **Descubrimiento Automático**: Efecto "flood fill" para celdas adyacentes vacías.
-   **Manejo de Clic Derecho Mejorado**: Alterna entre bandera (🚩), signo de interrogación (❓) y celda vacía.
-   **Función de Chording**: Revela automáticamente las celdas circundantes si el número de banderas coincide con el número de minas vecinas.
-   **Ventana Redimensionable Dinámicamente**: La ventana se ajusta automáticamente al tamaño del tablero seleccionado.
-   **Posibilidad de Reiniciar**: Comienza una nueva partida en cualquier momento desde el menú o el botón de reinicio.
-   **Código Organizado**: Estructura en clases para facilitar su comprensión y extensión.

## Requisitos

- Python 3.8 o superior.
- `tkinter` (viene preinstalado con la mayoría de las distribuciones de Python).

## Instalación y uso

1. Clona este repositorio:
   ```bash
   git clone https://github.com/nicolasscolnik/minesweeper-python.git
   cd minesweeper-python
   ```
2. Ejecuta el juego desde tu terminal:
   ```bash
   python3 minesweeper.py
   ```

Al iniciarse el programa se mostrará una ventana con el tablero y un botón
“Reiniciar” para comenzar una nueva partida en cualquier momento.

## Licencia

Este proyecto está licenciado bajo los términos de la **Licencia MIT**.  Puedes
consultar el archivo [`LICENSE`](LICENSE) para más información.

## Autor

Desarrollado por **Nicolas Scolnik**.

Contacto:

- Correo electrónico: <nicolasscolnik@gmail.com>
- LinkedIn: [Nicolas Scolnik](https://www.linkedin.com/in/nicolas-scolnik-it/)
