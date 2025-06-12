import { Component } from '@angular/core';
import { Router } from '@angular/router';
// --- CORRECTION ---
// On importe depuis 'auth' au lieu de 'auth.service'
import { AuthService } from '../../core/services/auth'; 

import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    FormsModule,
    CommonModule
  ],
  templateUrl: './login.html',
  styleUrl: './login.scss'
})
export class Login {
  username = '';
  password = '';
  errorMessage = '';

  constructor(
    // Cette injection est maintenant correcte car l'import est bon
    private authService: AuthService, 
    private router: Router
  ) {}

  onSubmit(): void {
    this.authService.login(this.username, this.password).subscribe({
      next: () => {
        this.router.navigate(['/home']);
      },
      // --- CORRECTION ---
      // On ajoute le type 'any' au paramètre 'err'
      error: (err: any) => { 
        this.errorMessage = 'Erreur de connexion. Vérifiez vos identifiants.';
        console.error(err);
      }
    });
  }
}