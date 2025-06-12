import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core'; // Important pour l'injection dans un guard fonctionnel
import { AuthService } from '../services/auth';

export const authGuard: CanActivateFn = (route, state) => {
  
  // On utilise 'inject' pour récupérer nos services
  const authService = inject(AuthService);
  const router = inject(Router);

  if (authService.isLoggedIn()) {
    // Si l'utilisateur est connecté (il a un token), on autorise la navigation
    return true; 
  } else {
    // Si l'utilisateur n'est pas connecté, on le redirige vers la page de login
    router.navigate(['/login']);
    // Et on bloque la navigation vers la page protégée
    return false;
  }
};