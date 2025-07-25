# Buscaminas en Python

Este repositorio contiene una implementación de dificultad media del clásico
juego **Buscaminas**, escrita en Python utilizando la biblioteca gráfica
integrada `tkinter`.  El juego presenta un tablero de 9×9 con 10 minas
colocadas al azar.  Haz clic izquierdo en una celda para descubrirla.  Si
descubres todas las celdas sin minas, ganas.  Si haces clic sobre una
mina, pierdes.  Puedes marcar celdas sospechosas con una bandera
haciendo clic derecho sobre ellas.

## Características

- Interfaz gráfica amigable construida con `tkinter`.
- Tablero de 9×9 con 10 minas aleatorias.
- Descubrimiento automático de celdas adyacentes vacías (efecto “flood”).
- Posibilidad de reiniciar la partida sin salir del programa.
- Código organizado en clases para facilitar su comprensión y extensión.

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
