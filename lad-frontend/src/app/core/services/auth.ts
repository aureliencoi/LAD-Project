import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private backendUrl = 'http://127.0.0.1:8000'; // L'URL de notre API FastAPI

  constructor(private http: HttpClient) { }

  login(username: string, password: string): Observable<any> {
    const headers = new HttpHeaders({ 'Content-Type': 'application/x-www-form-urlencoded' });
    const body = new URLSearchParams();
    body.set('username', username);
    body.set('password', password);

    return this.http.post(`${this.backendUrl}/auth/token`, body.toString(), { headers })
      .pipe(
        tap((response: any) => {
          // Quand la connexion réussit, on stocke le token dans le localStorage du navigateur
          if (response.access_token) {
            localStorage.setItem('access_token', response.access_token);
          }
        })
      );
  }

  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  isLoggedIn(): boolean {
    return this.getToken() !== null;
  }
}