#######################################################
#	Proyecto Software 2018/19 - UNIZAR
#	Bookalo
#	11 de Marzo de 2019
#######################################################
#	AUTORES:
#	Palacios Gracia, Ignacio (739359)
#	Ubide Alaiz, David (736520)
#	Torres Sanchez, Enrique (734980)
#######################################################

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime
from enum import Enum
# 	'''
# 	Tag :
# 		nombre_tag : String
# 	'''


class Tag(models.Model):
    nombre = models.CharField(
        max_length=50,
        verbose_name='Nombre del tag')

# 	'''
# 	EleccionEstadoProducto :
# 		tag = valor : 	Enumeración de los distintos posibles estados de un
#						producto.
# 	'''
class EleccionEstadoProducto(Enum):
	nuevo = "Nuevo"
	semi_nuevo = "Semi-nuevo"
	usado = "Usado"
	antiguo = "Antigüedad"
	roto = "Roto"
	desgastado = "Desgastado"

# 	'''
# 	Producto :
# 		vendido_por : 	FK String
# 		latitud:		real
# 		longitud:		real
# 		nombre:			String
# 		precio:			String (Integer guardado como Char)
# 		estado_venta:	String (Únicamente Vendido,Reservado o en venta)
# 		tipo_envio:		String (TODO: Qué es)
# 		tiene_tags:		Tabla relación entre tags y producto. Asocia a
# 						cada producto una serie de tags creados previamente.
# 	'''

class Producto(models.Model):
    vendido_por = models.ForeignKey(
        to=User,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Usuario que ha puesto a la venta el producto')
    latitud = models.DecimalField(
        verbose_name='Latitud del producto',
        max_digits=9,
        decimal_places=6)
    longitud = models.DecimalField(
        verbose_name='Longitud del producto',
        max_digits=9,
        decimal_places=6)
    nombre = models.CharField(
        max_length=50,
        verbose_name='Nombre del producto')
    precio = models.CharField(
        max_length=10,
        verbose_name='Precio del producto')
    estado_producto = models.CharField(
        max_length=50,
		choices=[(tag, tag.value) for tag in EleccionEstadoProducto],
        verbose_name='Estado en el que se encuentra el producto: Vendido, Reservado o En Venta')
    tipo_envio = models.CharField(
        max_length=50,
        verbose_name='Si el usuario que ha colgado el producto esta dispuestos a enviar a domicilio o no')
    descripcion = models.CharField(
        max_length=1000,
        verbose_name='Descripcion asociada al producto')
    tiene_tags = models.ManyToManyField(
        Tag,
        blank=True,
        editable=True,
        related_name='tiene_tags')

# 	'''
# 	Chat :
# 		vendedor:	String 	(PK de usuario)
# 		comprador:	String 	(PK de usuario)
# 		producto:	String	(PK de usuario)
# 	'''
#


class Chat(models.Model):
    vendedor = models.ForeignKey(
        to=User,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Usuario que ha puesto a la venta el producto',
        related_name='vendedor')
    comprador = models.ForeignKey(
        to=User,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Usuario que esta interesado en el producto',
        related_name='comprador')
    producto = models.ForeignKey(
        to=Producto,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Producto al que esta asociado el chat')

# 	'''
# 	Mensaje :
# 		texto:			String
# 		hora:			Date
# 		Chat_asociado:	ID	(PK de Chat)
# 	'''
#


class Mensaje(models.Model):
    texto = models.CharField(
        max_length=1000,
        verbose_name='Contenido del mensaje')
    hora = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Hora en la que se envio el mensaje')
    chat_asociado = models.ForeignKey(
        to=Chat,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Chat en el que se encuentra el mensaje')

# 	'''
# 	Report :
# 		identificador:		Integer
# 		Usuario_reportado:	String (PK de usuario)
# 		Causa:				String
# 	'''
#


class Report(models.Model):
    identificador = models.IntegerField(
        unique=True,
        verbose_name='Identificador unico del report')
    usuario_reportado = models.ForeignKey(
        to=User,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Usuario que ha sido reportado')
    causa = models.CharField(
        max_length=1000,
        verbose_name='Causa del reporte')

# 	'''
# 	Validación producto :
# 		Comentario:			String
# 		Usuario_reportado:	String (PK de usuario)
# 	'''
#


class ValidacionProducto(models.Model):
    comentario = models.CharField(
        max_length=1000,
        verbose_name='Comentario de la validacion')
    usuario_valorado = models.ForeignKey(
        to=User,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Usuario que ha sido valorado')
    usuario_que_valora = models.ForeignKey(
        to=User,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Usuario que ha valorado al otro usuario')
# 	'''
# 	Validación estrella :
# 		estrellas:			Integer
# 		usuario_valorado:	String (PK de usuario)
# 	'''
#


class ValidacionEstrella(models.Model):
    estrellas = models.IntegerField(
        verbose_name='Numero de estrellas que ha recibido')
    usuario_valorado = models.ForeignKey(
        to=User,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Usuario que ha sido valorado')
    usuario_que_valora = models.ForeignKey(
        to=User,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Usuario que ha valorado al otro usuario')
# 	'''
# 	Validación estrella :
# 		Contenido:	String (Indica el path del archivo)
# 		producto:	Integer (PK de producto)
# 	'''
#


class ContenidoMultimedia(models.Model):
    contenido = models.FileField()
    producto = models.ForeignKey(
        to=Producto,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Producto al que pertenece el cotenido multimedia')
