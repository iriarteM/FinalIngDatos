from conexion import conectar_bd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import random
import ctypes
import string

user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)


def center_window(window, width, height):
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


def ejecutar_query(conexion, query, parametros=None):
    cursor = conexion.cursor()
    if parametros is None:
        cursor.execute(query)
    else:
        cursor.execute(query, parametros)
    resultados = cursor.fetchall()
    cursor.close()
    return resultados


def cerrar_bd(conexion):
    if conexion is not None:
        conexion.close()


def iniciar_sesion():
    ventana_inicio.withdraw()
    ventana_sesion = tk.Tk()
    ventana_sesion.title("Iniciar Sesión")
    center_window(ventana_sesion, 300, 280)
    ventana_sesion.configure(bg="white")

    label_login = tk.Label(ventana_sesion, text="Login", font=("Arial", 16, "bold"))
    label_login.pack(pady=10)

    def regresar_a_inicio():
        ventana_sesion.destroy()
        mostrar_ventana_inicio()

    def verificar_sesion():
        username = entry_username.get()
        dni = entry_dni.get()
        consulta = """SELECT DNI_AF FROM AFILIADOS 
            WHERE USER_AF = :username"""
        parametros = {"username": username}
        result = ejecutar_query(conectar_bd(), consulta, parametros)

        if result is not None and str(result[0][0]) == dni:
            ventana_sesion.destroy()
            ventana_main(username)
        else:
            messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")

        cerrar_bd(conectar_bd())

    label_username = tk.Label(ventana_sesion, text="Usuario:")
    label_username.pack(pady=10)
    entry_username = tk.Entry(ventana_sesion)
    entry_username.pack()

    label_dni = tk.Label(ventana_sesion, text="Clave Nro DNI:")
    label_dni.pack(pady=10)
    entry_dni = tk.Entry(ventana_sesion, show="*")
    entry_dni.pack()

    button_login = tk.Button(
        ventana_sesion, text="Iniciar sesión", command=verificar_sesion
    )
    button_login.pack(pady=20)

    button_regresar = tk.Button(
        ventana_sesion, text="Regresar a Inicio", command=regresar_a_inicio
    )
    button_regresar.pack()

    ventana_sesion.mainloop()


def ventana_main(username):
    ventana_main = tk.Tk()
    ventana_main.title("Ventana main")
    center_window(ventana_main, 900, 720)
    ventana_main.configure(bg="white")

    def regresar_a_inicio():
        ventana_main.destroy()
        mostrar_ventana_inicio()

    def confirmar_eliminar_familiar():
        seleccion = listbox_familiares.curselection()
        if len(seleccion) == 0:
            messagebox.showwarning(
                "Sin selección", "No se ha seleccionado ningun familiar"
            )
            return
        respuesta = messagebox.askyesno(
            "Confirmar Eliminación", "Vas a eliminar un familiar. ¿Deseas continuar?"
        )
        if respuesta:
            eliminar_familiar_seleccionado(seleccion)

    def eliminar_familiar_seleccionado(seleccion):
        familiar_seleccionado = listbox_familiares.get(seleccion)

        split = str(familiar_seleccionado.split(":")[1].strip())
        dni_fam = str(split.split("|")[0].strip())

        conexion = conectar_bd()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute(
                    "call ELIMINAR_FAMILIAR(:dni_fam ,:username)", (dni_fam, username)
                )
                conexion.commit()
                cursor.close()
                cerrar_bd(conexion)

                listbox_familiares.delete(seleccion)

            except Exception as ex:
                cerrar_bd(conexion)
                messagebox.showerror("Error", "Error al eliminar familiar: " + str(ex))

    def editar_familiar_seleccionado():
        seleccion = listbox_familiares.curselection()
        if len(seleccion) == 0:
            messagebox.showwarning(
                "Sin selección", "No se ha seleccionado ningun familiar"
            )
            return

        familiar_seleccionado = listbox_familiares.get(seleccion)

        split = str(familiar_seleccionado.split(":")[1].strip())
        dni_fam = str(split.split("|")[0].strip())

        ventana_editar = tk.Tk()
        ventana_editar.title("Editar familiar")
        center_window(ventana_editar, 300, 200)

        def guardar_cambios():
            nombre = entry_nombres.get()
            parentesco = combobox_parentesco.get()
            direccion = entry_direccion.get()

            conexion = conectar_bd()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    cursor.execute(
                        "call ACTUALIZAR_FAMILIAR(:username, :dni_fam, :nombre, :parentesco, :direccion)",
                        (username, dni_fam, nombre, parentesco, direccion),
                    )
                    conexion.commit()
                    cursor.close()
                    cerrar_bd(conexion)
                    messagebox.showinfo(
                        "Familiar modificado",
                        "El familiar ha sido modificado con éxito.",
                    )
                    actualizar()

                except Exception as ex:
                    cerrar_bd(conexion)
                    messagebox.showerror(
                        "Error", "Error al modificar datos: " + str(ex)
                    )

            ventana_editar.destroy()

        label_nombres = tk.Label(ventana_editar, text="Nombres y Apellidos:")
        label_nombres.pack()
        entry_nombres = tk.Entry(ventana_editar)
        entry_nombres.pack()

        label_parentesco = tk.Label(ventana_editar, text="Parentesco:")
        label_parentesco.pack()
        opciones_familiar = ["Madre", "Padre", "Hermano/a", "Hijo/a"]
        selected_parentesco = tk.StringVar(ventana_editar)
        selected_parentesco.set(opciones_familiar[0])
        combobox_parentesco = ttk.Combobox(
            ventana_editar,
            textvariable=selected_parentesco,
            values=opciones_familiar,
            state="readonly",
        )
        combobox_parentesco.pack()

        label_direccion = tk.Label(ventana_editar, text="Dirección: ")
        label_direccion.pack()
        entry_direccion = tk.Entry(ventana_editar)
        entry_direccion.pack()

        button_guardar = tk.Button(
            ventana_editar, text="Guardar cambios", command=guardar_cambios
        )
        button_guardar.pack(pady=10)

        ventana_editar.mainloop()

    def registrar_familiar():
        ventana_registro = tk.Tk()
        ventana_registro.title("Registrar familiar")
        center_window(ventana_registro, 300, 230)

        def insertar_datos():
            dni = entry_dni.get()
            nombre = entry_nombres.get()
            parentesco = combobox_parentesco.get()
            direccion = entry_direccion.get()

            conexion = conectar_bd()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    cursor.execute(
                        "call INSERTAR_FAMILIAR(:username, :dni, :nombre, :parentesco, :direccion)",
                        (username, dni, nombre, parentesco, direccion),
                    )
                    conexion.commit()
                    cursor.close()
                    cerrar_bd(conexion)
                    messagebox.showinfo(
                        "Registro exitoso", "¡Familiar registrado con éxito!"
                    )
                    actualizar()

                except Exception as ex:
                    cerrar_bd(conexion)
                    messagebox.showerror("Error", "Error al insertar datos: " + str(ex))

            ventana_registro.destroy()

        label_dni = tk.Label(ventana_registro, text="DNI:")
        label_dni.pack()
        entry_dni = tk.Entry(ventana_registro)
        entry_dni.pack()

        label_nombres = tk.Label(ventana_registro, text="Nombres y Apellidos:")
        label_nombres.pack()
        entry_nombres = tk.Entry(ventana_registro)
        entry_nombres.pack()

        label_parentesco = tk.Label(ventana_registro, text="Parentesco:")
        label_parentesco.pack()
        opciones_familiar = ["Madre", "Padre", "Hermano/a", "Hijo/a"]
        selected_parentesco = tk.StringVar(ventana_registro)
        selected_parentesco.set(opciones_familiar[0])
        combobox_parentesco = ttk.Combobox(
            ventana_registro,
            textvariable=selected_parentesco,
            values=opciones_familiar,
            state="readonly",
        )
        combobox_parentesco.pack()

        label_direccion = tk.Label(ventana_registro, text="Dirección: ")
        label_direccion.pack()
        entry_direccion = tk.Entry(ventana_registro)
        entry_direccion.pack()

        button_registrar = tk.Button(
            ventana_registro, text="Registrar familiar", command=insertar_datos
        )
        button_registrar.pack(pady=20)

    def confirmar_eliminar_query():
        seleccion = listbox_querys.curselection()
        if len(seleccion) == 0:
            messagebox.showwarning(
                "Sin selección", "No se ha seleccionado ninguna consulta"
            )
            return
        respuesta = messagebox.askyesno(
            "Confirmar Eliminación", "Vas a eliminar una consulta. ¿Deseas continuar?"
        )
        if respuesta:
            eliminar_query_seleccionada(seleccion)

    def eliminar_query_seleccionada(seleccion):
        query_seleccionada = listbox_querys.get(seleccion)

        split = str(query_seleccionada.split(":")[2].strip())
        num_consulta = str(split.split("|")[0].strip())

        conexion = conectar_bd()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute(
                    "call ELIMINAR_CONSULTA(:num_consulta, :username)",
                    (num_consulta, username),
                )
                conexion.commit()
                cursor.close()
                cerrar_bd(conexion)

                listbox_querys.delete(seleccion)

            except Exception as ex:
                cerrar_bd(conexion)
                messagebox.showerror(
                    "Error", "Error al eliminar la consulta: " + str(ex)
                )

    def editar_query_seleccionada():
        seleccion = listbox_querys.curselection()
        if len(seleccion) == 0:
            messagebox.showwarning(
                "Sin selección", "No se ha seleccionado ninguna consulta"
            )
            return

        query_seleccionada = listbox_querys.get(seleccion)

        split = str(query_seleccionada.split(":")[2].strip())
        num_consulta = str(split.split("|")[0].strip())

        ventana_editar = tk.Tk()
        ventana_editar.title("Editar consulta")
        center_window(ventana_editar, 400, 200)

        def generar_user_emp():
            consulta = """SELECT USER_EMP
                ,NOMBRE_EMP 
                FROM EMPLEADOS"""
            users_emp = ejecutar_query(conectar_bd(), consulta)
            cerrar_bd(conectar_bd())
            for user in users_emp:
                if combobox_empleado.get() == user[1]:
                    return user[0]

        def obtener_fecha():
            fecha_seleccionada = entry_fecha.get_date()
            entry_fecha.config(state=tk.NORMAL)
            entry_fecha.delete(0, tk.END)
            entry_fecha.insert(tk.END, fecha_seleccionada)
            entry_fecha.config(state=tk.DISABLED)

        def guardar_cambios():
            tipo = combobox_tipo.get()
            fecha = entry_fecha.get()
            empleado = generar_user_emp()

            conexion = conectar_bd()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    cursor.execute(
                        "call ACTUALIZAR_CONSULTA(:num_consulta, :tipo, :fecha, :empleado, :username)",
                        (num_consulta, tipo, fecha, empleado, username),
                    )
                    conexion.commit()
                    cursor.close()
                    cerrar_bd(conexion)
                    messagebox.showinfo(
                        "Consulta modificada",
                        "La consulta ha sido modificada con éxito.",
                    )
                    actualizar()

                except Exception as ex:
                    cerrar_bd(conexion)
                    messagebox.showerror(
                        "Error", "Error al modificar datos: " + str(ex)
                    )

            ventana_editar.destroy()

        label_tipo = tk.Label(ventana_editar, text="   Tipo:")
        label_tipo.pack()
        opciones_tipo = ["Finanzas", "Cuentas", "Contratos", "Otros"]
        selected_tipo = tk.StringVar(ventana_editar)
        selected_tipo.set(opciones_tipo[0])
        combobox_tipo = ttk.Combobox(
            ventana_editar,
            textvariable=selected_tipo,
            values=opciones_tipo,
            state="readonly",
        )
        combobox_tipo.pack()

        label_empleado = tk.Label(ventana_editar, text="   Asesores disponibles:")
        label_empleado.pack()
        consulta = """SELECT 
            USER_EMP
            ,NOMBRE_EMP 
            FROM EMPLEADOS"""
        nombres_emp = ejecutar_query(conectar_bd(), consulta)
        cerrar_bd(conectar_bd())
        opciones_empleado = [nombre[1] for nombre in nombres_emp]
        selected_empleado = tk.StringVar(ventana_editar)
        selected_empleado.set(opciones_empleado[0])
        combobox_empleado = ttk.Combobox(
            ventana_editar,
            textvariable=selected_empleado,
            values=opciones_empleado,
            state="readonly",
        )
        combobox_empleado.pack()

        label_fecha = tk.Label(ventana_editar, text="   Seleccionar fecha:")
        label_fecha.pack()

        entry_fecha = DateEntry(ventana_editar, date_pattern="dd-mm-yyyy")
        entry_fecha.pack()
        entry_fecha.bind("<<DateEntrySelected>>", obtener_fecha)

        button_guardar = tk.Button(
            ventana_editar, text="Guardar cambios", command=guardar_cambios
        )
        button_guardar.pack(pady=10)

        ventana_editar.mainloop()

    def agregar_query():
        ventana_agregar = tk.Tk()
        ventana_agregar.title("Generar Consulta")
        center_window(ventana_agregar, 400, 300)

        def generar_id():
            numeros_random = "".join(random.choices(string.digits, k=3))
            id = "C" + numeros_random

            entry_id.config(state=tk.NORMAL)
            entry_id.delete(0, tk.END)
            entry_id.insert(tk.END, str(id))
            entry_id.config(state=tk.DISABLED)

        def generar_num():
            consulta = """SELECT COUNT(*) FROM CONSULTORIAS 
                WHERE AFILIADOS_USER_AF = :username"""
            parametros = {"username": username}
            conexion = conectar_bd()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    cursor.execute(consulta, parametros)
                    results = cursor.fetchall()
                    cursor.close()
                except Exception as ex:
                    print("Error al ejecutar la consulta:", ex)

            if results is not None:
                num = int(results[0][0]) + 1
            else:
                messagebox.showerror(
                    "Error", "Nombre de usuario o contraseña incorrectos."
                )

            entry_num.config(state=tk.NORMAL)
            entry_num.delete(0, tk.END)
            entry_num.insert(tk.END, str(num))
            entry_num.config(state=tk.DISABLED)

        def generar_user_emp():
            consulta = """SELECT 
                USER_EMP
                ,NOMBRE_EMP 
                FROM EMPLEADOS"""
            users_emp = ejecutar_query(conectar_bd(), consulta)
            cerrar_bd(conectar_bd())
            for user in users_emp:
                if combobox_empleado.get() == user[1]:
                    return user[0]

        def obtener_fecha():
            fecha_seleccionada = entry_fecha.get_date()
            entry_fecha.config(state=tk.NORMAL)
            entry_fecha.delete(0, tk.END)
            entry_fecha.insert(tk.END, fecha_seleccionada)
            entry_fecha.config(state=tk.DISABLED)

        def guardar_query():
            id = entry_id.get()
            num = str(entry_num.get())
            tipo = combobox_tipo.get()
            estado = "Pendiente"
            fecha = entry_fecha.get()
            empleado = generar_user_emp()

            conexion = conectar_bd()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    cursor.execute(
                        "call INSERTAR_CONSULTA(:id, :num, :tipo, :estado, :fecha, :empleado, :username)",
                        (id, num, tipo, estado, fecha, empleado, username),
                    )
                    conexion.commit()
                    cursor.close()
                    cerrar_bd(conexion)
                    messagebox.showinfo(
                        "Consulta agregada", "La consulta ha sido agregada con éxito."
                    )
                    actualizar()

                except Exception as ex:
                    cerrar_bd(conexion)
                    messagebox.showerror("Error", "Error al insertar datos: " + str(ex))

            ventana_agregar.destroy()

        label_tipo = tk.Label(ventana_agregar, text="Tipo: ")
        label_tipo.pack()
        opciones_tipo = ["Finanzas", "Cuentas", "Contratos", "Otros"]
        selected_tipo = tk.StringVar(ventana_agregar)
        selected_tipo.set(opciones_tipo[0])
        combobox_tipo = ttk.Combobox(
            ventana_agregar,
            textvariable=selected_tipo,
            values=opciones_tipo,
            state="readonly",
        )
        combobox_tipo.pack()

        label_id = tk.Label(ventana_agregar, text="ID: ")
        label_id.pack()
        entry_id = tk.Entry(ventana_agregar, state=tk.DISABLED)
        entry_id.pack()
        generar_id()

        label_num = tk.Label(ventana_agregar, text="Número: ")
        label_num.pack()
        entry_num = tk.Entry(ventana_agregar, state=tk.DISABLED)
        entry_num.pack()
        generar_num()

        label_empleado = tk.Label(ventana_agregar, text="Asesores disponibles: ")
        label_empleado.pack()
        consulta = """SELECT 
            USER_EMP
            ,NOMBRE_EMP 
            FROM EMPLEADOS"""
        nombres_emp = ejecutar_query(conectar_bd(), consulta)
        cerrar_bd(conectar_bd())
        opciones_empleado = [nombre[1] for nombre in nombres_emp]
        selected_empleado = tk.StringVar(ventana_agregar)
        selected_empleado.set(opciones_empleado[0])
        combobox_empleado = ttk.Combobox(
            ventana_agregar,
            textvariable=selected_empleado,
            values=opciones_empleado,
            state="readonly",
        )
        combobox_empleado.pack()

        label_fecha = tk.Label(ventana_agregar, text="Seleccionar fecha: ")
        label_fecha.pack()

        entry_fecha = DateEntry(ventana_agregar, date_pattern="dd-mm-yyyy")
        entry_fecha.pack()
        entry_fecha.bind("<<DateEntrySelected>>", obtener_fecha)

        button_guardar = tk.Button(
            ventana_agregar, text="Generar consulta", command=guardar_query
        )
        button_guardar.pack(pady=10)

        ventana_agregar.mainloop()

    def actualizar():
        listbox_querys.delete(0, tk.END)
        listbox_familiares.delete(0, tk.END)

        consulta = """SELECT 
            C.ID_CONSUL "ID"
            ,C.NUM_CONSUL "NUMERO"
            ,C.TIPO_CONSUL "TIPO"
            ,C.ESTADO_CONSUL "ESTADO"
            ,C.FECHA_CONSUL "FECHA"
            ,E.NOMBRE_EMP "ASESOR"
            FROM CONSULTORIAS C 
            JOIN EMPLEADOS E ON E.USER_EMP = C.EMPLEADOS_USER_EMP 
            WHERE C.AFILIADOS_USER_AF = :username 
            ORDER BY NUMERO ASC"""

        parametros = {"username": username}
        conexion = conectar_bd()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute(consulta, parametros)
                results = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
                cursor.close()

                for row in results:
                    formatted_row = " | ".join(
                        f"{column_names[i]}: {row[i]}" for i in range(len(column_names))
                    )
                    listbox_querys.insert(tk.END, formatted_row)

            except Exception as ex:
                print("Error al ejecutar la consulta:", ex)

        consulta = """SELECT 
            F.DNI_FAM "DNI FAMILIAR"
            ,F.NOMBRE_FAM "NOMBRE FAMILIAR"
            ,F.PARENTESCO "PARENTESCO"
            ,F.DIREC_FAM "DIRECCIÓN"
            FROM FAMILIARES F
            JOIN AFILIADOS A ON A.USER_AF = F.AFILIADOS_USER_AF
            WHERE F.AFILIADOS_USER_AF = :username"""

        parametros = {"username": username}
        conexion = conectar_bd()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute(consulta, parametros)
                results = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
                cursor.close()

                for row in results:
                    formatted_row = " | ".join(
                        f"{column_names[i]}: {row[i]}" for i in range(len(column_names))
                    )
                    listbox_familiares.insert(tk.END, formatted_row)

            except Exception as ex:
                print("Error al ejecutar familiares:", ex)

    def confirmar_cerrar_sesion():
        respuesta = messagebox.askyesno(
            "Confirmar Cierre de Sesión", "Vas a cerrar sesión. ¿Deseas continuar?"
        )
        if respuesta:
            regresar_a_inicio()

    consulta = """SELECT NOMBRE_AF FROM AFILIADOS 
        WHERE USER_AF = :username"""
    parametros = {"username": username}
    result = ejecutar_query(conectar_bd(), consulta, parametros)

    label_bienvenida = tk.Label(
        ventana_main, text=f"Bienvenido {result[0][0]}!", font=("Arial", 14, "bold")
    )
    label_bienvenida.pack(pady=10)

    label_titulo = tk.Label(
        ventana_main, text=f"Mis consultas: ", font=("Arial", 10, "bold")
    )
    label_titulo.pack(pady=10)

    scrollbar = tk.Scrollbar(ventana_main)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox_querys = tk.Listbox(
        ventana_main, yscrollcommand=scrollbar.set, width=105, height=10
    )
    listbox_querys.pack(side=tk.TOP, padx=100, pady=10)

    listbox_botones = tk.Listbox(
        ventana_main, yscrollcommand=scrollbar.set, width=105, height=10
    )
    listbox_botones.pack(side=tk.TOP, padx=100, pady=20)
    listbox_botones.configure(borderwidth=-1)

    label_titulo1 = tk.Label(
        ventana_main, text=f"Mis familiares: ", font=("Arial", 10, "bold")
    )
    label_titulo1.pack(pady=10)

    listbox_familiares = tk.Listbox(
        ventana_main, yscrollcommand=scrollbar.set, width=105, height=10
    )
    listbox_familiares.pack(side=tk.TOP, padx=100, pady=10)

    listbox_botones1 = tk.Listbox(
        ventana_main, yscrollcommand=scrollbar.set, width=105, height=10
    )
    listbox_botones1.pack(side=tk.TOP, padx=100, pady=10)
    listbox_botones1.configure(borderwidth=-1)

    listbox_botones2 = tk.Listbox(
        ventana_main, yscrollcommand=scrollbar.set, width=105, height=10
    )
    listbox_botones2.pack(side=tk.TOP, padx=100, pady=10)
    listbox_botones2.configure(borderwidth=-1)

    actualizar()

    scrollbar.config(command=listbox_querys.yview)

    frame_botones = tk.Frame(listbox_botones, bg="white")
    frame_botones.pack()

    frame_botones1 = tk.Frame(listbox_botones1, bg="white")
    frame_botones1.pack()

    frame_botones2 = tk.Frame(listbox_botones2, bg="gray")
    frame_botones2.pack()

    button_agregar = tk.Button(
        frame_botones, text="Generar nueva consulta", command=agregar_query
    )
    button_agregar.pack(side=tk.LEFT, padx=10)

    button_update = tk.Button(
        frame_botones, text="Editar consulta", command=editar_query_seleccionada
    )
    button_update.pack(side=tk.LEFT, padx=10)

    button_delete = tk.Button(
        frame_botones, text="Eliminar consulta", command=confirmar_eliminar_query
    )
    button_delete.pack(side=tk.LEFT, padx=10)

    button_registrar_familiar = tk.Button(
        frame_botones1, text="Registrar familiar", command=registrar_familiar
    )
    button_registrar_familiar.pack(side=tk.LEFT, padx=10)

    button_editar_familiar = tk.Button(
        frame_botones1, text="Editar familiar", command=editar_familiar_seleccionado
    )
    button_editar_familiar.pack(side=tk.LEFT, padx=10)

    button_eliminar_familiar = tk.Button(
        frame_botones1, text="Eliminar familiar", command=confirmar_eliminar_familiar
    )
    button_eliminar_familiar.pack(side=tk.LEFT, padx=10)

    button_actualizar = tk.Button(
        frame_botones2, text="Actualizar datos", command=actualizar
    )
    button_actualizar.pack(side=tk.LEFT, padx=5, pady=5)

    button_regresar = tk.Button(
        frame_botones2, text="Cerrar sesión", command=confirmar_cerrar_sesion
    )
    button_regresar.pack(side=tk.LEFT, padx=5, pady=5)

    ventana_main.mainloop()


def registrarse():
    ventana_inicio.withdraw()
    ventana_registro = tk.Tk()
    ventana_registro.title("Registrarse")
    center_window(ventana_registro, 400, 460)

    def regresar_a_inicio():
        ventana_registro.destroy()
        mostrar_ventana_inicio()

    def generar_username():
        institucion_elegida = combobox_institucion.get()
        numeros_random = "".join(random.choices(string.digits, k=3))

        if institucion_elegida == "Ejército":
            username = "EJ" + numeros_random
        elif institucion_elegida == "Marina":
            username = "MA" + numeros_random
        elif institucion_elegida == "Fuerza Aérea":
            username = "FA" + numeros_random
        else:
            username = "PL" + numeros_random

        entry_username.config(state=tk.NORMAL)
        entry_username.delete(0, tk.END)
        entry_username.insert(tk.END, str(username))
        entry_username.config(state=tk.DISABLED)

    def insertar_datos():
        username = entry_username.get()
        dni = entry_dni.get()
        nombre = entry_nombres.get()
        institution = combobox_institucion.get()
        salario = entry_salario.get()
        direccion = entry_direccion.get()
        correo = entry_correo.get()
        telefono = entry_telefono.get()

        conexion = conectar_bd()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute(
                    "call REGISTRO(:username, :dni, :name, :institution, :salario, :direccion, :correo, :telefono)",
                    (
                        username,
                        dni,
                        nombre,
                        institution,
                        salario,
                        direccion,
                        correo,
                        telefono,
                    ),
                )
                conexion.commit()
                cursor.close()
                cerrar_bd(conexion)
                messagebox.showinfo(
                    "Registro exitoso", "¡Registro completado con éxito!"
                )
            except Exception as ex:
                cerrar_bd(conexion)
                messagebox.showerror("Error", "Error al insertar datos: " + str(ex))

        ventana_registro.destroy()
        mostrar_ventana_inicio()

    label_nombres = tk.Label(ventana_registro, text="Nombres y Apellidos:")
    label_nombres.pack()
    entry_nombres = tk.Entry(ventana_registro)
    entry_nombres.pack()

    label_institucion = tk.Label(ventana_registro, text="Institución:")
    label_institucion.pack()
    opciones_institucion = ["Ejército", "Marina", "Fuerza Aérea", "Policía"]
    selected_institucion = tk.StringVar(ventana_registro)
    selected_institucion.set(opciones_institucion[0])
    combobox_institucion = ttk.Combobox(
        ventana_registro,
        textvariable=selected_institucion,
        values=opciones_institucion,
        state="readonly",
    )
    combobox_institucion.pack()

    label_username = tk.Label(ventana_registro, text="Username:")
    label_username.pack()
    entry_username = tk.Entry(ventana_registro, state=tk.DISABLED)
    entry_username.pack()

    button_generate = tk.Button(
        ventana_registro, text="Generar Username", command=generar_username
    )
    button_generate.pack()

    label_dni = tk.Label(ventana_registro, text="DNI:")
    label_dni.pack()
    entry_dni = tk.Entry(ventana_registro, show="*")
    entry_dni.pack()

    label_salario = tk.Label(ventana_registro, text="Salario: ")
    label_salario.pack()
    entry_salario = tk.Entry(ventana_registro)
    entry_salario.pack()

    label_direccion = tk.Label(ventana_registro, text="Dirección: ")
    label_direccion.pack()
    entry_direccion = tk.Entry(ventana_registro)
    entry_direccion.pack()

    label_correo = tk.Label(ventana_registro, text="Correo: ")
    label_correo.pack()
    entry_correo = tk.Entry(ventana_registro)
    entry_correo.pack()

    label_telefono = tk.Label(ventana_registro, text="Teléfono: ")
    label_telefono.pack()
    entry_telefono = tk.Entry(ventana_registro)
    entry_telefono.pack()

    button_registrar = tk.Button(
        ventana_registro, text="Registrarse", command=insertar_datos
    )
    button_registrar.pack(pady=20)

    button_regresar = tk.Button(
        ventana_registro, text="Regresar a Inicio", command=regresar_a_inicio
    )
    button_regresar.pack()

    ventana_registro.mainloop()


def mostrar_ventana_inicio():
    ventana_inicio.deiconify()


ventana_inicio = tk.Tk()
ventana_inicio.title("Inicio")
center_window(ventana_inicio, 300, 150)
ventana_inicio.configure(bg="white")

button_iniciar_sesion = tk.Button(
    ventana_inicio, text="Iniciar sesión", command=iniciar_sesion
)
button_iniciar_sesion.pack(pady=20)

button_registrarse = tk.Button(ventana_inicio, text="Registrarse", command=registrarse)
button_registrarse.pack(pady=20)

ventana_inicio.mainloop()
