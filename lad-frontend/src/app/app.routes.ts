import { Routes } from '@angular/router';

import { Login } from './pages/login/login'; 
import { Home } from './pages/home/home'; 
import { Settings } from './pages/settings/settings';
import { MediaDetail } from './pages/media-detail/media-detail'; // <-- AJOUTER
import { authGuard } from './core/guards/auth-guard';

export const routes: Routes = [
    { path: 'login', component: Login }, 
    { path: 'home', component: Home, canActivate: [authGuard] },
    { path: 'settings', component: Settings, canActivate: [authGuard] },
    
    // --- NOUVELLES ROUTES DYNAMIQUES ---
    // Le ':type' nous dira si c'est un 'movie' ou une 'series'
    // Le ':id' sera l'identifiant du média
    { path: ':type/:id', component: MediaDetail, canActivate: [authGuard] },
    
    { path: '', redirectTo: '/home', pathMatch: 'full' },
    { path: '**', redirectTo: '/home' }
];