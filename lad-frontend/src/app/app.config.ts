import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';

// Imports pour l'intercepteur
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { authInterceptor } from './core/interceptors/auth-interceptor';

export const config: ApplicationConfig = {
  providers: [
    provideRouter(routes),

    // Cette ligne doit être exactement comme ça
    provideHttpClient(withInterceptors([authInterceptor]))
  ]
};