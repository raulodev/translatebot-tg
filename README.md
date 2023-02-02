# translatebot-tg

## Tabla de Contenidos

- [Sobre](#about)
- [Comenzando](#getting_started)
- [Uso](#usage)

## Sobre <a name = "about"></a>

Esto es un bot de telegram lanzado hace ya casi 2 años para traducir mensajes a diferentes idiomas en grupos y en el chat privado con el bot, contruido con python y que actualmente cuenta con alrededor de 3000 usuarios a día de hoy y que a pesar de que telegram ya posee las traducciones incluidas en su aplicación las cifras de usuarios  de este bot siguen creciendo.

## Comenzando <a name = "getting_started"></a>

Estas son las intrucciones a seguir para copiar el proyecto y correrlo localmente para fines de desarrollo o de pruebas.

### Prerrequisitos

Python (3.8.10)

git (2.25.1)


### Clonar Repositorio



```console
git clone git@github.com:raulodev/translatebot-tg.git
```

Acceder a la carpeta del proyecto , crear entorno virtual e instalar dependencias.

```console
$ cd translatebot-tg/
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip3 install -r requirements.txt
```

Y para terminar cargar las variables de entorno

`TOKEN` : token del bot ([obtener](https://t.me/BotFather))

`API_ID` : api id de tu app  ([obtener](https://my.telegram.org/apps))

`API_HASH` : api hash de tu app  ([obtener](https://t.me/iDGetInfoBot))

`OWNER` : tu id de usuario en telegram ([obtener](https://my.telegram.org/apps))

`DATABASE_URL` : ejemplo `sqlite:///database.sqlite`

## Uso <a name = "usage"></a>

Una vez terminado con todo el proceso de instalación correr el bot usando :
```console
$ python3 main.py
```
