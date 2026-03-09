class Libro:
    """
    Clase que representa un libro en la biblioteca.
    Utiliza una tupla para almacenar el título y el autor (inmutables).
    """

    def __init__(self, isbn, titulo, autor, categoria):
        self.isbn = isbn
        self.categoria = categoria
        self.disponible = True  # Estado inicial del libro

        # REQUISITO: Utilizar una tupla para título y autor
        self.informacion = (titulo, autor)

    @property
    def titulo(self):
        return self.informacion[0]

    @property
    def autor(self):
        return self.informacion[1]

    def __str__(self):
        return f"[{self.isbn}] '{self.titulo}' por {self.autor} ({self.categoria})"


class Usuario:
    """
    Clase que representa a un usuario de la biblioteca.
    Utiliza una lista para almacenar los libros prestados.
    """

    def __init__(self, id_usuario, nombre):
        self.id_usuario = id_usuario
        self.nombre = nombre
        # REQUISITO: Lista para gestionar los libros prestados
        self.libros_prestados = []

    def __str__(self):
        return f"Usuario: {self.nombre} (ID: {self.id_usuario})"


class Biblioteca:
    """
    Clase principal que gestiona la biblioteca.
    Utiliza un diccionario para el catálogo (ISBN -> Libro).
    Utiliza un conjunto para validar IDs de usuarios únicos.
    """

    def __init__(self):
        # REQUISITO: Diccionario para libros con ISBN como clave (búsqueda eficiente)
        self.catalogo = {}
        # REQUISITO: Conjunto para IDs de usuarios únicos
        self.usuarios_ids = set()
        # Diccionario auxiliar para acceder a los objetos Usuario por ID
        self.usuarios = {}

    # --- Gestión de Libros ---

    def agregar_libro(self, libro):
        """Añade un libro al catálogo si no existe."""
        if libro.isbn in self.catalogo:
            print(f"❌ Error: El libro con ISBN {libro.isbn} ya existe.")
            return False

        self.catalogo[libro.isbn] = libro
        print(f"✅ Libro '{libro.titulo}' añadido correctamente.")
        return True

    def quitar_libro(self, isbn):
        """Elimina un libro del catálogo."""
        if isbn not in self.catalogo:
            print(f"❌ Error: No se encontró el libro con ISBN {isbn}.")
            return False

        libro = self.catalogo[isbn]
        if not libro.disponible:
            print(f"❌ Error: No se puede eliminar el libro '{libro.titulo}' porque está prestado.")
            return False

        del self.catalogo[isbn]
        print(f"✅ Libro '{libro.titulo}' eliminado del catálogo.")
        return True

    # --- Gestión de Usuarios ---

    def registrar_usuario(self, usuario):
        """Registra un nuevo usuario si su ID es único."""
        # REQUISITO: Validar unicidad usando el conjunto (set)
        if usuario.id_usuario in self.usuarios_ids:
            print(f"❌ Error: El ID de usuario {usuario.id_usuario} ya está registrado.")
            return False

        self.usuarios_ids.add(usuario.id_usuario)
        self.usuarios[usuario.id_usuario] = usuario
        print(f"✅ Usuario '{usuario.nombre}' registrado correctamente.")
        return True

    def dar_baja_usuario(self, id_usuario):
        """Da de baja a un usuario si no tiene libros prestados."""
        if id_usuario not in self.usuarios_ids:
            print(f"❌ Error: Usuario con ID {id_usuario} no encontrado.")
            return False

        usuario = self.usuarios[id_usuario]
        if usuario.libros_prestados:
            print(f"❌ Error: No se puede dar de baja a {usuario.nombre}. Tiene libros prestados.")
            return False

        # CORRECCIÓN: Usar .remove() para conjuntos, no del []
        self.usuarios_ids.remove(id_usuario)
        del self.usuarios[id_usuario]
        print(f"✅ Usuario '{usuario.nombre}' dado de baja.")
        return True

    # --- Préstamos y Devoluciones ---

    def prestar_libro(self, isbn, id_usuario):
        """Presta un libro a un usuario."""
        if isbn not in self.catalogo:
            print(f"❌ Error: Libro con ISBN {isbn} no encontrado.")
            return False

        if id_usuario not in self.usuarios_ids:
            print(f"❌ Error: Usuario con ID {id_usuario} no registrado.")
            return False

        libro = self.catalogo[isbn]
        usuario = self.usuarios[id_usuario]

        if not libro.disponible:
            print(f"❌ Error: El libro '{libro.titulo}' ya está prestado.")
            return False

        # Realizar préstamo
        libro.disponible = False
        usuario.libros_prestados.append(libro)
        print(f"✅ Libro '{libro.titulo}' prestado a {usuario.nombre}.")
        return True

    def devolver_libro(self, isbn, id_usuario):
        """Devuelve un libro prestado."""
        if id_usuario not in self.usuarios_ids:
            print(f"❌ Error: Usuario no encontrado.")
            return False

        usuario = self.usuarios[id_usuario]

        # Buscar el libro en la lista del usuario
        libro_encontrado = None
        for libro in usuario.libros_prestados:
            if libro.isbn == isbn:
                libro_encontrado = libro
                break

        if not libro_encontrado:
            print(f"❌ Error: El usuario no tiene el libro con ISBN {isbn} prestado.")
            return False

        # Realizar devolución
        libro_encontrado.disponible = True
        usuario.libros_prestados.remove(libro_encontrado)
        print(f"✅ Libro '{libro_encontrado.titulo}' devuelto correctamente.")
        return True

    # --- Búsquedas ---

    def buscar_libros(self, termino, tipo="titulo"):
        """
        Busca libros por título, autor o categoría.
        tipo: 'titulo', 'autor', 'categoria'
        """
        resultados = []
        termino = termino.lower()

        for libro in self.catalogo.values():
            encontrado = False
            if tipo == "titulo" and termino in libro.titulo.lower():
                encontrado = True
            elif tipo == "autor" and termino in libro.autor.lower():
                encontrado = True
            elif tipo == "categoria" and termino in libro.categoria.lower():
                encontrado = True

            if encontrado:
                resultados.append(libro)

        if not resultados:
            print("❌ No se encontraron libros con esos criterios.")
        else:
            print(f"\n📚 Resultados de búsqueda ({tipo}):")
            for libro in resultados:
                print(f"  - {libro}")
        return resultados

    # --- Listado ---

    def listar_libros_prestados(self, id_usuario):
        """Muestra todos los libros prestados a un usuario específico."""
        if id_usuario not in self.usuarios_ids:
            print(f"❌ Error: Usuario no encontrado.")
            return

        usuario = self.usuarios[id_usuario]
        if not usuario.libros_prestados:
            print(f"ℹ️ El usuario {usuario.nombre} no tiene libros prestados.")
        else:
            print(f"\n📖 Libros prestados a {usuario.nombre}:")
            for libro in usuario.libros_prestados:
                print(f"  - {libro}")

    def listar_todos_libros(self):
        """Muestra todos los libros del catálogo."""
        if not self.catalogo:
            print("ℹ️ No hay libros en el catálogo.")
        else:
            print(f"\n📚 Catálogo completo ({len(self.catalogo)} libros):")
            for libro in self.catalogo.values():
                estado = "✅ Disponible" if libro.disponible else "❌ Prestado"
                print(f"  - {libro} [{estado}]")

    def listar_todos_usuarios(self):
        """Muestra todos los usuarios registrados."""
        if not self.usuarios_ids:
            print("ℹ️ No hay usuarios registrados.")
        else:
            print(f"\n👥 Usuarios registrados ({len(self.usuarios_ids)}):")
            for id_usuario in self.usuarios_ids:
                usuario = self.usuarios[id_usuario]
                print(f"  - {usuario}")


# ==========================================
# SISTEMA DE MENÚ INTERACTIVO
# ==========================================
def mostrar_menu():
    """Muestra el menú principal de opciones."""
    print("\n" + "=" * 50)
    print("📚 SISTEMA DE GESTIÓN DE BIBLIOTECA DIGITAL 📚")
    print("=" * 50)
    print("1. Registrar Usuario")
    print("2. Dar de Baja Usuario")
    print("3. Añadir Libro")
    print("4. Eliminar Libro")
    print("5. Prestar Libro")
    print("6. Devolver Libro")
    print("7. Buscar Libro")
    print("8. Listar Libros Prestados (por usuario)")
    print("9. Listar Todos los Libros")
    print("10. Listar Todos los Usuarios")
    print("0. Salir")
    print("=" * 50)


def obtener_id_usuario(biblioteca):
    """Solicita y valida un ID de usuario."""
    while True:
        id_usuario = input("Ingrese ID de usuario: ").strip()
        if id_usuario in biblioteca.usuarios_ids:
            return id_usuario
        else:
            print("❌ Usuario no encontrado. Intente de nuevo.")


def obtener_isbn_libro(biblioteca):
    """Solicita y valida un ISBN de libro."""
    while True:
        isbn = input("Ingrese ISBN del libro: ").strip()
        if isbn in biblioteca.catalogo:
            return isbn
        else:
            print("❌ Libro no encontrado. Intente de nuevo.")


def main():
    """Función principal que ejecuta el sistema interactivo."""
    mi_biblioteca = Biblioteca()

    print("🎉 Bienvenido al Sistema de Gestión de Biblioteca Digital!")
    print("💡 Puede ingresar datos manualmente o usar el menú interactivo.\n")

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (0-10): ").strip()

        if opcion == "1":
            # Registrar Usuario
            id_usuario = input("Ingrese ID de usuario único: ").strip()
            nombre = input("Ingrese nombre del usuario: ").strip()
            usuario = Usuario(id_usuario, nombre)
            mi_biblioteca.registrar_usuario(usuario)

        elif opcion == "2":
            # Dar de Baja Usuario
            id_usuario = input("Ingrese ID de usuario a dar de baja: ").strip()
            mi_biblioteca.dar_baja_usuario(id_usuario)

        elif opcion == "3":
            # Añadir Libro
            isbn = input("Ingrese ISBN del libro: ").strip()
            titulo = input("Ingrese título del libro: ").strip()
            autor = input("Ingrese autor del libro: ").strip()
            categoria = input("Ingrese categoría del libro: ").strip()
            libro = Libro(isbn, titulo, autor, categoria)
            mi_biblioteca.agregar_libro(libro)

        elif opcion == "4":
            # Eliminar Libro
            isbn = input("Ingrese ISBN del libro a eliminar: ").strip()
            mi_biblioteca.quitar_libro(isbn)

        elif opcion == "5":
            # Prestar Libro
            isbn = obtener_isbn_libro(mi_biblioteca)
            id_usuario = obtener_id_usuario(mi_biblioteca)
            mi_biblioteca.prestar_libro(isbn, id_usuario)

        elif opcion == "6":
            # Devolver Libro
            isbn = obtener_isbn_libro(mi_biblioteca)
            id_usuario = obtener_id_usuario(mi_biblioteca)
            mi_biblioteca.devolver_libro(isbn, id_usuario)

        elif opcion == "7":
            # Buscar Libro
            print("\nTipo de búsqueda:")
            print("1. Por Título")
            print("2. Por Autor")
            print("3. Por Categoría")
            tipo_opcion = input("Seleccione (1-3): ").strip()
            tipo_busqueda = "titulo" if tipo_opcion == "1" else "autor" if tipo_opcion == "2" else "categoria"
            termino = input("Ingrese término de búsqueda: ").strip()
            mi_biblioteca.buscar_libros(termino, tipo_busqueda)

        elif opcion == "8":
            # Listar Libros Prestados
            id_usuario = obtener_id_usuario(mi_biblioteca)
            mi_biblioteca.listar_libros_prestados(id_usuario)

        elif opcion == "9":
            # Listar Todos los Libros
            mi_biblioteca.listar_todos_libros()

        elif opcion == "10":
            # Listar Todos los Usuarios
            mi_biblioteca.listar_todos_usuarios()

        elif opcion == "0":
            print("\n👋 ¡Gracias por usar el Sistema de Biblioteca Digital!")
            print("👋 ¡Hasta luego!\n")
            break

        else:
            print("❌ Opción no válida. Por favor seleccione una opción del 0 al 10.")


# Ejecutar el sistema interactivo
if __name__ == "__main__":
    main()