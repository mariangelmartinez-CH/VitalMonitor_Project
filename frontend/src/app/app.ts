import { Component, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  private http = inject(HttpClient);
  protected readonly mensaje = signal('Conectando con el backend...');

  constructor() {
    this.http
      .get<{ estado: string; mensaje: string }>('http://127.0.0.1:8000/api/salud')
      .subscribe({
        next: (respuesta) => this.mensaje.set(respuesta.mensaje),
        error: () => this.mensaje.set('No se pudo conectar con el backend'),
      });
  }
}
