# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ListaTareas(models.Model):
    _name = 'lista_tareas.lista_tareas'
    _description = 'Lista de tareas'

    tarea = fields.Char(string='Tarea', required=True)
    prioridad = fields.Integer(string='Prioridad')
    urgente = fields.Boolean(
        string='Urgente',
        compute='_value_urgente',
        store=True
    )
    realizada = fields.Boolean(string='Realizada')
    asignado_a = fields.Many2one('res.users', string='Asignado a', default=lambda self: self.env.user)
    
    # Nuevos campos de fecha
    fecha_limite = fields.Date(string='Fecha límite para completar la tarea')
    fecha_creacion = fields.Date(string='Fecha de creación', default=fields.Date.today)
    
    # Campo computado retrasada
    retrasada = fields.Boolean(
        string='Retrasada',
        compute='_value_retrasada',
        store=True
    )

    # --- PARTE 1: Campo de Estado ---
    estado = fields.Selection([
        ('nuevo', 'Nueva'),
        ('progreso', 'En curso'),
        ('bloqueado', 'Bloqueada'),
        ('hecho', 'Hecha')
    ], string='Estado', default='nuevo', required=True)

    @api.depends('prioridad')
    def _value_urgente(self):
        for record in self:
            record.urgente = record.prioridad > 10

    @api.depends('fecha_limite', 'realizada')
    def _value_retrasada(self):
        hoy = fields.Date.today()
        for record in self:
            if not record.fecha_limite:
                record.retrasada = False
            else:
                record.retrasada = not record.realizada and record.fecha_limite < hoy

    # --- PARTE 2: Métodos para los botones ---
    def action_nuevo(self):
        self.estado = 'nuevo'
        self.realizada = False

    def action_progreso(self):
        self.estado = 'progreso'
        self.realizada = False

    def action_bloqueado(self):
        self.estado = 'bloqueado'
        # No cambiamos realizada aquí, depende del contexto, pero generalmente sigue False

    def action_hecho(self):
        self.estado = 'hecho'
        self.realizada = True