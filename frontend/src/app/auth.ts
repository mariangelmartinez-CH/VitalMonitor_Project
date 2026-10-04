import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { tap } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class Auth {
  private http = inject(HttpClient);
  private readonly url = 'http://127.0.0.1:8000/api';

  login(correo: string, contrasena: string) {
    return this.http
      .post<{ token: string }>(`${this.url}/login`, { correo, contrasena })
      .pipe(tap((respuesta) => localStorage.setItem('token', respuesta.token)));
  }

  registrar(correo: string, contrasena: string) {
    return this.http.post(`${this.url}/registro`, { correo, contrasena });
  }

  get token() {
    return localStorage.getItem('token');
  }

  cerrarSesion() {
    localStorage.removeItem('token');
  }
}
