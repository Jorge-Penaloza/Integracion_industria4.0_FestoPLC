# Integración Industria 4.0 con PLC Festo

Este proyecto representa una solución integral para la comunicación y control de un PLC Festo utilizando Codesys. Se apoya en KepServer como servidor OPC UA para facilitar la comunicación. Una de las características destacadas es la implementación de un cliente en Python que, mediante visión artificial, detecta marcadores ArUCO. Estos marcadores son interpretados como sensores de posición en una maqueta física.

## Estructura del Repositorio

- **mesh**: Contiene archivos relacionados con la representación gráfica de la maqueta y los elementos que interactúan con ella.
- **prueba2**: Directorio con archivos de prueba.
- **interfaz_vmicrosoft.py**: Script de Python que representa la interfaz principal del sistema.
- **opc_cliente.py**: Cliente en Python que se comunica con el servidor OPC UA.
- **pruebas_ogre_marcadores.py**: Script de Python para pruebas con marcadores ArUCO y la biblioteca Ogre.
- **sensores.xlsx**: Archivo Excel con información sobre los sensores utilizados en el proyecto.
- **temporal_distancia tiempo.py**: Script de Python para calcular distancias temporales.

## Características Principales

- **Detección de Marcadores ArUCO**: A través de visión artificial, el sistema detecta marcadores ArUCO para determinar posiciones en una maqueta física.
- **Realidad Aumentada**: Según la proximidad de los sensores, el sistema superpone imágenes de realidad aumentada en correas transportadoras, proporcionando una visualización interactiva y dinámica de la maqueta.
- **Comunicación con PLC Festo**: El sistema establece una comunicación eficiente con un PLC Festo a través de Codesys y KepServer.


## Créditos

Este proyecto fue liderado y desarrollado por Jorge Peñaloza como programador principal. Contó con el valioso apoyo y colaboración de Ana Javiera Valdés y Catalina Lazo.


