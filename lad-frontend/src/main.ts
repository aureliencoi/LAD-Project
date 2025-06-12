import { bootstrapApplication } from '@angular/platform-browser';

// --- CORRECTION ---
// On importe 'config' au lieu de 'appConfig'
import { config } from './app/app.config'; 
import { App } from './app/app';

// Et on utilise 'config' ici
bootstrapApplication(App, config) 
  .catch((err) => console.error(err));