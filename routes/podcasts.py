import os
from flask import Blueprint, render_template, request, redirect, flash, url_for
from db import get_db_connection

podcasts_bp = Blueprint('podcasts', __name__)

@podcasts_bp.route('/agregar_podcast', methods=['GET', 'POST'])
def agregar_podcast():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        enlace = request.form['enlace']
        fecha = request.form['fecha']
        imagen = request.files['imagen']

        if imagen:
            imagen_path = os.path.join('static', 'imagenes_de_podcasts', imagen.filename)
            imagen.save(imagen_path)

        try:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO podcasts (titulo, descripcion, enlace, fecha, imagen) VALUES (?, ?, ?, ?, ?)",
                (titulo, descripcion, enlace, fecha, imagen.filename)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error al agregar el podcast: {e}")
            flash("Hubo un problema al guardar el podcast.")
            return redirect(url_for('podcasts.agregar_podcast'))

        return redirect(url_for('podcasts.ver_podcasts'))

    return render_template('agregar_podcast.html')


@podcasts_bp.route('/podcasts')
def ver_podcasts():
    try:
        conn = get_db_connection()
        podcasts = conn.execute("SELECT * FROM podcasts ORDER BY id DESC").fetchall()
        conn.close()
    except Exception as e:
        print(f"Error al obtener los podcasts: {e}")
        podcasts = []

    return render_template('podcasts.html', podcasts=podcasts)
