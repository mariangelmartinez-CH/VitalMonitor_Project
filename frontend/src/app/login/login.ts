import { HttpErrorResponse } from '@angular/common/http';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Auth } from '../auth';

@Component({
  selector: 'app-login',
  imports: [FormsModule],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  private auth = inject(Auth);

  correo = '';
  contrasena = '';
  mensaje = signal('');

  entrar() {
    this.auth.login(this.correo, this.contrasena).subscribe({
      next: () => this.mensaje.set('Sesion iniciada'),
      error: (e: HttpErrorResponse) => {
        const detalle = e.error?.detail;
        this.mensaje.set(
          typeof detalle === 'string' ? detalle : 'No se pudo iniciar sesion, revisa los datos',
        );
      },
    });
  }
}
