# Guía de instalación

1) Crear un entorno virtual. 
*NOTA:* Estamos usando la versión 3.5.* de __Python__ y la versión 1.11.* de __Django__.
2) Instalar django y pillow:
    * pip install django
    * pip install pillow
3) Para dejar corriendo las tareas diarias (como las *daily coins*) usamos __cron__:
    * Installar cron (en Ubuntu-Fedora ya viene instalado)
    * Ahora vamos a configurar la/s task/s:
        >$ crontab -e
    
        Esto nos abrirá un editor de texto donde debemos configurar el tiempo y el path a nuestro script.
        > __* * * * *__ /path/entorno/virtual/bin/python /path/directorio/proyecto/manage.py add_coins
        
        Los 5 asteriscos:
        De izquierda a derecha, los asteriscos representan:
        1.Minutos: de 0 a 59.
        2.Horas: de 0 a 23.
        3.Día del mes: de 1 a 31.
        4.Mes: de 1 a 12.
        5.Día de la semana: de 0 a 6, siendo 0 el domingo.
        
    * En caso de que el demonio no este activado:
        >$ systemctl start cronie
        >$ systemctl start cronie.service
    

[Documentación crontab](https://geekytheory.com/programar-tareas-en-linux-usando-crontab)

4) Ejecutar el siguiente comando, para crear las tablas en la BD:
    >$ python manage.py migrate

5) Ejecutar el siguiente comando, para poblar la tabla Difficulty:
    >$ python manage.py populate

6) Correr el server:
    >$ python manage.py runserver
